#!/usr/bin/env python3
"""
EFTA Crosswalk Builder - Document Provenance Tracker

Scans all data sources (PostgreSQL, raw files, HF datasets) and builds
a comprehensive crosswalk table using EFTA numbers as canonical IDs.

Usage:
  python build_efta_crosswalk.py --scan-postgresql
  python build_efta_crosswalk.py --scan-raw-files
  python build_efta_crosswalk.py --scan-hf-datasets
  python build_efta_crosswalk.py --full-sync          # Scan all sources
  python build_efta_crosswalk.py --analyze            # Show overlap analysis
  python build_efta_crosswalk.py --validate           # Run QA validation
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Configuration
PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = os.environ.get("PG_PASSWORD", "")
PG_DB = "epstein"

EPSTEIN_DATA = "/home/cbwinslow/workspace/epstein-data"
EPSTEIN_PROJECT = "/home/cbwinslow/workspace/epstein"


class EFTACrosswalkBuilder:
    """Build and maintain EFTA crosswalk table."""
    
    def __init__(self):
        self.conn = None
        self.stats = {
            'postgresql': 0,
            'raw_files': 0,
            'hf_ocr_complete': 0,
            'hf_house_oversight': 0,
            'hf_embeddings': 0,
            'hf_emails': 0,
        }
    
    def connect(self):
        """Connect to PostgreSQL."""
        self.conn = psycopg2.connect(
            host=PG_HOST, port=PG_PORT,
            user=PG_USER, password=PG_PASS,
            dbname=PG_DB
        )
        print("✓ Connected to PostgreSQL")
    
    def ensure_table(self):
        """Ensure efta_crosswalk table exists."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS efta_crosswalk (
                    efta_number VARCHAR(50) PRIMARY KEY,
                    in_postgresql BOOLEAN DEFAULT FALSE,
                    in_raw_files BOOLEAN DEFAULT FALSE,
                    in_hf_ocr_complete BOOLEAN DEFAULT FALSE,
                    in_hf_house_oversight BOOLEAN DEFAULT FALSE,
                    in_hf_embeddings BOOLEAN DEFAULT FALSE,
                    in_hf_emails BOOLEAN DEFAULT FALSE,
                    postgresql_dataset INTEGER,
                    postgresql_ingested_at TIMESTAMP,
                    raw_file_path TEXT,
                    raw_file_size BIGINT,
                    hf_dataset_name TEXT,
                    hf_downloaded_at TIMESTAMP,
                    has_ocr BOOLEAN DEFAULT FALSE,
                    has_embeddings BOOLEAN DEFAULT FALSE,
                    has_entities BOOLEAN DEFAULT FALSE,
                    has_classification BOOLEAN DEFAULT FALSE,
                    content_hash TEXT,
                    last_verified_at TIMESTAMP,
                    verification_status VARCHAR(20) DEFAULT 'unknown',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            print("✓ EFTA crosswalk table ready")
    
    def scan_postgresql(self, batch_size: int = 10000) -> int:
        """Scan PostgreSQL and populate crosswalk."""
        print("\n[1/4] Scanning PostgreSQL documents...")
        
        count = 0
        offset = 0
        
        while True:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT efta_number, dataset, created_at
                    FROM documents
                    ORDER BY id
                    LIMIT %s OFFSET %s
                """, (batch_size, offset))
                
                rows = cur.fetchall()
                if not rows:
                    break
                
                # Prepare data for upsert
                data = [
                    (efta, True, dataset, ingested)
                    for efta, dataset, ingested in rows
                ]
                
                # Upsert into crosswalk
                execute_values(
                    cur,
                    """
                    INSERT INTO efta_crosswalk 
                    (efta_number, in_postgresql, postgresql_dataset, postgresql_ingested_at)
                    VALUES %s
                    ON CONFLICT (efta_number) 
                    DO UPDATE SET
                        in_postgresql = TRUE,
                        postgresql_dataset = EXCLUDED.postgresql_dataset,
                        postgresql_ingested_at = EXCLUDED.postgresql_ingested_at,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    data
                )
                
                self.conn.commit()
                count += len(rows)
                offset += batch_size
                
                if offset % 100000 == 0:
                    print(f"  Processed {count:,} documents...")
        
        self.stats['postgresql'] = count
        print(f"✓ PostgreSQL: {count:,} documents mapped")
        return count
    
    def scan_raw_files(self) -> int:
        """Scan raw-files directory and map EFTA numbers."""
        print("\n[2/4] Scanning raw files...")
        
        raw_path = Path(EPSTEIN_DATA) / "raw-files"
        if not raw_path.exists():
            print("✗ raw-files directory not found")
            return 0
        
        efta_files = []
        
        for dataset_dir in raw_path.iterdir():
            if not dataset_dir.is_dir():
                continue
            
            dataset_name = dataset_dir.name
            pdf_files = list(dataset_dir.glob("EFTA*.pdf"))
            
            for pdf_file in pdf_files:
                efta = pdf_file.stem  # EFTA00000001
                file_size = pdf_file.stat().st_size
                rel_path = str(pdf_file.relative_to(EPSTEIN_DATA))
                
                efta_files.append((efta, True, rel_path, file_size))
        
        # Batch insert
        with self.conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO efta_crosswalk 
                (efta_number, in_raw_files, raw_file_path, raw_file_size)
                VALUES %s
                ON CONFLICT (efta_number) 
                DO UPDATE SET
                    in_raw_files = TRUE,
                    raw_file_path = EXCLUDED.raw_file_path,
                    raw_file_size = EXCLUDED.raw_file_size,
                    updated_at = CURRENT_TIMESTAMP
                """,
                efta_files
            )
            self.conn.commit()
        
        self.stats['raw_files'] = len(efta_files)
        print(f"✓ Raw files: {len(efta_files):,} PDFs mapped")
        return len(efta_files)
    
    def scan_hf_dataset(self, dataset_name: str, parquet_path: str) -> int:
        """Scan a HuggingFace parquet dataset."""
        print(f"\n[3/4] Scanning HF dataset: {dataset_name}...")
        
        if not os.path.exists(parquet_path):
            print(f"✗ Dataset not found: {parquet_path}")
            return 0
        
        try:
            # Read parquet file
            df = pd.read_parquet(parquet_path, columns=['document_id'])
            efta_numbers = df['document_id'].tolist()
            
            # Determine which source flag to update
            source_column = {
                'hf-ocr-complete': 'in_hf_ocr_complete',
                'hf-house-oversight': 'in_hf_house_oversight',
                'hf-embeddings': 'in_hf_embeddings',
                'hf-emails': 'in_hf_emails',
            }.get(dataset_name, 'in_hf_ocr_complete')
            
            # Batch insert
            batch_size = 10000
            total = len(efta_numbers)
            
            with self.conn.cursor() as cur:
                for i in range(0, total, batch_size):
                    batch = efta_numbers[i:i+batch_size]
                    
                    # Create parameterized query
                    placeholders = ','.join(['%s'] * len(batch))
                    cur.execute(f"""
                        INSERT INTO efta_crosswalk (efta_number, hf_dataset_name, {source_column})
                        VALUES UNNEST(ARRAY[{placeholders}]), %s, TRUE
                        ON CONFLICT (efta_number) 
                        DO UPDATE SET
                            hf_dataset_name = EXCLUDED.hf_dataset_name,
                            {source_column} = TRUE,
                            updated_at = CURRENT_TIMESTAMP
                    """, batch + [dataset_name])
                    
                    self.conn.commit()
                    
                    if (i + batch_size) % 50000 == 0:
                        print(f"  Processed {min(i+batch_size, total):,}/{total:,}...")
            
            self.stats[dataset_name.replace('-', '_')] = total
            print(f"✓ {dataset_name}: {total:,} documents mapped")
            return total
            
        except Exception as e:
            print(f"✗ Error scanning {dataset_name}: {e}")
            return 0
    
    def scan_all_hf_datasets(self) -> Dict[str, int]:
        """Scan all available HF datasets."""
        results = {}
        
        datasets = {
            'hf-ocr-complete': f"{EPSTEIN_DATA}/hf-ocr-complete/data/dataset.parquet",
            'hf-house-oversight': f"{EPSTEIN_DATA}/hf-house-oversight/data/*.parquet",
            'hf-embeddings': f"{EPSTEIN_DATA}/hf-embeddings/data/*.parquet",
            'hf-emails': f"{EPSTEIN_DATA}/hf-emails-threads/data/*.parquet",
        }
        
        for name, pattern in datasets.items():
            if '*' in pattern:
                # Find parquet files
                import glob
                files = glob.glob(pattern)
                if files:
                    count = self.scan_hf_dataset(name, files[0])
                    results[name] = count
            elif os.path.exists(pattern):
                count = self.scan_hf_dataset(name, pattern)
                results[name] = count
        
        return results
    
    def update_data_quality_flags(self):
        """Update has_ocr, has_embeddings flags based on existing tables."""
        print("\n[4/4] Updating data quality flags...")
        
        with self.conn.cursor() as cur:
            # Mark documents with OCR
            cur.execute("""
                UPDATE efta_crosswalk ec
                SET has_ocr = TRUE
                FROM ocr_results o
                WHERE ec.efta_number = o.efta_number
                  AND ec.has_ocr = FALSE
            """)
            ocr_count = cur.rowcount
            
            # Mark documents with embeddings
            cur.execute("""
                UPDATE efta_crosswalk ec
                SET has_embeddings = TRUE
                FROM (
                    SELECT DISTINCT p.efta_number
                    FROM pages p
                    JOIN page_embeddings pe ON p.id = pe.page_id
                ) sub
                WHERE ec.efta_number = sub.efta_number
                  AND ec.has_embeddings = FALSE
            """)
            embedding_count = cur.rowcount
            
            # Mark documents with entities
            cur.execute("""
                UPDATE efta_crosswalk ec
                SET has_entities = TRUE
                FROM (
                    SELECT DISTINCT efta_number FROM document_entities
                ) sub
                WHERE ec.efta_number = sub.efta_number
                  AND ec.has_entities = FALSE
            """)
            entity_count = cur.rowcount
            
            self.conn.commit()
        
        print(f"✓ Data quality flags updated:")
        print(f"  - {ocr_count:,} with OCR")
        print(f"  - {embedding_count:,} with embeddings")
        print(f"  - {entity_count:,} with entities")
    
    def analyze_coverage(self):
        """Print coverage analysis."""
        print("\n" + "="*80)
        print("EFTA COVERAGE ANALYSIS")
        print("="*80)
        
        with self.conn.cursor() as cur:
            # Source coverage
            cur.execute("SELECT * FROM efta_source_coverage")
            row = cur.fetchone()
            
            if row:
                print(f"\nTotal Unique EFTA Numbers: {row[0]:,}")
                print(f"\nBy Source:")
                print(f"  PostgreSQL:           {row[1]:>10,}")
                print(f"  Raw Files:            {row[2]:>10,}")
                print(f"  HF OCR Complete:      {row[3]:>10,}")
                print(f"  HF House Oversight:   {row[4]:>10,}")
                print(f"  HF Embeddings:        {row[5]:>10,}")
                print(f"  HF Emails:            {row[6]:>10,}")
                
                print(f"\nOverlap Analysis:")
                print(f"  In both PG and HF OCR:    {row[7]:>10,}")
                print(f"  PostgreSQL only:          {row[8]:>10,}")
                print(f"  HF OCR only (not in PG):  {row[9]:>10,}")
                
                print(f"\nData Quality:")
                print(f"  With OCR:         {row[10]:>10,}")
                print(f"  With Embeddings:  {row[11]:>10,}")
                print(f"  With Entities:    {row[12]:>10,}")
        
        print("\n" + "="*80)
    
    def validate(self):
        """Run validation checks."""
        print("\n" + "="*80)
        print("VALIDATION CHECKS")
        print("="*80)
        
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM validate_efta_crosswalk()")
            rows = cur.fetchall()
            
            for check_name, status, details, severity in rows:
                symbol = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
                print(f"{symbol} [{severity}] {check_name}: {status}")
                if details:
                    print(f"   {details}")
        
        print("\n" + "="*80)
    
    def run_full_sync(self):
        """Run complete synchronization of all sources."""
        print("\n" + "="*80)
        print("EFTA CROSSWALK FULL SYNC")
        print("="*80)
        
        self.connect()
        self.ensure_table()
        
        # Scan all sources
        self.scan_postgresql()
        self.scan_raw_files()
        self.scan_all_hf_datasets()
        self.update_data_quality_flags()
        
        # Analysis
        self.analyze_coverage()
        self.validate()
        
        self.conn.close()
        print("\n✓ Full sync complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Build and maintain EFTA crosswalk for document provenance"
    )
    parser.add_argument(
        "--scan-postgresql", action="store_true",
        help="Scan PostgreSQL documents"
    )
    parser.add_argument(
        "--scan-raw-files", action="store_true",
        help="Scan raw-files directory"
    )
    parser.add_argument(
        "--scan-hf-datasets", action="store_true",
        help="Scan HF datasets"
    )
    parser.add_argument(
        "--full-sync", action="store_true",
        help="Sync all sources (full rebuild)"
    )
    parser.add_argument(
        "--analyze", action="store_true",
        help="Show coverage analysis"
    )
    parser.add_argument(
        "--validate", action="store_true",
        help="Run validation checks"
    )
    
    args = parser.parse_args()
    
    if not any([args.scan_postgresql, args.scan_raw_files, args.scan_hf_datasets, 
                args.full_sync, args.analyze, args.validate]):
        parser.print_help()
        return 1
    
    builder = EFTACrosswalkBuilder()
    
    if args.full_sync:
        builder.run_full_sync()
    else:
        builder.connect()
        builder.ensure_table()
        
        if args.scan_postgresql:
            builder.scan_postgresql()
        if args.scan_raw_files:
            builder.scan_raw_files()
        if args.scan_hf_datasets:
            builder.scan_all_hf_datasets()
        if args.analyze:
            builder.analyze_coverage()
        if args.validate:
            builder.validate()
        
        builder.conn.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
