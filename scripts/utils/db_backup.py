#!/usr/bin/env python3
"""
Epstein Project — Database Backup

Creates compressed pg_dump backups with rotation (keeps last N backups).

Usage:
  python db_backup.py                          # Full backup
  python db_backup.py --schema                 # Schema only
  python db_backup.py --tables pages,entities  # Specific tables
  python db_backup.py --all-tables             # Auto-discover, per-table .dump files
  python db_backup.py --rotate 7               # Keep last 7 backups
"""

import argparse
import os
import subprocess
from datetime import datetime
from glob import glob

# =============================================================================
# Configuration
# =============================================================================

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = os.environ.get("PG_PASSWORD", "")
PG_DB = "epstein"
BACKUP_DIR = "/home/cbwinslow/workspace/epstein-data/backups"
DEFAULT_ROTATE = 5

# Shared env for pg_dump
PG_ENV = {**os.environ, "PGPASSWORD": PG_PASS}


def get_tables():
    """Auto-discover all tables in the database."""
    import psycopg2
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASS,
        dbname=PG_DB
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cur.fetchall()]
    conn.close()
    return tables


def backup_full(output_path):
    """Full database backup (schema + data)."""
    cmd = [
        "pg_dump",
        "-h", PG_HOST, "-p", str(PG_PORT),
        "-U", PG_USER, "-d", PG_DB,
        "-Fc",
        "-f", output_path,
    ]
    subprocess.run(cmd, env=PG_ENV, check=True)


def backup_schema(output_path):
    """Schema-only backup."""
    cmd = [
        "pg_dump",
        "-h", PG_HOST, "-p", str(PG_PORT),
        "-U", PG_USER, "-d", PG_DB,
        "--schema-only",
        "-f", output_path,
    ]
    subprocess.run(cmd, env=PG_ENV, check=True)


def backup_tables(tables, output_path):
    """Backup specific tables."""
    cmd = [
        "pg_dump",
        "-h", PG_HOST, "-p", str(PG_PORT),
        "-U", PG_USER, "-d", PG_DB,
        "-Fc",
        "-f", output_path,
    ]
    for table in tables:
        cmd.extend(["-t", table])
    subprocess.run(cmd, env=PG_ENV, check=True)


def backup_all_tables(output_dir, timestamp):
    """Auto-discover and backup each table as its own .dump file."""
    tables = get_tables()
    table_dir = os.path.join(output_dir, f"tables_{timestamp}")
    os.makedirs(table_dir, exist_ok=True)

    total_size = 0
    print(f"\nBacking up {len(tables)} tables to {table_dir}/\n")

    for table in tables:
        output = os.path.join(table_dir, f"{table}.dump")
        cmd = [
            "pg_dump",
            "-h", PG_HOST, "-p", str(PG_PORT),
            "-U", PG_USER, "-d", PG_DB,
            "-Fc",
            "-t", table,
            "-f", output,
        ]
        try:
            subprocess.run(cmd, env=PG_ENV, check=True, capture_output=True)
            size = os.path.getsize(output)
            total_size += size
            size_mb = size / (1024 ** 2)
            print(f"  ✓ {table:<30} {size_mb:>8.1f} MB")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ {table}: {e.stderr.decode()[:80]}")

    total_mb = total_size / (1024 ** 2)
    print(f"\n  Total: {len(tables)} tables, {total_mb:.1f} MB")
    return table_dir


def rotate_backups(keep, backup_dir):
    """Remove old backups, keep last N."""
    full_backups = sorted(glob(os.path.join(backup_dir, "epstein_*.dump")))
    if len(full_backups) > keep:
        for old in full_backups[:-keep]:
            os.remove(old)
            print(f"  Removed: {os.path.basename(old)}")

    table_dirs = sorted(glob(os.path.join(backup_dir, "tables_*")))
    if len(table_dirs) > keep:
        for old in table_dirs[:-keep]:
            import shutil
            shutil.rmtree(old)
            print(f"  Removed: {os.path.basename(old)}/")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL backup")
    parser.add_argument("--schema", action="store_true", help="Schema only")
    parser.add_argument("--tables", type=str, help="Comma-separated table names")
    parser.add_argument("--all-tables", action="store_true", help="Auto-discover, per-table .dump files")
    parser.add_argument("--rotate", type=int, default=DEFAULT_ROTATE, help=f"Keep last N backups (default: {DEFAULT_ROTATE})")
    parser.add_argument("--dir", type=str, default=BACKUP_DIR, help="Backup directory")
    args = parser.parse_args()

    os.makedirs(args.dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 60)
    print("  EPSTEIN DATABASE BACKUP")
    print("=" * 60)

    if args.all_tables:
        backup_all_tables(args.dir, timestamp)
    elif args.schema:
        output = os.path.join(args.dir, f"epstein_schema_{timestamp}.sql")
        print(f"\nBacking up schema to {output}...")
        backup_schema(output)
        size = os.path.getsize(output) / (1024 ** 2)
        print(f"  Size: {size:.1f} MB")
    elif args.tables:
        tables = args.tables.split(",")
        output = os.path.join(args.dir, f"epstein_tables_{timestamp}.dump")
        print(f"\nBacking up {len(tables)} tables to {output}...")
        backup_tables(tables, output)
        size = os.path.getsize(output) / (1024 ** 2)
        print(f"  Size: {size:.1f} MB")
    else:
        output = os.path.join(args.dir, f"epstein_{timestamp}.dump")
        print(f"\nBacking up full database to {output}...")
        backup_full(output)
        size = os.path.getsize(output) / (1024 ** 2)
        print(f"  Size: {size:.1f} MB")

    # Rotate
    if args.rotate > 0:
        print(f"\nRotating backups (keeping last {args.rotate})...")
        rotate_backups(args.rotate, args.dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
