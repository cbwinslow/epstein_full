#!/usr/bin/env python3
"""Fast import of jmail.world emails into PostgreSQL using COPY.

This script uses PostgreSQL's COPY command for bulk loading, which is
much faster than individual INSERT statements.

Usage:
    python scripts/import_jmail_emails_fast.py [--batch-size 10000]
"""

import argparse
import io
import json
import sys
from pathlib import Path

import pandas as pd
import psycopg2


# PostgreSQL connection
PG_DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Data paths
JMAIL_DIR = Path("/home/cbwinslow/workspace/epstein-data/supplementary")
EMAILS_PARQUET = JMAIL_DIR / "emails-slim.parquet"


def safe_json(val):
    """Convert value to JSON string safely."""
    if pd.isna(val) or val is None:
        return "[]"
    if isinstance(val, str):
        try:
            json.loads(val)
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
        if isinstance(val, str):
            if len(val) >= 4:
                year_str = val[:4]
                if year_str.isdigit():
                    year = int(year_str)
                    if year < 1990 or year > 2030:
                        return None
            dt = pd.to_datetime(val, utc=True, errors="coerce")
            if pd.isna(dt):
                return None
            return dt.isoformat()
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
    """Convert value to string safely."""
    if pd.isna(val):
        return ""
    s = str(val).strip()
    if max_len and len(s) > max_len:
        s = s[:max_len]
    return s


def prepare_dataframe(df):
    """Prepare dataframe for COPY import."""
    print("Preparing data...")
    
    # Create a new dataframe with properly typed columns
    result = pd.DataFrame()
    result["id"] = df["id"]
    result["doc_id"] = df["doc_id"].apply(lambda x: safe_str(x, 200))
    result["message_index"] = df["message_index"].apply(safe_int)
    result["sender"] = df["sender"].apply(lambda x: safe_str(x, 500))
    result["subject"] = df["subject"].apply(lambda x: safe_str(x, 1000))
    result["to_recipients"] = df["to_recipients"].apply(safe_json)
    result["cc_recipients"] = df["cc_recipients"].apply(safe_json)
    result["bcc_recipients"] = df["bcc_recipients"].apply(safe_json)
    result["sent_at"] = df["sent_at"].apply(parse_timestamp)
    result["attachments"] = df["attachments"].apply(safe_int)
    result["account_email"] = df["account_email"].apply(lambda x: safe_str(x, 200))
    result["email_drop_id"] = df["email_drop_id"].apply(lambda x: safe_str(x, 50))
    result["folder_path"] = df["folder_path"].apply(lambda x: safe_str(x, 200))
    result["is_promotional"] = df["is_promotional"].apply(lambda x: safe_bool(x))
    result["release_batch"] = df["release_batch"].apply(safe_int)
    result["epstein_is_sender"] = df["epstein_is_sender"].apply(lambda x: safe_bool(x))
    result["all_participants"] = df["all_participants"].apply(lambda x: safe_str(x, 2000))
    
    # Replace NaN with None for proper NULL handling
    result = result.where(pd.notna(result), None)
    
    print(f"Prepared {len(result):,} rows")
    return result


def copy_from_dataframe(conn, df, table="jmail_emails"):
    """Use COPY to bulk load data from a dataframe."""
    # Create a StringIO buffer
    buffer = io.StringIO()
    
    # Write data to buffer
    columns = [
        "id", "doc_id", "message_index", "sender", "subject",
        "to_recipients", "cc_recipients", "bcc_recipients",
        "sent_at", "attachments", "account_email", "email_drop_id",
        "folder_path", "is_promotional", "release_batch",
        "epstein_is_sender", "all_participants"
    ]
    
    for _, row in df.iterrows():
        values = []
        for col in columns:
            val = row[col]
            if val is None:
                values.append("\\N")
            elif isinstance(val, str):
                # Escape special characters for COPY
                val = val.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
                values.append(val)
            else:
                values.append(str(val))
        buffer.write("\t".join(values) + "\n")
    
    buffer.seek(0)
    
    # Use COPY to load data
    with conn.cursor() as cur:
        cur.copy_from(
            buffer,
            table,
            columns=columns,
            sep="\t",
            null="\\N"
        )
    conn.commit()


