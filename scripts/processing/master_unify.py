#!/usr/bin/env python3
"""
Master Data Unification Script for Epstein Project

Unifies all data sources into PostgreSQL with progress tracking.
Handles: JSON imports, CSV imports, HF parquet processing, downloads.

Usage:
  python master_unify.py --all                    # Run everything
  python master_unify.py --import-only          # Just imports (no downloads)
  python master_unify.py --download-only        # Just downloads
  python master_unify.py --source research-data # Specific source only
  python master_unify.py --dry-run              # Show what would be done

Background mode:
  nohup python master_unify.py --all > logs/unify_$(date +%Y%m%d_%H%M%S).log 2>&1 &
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration
PROJECT_ROOT = os.environ.get("EPSTEIN_PROJECT_ROOT", "/home/cbwinslow/workspace/epstein")
DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Database connection
PG_CONFIG = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": int(os.environ.get("PG_PORT", "5432")),
    "user": os.environ.get("PG_USER", "cbwinslow"),
    "password": os.environ.get("PG_PASSWORD", "123qweasd"),
    "dbname": os.environ.get("PG_DB", "epstein"),
}

# Data sources configuration - using existing tables
DATA_SOURCES = {
    "research-data": {
        "path": f"{PROJECT_ROOT}/Epstein-research-data",
        "files": [
            ("persons_registry.json", "json_import_staging", "json"),
            ("extracted_entities_filtered.json", "json_import_staging", "json"),
            ("extracted_names_multi_doc.csv", "csv_import_staging", "csv"),
            ("phone_numbers_enriched.csv", "csv_import_staging", "csv"),
        ],
        "priority": 1,
    },
    "supplementary": {
        "path": f"{DATA_ROOT}/supplementary",
        "files": [
            ("export_persons.json", "json_import_staging", "json"),
            ("export_flights.json", "json_import_staging", "json"),
            ("export_locations.json", "json_import_staging", "json"),
        ],
        "priority": 2,
    },
    "hf-parquet": {
        "path": f"{DATA_ROOT}/hf-parquet",
        "pattern": "*.parquet",
        "target_table": "documents_content",
        "priority": 3,
        "batch_size": 1000,
    },
    "jmail": {
        "url": "https://data.jmail.world/v1/emails-slim.parquet",
        "path": f"{DATA_ROOT}/supplementary/emails-slim.parquet",
        "target_table": "jmail_emails",
        "priority": 4,
    },
}


class ProgressTracker:
    """Track progress across all operations."""
    
    def __init__(self, log_file: Optional[str] = None):
        self.start_time = time.time()
        self.operations: Dict[str, Dict] = {}
        self.log_file = log_file or f"{LOG_DIR}/unify_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging to file and console."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def start_operation(self, name: str, total: int = 0, details: str = ""):
        """Start tracking an operation."""
        self.operations[name] = {
            "start": time.time(),
            "total": total,
            "current": 0,
            "status": "running",
            "details": details,
        }
        self.logger.info(f"[START] {name}: {details} (total: {total})")
        
    def update_progress(self, name: str, current: int, message: str = ""):
        """Update operation progress."""
        if name in self.operations:
            self.operations[name]["current"] = current
            total = self.operations[name]["total"]
            pct = (current / total * 100) if total > 0 else 0
            elapsed = time.time() - self.operations[name]["start"]
            rate = current / elapsed if elapsed > 0 else 0
            
            msg = f"[PROGRESS] {name}: {current}/{total} ({pct:.1f}%) - {rate:.1f} items/sec"
            if message:
                msg += f" - {message}"
            self.logger.info(msg)
            
    def complete_operation(self, name: str, message: str = ""):
        """Mark operation as complete."""
        if name in self.operations:
            self.operations[name]["status"] = "complete"
            elapsed = time.time() - self.operations[name]["start"]
            current = self.operations[name]["current"]
            rate = current / elapsed if elapsed > 0 else 0
            self.logger.info(f"[COMPLETE] {name}: {current} items in {elapsed:.1f}s ({rate:.1f}/sec) - {message}")
            
    def fail_operation(self, name: str, error: str):
        """Mark operation as failed."""
        if name in self.operations:
            self.operations[name]["status"] = "failed"
            self.operations[name]["error"] = error
            self.logger.error(f"[FAILED] {name}: {error}")
            
    def summary(self) -> str:
        """Generate summary report."""
        total_time = time.time() - self.start_time
        total_ops = len(self.operations)
        complete = sum(1 for o in self.operations.values() if o["status"] == "complete")
        failed = sum(1 for o in self.operations.values() if o["status"] == "failed")
        
        return f"""
{'='*80}
UNIFICATION SUMMARY
{'='*80}
Total Time: {total_time:.1f}s
Operations: {total_ops} (complete: {complete}, failed: {failed})
Log File: {self.log_file}

