#!/usr/bin/env python3
"""Import House Oversight documents from HuggingFace dataset.

Imports the teyler/epstein-files-20k dataset into PostgreSQL.
This contains 22,944 House Oversight Committee documents.

Usage:
    python scripts/import_house_oversight.py [--batch-size 1000]
    python scripts/import_house_oversight.py --verify
"""

import argparse
import csv
import io
import sys
from pathlib import Path

import pandas as pd
import psycopg2


# PostgreSQL connection
PG_DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Data paths
DATA_DIR = Path("/home/cbwinslow/workspace/epstein-data/hf-house-oversight")
CSV_FILE = DATA_DIR / "EPS_FILES_20K_NOV2025.txt"


def get_existing_eftas(conn):
    """Get existing HOUSE_OVERSIGHT EFTA numbers."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT efta_number FROM documents 
            WHERE efta_number LIKE 'HOUSE_OVERSIGHT%'
        """)
        return {row[0] for row in cur.fetchall()}


def prepare_data(df, existing_eftas):
    """Prepare data for import, filtering out existing records."""
    # Extract EFTA number from filename
    df['efta_number'] = df['filename'].str.extract(r'(HOUSE_OVERSIGHT_\d+)')
    
    # Filter to only HOUSE_OVERSIGHT documents
    df = df[df['efta_number'].notna()].copy()
    
    # Filter out existing records
    df = df[~df['efta_number'].isin(existing_eftas)]
    
    # Aggregate text by EFTA number (combine all pages)
    aggregated = df.groupby('efta_number').agg({
        'text': lambda x: '\n\n'.join([str(t) for t in x if pd.notna(t)]),
        'filename': 'count'
    }).reset_index()
    
    aggregated.columns = ['efta_number', 'text_content', 'page_count']
    
    # Extract document type from filename prefix
    df['doc_type'] = df['filename'].str.extract(r'^([A-Z]+-\d+)')
    doc_types = df.groupby('efta_number')['doc_type'].first().reset_index()
    
    aggregated = aggregated.merge(doc_types, on='efta_number', how='left')
    
    return aggregated


def import_documents(conn, df, batch_size=1000):
    """Import documents in batches."""
    total = len(df)
    inserted = 0
    errors = 0
    
    print(f"\nImporting {total:,} House Oversight documents (batch_size={batch_size})...")
    
    # Use autocommit for batch inserts
    ac_conn = psycopg2.connect(PG_DSN)
    ac_conn.autocommit = True
    
    try:
        with ac_conn.cursor() as cur:
            for i in range(0, total, batch_size):
                batch = df.iloc[i:i+batch_size]
                
                for _, row in batch.iterrows():
                    try:
                        # Insert into documents table (let id auto-increment)
                        cur.execute("""
                            INSERT INTO documents (
                                efta_number, dataset, file_path, total_pages,
                                document_type, source_system
                            ) VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (efta_number) DO NOTHING
                        """, (
                            row['efta_number'],
                            99,  # House Oversight dataset ID
                            f"house_oversight/{row['efta_number']}.txt",
                            int(row['page_count']),
                            row['doc_type'] if pd.notna(row['doc_type']) else 'TEXT',
                            'huggingface_teyler'
                        ))
                        
                        if cur.rowcount > 0:
                            inserted += 1
                    except Exception as e:
                        errors += 1
                        if errors <= 3:
                            print(f"\n  Error: {e}")
                
                # Progress update
                done = min(i + batch_size, total)
                pct = done / total * 100
                print(f"\r  Progress: {done:,}/{total:,} ({pct:.1f}%) inserted={inserted:,} errors={errors}",
                      end="", flush=True)
    
    finally:
        ac_conn.close()
    
    print(f"\n\nDone! Inserted: {inserted:,}, Errors: {errors}")
    return inserted


def verify_import(conn):
    """Verify import results."""
    print("\n=== Import Verification ===")
    
    with conn.cursor() as cur:
        # Count House Oversight documents
        cur.execute("""
            SELECT COUNT(*) FROM documents 
            WHERE efta_number LIKE 'HOUSE_OVERSIGHT%'
        """)
        total = cur.fetchone()[0]
        print(f"Total House Oversight documents: {total:,}")
        
        # Count by dataset
        cur.execute("""
            SELECT dataset, COUNT(*) as cnt 
            FROM documents 
            WHERE efta_number LIKE 'HOUSE_OVERSIGHT%'
            GROUP BY dataset
        """)
        print("\nBy dataset:")
        for row in cur.fetchall():
            print(f"  Dataset {row[0]}: {row[1]:,}")
        
        # Count by document type
        cur.execute("""
            SELECT document_type, COUNT(*) as cnt 
            FROM documents 
            WHERE efta_number LIKE 'HOUSE_OVERSIGHT%'
            GROUP BY document_type
            ORDER BY cnt DESC
            LIMIT 10
        """)
        print("\nBy document type:")
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]:,}")


def main():
    parser = argparse.ArgumentParser(description="Import House Oversight documents")
    parser.add_argument("--batch-size", type=int, default=1000, help="Batch size")
    parser.add_argument("--verify", action="store_true", help="Just verify")
    args = parser.parse_args()
    
    conn = psycopg2.connect(PG_DSN)
    try:
        if args.verify:
            verify_import(conn)
            return
        
        # Check existing records
        existing_eftas = get_existing_eftas(conn)
        print(f"Existing House Oversight documents: {len(existing_eftas):,}")
        
        # Load CSV
        print(f"Loading {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE, quoting=csv.QUOTE_ALL, escapechar='\\', on_bad_lines='skip')
        print(f"CSV rows: {len(df):,}")
        
        # Prepare data
        prepared = prepare_data(df, existing_eftas)
        print(f"New documents to import: {len(prepared):,}")
        
        if len(prepared) == 0:
            print("Nothing to import!")
            verify_import(conn)
            return
        
        # Import
        import_documents(conn, prepared, batch_size=args.batch_size)
        
        # Verify
        verify_import(conn)
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()
