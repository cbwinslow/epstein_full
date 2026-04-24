#!/usr/bin/env python3
"""
Import GovInfo BILLS bulk XML ZIPs into PostgreSQL.

This importer stores bill text versions in a normalized table tied to congress_bills.
"""

import argparse
import json
import logging
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import psycopg2
from lxml import etree as ET

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/bills")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_govinfo_bills_bulk_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

BILL_TYPE_MAP = {
    "HR": "hr",
    "S": "s",
    "HJRES": "hjres",
    "SJRES": "sjres",
    "HCONRES": "hconres",
    "SCONRES": "sconres",
    "HRES": "hres",
    "SRES": "sres",
}


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="epstein",
        user="cbwinslow",
        password="123qweasd",
    )


def is_valid_zip(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            archive.testzip()
        return True
    except zipfile.BadZipFile:
        return False
    except OSError:
        return False


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_legis_num(value: str) -> str:
    value = value.upper().replace(".", " ")
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\bH\s+J\s+RES\b", "HJRES", value)
    value = re.sub(r"\bS\s+J\s+RES\b", "SJRES", value)
    value = re.sub(r"\bH\s+CON\s+RES\b", "HCONRES", value)
    value = re.sub(r"\bS\s+CON\s+RES\b", "SCONRES", value)
    value = re.sub(r"\bH\s+RES\b", "HRES", value)
    value = re.sub(r"\bS\s+RES\b", "SRES", value)
    value = re.sub(r"\bH\s+R\b", "HR", value)
    return value


def extract_plain_text(elem: ET.Element) -> str:
    text = " ".join(t.strip() for t in elem.itertext() if t and t.strip())
    return clean_text(text)


def parse_from_member_name(member: str):
    stem = Path(member).stem.lower()
    match = re.match(r"bills-(\d+)(hr|s|hjres|sjres|hconres|sconres|hres|sres)(\d+)([a-z0-9]+)?$", stem)
    if not match:
        return None
    return int(match.group(1)), match.group(2), match.group(3), match.group(4) or stem


def parse_xml_root(xml_bytes: bytes, source_file: str):
    parser = ET.XMLParser(recover=True, huge_tree=True)
    root = ET.fromstring(xml_bytes, parser=parser)
    if root is None:
        raise ValueError(f"Could not parse XML for {source_file}")
    return root


def canonical_bill_type(raw_type: str, source_file: str) -> str:
    normalized = re.sub(r"[^A-Z]", "", raw_type.upper())
    bill_type = BILL_TYPE_MAP.get(normalized)
    if not bill_type:
        raise ValueError(f"Unknown bill type parsed from {source_file}: {raw_type}")
    return bill_type


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

            CREATE TABLE IF NOT EXISTS congress_bill_text_versions (
                id BIGSERIAL PRIMARY KEY,
                bill_id BIGINT NOT NULL REFERENCES congress_bills(id) ON DELETE CASCADE,
                congress INT NOT NULL,
                bill_type TEXT NOT NULL,
                bill_number TEXT NOT NULL,
                session_number INT,
                version_code TEXT,
                bill_stage TEXT,
                bill_xml_type TEXT,
                legis_num TEXT,
                legis_type TEXT,
                current_chamber TEXT,
                action_date DATE,
                action_desc TEXT,
                official_title TEXT,
                short_title TEXT,
                origin_chamber TEXT,
                publisher TEXT,
                document_date DATE,
                plain_text TEXT,
                raw_xml TEXT,
                metadata_json JSONB,
                source_file TEXT NOT NULL,
                imported_at TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE INDEX IF NOT EXISTS idx_cbtv_bill ON congress_bill_text_versions (bill_id);
            CREATE INDEX IF NOT EXISTS idx_cbtv_congress ON congress_bill_text_versions (congress, bill_type, bill_number);
            CREATE UNIQUE INDEX IF NOT EXISTS uq_cbtv_source
                ON congress_bill_text_versions (source_file);
            """
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def mark_import_status(file_path: Path, status: str, error_type: Optional[str] = None, error_message: Optional[str] = None):
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
            ("BILLS", str(file_path), status, error_type, error_message, status),
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
                  AND dataset = 'BILLS'
                  AND status = 'completed'
            )
            """,
            (str(zip_path),),
        )
        if cur.fetchone()[0]:
            return True
        cur.execute(
            "SELECT EXISTS (SELECT 1 FROM congress_bill_text_versions WHERE source_file LIKE %s LIMIT 1)",
            (f"{zip_path}:%",),
        )
        return bool(cur.fetchone()[0])
    finally:
        cur.close()
        conn.close()


def get_or_create_bill(cur, congress: int, bill_type: str, bill_number: str, title: str, source_file: str) -> int:
    cur.execute(
        "SELECT id FROM congress_bills WHERE congress = %s AND bill_type = %s AND bill_number = %s",
        (congress, bill_type, bill_number),
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE congress_bills
            SET title = COALESCE(NULLIF(%s, ''), title),
                imported_at = NOW()
            WHERE id = %s
            """,
            (title, row[0]),
        )
        return row[0]

    cur.execute(
        """
        INSERT INTO congress_bills (bill_number, bill_type, congress, title, raw_data, source_file)
        VALUES (%s, %s, %s, %s, '{}'::jsonb, %s)
        ON CONFLICT (congress, bill_type, bill_number) DO UPDATE SET
            title = COALESCE(NULLIF(EXCLUDED.title, ''), congress_bills.title),
            imported_at = NOW()
        RETURNING id
        """,
        (bill_number, bill_type, congress, title, source_file),
    )
    return cur.fetchone()[0]


def import_zip(zip_path: Path) -> Dict[str, int]:
    stats = {"bills": 0, "text_versions": 0}
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        with zipfile.ZipFile(zip_path) as archive:
            for member in archive.namelist():
                if not member.endswith(".xml"):
                    continue

                source_file = f"{zip_path}:{member}"
                xml_bytes = archive.read(member)
                root = parse_xml_root(xml_bytes, source_file)

                form = root.find("./form")
                metadata = root.find("./metadata")
                bill_stage = root.attrib.get("bill-stage", "")
                bill_xml_type = root.attrib.get("bill-type", "")
                congresst = clean_text(form.findtext("./congress")) if form is not None else ""
                sessiont = clean_text(form.findtext("./session")) if form is not None else ""
                legis_num = clean_text(form.findtext("./legis-num")) if form is not None else ""
                normalized_legis_num = normalize_legis_num(legis_num)
                current_chamber = clean_text(form.findtext("./current-chamber")) if form is not None else ""
                legis_type = clean_text(form.findtext("./legis-type")) if form is not None else ""
                official_title = clean_text(form.findtext("./official-title")) if form is not None else ""
                short_title = clean_text(root.findtext(".//short-title"))
                action_date_node = form.find("./action/action-date") if form is not None else None
                action_desc = extract_plain_text(form.find("./action/action-desc")) if form is not None and form.find("./action/action-desc") is not None else ""

                dc = {}
                if metadata is not None:
                    for elem in metadata.iter():
                        tag = elem.tag.split("}")[-1]
                        if elem.text and tag.startswith("dc:") is False and tag not in {"metadata", "dublinCore"}:
                            dc[tag] = clean_text(elem.text)

                match = re.search(r"([A-Z]+)\s+(\d+)$", normalized_legis_num)
                fallback = parse_from_member_name(member)
                if not match and not fallback:
                    raise ValueError(f"Could not parse legis-num from {source_file}: {legis_num}")

                congress = int(re.sub(r"\D", "", congresst)) if re.sub(r"\D", "", congresst) else (fallback[0] if fallback else None)
                if match:
                    bill_number = match.group(2)
                    raw_type = match.group(1)
                else:
                    bill_number = fallback[2]
                    raw_type = fallback[1].upper()
                bill_type = canonical_bill_type(raw_type, source_file)

                session_number = int(re.sub(r"\D", "", sessiont) or 0) or None
                bill_id = get_or_create_bill(cur, congress, bill_type, bill_number, official_title or short_title, source_file)

                cur.execute(
                    """
                    INSERT INTO congress_bill_text_versions (
                        bill_id, congress, bill_type, bill_number, session_number, version_code, bill_stage,
                        bill_xml_type, legis_num, legis_type, current_chamber, action_date, action_desc,
                        official_title, short_title, origin_chamber, publisher, document_date, plain_text,
                        raw_xml, metadata_json, source_file
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s)
                    ON CONFLICT (source_file) DO NOTHING
                    """,
                    (
                        bill_id,
                        congress,
                        bill_type,
                        bill_number,
                        session_number,
                        fallback[3] if fallback else Path(member).stem,
                        bill_stage,
                        bill_xml_type,
                        legis_num,
                        legis_type,
                        current_chamber,
                        action_date_node.get("date")[:4] + "-" + action_date_node.get("date")[4:6] + "-" + action_date_node.get("date")[6:8] if action_date_node is not None and action_date_node.get("date") else None,
                        action_desc,
                        official_title,
                        short_title,
                        current_chamber,
                        dc.get("publisher", ""),
                        dc.get("date", "")[:10] if dc.get("date") else None,
                        extract_plain_text(root.find("./legis-body")) if root.find("./legis-body") is not None else "",
                        xml_bytes.decode("utf-8", errors="ignore"),
                        json.dumps({"dublin_core": dc}),
                        source_file,
                    ),
                )
                stats["bills"] += 1

        conn.commit()
    finally:
        cur.close()
        conn.close()

    verify_conn = get_db_connection()
    verify_cur = verify_conn.cursor()
    try:
        verify_cur.execute("SELECT count(*) FROM congress_bill_text_versions WHERE source_file LIKE %s", (f"{zip_path}:%",))
        stats["text_versions"] = verify_cur.fetchone()[0]
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
    logger.info("GOVINFO BILLS BULK IMPORT")
    logger.info("=" * 80)
    create_tables()

    zip_files = sorted(args.base_dir.glob("**/*.zip" if args.recursive else "*.zip"))
    if not zip_files:
        logger.warning("No BILLS ZIP files found")
        return

    totals = {"bills": 0, "text_versions": 0}
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
        try:
            stats = import_zip(zip_path)
            mark_import_status(zip_path, "completed")
        except Exception as exc:
            logger.exception(f"Failed to import {zip_path}: {exc}")
            mark_import_status(zip_path, "failed", type(exc).__name__, str(exc))
            failed.append((str(zip_path), type(exc).__name__))
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