Per-Operation:
""" + "\n".join(
            f"  {name}: {o['status']} ({o.get('current', 0)} items)" 
            for name, o in sorted(self.operations.items())
        )


class DataUnifier:
    """Master unification orchestrator."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.tracker = ProgressTracker()
        self.conn = None
        
    def connect(self) -> bool:
        """Connect to PostgreSQL."""
        try:
            self.conn = psycopg2.connect(**PG_CONFIG)
            self.tracker.logger.info("✓ Connected to PostgreSQL")
            return True
        except Exception as e:
            self.tracker.logger.error(f"✗ Failed to connect: {e}")
            return False
            
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            
    def check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """, (table_name,))
            return cur.fetchone()[0]
            
    def get_table_count(self, table_name: str) -> int:
        """Get row count for a table."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cur.fetchone()[0]
        except:
            return 0
            
    def import_json_to_staging(self, file_path: str, table_name: str, source_name: str) -> int:
        """Import JSON file to staging table with proper transaction handling."""
        if not os.path.exists(file_path):
            self.tracker.logger.warning(f"File not found: {file_path}")
            return 0

        self.tracker.start_operation(f"import_{source_name}", details=f"{file_path} -> {table_name}")

        if self.dry_run:
            self.tracker.logger.info(f"[DRY-RUN] Would import {file_path} to {table_name}")
            return 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle both array and object formats
            if isinstance(data, dict):
                # Try to find an array inside
                for key, value in data.items():
                    if isinstance(value, list):
                        data = value
                        break
                else:
                    data = [data]

            total = len(data)
            self.tracker.operations[f"import_{source_name}"]["total"] = total

            imported = 0
            batch_size = 100

            # Process in separate transactions to avoid aborting everything
            for i in range(0, len(data), batch_size):
                batch = data[i:i+batch_size]
                try:
                    with self.conn.cursor() as cur:
                        for item in batch:
                            cur.execute(f"""
                                INSERT INTO {table_name} (source_file, data, imported_at)
                                VALUES (%s, %s, NOW())
                                ON CONFLICT DO NOTHING
                            """, (file_path, json.dumps(item)))
                        self.conn.commit()
                        imported += len(batch)
                        self.tracker.update_progress(f"import_{source_name}", imported)
                except Exception as e:
                    self.conn.rollback()
                    self.tracker.logger.warning(f"Batch failed: {e}")
                    continue

            self.tracker.complete_operation(f"import_{source_name}", f"Imported {imported}/{total} records")
            return imported

        except Exception as e:
            self.conn.rollback()
            self.tracker.fail_operation(f"import_{source_name}", str(e))
            return 0
            
    def import_csv_to_staging(self, file_path: str, table_name: str, source_name: str) -> int:
        """Import CSV file to staging table."""
        if not os.path.exists(file_path):
            self.tracker.logger.warning(f"File not found: {file_path}")
            return 0
            
        self.tracker.start_operation(f"import_{source_name}", details=f"{file_path} -> {table_name}")
        
        if self.dry_run:
            self.tracker.logger.info(f"[DRY-RUN] Would import {file_path} to {table_name}")
            return 0
            
        try:
            # Read CSV and convert to JSONB rows
            import csv
            imported = 0
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            self.tracker.operations[f"import_{source_name}"]["total"] = len(rows)
            
            batch_size = 100
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i+batch_size]
                try:
                    with self.conn.cursor() as cur:
                        for row in batch:
                            cur.execute(f"""
                                INSERT INTO {table_name} (source_file, row_data, imported_at)
                                VALUES (%s, %s, NOW())
                            """, (file_path, json.dumps(row)))
                        self.conn.commit()
                        imported += len(batch)
                        self.tracker.update_progress(f"import_{source_name}", imported)
                except Exception as e:
                    self.conn.rollback()
                    self.tracker.logger.warning(f"Batch failed: {e}")
                    continue
                    
            self.tracker.complete_operation(f"import_{source_name}", f"Imported {imported} records")
            return imported
            
        except Exception as e:
            self.tracker.fail_operation(f"import_{source_name}", str(e))
            return 0
            
    def process_parquet_directory(self, path: str, table_name: str) -> int:
        """Process all parquet files in directory."""
        import glob
        
        files = glob.glob(f"{path}/*.parquet")
        if not files:
            self.tracker.logger.warning(f"No parquet files found in {path}")
            return 0
            
        self.tracker.start_operation("parquet_import", total=len(files), details=f"Processing {len(files)} parquet files")
        
        if self.dry_run:
            self.tracker.logger.info(f"[DRY-RUN] Would process {len(files)} parquet files")
            return 0
            
        total_rows = 0
        for i, file_path in enumerate(files):
            try:
                # Each file in its own transaction
                import pandas as pd
                
                df = pd.read_parquet(file_path)
                
                # Filter rows with text_content
                if 'text_content' in df.columns:
                    df = df[df['text_content'].notna()]
                    
                records_imported = 0
                
                # Process in batches within a single transaction per file
                with self.conn.cursor() as cur:
                    for _, row in df.iterrows():
                        # Extract relevant fields
                        efta = row.get('doc_id', row.get('efta_number', ''))
                        text = row.get('text_content', '')
                        dataset = row.get('dataset_id', 0)
                        
                        if efta and text and len(text) > 10:
                            try:
                                cur.execute("""
                                    INSERT INTO documents_content (efta_number, text_content, dataset, source_file)
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (efta_number) DO UPDATE SET
                                        text_content = EXCLUDED.text_content,
                                        updated_at = NOW()
                                """, (efta, text, dataset, file_path))
                                records_imported += 1
                            except Exception as row_err:
                                # Skip individual row errors
                                continue
                                
                    self.conn.commit()
                    total_rows += records_imported
                    
                self.tracker.update_progress("parquet_import", i + 1, f"{file_path}: {records_imported} rows")
                
            except Exception as e:
                self.conn.rollback()
                self.tracker.logger.error(f"Error processing {file_path}: {e}")
                continue
                
        self.tracker.complete_operation("parquet_import", f"Total rows: {total_rows}")
        return total_rows
        
    def download_file(self, url: str, dest_path: str, desc: str = "") -> bool:
        """Download file with progress tracking."""
        self.tracker.start_operation(f"download_{desc}", details=f"{url} -> {dest_path}")
        
        if self.dry_run:
            self.tracker.logger.info(f"[DRY-RUN] Would download {url}")
            return True
            
        if os.path.exists(dest_path):
            size = os.path.getsize(dest_path)
            self.tracker.complete_operation(f"download_{desc}", f"Already exists ({size} bytes)")
            return True
            
        try:
            # Use aria2c for fast download
            cmd = [
                "aria2c",
                "-x", "4",  # 4 connections
                "-s", "4",  # 4 splits
                "--continue=true",
                "--summary-interval=10",
                "-d", str(Path(dest_path).parent),
                "-o", str(Path(dest_path).name),
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                size = os.path.getsize(dest_path) if os.path.exists(dest_path) else 0
                self.tracker.complete_operation(f"download_{desc}", f"Downloaded {size} bytes")
                return True
            else:
                self.tracker.fail_operation(f"download_{desc}", result.stderr)
                return False
                
        except Exception as e:
            self.tracker.fail_operation(f"download_{desc}", str(e))
            return False
            
    def run_imports(self, source_filter: Optional[str] = None):
        """Run all configured imports."""
        self.tracker.logger.info("=" * 80)
        self.tracker.logger.info("STARTING DATA IMPORTS")
        self.tracker.logger.info("=" * 80)
        
        # Sort by priority
        sources = sorted(DATA_SOURCES.items(), key=lambda x: x[1].get("priority", 99))
        
        for source_name, config in sources:
            if source_filter and source_name != source_filter:
                continue
                
            self.tracker.logger.info(f"\n--- Processing source: {source_name} ---")
            
            # Handle different source types
            if "files" in config:
                # JSON/CSV imports
                for filename, table, filetype in config["files"]:
                    file_path = os.path.join(config["path"], filename)
                    
                    if filetype == "json":
                        self.import_json_to_staging(file_path, table, f"{source_name}_{filename}")
                    elif filetype == "csv":
                        self.import_csv_to_staging(file_path, table, f"{source_name}_{filename}")
                        
            elif "pattern" in config and config["pattern"] == "*.parquet":
                # Parquet processing
                self.process_parquet_directory(config["path"], config["target_table"])
                
    def run_downloads(self):
        """Run all configured downloads."""
        self.tracker.logger.info("=" * 80)
        self.tracker.logger.info("STARTING DOWNLOADS")
        self.tracker.logger.info("=" * 80)
        
        # jmail emails
        if "jmail" in DATA_SOURCES:
            config = DATA_SOURCES["jmail"]
            self.download_file(config["url"], config["path"], "jmail_emails")
            
    def create_staging_tables(self):
        """Create staging tables for imports if they don't exist."""
        if self.dry_run:
            return

        ddl = """
        -- Staging table for JSON imports
        CREATE TABLE IF NOT EXISTS json_import_staging (
            id SERIAL PRIMARY KEY,
            source_file TEXT,
            data JSONB,
            imported_at TIMESTAMP DEFAULT NOW()
        );

        -- Staging table for CSV imports
        CREATE TABLE IF NOT EXISTS csv_import_staging (
            id SERIAL PRIMARY KEY,
            source_file TEXT,
            row_data JSONB,
            imported_at TIMESTAMP DEFAULT NOW()
        );

        -- Index for faster queries
        CREATE INDEX IF NOT EXISTS idx_json_staging_file ON json_import_staging(source_file);
        CREATE INDEX IF NOT EXISTS idx_json_staging_data ON json_import_staging USING GIN (data);
        CREATE INDEX IF NOT EXISTS idx_csv_staging_file ON csv_import_staging(source_file);
        """

        with self.conn.cursor() as cur:
            cur.execute(ddl)
            self.conn.commit()

        self.tracker.logger.info("✓ Staging tables created/verified")


def main():
    parser = argparse.ArgumentParser(description="Master Data Unification Script")
    parser.add_argument("--all", action="store_true", help="Run all operations")
    parser.add_argument("--import-only", action="store_true", help="Run imports only")
    parser.add_argument("--download-only", action="store_true", help="Run downloads only")
    parser.add_argument("--source", type=str, help="Specific source to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--background", action="store_true", help="Run in background mode")
    
    args = parser.parse_args()
    
    if args.background:
        # Re-run without background flag
        cmd = [sys.executable, __file__] + [a for a in sys.argv[1:] if a != "--background"]
        log_file = f"{LOG_DIR}/unify_bg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        with open(log_file, 'w') as f:
            subprocess.Popen(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=PROJECT_ROOT
            )
        print(f"Background process started. Log: {log_file}")
        return 0
        
    unifier = DataUnifier(dry_run=args.dry_run)
    
    if not unifier.connect():
        return 1
        
    try:
        unifier.create_staging_tables()
        
        if args.download_only or args.all:
            unifier.run_downloads()
            
        if args.import_only or args.all:
            unifier.run_imports(source_filter=args.source)
            
        # Print summary
        print(unifier.tracker.summary())
        
    finally:
        unifier.close()
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
