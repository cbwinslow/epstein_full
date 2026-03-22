#!/usr/bin/env python3
"""
Epstein Project — Database Maintenance

Runs VACUUM ANALYZE on all tables to reclaim space and update statistics.
PostgreSQL autovacuum handles most cases, but manual VACUUM is useful after
large migrations or bulk deletes.

Usage:
  python db_vacuum.py              # VACUUM ANALYZE all tables
  python db_vacuum.py --full       # VACUUM FULL (reclaims more space, locks tables)
  python db_vacuum.py --analyze    # ANALYZE only (no vacuum)
"""

import sys
import os
import argparse
import os
import time
import os
import psycopg2
import os

# =============================================================================
# Configuration
# =============================================================================

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = os.environ.get("PG_PASSWORD", "")
PG_DB = "epstein"


def get_conn():
    """Get PostgreSQL connection."""
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASS,
        dbname=PG_DB
    )


def get_tables(conn):
    """Get list of user tables."""
    cur = conn.cursor()
    cur.execute("""
        SELECT relname FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        ORDER BY n_live_tup DESC
    """)
    return [row[0] for row in cur.fetchall()]


def vacuum_table(conn, table, full=False):
    """Run VACUUM on a single table."""
    conn.autocommit = True
    cur = conn.cursor()
    cmd = f"VACUUM {'FULL' if full else ''} ANALYZE {table}"
    start = time.time()
    try:
        cur.execute(cmd)
        elapsed = time.time() - start
        print(f"  ✓ {table} ({elapsed:.1f}s)")
    except Exception as e:
        print(f"  ✗ {table}: {e}")


def analyze_table(conn, table):
    """Run ANALYZE on a single table."""
    conn.autocommit = True
    cur = conn.cursor()
    start = time.time()
    try:
        cur.execute(f"ANALYZE {table}")
        elapsed = time.time() - start
        print(f"  ✓ {table} ({elapsed:.1f}s)")
    except Exception as e:
        print(f"  ✗ {table}: {e}")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL maintenance")
    parser.add_argument("--full", action="store_true", help="VACUUM FULL (locks tables)")
    parser.add_argument("--analyze", action="store_true", help="ANALYZE only")
    args = parser.parse_args()

    conn = get_conn()
    tables = get_tables(conn)

    mode = "ANALYZE" if args.analyze else f"VACUUM {'FULL' if args.full else ''} ANALYZE"
    print(f"\nRunning {mode} on {len(tables)} tables...\n")

    start = time.time()
    for table in tables:
        if args.analyze:
            analyze_table(conn, table)
        else:
            vacuum_table(conn, table, full=args.full)

    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s")

    conn.close()


if __name__ == "__main__":
    main()
