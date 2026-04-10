#!/usr/bin/env python3
"""
Epstein Files - Batch NER Extraction at Scale

Reads text content from PostgreSQL database, converts to ProcessingResult JSON format,
writes JSON files in batches, and calls epstein-pipeline extract-entities on each batch.

Usage:
    python batch_ner_extraction.py [--batch-size 1000] [--limit N] [--resume]

Features:
    - Reads from PostgreSQL text_content table
    - Converts to ProcessingResult JSON format for epstein-pipeline
    - Batches JSON files to avoid context overflow
    - Calls epstein-pipeline extract-entities on each batch
    - Uses CUDA_VISIBLE_DEVICES=1,2 for K80 GPUs
    - Resumable (checks for existing output before processing)
    - Progress tracking and logging

Author: Epstein Files Analysis Project
Date: 2026-03-25
"""

import os
import sys
import logging
import argparse
import json
import time
import subprocess
import glob
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/processed")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "batch_ner_extraction.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_BATCH_SIZE = 1000
DEFAULT_WORKERS = 4

# PostgreSQL configuration
PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}

# Paths
OUTPUT_BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/processed")
ENTITIES_OUTPUT_DIR = OUTPUT_BASE_DIR / "entities"
REGISTRY_PATH = Path("/home/cbwinslow/workspace/epstein/Epstein-Pipeline/data/persons-registry.json")

# ProcessingResult JSON format expected by epstein-pipeline
# {
#   "source_path": "...",
#   "document": {
#     "id": "EFTA00000001",
#     "title": "...",
#     "summary": "...",
#     "ocrText": "..."
#   }
# }


