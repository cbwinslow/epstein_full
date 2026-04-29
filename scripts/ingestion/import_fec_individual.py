#!/usr/bin/env python3
"""
Import FEC Individual Contributions data to PostgreSQL
Source: FEC bulk data files (indiv24.zip)
Table: fec_individual_contributions
"""

import csv
import io
import logging
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

import psycopg2

# Configuration
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fec")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_fec_individual_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Get PostgreSQL connection with hardcoded credentials"""
    return psycopg2.connect(
        host="localhost", database="epstein", user="cbwinslow", password="123qweasd"
    )


def create_table():
    """Create FEC individual contributions table if it doesn't exist"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fec_individual_contributions (
            id SERIAL PRIMARY KEY,
            cmte_id TEXT,
            amndt_ind TEXT,
            rpt_tp TEXT,
            transaction_pgi TEXT,
            image_num TEXT,
            transaction_tp TEXT,
            entity_tp TEXT,
            name TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            employer TEXT,
            occupation TEXT,
            transaction_dt DATE,
            transaction_amt NUMERIC,
            other_id TEXT,
            tran_id TEXT,
            file_num INT,
            memo_cd TEXT,
            memo_text TEXT,
            sub_id INT,
            cycle INT,
            raw_data TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)

    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fi_cmte ON fec_individual_contributions (cmte_id);
        CREATE INDEX IF NOT EXISTS idx_fi_name ON fec_individual_contributions (name);
        CREATE INDEX IF NOT EXISTS idx_fi_state ON fec_individual_contributions (state);
        CREATE INDEX IF NOT EXISTS idx_fi_date ON fec_individual_contributions (transaction_dt);
        CREATE INDEX IF NOT EXISTS idx_fi_amt ON fec_individual_contributions (transaction_amt);
        CREATE INDEX IF NOT EXISTS idx_fi_cycle ON fec_individual_contributions (cycle);
    """)

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Table and indexes created/verified")


def parse_date(value: str) -> Optional[str]:
    """Parse date string (MMDDYYYY format) to ISO format (YYYY-MM-DD)"""
    if not value or len(value) != 8:
        return None
    try:
        return f"{value[4:8]}-{value[0:2]}-{value[2:4]}"
    except:
        return None


def parse_amount(value: str) -> float:
    """Parse amount string to float"""
    if not value:
        return 0.0
    try:
        return float(value.strip())
    except:
        return 0.0


def transform_row(row: list, cycle: int) -> Optional[tuple]:
    """Transform a single row from FEC format to PostgreSQL format

    FEC itcont.txt format (21 pipe-delimited fields, NO header row):
    01: cmte_id
    02: amndt_ind
    03: rpt_tp
    04: transaction_pgi
    05: image_num
    06: transaction_tp
    07: entity_tp
    08: name
    09: city
    10: state
    11: zip_code
    12: employer
    13: occupation
    14: transaction_dt (MMDDYYYY)
    15: transaction_amt
    16: other_id
    17: tran_id
    18: file_num
    19: memo_cd
    20: memo_text
    21: sub_id
    """
    try:
        if len(row) < 21:
            return None

        transaction_dt = parse_date(row[13])  # Column 14: MMDDYYYY
        amount = parse_amount(row[14])  # Column 15: amount
        file_num = row[17].strip() if len(row) > 17 else ""
        sub_id = row[20].strip() if len(row) > 20 else ""

        return (
            row[0][:9],  # cmte_id
            row[1][:1],  # amndt_ind
            row[2][:3],  # rpt_tp
            row[3][:5],  # transaction_pgi
            row[4][:18],  # image_num
            row[5][:3],  # transaction_tp
            row[6][:3],  # entity_tp
            row[7][:200],  # name
            row[8][:100],  # city
            row[9][:2],  # state
            row[10][:9],  # zip_code
            row[11][:200],  # employer
            row[12][:200],  # occupation
            transaction_dt,
            amount,
            row[15][:9] if len(row) > 15 else "",  # other_id
            row[16][:32] if len(row) > 16 else "",  # tran_id
            int(file_num) if file_num.isdigit() else None,
            row[18][:1] if len(row) > 18 else "",  # memo_cd
            row[19][:500] if len(row) > 19 else "",  # memo_text
            int(sub_id) if sub_id.isdigit() else None,
            cycle,
        )
    except Exception as e:
        logger.debug(f"Transform failed: {e}")
        return None


