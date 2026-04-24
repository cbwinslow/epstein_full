#!/usr/bin/env python3
"""
Import White House Visitor Logs to PostgreSQL
Source: 2021-2024 WAVES access records
Table: whitehouse_visitors

Fast batch import using COPY
"""
import csv
import logging
import sys
import psycopg2
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/whitehouse")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_whitehouse_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        database='epstein',
        user='cbwinslow',
        password='123qweasd'
    )


def create_table():
    """Create whitehouse_visitors table"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS whitehouse_visitors (
            id SERIAL PRIMARY KEY,
            visitor_lastname TEXT,
            visitor_firstname TEXT,
            visitor_mid TEXT,
            uin TEXT,
            badge_number TEXT,
            access_type TEXT,
            time_of_arrival TIME,
            time_of_departure TIME,
            visitor_post TEXT,
            appointee_lastname TEXT,
            appointee_firstname TEXT,
            meeting_location TEXT,
            meeting_room TEXT,
            caller_lastname TEXT,
            caller_firstname TEXT,
            caller_room TEXT,
            appointment_made_date TIMESTAMPTZ,
            appointment_start TIMESTAMPTZ,
            appointment_end TIMESTAMPTZ,
            appointment_cancelled TIMESTAMPTZ,
            total_people INTEGER,
            release_date TIMESTAMPTZ,
            administration TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_wh_visitor_name ON whitehouse_visitors (visitor_lastname, visitor_firstname);
        CREATE INDEX IF NOT EXISTS idx_wh_appointee ON whitehouse_visitors (appointee_lastname, appointee_firstname);
        CREATE INDEX IF NOT EXISTS idx_wh_meeting_date ON whitehouse_visitors (appointment_start);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("✅ Table created")


def parse_date(date_str: str):
    """Parse date string to PostgreSQL TIMESTAMPTZ"""
    if not date_str:
        return None
    date_str = date_str.strip()
    for fmt in ['%m/%d/%Y %H:%M', '%m/%d/%Y']:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt
        except ValueError:
            continue
    return None


def import_csv_fast(csv_path: Path, administration: str) -> int:
    """Import CSV using COPY command"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    records = []
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Clean BOM from keys
            clean = {k.replace('\ufeff', ''): v for k, v in row.items()}
            
            record = (
                clean.get('NAMELAST', '').strip() or None,
                clean.get('NAMEFIRST', '').strip() or None,
                clean.get('NAMEMID', '').strip() or None,
                clean.get('UIN', '').strip() or None,
                clean.get('BDGNBR', '').strip() or None,
                clean.get('ACCESS_TYPE', '').strip() or None,
                clean.get('TOA', '').strip() or None,
                clean.get('TOD', '').strip() or None,
                clean.get('POA', '').strip() or None,
                clean.get('VISITEE_NAMELAST', '').strip() or None,
                clean.get('VISITEE_NAMEFIRST', '').strip() or None,
                clean.get('MEETING_LOC', '').strip() or None,
                clean.get('MEETING_ROOM', '').strip() or None,
                clean.get('CALLER_NAME_LAST', '').strip() or None,
                clean.get('CALLER_NAME_FIRST', '').strip() or None,
                clean.get('CALLER_ROOM', '').strip() or None,
                parse_date(clean.get('APPT_MADE_DATE', '')),
                parse_date(clean.get('APPT_START_DATE', '')),
                parse_date(clean.get('APPT_END_DATE', '')),
                parse_date(clean.get('APPT_CANCEL_DATE', '')),
                int(clean['TOTAL_PEOPLE']) if clean.get('TOTAL_PEOPLE', '').isdigit() else 1,
                parse_date(clean.get('RELEASEDATE', '')),
                administration,
                str(clean)  # raw_data as string for now
            )
            records.append(record)
    
    # Use execute_values for batch insert
    if records:
        from psycopg2 import extras
        try:
            cur.extras.execute_values("""
                INSERT INTO whitehouse_visitors (
                    visitor_lastname, visitor_firstname, visitor_mid, uin, badge_number,
                    access_type, time_of_arrival, time_of_departure, visitor_post,
                    appointee_lastname, appointee_firstname, meeting_location, meeting_room,
                    caller_lastname, caller_firstname, caller_room,
                    appointment_made_date, appointment_start, appointment_end,
                    appointment_cancelled, total_people, release_date,
                    administration, raw_data
                ) VALUES %s
            """, records, template=None, page_size=1000)
            conn.commit()
        except Exception as e:
            logger.error(f"Batch insert error: {e}")
            conn.rollback()
            # Fall back to individual inserts
            for record in records:
                try:
                    cur.execute("""
                        INSERT INTO whitehouse_visitors (
                            visitor_lastname, visitor_firstname, visitor_mid, uin, badge_number,
                            access_type, time_of_arrival, time_of_departure, visitor_post,
                            appointee_lastname, appointee_firstname, meeting_location, meeting_room,
                            caller_lastname, caller_firstname, caller_room,
                            appointment_made_date, appointment_start, appointment_end,
                            appointment_cancelled, total_people, release_date,
                            administration, raw_data
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """, record)
                except Exception:
                    pass
            conn.commit()
    
    cur.close()
    conn.close()
    return len(records)


def main():
    logger.info("=" * 80)
    logger.info("WHITE HOUSE VISITOR LOGS IMPORT")
    logger.info("=" * 80)
    
    create_table()
    
    csv_files = sorted(BASE_DIR.rglob("*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files")
    
    total = 0
    for csv_path in csv_files:
        logger.info(f"Importing: {csv_path.name}...")
        count = import_csv_fast(csv_path, "Biden")
        total += count
        logger.info(f"✅ {csv_path.name}: {count:,} records")
    
    logger.info("=" * 80)
    logger.info(f"TOTAL IMPORTED: {total:,} visitor records")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()