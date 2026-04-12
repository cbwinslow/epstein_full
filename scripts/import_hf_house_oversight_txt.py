#!/usr/bin/env python3
"""
Import House Oversight TXT file (EPS_FILES_20K_NOV2025.txt)
Dataset: notesbymuneeb/epstein-emails
Location: /home/cbwinslow/workspace/epstein-data/hf-house-oversight/
"""

import asyncio
import asyncpg
import re
from pathlib import Path
from datetime import datetime

FILE_PATH = Path("/home/cbwinslow/workspace/epstein-data/hf-house-oversight/EPS_FILES_20K_NOV2025.txt")
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
BATCH_SIZE = 500

async def create_table(conn):
    """Create table for House Oversight document references."""
    print("Creating hf_house_oversight_docs table...")
    
    await conn.execute("DROP TABLE IF EXISTS hf_house_oversight_docs CASCADE")
    
    await conn.execute("""
        CREATE TABLE hf_house_oversight_docs (
            id SERIAL PRIMARY KEY,
            doc_id TEXT,
            doc_type TEXT,
            title TEXT,
            source TEXT,
            file_path TEXT,
            extracted_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # Create indexes
    await conn.execute("CREATE INDEX idx_hf_ho_docs_id ON hf_house_oversight_docs(doc_id)")
    await conn.execute("CREATE INDEX idx_hf_ho_docs_type ON hf_house_oversight_docs(doc_type)")
    
    print("✅ Table created")

async def parse_and_import(conn):
    """Parse the TXT file and import references."""
    if not FILE_PATH.exists():
        print(f"❌ File not found: {FILE_PATH}")
        return 0
    
    size_mb = FILE_PATH.stat().st_size / (1024 * 1024)
    print(f"📁 File: {FILE_PATH}")
    print(f"📊 Size: {size_mb:.2f} MB")
    
    count = 0
    batch = []
    
    with open(FILE_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line - format varies but typically contains:
            # Document ID, type, title information
            
            # Extract potential document ID (EFT-XXXXX or similar patterns)
            doc_id_match = re.search(r'(EFT[A-Z]*[-_]?\d+)', line, re.IGNORECASE)
            doc_id = doc_id_match.group(1) if doc_id_match else None
            
            # Determine doc type from line content
            doc_type = 'unknown'
            if 'email' in line.lower():
                doc_type = 'email'
            elif 'flight' in line.lower():
                doc_type = 'flight_log'
            elif 'contact' in line.lower() or 'address' in line.lower():
                doc_type = 'contact_list'
            elif 'note' in line.lower():
                doc_type = 'note'
            elif 'doc' in line.lower() or 'document' in line.lower():
                doc_type = 'document'
            
            batch.append({
                'doc_id': doc_id,
                'doc_type': doc_type,
                'title': line[:500] if len(line) > 500 else line,
                'source': 'House_Oversight_2025',
                'file_path': str(FILE_PATH)
            })
            
            if len(batch) >= BATCH_SIZE:
                await insert_batch(conn, batch)
                count += len(batch)
                print(f"  Imported {count} references...")
                batch = []
    
    # Insert remaining
    if batch:
        await insert_batch(conn, batch)
        count += len(batch)
    
    return count

async def insert_batch(conn, batch):
    """Insert batch of records."""
    await conn.executemany("""
        INSERT INTO hf_house_oversight_docs 
        (doc_id, doc_type, title, source, file_path)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT DO NOTHING
    """, [
        (b['doc_id'], b['doc_type'], b['title'], b['source'], b['file_path'])
        for b in batch
    ])

async def main():
    print("="*60)
    print("Importing House Oversight TXT (EPS_FILES_20K_NOV2025.txt)")
    print("="*60)
    
    conn = await asyncpg.connect(DB_URL)
    try:
        await create_table(conn)
        count = await parse_and_import(conn)
        print(f"\n✅ Complete! Imported {count} document references")
        
        # Verify
        total = await conn.fetchval("SELECT COUNT(*) FROM hf_house_oversight_docs")
        print(f"📊 Total in table: {total}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
