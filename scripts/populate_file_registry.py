#!/usr/bin/env python3
"""
Epstein Files - File Registry Population Script

Scans filesystem for downloaded files, computes SHA-256 hashes,
and populates the PostgreSQL file_registry table. Provides
verification reports and cross-referencing with documents table.

Usage:
    python populate_file_registry.py [--scan-dirs /mnt/data/epstein-project/raw-files]
                                     [--workers 38]
                                     [--batch-size 1000]
                                     [--report-only]
                                     [--resume]

Features:
    - Parallel SHA-256 hashing with multiprocessing
    - Batch PostgreSQL inserts for performance
    - Resume capability (skip processed files)
    - PDF validation (signature check)
    - Cross-reference with documents table
    - Generate verification reports
    - Generalizable for other file scanning tasks

Author: Epstein Files Analysis Project
Date: 2026-03-23
"""

import os
import sys
import hashlib
import logging
import argparse
import json
import csv
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/cbwinslow/workspace/epstein/processed/file_registry.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_BATCH_SIZE = 1000
DEFAULT_WORKERS = max(1, cpu_count() - 2)  # Leave 2 cores for system
MIN_PDF_SIZE = 100  # Minimum valid PDF size in bytes
MAX_PATH_LENGTH = 1000  # Maximum file path length

# PostgreSQL configuration
PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}


@dataclass
class FileMetadata:
    """Container for file metadata."""

    file_path: str
    file_name: str
    file_size: int
    sha256_hash: str
    efta_number: Optional[str]
    dataset: Optional[int]
    source: str  # 'doj', 'hf', 'cdn', 'archive_org', 'prebuilt'
    is_valid_pdf: bool
    error: Optional[str] = None
    processed_at: Optional[datetime] = None


def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 hash of a file using chunked reading.

    Args:
        file_path: Path to file

    Returns:
        SHA-256 hex digest string
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(65536)  # 64KB chunks
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        logger.error(f"Error computing hash for {file_path}: {e}")
        return ""


def is_valid_pdf(file_path: str) -> bool:
    """Check if file is a valid PDF by checking magic bytes.

    Args:
        file_path: Path to file

    Returns:
        True if file starts with %PDF-, False otherwise
    """
    try:
        with open(file_path, "rb") as f:
            header = f.read(5)
            return header == b"%PDF-"
    except Exception:
        return False


def extract_efta_number(file_name: str) -> Optional[str]:
    """Extract EFTA number from filename.

    Supports patterns:
    - EFTA{8-digits}.pdf
    - EFTA{8-digits}.{version}.pdf
    - HOUSE_OVERSIGHT_{digits}.pdf (non-standard)
    - DOJ-OGR-{digits}.pdf (non-standard)

    Args:
        file_name: Name of file

    Returns:
        EFTA number string or None if not found
    """
    import re

    # Standard EFTA pattern
    match = re.match(r"^(EFTA\d{8})(?:\.\d+)?\.pdf$", file_name)
    if match:
        return match.group(1)

    # House Oversight pattern
    match = re.match(r"^HOUSE_OVERSIGHT_(\d+)\.pdf$", file_name)
    if match:
        return f"HOUSE_OVERSIGHT_{match.group(1)}"

    # DOJ-OGR pattern
    match = re.match(r"^DOJ-OGR-(\d+)\.pdf$", file_name)
    if match:
        return f"DOJ-OGR-{match.group(1)}"

    # Generic pattern for other naming
    match = re.match(r"^([A-Z0-9_-]+)\.pdf$", file_name)
    if match:
        return match.group(1)

    return None


def determine_dataset(file_path: str) -> Optional[int]:
    """Determine dataset number from file path.

    Args:
        file_path: Full path to file

    Returns:
        Dataset number (1-12) or None
    """
    import re

    # Look for /data{N}/ pattern in path
    match = re.search(r"/data(\d+)/", file_path)
    if match:
        return int(match.group(1))

    return None


