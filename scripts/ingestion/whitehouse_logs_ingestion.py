#!/usr/bin/env python3
"""
White House Visitor Logs Ingestion - Years 2000-2008

This script ingests White House visitor logs from the WAVES system
(White House Visitor Access and Entry System) for 2000-2008.

Usage:
    python3 whitehouse_logs_ingestion.py [--start-year YYYY] [--end-year YYYY]
"""

import argparse
import csv
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_batch

from config import get_db_connection, setup_file_logger, RAW_FILES_DIR

# Configuration
WH_DIR = RAW_FILES_DIR / "whitehouse"
LOG_DIR = RAW_FILES_DIR / "logs" / "whitehouse"
LOG_DIR.mkdir(parents=True, exist_ok=True)
WH_DIR.mkdir(parents=True, exist_ok=True)

BATCH_SIZE = 5000


def setup_logging():
    """Setup logging for White House ingestion."""
    logger, log_file = setup_file_logger("whitehouse_logs_ingestion")
    return logger, log_file


def create_tables(conn):
    """Create whitehouse_visitors table if it doesn't exist."""
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
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_wh_visitor_name ON whitehouse_visitors(visitor_lastname, visitor_firstname);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_wh_visit_date ON whitehouse_visitors(appointment_start);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_wh_uin ON whitehouse_visitors(uin);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_wh_meeting_with ON whitehouse_visitors(appointee_lastname, appointee_firstname);")
    conn.commit()
    cur.close()


def get_existing_records(conn):
    """Get count of existing records to track duplicates."""
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM whitehouse_visitors")
    count = cur.fetchone()[0]
    cur.close()
    return count


def find_csv_files(start_year: int, end_year: int) -> list:
    """Find CSV files for the given year range."""
    csv_files = []

    # Check for pre-downloaded CSV files
    for year in range(start_year, end_year + 1):
        year_patterns = [
            WH_DIR / f"visitors_{year}.csv",
            WH_DIR / f"whitehouse_visitors_{year}.csv",
            WH_DIR / f"{year}" / "visitors.csv",
        ]
        for pattern in year_patterns:
            if pattern.exists():
                csv_files.append((year, pattern))
                break

    return csv_files


def normalize_value(value):
    """Normalize CSV field value - handle empty strings and whitespace."""
    if value is None:
        return None
    v = value.strip()
    return v if v else None


