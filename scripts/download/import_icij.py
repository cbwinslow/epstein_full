#!/usr/bin/env python3
"""Import ICIJ Offshore Leaks data into PostgreSQL.

Imports all CSV files from the ICIJ Offshore Leaks database:
- nodes-entities.csv (companies/offshore entities)
- nodes-officers.csv (people/officers)
- nodes-addresses.csv (addresses)
- nodes-intermediaries.csv (intermediaries/brokers)
- nodes-others.csv (other entities)
- relationships.csv (entity relationships)

Usage:
    python scripts/import_icij.py [--dry-run] [--batch-size 5000]
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

import psycopg2
import psycopg2.extras


# PostgreSQL connection
PG_DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Data paths
ICIJ_DIR = Path("/home/cbwinslow/workspace/epstein-data/downloads/icij_extracted")

# Batch size for inserts
BATCH_SIZE = 5000

# Table creation SQL
CREATE_TABLES_SQL = """
-- ICIJ Entities (companies/offshore entities)
CREATE TABLE IF NOT EXISTS icij_entities (
    node_id BIGINT PRIMARY KEY,
    name TEXT,
    original_name TEXT,
    former_name TEXT,
    jurisdiction TEXT,
    jurisdiction_description TEXT,
    company_type TEXT,
    address TEXT,
    internal_id TEXT,
    incorporation_date TEXT,
    inactivation_date TEXT,
    struck_off_date TEXT,
    dorm_date TEXT,
    status TEXT,
    service_provider TEXT,
    ibcRUC TEXT,
    country_codes TEXT,
    countries TEXT,
    sourceID TEXT,
    valid_until TEXT,
    note TEXT,
    imported_at TIMESTAMP DEFAULT NOW()
);

-- ICIJ Officers (people)
CREATE TABLE IF NOT EXISTS icij_officers (
    node_id BIGINT PRIMARY KEY,
    name TEXT,
    original_name TEXT,
    former_name TEXT,
    jurisdiction TEXT,
    jurisdiction_description TEXT,
    company_type TEXT,
    address TEXT,
    internal_id TEXT,
    incorporation_date TEXT,
    inactivation_date TEXT,
    struck_off_date TEXT,
    dorm_date TEXT,
    status TEXT,
    service_provider TEXT,
    ibcRUC TEXT,
    country_codes TEXT,
    countries TEXT,
    sourceID TEXT,
    valid_until TEXT,
    note TEXT,
    imported_at TIMESTAMP DEFAULT NOW()
);

-- ICIJ Addresses
CREATE TABLE IF NOT EXISTS icij_addresses (
    node_id BIGINT PRIMARY KEY,
    name TEXT,
    original_name TEXT,
    former_name TEXT,
    jurisdiction TEXT,
    jurisdiction_description TEXT,
    company_type TEXT,
    address TEXT,
    internal_id TEXT,
    incorporation_date TEXT,
    inactivation_date TEXT,
    struck_off_date TEXT,
    dorm_date TEXT,
    status TEXT,
    service_provider TEXT,
    ibcRUC TEXT,
    country_codes TEXT,
    countries TEXT,
    sourceID TEXT,
    valid_until TEXT,
    note TEXT,
    imported_at TIMESTAMP DEFAULT NOW()
);

-- ICIJ Intermediaries
CREATE TABLE IF NOT EXISTS icij_intermediaries (
    node_id BIGINT PRIMARY KEY,
    name TEXT,
    original_name TEXT,
    former_name TEXT,
    jurisdiction TEXT,
    jurisdiction_description TEXT,
    company_type TEXT,
    address TEXT,
    internal_id TEXT,
    incorporation_date TEXT,
    inactivation_date TEXT,
    struck_off_date TEXT,
    dorm_date TEXT,
    status TEXT,
    service_provider TEXT,
    ibcRUC TEXT,
    country_codes TEXT,
    countries TEXT,
    sourceID TEXT,
    valid_until TEXT,
    note TEXT,
    imported_at TIMESTAMP DEFAULT NOW()
);

