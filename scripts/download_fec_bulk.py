#!/usr/bin/env python3
"""
FEC Data Download and Ingest Script
Downloads bulk FEC data and ingests into PostgreSQL
Uses API for targeted Epstein-related entity searches
"""

import os
import sys
import zipfile
import csv
import psycopg2
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from io import StringIO

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_KEY = os.getenv('FEC_API_KEY', 'FpB5TzG4hjf7W9IwjBsdTKGyQImqhhidMKRLDXFm')
BASE_URL = 'https://www.fec.gov/files/bulk-downloads'
API_BASE = 'https://api.open.fec.gov/v1'
DATA_DIR = Path('/mnt/data/epstein-project/raw-files/fec')
YEARS = list(range(1980, 2027, 2))  # 1980-2026 (FEC cycles are 2-year periods)

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'epstein',
    'user': 'cbwinslow',
    'password': '123qweasd'
}

# FEC bulk file types to download
BULK_FILES = {
    'indiv': {  # Individual contributions - MOST IMPORTANT
        'description': 'Contributions by individuals',
        'filename': 'indiv{}.zip',
        'format': 'two_digit',  # Uses 2-digit year (e.g., 26 for 2026)
        'size_gb': 2.5,  # Approximate per cycle
        'priority': 1
    },
    'cm': {  # Committee master
        'description': 'Committee master file',
        'filename': 'cm{}.zip',
        'format': 'two_digit',
        'size_gb': 0.1,
        'priority': 2
    },
    'cn': {  # Candidate master
        'description': 'Candidate master file',
        'filename': 'cn{}.zip',
        'format': 'two_digit',
        'size_gb': 0.05,
        'priority': 2
    },
    'ccl': {  # Candidate-committee linkage
        'description': 'Candidate-committee linkage',
        'filename': 'ccl{}.zip',
        'format': 'two_digit',
        'size_gb': 0.05,
        'priority': 3
    },
    'oth': {  # Committee-to-committee contributions
        'description': 'Contributions from committees',
        'filename': 'oth{}.zip',
        'format': 'two_digit',
        'size_gb': 0.2,
        'priority': 3
    },
    'pas2': {  # Contributions to candidates
        'description': 'Contributions to candidates',
        'filename': 'pas2{}.zip',
        'format': 'two_digit',
        'size_gb': 0.5,
        'priority': 3
    },
    'oppexp': {  # Operating expenditures
        'description': 'Operating expenditures',
        'filename': 'oppexp{}.zip',
        'format': 'two_digit',
        'size_gb': 1.0,
        'priority': 4
    }
}


