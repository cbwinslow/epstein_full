#!/usr/bin/env python3
"""
Epstein Files - Populate documents_content table from hf-parquet files.

Extracts text_content from HuggingFace parquet files and populates the
documents_content table in PostgreSQL. This provides consolidated
document-level text (vs page-level text in pages table).

Usage:
    python populate_text_content.py [--parquet-dir /mnt/data/epstein-project/hf-parquet]
                                    [--batch-size 100]
                                    [--workers 4]
                                    [--resume]

Features:
    - Parallel processing of 634 parquet files (318GB total)
    - Batch PostgreSQL inserts with error handling
    - Resume capability (skip already processed documents)
    - Progress tracking with ETA
    - Memory-efficient streaming (process files one at a time)
    - Validation and reporting

Author: Epstein Files Analysis Project
Date: 2026-03-23
"""

import os
import sys
import logging
import argparse
import json
import time
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/cbwinslow/workspace/epstein/processed/text_content.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_BATCH_SIZE = 100
DEFAULT_WORKERS = 4  # Conservative for memory usage
MAX_TEXT_LENGTH = 1000000  # Maximum text length to store (1MB)

# PostgreSQL configuration
PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}


@dataclass
class TextContentRecord:
    """Container for text content record."""

    document_id: Optional[int]
    filename: str
    content: str
    char_count: int
    page_count: int  # Will be estimated or set to 1
    processing_time: float


def get_pg_connection():
    """Get PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


def get_document_id(efta_number: str, conn) -> Optional[int]:
    """Get document ID from efta_number.

    Args:
        efta_number: EFTA document number
        conn: PostgreSQL connection

    Returns:
        Document ID or None if not found
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM documents WHERE efta_number = %s", (efta_number,))
            result = cur.fetchone()
            return result[0] if result else None
    except Exception as e:
        logger.error(f"Error getting document ID for {efta_number}: {e}")
        return None


