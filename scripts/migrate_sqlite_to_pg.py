#!/usr/bin/env python3
"""
Epstein SQLite-to-PostgreSQL Migration — Comprehensive & Re-runnable

Migrates all 8 SQLite databases into unified PostgreSQL.
Skips tables that already match. Truncates & remigrates mismatches.
Validates every table at the end.

Usage:
  python migrate_sqlite_to_pg.py              # Run migration (skip matches)
  python migrate_sqlite_to_pg.py --force      # Force re-migrate everything
  python migrate_sqlite_to_pg.py --validate   # Just validate, don't migrate
  python migrate_sqlite_to_pg.py --db full_text_corpus  # Migrate one DB only
"""

import os
import io
import sys
import csv
import sqlite3
import argparse
from datetime import datetime

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = "123qweasd"
PG_DB = "epstein"
DB_DIR = "/mnt/data/epstein-project/databases"
BATCH = 200000

# Master table mapping: (sqlite_db, sqlite_table, pg_table, column_map)
# column_map renames SQLite columns to PG column names (e.g. extracted_entities -> redaction_entities)
TABLE_MAP = [
    # full_text_corpus.db
    ("full_text_corpus.db", "documents", "documents", None),
    ("full_text_corpus.db", "pages", "pages", None),
    ("full_text_corpus.db", "document_classification", "document_classification", None),
    ("full_text_corpus.db", "efta_crosswalk", "efta_crosswalk", None),
    # redaction_analysis_v2.db
    ("redaction_analysis_v2.db", "redactions", "redactions", None),
    ("redaction_analysis_v2.db", "document_summary", "document_summary", None),
    ("redaction_analysis_v2.db", "reconstructed_pages", "reconstructed_pages", None),
    (
        "redaction_analysis_v2.db",
        "extracted_entities",
        "redaction_entities",
        {"extracted_entities": "redaction_entities"},
    ),
    # communications.db
    ("communications.db", "emails", "emails", None),
    ("communications.db", "email_participants", "email_participants", None),
    ("communications.db", "resolved_identities", "resolved_identities", None),
    ("communications.db", "communication_pairs", "communication_pairs", None),
    # knowledge_graph.db
    ("knowledge_graph.db", "entities", "entities", None),
    ("knowledge_graph.db", "relationships", "relationships", None),
    ("knowledge_graph.db", "edge_sources", "edge_sources", None),
    # ocr_database.db
    ("ocr_database.db", "ocr_results", "ocr_results", None),
    # image_analysis.db
    ("image_analysis.db", "images", "images", None),
    # transcripts.db
    ("transcripts.db", "transcripts", "transcripts", None),
    ("transcripts.db", "transcript_segments", "transcript_segments", None),
    # prosecutorial_query_graph.db
    ("prosecutorial_query_graph.db", "subpoenas", "subpoenas", None),
    ("prosecutorial_query_graph.db", "rider_clauses", "rider_clauses", None),
    ("prosecutorial_query_graph.db", "returns", "returns", None),
    ("prosecutorial_query_graph.db", "subpoena_return_links", "subpoena_return_links", None),
    ("prosecutorial_query_graph.db", "clause_fulfillment", "clause_fulfillment", None),
    ("prosecutorial_query_graph.db", "graph_nodes", "graph_nodes", None),
    ("prosecutorial_query_graph.db", "graph_edges", "graph_edges", None),
    ("prosecutorial_query_graph.db", "investigative_gaps", "investigative_gaps", None),
]

# Cache SQLite connections to avoid reopening
_sq_conns = {}


def get_pg_conn():
    import psycopg2

    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASS,
        dbname=PG_DB,
    )


def get_sq_conn(db_file):
    if db_file not in _sq_conns:
        path = os.path.join(DB_DIR, db_file)
        if not os.path.exists(path):
            print(f"  WARNING: {path} not found, skipping")
            return None
        _sq_conns[db_file] = sqlite3.connect(path)
    return _sq_conns[db_file]


