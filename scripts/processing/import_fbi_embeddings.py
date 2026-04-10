#!/usr/bin/env python3
"""
Import FBI embeddings from JSONL to PostgreSQL.

FBI embeddings dataset from svetfm/epstein-fbi-files
- 236,174 chunks with 768-dim vectors
- Source: https://huggingface.co/datasets/svetfm/epstein-fbi-files
"""

import json
import os
import sys
from pathlib import Path
from typing import Iterator
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm

# Configuration
DATA_FILE = "/home/cbwinslow/workspace/epstein-data/supplementary-datasets/fbi-embeddings/embeddings/all_embeddings.jsonl"
BATCH_SIZE = 1000

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
    """Create table for FBI embeddings if not exists."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fbi_embeddings (
            id UUID PRIMARY KEY,
            bates_number TEXT,
            bates_range TEXT,
            source_volume INTEGER,
            source_path TEXT,
            doc_type TEXT,
            ocr_confidence REAL,
            ocr_engine TEXT,
            page_number INTEGER,
            total_pages INTEGER,
            chunk_index INTEGER,
            total_chunks INTEGER,
            chunk_text TEXT,
            embedding vector(768),
            ingested_at BIGINT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fbi_embeddings_bates 
        ON fbi_embeddings(bates_number);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fbi_embeddings_embedding 
        ON fbi_embeddings USING ivfflat (embedding vector_cosine_ops);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table fbi_embeddings created/verified")


def stream_jsonl(file_path: str) -> Iterator[dict]:
    """Stream JSONL file line by line to avoid memory issues."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def count_lines(file_path: str) -> int:
    """Count total lines in file for progress bar."""
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for _ in f:
            count += 1
    return count


def import_fbi_embeddings():
    """Import FBI embeddings from JSONL to PostgreSQL."""
    print(f"📊 Importing FBI embeddings from {DATA_FILE}")
    
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
    cur.execute("SELECT COUNT(*) FROM fbi_embeddings")
    existing_count = cur.fetchone()[0]
    print(f"📝 Existing records in table: {existing_count:,}")
    
    # Stream and import
    batch = []
    imported = 0
    skipped = 0
    
    with tqdm(total=total_lines, desc="Importing", unit="records") as pbar:
        for record in stream_jsonl(DATA_FILE):
            skipped += 1
            if skipped <= existing_count:
                pbar.update(1)
                continue  # Skip already imported records
            
            batch.append((
                record['id'],
                record.get('bates_number'),
                record.get('bates_range'),
                record.get('source_volume'),
                record.get('source_path'),
                record.get('doc_type'),
                record.get('ocr_confidence'),
                record.get('ocr_engine'),
                record.get('page_number'),
                record.get('total_pages'),
                record.get('chunk_index'),
                record.get('total_chunks'),
                record.get('chunk_text'),
                record.get('embedding'),
                record.get('ingested_at')
            ))
            
            if len(batch) >= BATCH_SIZE:
                execute_values(
                    cur,
                    """
                    INSERT INTO fbi_embeddings 
                    (id, bates_number, bates_range, source_volume, source_path, 
                     doc_type, ocr_confidence, ocr_engine, page_number, total_pages,
                     chunk_index, total_chunks, chunk_text, embedding, ingested_at)
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
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
                INSERT INTO fbi_embeddings 
                (id, bates_number, bates_range, source_volume, source_path, 
                 doc_type, ocr_confidence, ocr_engine, page_number, total_pages,
                 chunk_index, total_chunks, chunk_text, embedding, ingested_at)
                VALUES %s
                ON CONFLICT (id) DO NOTHING
                """,
                batch
            )
            conn.commit()
            imported += len(batch)
            pbar.update(len(batch))
    
    # Verify import
    cur.execute("SELECT COUNT(*) FROM fbi_embeddings")
    final_count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    print(f"\n✅ Import complete!")
    print(f"   Records imported: {imported:,}")
    print(f"   Total in database: {final_count:,}")
    print(f"   File: {DATA_FILE}")


if __name__ == "__main__":
    import_fbi_embeddings()
