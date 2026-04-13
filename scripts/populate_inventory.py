#!/usr/bin/env python3
import asyncpg
import asyncio
from pathlib import Path

async def main():
    conn = await asyncpg.connect("postgresql://cbwinslow:123qweasd@localhost:5432/epstein")
    
    # Insert HF completed sources
    hf_sources = [
        ("HF epstein-files-20k", "huggingface", "hf-epstein-files-20k", "hf_epstein_files_20k", 2136420, "complete", 1),
        ("HF House Oversight", "huggingface", "hf-house-oversight", "hf_house_oversight_docs", 1791798, "complete", 1),
        ("HF OCR Complete", "huggingface", "hf-ocr-complete", "hf_ocr_complete", 1380932, "complete", 1),
        ("HF Embeddings", "huggingface", "hf-embeddings", "hf_embeddings", 69290, "complete", 1),
        ("HF Data Text", "huggingface", "hf-new-datasets/epstein-data-text", "hf_epstein_data_text", 451720, "complete", 1),
        ("HF FBI Files", "huggingface", "hf-datasets/fbi-files", "fbi_vault_pages", 1426, "complete", 1),
        ("HF Full Index", "huggingface", "hf-datasets/full-index", "full_epstein_index", 8531, "complete", 1),
        ("HF Email Threads", "huggingface", "hf-emails-threads", None, 5082, "duplicate", 10),
    ]
    
    # Insert ICIJ pending sources
    icij_sources = [
        ("ICIJ Entities", "icij", "icij_extracted/nodes-entities.csv", "icij_entities", 814617, "pending", 1),
        ("ICIJ Officers", "icij", "icij_extracted/nodes-officers.csv", "icij_officers", 1800000, "pending", 1),
        ("ICIJ Addresses", "icij", "icij_extracted/nodes-addresses.csv", "icij_addresses", 700000, "pending", 1),
        ("ICIJ Intermediaries", "icij", "icij_extracted/nodes-intermediaries.csv", "icij_intermediaries", 38000, "pending", 1),
        ("ICIJ Others", "icij", "icij_extracted/nodes-others.csv", "icij_others", 4000, "pending", 1),
        ("ICIJ Relationships", "icij", "icij_extracted/relationships.csv", "icij_relationships", 3339272, "pending", 1),
    ]
    
    for name, stype, path, table, expected, status, priority in hf_sources + icij_sources:
        await conn.execute("""
            INSERT INTO data_sources (source_name, source_type, base_path, target_table, 
                                     expected_records, status, priority)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (source_name) DO UPDATE SET
                status = EXCLUDED.status,
                records_imported = EXCLUDED.expected_records,
                last_updated = NOW()
        """, name, stype, str(Path.home() / "workspace/epstein-data" / path), table, expected, status, priority)
    
    print(f"Inserted {len(hf_sources)} HF and {len(icij_sources)} ICIJ sources")
    
    # Populate ICIJ files for queue
    icij_dir = Path.home() / "workspace/epstein-data/icij_extracted"
    if icij_dir.exists():
        for csv_file in icij_dir.glob("*.csv"):
            source_name = f"ICIJ {csv_file.stem.replace('nodes-', '').replace('-', ' ').title()}"
            source_id = await conn.fetchval(
                "SELECT id FROM data_sources WHERE source_name = $1",
                source_name
            )
            if source_id:
                size = csv_file.stat().st_size
                await conn.execute("""
                    INSERT INTO data_files (source_id, filename, full_path, file_size_bytes, status)
                    VALUES ($1, $2, $3, $4, 'pending')
                    ON CONFLICT DO NOTHING
                """, source_id, csv_file.name, str(csv_file), size)
                
                # Add to queue
                file_id = await conn.fetchval(
                    "SELECT id FROM data_files WHERE full_path = $1",
                    str(csv_file)
                )
                if file_id:
                    await conn.execute("""
                        INSERT INTO import_queue (file_id, source_type, priority, status)
                        VALUES ($1, 'icij', 1, 'pending')
                        ON CONFLICT DO NOTHING
                    """, file_id)
        
        print("Populated ICIJ files and queue")
    
    await conn.close()
    print("Inventory population complete!")

if __name__ == "__main__":
    asyncio.run(main())