def get_sq_count(sq_conn, table):
    try:
        cur = sq_conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        return cur.fetchone()[0]
    except Exception:
        return 0


def get_pg_count(pg_conn, table):
    cur = pg_conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    return cur.fetchone()[0]


def escape_text(val):
    """Escape a value for PostgreSQL COPY TEXT format."""
    if val is None:
        return "\\N"
    s = str(val).replace("\x00", "")
    s = s.replace("\\", "\\\\")
    s = s.replace("\t", "\\t")
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    return s


def migrate_table(pg_conn, sq_conn, sq_table, pg_table, column_map=None):
    """Migrate one table using COPY protocol. Truncates PG table first."""
    cur_sq = sq_conn.cursor()
    cur_sq.execute(f"PRAGMA table_info({sq_table})")
    sq_cols = [row[1] for row in cur_sq.fetchall()]

    if column_map:
        pg_cols = [column_map.get(c, c) for c in sq_cols]
    else:
        pg_cols = list(sq_cols)

    cur_sq.execute(f"SELECT * FROM {sq_table}")
    col_str = ", ".join(pg_cols)

    cur_pg = pg_conn.cursor()
    cur_pg.execute(f"TRUNCATE TABLE {pg_table} CASCADE")
    pg_conn.commit()

    total = get_sq_count(sq_conn, sq_table)
    if total == 0:
        print(f"    {pg_table}: 0 rows, nothing to migrate")
        return 0

    migrated = 0
    while True:
        rows = cur_sq.fetchmany(BATCH)
        if not rows:
            break

        buf = io.StringIO()
        for row in rows:
            buf.write("\t".join(escape_text(v) for v in row) + "\n")
        buf.seek(0)

        cur_pg.copy_expert(f"COPY {pg_table} ({col_str}) FROM STDIN", buf)
        pg_conn.commit()
        migrated += len(rows)
        print(f"    {pg_table}: {migrated:,} / {total:,}")

    return migrated


def migrate_one_db(pg_conn, db_file, sq_table, pg_table, column_map=None):
    """Migrate a single table from one SQLite DB."""
    sq_conn = get_sq_conn(db_file)
    if sq_conn is None:
        return 0
    return migrate_table(pg_conn, sq_conn, sq_table, pg_table, column_map)


def run_migration(force=False):
    """Run full migration. Skips tables whose counts already match (unless force=True)."""
    pg_conn = get_pg_conn()

    print("=" * 60)
    print("EPSTEIN SQLite → PostgreSQL Migration")
    print("=" * 60)

    migrated = 0
    skipped = 0
    failed = 0

    for db_file, sq_table, pg_table, col_map in TABLE_MAP:
        sq_conn = get_sq_conn(db_file)
        if sq_conn is None:
            print(f"  SKIP {pg_table}: SQLite DB not found")
            failed += 1
            continue

        sq_count = get_sq_count(sq_conn, sq_table)
        pg_count = get_pg_count(pg_conn, pg_table)

        if not force and sq_count == pg_count and sq_count > 0:
            print(f"  OK   {pg_table}: {pg_count:,} rows (matches)")
            skipped += 1
            continue

        if sq_count == 0 and pg_count == 0:
            print(f"  OK   {pg_table}: empty in both, skipping")
            skipped += 1
            continue

        tag = "FORCE" if force else "FIX"
        print(f"  {tag}  {pg_table}: SQLite={sq_count:,} PG={pg_count:,}")

        try:
            n = migrate_one_db(pg_conn, db_file, sq_table, pg_table, col_map)
            print(f"    → migrated {n:,} rows")
            migrated += 1
        except Exception as e:
            print(f"    → FAILED: {e}")
            failed += 1

    pg_conn.close()

    # Clean up SQLite connections
    for c in _sq_conns.values():
        c.close()
    _sq_conns.clear()

    print()
    print(f"Done: {migrated} migrated, {skipped} skipped, {failed} failed")
    return failed == 0