def ingest_csv_file(conn, filepath: Path, year: int, logger) -> int:
    """Ingest a single CSV file of White House visitor records."""
    records_inserted = 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            # Try to detect delimiter
            sample = f.read(4096)
            f.seek(0)

            # Check if it's pipe-delimited or comma-delimited
            if sample.count('|') > sample.count(','):
                delimiter = '|'
            else:
                delimiter = ','

            reader = csv.DictReader(f, delimiter=delimiter)

            # Normalize column names
            field_map = {}
            if reader.fieldnames:
                for col in reader.fieldnames:
                    col_lower = col.strip().lower().replace(' ', '_').replace('-', '_')
                    field_map[col] = col_lower

            batch = []

            for row_num, row in enumerate(reader, 1):
                try:
                    # Map fields flexibly based on column names
                     visitor_lastname = None
                    visitor_firstname = None
                    visitor_mid = None
                    uin = None
                    badge_number = None
                    access_type = None
                    time_of_arrival = None
                    time_of_departure = None
                    visitor_post = None
                    appointee_lastname = None
                    appointee_firstname = None
                    meeting_location = None
                    meeting_room = None
                    caller_lastname = None
                    caller_firstname = None
                    caller_room = None
                    appointment_made_date = None
                    appointment_start = None
                    appointment_end = None
                    appointment_cancelled = None
                    total_people = None
                    release_date = None
                    administration = None
                    raw_data = None

                    for orig_col, norm_col in field_map.items():
                        val = normalize_value(row[orig_col])
                        if not val:
                            continue

                         if 'last' in norm_col and 'name' in norm_col:
                             visitor_lastname = val
                        elif 'first' in norm_col and 'name' in norm_col:
                            visitor_firstname = val
                        elif 'mid' in norm_col and 'name' in norm_col:
                            visitor_mid = val
                        elif 'uin' in norm_col:
                            uin = val
                        elif 'badge' in norm_col:
                            badge_number = val
                        elif 'access' in norm_col and 'type' in norm_col:
                            access_type = val
                        elif 'arrival' in norm_col or ('time' in norm_col and 'arrival' in norm_col):
                            time_of_arrival = val
                        elif 'departure' in norm_col or ('time' in norm_col and 'departure' in norm_col):
                            time_of_departure = val
                        elif 'visitor' in norm_col and 'post' in norm_col:
                            visitor_post = val
                        elif 'appointee' in norm_col:
                            if 'last' in norm_col and 'name' in norm_col:
                                appointee_lastname = val
                            elif 'first' in norm_col and 'name' in norm_col:
                                appointee_firstname = val
                        elif 'meeting' in norm_col:
                            if 'location' in norm_col:
                                meeting_location = val
                            elif 'room' in norm_col:
                                meeting_room = val
                            else:
                                meeting_location = val  # fallback
                        elif 'caller' in norm_col:
                            if 'last' in norm_col and 'name' in norm_col:
                                caller_lastname = val
                            elif 'first' in norm_col and 'name' in norm_col:
                                caller_firstname = val
                            elif 'room' in norm_col:
                                caller_room = val
                        elif 'appointment' in norm_col:
                            if 'made' in norm_col and 'date' in norm_col:
                                try:
                                    appointment_made_date = datetime.strptime(val[:19], '%Y-%m-%d %H:%M:%S')
                                except:
                                    try:
                                        appointment_made_date = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S')
                                    except:
                                        pass
                            elif 'start' in norm_col:
                                try:
                                    appointment_start = datetime.strptime(val[:19], '%Y-%m-%d %H:%M:%S')
                                except:
                                    try:
                                        appointment_start = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S')
                                    except:
                                        pass
                            elif 'end' in norm_col:
                                try:
                                    appointment_end = datetime.strptime(val[:19], '%Y-%m-%d %H:%M:%S')
                                except:
                                    try:
                                        appointment_end = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S')
                                    except:
                                        pass
                            elif 'cancelled' in norm_col:
                                try:
                                    appointment_cancelled = datetime.strptime(val[:19], '%Y-%m-%d %H:%M:%S')
                                except:
                                    try:
                                        appointment_cancelled = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S')
                                    except:
                                        pass
                        elif 'total' in norm_col and 'people' in norm_col:
                            try:
                                total_people = int(val)
                            except:
                                pass
                        elif 'release' in norm_col and 'date' in norm_col:
                            try:
                                release_date = datetime.strptime(val[:19], '%Y-%m-%d %H:%M:%S')
                            except:
                                try:
                                    release_date = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S')
                                except:
                                    pass
                        elif 'administration' in norm_col:
                            administration = val
                        elif 'visiting' in norm_col:
                            visitor_post = val  # fallback
                        elif 'purpose' in norm_col:
                            meeting_location = val  # fallback
                        elif 'meeting' in norm_col and 'with' in norm_col:
                            appointee_lastname = val  # fallback
                        elif 'special' in norm_col or 'note' in norm_col:
                            pass  # no matching column in new schema
                        elif 'affiliat' in norm_col or 'organization' in norm_col:
                            pass  # no matching column in new schema
                        elif 'visitor' in norm_col and 'type' in norm_col:
                            pass  # no matching column in new schema
                        elif 'visit' in norm_col and 'date' in norm_col:
                            try:
                                appointment_start = datetime.strptime(val[:10], '%Y-%m-%d')
                            except:
                                try:
                                    appointment_start = datetime.strptime(val, '%m/%d/%Y')
                                except:
                                    pass
                        elif 'entry' in norm_col and 'time' in norm_col:
                            time_of_arrival = val
                        elif 'exit' in norm_col and 'time' in norm_col:
                            time_of_departure = val
                        elif 'name' in norm_col and 'visitor' not in norm_col and 'last' not in norm_col and 'first' not in norm_col:
                            # Could be a combined name field
                            if ',' in val:
                                parts = [p.strip() for p in val.split(',', 1)]
                                visitor_lastname = parts[0]
                                if len(parts) > 1:
                                    visitor_firstname = parts[1]
                            else:
                                visitor_lastname = val

                    # If no date found, use the year from filename
                    if not visit_date:
                        try:
                            visit_date = datetime(year, 1, 1).date()
                        except:
                            pass

                     batch.append((
                        visitor_lastname,
                        visitor_firstname,
                        visitor_mid,
                        uin,
                        badge_number,
                        access_type,
                        time_of_arrival,
                        time_of_departure,
                        visitor_post,
                        appointee_lastname,
                        appointee_firstname,
                        meeting_location,
                        meeting_room,
                        caller_lastname,
                        caller_firstname,
                        caller_room,
                        appointment_made_date,
                        appointment_start,
                        appointment_end,
                        appointment_cancelled,
                        total_people,
                        release_date,
                        administration,
                        raw_data
                    ))

                    if len(batch) >= BATCH_SIZE:
                        cur = conn.cursor()
                         execute_batch(cur, """
                             INSERT INTO whitehouse_visitors (
                                 visitor_lastname, visitor_firstname, visitor_mid,
                                 uin, badge_number, access_type,
                                 time_of_arrival, time_of_departure,
                                 visitor_post,
                                 appointee_lastname, appointee_firstname,
                                 meeting_location, meeting_room,
                                 caller_lastname, caller_firstname, caller_room,
                                 appointment_made_date,
                                 appointment_start, appointment_end, appointment_cancelled,
                                 total_people, release_date, administration, raw_data
                             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                         """, batch, page_size=100)
                        conn.commit()
                        cur.close()
                        records_inserted += len(batch)
                        logger.info(f"    Inserted batch of {len(batch)} records (total: {records_inserted})")
                        batch = []

                except Exception as e:
                    logger.warning(f"    Warning processing row {row_num}: {e}")
                    continue

            # Insert remaining records
            if batch:
                cur = conn.cursor()
                 execute_batch(cur, """
                     INSERT INTO whitehouse_visitors (
                         visitor_lastname, visitor_firstname, visitor_mid,
                         uin, badge_number, access_type,
                         time_of_arrival, time_of_departure,
                         visitor_post,
                         appointee_lastname, appointee_firstname,
                         meeting_location, meeting_room,
                         caller_lastname, caller_firstname, caller_room,
                         appointment_made_date,
                         appointment_start, appointment_end, appointment_cancelled,
                         total_people, release_date, administration, raw_data
                     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """, batch, page_size=100)
                conn.commit()
                cur.close()
                records_inserted += len(batch)
                logger.info(f"    Inserted final batch of {len(batch)} records")

        logger.info(f"  Completed {filepath.name}: {records_inserted} records inserted")

    except Exception as e:
        logger.error(f"  Error processing {filepath.name}: {e}")

    return records_inserted


