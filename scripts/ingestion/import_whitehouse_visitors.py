#!/usr/bin/env python3
"""
Import White House Visitor Logs to PostgreSQL
Source: WAVES access records (2009-2025)
Table: whitehouse_visitors
"""

import os
import sys
import csv
import json
import logging
import psycopg2
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Configuration
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/whitehouse")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")
BATCH_SIZE = 10000

# Logging
log_file = LOG_DIR / f"import_whitehouse_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(
        host='localhost',
        database='epstein',
        user='cbwinslow',
        password='123qweasd'
    )


def create_table():
    """Create whitehouse_visitors table if not exists"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS whitehouse_visitors (
            id SERIAL PRIMARY KEY,
            visitor_name TEXT,
            visitor_lastname TEXT,
            visitor_firstname TEXT,
            visitee_name TEXT,
            visitee_lastname TEXT,
            visitee_firstname TEXT,
            description TEXT,
            meeting_date DATE,
            meeting_time TIME,
            location TEXT,
            total_people INT,
            post_date DATE,
            release_date DATE,
            administration TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_wh_visitors_name ON whitehouse_visitors (visitor_lastname);
        CREATE INDEX IF NOT EXISTS idx_wh_visitors_visitee ON whitehouse_visitors (visitee_lastname);
        CREATE INDEX IF NOT EXISTS idx_wh_visitors_date ON whitehouse_visitors (meeting_date);
        CREATE INDEX IF NOT EXISTS idx_wh_visitors_admin ON whitehouse_visitors (administration);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Table and indexes created/verified")


def parse_csv_file(filepath: Path, administration: str) -> List[Dict]:
    """Parse White House CSV file"""
    records = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse name fields (varies by administration format)
                visitor_name = row.get('NAMELAST', row.get('visitee_last_name', '')) + ', ' + \
                              row.get('NAMEFIRST', row.get('visitee_first_name', ''))
                
                visitee_name = row.get('VISITEE_NAMELAST', row.get('meeting_location', '')) + ', ' + \
                              row.get('VISITEE_NAMEFIRST', '')
                
                record = {
                    'visitor_name': visitor_name.strip(', '),
                    'visitor_lastname': row.get('NAMELAST', row.get('visitee_last_name', '')),
                    'visitor_firstname': row.get('NAMEFIRST', row.get('visitee_first_name', '')),
                    'visitee_name': visitee_name.strip(', '),
                    'visitee_lastname': row.get('VISITEE_NAMELAST', ''),
                    'visitee_firstname': row.get('VISITEE_NAMEFIRST', ''),
                    'description': row.get('DESCRIPTION', row.get('meeting_description', '')),
                    'meeting_date': row.get('APPT_START_DATE', row.get('meeting_date', '')),
                    'meeting_time': row.get('APPT_START_TIME', row.get('meeting_time', '')),
                    'location': row.get('MEETING_LOCATION', row.get('meeting_location', 'White House')),
                    'total_people': row.get('TOTAL_PEOPLE', '1'),
                    'post_date': row.get('POST_DATE', ''),
                    'release_date': row.get('RELEASE_DATE', ''),
                    'administration': administration,
                    'raw_data': json.dumps(row),
                    'source_file': str(filepath.name)
                }
                records.append(record)
                
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def import_records(records: List[Dict]) -> int:
    """Import records to PostgreSQL"""
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    try:
        # Use COPY for bulk insert
        from io import StringIO
        
        buffer = StringIO()
        for r in records:
            buffer.write('\t'.join([
                r['visitor_name'] or '',
                r['visitor_lastname'] or '',
                r['visitor_firstname'] or '',
                r['visitee_name'] or '',
                r['visitee_lastname'] or '',
                r['visitee_firstname'] or '',
                r['description'] or '',
                r['meeting_date'] or '',
                r['meeting_time'] or '',
                r['location'] or 'White House',
                str(r['total_people']) if r['total_people'] else '1',
                r['post_date'] or '',
                r['release_date'] or '',
                r['administration'],
                r['raw_data'],
                r['source_file']
            ]) + '\n')
        
        buffer.seek(0)
        cur.copy_from(
            buffer,
            'whitehouse_visitors',
            columns=[
                'visitor_name', 'visitor_lastname', 'visitor_firstname',
                'visitee_name', 'visitee_lastname', 'visitee_firstname',
                'description', 'meeting_date', 'meeting_time', 'location',
                'total_people', 'post_date', 'release_date', 'administration',
                'raw_data', 'source_file'
            ],
            null=''
        )
        
        conn.commit()
        inserted = len(records)
        
    except Exception as e:
        logger.error(f"Import error: {e}")
        conn.rollback()
        
        # Fall back to individual inserts
        for r in records:
            try:
                cur.execute("""
                    INSERT INTO whitehouse_visitors (
                        visitor_name, visitor_lastname, visitor_firstname,
                        visitee_name, visitee_lastname, visitee_firstname,
                        description, meeting_date, meeting_time, location,
                        total_people, post_date, release_date, administration,
                        raw_data, source_file
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    r['visitor_name'], r['visitor_lastname'], r['visitor_firstname'],
                    r['visitee_name'], r['visitee_lastname'], r['visitee_firstname'],
                    r['description'], r['meeting_date'], r['meeting_time'], r['location'],
                    r['total_people'], r['post_date'], r['release_date'], r['administration'],
                    r['raw_data'], r['source_file']
                ))
                inserted += 1
            except Exception as e2:
                logger.debug(f"Insert failed: {e2}")
        
        conn.commit()
    
    finally:
        cur.close()
        conn.close()
    
    return inserted


def update_inventory(count: int):
    """Update data_inventory table"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE data_inventory 
        SET status = 'imported',
            actual_records = %s,
            last_updated = NOW()
        WHERE source_name = 'White House Visitor Logs'
    """, (count,))
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Inventory updated: {count} records")


def main():
    """Main import process"""
    logger.info("=" * 80)
    logger.info("WHITE HOUSE VISITOR LOGS IMPORT")
    logger.info("=" * 80)
    
    # Create table
    create_table()
    
    # Find all CSV files
    csv_files = list(BASE_DIR.glob("*.csv"))
    if not csv_files:
        logger.warning("No CSV files found in " + str(BASE_DIR))
        return
    
    logger.info(f"Found {len(csv_files)} CSV files")
    
    total_imported = 0
    total_files = 0
    
    for csv_file in csv_files:
        # Determine administration from filename
        if '2009' in csv_file.name or '2017' in csv_file.name:
            admin = 'Obama'
        elif '2017' in csv_file.name and '2021' not in csv_file.name:
            admin = 'Trump'
        elif '2021' in csv_file.name or '2024' in csv_file.name:
            admin = 'Biden'
        else:
            admin = 'Unknown'
        
        logger.info(f"Processing {csv_file.name} ({admin})...")
        
        records = parse_csv_file(csv_file, admin)
        
        if records:
            # Batch import
            for i in range(0, len(records), BATCH_SIZE):
                batch = records[i:i + BATCH_SIZE]
                imported = import_records(batch)
                total_imported += imported
                logger.info(f"  Imported {imported}/{len(batch)} records (batch {i//BATCH_SIZE + 1})")
            
            total_files += 1
        else:
            logger.warning(f"  No records parsed from {csv_file.name}")
    
    # Update inventory
    update_inventory(total_imported)
    
    logger.info("=" * 80)
    logger.info("IMPORT COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Files processed: {total_files}")
    logger.info(f"Total records imported: {total_imported}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