def validate():
    """Compare SQLite vs PostgreSQL row counts for every table."""
    pg_conn = get_pg_conn()

    print("=" * 60)
    print("VALIDATION: SQLite vs PostgreSQL")
    print("=" * 60)
    print(f"{'Table':<30} {'SQLite':>10} {'PostgreSQL':>10} {'Status':>10}")
    print("-" * 62)

    all_ok = True
    total_sq = 0
    total_pg = 0

    for db_file, sq_table, pg_table, _ in TABLE_MAP:
        sq_conn = get_sq_conn(db_file)
        sq_count = get_sq_count(sq_conn, sq_table) if sq_conn else 0
        pg_count = get_pg_count(pg_conn, pg_table)

        total_sq += sq_count
        total_pg += pg_count

        if sq_count == 0 and pg_count == 0:
            status = "EMPTY"
        elif sq_count == pg_count:
            status = "OK"
        elif pg_count > sq_count:
            status = f"EXCESS +{pg_count - sq_count}"
            all_ok = False
        else:
            status = f"MISSING {sq_count - pg_count}"
            all_ok = False

        print(f"{pg_table:<30} {sq_count:>10,} {pg_count:>10,} {status:>10}")

    print("-" * 62)
    print(f"{'TOTAL':<30} {total_sq:>10,} {total_pg:>10,}")

    # Check PG-only tables (no SQLite source)
    print()
    print("Application tables (no SQLite source):")
    for t in ["tasks", "task_history", "file_registry", "external_references"]:
        c = get_pg_count(pg_conn, t)
        print(f"  {t}: {c:,} rows")

    pg_conn.close()
    for c in _sq_conns.values():
        c.close()
    _sq_conns.clear()

    print()
    if all_ok:
        print("ALL TABLES MATCH — migration is complete")
    else:
        print("MISMATCHES FOUND — run without --validate to fix")
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Epstein SQLite-to-PostgreSQL migration")
    parser.add_argument("--validate", action="store_true", help="Validate only, don't migrate")
    parser.add_argument("--force", action="store_true", help="Force re-migrate all tables")
    parser.add_argument(
        "--db",
        type=str,
        help="Migrate one DB: full_text_corpus, knowledge_graph, communications, redaction, image_analysis, ocr, transcripts, prosecutorial",
    )
    args = parser.parse_args()

    DB_FILTER = {
        "full_text_corpus": ["documents", "pages", "document_classification", "efta_crosswalk"],
        "knowledge_graph": ["entities", "relationships", "edge_sources"],
        "communications": [
            "emails",
            "email_participants",
            "resolved_identities",
            "communication_pairs",
        ],
        "redaction": [
            "redactions",
            "document_summary",
            "reconstructed_pages",
            "extracted_entities",
        ],
        "image_analysis": ["images"],
        "ocr": ["ocr_results"],
        "transcripts": ["transcripts", "transcript_segments"],
        "prosecutorial": [
            "subpoenas",
            "rider_clauses",
            "returns",
            "subpoena_return_links",
            "clause_fulfillment",
            "graph_nodes",
            "graph_edges",
            "investigative_gaps",
        ],
    }

    if args.validate:
        ok = validate()
        sys.exit(0 if ok else 1)

    start = datetime.now()
    print(f"Starting at {start.strftime('%Y-%m-%d %H:%M:%S')}")

    if args.db:
        if args.db not in DB_FILTER:
            print(f"Unknown DB: {args.db}. Options: {', '.join(DB_FILTER.keys())}")
            sys.exit(1)
        # Filter TABLE_MAP to only the requested DB's tables
        filter_tables = DB_FILTER[args.db]
        filtered = [t for t in TABLE_MAP if t[1] in filter_tables]
        original = list(TABLE_MAP)
        TABLE_MAP.clear()
        TABLE_MAP.extend(filtered)

    ok = run_migration(force=args.force)

    if args.db:
        TABLE_MAP.clear()
        TABLE_MAP.extend(original)

    elapsed = datetime.now() - start
    print(f"Finished in {elapsed}")
    print("Run with --validate to verify.")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