def main():
    parser = argparse.ArgumentParser(
        description="Ingest White House visitor logs into PostgreSQL"
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=2000,
        help="Start year (default: 2000)"
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=2008,
        help="End year (default: 2008)"
    )
    args = parser.parse_args()

    start_year = args.start_year
    end_year = args.end_year

    logger, log_file = setup_logging()

    logger.info("=" * 80)
    logger.info("WHITE HOUSE VISITOR LOGS INGESTION")
    logger.info("=" * 80)
    logger.info(f"Start Time: {datetime.now().isoformat()}")
    logger.info(f"Year Range: {start_year} - {end_year}")
    logger.info(f"Log File: {log_file}")
    logger.info("=" * 80)

    conn = None
    try:
        conn = get_db_connection()
        logger.info("✅ Connected to database")

        create_tables(conn)
        logger.info("✅ Tables created/verified")

        existing_count = get_existing_records(conn)
        logger.info(f"Existing records in table: {existing_count:,}")

        csv_files = find_csv_files(start_year, end_year)

        if not csv_files:
            logger.warning(f"\n⚠️  No CSV files found in {WH_DIR}")
            logger.warning("   Expected files: visitors_YYYY.csv or whitehouse_visitors_YYYY.csv")
            logger.warning("   The ingestion script is ready but requires data files.")
            logger.warning("   Run download_whitehouse.py first to fetch the data.")
        else:
            logger.info(f"\n🚀 Starting ingestion for {len(csv_files)} CSV files...")
            start_time = time.time()

            total_inserted = 0
            for year, filepath in csv_files:
                logger.info(f"\n  Processing {filepath.name}...")
                inserted = ingest_csv_file(conn, filepath, year, logger)
                total_inserted += inserted

            elapsed = time.time() - start_time

            logger.info("\n" + "=" * 80)
            logger.info("INGESTION SUMMARY")
            logger.info("=" * 80)
            logger.info(f"Files processed: {len(csv_files)}")
            logger.info(f"New records inserted: {total_inserted:,}")
            logger.info(f"Total elapsed time: {elapsed:.2f}s ({elapsed/60:.2f} minutes)")
            logger.info("=" * 80)

        # Verify final count
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM whitehouse_visitors")
        total_count = cur.fetchone()[0]
        cur.close()
        logger.info(f"Total records in whitehouse_visitors: {total_count:,}")

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

    logger.info(f"\n✅ White House Ingestion Complete at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
