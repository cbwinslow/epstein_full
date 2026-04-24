#!/usr/bin/env python3
"""
Import FBI files OCR and embeddings into PostgreSQL
"""

import json
import logging
import os
import psycopg2
from datetime import datetime

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data"
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/fbi_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
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


def import_fbi_ocr():
    """Import FBI OCR text from JSONL files."""
    ocr_dir = f"{DATA_ROOT}/hf-datasets/fbi-files/ocr"
    
    if not os.path.exists(ocr_dir):
        logging.warning(f"OCR directory not found: {ocr_dir}")
        return 0
    
    conn = psycopg2.connect(**PG_CONFIG)
    
    total = 0
    for filename in os.listdir(ocr_dir):
        if not filename.endswith('.jsonl'):
            continue
        
        filepath = os.path.join(ocr_dir, filename)
        logging.info(f"Processing {filename}")
        
        with open(filepath, 'r') as f:
            with conn.cursor() as cur:
                for line in f:
                    try:
                        data = json.loads(line)
                        
                        # Insert or update
                        cur.execute("""
                            INSERT INTO documents_content (document_id, filename, content, char_count, page_count)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (document_id) DO UPDATE SET
                                content = EXCLUDED.content,
                                updated_at = NOW()
                        """, (
                            data.get('document_id'),
                            data.get('filename', filename),
                            data.get('text', ''),
                            len(data.get('text', '')),
                            data.get('page_count', 1)
                        ))
                        total += 1
                    except Exception as e:
                        continue
                
                conn.commit()
        
        logging.info(f"✓ {filename}: {total} records")
    
    conn.close()
    return total


def main():
    logging.info("=" * 60)
    logging.info("FBI FILES IMPORT")
    logging.info("=" * 60)
    
    count = import_fbi_ocr()
    logging.info(f"Complete: {count} OCR records imported")


if __name__ == "__main__":
    main()
