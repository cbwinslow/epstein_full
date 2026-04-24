#!/usr/bin/env python3
"""Import Epstein Data Text (16 parquet files)"""
import asyncio
import asyncpg
from pathlib import Path
import pandas as pd

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/hf-new-datasets/epstein-data-text")
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
BATCH_SIZE = 500

async def main():
    print("Importing Epstein Data Text...")
    
    conn = await asyncpg.connect(DB_URL)
    try:
        # Create table
        await conn.execute("DROP TABLE IF EXISTS hf_epstein_data_text CASCADE")
        await conn.execute("""
            CREATE TABLE hf_epstein_data_text (
                id SERIAL PRIMARY KEY,
                doc_id TEXT,
                text_content TEXT,
                source_file TEXT,
                imported_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        await conn.execute("CREATE INDEX idx_hf_edt_doc ON hf_epstein_data_text(doc_id)")
        print("✅ Table created")
        
        # Find all parquet files
        parquet_files = sorted(BASE_DIR.glob("*.parquet"))
        print(f"📁 Found {len(parquet_files)} parquet files")
        
        total_count = 0
        for pf in parquet_files:
            print(f"\n📄 Processing: {pf.name}")
            df = pd.read_parquet(pf)
            print(f"   Records: {len(df)}")
            
            for idx, row in df.iterrows():
                doc_id = str(row.get('doc_id', ''))[:100] if pd.notna(row.get('doc_id')) else None
                text = str(row.get('text', ''))[:50000] if pd.notna(row.get('text')) else None
                
                await conn.execute("""
                    INSERT INTO hf_epstein_data_text (doc_id, text_content, source_file)
                    VALUES ($1, $2, $3)
                """, doc_id, text, pf.name)
                
                total_count += 1
                if total_count % 5000 == 0:
                    print(f"  Total imported: {total_count}...")
        
        print(f"\n✅ Complete! Imported {total_count} text records")
        
        final = await conn.fetchval("SELECT COUNT(*) FROM hf_epstein_data_text")
        print(f"📊 Total in table: {final}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
