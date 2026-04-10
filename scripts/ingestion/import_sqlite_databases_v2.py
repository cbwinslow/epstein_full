#!/usr/bin/env python3
"""
SQLite database importer - creates tables dynamically and imports with proper transaction handling
"""

import logging
import os
import sqlite3
from datetime import datetime

import psycopg2

DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "cbwinslow",
    "password": "123qweasd",
    "dbname": "epstein",
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/sqlite_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)


def sqlite_type_to_pg(sqlite_type):
    """Convert SQLite types to PostgreSQL types."""
    type_upper = sqlite_type.upper() if sqlite_type else 'TEXT'
    if 'INT' in type_upper:
        return 'INTEGER'
    elif 'REAL' in type_upper or 'FLOA' in type_upper or 'DOUB' in type_upper:
        return 'REAL'
    elif 'BLOB' in type_upper:
        return 'BYTEA'
    elif 'BOOL' in type_upper:
        return 'BOOLEAN'
    else:
        return 'TEXT'


def create_pg_table(pg_conn, table_name, columns):
    """Create PostgreSQL table from SQLite schema."""
    # Skip FTS tables
    if '_fts' in table_name:
        return False
    
    col_defs = []
    for col in columns:
        col_name = col[1]
        col_type = sqlite_type_to_pg(col[2])
        not_null = 'NOT NULL' if col[3] else ''
        default = f"DEFAULT {col[4]}" if col[4] else ''
        col_defs.append(f'"{col_name}" {col_type} {not_null} {default}'.strip())
    
    create_sql = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            {', '.join(col_defs)}
        )
    """
    
    try:
        with pg_conn.cursor() as cur:
            cur.execute(create_sql)
            pg_conn.commit()
        return True
    except Exception as e:
        logging.warning(f"Could not create table {table_name}: {e}")
        return False


def import_table(sqlite_path, table_name, pg_conn, batch_size=1000):
    """Import a single table with per-batch transactions."""
    # Skip FTS tables
    if '_fts' in table_name:
        logging.info(f"  Skipping FTS table: {table_name}")
        return 0
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # Get schema
        sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = sqlite_cursor.fetchall()
        
        if not columns_info:
            return 0
        
        # Create table in PG
        pg_table = table_name
        if not create_pg_table(pg_conn, pg_table, columns_info):
            return 0
        
        # Get row count
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = sqlite_cursor.fetchone()[0]
        
        if total_rows == 0:
            logging.info(f"  {table_name}: empty")
            return 0
        
        logging.info(f"  {table_name}: {total_rows} rows")
        
        # Get column names
        columns = [col[1] for col in columns_info]
        
        # Import in batches with per-batch transactions
        imported = 0
        offset = 0
        errors_in_batch = 0
        
        while offset < total_rows:
            sqlite_cursor.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                break
            
            batch_imported = 0
            with pg_conn.cursor() as pg_cur:
                for row in rows:
                    try:
                        values = [row[col] for col in columns]
                        placeholders = ','.join(['%s'] * len(columns))
                        
                        pg_cur.execute(f"""
                            INSERT INTO "{pg_table}" ({','.join(f'"{c}"' for c in columns)})
                            VALUES ({placeholders})
                            ON CONFLICT DO NOTHING
                        """, values)
                        batch_imported += 1
                    except Exception:
                        errors_in_batch += 1
                        continue
                
                pg_conn.commit()
            
            imported += batch_imported
            offset += batch_size
            
            if (offset // batch_size) % 10 == 0:
                logging.info(f"    Progress: {imported}/{total_rows} rows")
        
        sqlite_conn.close()
        
        if errors_in_batch > 0:
            logging.warning(f"  {table_name}: {errors_in_batch} rows failed")
        
        logging.info(f"  ✓ Imported {imported} rows")
        return imported
        
    except Exception as e:
        logging.error(f"  Error importing {table_name}: {e}")
        return 0


def import_sqlite_to_postgres(sqlite_path, pg_conn):
    """Import all tables from a SQLite database."""
    db_name = os.path.basename(sqlite_path)
    logging.info(f"\nProcessing: {db_name}")
    
    if not os.path.exists(sqlite_path):
        logging.warning(f"Not found: {sqlite_path}")
        return 0
    
    # Connect to SQLite and get tables
    sqlite_conn = sqlite3.connect(sqlite_path)
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    sqlite_conn.close()
    
    logging.info(f"  Tables: {len(tables)} ({', '.join(tables[:5])}{'...' if len(tables) > 5 else ''})")
    
    total_imported = 0
    for table in tables:
        count = import_table(sqlite_path, table, pg_conn)
        total_imported += count
    
    return total_imported


def main():
    logging.info("=" * 60)
    logging.info("SQLITE DATABASE IMPORTER v2")
    logging.info("=" * 60)
    
    databases_dir = f"{DATA_ROOT}/databases"
    
    if not os.path.exists(databases_dir):
        logging.error(f"Directory not found: {databases_dir}")
        return 1
    
    pg_conn = psycopg2.connect(**PG_CONFIG)
    pg_conn.autocommit = False
    
    # Find all .db files
    db_files = [os.path.join(databases_dir, f) for f in os.listdir(databases_dir) if f.endswith('.db')]
    db_files.sort()
    
    logging.info(f"Found {len(db_files)} databases")
    
    total_rows = 0
    for db_path in db_files:
        count = import_sqlite_to_postgres(db_path, pg_conn)
        total_rows += count
    
    pg_conn.close()
    
    logging.info("\n" + "=" * 60)
    logging.info(f"COMPLETE: {len(db_files)} databases, {total_rows} rows")
    logging.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
