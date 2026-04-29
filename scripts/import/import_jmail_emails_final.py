#!/usr/bin/env python3
"""
JMail Emails Final Import Script - Reproducible Setup
=====================================================

This script imports the complete JMail emails dataset from the parquet file
into the PostgreSQL database. This is the authoritative script for recreating
the jmail_emails table from scratch.

ORIGINAL ISSUE:
- Original table used `id INTEGER PRIMARY KEY` with sequence
- Source parquet uses string hash IDs (not integers)
- This caused only 1,596,220 rows to load (with wrong integer IDs)
- Full dataset has 1,783,792 rows with string hash IDs

SOLUTION:
- Table recreated with `id TEXT PRIMARY KEY` (matching parquet's string IDs)
- Proper data cleaning (invalid JSON, timestamp validation)
- Batch insert with conflict handling

USAGE:
    # First, ensure table exists with correct schema:
    python3 scripts/import/import_jmail_emails_final.py --create-table

    # Import all data (assumes if interrupted):
    python3 scripts/import/import_jmail_emails_final.py

    # Verify the import:
    python3 scripts/import/import_jmail_emails_final.py --verify

    # Dry run (just check what would be imported):
    python3 scripts/import/import_jmail_emails_final.py --dry-run

AUTHOR: cbwinslow
DATE: 2026-04-25
"""

import argparse
import json
import time
from pathlib import Path

import pandas as pd
import psycopg2

# ============================================================================
# CONFIGURATION
# ============================================================================

# PostgreSQL connection string
PG_DSN = "dbname=epstein user=cbwinslow host=localhost"

# Data paths
JMAIL_DIR = Path("/home/cbwinslow/workspace/epstein-data/supplementary")
EMAILS_PARQUET = JMAIL_DIR / "emails-slim.parquet"

# Expected row count from parquet file
EXPECTED_TOTAL = 1_783_792

# Batch size for inserts
BATCH_SIZE = 5000

# ============================================================================
# SQL STATEMENTS
# ============================================================================

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

# FIXED: 17 placeholders to match 17 columns
INSERT_SQL = """
INSERT INTO jmail_emails (
    id, doc_id, message_index, sender, subject,
    to_recipients, cc_recipients, bcc_recipients,
    sent_at, attachments, account_email, email_drop_id,
    folder_path, is_promotional, release_batch,
    epstein_is_sender, all_participants
) VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s,
    %s, %s, %s
)
ON CONFLICT (id) DO NOTHING
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def safe_json(val):
    """Convert value to valid JSON string safely."""
    if pd.isna(val) or val is None:
        return "[]"
    if isinstance(val, list):
        return json.dumps(val)
    if isinstance(val, str):
        try:
            json.loads(val)  # Validate it's valid JSON
            return val
        except (json.JSONDecodeError, ValueError):
            return "[]"
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
        safe_str(row.get("id")),
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


# ============================================================================
# MAIN IMPORT FUNCTIONS
# ============================================================================


def get_existing_count(conn):
    """Get count of existing rows in jmail_emails."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM jmail_emails")
        return cur.fetchone()[0]


def get_existing_ids(conn):
    """Get set of existing IDs in jmail_emails."""
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM jmail_emails")
        return set(row[0] for row in cur.fetchall())


def import_emails(df, conn, batch_size=BATCH_SIZE):
    """Import emails in batches using cur.executemany."""
    total = len(df)
    inserted = 0
    errors = 0
    skipped = 0

    print(f"\nImporting {total:,} emails (batch_size={batch_size})...")

    start = time.time()

    for i in range(0, total, batch_size):
        batch = df.iloc[i : i + batch_size]
        batch_data = []

        for _, row in batch.iterrows():
            try:
                values = prepare_row(row)
                # Skip rows with no ID
                if values[0] is None:
                    skipped += 1
                    continue
                batch_data.append(values)
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  Error preparing row: {e}")

        if batch_data:
            try:
                with conn.cursor() as cur:
                    # FIXED: Use cur.executemany instead of psycopg2.extras.executemany
                    cur.executemany(INSERT_SQL, batch_data)
                    conn.commit()
                    inserted += len(batch_data)
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  Error inserting batch at {i}: {e}")
                conn.rollback()

        # Progress update
        done = min(i + batch_size, total)
        pct = done / total * 100
        elapsed = time.time() - start
        rate = inserted / elapsed if elapsed > 0 else 0
        print(
            f"\r  Progress: {done:,}/{total:,} ({pct:.1f}%) "
            f"inserted={inserted:,} skipped={skipped:,} errors={errors} ({rate:.0f} rows/s)",
            end="",
            flush=True,
        )

    print(f"\n\nDone! Inserted: {inserted:,}, Skipped: {skipped:,}, Errors: {errors}")
    return inserted, skipped, errors


