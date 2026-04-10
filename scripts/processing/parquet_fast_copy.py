#!/usr/bin/env python3
"""
Fast Parquet Processor with COPY bulk loading
Single-process but optimized for throughput
"""

import io
import logging
import os
import re
import time
from datetime import datetime

import pandas as pd
import psycopg2

# Config
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


def setup_logging():
    log_file = f"{LOG_DIR}/parquet_fast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return log_file


def extract_doc_number(doc_id: str) -> int:
    """Extract numeric part from doc_id like EFTA00012345 -> 12345"""
    if not doc_id:
        return 0
    match = re.search(r'(\d+)', str(doc_id))
    return int(match.group(1)) if match else 0


def process_and_copy_file(file_path: str, conn) -> int:
    """Process single file and COPY to postgres. Returns rows inserted."""
    try:
        df = pd.read_parquet(file_path)

        if 'text_content' not in df.columns:
            return 0

        df = df[df['text_content'].notna()]
        df = df[df['text_content'].str.len() > 10]

        if len(df) == 0:
            return 0

        # Build CSV buffer (handles embedded newlines better than TSV)
        buffer = io.StringIO()
        rows = 0

        for _, row in df.iterrows():
            doc_id_str = str(row.get('doc_id', ''))
            document_id = extract_doc_number(doc_id_str)
            filename = str(row.get('file_name', '')) or ''
            content = str(row.get('text_content', '')) or ''
            char_count = len(content) if content else 0
            page_count = 1

            if document_id > 0 and content:
                # Escape for CSV - wrap in quotes, escape internal quotes
                filename_clean = filename.replace('"', '""')[:250]
                content_clean = content.replace('"', '""')
                buffer.write(f'"{document_id}","{filename_clean}","{content_clean}",{char_count},{page_count}\n')
                rows += 1

        if rows == 0:
            return 0

        # COPY to postgres using CSV format
        buffer.seek(0)
        with conn.cursor() as cur:
            cur.copy_expert(
                """COPY documents_content (document_id, filename, content, char_count, page_count) 
                   FROM STDIN WITH CSV""",
                buffer
            )
            conn.commit()

        return rows

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        conn.rollback()
        return 0


def main():
    import glob

    log_file = setup_logging()
    logging.info(f"Fast Parquet Processor starting (log: {log_file})")

    parquet_dir = f"{DATA_ROOT}/hf-parquet"
    files = sorted(glob.glob(f"{parquet_dir}/*.parquet"))

    logging.info(f"Found {len(files)} parquet files")

    conn = psycopg2.connect(**PG_CONFIG)
    total_rows = 0
    start_time = time.time()

    for i, file_path in enumerate(files, 1):
        rows = process_and_copy_file(file_path, conn)
        total_rows += rows

        if i % 10 == 0 or i == len(files):
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            logging.info(f"Progress: {i}/{len(files)} files, {total_rows} rows, {rate:.1f} files/sec")

    conn.close()

    elapsed = time.time() - start_time
    logging.info(f"Complete: {len(files)} files, {total_rows} rows in {elapsed:.1f}s")

    return 0


if __name__ == "__main__":
    exit(main())