def determine_source(file_path: str) -> str:
    """Determine source of file based on path.

    Args:
        file_path: Full path to file

    Returns:
        Source string: 'doj', 'hf', 'cdn', 'archive_org', 'prebuilt'
    """
    if "/hf-parquet/" in file_path:
        return "hf"
    elif "/raw-files/" in file_path:
        return "doj"
    elif "archive.org" in file_path:
        return "archive_org"
    elif "cdn.rollcall.com" in file_path:
        return "cdn"
    else:
        return "prebuilt"


def process_single_file(file_path: str) -> Optional[FileMetadata]:
    """Process a single file and extract metadata.

    Args:
        file_path: Full path to file

    Returns:
        FileMetadata object or None if processing failed
    """
    try:
        path_obj = Path(file_path)
        file_name = path_obj.name
        file_size = path_obj.stat().st_size

        # Skip tiny files (likely corrupted or control files)
        if file_size < MIN_PDF_SIZE:
            return None

        # Skip aria2 control files
        if file_name.endswith(".aria2"):
            return None

        # Compute hash
        sha256_hash = compute_sha256(file_path)
        if not sha256_hash:
            return None

        # Extract EFTA number
        efta_number = extract_efta_number(file_name)

        # Determine dataset
        dataset = determine_dataset(file_path)

        # Determine source
        source = determine_source(file_path)

        # Validate PDF (only for .pdf files)
        is_pdf = file_name.lower().endswith(".pdf")
        is_valid = is_valid_pdf(file_path) if is_pdf else True  # Non-PDFs are considered valid

        return FileMetadata(
            file_path=str(path_obj.absolute()),
            file_name=file_name,
            file_size=file_size,
            sha256_hash=sha256_hash,
            efta_number=efta_number,
            dataset=dataset,
            source=source,
            is_valid_pdf=is_valid,
            processed_at=datetime.now(),
        )

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return None


def get_pg_connection():
    """Get PostgreSQL database connection.

    Returns:
        psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


def insert_batch_to_registry(records: List[FileMetadata], conn) -> int:
    """Insert batch of records into file_registry table.

    Args:
        records: List of FileMetadata objects
        conn: PostgreSQL connection

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
                        rec.file_path,
                        rec.sha256_hash,
                        rec.efta_number,
                        rec.dataset,
                        rec.file_size,
                        rec.source,
                        rec.processed_at,
                        rec.is_valid_pdf,
                        None,  # notes
                    )
                )

            # Use INSERT ... ON CONFLICT for upsert behavior
            query = """
                INSERT INTO file_registry 
                (file_path, sha256_hash, efta_number, dataset, file_size_bytes, 
                 source, downloaded_at, validated, notes)
                VALUES %s
                ON CONFLICT (file_path) DO UPDATE SET
                    sha256_hash = EXCLUDED.sha256_hash,
                    file_size_bytes = EXCLUDED.file_size_bytes,
                    validated = EXCLUDED.validated,
                    downloaded_at = EXCLUDED.downloaded_at
            """

            execute_values(cur, query, data)
            conn.commit()

            return len(data)

    except Exception as e:
        logger.error(f"Error inserting batch: {e}")
        conn.rollback()
        return 0


def scan_directory(root_dir: str, pattern: str = "*.pdf") -> List[str]:
    """Recursively scan directory for files matching pattern.

    Args:
        root_dir: Root directory to scan
        pattern: File pattern to match

    Returns:
        List of file paths
    """
    root_path = Path(root_dir)
    if not root_path.exists():
        logger.warning(f"Directory does not exist: {root_dir}")
        return []

    files = []
    for ext in ["*.pdf", "*.PDF", "*.parquet"]:
        files.extend([str(f) for f in root_path.rglob(ext)])

    logger.info(f"Found {len(files)} files in {root_dir}")
    return files


