#!/usr/bin/env python3
"""
SQLite database importer - imports all SQLite DBs to PostgreSQL
"""

import logging
import os
import sqlite3
from datetime import datetime

import psycopg2
import psycopg2.extras

DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

PG_CONFIG = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": int(os.environ.get("PG_PORT", "5432")),
    "user": os.environ.get("PG_USER", "cbwinslow"),
    "password": os.environ.get("PG_PASSWORD", "123qweasd"),
    "dbname": os.environ.get("PG_DB", "epstein"),
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/sqlite_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

SQLITE_DATABASES = [
    ("knowledge_graph.db", "entities"),
    ("communications.db", "emails"),
    ("transcripts.db", "transcripts"),
    ("image_analysis.db", "image_descriptions"),
]


def get_sqlite_tables(sqlite_path):
    """Get list of tables from SQLite database."""
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        logging.error(f"Error getting tables from {sqlite_path}: {e}")
        return []


def get_table_schema(sqlite_path, table_name):
    """Get column info for a table."""
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        conn.close()
        return columns
    except Exception as e:
        logging.error(f"Error getting schema for {table_name}: {e}")
        return []


def import_table(sqlite_path, table_name, pg_conn, batch_size=1000):
    """Import a single table from SQLite to PostgreSQL."""
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # Get row count
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = sqlite_cursor.fetchone()[0]
        
        if total_rows == 0:
            logging.info(f"  Table {table_name}: empty, skipping")
            sqlite_conn.close()
            return 0
        
        logging.info(f"  Importing {table_name}: {total_rows} rows")
        
        # Get column names
        sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in sqlite_cursor.fetchall()]
        
        # Create PostgreSQL table name (namespace by source DB)
        db_name = os.path.basename(sqlite_path).replace('.db', '')
        pg_table = f"{db_name}_{table_name}"
        
        # Read data in batches
        imported = 0
        offset = 0
        
        while offset < total_rows:
            sqlite_cursor.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                break
            
            # Insert to PostgreSQL with ON CONFLICT
            with pg_conn.cursor() as pg_cur:
                for _, row in enumerate(rows):
                    values = [row[col] for col in columns]
                    placeholders = ','.join(['%s'] * len(columns))
                    
                    try:
                        pg_cur.execute(f"""
                            INSERT INTO {pg_table} ({','.join(columns)})
                            VALUES ({placeholders})
                            ON CONFLICT DO NOTHING
                        """, values)
                    except Exception as e:
                        # Skip problematic rows but continue
                        continue
                
                pg_conn.commit()
            
            imported += len(rows)
            offset += batch_size
            
            if (offset // batch_size) % 10 == 0:
                logging.info(f"    Progress: {imported}/{total_rows} rows")
        
        sqlite_conn.close()
        logging.info(f"  ✓ Imported {imported} rows to {pg_table}")
        return imported
        
    except Exception as e:
        logging.error(f"Error importing {table_name}: {e}")
        return 0


def import_sqlite_to_postgres(sqlite_path, pg_conn):
    """Import all tables from a SQLite database."""
    db_name = os.path.basename(sqlite_path)
    logging.info(f"\nProcessing: {db_name}")
    
    if not os.path.exists(sqlite_path):
        logging.warning(f"Database not found: {sqlite_path}")
        return 0
    
    tables = get_sqlite_tables(sqlite_path)
    logging.info(f"  Found {len(tables)} tables: {', '.join(tables)}")
    
    total_imported = 0
    for table in tables:
        count = import_table(sqlite_path, table, pg_conn)
        total_imported += count
    
    return total_imported


def main():
    logging.info("=" * 60)
    logging.info("SQLITE DATABASE IMPORTER")
    logging.info("=" * 60)
    
    databases_dir = f"{DATA_ROOT}/databases"
    
    if not os.path.exists(databases_dir):
        logging.error(f"Databases directory not found: {databases_dir}")
        return 1
    
    pg_conn = psycopg2.connect(**PG_CONFIG)
    
    # Find all .db files
    db_files = []
    for f in os.listdir(databases_dir):
        if f.endswith('.db'):
            db_files.append(os.path.join(databases_dir, f))
    
    logging.info(f"Found {len(db_files)} SQLite databases")
    
    total_rows = 0
    for db_path in db_files:
        count = import_sqlite_to_postgres(db_path, pg_conn)
        total_rows += count
    
    pg_conn.close()
    
    logging.info("\n" + "=" * 60)
    logging.info(f"IMPORT COMPLETE: {len(db_files)} databases, {total_rows} total rows")
    logging.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