-- ICIJ Others
CREATE TABLE IF NOT EXISTS icij_others (
    node_id BIGINT PRIMARY KEY,
    name TEXT,
    original_name TEXT,
    former_name TEXT,
    jurisdiction TEXT,
    jurisdiction_description TEXT,
    company_type TEXT,
    address TEXT,
    internal_id TEXT,
    incorporation_date TEXT,
    inactivation_date TEXT,
    struck_off_date TEXT,
    dorm_date TEXT,
    status TEXT,
    service_provider TEXT,
    ibcRUC TEXT,
    country_codes TEXT,
    countries TEXT,
    sourceID TEXT,
    valid_until TEXT,
    note TEXT,
    imported_at TIMESTAMP DEFAULT NOW()
);

-- ICIJ Relationships
CREATE TABLE IF NOT EXISTS icij_relationships (
    id SERIAL PRIMARY KEY,
    node_id_start BIGINT,
    node_id_end BIGINT,
    rel_type TEXT,
    link TEXT,
    status TEXT,
    start_date TEXT,
    end_date TEXT,
    sourceID TEXT,
    imported_at TIMESTAMP DEFAULT NOW()
);
"""

CREATE_INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_icij_entities_name ON icij_entities(name);
CREATE INDEX IF NOT EXISTS idx_icij_entities_jurisdiction ON icij_entities(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_icij_entities_source ON icij_entities(sourceID);
CREATE INDEX IF NOT EXISTS idx_icij_officers_name ON icij_officers(name);
CREATE INDEX IF NOT EXISTS idx_icij_officers_jurisdiction ON icij_officers(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_icij_addresses_address ON icij_addresses(address);
CREATE INDEX IF NOT EXISTS idx_icij_rel_start ON icij_relationships(node_id_start);
CREATE INDEX IF NOT EXISTS idx_icij_rel_end ON icij_relationships(node_id_end);
CREATE INDEX IF NOT EXISTS idx_icij_rel_type ON icij_relationships(rel_type);
"""

# File configurations
FILES_CONFIG = {
    "nodes-entities.csv": {
        "table": "icij_entities",
        "columns": ["node_id", "name", "original_name", "former_name", "jurisdiction",
                   "jurisdiction_description", "company_type", "address", "internal_id",
                   "incorporation_date", "inactivation_date", "struck_off_date", "dorm_date",
                   "status", "service_provider", "ibcRUC", "country_codes", "countries",
                   "sourceID", "valid_until", "note"]
    },
    "nodes-officers.csv": {
        "table": "icij_officers",
        "columns": ["node_id", "name", "original_name", "former_name", "jurisdiction",
                   "jurisdiction_description", "company_type", "address", "internal_id",
                   "incorporation_date", "inactivation_date", "struck_off_date", "dorm_date",
                   "status", "service_provider", "ibcRUC", "country_codes", "countries",
                   "sourceID", "valid_until", "note"]
    },
    "nodes-addresses.csv": {
        "table": "icij_addresses",
        "columns": ["node_id", "name", "original_name", "former_name", "jurisdiction",
                   "jurisdiction_description", "company_type", "address", "internal_id",
                   "incorporation_date", "inactivation_date", "struck_off_date", "dorm_date",
                   "status", "service_provider", "ibcRUC", "country_codes", "countries",
                   "sourceID", "valid_until", "note"]
    },
    "nodes-intermediaries.csv": {
        "table": "icij_intermediaries",
        "columns": ["node_id", "name", "original_name", "former_name", "jurisdiction",
                   "jurisdiction_description", "company_type", "address", "internal_id",
                   "incorporation_date", "inactivation_date", "struck_off_date", "dorm_date",
                   "status", "service_provider", "ibcRUC", "country_codes", "countries",
                   "sourceID", "valid_until", "note"]
    },
    "nodes-others.csv": {
        "table": "icij_others",
        "columns": ["node_id", "name", "original_name", "former_name", "jurisdiction",
                   "jurisdiction_description", "company_type", "address", "internal_id",
                   "incorporation_date", "inactivation_date", "struck_off_date", "dorm_date",
                   "status", "service_provider", "ibcRUC", "country_codes", "countries",
                   "sourceID", "valid_until", "note"]
    },
    "relationships.csv": {
        "table": "icij_relationships",
        "columns": ["node_id_start", "node_id_end", "rel_type", "link", "status",
                   "start_date", "end_date", "sourceID"]
    }
}


def safe_value(val):
    """Clean CSV value for PostgreSQL."""
    if val is None or val == '':
        return None
    return val.strip()


