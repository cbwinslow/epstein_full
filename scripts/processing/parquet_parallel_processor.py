#!/usr/bin/env python3
"""
Parallel Parquet Processor with COPY bulk loading
Uses multiprocessing for I/O parallelism + PostgreSQL COPY for fast inserts
"""

import io
import json
import logging
import multiprocessing as mp
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration
DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

PG_CONFIG = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": int(os.environ.get("PG_PORT", "5432")),
    "user": os.environ.get("PG_USER", "cbwinslow"),
    "password": os.environ.get("PG_PASSWORD", "123qweasd"),
    "dbname": os.environ.get("PG_DB", "epstein"),
}

# Parallelism settings
NUM_WORKERS = min(mp.cpu_count(), 8)  # Use up to 8 cores
BATCH_SIZE = 5000  # Rows per COPY batch


def setup_logging():
    """Setup logging."""
    log_file = f"{LOG_DIR}/parquet_parallel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return log_file


def process_file_to_buffer(file_path: str) -> Tuple[str, int, io.StringIO]:
    """
    Process a single parquet file into a StringIO buffer for COPY.
    Returns (file_path, row_count, buffer).
    """
    try:
        df = pd.read_parquet(file_path)

        # Map parquet columns to table columns
        # HF parquet has: dataset_id, doc_id, file_name, text_content
        if 'text_content' not in df.columns:
            return file_path, 0, None

        df = df[df['text_content'].notna()]
        df = df[df['text_content'].str.len() > 10]

        if len(df) == 0:
            return file_path, 0, None

        # Create CSV buffer for COPY - match documents_content schema
        buffer = io.StringIO()
        for _, row in df.iterrows():
            doc_id = str(row.get('doc_id', '')).replace('\t', ' ').replace('\n', ' ')
            filename = str(row.get('file_name', '')).replace('\t', ' ').replace('\n', ' ')
            content = str(row.get('text_content', '')).replace('\t', ' ').replace('\n', ' ')
            char_count = len(content) if content else 0
            page_count = 1  # Default, could be extracted from metadata

            if doc_id and content:
                buffer.write(f"{doc_id}\t{filename}\t{content}\t{char_count}\t{page_count}\n")

        return file_path, len(df), buffer

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        return file_path, 0, None


def bulk_copy_to_postgres(files_batch: List[str], worker_id: int) -> Tuple[int, int]:
    """
    Process a batch of files using COPY.
    Returns (files_processed, rows_inserted).
    """
    conn = psycopg2.connect(**PG_CONFIG)
    files_done = 0
    total_rows = 0

    try:
        for file_path in files_batch:
            # Process file to buffer
            _, count, buffer = process_file_to_buffer(file_path)

            if buffer is None or count == 0:
                files_done += 1
                continue

            # Use COPY for fast bulk insert
            buffer.seek(0)
            with conn.cursor() as cur:
                cur.copy_from(
                    buffer,
                    'documents_content',
                    columns=('efta_number', 'text_content', 'dataset', 'source_file'),
                    sep='\t',
                    null=''
                )
                conn.commit()

            files_done += 1
            total_rows += count

            if files_done % 10 == 0:
                logging.info(f"Worker {worker_id}: {files_done} files, {total_rows} rows")

    except Exception as e:
        logging.error(f"Worker {worker_id} error: {e}")
        conn.rollback()
    finally:
        conn.close()

    return files_done, total_rows


def parallel_process_parquet(parquet_dir: str, num_workers: int = NUM_WORKERS):
    """
    Process all parquet files in parallel.
    """
    import glob

    files = sorted(glob.glob(f"{parquet_dir}/*.parquet"))
    total_files = len(files)

    if total_files == 0:
        logging.error(f"No parquet files found in {parquet_dir}")
        return 0, 0

    logging.info(f"Processing {total_files} files with {num_workers} workers...")
    start_time = time.time()

    # Split files among workers
    batch_size = (total_files + num_workers - 1) // num_workers
    file_batches = [files[i:i + batch_size] for i in range(0, total_files, batch_size)]

    # Process in parallel
    with mp.Pool(num_workers) as pool:
        results = pool.starmap(
            bulk_copy_to_postgres,
            [(batch, i) for i, batch in enumerate(file_batches)]
        )

    # Aggregate results
    total_files_done = sum(r[0] for r in results)
    total_rows = sum(r[1] for r in results)

    elapsed = time.time() - start_time
    rate = total_rows / elapsed if elapsed > 0 else 0

    logging.info(f"Complete: {total_files_done} files, {total_rows} rows in {elapsed:.1f}s ({rate:.0f} rows/sec)")

    return total_files_done, total_rows


def main():
    log_file = setup_logging()
    logging.info(f"Parallel Parquet Processor starting (log: {log_file})")
    logging.info(f"Workers: {NUM_WORKERS}, Batch size: {BATCH_SIZE}")

    parquet_dir = f"{DATA_ROOT}/hf-parquet"

    files_done, rows_inserted = parallel_process_parquet(parquet_dir)

    logging.info(f"Finished: {files_done} files, {rows_inserted} total rows")

    # Show final count
    conn = psycopg2.connect(**PG_CONFIG)
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM documents_content")
        final_count = cur.fetchone()[0]
        logging.info(f"documents_content table now has {final_count:,} rows")
    conn.close()

    return 0


if __name__ == "__main__":
    # Required for multiprocessing
    mp.set_start_method('spawn', force=True)
    exit(main())
