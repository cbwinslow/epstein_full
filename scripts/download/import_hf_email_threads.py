#!/usr/bin/env python3
"""
Import Email Threads from HuggingFace
Dataset: notesbymuneeb/epstein-emails (epstein_email_threads.parquet)
Location: /home/cbwinslow/workspace/epstein-data/hf-emails-threads/
Check for duplicates with house_oversight_emails
"""

import asyncio
import asyncpg
from pathlib import Path
import pandas as pd

PARQUET_FILE = Path("/home/cbwinslow/workspace/epstein-data/hf-emails-threads/epstein_email_threads.parquet")
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
BATCH_SIZE = 1000

async def create_table(conn):
    """Create table for email threads."""
    print("Creating hf_email_threads table...")
    
    # Check if table exists
    exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'hf_email_threads'
        )
    """)
    
    if not exists:
        await conn.execute("""
            CREATE TABLE hf_email_threads (
                id SERIAL PRIMARY KEY,
                thread_id TEXT,
                subject TEXT,
                sender TEXT,
                recipients TEXT[],
                date TIMESTAMPTZ,
                content TEXT,
                source TEXT,
                file_path TEXT,
                extracted_at TIMESTAMPTZ DEFAULT NOW(),
                UNIQUE(thread_id, date)
            )
        """)
        
        await conn.execute("CREATE INDEX idx_hf_et_thread ON hf_email_threads(thread_id)")
        await conn.execute("CREATE INDEX idx_hf_et_sender ON hf_email_threads(sender)")
        await conn.execute("CREATE INDEX idx_hf_et_date ON hf_email_threads(date)")
        
        print("✅ Table created")
    else:
        print("⚠️  Table already exists - will check for duplicates")

async def check_duplicates(conn, df):
    """Check how many records already exist in SQL."""
    # Get count of existing house_oversight_emails
    existing = await conn.fetchval("SELECT COUNT(*) FROM house_oversight_emails")
    print(f"  Existing house_oversight_emails: {existing}")
    
    # Check overlap - sample a few thread_ids
    sample_ids = df['thread_id'].head(10).tolist() if 'thread_id' in df.columns else []
    if sample_ids:
        overlap = await conn.fetchval(
            "SELECT COUNT(*) FROM house_oversight_emails WHERE thread_id = ANY($1)",
            sample_ids
        )
        print(f"  Sample overlap check: {overlap}/10 thread IDs exist")
    
    return existing

async def import_parquet(conn):
    """Import parquet file."""
    if not PARQUET_FILE.exists():
        print(f"❌ File not found: {PARQUET_FILE}")
        return 0
    
    size_mb = PARQUET_FILE.stat().st_size / (1024 * 1024)
    print(f"📁 File: {PARQUET_FILE}")
    print(f"📊 Size: {size_mb:.2f} MB")
    
    # Read parquet
    print("Reading parquet file...")
    df = pd.read_parquet(PARQUET_FILE)
    print(f"📊 Records in file: {len(df)}")
    print(f"📊 Columns: {list(df.columns)}")
    
    # Check for duplicates
    await check_duplicates(conn, df)
    
    # Import data
    count = 0
    skipped = 0
    
    for idx, row in df.iterrows():
        try:
            # Map columns - adjust based on actual parquet structure
            thread_id = str(row.get('thread_id', ''))[:100] if pd.notna(row.get('thread_id')) else None
            subject = str(row.get('subject', ''))[:500] if pd.notna(row.get('subject')) else None
            sender = str(row.get('sender', ''))[:255] if pd.notna(row.get('sender')) else None
            
            # Handle recipients (may be list or string)
            recipients = row.get('recipients', [])
            if isinstance(recipients, str):
                recipients = [recipients]
            elif not isinstance(recipients, list):
                recipients = []
            
            # Parse date
            date = row.get('date')
            if pd.notna(date) and date:
                try:
                    date = pd.to_datetime(date)
                except:
                    date = None
            else:
                date = None
            
            content = str(row.get('content', ''))[:10000] if pd.notna(row.get('content')) else None
            
            await conn.execute("""
                INSERT INTO hf_email_threads 
                (thread_id, subject, sender, recipients, date, content, source, file_path)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (thread_id, date) DO NOTHING
            """, thread_id, subject, sender, recipients, date, content, 
                'notesbymuneeb/epstein-emails', str(PARQUET_FILE))
            
            count += 1
            if count % BATCH_SIZE == 0:
                print(f"  Imported {count}...")
                
        except Exception as e:
            skipped += 1
            if skipped <= 5:
                print(f"  ⚠️  Skipped row {idx}: {e}")
    
    return count

async def main():
    print("="*60)
    print("Importing Email Threads (epstein_email_threads.parquet)")
    print("="*60)
    
    conn = await asyncpg.connect(DB_URL)
    try:
        await create_table(conn)
        count = await import_parquet(conn)
        print(f"\n✅ Complete! Imported {count} email threads")
        
        # Verify
        total = await conn.fetchval("SELECT COUNT(*) FROM hf_email_threads")
        print(f"📊 Total in table: {total}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
