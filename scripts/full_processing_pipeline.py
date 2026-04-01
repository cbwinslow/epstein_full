#!/usr/bin/env python3
"""
Full Processing Pipeline - Scale to Epstein Dataset

Processes all PDF files using PyMuPDF for OCR and spaCy for entity extraction.
Integrates results with existing knowledge graph and databases.
"""

import concurrent.futures
import json
import os
import time
from collections import defaultdict

import fitz
import spacy
from tqdm import tqdm


class EpsteinProcessingPipeline:
    def __init__(self):
        self.nlp = None
        self.processed_dir = '/home/cbwinslow/workspace/epstein/processed/'
        self.pg_conn = None

        # Create processed directory
        os.makedirs(self.processed_dir, exist_ok=True)

        # Statistics
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'total_chars': 0,
            'total_entities': 0,
            'entity_type_counts': defaultdict(int),
            'processing_times': []
        }

    def load_models(self):
        """Load spaCy model."""
        try:
            self.nlp = spacy.load('en_core_web_sm')
            print("✓ spaCy model loaded successfully")
            return True
        except Exception as e:
            print(f"✗ spaCy model error: {e}")
            return False

    def process_single_pdf(self, pdf_path):
        """Process a single PDF file."""
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

            # Run NER
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

            return {
                'filename': os.path.basename(pdf_path),
                'char_count': len(text),
                'page_count': page_count,
                'entities': entities,
                'sample_text': text[:1000] if text else ""
            }

        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return None

    def process_dataset(self, dataset_num, max_files=None):
        """Process all files in a dataset."""
        pdf_dir = f'/mnt/data/epstein-project/raw-files/data{dataset_num}/'

        if not os.path.exists(pdf_dir):
            print(f"Dataset {dataset_num} directory not found: {pdf_dir}")
            return

        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

        if max_files:
            pdf_files = pdf_files[:max_files]

        print(f"\\nProcessing Dataset {dataset_num}: {len(pdf_files)} files")

        results = []
        file_paths = [os.path.join(pdf_dir, f) for f in pdf_files]

        # Process files with progress bar
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(self.process_single_pdf, path): path for path in file_paths}

            for future in tqdm(concurrent.futures.as_completed(future_to_file),
                             total=len(file_paths), desc=f"DS{dataset_num}"):
                result = future.result()
                if result:
                    results.append(result)
                    self.update_stats(result)

        # Save results
        output_file = os.path.join(self.processed_dir, f'dataset_{dataset_num}_results.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✓ Dataset {dataset_num} complete: {len(results)} files processed")
        return results

    def update_stats(self, result):
        """Update processing statistics."""
        self.stats['processed_files'] += 1
        self.stats['total_chars'] += result['char_count']
        self.stats['total_entities'] += len(result['entities'])

        for entity in result['entities']:
            self.stats['entity_type_counts'][entity['label']] += 1

    def integrate_with_knowledge_graph(self, results):
        """Integrate new entities with existing knowledge graph."""
        if not os.path.exists(self.kg_db):
            print("Knowledge graph database not found, skipping integration")
            return

        conn = sqlite3.connect(self.kg_db)

        # Create temporary table for new entities
        conn.execute('''
            CREATE TEMP TABLE temp_entities (
                text TEXT,
                label TEXT,
                frequency INTEGER
            )
        ''')

        # Count entity frequencies
        entity_freq = defaultdict(int)
        for result in results:
            for entity in result['entities']:
                if entity['label'] == 'PERSON':
                    entity_freq[entity['text']] += 1

        # Insert into temp table
        for entity_text, freq in entity_freq.items():
            conn.execute(
                "INSERT INTO temp_entities (text, label, frequency) VALUES (?, ?, ?)",
                (entity_text, 'PERSON', freq)
            )

        # Update existing entities or insert new ones
        conn.execute('''
            INSERT OR IGNORE INTO entities (name, entity_type, metadata)
            SELECT text, 'person', json_object('frequency', frequency)
            FROM temp_entities
            WHERE label = 'PERSON'
        ''')

        conn.commit()
        conn.close()

        print(f"✓ Integrated {len(entity_freq)} new entities with knowledge graph")

    def generate_report(self):
        """Generate processing report."""
        print("\\n" + "="*60)
        print("EPSTEIN FILES PROCESSING REPORT")
        print("="*60)

        print(f"\\nFiles processed: {self.stats['processed_files']:,}")
        print(f"Total characters: {self.stats['total_chars']:,}")
        print(f"Total entities: {self.stats['total_entities']:,}")
        if self.stats['processing_times']:
            avg_time = sum(self.stats['processing_times'])/len(self.stats['processing_times'])
            print(f"Average processing time: {avg_time:.3f}s")
        else:
            print("Average processing time: N/A (no timing data)")

        print("\\nEntity Type Distribution:")
        for entity_type, count in sorted(self.stats['entity_type_counts'].items()):
            print(f"  {entity_type:10s}: {count:6d}")

        # Save report
        report_file = os.path.join(self.processed_dir, 'processing_report.json')
        with open(report_file, 'w') as f:
            json.dump(dict(self.stats), f, indent=2, default=str)

        print(f"\\nReport saved to: {report_file}")

    def run_full_pipeline(self, datasets=None, max_files_per_dataset=None):
        """Run the full processing pipeline."""
        print("Epstein Files - Full Processing Pipeline")
        print("="*50)

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
                self.integrate_with_knowledge_graph(results)

                print(f"Dataset {dataset} time: {end_time - start_time:.2f}s")

        self.generate_report()
        print(f"\\n✓ Pipeline complete! Processed {len(all_results)} files total.")

def main():
    """Main function."""
    pipeline = EpsteinProcessingPipeline()

    # Start with a small test batch to verify everything works
    print("Starting Epstein Files Processing Pipeline...")
    print("Testing with Dataset 9 (first 50 files)...")

    pipeline.run_full_pipeline(datasets=[9], max_files_per_dataset=50)

    print("\\nTest batch complete! Now scaling up to multiple datasets...")

    # Scale up to process more datasets
    print("\\nProcessing Datasets 9, 10, and 11 (first 100 files each)...")
    pipeline.run_full_pipeline(datasets=[9, 10, 11], max_files_per_dataset=100)

    print("\\nProcessing complete! Check the processed/ directory for results.")

if __name__ == "__main__":
    main()