def print_summary(conn):
    """Print summary statistics after import."""
    print("\n=== Import Summary ===")

    with conn.cursor() as cur:
        # Total count
        cur.execute("SELECT COUNT(*) as cnt FROM jmail_emails")
        total = cur.fetchone()[0]
        print(f"Total emails: {total:,}")
        print(f"Expected: {EXPECTED_TOTAL:,}")
        print(f"Completeness: {total / EXPECTED_TOTAL * 100:.1f}%")

        # By source
        cur.execute("""
            SELECT email_drop_id, COUNT(*) as cnt
            FROM jmail_emails
            GROUP BY email_drop_id
            ORDER BY cnt DESC
        """)
        print("\nBy source:")
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]:,}")

        # Epstein as sender
        cur.execute("""
            SELECT epstein_is_sender, COUNT(*) as cnt
            FROM jmail_emails
            GROUP BY epstein_is_sender
        """)
        print("\nEpstein as sender:")
        for row in cur.fetchall():
            label = "Yes" if row[0] else "No"
            print(f"  {label}: {row[1]:,}")

        # Promotional
        cur.execute("""
            SELECT is_promotional, COUNT(*) as cnt
            FROM jmail_emails
            GROUP BY is_promotional
        """)
        print("\nPromotional:")
        for row in cur.fetchall():
            label = "Yes" if row[0] else "No"
            print(f"  {label}: {row[1]:,}")

        # Date range
        cur.execute("""
            SELECT MIN(sent_at) as earliest, MAX(sent_at) as latest
            FROM jmail_emails
            WHERE sent_at IS NOT NULL
        """)
        row = cur.fetchone()
        if row[0]:
            print(f"\nDate range: {row[0]} to {row[1]}")

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
            print(f"  {row[0][:60]}: {row[1]:,}")


def create_table(conn):
    """Create the jmail_emails table with correct schema."""
    print("Creating jmail_emails table with correct schema...")
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
    print("Table created (or already exists).")


def create_indexes(conn):
    """Create indexes on jmail_emails table."""
    print("Creating indexes...")
    with conn.cursor() as cur:
        cur.execute(CREATE_INDEXES_SQL)
        conn.commit()
    print("Indexes created (or already exist).")


def main():
    parser = argparse.ArgumentParser(
        description="Import JMail emails to PostgreSQL - Reproducible Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create table with correct schema:
  python3 scripts/import/import_jmail_emails_final.py --create-table

  # Import all data:
  python3 scripts/import/import_jmail_emails_final.py

  # Verify only:
  python3 scripts/import/import_jmail_emails_final.py --verify

  # Dry run (check what would be imported):
  python3 scripts/import/import_jmail_emails_final.py --dry-run
""",
    )
    parser.add_argument("--dry-run", action="store_true", help="Parse only, don't insert")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--verify", action="store_true", help="Just print summary stats")
    parser.add_argument(
        "--create-table", action="store_true", help="Create table with correct schema"
    )
    args = parser.parse_args()

    # Check parquet file exists
    if not EMAILS_PARQUET.exists():
        print(f"ERROR: {EMAILS_PARQUET} not found")
        print(
            f"Download with: curl -o {EMAILS_PARQUET} https://data.jmail.world/v1/emails-slim.parquet"
        )
        return 1

    # Connect to PostgreSQL
    conn = psycopg2.connect(PG_DSN)
    try:
        if args.create_table:
            create_table(conn)
            create_indexes(conn)
            return 0

        if args.verify:
            print_summary(conn)
            return 0

        # Create table and indexes
        print("Setting up database...")
        create_table(conn)

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
            existing_ids = get_existing_ids(conn)
            before = len(df)
            df = df[~df["id"].astype(str).isin(existing_ids)]
            print(f"New rows to insert: {len(df):,} (skipped {before - len(df):,} existing)")

        if len(df) == 0:
            print("\nNothing to insert!")
            print_summary(conn)
            return 0

        # Import
        inserted, skipped, errors = import_emails(df, conn, batch_size=args.batch_size)

        # Create indexes
        create_indexes(conn)

        # Print summary
        print_summary(conn)

        if inserted + skipped == len(df):
            print("\n✓ All rows processed successfully!")
            return 0
        else:
            print("\n⚠ Some rows may have been skipped or errored")
            return 1

    except Exception as e:
        import traceback

        print(f"\nERROR: {e}")
        traceback.print_exc()
        conn.rollback()
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    exit(main())
