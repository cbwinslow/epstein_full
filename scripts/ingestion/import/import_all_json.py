#!/usr/bin/env python3
"""
Import all JSON files from processed/ directory into PostgreSQL
"""

import json
import logging
import os
import psycopg2
from datetime import datetime
import glob

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data"
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/json_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "cbwinslow",
    "password": "123qweasd",
    "dbname": "epstein",
}


def import_json_file(filepath, conn, source_name):
    """Import a single JSON file into json_import_staging."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        with conn.cursor() as cur:
            # Handle both single object and array
            if isinstance(data, list):
                for item in data:
                    cur.execute("""
                        INSERT INTO json_import_staging (source_file, data)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (os.path.basename(filepath), json.dumps(item)))
            else:
                cur.execute("""
                    INSERT INTO json_import_staging (source_file, data)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (os.path.basename(filepath), json.dumps(data)))
            
            conn.commit()
        
        return True
    except Exception as e:
        logging.error(f"Error importing {filepath}: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info("JSON FILE IMPORT")
    logging.info("=" * 60)
    
    conn = psycopg2.connect(**PG_CONFIG)
    
    # Find all JSON files
    json_dirs = [
        f"{DATA_ROOT}/processed",
        f"{DATA_ROOT}/datasets",
    ]
    
    total_imported = 0
    total_errors = 0
    
    for json_dir in json_dirs:
        if not os.path.exists(json_dir):
            continue
        
        json_files = glob.glob(f"{json_dir}/**/*.json", recursive=True)
        logging.info(f"Found {len(json_files)} JSON files in {json_dir}")
        
        for filepath in json_files:
            if import_json_file(filepath, conn, os.path.basename(json_dir)):
                total_imported += 1
            else:
                total_errors += 1
            
            if (total_imported + total_errors) % 100 == 0:
                logging.info(f"Progress: {total_imported} imported, {total_errors} errors")
    
    conn.close()
    
    logging.info(f"\nComplete: {total_imported} files imported, {total_errors} errors")


if __name__ == "__main__":
    main()
