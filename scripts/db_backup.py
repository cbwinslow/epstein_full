#!/usr/bin/env python3
"""
Epstein Project — Database Backup

Creates compressed pg_dump backups with rotation (keeps last N backups).

Usage:
  python db_backup.py                          # Full backup
  python db_backup.py --schema                 # Schema only
  python db_backup.py --tables pages,entities  # Specific tables
  python db_backup.py --rotate 7               # Keep last 7 backups
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from glob import glob

# =============================================================================
# Configuration
# =============================================================================

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = "123qweasd"
PG_DB = "epstein"
BACKUP_DIR = "/mnt/data/epstein-project/backups"
DEFAULT_ROTATE = 5


def backup_full(output_path):
    """Full database backup (schema + data)."""
    cmd = [
        "pg_dump",
        "-h", PG_HOST, "-p", str(PG_PORT),
        "-U", PG_USER, "-d", PG_DB,
        "-Fc",  # Custom format (compressed)
        "-f", output_path,
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = PG_PASS
    subprocess.run(cmd, env=env, check=True)


def backup_schema(output_path):
    """Schema-only backup."""
    cmd = [
        "pg_dump",
        "-h", PG_HOST, "-p", str(PG_PORT),
        "-U", PG_USER, "-d", PG_DB,
        "--schema-only",
        "-f", output_path,
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = PG_PASS
    subprocess.run(cmd, env=env, check=True)


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
    env = os.environ.copy()
    env["PGPASSWORD"] = PG_PASS
    subprocess.run(cmd, env=env, check=True)


def rotate_backups(keep):
    """Remove old backups, keep last N."""
    backups = sorted(glob(os.path.join(BACKUP_DIR, "epstein_*.dump")))
    if len(backups) > keep:
        for old in backups[:-keep]:
            os.remove(old)
            print(f"  Removed: {os.path.basename(old)}")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL backup")
    parser.add_argument("--schema", action="store_true", help="Schema only")
    parser.add_argument("--tables", type=str, help="Comma-separated table names")
    parser.add_argument("--rotate", type=int, default=DEFAULT_ROTATE, help=f"Keep last N backups (default: {DEFAULT_ROTATE})")
    parser.add_argument("--dir", type=str, default=BACKUP_DIR, help="Backup directory")
    args = parser.parse_args()

    os.makedirs(args.dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.schema:
        output = os.path.join(args.dir, f"epstein_schema_{timestamp}.sql")
        print(f"Backing up schema to {output}...")
        backup_schema(output)
    elif args.tables:
        tables = args.tables.split(",")
        output = os.path.join(args.dir, f"epstein_tables_{timestamp}.dump")
        print(f"Backing up {len(tables)} tables to {output}...")
        backup_tables(tables, output)
    else:
        output = os.path.join(args.dir, f"epstein_{timestamp}.dump")
        print(f"Backing up full database to {output}...")
        backup_full(output)

    size = os.path.getsize(output) / (1024 ** 2)
    print(f"  Size: {size:.1f} MB")

    # Rotate
    if args.rotate > 0:
        print(f"\nRotating backups (keeping last {args.rotate})...")
        rotate_backups(args.rotate)

    print("Done.")


if __name__ == "__main__":
    main()
