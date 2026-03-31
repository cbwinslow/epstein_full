#!/usr/bin/env python3
"""
Import House Oversight embeddings from Parquet to PostgreSQL.

House Oversight dataset from svetfm/epstein-files-nov11-25-house-post-ocr-embeddings
- 69,290 chunks with 768-dim vectors
- Source: https://huggingface.co/datasets/svetfm/epstein-files-nov11-25-house-post-ocr-embeddings
"""

import os
import sys
from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm

# Configuration
DATA_FILE = "/mnt/data/epstein-project/supplementary-datasets/house-oversight-embeddings/train-00000-of-00001.parquet"
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
    """Create table for House Oversight embeddings if not exists."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS house_oversight_embeddings (
            id SERIAL PRIMARY KEY,
            chunk_id TEXT,
            source_file TEXT,
            text_content TEXT,
            embedding vector(768),
            metadata JSONB,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_house_oversight_chunk_id 
        ON house_oversight_embeddings(chunk_id);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_house_oversight_source_file 
        ON house_oversight_embeddings(source_file);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_house_oversight_embedding 
        ON house_oversight_embeddings USING ivfflat (embedding vector_cosine_ops);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table house_oversight_embeddings created/verified")


def explore_parquet():
    """Explore Parquet file structure."""
    print(f"🔍 Exploring {DATA_FILE}...")
    df = pd.read_parquet(DATA_FILE)
    
    print(f"\n📊 Parquet file info:")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Dtypes:\n{df.dtypes}")
    
    # Show sample
    print(f"\n📋 Sample record:")
    if len(df) > 0:
        sample = df.iloc[0]
        for col in df.columns:
            val = sample[col]
            if col == 'embedding' and isinstance(val, (list, tuple)):
                print(f"   {col}: {type(val)} with {len(val)} dimensions")
            else:
                display_val = str(val)[:100] + "..." if len(str(val)) > 100 else str(val)
                print(f"   {col}: {display_val}")
    
    return df


def import_house_oversight_embeddings():
    """Import House Oversight embeddings from Parquet to PostgreSQL."""
    print(f"📊 Importing House Oversight embeddings from {DATA_FILE}")
    
    # Verify file exists
    if not Path(DATA_FILE).exists():
        print(f"❌ Error: File not found: {DATA_FILE}")
        sys.exit(1)
    
    # Create table
    create_table()
    
    # Load and explore
    df = explore_parquet()
    total_rows = len(df)
    
    # Get connection
    conn = get_connection()
    cur = conn.cursor()
    
    # Check existing count
    cur.execute("SELECT COUNT(*) FROM house_oversight_embeddings")
    existing_count = cur.fetchone()[0]
    print(f"\n📝 Existing records in table: {existing_count:,}")
    
    if existing_count > 0:
        print("⚠️  Table already has data. Truncating...")
        cur.execute("TRUNCATE TABLE house_oversight_embeddings")
        conn.commit()
    
    # Prepare data for import
    print(f"\n📥 Importing {total_rows:,} records...")
    
    # Map columns - adjust based on actual parquet structure
    records = []
    for idx, row in df.iterrows():
        # Convert numpy array to Python list for PostgreSQL
        embedding = row.get('embedding', [])
        if hasattr(embedding, 'tolist'):
            embedding = embedding.tolist()
        
        record = (
            f"{row.get('source_file', '')}_{row.get('chunk_index', idx)}",
            str(row.get('source_file', '')),
            str(row.get('text', '')),
            embedding,
            None  # metadata
        )
        records.append(record)
    
    # Batch insert
    imported = 0
    for i in tqdm(range(0, len(records), BATCH_SIZE), desc="Importing batches"):
        batch = records[i:i+BATCH_SIZE]
        
        execute_values(
            cur,
            """
            INSERT INTO house_oversight_embeddings 
            (chunk_id, source_file, text_content, embedding, metadata)
            VALUES %s
            ON CONFLICT DO NOTHING
            """,
            batch
        )
        conn.commit()
        imported += len(batch)
    
    # Verify import
    cur.execute("SELECT COUNT(*) FROM house_oversight_embeddings")
    final_count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    print(f"\n✅ Import complete!")
    print(f"   Records imported: {imported:,}")
    print(f"   Total in database: {final_count:,}")
    print(f"   File: {DATA_FILE}")


if __name__ == "__main__":
    import json
    import_house_oversight_embeddings()
