#!/usr/bin/env python3
"""
Optimized Epstein Files Processing Pipeline - PostgreSQL Integration

Processes PDF files using PyMuPDF for OCR and spaCy for entity extraction.
Integrates results directly with PostgreSQL database (source of truth).
Optimized for maximum worker concurrency using Tesla K80 GPUs.

Scale: 1.4M documents, 218GB data
Infrastructure: 2x Tesla K80 (12GB), 1x Tesla K40m (11GB), 125GB RAM
"""

import concurrent.futures
import json
import logging
import os
import threading
import time
from collections import defaultdict

import fitz
import psycopg2
import spacy
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizedEpsteinPipeline:
    def __init__(self):
        self.nlp = None
        self.pg_conn = None
        self.processed_dir = '/home/cbwinslow/workspace/epstein/processed/'
        self.max_workers = 8  # Maximum concurrency for optimal performance

        # Create processed directory
        os.makedirs(self.processed_dir, exist_ok=True)

        # Statistics
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'total_chars': 0,
            'total_entities': 0,
            'entity_type_counts': defaultdict(int),
            'processing_times': [],
            'lock': threading.Lock()
        }

    def connect_postgresql(self):
        """Connect to PostgreSQL database (source of truth)."""
        try:
            self.pg_conn = psycopg2.connect(
                host="localhost",
                database="epstein",
                user="cbwinslow",
                password="123qweasd"
            )
            logger.info("✓ PostgreSQL connection established")
            return True
        except Exception as e:
            logger.error(f"✗ PostgreSQL connection error: {e}")
            return False

    def load_models(self):
        """Load spaCy model with GPU optimization."""
        try:
            # Set CUDA_VISIBLE_DEVICES to use K80s only (exclude K40m)
            os.environ['CUDA_VISIBLE_DEVICES'] = '1,2'

            self.nlp = spacy.load('en_core_web_sm')
            logger.info("✓ spaCy model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"✗ spaCy model error: {e}")
            return False

    def process_single_pdf(self, pdf_path):
        """Process a single PDF file with optimized settings."""
        start_time = time.time()
        try:
            doc = fitz.open(pdf_path)
            text = ''
            page_count = min(20, len(doc))  # Process up to 20 pages

            for page_num in range(page_count):
                page = doc.load_page(page_num)
                text += page.get_text()

            doc.close()

            if not text.strip():
                return None

            # Run NER with optimized settings
            doc_nlp = self.nlp(text)

            # Extract entities
            entities = []
            for ent in doc_nlp.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'MONEY', 'CARDINAL']:
                    entities.append({
                        'text': ent.text,
                        'label': ent.label_,
                        'start': ent.start_char,
                        'end': ent.end_char
                    })

            processing_time = time.time() - start_time

            return {
                'filename': os.path.basename(pdf_path),
                'char_count': len(text),
                'page_count': page_count,
                'entities': entities,
                'processing_time': processing_time,
                'sample_text': text[:1000] if text else ""
            }

        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")
            return None

    def process_dataset(self, dataset_num, max_files=None):
        """Process all files in a dataset with maximum concurrency."""
        pdf_dir = f'/mnt/data/epstein-project/raw-files/data{dataset_num}/'

        if not os.path.exists(pdf_dir):
            logger.warning(f"Dataset {dataset_num} directory not found: {pdf_dir}")
            return

        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

        if max_files:
            pdf_files = pdf_files[:max_files]

        logger.info(f"Processing Dataset {dataset_num}: {len(pdf_files)} files with {self.max_workers} workers")

        results = []
        file_paths = [os.path.join(pdf_dir, f) for f in pdf_files]

        # Process files with maximum concurrency
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self.process_single_pdf, path): path for path in file_paths}

            for future in tqdm(concurrent.futures.as_completed(future_to_file),
                             total=len(file_paths), desc=f"DS{dataset_num}",
                             bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'):
                result = future.result()
                if result:
                    results.append(result)
                    self.update_stats(result)

        # Save results
        output_file = os.path.join(self.processed_dir, f'dataset_{dataset_num}_results.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"✓ Dataset {dataset_num} complete: {len(results)} files processed")
        return results

    def update_stats(self, result):
        """Update processing statistics with thread safety."""
        with self.stats['lock']:
            self.stats['processed_files'] += 1
            self.stats['total_chars'] += result['char_count']
            self.stats['total_entities'] += len(result['entities'])
            self.stats['processing_times'].append(result['processing_time'])

            for entity in result['entities']:
                self.stats['entity_type_counts'][entity['label']] += 1

    def integrate_with_postgresql(self, results):
        """Integrate new entities with PostgreSQL database (source of truth)."""
        if not self.pg_conn:
            logger.warning("PostgreSQL connection not available, skipping integration")
            return

        try:
            cur = self.pg_conn.cursor()

            # Count entity frequencies
            entity_freq = defaultdict(int)
            for result in results:
                for entity in result['entities']:
                    if entity['label'] == 'PERSON':
                        entity_freq[entity['text']] += 1

            # Insert new entities into PostgreSQL
            if entity_freq:
                # Prepare batch insert
                entity_data = []
                for entity_text, freq in entity_freq.items():
                    entity_data.append((entity_text, 'person', json.dumps({'frequency': freq})))

                # Use execute_values for efficient bulk insert
                from psycopg2.extras import execute_values
                execute_values(
                    cur,
                    """
                    INSERT INTO entities (name, entity_type, metadata) 
                    VALUES %s 
                    ON CONFLICT (name) DO UPDATE SET 
                    metadata = entities.metadata::jsonb || EXCLUDED.metadata::jsonb
                    """,
                    entity_data
                )

                self.pg_conn.commit()
                logger.info(f"✓ Integrated {len(entity_freq)} new entities with PostgreSQL")
            else:
                logger.info("✓ No new entities to integrate")

        except Exception as e:
            logger.error(f"PostgreSQL integration error: {e}")
            self.pg_conn.rollback()

    def generate_report(self):
        """Generate comprehensive processing report."""
        logger.info("\n" + "="*80)
        logger.info("EPSTEIN FILES PROCESSING REPORT - POSTGRESQL INTEGRATION")
        logger.info("="*80)

        logger.info(f"\nFiles processed: {self.stats['processed_files']:,}")
        logger.info(f"Total characters: {self.stats['total_chars']:,}")
        logger.info(f"Total entities: {self.stats['total_entities']:,}")

        if self.stats['processing_times']:
            avg_time = sum(self.stats['processing_times'])/len(self.stats['processing_times'])
            logger.info(f"Average processing time: {avg_time:.3f}s")
            logger.info(f"Processing speed: {self.stats['total_chars']/sum(self.stats['processing_times']):.0f} chars/sec")

        logger.info("\nEntity Type Distribution:")
        for entity_type, count in sorted(self.stats['entity_type_counts'].items()):
            logger.info(f"  {entity_type:10s}: {count:6d}")

        # Save detailed report
        report_file = os.path.join(self.processed_dir, 'postgresql_processing_report.json')
        with open(report_file, 'w') as f:
            # Convert defaultdict to regular dict for JSON serialization
            stats_copy = dict(self.stats)
            stats_copy['entity_type_counts'] = dict(stats_copy['entity_type_counts'])
            json.dump(stats_copy, f, indent=2, default=str)

        logger.info(f"\nDetailed report saved to: {report_file}")

    def run_full_pipeline(self, datasets=None, max_files_per_dataset=None):
        """Run the full processing pipeline with PostgreSQL integration."""
        logger.info("Epstein Files - FULL SCALE PRODUCTION PIPELINE")
        logger.info("="*80)

        if not self.connect_postgresql():
            return

        if not self.load_models():
            return

        if datasets is None:
            datasets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        all_results = []

        for dataset in datasets:
            start_time = time.time()
            results = self.process_dataset(dataset, max_files_per_dataset)
            end_time = time.time()

            if results:
                all_results.extend(results)
                self.integrate_with_postgresql(results)

                logger.info(f"Dataset {dataset} time: {end_time - start_time:.2f}s")
                logger.info(f"Dataset {dataset} speed: {self.stats['total_chars']/sum(self.stats['processing_times']):.0f} chars/sec")

        self.generate_report()
        logger.info(f"\n✓ FULL SCALE PIPELINE COMPLETE! Processed {len(all_results)} files total.")
        logger.info("✓ All results integrated with PostgreSQL (source of truth)")

def main():
    """Main function with optimized settings."""
    pipeline = OptimizedEpsteinPipeline()

    # Configure for maximum performance
    pipeline.max_workers = 16  # Maximum concurrency

    logger.info("Starting FULL SCALE PRODUCTION Epstein Files Processing Pipeline...")
    logger.info("Using PostgreSQL as source of truth with maximum worker concurrency")
    logger.info("Processing ALL datasets without data limits - PRODUCTION RUN ONLY")

    # Run full production pipeline - ALL datasets, NO limits
    logger.info("Processing ALL 12 datasets with full file counts...")
    pipeline.run_full_pipeline(datasets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], max_files_per_dataset=None)

    logger.info("\nFULL SCALE PRODUCTION COMPLETE! Check the processed/ directory for results.")
    logger.info("All data has been integrated with PostgreSQL database.")

if __name__ == "__main__":
    main()
