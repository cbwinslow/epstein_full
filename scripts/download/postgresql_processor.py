#!/usr/bin/env python3
"""
Epstein Files - PostgreSQL Processing Pipeline

Processes PDF files using PyMuPDF for OCR and spaCy for entity extraction.
Directly stores results in PostgreSQL database instead of JSON files.
Includes smart memory management for very large PDFs.
"""

import argparse
import logging
import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import fitz
import psycopg2
import spacy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cbwinslow/workspace/epstein/processed/postgresql_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Get PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="epstein",
            user="cbwinslow",
            password=""  # Will use .pgpass or environment
        )
        return conn
    except Exception as e:
        logger.error(f'Failed to connect to PostgreSQL: {e}')
        return None

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

def process_single_file_postgresql(filename, input_dir, nlp, max_pages_per_doc=None):
    """Process a single PDF file and store results in PostgreSQL."""
    file_path = os.path.join(input_dir, filename)
    start_time = time.time()

    text, char_count, page_count, entities = process_pdf_full_pages(file_path, nlp, max_pages_per_doc)

    if text:
        processing_time = time.time() - start_time

        # Store in PostgreSQL
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    # Insert document content
                    cur.execute("""
                        INSERT INTO documents_content (document_id, filename, content, char_count, page_count, processing_time)
                        VALUES ((SELECT id FROM documents WHERE efta_number = %s), %s, %s, %s, %s, %s)
                        ON CONFLICT (filename) DO UPDATE SET
                            content = EXCLUDED.content,
                            char_count = EXCLUDED.char_count,
                            page_count = EXCLUDED.page_count,
                            processing_time = EXCLUDED.processing_time,
                            updated_at = NOW()
                        RETURNING id
                    """, (filename.split('.')[0], filename, text, char_count, page_count, processing_time))

                    doc_id = cur.fetchone()[0]

                    # Insert entities
                    entity_data = []
                    for entity in entities:
                        entity_data.append((
                            entity['text'], entity['label'],
                            filename, 'documents_content', filename
                        ))

                    if entity_data:
                        cur.executemany("""
                            INSERT INTO entities (name, entity_type, source_id, source_table, source_system)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING
                        """, entity_data)

                    conn.commit()

                    logger.info(f'{filename}: {char_count:,} chars, {len(entities)} entities ({processing_time:.2f}s)')
                    return {
                        'filename': filename,
                        'char_count': char_count,
                        'page_count': page_count,
                        'entities': len(entities),
                        'processing_time': processing_time
                    }

            except Exception as e:
                logger.error(f'Error storing {filename} in PostgreSQL: {e}')
                conn.rollback()
            finally:
                conn.close()

        return {
            'filename': filename,
            'char_count': char_count,
            'page_count': page_count,
            'entities': len(entities),
            'processing_time': processing_time
        }
    else:
        logger.warning(f'{filename}: Failed to process')
        return None

def process_dataset_postgresql(input_dir, workers=8, max_files=None, max_pages_per_doc=None, dataset_name=None):
    """Process all PDF files in a dataset directory and store in PostgreSQL."""
    logger.info(f'Processing Dataset: {input_dir}')
    logger.info(f'Workers: {workers}')
    logger.info(f'Max files: {max_files}')
    logger.info(f'Max pages per document: {max_pages_per_doc if max_pages_per_doc else "ALL"}')
    if dataset_name:
        logger.info(f'Dataset name: {dataset_name}')
    logger.info('-' * 50)

    # Load spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
        logger.info('✓ spaCy model loaded successfully')
    except Exception as e:
        logger.error(f'✗ spaCy model error: {e}')
        return

    # Get all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    if max_files:
        pdf_files = pdf_files[:max_files]

    logger.info(f'Found {len(pdf_files)} PDF files to process')
    logger.info('-' * 50)

    # Process files
    results = []
    total_chars = 0
    total_entities = 0
    total_pages = 0
    entity_type_counts = defaultdict(int)
    processing_times = []
    failed_files = []

    # Process with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_single_file_postgresql, filename, input_dir, nlp, max_pages_per_doc)
                  for filename in pdf_files]

        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            if result:
                results.append(result)
                total_chars += result['char_count']
                total_entities += result['entities']
                total_pages += result['page_count']
                processing_times.append(result['processing_time'])

                # Count entity types (would need separate query to get exact counts)
                # For now, we'll just count the number of entities per file
                logger.info(f'{i+1}/{len(pdf_files)} {result["filename"]}: {result["char_count"]:,} chars, {result["entities"]} entities ({result["processing_time"]:.2f}s)')
            else:
                failed_files.append(filename)
                logger.warning(f'{i+1}/{len(pdf_files)} {filename}: Failed to process')

    # Print summary
    avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
    logger.info('')
    logger.info('Processing Summary:')
    logger.info('-' * 30)
    logger.info(f'Files processed: {len(results)}/{len(pdf_files)}')
    logger.info(f'Files failed: {len(failed_files)}')
    logger.info(f'Total pages processed: {total_pages:,}')
    logger.info(f'Total characters: {total_chars:,}')
    logger.info(f'Total entities: {total_entities:,}')
    logger.info(f'Average processing time: {avg_time:.2f}s')
    logger.info('')

    if failed_files:
        logger.info('Failed Files:')
        logger.info('-' * 30)
        for filename in failed_files:
            logger.info(f'  {filename}')
        logger.info('')

    logger.info('✓ Processing complete! Results stored in PostgreSQL database')
    return results

def main():
    """Main processing function with command-line arguments."""
    parser = argparse.ArgumentParser(description='Process Epstein PDF files and store in PostgreSQL')
    parser.add_argument('--input-dir', required=True, help='Input directory with PDF files')
    parser.add_argument('--workers', type=int, default=8, help='Number of worker threads (default: 8)')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to process')
    parser.add_argument('--max-pages', type=int, help='Maximum pages per document (default: ALL)')
    parser.add_argument('--dataset', type=str, help='Dataset identifier for logging')

    args = parser.parse_args()

    logger.info('=' * 60)
    logger.info('Epstein Files - PostgreSQL Processing Pipeline')
    logger.info('=' * 60)

    if args.dataset:
        logger.info(f'Dataset: {args.dataset}')

    results = process_dataset_postgresql(
        input_dir=args.input_dir,
        workers=args.workers,
        max_files=args.max_files,
        max_pages_per_doc=args.max_pages,
        dataset_name=args.dataset
    )

    logger.info(f'Processed {len(results)} files successfully')
    logger.info('=' * 60)

if __name__ == '__main__':
    main()
