#!/usr/bin/env python3
"""Import jmail.world FULL documents dataset into PostgreSQL.

Imports jmail_documents.parquet into jmail_documents table.

Usage:
    python scripts/import_jmail_documents.py [--dry-run] [--batch-size 1000]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import psycopg2
import psycopg2.extras


# PostgreSQL connection
PG_DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Data paths
DOWNLOADS_DIR = Path("/home/cbwinslow/workspace/epstein-data/downloads")
DOCUMENTS_PARQUET = DOWNLOADS_DIR / "jmail_documents.parquet"

# Batch size for inserts
BATCH_SIZE = 1000

# Schema for jmail_documents table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS jmail_documents (
    id TEXT PRIMARY KEY,
    doc_id TEXT,
    filename TEXT,
    file_size BIGINT,
    mime_type TEXT,
    md5_hash TEXT,
    description TEXT,
    path TEXT,
    email_drop_id TEXT,
    release_batch INT,
    source_file TEXT,
    extracted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_jmail_docs_drop ON jmail_documents(email_drop_id);
CREATE INDEX IF NOT EXISTS idx_jmail_docs_batch ON jmail_documents(release_batch);
CREATE INDEX IF NOT EXISTS idx_jmail_docs_md5 ON jmail_documents(md5_hash);
CREATE INDEX IF NOT EXISTS idx_jmail_docs_mime ON jmail_documents(mime_type);
"""

INSERT_SQL = """
INSERT INTO jmail_documents (
    id, doc_id, filename, file_size, mime_type, md5_hash,
    description, path, email_drop_id, release_batch, source_file, extracted_at
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING
"""


def safe_str(val, max_len=None):
    """Convert value to string safely, truncating if needed."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    if not s:
        return None
    if max_len and len(s) > max_len:
        s = s[:max_len]
    return s


def safe_int(val, default=None):
    """Convert value to int safely."""
    if pd.isna(val):
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def safe_timestamp(val):
    """Parse timestamp safely."""
    if pd.isna(val):
        return None
    try:
        dt = pd.to_datetime(val, utc=True, errors="coerce")
        if pd.isna(dt):
            return None
        return dt.to_pydatetime()
    except Exception:
        return None


def prepare_row(row):
    """Prepare a row for insertion."""
    return (
        str(row["id"]),
        safe_str(row.get("doc_id"), 200),
        safe_str(row.get("filename"), 500),
        safe_int(row.get("file_size")),
        safe_str(row.get("mime_type"), 100),
        safe_str(row.get("md5_hash"), 64),
        safe_str(row.get("description"), 2000),
        safe_str(row.get("path"), 500),
        safe_str(row.get("email_drop_id"), 50),
        safe_int(row.get("release_batch")),
        safe_str(row.get("source_file"), 500),
        safe_timestamp(row.get("extracted_at")),
    )


def get_existing_count(conn):
    """Get count of existing rows."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM jmail_documents")
        return cur.fetchone()[0]


def import_documents(df, conn, dry_run=False, batch_size=BATCH_SIZE):
    """Import documents in batches."""
    total = len(df)
    inserted = 0
    errors = 0
    skipped = 0

    print(f"\nImporting {total:,} documents (batch_size={batch_size})...")

    if not dry_run:
        ac_conn = psycopg2.connect(PG_DSN)
        ac_conn.autocommit = True
    else:
        ac_conn = None

    try:
        for i in range(0, total, batch_size):
            batch = df.iloc[i : i + batch_size]
            batch_inserted = 0
            batch_errors = 0

            if not dry_run:
                with ac_conn.cursor() as cur:
                    for _, row in batch.iterrows():
                        try:
                            values = prepare_row(row)
                            cur.execute(INSERT_SQL, values)
                            if cur.rowcount > 0:
                                batch_inserted += 1
                            else:
                                skipped += 1
                        except Exception as e:
                            batch_errors += 1
                            if batch_errors <= 3:
                                print(f"\n  Error on row {i}: {e}")

            inserted += batch_inserted
            errors += batch_errors

            done = min(i + batch_size, total)
            pct = done / total * 100
            print(
                f"\r  Progress: {done:,}/{total:,} ({pct:.1f}%) "
                f"inserted={inserted:,} skipped={skipped:,} errors={errors}",
                end="",
                flush=True,
            )

    finally:
        if ac_conn:
            ac_conn.close()

    print(f"\n\nDone! Inserted: {inserted:,}, Skipped: {skipped:,}, Errors: {errors}")
    return inserted, skipped, errors


def print_summary(conn):
    """Print summary statistics."""
    print("\n=== Import Summary ===")

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT COUNT(*) as cnt FROM jmail_documents")
        total = cur.fetchone()["cnt"]
        print(f"Total documents: {total:,}")

        cur.execute("""
            SELECT email_drop_id, COUNT(*) as cnt
            FROM jmail_documents
            GROUP BY email_drop_id
            ORDER BY cnt DESC
        """)
        print("\nBy source:")
        for row in cur.fetchall():
            print(f"  {row['email_drop_id']}: {row['cnt']:,}")

        cur.execute("""
            SELECT mime_type, COUNT(*) as cnt
            FROM jmail_documents
            WHERE mime_type IS NOT NULL
            GROUP BY mime_type
            ORDER BY cnt DESC
            LIMIT 10
        """)
        print("\nTop MIME types:")
        for row in cur.fetchall():
            print(f"  {row['mime_type']}: {row['cnt']:,}")


def main():
    parser = argparse.ArgumentParser(description="Import jmail.world documents to PostgreSQL")
    parser.add_argument("--dry-run", action="store_true", help="Parse only, don't insert")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--verify", action="store_true", help="Just print summary stats")
    args = parser.parse_args()

    if not DOCUMENTS_PARQUET.exists():
        print(f"ERROR: {DOCUMENTS_PARQUET} not found")
        sys.exit(1)

    conn = psycopg2.connect(PG_DSN)
    try:
        if args.verify:
            print_summary(conn)
            return

        print("Creating jmail_documents table...")
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
            conn.commit()

        existing = get_existing_count(conn)
        print(f"Existing rows: {existing:,}")

        print(f"Loading {DOCUMENTS_PARQUET}...")
        df = pd.read_parquet(DOCUMENTS_PARQUET)
        print(f"Parquet rows: {len(df):,}")
        print(f"Columns: {list(df.columns)}")

        if existing > 0:
            print("Checking for existing IDs to skip...")
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM jmail_documents")
                existing_ids = {row[0] for row in cur.fetchall()}
            before = len(df)
            df = df[~df.id.isin(existing_ids)]
            print(f"New rows to insert: {len(df):,} (skipped {before - len(df):,} existing)")

        if len(df) == 0:
            print("Nothing to insert!")
            print_summary(conn)
            return

        inserted, skipped, errors = import_documents(df, conn, dry_run=args.dry_run, batch_size=args.batch_size)

        if not args.dry_run:
            print("Creating indexes...")
            with conn.cursor() as cur:
                cur.execute(CREATE_INDEXES_SQL)
                conn.commit()

            print_summary(conn)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
