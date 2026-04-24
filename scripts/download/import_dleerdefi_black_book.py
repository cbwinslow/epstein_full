#!/usr/bin/env python3
"""
Import Black Book contacts from dleerdefi/epstein-network-data

Source: /home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/csv/black_book_contacts.csv
"""

import asyncio
import asyncpg
import csv
from pathlib import Path
from datetime import datetime

CSV_FILE = Path("/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/csv/black_book_contacts.csv")
BATCH_SIZE = 1000
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

async def create_table(conn):
    """Create table for Black Book contacts."""
    print("Creating table black_book_contacts...")
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS black_book_contacts (
            id SERIAL PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            company TEXT,
            notes TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_black_book_name 
        ON black_book_contacts(name)
    """)
    
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_black_book_company 
        ON black_book_contacts(company)
    """)
    
    print("✅ Table created")

async def import_csv(conn):
    """Import CSV data."""
    print(f"Importing from {CSV_FILE}...")
    
    if not CSV_FILE.exists():
        print(f"❌ File not found: {CSV_FILE}")
        return 0
    
    # Check current count
    current = await conn.fetchval("SELECT COUNT(*) FROM black_book_contacts")
    print(f"Current records: {current}")
    
    if current > 0:
        print("⚠️  Table has data. Truncating...")
        await conn.execute("TRUNCATE TABLE black_book_contacts")
    
    # Count lines
    with open(CSV_FILE, 'r') as f:
        total = sum(1 for _ in f) - 1  # minus header
    print(f"Total to import: {total}")
    
    imported = 0
    batch = []
    
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            batch.append((
                row.get('name', ''),
                row.get('phone', ''),
                row.get('email', ''),
                row.get('address', ''),
                row.get('company', ''),
                row.get('notes', ''),
                str(CSV_FILE)
            ))
            
            if len(batch) >= BATCH_SIZE:
                await conn.copy_records_to_table(
                    'black_book_contacts',
                    records=batch,
                    columns=['name', 'phone', 'email', 'address', 'company', 'notes', 'source_file']
                )
                imported += len(batch)
                batch = []
                print(f"   Imported {imported} / {total}")
    
    if batch:
        await conn.copy_records_to_table(
            'black_book_contacts',
            records=batch,
            columns=['name', 'phone', 'email', 'address', 'company', 'notes', 'source_file']
        )
        imported += len(batch)
    
    print(f"✅ Import complete: {imported} records")
    return imported

async def verify(conn):
    """Verify import."""
    print("\nVerification:")
    count = await conn.fetchval("SELECT COUNT(*) FROM black_book_contacts")
    print(f"Total: {count}")
    
    samples = await conn.fetch("SELECT * FROM black_book_contacts LIMIT 3")
    for s in samples:
        print(f"   - {s['name']} | {s['company']} | {s['phone']}")

async def main():
    print("="*70)
    print("BLACK BOOK CONTACTS IMPORT")
    print("="*70)
    print(f"Started: {datetime.now()}")
    print(f"Source: {CSV_FILE}")
    print("="*70)
    
    conn = await asyncpg.connect(DB_URL)
    try:
        await create_table(conn)
        imported = await import_csv(conn)
        await verify(conn)
        print("\n" + "="*70)
        print(f"✅ COMPLETE - {imported} contacts imported")
        print("="*70)
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
