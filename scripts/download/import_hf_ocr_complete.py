#!/usr/bin/env python3
"""
Import OCR Complete data
Dataset: tensonaut/EPSTEIN_FILES_20K_OCR
Location: /home/cbwinslow/workspace/epstein-data/hf-ocr-complete/data/dataset.parquet
"""

import asyncio
import asyncpg
from pathlib import Path
import pandas as pd

PARQUET_FILE = Path("/home/cbwinslow/workspace/epstein-data/hf-ocr-complete/data/dataset.parquet")
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
BATCH_SIZE = 500

async def create_table(conn):
    """Create table for OCR data."""
    print("Creating hf_ocr_complete table...")
    
    await conn.execute("DROP TABLE IF EXISTS hf_ocr_complete CASCADE")
    
    await conn.execute("""
        CREATE TABLE hf_ocr_complete (
            id SERIAL PRIMARY KEY,
            doc_id TEXT,
            page_num INT,
            ocr_text TEXT,
            confidence FLOAT,
            source TEXT,
            file_path TEXT,
            extracted_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    await conn.execute("CREATE INDEX idx_hf_ocr_doc ON hf_ocr_complete(doc_id)")
    await conn.execute("CREATE INDEX idx_hf_ocr_page ON hf_ocr_complete(page_num)")
    
    print("✅ Table created")

async def import_parquet(conn):
    """Import parquet file."""
    if not PARQUET_FILE.exists():
        print(f"❌ File not found: {PARQUET_FILE}")
        return 0
    
    size_mb = PARQUET_FILE.stat().st_size / (1024 * 1024)
    print(f"📁 File: {PARQUET_FILE}")
    print(f"📊 Size: {size_mb:.2f} MB")
    
    # Read parquet - load in portions
    print("Reading parquet file...")
    
    # Read entire file (for large files, use pyarrow directly)
    df = pd.read_parquet(PARQUET_FILE)
    print(f"Loaded {len(df)} records")
    
    count = 0
    batch = []
    
    for idx, row in df.iterrows():
        batch.append({
            'doc_id': str(row.get('doc_id', ''))[:100] if pd.notna(row.get('doc_id')) else None,
            'page_num': int(row.get('page_num', 0)) if pd.notna(row.get('page_num')) else None,
            'ocr_text': str(row.get('text', ''))[:50000] if pd.notna(row.get('text')) else None,
            'confidence': float(row.get('confidence', 0)) if pd.notna(row.get('confidence')) else None,
        })
        
        if len(batch) >= BATCH_SIZE:
            await insert_batch(conn, batch)
            count += len(batch)
            if count % 10000 == 0:
                print(f"  Imported {count}...")
            batch = []
    
    # Insert remaining
    if batch:
        await insert_batch(conn, batch)
        count += len(batch)
    
    return count

async def insert_batch(conn, batch):
    """Insert batch of records."""
    await conn.executemany("""
        INSERT INTO hf_ocr_complete 
        (doc_id, page_num, ocr_text, confidence, source, file_path)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT DO NOTHING
    """, [
        (b['doc_id'], b['page_num'], b['ocr_text'], b['confidence'],
         'tensonaut/EPSTEIN_FILES_20K_OCR', str(PARQUET_FILE))
        for b in batch
    ])

async def main():
    print("="*60)
    print("Importing OCR Complete (dataset.parquet)")
    print("="*60)
    
    conn = await asyncpg.connect(DB_URL)
    try:
        await create_table(conn)
        count = await import_parquet(conn)
        print(f"\n✅ Complete! Imported {count} OCR records")
        
        # Verify
        total = await conn.fetchval("SELECT COUNT(*) FROM hf_ocr_complete")
        print(f"📊 Total in table: {total}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