def import_with_copy(df, conn, batch_size=10000):
    """Import using COPY in batches."""
    total = len(df)
    inserted = 0
    
    print(f"\nImporting {total:,} emails using COPY (batch_size={batch_size:,})...")
    
    for i in range(0, total, batch_size):
        batch = df.iloc[i : i + batch_size]
        
        try:
            copy_from_dataframe(conn, batch)
            inserted += len(batch)
        except Exception as e:
            print(f"\n  Error at batch {i}: {e}")
            # Fall back to individual inserts for this batch
            conn.rollback()
            with conn.cursor() as cur:
                for _, row in batch.iterrows():
                    try:
                        cur.execute("""
                            INSERT INTO jmail_emails (
                                id, doc_id, message_index, sender, subject,
                                to_recipients, cc_recipients, bcc_recipients,
                                sent_at, attachments, account_email, email_drop_id,
                                folder_path, is_promotional, release_batch,
                                epstein_is_sender, all_participants
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO NOTHING
                        """, (
                            row["id"], row["doc_id"], row["message_index"],
                            row["sender"], row["subject"],
                            row["to_recipients"], row["cc_recipients"], row["bcc_recipients"],
                            row["sent_at"], row["attachments"], row["account_email"],
                            row["email_drop_id"], row["folder_path"], row["is_promotional"],
                            row["release_batch"], row["epstein_is_sender"], row["all_participants"]
                        ))
                        if cur.rowcount > 0:
                            inserted += 1
                    except Exception as e2:
                        pass
            conn.commit()
        
        # Progress update
        done = min(i + batch_size, total)
        pct = done / total * 100
        print(f"\r  Progress: {done:,}/{total:,} ({pct:.1f}%) inserted={inserted:,}", end="", flush=True)
    
    print(f"\n\nDone! Inserted: {inserted:,}")
    return inserted


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
    parser = argparse.ArgumentParser(description="Fast import jmail.world emails to PostgreSQL")
    parser.add_argument("--batch-size", type=int, default=10000, help="Batch size for COPY")
    parser.add_argument("--verify", action="store_true", help="Just print summary stats")
    args = parser.parse_args()

    # Check parquet file exists
    if not EMAILS_PARQUET.exists():
        print(f"ERROR: {EMAILS_PARQUET} not found")
        sys.exit(1)

    # Connect to PostgreSQL
    conn = psycopg2.connect(PG_DSN)
    try:
        if args.verify:
            print_summary(conn)
            return

        # Check existing count
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM jmail_emails")
            existing = cur.fetchone()[0]
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

        # Prepare data
        prepared_df = prepare_dataframe(df)

        # Import
        import_with_copy(prepared_df, conn, batch_size=args.batch_size)

        # Create indexes
        print("Creating indexes...")
        with conn.cursor() as cur:
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_jmail_emails_sent ON jmail_emails(sent_at);
                CREATE INDEX IF NOT EXISTS idx_jmail_emails_sender ON jmail_emails(sender);
                CREATE INDEX IF NOT EXISTS idx_jmail_emails_account ON jmail_emails(account_email);
                CREATE INDEX IF NOT EXISTS idx_jmail_emails_promo ON jmail_emails(is_promotional);
                CREATE INDEX IF NOT EXISTS idx_jmail_emails_doc ON jmail_emails(doc_id);
                CREATE INDEX IF NOT EXISTS idx_jmail_emails_drop ON jmail_emails(email_drop_id);
                CREATE INDEX IF NOT EXISTS idx_jmail_emails_epstein ON jmail_emails(epstein_is_sender);
            """)
            conn.commit()

        # Print summary
        print_summary(conn)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
