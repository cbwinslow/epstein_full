#!/usr/bin/env python3
"""
Import GovInfo BILLSUM bulk XML ZIPs into PostgreSQL.

This importer reuses:
- congress_bills
- congress_bill_summaries
- govinfo_bulk_import_status
"""

import argparse
import logging
import re
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import psycopg2
from psycopg2 import errors

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/billsum")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_govinfo_billsum_bulk_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="epstein",
        user="cbwinslow",
        password="123qweasd",
    )


def parse_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return value[:10]


def clean_summary_text(value: Optional[str]) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_valid_zip(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            archive.testzip()
        return True
    except zipfile.BadZipFile:
        return False
    except OSError:
        return False


def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS govinfo_bulk_import_status (
                id BIGSERIAL PRIMARY KEY,
                dataset TEXT NOT NULL,
                file_path TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL,
                error_type TEXT,
                error_message TEXT,
                last_success_at TIMESTAMPTZ,
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE UNIQUE INDEX IF NOT EXISTS uq_congress_bills_key
                ON congress_bills (congress, bill_type, bill_number);

            ALTER TABLE congress_bill_summaries
                ADD COLUMN IF NOT EXISTS current_chamber TEXT;
            """
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def mark_import_status(
    file_path: Path,
    status: str,
    error_type: Optional[str] = None,
    error_message: Optional[str] = None,
):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO govinfo_bulk_import_status (
                dataset, file_path, status, error_type, error_message, last_success_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, CASE WHEN %s = 'completed' THEN NOW() ELSE NULL END, NOW())
            ON CONFLICT (file_path) DO UPDATE SET
                status = EXCLUDED.status,
                error_type = EXCLUDED.error_type,
                error_message = EXCLUDED.error_message,
                last_success_at = CASE
                    WHEN EXCLUDED.status = 'completed' THEN NOW()
                    ELSE govinfo_bulk_import_status.last_success_at
                END,
                updated_at = NOW()
            """,
            ("BILLSUM", str(file_path), status, error_type, error_message, status),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def zip_already_imported(zip_path: Path) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM govinfo_bulk_import_status
                WHERE file_path = %s
                  AND dataset = 'BILLSUM'
                  AND status = 'completed'
            )
            """,
            (str(zip_path),),
        )
        if cur.fetchone()[0]:
            return True
        cur.execute(
            "SELECT EXISTS (SELECT 1 FROM congress_bill_summaries WHERE source_file LIKE %s LIMIT 1)",
            (f"{zip_path}:%",),
        )
        return bool(cur.fetchone()[0])
    finally:
        cur.close()
        conn.close()


def get_or_create_bill(
    cur,
    congress: int,
    bill_type: str,
    bill_number: str,
    title: str,
    latest_summary: str,
    source_file: str,
) -> int:
    cur.execute(
        """
        SELECT id
        FROM congress_bills
        WHERE congress = %s AND bill_type = %s AND bill_number = %s
        """,
        (congress, bill_type, bill_number),
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE congress_bills
            SET title = COALESCE(NULLIF(%s, ''), title),
                summary = COALESCE(NULLIF(%s, ''), summary),
                imported_at = NOW()
            WHERE id = %s
            """,
            (title, latest_summary, row[0]),
        )
        return row[0]

    cur.execute(
        """
        INSERT INTO congress_bills (bill_number, bill_type, congress, title, summary, raw_data, source_file)
        VALUES (%s, %s, %s, %s, %s, '{}'::jsonb, %s)
        ON CONFLICT (congress, bill_type, bill_number) DO UPDATE SET
            title = COALESCE(NULLIF(EXCLUDED.title, ''), congress_bills.title),
            summary = COALESCE(NULLIF(EXCLUDED.summary, ''), congress_bills.summary),
            source_file = COALESCE(congress_bills.source_file, EXCLUDED.source_file),
            imported_at = NOW()
        RETURNING id
        """,
        (bill_number, bill_type, congress, title, latest_summary, source_file),
    )
    return cur.fetchone()[0]


def insert_summary(
    cur,
    bill_id: int,
    version_code: str,
    current_chamber: str,
    action_date: Optional[str],
    action_desc: str,
    update_date: Optional[str],
    summary_text: str,
    source_file: str,
):
    cur.execute(
        """
        INSERT INTO congress_bill_summaries (
            bill_id, version_code, current_chamber, action_date, action_desc, update_date, summary_text, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        """,
        (
            bill_id,
            version_code,
            current_chamber,
            action_date,
            action_desc,
            update_date,
            summary_text,
            source_file,
        ),
    )


