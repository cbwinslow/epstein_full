#!/usr/bin/env python3
"""Import HF Embeddings dataset"""
import asyncio
import asyncpg
from pathlib import Path
import pandas as pd

PARQUET_FILE = Path("/home/cbwinslow/workspace/epstein-data/hf-embeddings/data/train-00000-of-00001.parquet")
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
BATCH_SIZE = 1000

async def main():
    print("Importing HF Embeddings...")
    
    if not PARQUET_FILE.exists():
        print(f"❌ File not found: {PARQUET_FILE}")
        return
    
    conn = await asyncpg.connect(DB_URL)
    try:
        # Create table
        await conn.execute("DROP TABLE IF EXISTS hf_embeddings CASCADE")
        await conn.execute("""
            CREATE TABLE hf_embeddings (
                id SERIAL PRIMARY KEY,
                doc_id TEXT,
                embedding FLOAT[],
                source TEXT,
                file_path TEXT
            )
        """)
        await conn.execute("CREATE INDEX idx_hf_emb_doc ON hf_embeddings(doc_id)")
        print("✅ Table created")
        
        # Import
        df = pd.read_parquet(PARQUET_FILE)
        print(f"📊 Records: {len(df)}")
        
        count = 0
        for idx, row in df.iterrows():
            doc_id = str(row.get('doc_id', ''))[:100] if pd.notna(row.get('doc_id')) else None
            embedding = row.get('embedding', [])
            if isinstance(embedding, list):
                embedding = [float(x) for x in embedding]
            
            await conn.execute("""
                INSERT INTO hf_embeddings (doc_id, embedding, source, file_path)
                VALUES ($1, $2, $3, $4)
            """, doc_id, embedding, 'hf-embeddings', str(PARQUET_FILE))
            
            count += 1
            if count % 5000 == 0:
                print(f"  Imported {count}...")
        
        print(f"\n✅ Complete! Imported {count} embeddings")
        
        total = await conn.fetchval("SELECT COUNT(*) FROM hf_embeddings")
        print(f"📊 Total: {total}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
