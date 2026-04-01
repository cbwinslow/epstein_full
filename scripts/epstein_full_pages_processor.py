#!/usr/bin/env python3
"""
Epstein Files - Full Pages Processing Pipeline

Processes PDF files using PyMuPDF for OCR and spaCy for entity extraction.
Processes ALL pages in each PDF (no 10-page limit).
Includes smart memory management for very large PDFs.
"""

import argparse
import json
import logging
import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import fitz
import spacy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cbwinslow/workspace/epstein/processed/processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_pdf_full_pages(pdf_path, nlp, max_pages=None):
    """Process a single PDF file - extract text from ALL pages."""
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        # Determine pages to process
        if max_pages and max_pages > 0:
            pages_to_process = min(max_pages, total_pages)
        else:
            pages_to_process = total_pages

        logger.info(f"Processing {pdf_path}: {total_pages} total pages, processing {pages_to_process}")

        text = ''
        page_texts = []

        # Process pages in chunks to manage memory
        chunk_size = 50  # Process 50 pages at a time

        for start_page in range(0, pages_to_process, chunk_size):
            end_page = min(start_page + chunk_size, pages_to_process)

            chunk_text = ''
            for page_num in range(start_page, end_page):
                try:
                    page = doc.load_page(page_num)
                    page_text = page.get_text()
                    chunk_text += page_text + "\n\n"
                except Exception as e:
                    logger.warning(f"Error processing page {page_num} in {pdf_path}: {e}")
                    continue

            page_texts.append(chunk_text)

            # Clear chunk from memory
            chunk_text = ""

            # Log progress for long documents
            if pages_to_process > 100:
                logger.info(f"  Progress: {end_page}/{pages_to_process} pages processed")

        doc.close()

        # Combine all page texts
        text = "".join(page_texts)

        if not text.strip():
            logger.warning(f"No text extracted from {pdf_path}")
            return None, 0, 0, []

        # Run NER
        doc_nlp = nlp(text)

        # Extract entities
        entities = []
        entity_counts = defaultdict(int)

        for ent in doc_nlp.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'MONEY', 'CARDINAL']:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
                entity_counts[ent.label_] += 1

        return text, len(text), pages_to_process, entities

    except Exception as e:
        logger.error(f'Error processing {pdf_path}: {e}')
        return None, 0, 0, []

class EpsteinProcessor:
    def __init__(self, input_dir, output_dir, workers=8, max_files=None, max_pages_per_doc=None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.workers = workers
        self.max_files = max_files
        self.max_pages_per_doc = max_pages_per_doc

        # Statistics tracking
        self.results = []
        self.total_chars = 0
        self.total_entities = 0
        self.total_pages = 0
        self.entity_type_counts = defaultdict(int)
        self.processing_times = []
        self.failed_files = []

        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
            logger.info('✓ spaCy model loaded successfully')
        except Exception as e:
            logger.error(f'✗ spaCy model error: {e}')
            raise

    def process_dataset(self):
        """Process all PDF files in the dataset directory."""
        logger.info(f'Processing Dataset: {self.input_dir}')
        logger.info(f'Output directory: {self.output_dir}')
        logger.info(f'Workers: {self.workers}')
        logger.info(f'Max files: {self.max_files}')
        logger.info(f'Max pages per document: {self.max_pages_per_doc if self.max_pages_per_doc else "ALL"}')
        logger.info('-' * 50)

        # Get all PDF files
        pdf_files = [f for f in os.listdir(self.input_dir) if f.endswith('.pdf')]
        if self.max_files:
            pdf_files = pdf_files[:self.max_files]

        logger.info(f'Found {len(pdf_files)} PDF files to process')
        logger.info('-' * 50)

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Process files
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(self.process_single_file, filename) for filename in pdf_files]

            for i, future in enumerate(as_completed(futures)):
                result = future.result()
                if result:
                    self.results.append(result)
                    logger.info(f'{i+1}/{len(pdf_files)} {result["filename"]}: {result["char_count"]:,} chars, {len(result["entities"])} entities ({result["processing_time"]:.2f}s)')
                else:
                    logger.warning(f'{i+1}/{len(pdf_files)} {filename}: Failed to process')

        # Save results
        output_file = os.path.join(self.output_dir, 'full_pages_results.json')
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        # Print summary
        avg_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
        logger.info('')
        logger.info('Processing Summary:')
        logger.info('-' * 30)
        logger.info(f'Files processed: {len(self.results)}/{len(pdf_files)}')
        logger.info(f'Files failed: {len(self.failed_files)}')
        logger.info(f'Total pages processed: {self.total_pages:,}')
        logger.info(f'Total characters: {self.total_chars:,}')
        logger.info(f'Total entities: {self.total_entities:,}')
        logger.info(f'Average processing time: {avg_time:.2f}s')
        logger.info('')

        logger.info('Entity Type Distribution:')
        logger.info('-' * 30)
        for entity_type, count in sorted(self.entity_type_counts.items()):
            logger.info(f'  {entity_type:10s}: {count:4d}')
        logger.info('')

        if self.failed_files:
            logger.info('Failed Files:')
            logger.info('-' * 30)
            for filename in self.failed_files:
                logger.info(f'  {filename}')
            logger.info('')

        logger.info(f'✓ Processing complete! Results saved to: {output_file}')
        return self.results

    def process_single_file(self, filename):
        """Process a single PDF file."""
        file_path = os.path.join(self.input_dir, filename)
        start_time = time.time()

        text, char_count, page_count, entities = process_pdf_full_pages(file_path, self.nlp, self.max_pages_per_doc)

        if text:
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)

            result = {
                'filename': filename,
                'char_count': char_count,
                'page_count': page_count,
                'entities': entities,
                'processing_time': processing_time
            }

            # Update statistics
            self.total_chars += char_count
            self.total_entities += len(entities)
            self.total_pages += page_count
            for entity in entities:
                self.entity_type_counts[entity['label']] += 1

            return result
        else:
            self.failed_files.append(filename)
            return None

def process_dataset_full_pages(input_dir, output_dir, workers=8, max_files=None, max_pages_per_doc=None):
    """Process all PDF files in a dataset directory with full page support."""
    processor = EpsteinProcessor(input_dir, output_dir, workers, max_files, max_pages_per_doc)
    return processor.process_dataset()

def main():
    """Main processing function with command-line arguments."""
    parser = argparse.ArgumentParser(description='Process Epstein PDF files with full page support')
    parser.add_argument('--input-dir', required=True, help='Input directory with PDF files')
    parser.add_argument('--output-dir', required=True, help='Output directory for results')
    parser.add_argument('--workers', type=int, default=8, help='Number of worker threads (default: 8)')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to process')
    parser.add_argument('--max-pages', type=int, help='Maximum pages per document (default: ALL)')
    parser.add_argument('--dataset', type=str, help='Dataset identifier for logging')

    args = parser.parse_args()

    logger.info('=' * 60)
    logger.info('Epstein Files - Full Pages Processing Pipeline')
    logger.info('=' * 60)

    if args.dataset:
        logger.info(f'Dataset: {args.dataset}')

    results = process_dataset_full_pages(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        workers=args.workers,
        max_files=args.max_files,
        max_pages_per_doc=args.max_pages
    )

    logger.info(f'Processed {len(results)} files successfully')
    logger.info('=' * 60)

if __name__ == '__main__':
    main()
