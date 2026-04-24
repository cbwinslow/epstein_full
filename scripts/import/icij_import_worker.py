#!/usr/bin/env python3
"""ICIJ Import Worker - Parallel CSV Import"""
import asyncpg
import asyncio
import csv
import sys
from pathlib import Path

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
DATA_DIR = Path("/home/cbwinslow/workspace/epstein-data/icij_extracted")

# Table configurations
TABLES = {
    'entities': {
        'file': 'nodes-entities.csv',
        'table': 'icij_entities',
        'cols': ['node_id', 'name', 'original_name', 'former_name', 'jurisdiction',
                'jurisdiction_description', 'company_type', 'address', 'internal_id',
                'incorporation_date', 'inactivation_date', 'struck_off_date', 'dorm_date',
                'status', 'service_provider', 'ibcruc', 'country_codes', 'countries',
                'sourceid', 'valid_until', 'note', 'source_file']
    },
    'officers': {
        'file': 'nodes-officers.csv', 
        'table': 'icij_officers',
        'cols': ['node_id', 'name', 'icij_id', 'valid_until', 'country_codes',
                'countries', 'sourceid', 'address', 'source_file']
    },
    'addresses': {
        'file': 'nodes-addresses.csv',
        'table': 'icij_addresses',
        'cols': ['node_id', 'address', 'country_codes', 'country', 'sourceid',
                'valid_until', 'source_file']
    },
    'intermediaries': {
        'file': 'nodes-intermediaries.csv',
        'table': 'icij_intermediaries',
        'cols': ['node_id', 'name', 'internal_id', 'address', 'valid_until',
                'country_codes', 'countries', 'sourceid', 'status', 'source_file']
    },
    'others': {
        'file': 'nodes-others.csv',
        'table': 'icij_others',
        'cols': ['node_id', 'name', 'sourceid', 'valid_until', 'source_file']
    },
    'relationships': {
        'file': 'relationships.csv',
        'table': 'icij_relationships',
        'cols': ['node_id_start', 'node_id_end', 'rel_type', 'link', 'status',
                'start_date', 'end_date', 'sourceid', 'source_file']
    }
}

async def import_file(worker_id, table_key, batch_size=10000):
    """Import a single CSV file."""
    config = TABLES[table_key]
    file_path = DATA_DIR / config['file']
    table_name = config['table']
    columns = config['cols']
    
    if not file_path.exists():
        print(f"[{worker_id}] File not found: {file_path}")
        return 0
    
    conn = await asyncpg.connect(DB_URL)
    
    # Mark as running
    await conn.execute("""
        UPDATE icij_import_progress 
        SET status = 'running', worker_id = $1, started_at = NOW()
        WHERE filename = $2
    """, worker_id, config['file'])
    
    count = 0
    batch = []
    errors = 0
    
    print(f"[{worker_id}] Starting {config['file']}...")
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Extract values based on table type
                if table_key == 'entities':
                    vals = (row.get('node_id'), row.get('name'), row.get('original_name'),
                           row.get('former_name'), row.get('jurisdiction'),
                           row.get('jurisdiction_description'), row.get('company_type'),
                           row.get('address'), row.get('internal_id'),
                           row.get('incorporation_date'), row.get('inactivation_date'),
                           row.get('struck_off_date'), row.get('dorm_date'),
                           row.get('status'), row.get('service_provider'),
                           row.get('ibcRUC'), row.get('country_codes'),
                           row.get('countries'), row.get('sourceID'),
                           row.get('valid_until'), row.get('note'), config['file'])
                elif table_key == 'officers':
                    vals = (row.get('node_id'), row.get('name'), row.get('icij_id'),
                           row.get('valid_until'), row.get('country_codes'),
                           row.get('countries'), row.get('sourceID'),
                           row.get('address'), config['file'])
                elif table_key == 'addresses':
                    vals = (row.get('node_id'), row.get('address'),
                           row.get('country_codes'), row.get('country'),
                           row.get('sourceID'), row.get('valid_until'), config['file'])
                elif table_key == 'intermediaries':
                    vals = (row.get('node_id'), row.get('name'), row.get('internal_id'),
                           row.get('address'), row.get('valid_until'),
                           row.get('country_codes'), row.get('countries'),
                           row.get('sourceID'), row.get('status'), config['file'])
                elif table_key == 'others':
                    vals = (row.get('node_id'), row.get('name'), row.get('sourceID'),
                           row.get('valid_until'), config['file'])
                elif table_key == 'relationships':
                    vals = (row.get('node_id_start'), row.get('node_id_end'),
                           row.get('rel_type'), row.get('link'), row.get('status'),
                           row.get('start_date'), row.get('end_date'),
                           row.get('sourceID'), config['file'])
                else:
                    continue
                
                batch.append(vals)
                
                if len(batch) >= batch_size:
                    await conn.copy_records_to_table(table_name, records=batch, columns=columns)
                    count += len(batch)
                    batch = []
                    
                    # Update progress every 50k rows
                    if count % 50000 == 0:
                        await conn.execute("""
                            UPDATE icij_import_progress 
                            SET rows_imported = $1, updated_at = NOW()
                            WHERE filename = $2
                        """, count, config['file'])
                        print(f"[{worker_id}] {config['file']}: {count:,} rows...")
                        
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"[{worker_id}] Error: {e}")
    
    # Final batch
    if batch:
        await conn.copy_records_to_table(table_name, records=batch, columns=columns)
        count += len(batch)
    
    # Mark complete
    await conn.execute("""
        UPDATE icij_import_progress 
        SET status = 'complete', rows_imported = $1, completed_at = NOW(), updated_at = NOW()
        WHERE filename = $2
    """, count, config['file'])
    
    await conn.close()
    print(f"[{worker_id}] ✓ {config['file']}: {count:,} rows imported ({errors} errors)")
    return count

async def main():
    if len(sys.argv) < 2:
        print("Usage: icij_import_worker.py <table_key> [worker_id]")
        print(f"Available: {', '.join(TABLES.keys())}")
        sys.exit(1)
    
    table_key = sys.argv[1]
    worker_id = sys.argv[2] if len(sys.argv) > 2 else "worker-1"
    
    if table_key not in TABLES:
        print(f"Unknown table: {table_key}")
        sys.exit(1)
    
    count = await import_file(worker_id, table_key)
    print(f"[{worker_id}] Done. Total: {count:,} rows")

if __name__ == "__main__":
    asyncio.run(main())