def get_pg_connection():
    """Get PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


def get_processed_document_ids(output_dir: Path) -> Set[str]:
    """Get set of document IDs that have already been processed.
    
    Args:
        output_dir: Directory containing processed entity JSON files
        
    Returns:
        Set of document IDs (EFTA numbers)
    """
    if not output_dir.exists():
        return set()
    
    processed = set()
    for json_file in output_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if "document" in data and data["document"]:
                doc_id = data["document"].get("id")
                if doc_id:
                    processed.add(doc_id)
        except Exception:
            continue
    
    return processed


def get_documents_from_db(conn, batch_size: int = 1000, offset: int = 0, 
                          limit: Optional[int] = None) -> List[Dict]:
    """Get documents with text content from PostgreSQL.
    
    Args:
        conn: PostgreSQL connection
        batch_size: Number of documents to fetch
        offset: Offset for pagination
        limit: Maximum total documents to fetch
        
    Returns:
        List of document dictionaries
    """
    # Filter to only include records with substantial content (>100 chars)
    # This avoids processing records with NULL content or minimal EFTA-only content
    query = """
        SELECT 
            d.id as document_id,
            d.efta_number,
            dc.content,
            dc.char_count,
            dc.filename
        FROM documents d
        JOIN documents_content dc ON d.id = dc.document_id
        WHERE dc.content IS NOT NULL 
          AND LENGTH(dc.content) > 100
        ORDER BY d.efta_number
        LIMIT %s OFFSET %s
    """
    
    if limit:
        query = f"{query.rstrip(';')} LIMIT {limit}"
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (batch_size, offset))
            return list(cur.fetchall())
    except Exception as e:
        logger.error(f"Error fetching documents: {e}")
        return []


def get_total_document_count(conn) -> int:
    """Get total count of documents with substantial content (>100 chars)."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) 
                FROM documents d
                JOIN documents_content dc ON d.id = dc.document_id
                WHERE dc.content IS NOT NULL 
                  AND LENGTH(dc.content) > 100
            """)
            return cur.fetchone()[0]
    except Exception as e:
        logger.error(f"Error getting document count: {e}")
        return 0


def create_processing_result_json(doc: Dict) -> Dict:
    """Convert database document to ProcessingResult JSON format.
    
    Args:
        doc: Document dictionary from database
        
    Returns:
        ProcessingResult JSON structure
    """
    efta_number = doc.get("efta_number", "")
    content = doc.get("content", "")
    filename = doc.get("filename", "")
    
    # Generate title from filename
    title = filename.replace(".pdf", "").replace("_", " ").replace("-", " ") if filename else efta_number
    
    # Truncate content if too long (avoid context overflow)
    max_content_length = 500000  # ~500KB of text
    if content and len(content) > max_content_length:
        content = content[:max_content_length]
    
    # Include all required fields for ProcessingResult validation:
    # - document.source (required: DocumentSource enum)
    # - document.category (required: DocumentCategory enum)
    # - processing_time_ms (required)
    return {
        "source_path": f"batch/{efta_number}",
        "document": {
            "id": efta_number,
            "title": title,
            "source": "efta",  # DocumentSource enum value
            "category": "other",  # DocumentCategory enum value
            "summary": None,
            "ocrText": content
        },
        "processing_time_ms": 0  # Required field
    }


def write_batch_json_files(documents: List[Dict], batch_dir: Path) -> int:
    """Write batch of documents as JSON files.
    
    Args:
        documents: List of document dictionaries
        batch_dir: Directory to write JSON files
        
    Returns:
        Number of files written
    """
    batch_dir.mkdir(parents=True, exist_ok=True)
    
    files_written = 0
    for doc in documents:
        efta_number = doc.get("efta_number", "")
        if not efta_number:
            continue
        
        # Create ProcessingResult JSON
        result = create_processing_result_json(doc)
        
        # Write to file
        output_file = batch_dir / f"{efta_number}.json"
        try:
            output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            files_written += 1
        except Exception as e:
            logger.error(f"Error writing {output_file}: {e}")
            continue
    
    return files_written


def run_extract_entities(input_dir: Path, output_dir: Path, registry_path: Path) -> bool:
    """Run epstein-pipeline extract-entities on a batch.
    
    Args:
        input_dir: Input directory with JSON files
        output_dir: Output directory for entities
        registry_path: Path to persons-registry.json
        
    Returns:
        True if successful, False otherwise
    """
    # Set GPU environment and PATH
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "1,2"
    
    # Add local bin to PATH for epstein-pipeline
    local_bin = os.path.expanduser("~/.local/bin")
    env["PATH"] = f"{local_bin}:{env.get('PATH', '')}"
    
    # Build command
    cmd = [
        "epstein-pipeline",
        "extract-entities",
        str(input_dir),
        "-r", str(registry_path),
        "-o", str(output_dir),
        "--entity-types", "all"
    ]
    
    logger.info(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode == 0:
            logger.info(f"extract-entities completed successfully")
            if result.stdout:
                logger.info(f"Output: {result.stdout[:500]}")
            return True
        else:
            logger.error(f"extract-entities failed with code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("extract-entities timed out after 1 hour")
        return False
    except Exception as e:
        logger.error(f"Error running extract-entities: {e}")
        return False


def process_batch(conn, batch_num: int, batch_size: int, 
                  processed_ids: Set[str], resume: bool) -> Dict:
    """Process a single batch of documents.
    
    Args:
        conn: PostgreSQL connection
        batch_num: Batch number
        batch_size: Number of documents per batch
        processed_ids: Set of already processed document IDs
        resume: Whether to skip already processed documents
        
    Returns:
        Dictionary with batch results
    """
    batch_dir = OUTPUT_BASE_DIR / "batch_temp" / f"batch_{batch_num:04d}"
    entities_batch_dir = ENTITIES_OUTPUT_DIR / f"batch_{batch_num:04d}"
    
    # Skip if batch already processed (resume mode)
    if resume and entities_batch_dir.exists():
        existing_files = list(entities_batch_dir.glob("*.json"))
        if len(existing_files) > 0:
            logger.info(f"Batch {batch_num} already processed, skipping")
            return {"status": "skipped", "files": len(existing_files)}
    
    # Create batch directory
    batch_dir.mkdir(parents=True, exist_ok=True)
    entities_batch_dir.mkdir(parents=True, exist_ok=True)
    
    # Get documents from database
    offset = batch_num * batch_size
    documents = get_documents_from_db(conn, batch_size=batch_size, offset=offset)
    
    if not documents:
        return {"status": "no_data", "files": 0}
    
    # Filter out already processed documents
    if resume:
        documents = [d for d in documents if d.get("efta_number") not in processed_ids]
        if not documents:
            return {"status": "all_processed", "files": 0}
    
    # Write JSON files
    files_written = write_batch_json_files(documents, batch_dir)
    
    # Log content length statistics for this batch
    if documents:
        content_lengths = [len(doc.get("content", "")) for doc in documents]
        min_len = min(content_lengths)
        max_len = max(content_lengths)
        avg_len = sum(content_lengths) / len(content_lengths)
        logger.info(
            f"Batch {batch_num}: Wrote {files_written} JSON files | "
            f"Content length: min={min_len:,}, max={max_len:,}, avg={avg_len:,.0f}"
        )
    else:
        logger.info(f"Batch {batch_num}: Wrote {files_written} JSON files")
    
    if files_written == 0:
        return {"status": "no_files", "files": 0}
    
    # Run extract-entities
    success = run_extract_entities(batch_dir, entities_batch_dir, REGISTRY_PATH)
    
    if success:
        # Count output files
        output_files = list(entities_batch_dir.glob("*.json"))
        return {
            "status": "success",
            "files": files_written,
            "output_files": len(output_files)
        }
    else:
        return {"status": "failed", "files": files_written}


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Batch NER extraction at scale")
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=DEFAULT_BATCH_SIZE,
        help=f"Number of documents per batch (default: {DEFAULT_BATCH_SIZE})"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit total number of documents to process"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from existing output (skip already processed)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="Number of parallel workers (for future use)"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Epstein Files - Batch NER Extraction")
    logger.info("=" * 60)
    logger.info(f"Batch size: {args.batch_size}")
    logger.info(f"Output directory: {ENTITIES_OUTPUT_DIR}")
    logger.info(f"Registry path: {REGISTRY_PATH}")
    logger.info(f"Resume mode: {args.resume}")
    
    start_time = time.time()
    
    # Ensure output directories exist
    ENTITIES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Connect to PostgreSQL
    conn = get_pg_connection()
    if not conn:
        logger.error("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)
    
    try:
        # Get total document count
        total_docs = get_total_document_count(conn)
        logger.info(f"Total documents with content in database: {total_docs:,}")
        
        if total_docs == 0:
            logger.error("No documents found in database. Exiting.")
            return
        
        # Get already processed document IDs (for resume)
        processed_ids = set()
        if args.resume:
            processed_ids = get_processed_document_ids(ENTITIES_OUTPUT_DIR)
            logger.info(f"Found {len(processed_ids):,} already processed documents")
        
        # Calculate number of batches
        docs_to_process = total_docs - len(processed_ids) if args.resume else total_docs
        num_batches = (docs_to_process + args.batch_size - 1) // args.batch_size
        
        logger.info(f"Documents to process: {docs_to_process:,}")
        logger.info(f"Number of batches: {num_batches}")
        
        if args.limit:
            num_batches = min(num_batches, (args.limit + args.batch_size - 1) // args.batch_size)
            logger.info(f"Limited to {num_batches} batches")
        
        # Process batches
        total_files = 0
        total_output = 0
        successful_batches = 0
        failed_batches = 0
        
        for batch_num in range(num_batches):
            logger.info(f"\n--- Processing batch {batch_num + 1}/{num_batches} ---")
            
            result = process_batch(
                conn, 
                batch_num, 
                args.batch_size,
                processed_ids,
                args.resume
            )
            
            status = result.get("status", "unknown")
            files = result.get("files", 0)
            output_files = result.get("output_files", 0)
            
            if status == "success":
                successful_batches += 1
                total_files += files
                total_output += output_files
            elif status in ("skipped", "all_processed"):
                logger.info(f"Batch {batch_num}: {status}")
            elif status == "no_data":
                logger.info(f"Batch {batch_num}: No more data, stopping")
                break
            else:
                failed_batches += 1
                logger.error(f"Batch {batch_num} failed: {status}")
            
            # Log progress
            elapsed = time.time() - start_time
            docs_done = (batch_num + 1) * args.batch_size
            if docs_done > 0:
                rate = docs_done / elapsed
                eta = (total_docs - docs_done) / rate if rate > 0 else 0
                logger.info(
                    f"Progress: {docs_done:,}/{total_docs:,} documents | "
                    f"Rate: {rate:.1f} docs/sec | ETA: {eta/60:.1f} min"
                )
        
        # Summary
        logger.info("=" * 60)
        logger.info("EXTRACTION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Batches successful: {successful_batches}")
        logger.info(f"Batches failed: {failed_batches}")
        logger.info(f"Total JSON files written: {total_files:,}")
        logger.info(f"Total entity files output: {total_output:,}")
        
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
