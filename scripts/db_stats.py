#!/usr/bin/env python3
"""
Epstein Project — Database Statistics

Shows PostgreSQL database size, table sizes, index sizes, and row counts.

Usage:
  python db_stats.py              # Full stats
  python db_stats.py --tables     # Table sizes only
  python db_stats.py --indexes    # Index sizes only
"""

import sys
import os
import argparse
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


def show_database_size(conn):
    """Show overall database size."""
    cur = conn.cursor()
    cur.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
    size = cur.fetchone()[0]
    print(f"\nDatabase Size: {size}")


def show_table_stats(conn):
    """Show table row counts and sizes."""
    cur = conn.cursor()
    cur.execute("""
        SELECT
            relname AS table_name,
            n_live_tup AS rows,
            pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
            pg_size_pretty(pg_relation_size(relid)) AS table_size,
            pg_size_pretty(pg_indexes_size(relid)) AS index_size
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        ORDER BY n_live_tup DESC
    """)

    print(f"\n{'Table':<30} {'Rows':>12} {'Total':>10} {'Table':>10} {'Index':>10}")
    print("-" * 75)

    total_rows = 0
    for row in cur.fetchall():
        table_name, rows, total, table_size, index_size = row
        total_rows += rows or 0
        print(f"  {table_name:<28} {rows or 0:>12,} {total:>10} {table_size:>10} {index_size:>10}")

    print("-" * 75)
    print(f"  {'TOTAL':<28} {total_rows:>12,}")


def show_index_stats(conn):
    """Show index sizes."""
    cur = conn.cursor()
    cur.execute("""
        SELECT
            indexrelname AS index_name,
            relname AS table_name,
            pg_size_pretty(pg_relation_size(indexrelid)) AS size,
            idx_scan AS scans,
            idx_tup_read AS tuples_read
        FROM pg_stat_user_indexes
        WHERE schemaname = 'public'
        ORDER BY pg_relation_size(indexrelid) DESC
        LIMIT 20
    """)

    print(f"\n{'Index':<45} {'Table':<25} {'Size':>10} {'Scans':>8}")
    print("-" * 90)

    for row in cur.fetchall():
        index_name, table_name, size, scans, tuples = row
        print(f"  {index_name:<43} {table_name:<25} {size:>10} {scans or 0:>8,}")


def show_fts_stats(conn):
    """Show FTS coverage."""
    cur = conn.cursor()
    cur.execute("""
        SELECT
            COUNT(*) AS total,
            COUNT(search_vector) AS with_fts,
            ROUND(COUNT(search_vector)::numeric / COUNT(*) * 100, 1) AS pct
        FROM pages
    """)
    total, with_fts, pct = cur.fetchone()
    print(f"\nFTS Coverage: {with_fts:,} / {total:,} ({pct}%)")


def show_extensions(conn):
    """Show installed extensions."""
    cur = conn.cursor()
    cur.execute("SELECT extname, extversion FROM pg_extension ORDER BY extname")
    print("\nExtensions:")
    for name, version in cur.fetchall():
        print(f"  {name}: {version}")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL database statistics")
    parser.add_argument("--tables", action="store_true", help="Show table sizes only")
    parser.add_argument("--indexes", action="store_true", help="Show index sizes only")
    args = parser.parse_args()

    conn = get_conn()

    print("=" * 60)
    print("  EPSTEIN DATABASE STATISTICS")
    print("=" * 60)

    if args.tables:
        show_table_stats(conn)
    elif args.indexes:
        show_index_stats(conn)
    else:
        show_database_size(conn)
        show_table_stats(conn)
        show_index_stats(conn)
        show_fts_stats(conn)
        show_extensions(conn)

    conn.close()
    print()


if __name__ == "__main__":
    main()
