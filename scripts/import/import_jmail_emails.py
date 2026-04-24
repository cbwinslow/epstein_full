#!/usr/bin/env python3
"""Import jmail.world emails into PostgreSQL.

Downloads emails-slim.parquet from jmail.world (1.78M emails) and imports
into a jmail_emails table. Handles 4 distinct email sources:
- VOL00009-12: DOJ EFTA document emails (1.75M)
- yahoo_2: Epstein's personal Yahoo inbox (17K)
- House Oversight: Congressional releases (8K)
- Ehud Barak: Former Israeli PM emails (1K)

Usage:
    python scripts/import_jmail_emails.py [--dry-run] [--batch-size 500]
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
JMAIL_DIR = Path("/home/cbwinslow/workspace/epstein-data/supplementary")
EMAILS_PARQUET = JMAIL_DIR / "emails-slim.parquet"

# Batch size for inserts
BATCH_SIZE = 500

# Schema for jmail_emails table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS jmail_emails (
    id TEXT PRIMARY KEY,
    doc_id TEXT,
    message_index TEXT,
    sender TEXT,
    subject TEXT,
    to_recipients JSONB DEFAULT '[]',
    cc_recipients JSONB DEFAULT '[]',
    bcc_recipients JSONB DEFAULT '[]',
    sent_at TIMESTAMPTZ,
    attachments INT DEFAULT 0,
    account_email TEXT,
    email_drop_id TEXT,
    folder_path TEXT,
    is_promotional BOOLEAN DEFAULT FALSE,
    release_batch INT,
    epstein_is_sender BOOLEAN DEFAULT FALSE,
    all_participants TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_jmail_emails_sent ON jmail_emails(sent_at);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_sender ON jmail_emails(sender);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_account ON jmail_emails(account_email);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_promo ON jmail_emails(is_promotional);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_doc ON jmail_emails(doc_id);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_drop ON jmail_emails(email_drop_id);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_epstein ON jmail_emails(epstein_is_sender);
"""

INSERT_SQL = """
INSERT INTO jmail_emails (
    id, doc_id, message_index, sender, subject,
    to_recipients, cc_recipients, bcc_recipients,
    sent_at, attachments, account_email, email_drop_id,
    folder_path, is_promotional, release_batch,
    epstein_is_sender, all_participants
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (id) DO NOTHING
"""


def safe_json(val):
    """Convert value to JSON string safely."""
    if pd.isna(val) or val is None:
        return "[]"
    if isinstance(val, str):
        try:
            json.loads(val)  # Validate it's valid JSON
            return val
        except (json.JSONDecodeError, ValueError):
            return "[]"
    if isinstance(val, list):
        return json.dumps(val)
    return "[]"


def parse_timestamp(val):
    """Parse timestamp, filtering out obviously wrong dates."""
    if pd.isna(val):
        return None
    try:
        # Handle ISO format strings
        if isinstance(val, str):
            # Quick sanity check on year
            if len(val) >= 4:
                year_str = val[:4]
                if year_str.isdigit():
                    year = int(year_str)
                    if year < 1990 or year > 2030:
                        return None
            dt = pd.to_datetime(val, utc=True, errors="coerce")
            if pd.isna(dt):
                return None
            return dt.to_pydatetime()
        return None
    except Exception:
        return None


def safe_bool(val, default=False):
    """Convert value to boolean safely."""
    if pd.isna(val):
        return default
    return bool(val)


def safe_int(val, default=0):
    """Convert value to int safely."""
    if pd.isna(val):
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


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


def prepare_row(row):
    """Prepare a row for insertion."""
    return (
        row["id"],
        safe_str(row.get("doc_id"), 200),
        safe_int(row.get("message_index")),
        safe_str(row.get("sender"), 500),
        safe_str(row.get("subject"), 1000),
        safe_json(row.get("to_recipients")),
        safe_json(row.get("cc_recipients")),
        safe_json(row.get("bcc_recipients")),
        parse_timestamp(row.get("sent_at")),
        safe_int(row.get("attachments")),
        safe_str(row.get("account_email"), 200),
        safe_str(row.get("email_drop_id"), 50),
        safe_str(row.get("folder_path"), 200),
        safe_bool(row.get("is_promotional")),
        safe_int(row.get("release_batch")),
        safe_bool(row.get("epstein_is_sender")),
        safe_str(row.get("all_participants"), 2000),
    )