def import_csv_file(filepath, table, columns, conn, dry_run=False, batch_size=BATCH_SIZE):
    """Import a single CSV file to PostgreSQL."""
    total_rows = 0
    inserted = 0
    errors = 0
    
    print(f"\nImporting {filepath.name} -> {table}...")
    
    # Count total rows
    with open(filepath, 'r', encoding='utf-8') as f:
        total_rows = sum(1 for _ in f) - 1  # Exclude header
    
    print(f"  Total rows to import: {total_rows:,}")
    
    if dry_run:
        print(f"  [DRY RUN] Would import {total_rows:,} rows")
        return total_rows, 0, 0
    
    # Build INSERT SQL
    placeholders = ','.join(['%s'] * len(columns))
    insert_sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
    
    # Import with autocommit for batch inserts
    ac_conn = psycopg2.connect(PG_DSN)
    ac_conn.autocommit = True
    
    try:
        batch = []
        processed = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    values = [safe_value(row.get(col)) for col in columns]
                    batch.append(values)
                    
                    if len(batch) >= batch_size:
                        with ac_conn.cursor() as cur:
                            cur.executemany(insert_sql, batch)
                            inserted += len(batch)
                        batch = []
                        
                        processed += batch_size
                        pct = min(processed / total_rows * 100, 100)
                        print(f"\r  Progress: {processed:,}/{total_rows:,} ({pct:.1f}%)", end='', flush=True)
                        
                except Exception as e:
                    errors += 1
                    if errors <= 5:
                        print(f"\n  Error on row {processed}: {e}")
        
        # Insert remaining batch
        if batch:
            with ac_conn.cursor() as cur:
                cur.executemany(insert_sql, batch)
                inserted += len(batch)
            processed += len(batch)
        
        print(f"\r  Progress: {processed:,}/{total_rows:,} (100.0%)")
        print(f"  Done! Inserted: {inserted:,}, Errors: {errors}")
        
    finally:
        ac_conn.close()
    
    return total_rows, inserted, errors


def print_summary(conn):
    """Print summary statistics."""
    print("\n=== ICIJ Import Summary ===")
    
    tables = [
        ('icij_entities', 'Entities'),
        ('icij_officers', 'Officers'),
        ('icij_addresses', 'Addresses'),
        ('icij_intermediaries', 'Intermediaries'),
        ('icij_others', 'Others'),
        ('icij_relationships', 'Relationships')
    ]
    
    total_records = 0
    for table, label in tables:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            total_records += count
            print(f"  {label}: {count:,}")
    
    print(f"\n  Total: {total_records:,} records")
    
    # Show source breakdown
    print("\n=== Sources ===")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT source_id, COUNT(*) as cnt
            FROM icij_entities
            WHERE source_id IS NOT NULL
            GROUP BY source_id
            ORDER BY cnt DESC
        """)
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]:,}")


def main():
    parser = argparse.ArgumentParser(description="Import ICIJ Offshore Leaks to PostgreSQL")
    parser.add_argument("--dry-run", action="store_true", help="Parse only, don't insert")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--file", type=str, help="Import specific file only")
    parser.add_argument("--verify", action="store_true", help="Just print summary stats")
    args = parser.parse_args()

    conn = psycopg2.connect(PG_DSN)
    try:
        if args.verify:
            print_summary(conn)
            return

        print("Creating ICIJ tables...")
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLES_SQL)
            conn.commit()

        total_stats = {"total": 0, "inserted": 0, "errors": 0}
        
        # Import each file
        files_to_import = [args.file] if args.file else list(FILES_CONFIG.keys())
        
        for filename in files_to_import:
            if filename not in FILES_CONFIG:
                print(f"ERROR: Unknown file {filename}")
                continue
                
            filepath = ICIJ_DIR / filename
            if not filepath.exists():
                print(f"WARNING: {filepath} not found, skipping")
                continue
            
            config = FILES_CONFIG[filename]
            total, inserted, errors = import_csv_file(
                filepath, 
                config["table"], 
                config["columns"],
                conn,
                dry_run=args.dry_run,
                batch_size=args.batch_size
            )
            
            total_stats["total"] += total
            total_stats["inserted"] += inserted
            total_stats["errors"] += errors

        if not args.dry_run:
            print("\nCreating indexes...")
            with conn.cursor() as cur:
                cur.execute(CREATE_INDEXES_SQL)
                conn.commit()

            print_summary(conn)
        else:
            print(f"\n[DRY RUN] Would import {total_stats['total']:,} total rows")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