def import_from_zip(zip_path: Path, cycle: int, batch_size: int = 10000) -> int:
    """Import individual contributions from ZIP file"""
    total_imported = 0

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            txt_files = [f for f in z.namelist() if f.endswith(".txt")]

            for filename in txt_files:
                logger.info(f"Processing {filename}...")

                with z.open(filename) as f:
                    # Detect delimiter
                    first_line = f.readline().decode("utf-8", errors="ignore")
                    f.seek(0)
                    delimiter = "|" if "|" in first_line else ","

                    text_io = io.TextIOWrapper(f, encoding="utf-8", errors="ignore")
                    reader = csv.reader(text_io, delimiter=delimiter, quoting=csv.QUOTE_NONE)

                    # Process in batches
                    batch = []
                    file_imported = 0

                    for row in reader:
                        if len(row) < 10:
                            continue

                        transformed = transform_row(row, cycle)
                        if transformed:
                            batch.append(transformed)

                            if len(batch) >= batch_size:
                                # Insert batch
                                imported = insert_batch(batch)
                                total_imported += imported
                                file_imported += imported
                                batch = []
                                logger.info(f"  Imported {total_imported:,} total rows...")

                    # Insert remaining batch
                    if batch:
                        imported = insert_batch(batch)
                        total_imported += imported
                        file_imported += imported

                    logger.info(f"  Completed {filename}: {file_imported:,} rows")

    except Exception as e:
        logger.error(f"Error processing {zip_path}: {e}")
        import traceback

        logger.error(traceback.format_exc())

    return total_imported


def insert_batch(batch: list) -> int:
    """Insert a batch of rows using executemany for performance"""
    if not batch:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.executemany(
            """
            INSERT INTO fec_individual_contributions (
                cmte_id, amndt_ind, rpt_tp, transaction_pgi, image_num,
                transaction_tp, entity_tp, name, city, state, zip_code,
                employer, occupation, transaction_dt, transaction_amt,
                other_id, tran_id, file_num, memo_cd, memo_text, sub_id,
                cycle
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """,
            batch,
        )
        conn.commit()
        return len(batch)
    except Exception as e:
        conn.rollback()
        logger.error(f"Batch insert failed: {e}")
        return 0
    finally:
        cur.close()
        conn.close()


def update_inventory(count: int):
    """Update data inventory table"""
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO data_inventory (source_name, source_type, status, actual_records, last_updated)
            VALUES ('FEC Individual Contributions', 'government', 'imported', %s, NOW())
            ON CONFLICT (source_name) DO UPDATE SET
                status = 'imported',
                actual_records = %s,
                last_updated = NOW()
        """,
            (count, count),
        )
    except Exception as e:
        logger.warning(f"Could not update inventory: {e}")

    conn.commit()
    cur.close()
    conn.close()


def main():
    logger.info("=" * 80)
    logger.info("FEC INDIVIDUAL CONTRIBUTIONS IMPORT")
    logger.info("=" * 80)

    create_table()

    # Find indiv24.zip
    zip_file = BASE_DIR / "indiv24.zip"
    if not zip_file.exists():
        logger.error(f"ZIP file not found: {zip_file}")
        return

    logger.info(f"Processing {zip_file.name} (11GB compressed)...")
    logger.info("This may take several hours...")

    # Import 2024 cycle data
    total_rows = import_from_zip(zip_file, cycle=2024, batch_size=10000)

    update_inventory(total_rows)

    logger.info("=" * 80)
    logger.info(f"IMPORT COMPLETE: {total_rows:,} individual contributions")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