def get_existing_count(conn):
    """Get count of existing rows in jmail_emails."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM jmail_emails")
        return cur.fetchone()[0]


def import_emails(df, conn, dry_run=False, batch_size=BATCH_SIZE):
    """Import emails in batches."""
    total = len(df)
    inserted = 0
    errors = 0
    skipped = 0

    print(f"\nImporting {total:,} emails (batch_size={batch_size})...")

    # Use autocommit for batch inserts to avoid transaction abort cascading
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

            # Progress update
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
    """Print summary statistics after import."""
    print("\n=== Import Summary ===")

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        # Total count
        cur.execute("SELECT COUNT(*) as cnt FROM jmail_emails")
        total = cur.fetchone()["cnt"]
        print(f"Total emails: {total:,}")

        # By source
        cur.execute("""
            SELECT email_drop_id, COUNT(*) as cnt
            FROM jmail_emails
            GROUP BY email_drop_id
            ORDER BY cnt DESC
        """)
        print("\nBy source:")
        for row in cur.fetchall():
            print(f"  {row['email_drop_id']}: {row['cnt']:,}")

        # Epstein sent
        cur.execute("""
            SELECT epstein_is_sender, COUNT(*) as cnt
            FROM jmail_emails
            GROUP BY epstein_is_sender
        """)
        print("\nEpstein as sender:")
        for row in cur.fetchall():
            label = "Yes" if row["epstein_is_sender"] else "No"
            print(f"  {label}: {row['cnt']:,}")

        # Promotional
        cur.execute("""
            SELECT is_promotional, COUNT(*) as cnt
            FROM jmail_emails
            GROUP BY is_promotional
        """)
        print("\nPromotional:")
        for row in cur.fetchall():
            label = "Yes" if row["is_promotional"] else "No"
            print(f"  {label}: {row['cnt']:,}")

        # Date range
        cur.execute("""
            SELECT MIN(sent_at) as earliest, MAX(sent_at) as latest
            FROM jmail_emails
            WHERE sent_at IS NOT NULL
        """)
        row = cur.fetchone()
        print(f"\nDate range: {row['earliest']} to {row['latest']}")

        # Top senders
        cur.execute("""
            SELECT sender, COUNT(*) as cnt
            FROM jmail_emails
            WHERE sender IS NOT NULL AND sender != ''
            GROUP BY sender
            ORDER BY cnt DESC
            LIMIT 10
        """)
        print("\nTop 10 senders:")
        for row in cur.fetchall():
            print(f"  {row['sender'][:60]}: {row['cnt']:,}")


def main():
    parser = argparse.ArgumentParser(description="Import jmail.world emails to PostgreSQL")
    parser.add_argument("--dry-run", action="store_true", help="Parse only, don't insert")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--verify", action="store_true", help="Just print summary stats")
    args = parser.parse_args()

    # Check parquet file exists
    if not EMAILS_PARQUET.exists():
        print(f"ERROR: {EMAILS_PARQUET} not found")
        print("Download with: curl -o {path} https://data.jmail.world/v1/emails-slim.parquet")
        sys.exit(1)

    # Connect to PostgreSQL
    conn = psycopg2.connect(PG_DSN)
    try:
        if args.verify:
            print_summary(conn)
            return

        # Create table and indexes
        print("Creating jmail_emails table...")
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
            conn.commit()

        # Check existing count
        existing = get_existing_count(conn)
        print(f"Existing rows: {existing:,}")

        # Load parquet
        print(f"Loading {EMAILS_PARQUET}...")
        df = pd.read_parquet(EMAILS_PARQUET)
        print(f"Parquet rows: {len(df):,}")

        # Filter out existing IDs if needed
        if existing > 0:
            print("Checking for existing IDs to skip...")
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM jmail_emails")
                existing_ids = {row[0] for row in cur.fetchall()}
            before = len(df)
            df = df[~df.id.isin(existing_ids)]
            print(f"New rows to insert: {len(df):,} (skipped {before - len(df):,} existing)")

        if len(df) == 0:
            print("Nothing to insert!")
            print_summary(conn)
            return

        # Import
        inserted, skipped, errors = import_emails(df, conn, dry_run=args.dry_run, batch_size=args.batch_size)

        if not args.dry_run:
            # Create indexes
            print("Creating indexes...")
            with conn.cursor() as cur:
                cur.execute(CREATE_INDEXES_SQL)
                conn.commit()

            # Print summary
            print_summary(conn)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
