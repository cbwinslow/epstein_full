#!/usr/bin/env python3
"""
Import HuggingFace epstein-files-20k into PostgreSQL

Dataset: teyler/epstein-files-20k (2,136,420 records)
Location: /home/cbwinslow/workspace/epstein-data/huggingface/epstein_files_20k/data.jsonl
"""

import asyncio
import asyncpg
import json
from pathlib import Path
from datetime import datetime

# Configuration
DATA_FILE = Path("/home/cbwinslow/workspace/epstein-data/huggingface/epstein_files_20k/data.jsonl")
BATCH_SIZE = 5000
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

async def create_table(conn):
    """Create the table for HF epstein-files-20k data."""
    print("Creating table hf_epstein_files_20k...")
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS hf_epstein_files_20k (
            id SERIAL PRIMARY KEY,
            line_number INTEGER,
            content TEXT,
            content_length INTEGER,
            word_count INTEGER,
            ingestion_date TIMESTAMPTZ DEFAULT NOW(),
            source_dataset TEXT DEFAULT 'teyler/epstein-files-20k'
        )
    """)
    
    # Create indexes
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_hf_epstein_20k_line 
        ON hf_epstein_files_20k(line_number)
    """)
    
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_hf_epstein_20k_content_length 
        ON hf_epstein_files_20k(content_length)
    """)
    
    print("✅ Table and indexes created")

async def import_data(conn):
    """Import data from JSONL file."""
    print(f"Starting import from {DATA_FILE}...")
    
    # Get current count
    current_count = await conn.fetchval("SELECT COUNT(*) FROM hf_epstein_files_20k")
    print(f"Current records in table: {current_count:,}")
    
    if current_count > 0:
        print("⚠️  Table already has data. Truncating and re-importing...")
        await conn.execute("TRUNCATE TABLE hf_epstein_files_20k")
    
    # Count total lines
    print("Counting total lines...")
    with open(DATA_FILE, 'r') as f:
        total_lines = sum(1 for _ in f)
    print(f"Total lines to import: {total_lines:,}")
    
    # Import in batches
    batch = []
    imported = 0
    line_num = 0
    
    with open(DATA_FILE, 'r') as f:
        for line in f:
            line_num += 1
            
            try:
                data = json.loads(line.strip())
                content = data.get('text', '')
                
                batch.append((
                    line_num,
                    content,
                    len(content),
                    len(content.split()) if content else 0
                ))
                
                if len(batch) >= BATCH_SIZE:
                    await conn.copy_records_to_table(
                        'hf_epstein_files_20k',
                        records=batch,
                        columns=['line_number', 'content', 'content_length', 'word_count']
                    )
                    imported += len(batch)
                    batch = []
                    
                    if imported % 50000 == 0:
                        print(f"   Imported {imported:,} / {total_lines:,} ({imported/total_lines*100:.1f}%)")
                        
            except json.JSONDecodeError as e:
                print(f"   ⚠️  Skipping line {line_num}: JSON error - {e}")
                continue
    
    # Insert remaining batch
    if batch:
        await conn.copy_records_to_table(
            'hf_epstein_files_20k',
            records=batch,
            columns=['line_number', 'content', 'content_length', 'word_count']
        )
        imported += len(batch)
    
    print(f"✅ Import complete! Total imported: {imported:,} records")
    return imported

async def verify_import(conn):
    """Verify the import."""
    print("\nVerifying import...")
    
    count = await conn.fetchval("SELECT COUNT(*) FROM hf_epstein_files_20k")
    print(f"Total records: {count:,}")
    
    avg_length = await conn.fetchval("SELECT AVG(content_length) FROM hf_epstein_files_20k")
    print(f"Average content length: {avg_length:.0f} characters")
    
    total_words = await conn.fetchval("SELECT SUM(word_count) FROM hf_epstein_files_20k")
    print(f"Total words: {total_words:,}")
    
    # Sample records
    samples = await conn.fetch("""
        SELECT id, line_number, LEFT(content, 100) as preview, content_length
        FROM hf_epstein_files_20k
        WHERE content_length > 50
        ORDER BY RANDOM()
        LIMIT 3
    """)
    
    print("\nSample records:")
    for s in samples:
        print(f"   Line {s['line_number']}: {s['preview']}... (len={s['content_length']})")

async def main():
    print("="*70)
    print("HUGGINGFACE EPSTEIN-FILES-20K IMPORT")
    print("="*70)
    print(f"Started: {datetime.now()}")
    print(f"Data file: {DATA_FILE}")
    print(f"Database: {DB_URL}")
    print(f"Batch size: {BATCH_SIZE}")
    print("="*70)
    
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Create table
        await create_table(conn)
        
        # Import data
        imported = await import_data(conn)
        
        # Verify
        await verify_import(conn)
        
        print("\n" + "="*70)
        print(f"✅ IMPORT COMPLETE - {imported:,} records")
        print(f"Finished: {datetime.now()}")
        print("="*70)
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