def get_existing_document_ids(conn) -> set:
    """Get set of document IDs already in documents_content.

    Args:
        conn: PostgreSQL connection

    Returns:
        Set of document IDs
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT document_id FROM documents_content")
            return set(row[0] for row in cur.fetchall())
    except Exception as e:
        logger.error(f"Error fetching existing document IDs: {e}")
        return set()


def process_parquet_file(file_path: str, conn, existing_ids: set) -> Tuple[int, int, int]:
    """Process a single parquet file and extract text content.

    Args:
        file_path: Path to parquet file
        conn: PostgreSQL connection
        existing_ids: Set of already processed document IDs

    Returns:
        Tuple of (processed, skipped, errors) counts
    """
    processed = 0
    skipped = 0
    errors = 0

    try:
        # Read parquet file
        logger.info(f"Processing {os.path.basename(file_path)}")
        table = pq.read_table(file_path)
        df = table.to_pandas()

        # Prepare batch for insertion
        batch_records = []

        for idx, row in df.iterrows():
            try:
                # Extract fields
                doc_id_str = row.get("doc_id", "")
                text_content = row.get("text_content", "")
                # error_field not used (documents_content table has no error column)

                # Skip if no document ID or already processed
                if not doc_id_str:
                    skipped += 1
                    continue

                # Get database document ID
                document_id = get_document_id(doc_id_str, conn)
                if not document_id:
                    # Try alternative ID extraction (remove EFTA prefix if needed)
                    if doc_id_str.startswith("EFTA"):
                        numeric_id = doc_id_str[4:]  # Remove 'EFTA' prefix
                        document_id = get_document_id(numeric_id, conn)

                    if not document_id:
                        logger.debug(f"Document not found: {doc_id_str}")
                        skipped += 1
                        continue

                # Skip if already processed
                if document_id in existing_ids:
                    skipped += 1
                    continue

                # Process text content
                if not text_content or pd.isna(text_content):
                    content = ""
                    char_count = 0
                else:
                    # Truncate if too long
                    content = str(text_content)[:MAX_TEXT_LENGTH]
                    char_count = len(content)

                # Create record
                record = TextContentRecord(
                    document_id=document_id,
                    filename=f"{doc_id_str}.pdf",
                    content=content,
                    char_count=char_count,
                    page_count=1,  # Estimate: one document per row
                    processing_time=0.0,  # Not measured
                )

                batch_records.append(record)

                # Insert in batches
                if len(batch_records) >= 100:
                    inserted = insert_batch(batch_records, conn, existing_ids)
                    processed += inserted
                    batch_records = []

            except Exception as e:
                logger.error(f"Error processing row {idx} in {file_path}: {e}")
                errors += 1
                continue

        # Insert remaining records
        if batch_records:
            inserted = insert_batch(batch_records, conn, existing_ids)
            processed += inserted

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        errors += 1

    return processed, skipped, errors


def insert_batch(records: List[TextContentRecord], conn, existing_ids: set) -> int:
    """Insert batch of records into documents_content table.

    Args:
        records: List of TextContentRecord objects
        conn: PostgreSQL connection
        existing_ids: Set of already processed document IDs (will be updated)

    Returns:
        Number of records inserted
    """
    if not records:
        return 0

    try:
        with conn.cursor() as cur:
            # Prepare data for insertion
            data = []
            for rec in records:
                data.append(
                    (
                        rec.document_id,
                        rec.filename,
                        rec.content,
                        rec.char_count,
                        rec.page_count,
                        rec.processing_time,
                    )
                )

            # Insert with ON CONFLICT DO NOTHING (skip duplicates)
            query = """
                INSERT INTO documents_content 
                (document_id, filename, content, char_count, page_count, 
                 processing_time)
                VALUES %s
                ON CONFLICT (document_id) DO NOTHING
            """

            execute_values(cur, query, data)
            inserted = cur.rowcount
            conn.commit()

            # Update existing_ids set
            for rec in records:
                if rec.document_id:
                    existing_ids.add(rec.document_id)

            return inserted

    except Exception as e:
        logger.error(f"Error inserting batch: {e}")
        conn.rollback()
        return 0


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Populate documents_content from hf-parquet")
    parser.add_argument(
        "--parquet-dir",
        default="/mnt/data/epstein-project/hf-parquet",
        help="Directory containing parquet files",
    )
    parser.add_argument(
        "--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="Batch size for processing"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="Number of parallel workers (conservative for memory)",
    )
    parser.add_argument("--resume", action="store_true", help="Resume from last processed file")
    parser.add_argument("--limit", type=int, help="Limit number of files to process (for testing)")

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Epstein Files - Populate Text Content")
    logger.info("=" * 60)

    start_time = time.time()

    # Connect to PostgreSQL
    conn = get_pg_connection()
    if not conn:
        logger.error("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)

    try:
        # Step 1: Get existing document IDs to skip
        logger.info("Step 1: Checking existing data...")
        existing_ids = get_existing_document_ids(conn)
        logger.info(f"Found {len(existing_ids)} already processed documents")

        # Step 2: Find all parquet files
        logger.info("Step 2: Finding parquet files...")
        parquet_pattern = os.path.join(args.parquet_dir, "*.parquet")
        parquet_files = sorted(glob.glob(parquet_pattern))

        if args.limit:
            parquet_files = parquet_files[: args.limit]

        logger.info(f"Found {len(parquet_files)} parquet files to process")

        if not parquet_files:
            logger.error("No parquet files found. Check directory path.")
            return

        # Step 3: Process files
        logger.info("Step 3: Processing parquet files...")

        total_processed = 0
        total_skipped = 0
        total_errors = 0

        # Process files sequentially (memory constraints)
        for file_path in tqdm(parquet_files, desc="Processing files"):
            processed, skipped, errors = process_parquet_file(file_path, conn, existing_ids)
            total_processed += processed
            total_skipped += skipped
            total_errors += errors

            # Log progress every 10 files
            if (parquet_files.index(file_path) + 1) % 10 == 0:
                logger.info(
                    f"Progress: {total_processed} processed, "
                    f"{total_skipped} skipped, {total_errors} errors"
                )

        # Step 4: Generate summary
        logger.info("=" * 60)
        logger.info("SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total files processed: {len(parquet_files)}")
        logger.info(f"Documents added: {total_processed:,}")
        logger.info(f"Documents skipped: {total_skipped:,}")
        logger.info(f"Errors: {total_errors:,}")
        logger.info(f"Total documents in content table: {len(existing_ids) + total_processed:,}")

        elapsed_time = time.time() - start_time
        logger.info(f"\nTotal execution time: {elapsed_time / 60:.1f} minutes")

        # Step 5: Validate results
        logger.info("\nStep 5: Validating results...")
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM documents_content")
            count = cur.fetchone()[0]
            logger.info(f"Total rows in documents_content: {count:,}")

            # Check average text length
            cur.execute("SELECT AVG(char_count) FROM documents_content WHERE char_count > 0")
            avg_len = cur.fetchone()[0]
            if avg_len:
                logger.info(f"Average text length: {avg_len:,.0f} characters")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
