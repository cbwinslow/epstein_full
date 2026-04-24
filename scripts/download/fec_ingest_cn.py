#!/usr/bin/env python3
"""
FEC Candidate Master Ingestion
Uses COPY protocol for fast ingestion
"""

import zipfile
import csv
import io
import psycopg2
from pathlib import Path
import logging
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATA_DIR = Path('/home/cbwinslow/workspace/epstein-data/raw-files/fec')

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'epstein',
    'user': 'cbwinslow',
    'password': '123qweasd'
}

def copy_data_to_postgres(conn, cursor, data_buffer: io.StringIO, table: str, columns: list):
    """Use PostgreSQL COPY protocol"""
    try:
        data_buffer.seek(0)
        copy_sql = f"COPY {table} ({', '.join(columns)}) FROM STDIN WITH (FORMAT CSV, NULL '')"
        cursor.copy_expert(copy_sql, data_buffer)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"COPY failed: {e}")
        return False

def transform_candidate_row(row: list, cycle: int) -> Optional[list]:
    """Transform candidate master row using positional indices"""
    try:
        if len(row) < 15:
            return None
        return [
            row[0][:9],   # cand_id
            row[1][:200], # cand_name
            row[2][:3],   # cand_pty_affiliation
            row[3][:4],   # cand_election_yr
            row[4][:2],   # cand_office_st
            row[5][:1],   # cand_office
            row[6][:2],   # cand_office_district
            row[7][:1],   # cand_ici
            row[8][:1],   # cand_status
            row[9][:9],   # cand_pcc
            row[10][:200], # cand_st1
            row[11][:200], # cand_st2
            row[12][:100], # cand_city
            row[13][:2],   # cand_st
            row[14][:9],   # cand_zip
            cycle
        ]
    except Exception:
        return None

def process_cn_zip(zip_path: Path, cycle: int, conn, cursor) -> int:
    """Process candidate master ZIP file"""
    rows_imported = 0
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for filename in z.namelist():
                if not filename.endswith('.txt'):
                    continue
                    
                logger.info(f"Processing {filename}")
                
                with z.open(filename) as f:
                    first_line = f.readline().decode('utf-8', errors='ignore')
                    f.seek(0)
                    delimiter = '|' if '|' in first_line else ','
                    
                    text_io = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                    reader = csv.reader(text_io, delimiter=delimiter, quoting=csv.QUOTE_NONE)
                    headers = [h.strip().lower().replace(' ', '_') for h in next(reader)]
                    
                    buffer = io.StringIO()
                    csv_writer = csv.writer(buffer, lineterminator='\n')
                    
                    batch_size = 50000
                    batch_count = 0
                    
                    for row in reader:
                        if len(row) < 15:
                            continue
                            
                        transformed = transform_candidate_row(row, cycle)
                        if transformed:
                            csv_writer.writerow(transformed)
                            batch_count += 1
                            
                            if batch_count >= batch_size:
                                columns = ['cand_id', 'cand_name', 'cand_pty_affiliation', 
                                          'cand_election_yr', 'cand_office_st', 'cand_office',
                                          'cand_office_district', 'cand_ici', 'cand_status',
                                          'cand_pcc', 'cand_st1', 'cand_st2', 'cand_city',
                                          'cand_st', 'cand_zip', 'cycle']
                                
                                if copy_data_to_postgres(conn, cursor, buffer, 'fec_candidate_master', columns):
                                    rows_imported += batch_count
                                    logger.info(f"  Imported {rows_imported:,} rows...")
                                
                                buffer = io.StringIO()
                                csv_writer = csv.writer(buffer, lineterminator='\n')
                                batch_count = 0
                    
                    if batch_count > 0:
                        columns = ['cand_id', 'cand_name', 'cand_pty_affiliation', 
                                  'cand_election_yr', 'cand_office_st', 'cand_office',
                                  'cand_office_district', 'cand_ici', 'cand_status',
                                  'cand_pcc', 'cand_st1', 'cand_st2', 'cand_city',
                                  'cand_st', 'cand_zip', 'cycle']
                        if copy_data_to_postgres(conn, cursor, buffer, 'fec_candidate_master', columns):
                            rows_imported += batch_count
                            
    except Exception as e:
        logger.error(f"Error processing {zip_path}: {e}")
    
    return rows_imported

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Ingest candidate master files')
    parser.add_argument('--file', required=True, help='ZIP file to process')
    parser.add_argument('--cycle', type=int, required=True, help='Election cycle')
    
    args = parser.parse_args()
    
    zip_path = Path(args.file)
    if not zip_path.exists():
        logger.error(f"File not found: {zip_path}")
        return
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        logger.info(f"Processing {zip_path.name} for cycle {args.cycle}")
        rows = process_cn_zip(zip_path, args.cycle, conn, cursor)
        logger.info(f"Total rows imported: {rows:,}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
