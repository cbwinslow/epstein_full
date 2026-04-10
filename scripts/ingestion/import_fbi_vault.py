#!/usr/bin/env python3
"""Import FBI Vault documents to PostgreSQL.

Imports FBI Vault text files downloaded from Archive.org.

Usage:
    python scripts/import_fbi_vault.py
    python scripts/import_fbi_vault.py --verify
"""

import argparse
import sys
from pathlib import Path

import psycopg2


# PostgreSQL connection
PG_DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Data paths
FBI_DIR = Path("/home/cbwinslow/workspace/epstein-data/fbi-vault")


def get_existing_fbi_docs(conn):
    """Get existing FBI Vault documents."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT efta_number FROM documents 
            WHERE efta_number LIKE 'FBI_VAULT_%'
        """)
        return {row[0] for row in cur.fetchall()}


def import_fbi_vault(conn):
    """Import FBI Vault text files."""
    existing = get_existing_fbi_docs(conn)
    print(f"Existing FBI Vault documents: {len(existing)}")
    
    txt_files = sorted(FBI_DIR.glob("fbi_vault_part_*.txt"))
    print(f"Found {len(txt_files)} FBI Vault text files")
    
    inserted = 0
    errors = 0
    
    ac_conn = psycopg2.connect(PG_DSN)
    ac_conn.autocommit = True
    
    try:
        with ac_conn.cursor() as cur:
            for txt_file in txt_files:
                # Extract part number from filename
                part_num = txt_file.stem.split('_')[-1]
                efta_number = f"FBI_VAULT_PART_{part_num:0>2}"
                
                if efta_number in existing:
                    print(f"  Skipping {efta_number} (already exists)")
                    continue
                
                try:
                    # Read text content
                    text_content = txt_file.read_text(encoding='utf-8', errors='ignore')
                    
                    if not text_content.strip():
                        print(f"  Skipping {efta_number} (empty file)")
                        continue
                    
                    # Count pages (approximate - every 3000 chars = 1 page)
                    page_count = max(1, len(text_content) // 3000)
                    
                    # Insert into documents table
                    cur.execute("""
                        INSERT INTO documents (
                            efta_number, dataset, file_path, total_pages,
                            document_type, source_system
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (efta_number) DO NOTHING
                    """, (
                        efta_number,
                        98,  # FBI Vault dataset ID
                        str(txt_file),
                        page_count,
                        'FBI_INVESTIGATIVE',
                        'archive_org'
                    ))
                    
                    if cur.rowcount > 0:
                        inserted += 1
                        print(f"  Imported {efta_number} ({len(text_content):,} chars, ~{page_count} pages)")
                    else:
                        print(f"  Skipped {efta_number} (conflict)")
                
                except Exception as e:
                    errors += 1
                    print(f"  Error importing {efta_number}: {e}")
    
    finally:
        ac_conn.close()
    
    print(f"\nDone! Inserted: {inserted}, Errors: {errors}")
    return inserted


def verify_import(conn):
    """Verify import results."""
    print("\n=== FBI Vault Import Verification ===")
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) FROM documents 
            WHERE efta_number LIKE 'FBI_VAULT_%'
        """)
        total = cur.fetchone()[0]
        print(f"Total FBI Vault documents: {total}")
        
        cur.execute("""
            SELECT efta_number, total_pages 
            FROM documents 
            WHERE efta_number LIKE 'FBI_VAULT_%'
            ORDER BY efta_number
        """)
        print("\nDocuments:")
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]} pages")


def main():
    parser = argparse.ArgumentParser(description="Import FBI Vault documents")
    parser.add_argument("--verify", action="store_true", help="Just verify")
    args = parser.parse_args()
    
    conn = psycopg2.connect(PG_DSN)
    try:
        if args.verify:
            verify_import(conn)
            return
        
        import_fbi_vault(conn)
        verify_import(conn)
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()
