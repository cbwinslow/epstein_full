#!/usr/bin/env python3
"""
Epstein Project — FTS Rebuild

Rebuilds the full-text search vectors for all pages.
Useful after bulk data imports or if FTS is corrupted.

Usage:
  python db_fts_rebuild.py              # Rebuild all FTS
  python db_fts_rebuild.py --check      # Check FTS coverage only
  python db_fts_rebuild.py --batch 50000  # Custom batch size
"""

import argparse
import os
import time

import psycopg2

# =============================================================================
# Configuration
# =============================================================================

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = os.environ.get("PG_PASSWORD", "")
PG_DB = "epstein"
DEFAULT_BATCH = 50000


def get_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASS,
        dbname=PG_DB
    )


def check_fts(conn):
    """Check FTS coverage."""
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total,
               COUNT(search_vector) AS with_fts,
               COUNT(*) - COUNT(search_vector) AS missing,
               ROUND(COUNT(search_vector)::numeric / COUNT(*) * 100, 1) AS pct
        FROM pages
    """)
    total, with_fts, missing, pct = cur.fetchone()

    print("\nFTS Coverage:")
    print(f"  Total pages:    {total:,}")
    print(f"  With FTS:       {with_fts:,}")
    print(f"  Missing:        {missing:,}")
    print(f"  Coverage:       {pct}%")

    # Test search
    cur.execute("SELECT COUNT(*) FROM pages WHERE search_vector @@ plainto_tsquery('english', 'Epstein')")
    test = cur.fetchone()[0]
    print(f"  Search test:    {test:,} pages match 'Epstein'")

    return missing


def rebuild_fts(conn, batch_size):
    """Rebuild FTS vectors in batches."""
    cur = conn.cursor()

    # Get count of missing
    cur.execute("SELECT COUNT(*) FROM pages WHERE search_vector IS NULL")
    total = cur.fetchone()[0]

    if total == 0:
        print("All pages already have FTS. Nothing to rebuild.")
        return

    print(f"Rebuilding FTS for {total:,} pages (batch: {batch_size:,})...")

    conn.autocommit = True
    cur2 = conn.cursor()
    done = 0

    while True:
        start = time.time()
        cur2.execute("""
            UPDATE pages SET search_vector =
                setweight(to_tsvector('english', coalesce(efta_number, '')), 'A') ||
                setweight(to_tsvector('english', substring(coalesce(text_content, ''), 1, 50000)), 'B')
            WHERE id IN (
                SELECT id FROM pages WHERE search_vector IS NULL LIMIT %s
            )
        """, (batch_size,))

        updated = cur2.rowcount
        done += updated
        elapsed = time.time() - start

        if updated == 0:
            break

        pct = done / total * 100
        rate = updated / elapsed if elapsed > 0 else 0
        print(f"  {done:,} / {total:,} ({pct:.1f}%) — {rate:.0f} pages/sec")

    print(f"Done. {done:,} pages indexed.")


def main():
    parser = argparse.ArgumentParser(description="FTS rebuild")
    parser.add_argument("--check", action="store_true", help="Check coverage only")
    parser.add_argument("--batch", type=int, default=DEFAULT_BATCH, help="Batch size")
    args = parser.parse_args()

    conn = get_conn()

    if args.check:
        check_fts(conn)
    else:
        check_fts(conn)
        missing = check_fts(conn)
        if missing > 0:
            rebuild_fts(conn, args.batch)
            check_fts(conn)
        else:
            print("\nFTS is complete. Nothing to rebuild.")

    conn.close()


if __name__ == "__main__":
    main()
