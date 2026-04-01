#!/usr/bin/env python3
"""
Import Full Epstein Index from CSV to PostgreSQL.

Full Epstein Index dataset from theelderemo/FULL_EPSTEIN_INDEX
- 221,389 rows with EFTA IDs and extracted text
- Source: https://huggingface.co/datasets/theelderemo/FULL_EPSTEIN_INDEX
"""

import csv
import os
import sys
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm

# Configuration
DATA_FILE = "/mnt/data/epstein-project/supplementary-datasets/full-epstein-index/dataset_text_extract.csv"
BATCH_SIZE = 5000

# PostgreSQL connection
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd"
}


def get_connection():
    """Get PostgreSQL connection."""
    return psycopg2.connect(**DB_CONFIG)


def create_table():
    """Create table for Full Epstein Index if not exists."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS full_epstein_index (
            id SERIAL PRIMARY KEY,
            efta_id TEXT,
            extracted_text TEXT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_full_epstein_efta 
        ON full_epstein_index(efta_id);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_full_epstein_text_search 
        ON full_epstein_index USING gin(to_tsvector('english', extracted_text));
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table full_epstein_index created/verified")


def count_lines(file_path: str) -> int:
    """Count total lines in file for progress bar (excluding header)."""
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        for _ in f:
            count += 1
    return count


def import_full_epstein_index():
    """Import Full Epstein Index from CSV to PostgreSQL."""
    print(f"📊 Importing Full Epstein Index from {DATA_FILE}")
    
    # Verify file exists
    if not Path(DATA_FILE).exists():
        print(f"❌ Error: File not found: {DATA_FILE}")
        sys.exit(1)
    
    # Create table
    create_table()
    
    # Count total lines
    total_lines = count_lines(DATA_FILE)
    print(f"📁 Total records to import: {total_lines:,}")
    
    # Get connection
    conn = get_connection()
    cur = conn.cursor()
    
    # Check existing count
    cur.execute("SELECT COUNT(*) FROM full_epstein_index")
    existing_count = cur.fetchone()[0]
    print(f"📝 Existing records in table: {existing_count:,}")
    
    if existing_count > 0:
        print("⚠️  Table already has data. Truncating...")
        cur.execute("TRUNCATE TABLE full_epstein_index")
        conn.commit()
    
    # Stream and import CSV
    batch = []
    imported = 0
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        with tqdm(total=total_lines, desc="Importing", unit="records") as pbar:
            for row in reader:
                # Extract EFTA ID from filename (e.g., "EFTA00005586.pdf" -> "EFTA00005586")
                efta_id = row.get('id', '').replace('.pdf', '')
                text = row.get('text', '')
                
                batch.append((efta_id, text))
                
                if len(batch) >= BATCH_SIZE:
                    execute_values(
                        cur,
                        """
                        INSERT INTO full_epstein_index (efta_id, extracted_text)
                        VALUES %s
                        ON CONFLICT DO NOTHING
                        """,
                        batch
                    )
                    conn.commit()
                    imported += len(batch)
                    batch = []
                    pbar.update(BATCH_SIZE)
            
            # Insert remaining records
            if batch:
                execute_values(
                    cur,
                    """
                    INSERT INTO full_epstein_index (efta_id, extracted_text)
                    VALUES %s
                    ON CONFLICT DO NOTHING
                    """,
                    batch
                )
                conn.commit()
                imported += len(batch)
                pbar.update(len(batch))
    
    # Verify import
    cur.execute("SELECT COUNT(*) FROM full_epstein_index")
    final_count = cur.fetchone()[0]
    
    # Get sample for verification
    cur.execute("SELECT efta_id, LEFT(extracted_text, 100) FROM full_epstein_index LIMIT 3")
    samples = cur.fetchall()
    
    cur.close()
    conn.close()
    
    print(f"\n✅ Import complete!")
    print(f"   Records imported: {imported:,}")
    print(f"   Total in database: {final_count:,}")
    print(f"   File: {DATA_FILE}")
    
    print(f"\n📋 Sample records:")
    for efta, text in samples:
        print(f"   {efta}: {text}...")


if __name__ == "__main__":
    import_full_epstein_index()