def import_zip(zip_path: Path) -> Dict[str, int]:
    stats = {"bills": 0, "summaries": 0}
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        with zipfile.ZipFile(zip_path) as archive:
            for member in archive.namelist():
                if not member.endswith(".xml"):
                    continue

                root = ET.fromstring(archive.read(member))
                item = root.find("./item")
                if item is None:
                    continue

                congress = int(item.attrib["congress"])
                bill_type = item.attrib["measure-type"].lower()
                bill_number = item.attrib["measure-number"]
                title = (item.findtext("./title") or "").strip()
                source_file = f"{zip_path}:{member}"

                summaries = item.findall("./summary")
                latest_summary = ""
                if summaries:
                    latest_summary = clean_summary_text(summaries[0].findtext("./summary-text"))

                bill_id = get_or_create_bill(
                    cur, congress, bill_type, bill_number, title, latest_summary, source_file
                )
                stats["bills"] += 1

                for summary in summaries:
                    version_code = summary.attrib.get("summary-id", "")
                    current_chamber = summary.attrib.get("currentChamber", "")
                    action_date = parse_date(summary.findtext("./action-date"))
                    action_desc = (summary.findtext("./action-desc") or "").strip()
                    update_date = parse_date(summary.attrib.get("update-date"))
                    summary_text = clean_summary_text(summary.findtext("./summary-text"))
                    insert_summary(
                        cur,
                        bill_id,
                        version_code,
                        current_chamber,
                        action_date,
                        action_desc,
                        update_date,
                        summary_text,
                        source_file,
                    )

        conn.commit()
    finally:
        cur.close()
        conn.close()

    verify_conn = get_db_connection()
    verify_cur = verify_conn.cursor()
    try:
        verify_cur.execute(
            "SELECT count(*) FROM congress_bills WHERE source_file LIKE %s", (f"{zip_path}:%",)
        )
        stats["bills"] = verify_cur.fetchone()[0]
        verify_cur.execute(
            "SELECT count(*) FROM congress_bill_summaries WHERE source_file LIKE %s",
            (f"{zip_path}:%",),
        )
        stats["summaries"] = verify_cur.fetchone()[0]
    finally:
        verify_cur.close()
        verify_conn.close()

    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-dir", type=Path, default=BASE_DIR)
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--skip-imported", dest="skip_imported", action="store_true")
    parser.add_argument("--no-skip-imported", dest="skip_imported", action="store_false")
    parser.set_defaults(skip_imported=True)
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("GOVINFO BILLSUM BULK IMPORT")
    logger.info("=" * 80)
    create_tables()

    zip_files = sorted(args.base_dir.glob("**/*.zip" if args.recursive else "*.zip"))
    if not zip_files:
        logger.warning("No BILLSUM ZIP files found")
        return

    totals = {"bills": 0, "summaries": 0}
    failed = []
    for zip_path in zip_files:
        if not is_valid_zip(zip_path):
            logger.error(f"Skipping corrupt ZIP: {zip_path}")
            mark_import_status(zip_path, "failed", "BadZipFile", "File is not a valid ZIP archive")
            failed.append((str(zip_path), "BadZipFile"))
            continue
        if args.skip_imported and zip_already_imported(zip_path):
            logger.info(f"Skipping already imported ZIP: {zip_path}")
            continue

        logger.info(f"Processing {zip_path}...")
        for attempt in range(1, 4):
            try:
                stats = import_zip(zip_path)
                mark_import_status(zip_path, "completed")
                break
            except errors.DeadlockDetected as exc:
                logger.warning(f"Deadlock importing {zip_path} (attempt {attempt}/3): {exc}")
                if attempt == 3:
                    mark_import_status(zip_path, "failed", type(exc).__name__, str(exc))
                    failed.append((str(zip_path), type(exc).__name__))
                    stats = None
                else:
                    time.sleep(attempt * 2)
            except Exception as exc:
                logger.exception(f"Failed to import {zip_path}: {exc}")
                mark_import_status(zip_path, "failed", type(exc).__name__, str(exc))
                failed.append((str(zip_path), type(exc).__name__))
                stats = None
                break
        if stats is None:
            continue

        for key, value in stats.items():
            totals[key] += value
        logger.info(f"Imported {zip_path.name}: {stats}")

    logger.info("=" * 80)
    logger.info(f"IMPORT COMPLETE: {totals}")
    if failed:
        logger.warning(f"FAILED ZIPS: {len(failed)}")
        for path, error in failed:
            logger.warning(f"  {error}: {path}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
