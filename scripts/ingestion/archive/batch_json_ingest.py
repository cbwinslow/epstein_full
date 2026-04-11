#!/usr/bin/env python3
"""
Ingest all available JSON files from processed/ and other directories
"""

import glob
import json
import logging
import os
from datetime import datetime

import psycopg2

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/json_batch_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)


def find_json_files():
    """Find all JSON files across data directories."""
    patterns = [
        f"{DATA_ROOT}/processed/*.json",
        f"{DATA_ROOT}/Epstein-research-data/**/*.json",
        f"{DATA_ROOT}/supplementary-datasets/*.json",
        f"{DATA_ROOT}/knowledge-graph/*.json",
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))
    
    # Filter to reasonable size files (skip tiny metadata files)
    files = [f for f in files if os.path.getsize(f) > 100]
    
    return sorted(files)


def get_file_type(file_path):
    """Guess the type of data in the JSON file."""
    basename = os.path.basename(file_path).lower()
    
    if 'entity' in basename or 'person' in basename:
        return 'entities'
    elif 'email' in basename or 'communication' in basename:
        return 'emails'
    elif 'flight' in basename:
        return 'flights'
    elif 'location' in basename:
        return 'locations'
    elif 'redaction' in basename:
        return 'redactions'
    elif 'alteration' in basename:
        return 'alterations'
    else:
        return 'generic'


def import_json_file(file_path, conn):
    """Import a JSON file to json_import_staging."""
    try:
        file_size = os.path.getsize(file_path)
        
        # Load JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both single objects and arrays
        if isinstance(data, dict):
            records = [data]
        elif isinstance(data, list):
            records = data
        else:
            logging.warning(f"Unknown JSON structure in {file_path}")
            return 0
        
        file_type = get_file_type(file_path)
        imported = 0
        
        with conn.cursor() as cur:
            for record in records:
                try:
                    cur.execute("""
                        INSERT INTO json_import_staging (source_file, file_type, json_data)
                        VALUES (%s, %s, %s::jsonb)
                        ON CONFLICT DO NOTHING
                    """, (file_path, file_type, json.dumps(record)))
                    imported += 1
                except Exception as e:
                    # Skip problematic records
                    continue
            
            conn.commit()
        
        logging.info(f"  Imported {imported} records from {os.path.basename(file_path)} ({file_size} bytes)")
        return imported
        
    except json.JSONDecodeError as e:
        logging.error(f"  JSON parse error in {file_path}: {e}")
        return 0
    except Exception as e:
        logging.error(f"  Error importing {file_path}: {e}")
        return 0


def main():
    logging.info("=" * 60)
    logging.info("BATCH JSON IMPORTER")
    logging.info("=" * 60)
    
    # Find all JSON files
    json_files = find_json_files()
    logging.info(f"Found {len(json_files)} JSON files to process")
    
    if not json_files:
        logging.info("No JSON files found")
        return 0
    
    # Connect to PostgreSQL
    conn = psycopg2.connect(**PG_CONFIG)
    
    # Ensure staging table exists
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS json_import_staging (
                id SERIAL PRIMARY KEY,
                source_file TEXT,
                file_type TEXT,
                json_data JSONB,
                imported_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(source_file, json_data)
            )
        """)
        conn.commit()
    
    # Process each file
    total_imported = 0
    for i, file_path in enumerate(json_files, 1):
        logging.info(f"[{i}/{len(json_files)}] Processing: {file_path}")
        count = import_json_file(file_path, conn)
        total_imported += count
    
    conn.close()
    
    logging.info("\n" + "=" * 60)
    logging.info(f"IMPORT COMPLETE: {len(json_files)} files, {total_imported} total records")
    logging.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