class FECDownloader:
    """Download and ingest FEC bulk data"""

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.cursor = None

    def connect_db(self):
        """Connect to PostgreSQL"""
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        logger.info("Connected to PostgreSQL")

    def close_db(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("Disconnected from PostgreSQL")

    def create_tables(self):
        """Create FEC tables if they don't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fec_individual_contributions (
                id SERIAL PRIMARY KEY,
                cmte_id VARCHAR(9),
                amndt_ind VARCHAR(1),
                rpt_tp VARCHAR(3),
                transaction_pgi VARCHAR(5),
                image_num VARCHAR(18),
                transaction_tp VARCHAR(3),
                entity_tp VARCHAR(3),
                name TEXT,
                city TEXT,
                state VARCHAR(2),
                zip_code VARCHAR(9),
                employer TEXT,
                occupation TEXT,
                transaction_dt DATE,
                transaction_amt NUMERIC(14,2),
                other_id VARCHAR(9),
                tran_id VARCHAR(32),
                file_num BIGINT,
                memo_cd VARCHAR(1),
                memo_text TEXT,
                sub_id BIGINT UNIQUE,
                cycle INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS fec_committees (
                id SERIAL PRIMARY KEY,
                cmte_id VARCHAR(9) UNIQUE,
                cmte_nm TEXT,
                tres_nm TEXT,
                cmte_tp VARCHAR(1),
                cmte_dsgn VARCHAR(1),
                cmte_filing_freq VARCHAR(1),
                org_tp VARCHAR(1),
                connected_org_nm TEXT,
                cand_id VARCHAR(9),
                cycle INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS fec_candidates (
                id SERIAL PRIMARY KEY,
                cand_id VARCHAR(9) UNIQUE,
                cand_name TEXT,
                cand_pty_affiliation VARCHAR(3),
                cand_election_yr INTEGER,
                cand_office VARCHAR(1),
                cand_office_st VARCHAR(2),
                cand_office_district VARCHAR(2),
                cand_ici VARCHAR(1),
                cand_status VARCHAR(1),
                cand_pcc VARCHAR(9),
                cycle INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS fec_committee_contributions (
                id SERIAL PRIMARY KEY,
                cmte_id VARCHAR(9),
                amndt_ind VARCHAR(1),
                rpt_tp VARCHAR(3),
                transaction_pgi VARCHAR(5),
                image_num VARCHAR(18),
                transaction_tp VARCHAR(3),
                entity_tp VARCHAR(3),
                name TEXT,
                city TEXT,
                state VARCHAR(2),
                zip_code VARCHAR(9),
                employer TEXT,
                occupation TEXT,
                transaction_dt DATE,
                transaction_amt NUMERIC(14,2),
                other_id VARCHAR(9),
                tran_id VARCHAR(32),
                file_num BIGINT,
                memo_cd VARCHAR(1),
                memo_text TEXT,
                sub_id BIGINT UNIQUE,
                cycle INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS fec_candidate_contributions (
                id SERIAL PRIMARY KEY,
                cmte_id VARCHAR(9),
                amndt_ind VARCHAR(1),
                rpt_tp VARCHAR(3),
                transaction_pgi VARCHAR(5),
                image_num VARCHAR(18),
                transaction_tp VARCHAR(3),
                entity_tp VARCHAR(3),
                name TEXT,
                city TEXT,
                state VARCHAR(2),
                zip_code VARCHAR(9),
                employer TEXT,
                occupation TEXT,
                transaction_dt DATE,
                transaction_amt NUMERIC(14,2),
                other_id VARCHAR(9),
                cand_id VARCHAR(9),
                tran_id VARCHAR(32),
                file_num BIGINT,
                memo_cd VARCHAR(1),
                memo_text TEXT,
                sub_id BIGINT UNIQUE,
                cycle INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS fec_operating_expenditures (
                id SERIAL PRIMARY KEY,
                cmte_id VARCHAR(9),
                amndt_ind VARCHAR(1),
                rpt_yr INTEGER,
                rpt_tp VARCHAR(3),
                image_num VARCHAR(18),
                line_num VARCHAR(3),
                form_tp_cd VARCHAR(8),
                sched_tp_cd VARCHAR(8),
                name TEXT,
                city TEXT,
                state VARCHAR(2),
                zip_code VARCHAR(9),
                transaction_dt DATE,
                transaction_amt NUMERIC(14,2),
                transaction_pgi VARCHAR(5),
                purpose TEXT,
                category TEXT,
                category_desc TEXT,
                memo_cd VARCHAR(1),
                memo_text TEXT,
                entity_tp VARCHAR(3),
                sub_id BIGINT UNIQUE,
                file_num BIGINT,
                cycle INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS fec_download_log (
                id SERIAL PRIMARY KEY,
                file_type VARCHAR(20),
                cycle INTEGER,
                download_date TIMESTAMP,
                file_size BIGINT,
                rows_imported INTEGER,
                status VARCHAR(20),
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_fec_indiv_name ON fec_individual_contributions(name);
            CREATE INDEX IF NOT EXISTS idx_fec_indiv_employer ON fec_individual_contributions(employer);
            CREATE INDEX IF NOT EXISTS idx_fec_indiv_date ON fec_individual_contributions(transaction_dt);
            CREATE INDEX IF NOT EXISTS idx_fec_indiv_zip ON fec_individual_contributions(zip_code);
            CREATE INDEX IF NOT EXISTS idx_fec_indiv_subid ON fec_individual_contributions(sub_id);
            CREATE INDEX IF NOT EXISTS idx_fec_cmte_id ON fec_committees(cmte_id);
            CREATE INDEX IF NOT EXISTS idx_fec_cand_id ON fec_candidates(cand_id);
        """)
        self.conn.commit()
        logger.info("FEC tables created/verified")

    def download_file(self, url: str, dest_path: Path) -> bool:
        """Download a file with progress logging"""
        try:
            logger.info(f"Downloading {url}")
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0 and downloaded % (1024 * 1024) == 0:  # Every MB
                            progress = (downloaded / total_size) * 100
                            logger.info(f"Progress: {progress:.1f}% ({downloaded // 1024 // 1024}MB / {total_size // 1024 // 1024}MB)")

            logger.info(f"Downloaded: {dest_path} ({downloaded // 1024 // 1024}MB)")
            return True

        except Exception as e:
            logger.error(f"Download failed: {url} - {e}")
            return False

    def extract_and_ingest_zip(self, zip_path: Path, file_type: str, cycle: int) -> int:
        """Extract ZIP and ingest CSV data in chunks"""
        rows_imported = 0
        chunk_size = 100000  # Process 100K rows at a time

        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                for filename in z.namelist():
                    if not filename.endswith('.txt'):
                        continue

                    logger.info(f"Processing {filename} in chunks of {chunk_size}")

                    with z.open(filename) as f:
                        # Read first line to detect delimiter
                        first_line = f.readline().decode('utf-8', errors='ignore')
                        f.seek(0)

                        # Determine delimiter (usually | for FEC files)
                        delimiter = '|' if '|' in first_line else ','

                        # Process in chunks
                        chunk_iter = pd.read_csv(
                            f,
                            delimiter=delimiter,
                            quoting=csv.QUOTE_NONE,
                            dtype=str,
                            low_memory=False,
                            on_bad_lines='skip',
                            encoding='utf-8',
                            chunksize=chunk_size
                        )

                        for i, chunk in enumerate(chunk_iter):
                            # Clean column names
                            chunk.columns = [col.strip().lower().replace(' ', '_') for col in chunk.columns]
                            chunk['cycle'] = cycle

                            # Insert data based on file type
                            if file_type == 'indiv':
                                rows = self.ingest_individual_contributions_chunk(chunk)
                            elif file_type == 'cm':
                                rows = self.ingest_committees_chunk(chunk)
                            elif file_type == 'cn':
                                rows = self.ingest_candidates_chunk(chunk)
                            elif file_type == 'oth':
                                rows = self.ingest_committee_contributions_chunk(chunk)
                            elif file_type == 'pas2':
                                rows = self.ingest_candidate_contributions_chunk(chunk)
                            elif file_type == 'oppexp':
                                rows = self.ingest_operating_expenditures_chunk(chunk)
                            else:
                                rows = 0

                            rows_imported += rows

                            if (i + 1) % 10 == 0:
                                logger.info(f"  Processed chunk {i+1}, total rows: {rows_imported:,}")

                        logger.info(f"Finished processing {filename}: {rows_imported:,} total rows")

        except Exception as e:
            logger.error(f"Error processing {zip_path}: {e}")
            import traceback
            logger.error(traceback.format_exc())

        return rows_imported

    def ingest_individual_contributions_chunk(self, df: pd.DataFrame) -> int:
        """Ingest a chunk of individual contributions"""
        rows = []
        for _, row in df.iterrows():
            try:
                transaction_dt = None
                if 'transaction_dt' in row and pd.notna(row['transaction_dt']):
                    try:
                        transaction_dt = pd.to_datetime(row['transaction_dt'], format='%m%d%Y', errors='coerce')
                    except:
                        pass

                rows.append((
                    row.get('cmte_id', ''),
                    row.get('amndt_ind', ''),
                    row.get('rpt_tp', ''),
                    row.get('transaction_pgi', ''),
                    row.get('image_num', ''),
                    row.get('transaction_tp', ''),
                    row.get('entity_tp', ''),
                    row.get('name', ''),
                    row.get('city', ''),
                    row.get('state', ''),
                    row.get('zip_code', ''),
                    row.get('employer', ''),
                    row.get('occupation', ''),
                    transaction_dt,
                    float(row.get('transaction_amt', 0) or 0),
                    row.get('other_id', ''),
                    row.get('tran_id', ''),
                    int(row.get('file_num', 0) or 0) if pd.notna(row.get('file_num')) else None,
                    row.get('memo_cd', ''),
                    row.get('memo_text', ''),
                    int(row.get('sub_id', 0) or 0) if pd.notna(row.get('sub_id')) else None,
                    int(row.get('cycle', 0))
                ))
            except Exception as e:
                continue

        if rows:
            self.cursor.executemany("""
                INSERT INTO fec_individual_contributions (
                    cmte_id, amndt_ind, rpt_tp, transaction_pgi, image_num,
                    transaction_tp, entity_tp, name, city, state, zip_code,
                    employer, occupation, transaction_dt, transaction_amt,
                    other_id, tran_id, file_num, memo_cd, memo_text, sub_id, cycle
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (sub_id) DO NOTHING
            """, rows)
            self.conn.commit()

        return len(rows)

    def ingest_committees_chunk(self, df: pd.DataFrame) -> int:
        """Ingest a chunk of committee data"""
        rows = []
        for _, row in df.iterrows():
            try:
                rows.append((
                    row.get('cmte_id', ''),
                    row.get('cmte_nm', ''),
                    row.get('tres_nm', ''),
                    row.get('cmte_tp', ''),
                    row.get('cmte_dsgn', ''),
                    row.get('cmte_filing_freq', ''),
                    row.get('org_tp', ''),
                    row.get('connected_org_nm', ''),
                    row.get('cand_id', ''),
                    int(row.get('cycle', 0))
                ))
            except:
                continue

        if rows:
            self.cursor.executemany("""
                INSERT INTO fec_committees (cmte_id, cmte_nm, tres_nm, cmte_tp, cmte_dsgn,
                    cmte_filing_freq, org_tp, connected_org_nm, cand_id, cycle)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cmte_id) DO UPDATE SET
                    cmte_nm = EXCLUDED.cmte_nm, tres_nm = EXCLUDED.tres_nm, cycle = EXCLUDED.cycle
            """, rows)
            self.conn.commit()

        return len(rows)

    def ingest_candidates_chunk(self, df: pd.DataFrame) -> int:
        """Ingest a chunk of candidate data"""
        rows = []
        for _, row in df.iterrows():
            try:
                rows.append((
                    row.get('cand_id', ''),
                    row.get('cand_name', ''),
                    row.get('cand_pty_affiliation', ''),
                    int(row.get('cand_election_yr', 0) or 0) if pd.notna(row.get('cand_election_yr')) else None,
                    row.get('cand_office', ''),
                    row.get('cand_office_st', ''),
                    row.get('cand_office_district', ''),
                    row.get('cand_ici', ''),
                    row.get('cand_status', ''),
                    row.get('cand_pcc', ''),
                    int(row.get('cycle', 0))
                ))
            except:
                continue

        if rows:
            self.cursor.executemany("""
                INSERT INTO fec_candidates (cand_id, cand_name, cand_pty_affiliation, cand_election_yr,
                    cand_office, cand_office_st, cand_office_district, cand_ici, cand_status, cand_pcc, cycle)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cand_id) DO UPDATE SET
                    cand_name = EXCLUDED.cand_name, cand_election_yr = EXCLUDED.cand_election_yr, cycle = EXCLUDED.cycle
            """, rows)
            self.conn.commit()

        return len(rows)

    def ingest_committee_contributions_chunk(self, df: pd.DataFrame) -> int:
        """Ingest a chunk of committee contributions"""
        rows = []
        for _, row in df.iterrows():
            try:
                transaction_dt = None
                if 'transaction_dt' in row and pd.notna(row['transaction_dt']):
                    try:
                        transaction_dt = pd.to_datetime(row['transaction_dt'], format='%m%d%Y', errors='coerce')
                    except:
                        pass

                rows.append((
                    row.get('cmte_id', ''), row.get('amndt_ind', ''), row.get('rpt_tp', ''),
                    row.get('transaction_pgi', ''), row.get('image_num', ''), row.get('transaction_tp', ''),
                    row.get('entity_tp', ''), row.get('name', ''), row.get('city', ''), row.get('state', ''),
                    row.get('zip_code', ''), row.get('employer', ''), row.get('occupation', ''),
                    transaction_dt, float(row.get('transaction_amt', 0) or 0), row.get('other_id', ''),
                    row.get('tran_id', ''), int(row.get('file_num', 0) or 0) if pd.notna(row.get('file_num')) else None,
                    row.get('memo_cd', ''), row.get('memo_text', ''),
                    int(row.get('sub_id', 0) or 0) if pd.notna(row.get('sub_id')) else None,
                    int(row.get('cycle', 0))
                ))
            except:
                continue

        if rows:
            self.cursor.executemany("""
                INSERT INTO fec_committee_contributions (
                    cmte_id, amndt_ind, rpt_tp, transaction_pgi, image_num, transaction_tp, entity_tp,
                    name, city, state, zip_code, employer, occupation, transaction_dt, transaction_amt,
                    other_id, tran_id, file_num, memo_cd, memo_text, sub_id, cycle
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (sub_id) DO NOTHING
            """, rows)
            self.conn.commit()

        return len(rows)

    def ingest_candidate_contributions_chunk(self, df: pd.DataFrame) -> int:
        """Ingest a chunk of candidate contributions"""
        rows = []
        for _, row in df.iterrows():
            try:
                transaction_dt = None
                if 'transaction_dt' in row and pd.notna(row['transaction_dt']):
                    try:
                        transaction_dt = pd.to_datetime(row['transaction_dt'], format='%m%d%Y', errors='coerce')
                    except:
                        pass

                rows.append((
                    row.get('cmte_id', ''), row.get('amndt_ind', ''), row.get('rpt_tp', ''),
                    row.get('transaction_pgi', ''), row.get('image_num', ''), row.get('transaction_tp', ''),
                    row.get('entity_tp', ''), row.get('name', ''), row.get('city', ''), row.get('state', ''),
                    row.get('zip_code', ''), row.get('employer', ''), row.get('occupation', ''),
                    transaction_dt, float(row.get('transaction_amt', 0) or 0), row.get('other_id', ''),
                    row.get('cand_id', ''), row.get('tran_id', ''),
                    int(row.get('file_num', 0) or 0) if pd.notna(row.get('file_num')) else None,
                    row.get('memo_cd', ''), row.get('memo_text', ''),
                    int(row.get('sub_id', 0) or 0) if pd.notna(row.get('sub_id')) else None,
                    int(row.get('cycle', 0))
                ))
            except:
                continue

        if rows:
            self.cursor.executemany("""
                INSERT INTO fec_candidate_contributions (
                    cmte_id, amndt_ind, rpt_tp, transaction_pgi, image_num, transaction_tp, entity_tp,
                    name, city, state, zip_code, employer, occupation, transaction_dt, transaction_amt,
                    other_id, cand_id, tran_id, file_num, memo_cd, memo_text, sub_id, cycle
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (sub_id) DO NOTHING
            """, rows)
            self.conn.commit()

        return len(rows)

    def ingest_operating_expenditures_chunk(self, df: pd.DataFrame) -> int:
        """Ingest a chunk of operating expenditures"""
        rows = []
        for _, row in df.iterrows():
            try:
                transaction_dt = None
                if 'transaction_dt' in row and pd.notna(row['transaction_dt']):
                    try:
                        transaction_dt = pd.to_datetime(row['transaction_dt'], format='%m%d%Y', errors='coerce')
                    except:
                        pass

                rows.append((
                    row.get('cmte_id', ''), row.get('amndt_ind', ''),
                    int(row.get('rpt_yr', 0) or 0) if pd.notna(row.get('rpt_yr')) else None,
                    row.get('rpt_tp', ''), row.get('image_num', ''), row.get('line_num', ''),
                    row.get('form_tp_cd', ''), row.get('sched_tp_cd', ''), row.get('name', ''),
                    row.get('city', ''), row.get('state', ''), row.get('zip_code', ''),
                    transaction_dt, float(row.get('transaction_amt', 0) or 0), row.get('transaction_pgi', ''),
                    row.get('purpose', ''), row.get('category', ''), row.get('category_desc', ''),
                    row.get('memo_cd', ''), row.get('memo_text', ''), row.get('entity_tp', ''),
                    int(row.get('sub_id', 0) or 0) if pd.notna(row.get('sub_id')) else None,
                    int(row.get('file_num', 0) or 0) if pd.notna(row.get('file_num')) else None,
                    int(row.get('cycle', 0))
                ))
            except:
                continue

        if rows:
            self.cursor.executemany("""
                INSERT INTO fec_operating_expenditures (
                    cmte_id, amndt_ind, rpt_yr, rpt_tp, image_num, line_num, form_tp_cd, sched_tp_cd,
                    name, city, state, zip_code, transaction_dt, transaction_amt, transaction_pgi,
                    purpose, category, category_desc, memo_cd, memo_text, entity_tp, sub_id, file_num, cycle
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (sub_id) DO NOTHING
            """, rows)
            self.conn.commit()

        return len(rows)

    def download_cycle(self, file_type: str, cycle: int) -> bool:
        """Download and ingest data for a specific cycle"""
        config = BULK_FILES[file_type]
        # FEC uses 2-digit year in filename (e.g., 26 for 2026)
        two_digit_year = cycle % 100
        filename = config['filename'].format(two_digit_year)
        # URL uses 4-digit cycle year
        url = f"{BASE_URL}/{cycle}/{filename}"
        zip_path = self.data_dir / filename

        # Check if already downloaded
        if zip_path.exists():
            file_size = zip_path.stat().st_size
            logger.info(f"File exists: {zip_path} ({file_size // 1024 // 1024}MB)")
        else:
            # Download
            if not self.download_file(url, zip_path):
                return False

        # Extract and ingest
        logger.info(f"Ingesting {filename}...")
        rows = self.extract_and_ingest_zip(zip_path, file_type, cycle)

        # Log download
        self.cursor.execute("""
            INSERT INTO fec_download_log (file_type, cycle, download_date, file_size, rows_imported, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (file_type, cycle, datetime.now(), zip_path.stat().st_size, rows, 'success'))
        self.conn.commit()

        logger.info(f"Imported {rows} rows from {filename}")
        return True

    def download_all(self, file_types: Optional[List[str]] = None, cycles: Optional[List[int]] = None):
        """Download all specified file types and cycles"""
        if file_types is None:
            # Priority order: indiv first (most important), then others
            file_types = sorted(BULK_FILES.keys(), key=lambda x: BULK_FILES[x]['priority'])

        if cycles is None:
            # Focus on recent cycles + Epstein era (1990s-2000s)
            # Epstein was active politically from late 1990s through 2019
            cycles = [2024, 2022, 2020, 2018, 2016, 2014, 2012, 2010, 2008, 2006, 2004, 2002, 2000, 1998, 1996]

        self.connect_db()
        self.create_tables()

        try:
            for file_type in file_types:
                config = BULK_FILES[file_type]
                logger.info(f"\n{'='*60}")
                logger.info(f"Processing: {config['description']}")
                logger.info(f"{'='*60}")

                for cycle in cycles:
                    try:
                        self.download_cycle(file_type, cycle)
                    except Exception as e:
                        logger.error(f"Failed {file_type} cycle {cycle}: {e}")
                        continue

        finally:
            self.close_db()

    def search_epstein_entities_api(self, names: List[str]) -> List[Dict]:
        """Search FEC API for Epstein-related entities"""
        results = []

        for name in names:
            try:
                # Search individual contributions
                url = f"{API_BASE}/schedules/schedule_a/"
                params = {
                    'api_key': API_KEY,
                    'contributor_name': name,
                    'per_page': 100,
                    'sort': '-contribution_receipt_date'
                }

                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    results.extend(data.get('results', []))
                    logger.info(f"API search '{name}': {len(data.get('results', []))} results")

                # Respect rate limit (1000/hour = ~1 per 3.6 seconds)
                import time
                time.sleep(4)

            except Exception as e:
                logger.error(f"API search error for '{name}': {e}")

        return results

    def get_stats(self):
        """Get database statistics"""
        self.connect_db()

        tables = [
            'fec_individual_contributions',
            'fec_committees',
            'fec_candidates',
            'fec_committee_contributions',
            'fec_candidate_contributions',
            'fec_operating_expenditures'
        ]

        stats = {}
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            stats[table] = count

        self.close_db()
        return stats


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Download and ingest FEC bulk data')
    parser.add_argument('--download', action='store_true', help='Download all FEC data')
    parser.add_argument('--file-types', nargs='+', choices=list(BULK_FILES.keys()),
                        help='Specific file types to download')
    parser.add_argument('--cycles', nargs='+', type=int,
                        help='Specific cycles to download (e.g., 2024 2022)')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--search', nargs='+', help='Search API for specific names')
    parser.add_argument('--setup', action='store_true', help='Create tables only')

    args = parser.parse_args()

    downloader = FECDownloader()

    if args.setup:
        downloader.connect_db()
        downloader.create_tables()
        downloader.close_db()
        logger.info("Tables created successfully")

    elif args.download:
        file_types = args.file_types if args.file_types else None
        cycles = args.cycles if args.cycles else None
        downloader.download_all(file_types, cycles)

    elif args.stats:
        stats = downloader.get_stats()
        logger.info("\nFEC Database Statistics:")
        logger.info("=" * 60)
        for table, count in stats.items():
            logger.info(f"{table}: {count:,} rows")

    elif args.search:
        results = downloader.search_epstein_entities_api(args.search)
        logger.info(f"\nFound {len(results)} contributions matching: {args.search}")
        for r in results[:10]:  # Show first 10
            logger.info(f"  - {r.get('contributor_name')}: ${r.get('contribution_receipt_amount')} to {r.get('committee_name')} on {r.get('contribution_receipt_date')}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