def process_files_parallel(
    file_paths: List[str], workers: int = DEFAULT_WORKERS
) -> List[FileMetadata]:
    """Process files in parallel using multiprocessing.

    Args:
        file_paths: List of file paths to process
        workers: Number of parallel workers

    Returns:
        List of FileMetadata objects
    """
    logger.info(f"Processing {len(file_paths)} files with {workers} workers")

    results = []
    with Pool(workers) as pool:
        # Use tqdm for progress tracking
        for result in tqdm(
            pool.imap_unordered(process_single_file, file_paths),
            total=len(file_paths),
            desc="Processing files",
        ):
            if result:
                results.append(result)

    logger.info(f"Successfully processed {len(results)} files")
    return results


def get_existing_files_in_registry(conn) -> set:
    """Get set of file paths already in registry.

    Args:
        conn: PostgreSQL connection

    Returns:
        Set of file paths
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT file_path FROM file_registry")
            return set(row[0] for row in cur.fetchall())
    except Exception as e:
        logger.error(f"Error fetching existing files: {e}")
        return set()


def generate_verification_report(conn) -> Dict[str, Any]:
    """Generate verification report by cross-referencing with documents table.

    Args:
        conn: PostgreSQL connection

    Returns:
        Dictionary with verification statistics
    """
    report = {"generated_at": datetime.now().isoformat(), "statistics": {}, "issues": []}

    try:
        with conn.cursor() as cur:
            # Total files in registry
            cur.execute("SELECT COUNT(*) FROM file_registry")
            total_files = cur.fetchone()[0]
            report["statistics"]["total_files_in_registry"] = total_files

            # Total documents in documents table
            cur.execute("SELECT COUNT(*) FROM documents")
            total_documents = cur.fetchone()[0]
            report["statistics"]["total_documents"] = total_documents

            # Files with valid EFTA numbers
            cur.execute("SELECT COUNT(*) FROM file_registry WHERE efta_number IS NOT NULL")
            files_with_efta = cur.fetchone()[0]
            report["statistics"]["files_with_efta_numbers"] = files_with_efta

            # Documents with files
            cur.execute("""
                SELECT COUNT(DISTINCT d.efta_number) 
                FROM documents d
                JOIN file_registry r ON d.efta_number = r.efta_number
            """)
            documents_with_files = cur.fetchone()[0]
            report["statistics"]["documents_with_files"] = documents_with_files

            # Documents missing files
            cur.execute("""
                SELECT d.efta_number, d.dataset, d.file_path
                FROM documents d
                LEFT JOIN file_registry r ON d.efta_number = r.efta_number
                WHERE r.efta_number IS NULL
                LIMIT 10
            """)
            missing_docs = cur.fetchall()
            report["statistics"]["documents_missing_files"] = len(missing_docs)

            # Duplicate SHA-256 hashes
            cur.execute("""
                SELECT sha256_hash, COUNT(*) as count, 
                       STRING_AGG(efta_number, ', ') as efta_numbers
                FROM file_registry 
                WHERE sha256_hash IS NOT NULL
                GROUP BY sha256_hash 
                HAVING COUNT(*) > 1
            """)
            duplicate_hashes = cur.fetchall()
            report["statistics"]["duplicate_hash_groups"] = len(duplicate_hashes)

            # Invalid PDFs
            cur.execute("SELECT COUNT(*) FROM file_registry WHERE validated = FALSE")
            invalid_pdfs = cur.fetchone()[0]
            report["statistics"]["invalid_pdfs"] = invalid_pdfs

            # Generate issues list
            if missing_docs:
                for doc in missing_docs[:5]:  # First 5
                    report["issues"].append(
                        {
                            "type": "missing_file",
                            "efta_number": doc[0],
                            "dataset": doc[1],
                            "file_path": doc[2],
                            "description": f"Document has no corresponding file in registry",
                        }
                    )

            if duplicate_hashes:
                for dup in duplicate_hashes[:5]:  # First 5
                    report["issues"].append(
                        {
                            "type": "duplicate_hash",
                            "sha256_hash": dup[0],
                            "count": dup[1],
                            "efta_numbers": dup[2],
                            "description": f"Same file referenced by {dup[1]} different EFTA numbers",
                        }
                    )

    except Exception as e:
        logger.error(f"Error generating verification report: {e}")

    return report


def save_report_to_file(report: Dict[str, Any], output_dir: str) -> str:
    """Save verification report to file.

    Args:
        report: Report dictionary
        output_dir: Directory to save report

    Returns:
        Path to saved report file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save as JSON
    json_path = output_path / f"file_registry_report_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    # Save as CSV for issues
    csv_path = output_path / f"file_registry_issues_{timestamp}.csv"
    with open(csv_path, "w", newline="") as f:
        if report["issues"]:
            writer = csv.DictWriter(f, fieldnames=report["issues"][0].keys())
            writer.writeheader()
            writer.writerows(report["issues"])

    logger.info(f"Reports saved to: {json_path}, {csv_path}")
    return str(json_path)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Populate file registry with SHA-256 hashes")
    parser.add_argument(
        "--scan-dirs",
        nargs="+",
        default=["/mnt/data/epstein-project/raw-files", "/mnt/data/epstein-project/hf-parquet"],
        help="Directories to scan",
    )
    parser.add_argument(
        "--workers", type=int, default=DEFAULT_WORKERS, help="Number of parallel workers"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Batch size for PostgreSQL inserts",
    )
    parser.add_argument(
        "--report-only", action="store_true", help="Only generate report, do not scan/insert"
    )
    parser.add_argument("--resume", action="store_true", help="Resume from last processed file")
    parser.add_argument(
        "--output-dir", default="/mnt/data/epstein-project/logs", help="Directory to save reports"
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Epstein Files - File Registry Population")
    logger.info("=" * 60)
    logger.info(f"Scan directories: {args.scan_dirs}")
    logger.info(f"Workers: {args.workers}")
    logger.info(f"Batch size: {args.batch_size}")

    start_time = time.time()

    # Connect to PostgreSQL
    conn = get_pg_connection()
    if not conn:
        logger.error("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)

    try:
        if not args.report_only:
            # Step 1: Scan directories and collect files
            logger.info("Step 1: Scanning directories...")
            all_files = []
            for scan_dir in args.scan_dirs:
                files = scan_directory(scan_dir)
                all_files.extend(files)

            logger.info(f"Total files found: {len(all_files)}")

            # Step 2: Filter already processed files if resuming
            if args.resume:
                logger.info("Step 2: Checking for already processed files...")
                existing_files = get_existing_files_in_registry(conn)
                if existing_files:
                    all_files = [f for f in all_files if f not in existing_files]
                    logger.info(f"Skipping {len(existing_files)} already processed files")
                    logger.info(f"Remaining files to process: {len(all_files)}")

            # Step 3: Process files in parallel
            logger.info("Step 3: Processing files (computing SHA-256 hashes)...")
            file_metadata = process_files_parallel(all_files, args.workers)

            # Step 4: Insert into PostgreSQL in batches
            logger.info("Step 4: Inserting into PostgreSQL...")
            total_inserted = 0
            for i in range(0, len(file_metadata), args.batch_size):
                batch = file_metadata[i : i + args.batch_size]
                inserted = insert_batch_to_registry(batch, conn)
                total_inserted += inserted
                logger.debug(f"Inserted batch {i // args.batch_size + 1}: {inserted} records")

            logger.info(f"Total records inserted/updated: {total_inserted}")

        # Step 5: Generate verification report
        logger.info("Step 5: Generating verification report...")
        report = generate_verification_report(conn)

        # Save report
        report_file = save_report_to_file(report, args.output_dir)

        # Print summary
        logger.info("=" * 60)
        logger.info("SUMMARY")
        logger.info("=" * 60)
        for key, value in report["statistics"].items():
            logger.info(f"{key.replace('_', ' ').title()}: {value:,}")

        if report["issues"]:
            logger.info(f"\nFound {len(report['issues'])} issues (see {report_file})")

        elapsed_time = time.time() - start_time
        logger.info(f"\nTotal execution time: {elapsed_time / 60:.1f} minutes")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
