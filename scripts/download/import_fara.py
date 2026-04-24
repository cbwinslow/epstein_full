#!/usr/bin/env python3
"""Import FARA bulk XML datasets into normalized PostgreSQL tables."""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional

import psycopg2
from lxml import etree
from psycopg2.extras import execute_values

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fara")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_fara_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg2.connect(
        host="localhost", database="epstein", user="cbwinslow", password="123qweasd"
    )


def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    # FARA Registrations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fara_registrations (
            id SERIAL PRIMARY KEY,
            registration_number TEXT UNIQUE,
            registrant_name TEXT,
            registrant_address TEXT,
            registrant_city TEXT,
            registrant_state TEXT,
            registrant_zip TEXT,
            registrant_country TEXT,
            registration_date DATE,
            foreign_principal TEXT,
            foreign_principal_address TEXT,
            foreign_principal_city TEXT,
            foreign_principal_state TEXT,
            foreign_principal_zip TEXT,
            foreign_principal_country TEXT,
            registration_purpose TEXT,
            signed_date DATE,
            document_url TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    cur.execute(
        "ALTER TABLE fara_registrations ADD COLUMN IF NOT EXISTS foreign_principal_state TEXT;"
    )
    cur.execute(
        "ALTER TABLE fara_registrations ADD COLUMN IF NOT EXISTS foreign_principal_zip TEXT;"
    )
    cur.execute("ALTER TABLE fara_registrations ADD COLUMN IF NOT EXISTS raw_data JSONB;")
    cur.execute(
        "ALTER TABLE fara_registrations ADD COLUMN IF NOT EXISTS imported_at TIMESTAMPTZ DEFAULT NOW();"
    )

    # FARA Foreign Principals table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fara_foreign_principals (
            id SERIAL PRIMARY KEY,
            registration_number TEXT,
            principal_name TEXT,
            principal_address TEXT,
            principal_city TEXT,
            principal_country TEXT,
            principal_type TEXT,
            foreign_government BOOLEAN DEFAULT FALSE,
            foreign_political_party BOOLEAN DEFAULT FALSE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)

    # FARA short-form registrations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fara_short_forms (
            id BIGSERIAL PRIMARY KEY,
            registration_number TEXT,
            registration_date DATE,
            registrant_name TEXT,
            short_form_date DATE,
            short_form_last_name TEXT,
            short_form_first_name TEXT,
            short_form_middle_name TEXT,
            short_form_title TEXT,
            address_1 TEXT,
            address_2 TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            country TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)

    # FARA registrant-linked documents
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fara_registrant_docs (
            id BIGSERIAL PRIMARY KEY,
            cdate_stamped DATE,
            registrant_name TEXT,
            registration_number TEXT,
            document_type TEXT,
            foreign_principal_name TEXT,
            foreign_principal_country TEXT,
            short_form_name TEXT,
            url TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)

    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fr_regnum ON fara_registrations (registration_number);
        CREATE INDEX IF NOT EXISTS idx_fr_name ON fara_registrations (registrant_name);
        CREATE INDEX IF NOT EXISTS idx_fp_regnum ON fara_foreign_principals (registration_number);
        CREATE INDEX IF NOT EXISTS idx_fp_country ON fara_foreign_principals (principal_country);
        CREATE INDEX IF NOT EXISTS idx_fs_regnum ON fara_short_forms (registration_number);
        CREATE INDEX IF NOT EXISTS idx_frd_regnum ON fara_registrant_docs (registration_number);
        CREATE INDEX IF NOT EXISTS idx_frd_doctype ON fara_registrant_docs (document_type);
    """)

    cur.execute("DROP INDEX IF EXISTS uq_fp_identity;")
    cur.execute("DROP INDEX IF EXISTS uq_fs_identity;")
    cur.execute("DROP INDEX IF EXISTS uq_frd_url;")
    cur.execute("""
        CREATE UNIQUE INDEX uq_fp_identity
        ON fara_foreign_principals (registration_number, principal_name, principal_country);
    """)
    cur.execute("""
        CREATE UNIQUE INDEX uq_fs_identity
        ON fara_short_forms (registration_number, short_form_last_name, short_form_first_name, short_form_date);
    """)
    cur.execute("""
        CREATE UNIQUE INDEX uq_frd_url
        ON fara_registrant_docs (url);
    """)

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables and indexes created/verified")


def _norm_key(key: str) -> str:
    return key.strip().lower()


def _parse_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def _row_to_map(row_el: etree._Element) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for child in row_el:
        key = _norm_key(child.tag)
        out[key] = (child.text or "").strip()
    return out


def iter_rows(filepath: Path, row_tag: str = "ROW") -> Iterator[Dict[str, str]]:
    context = etree.iterparse(
        str(filepath),
        events=("end",),
        tag=row_tag,
        recover=True,
        huge_tree=True,
    )
    for _, elem in context:
        yield _row_to_map(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]


def _batched(rows: Iterable[Dict[str, str]], batch_size: int) -> Iterator[List[Dict[str, str]]]:
    batch: List[Dict[str, str]] = []
    for row in rows:
        batch.append(row)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def _dedupe_rows(rows: List[Dict[str, str]], key_fields: List[str]) -> List[Dict[str, str]]:
    if not rows:
        return rows
    kept: Dict[tuple, Dict[str, str]] = {}
    for row in rows:
        key = tuple((row.get(k) or "").strip() for k in key_fields)
        if all(not v for v in key):
            continue
        kept[key] = row
    return list(kept.values())


def import_registrations(records: List[Dict]) -> int:
    records = _dedupe_rows(records, ["registration_number"])
    if not records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()

    values = []
    for r in records:
        values.append(
            (
                r.get("registration_number"),
                r.get("registrant_name") or r.get("name"),
                r.get("registrant_address") or r.get("address_1"),
                r.get("registrant_city") or r.get("city"),
                r.get("registrant_state") or r.get("state"),
                r.get("registrant_zip") or r.get("zip"),
                r.get("registrant_country") or r.get("country"),
                _parse_date(r.get("registration_date")),
                r.get("foreign_principal"),
                r.get("foreign_principal_address") or r.get("address_1"),
                r.get("foreign_principal_city") or r.get("city"),
                r.get("foreign_principal_state") or r.get("state"),
                r.get("foreign_principal_zip") or r.get("zip"),
                r.get("foreign_principal_country") or r.get("country_location_represented"),
                r.get("registration_purpose"),
                _parse_date(r.get("signed_date")),
                r.get("document_url"),
                json.dumps(r),
                r.get("source_file"),
            )
        )

    execute_values(
        cur,
        """
        INSERT INTO fara_registrations (
            registration_number, registrant_name, registrant_address, registrant_city,
            registrant_state, registrant_zip, registrant_country, registration_date,
            foreign_principal, foreign_principal_address, foreign_principal_city,
            foreign_principal_state, foreign_principal_zip, foreign_principal_country,
            registration_purpose, signed_date, document_url, raw_data, source_file
        ) VALUES %s
        ON CONFLICT (registration_number) DO UPDATE SET
            registrant_name = EXCLUDED.registrant_name,
            registrant_address = EXCLUDED.registrant_address,
            registrant_city = EXCLUDED.registrant_city,
            registrant_state = EXCLUDED.registrant_state,
            registrant_zip = EXCLUDED.registrant_zip,
            registrant_country = EXCLUDED.registrant_country,
            registration_date = EXCLUDED.registration_date,
            imported_at = NOW(),
            raw_data = EXCLUDED.raw_data,
            source_file = EXCLUDED.source_file
    """,
        values,
        page_size=2000,
    )
    conn.commit()
    cur.close()
    conn.close()
    return len(values)


def import_foreign_principals(records: List[Dict]) -> int:
    records = _dedupe_rows(
        records,
        [
            "registration_number",
            "principal_name",
            "foreign_principal",
            "principal_country",
            "country_location_represented",
        ],
    )
    if not records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()

    values = []
    for r in records:
        values.append(
            (
                r.get("registration_number"),
                r.get("principal_name") or r.get("foreign_principal"),
                r.get("principal_address") or r.get("address_1"),
                r.get("principal_city") or r.get("city"),
                r.get("principal_country") or r.get("country_location_represented"),
                r.get("principal_type"),
                str(r.get("foreign_government", "")).strip().lower() in {"true", "1", "yes", "y"},
                str(r.get("foreign_political_party", "")).strip().lower()
                in {"true", "1", "yes", "y"},
                json.dumps(r),
                r.get("source_file"),
            )
        )

    execute_values(
        cur,
        """
        INSERT INTO fara_foreign_principals (
            registration_number, principal_name, principal_address, principal_city,
            principal_country, principal_type, foreign_government,
            foreign_political_party, raw_data, source_file
        ) VALUES %s
        ON CONFLICT (registration_number, principal_name, principal_country) DO UPDATE SET
            principal_address = EXCLUDED.principal_address,
            principal_city = EXCLUDED.principal_city,
            principal_type = EXCLUDED.principal_type,
            foreign_government = EXCLUDED.foreign_government,
            foreign_political_party = EXCLUDED.foreign_political_party,
            raw_data = EXCLUDED.raw_data,
            source_file = EXCLUDED.source_file,
            imported_at = NOW()
    """,
        values,
        page_size=2000,
    )
    conn.commit()
    cur.close()
    conn.close()
    return len(values)


def import_short_forms(records: List[Dict]) -> int:
    records = _dedupe_rows(
        records,
        ["registration_number", "short_form_last_name", "short_form_first_name", "short_form_date"],
    )
    if not records:
        return 0
    conn = get_db_connection()
    cur = conn.cursor()
    values = []
    for r in records:
        values.append(
            (
                r.get("registration_number"),
                _parse_date(r.get("registration_date")),
                r.get("registrant_name"),
                _parse_date(r.get("short_form_date")),
                r.get("short_form_last_name"),
                r.get("short_form_first_name"),
                r.get("short_form_middle_name"),
                r.get("short_form_title"),
                r.get("address_1"),
                r.get("address_2"),
                r.get("city"),
                r.get("state"),
                r.get("zip"),
                r.get("country"),
                json.dumps(r),
                r.get("source_file"),
            )
        )
    execute_values(
        cur,
        """
        INSERT INTO fara_short_forms (
            registration_number, registration_date, registrant_name,
            short_form_date, short_form_last_name, short_form_first_name,
            short_form_middle_name, short_form_title, address_1, address_2,
            city, state, zip, country, raw_data, source_file
        ) VALUES %s
        ON CONFLICT (registration_number, short_form_last_name, short_form_first_name, short_form_date) DO UPDATE SET
            registrant_name = EXCLUDED.registrant_name,
            address_1 = EXCLUDED.address_1,
            city = EXCLUDED.city,
            state = EXCLUDED.state,
            zip = EXCLUDED.zip,
            country = EXCLUDED.country,
            raw_data = EXCLUDED.raw_data,
            source_file = EXCLUDED.source_file,
            imported_at = NOW()
    """,
        values,
        page_size=2000,
    )
    conn.commit()
    cur.close()
    conn.close()
    return len(values)


def import_registrant_docs(records: List[Dict]) -> int:
    if not records:
        return 0
    conn = get_db_connection()
    cur = conn.cursor()
    keyed_values: Dict[tuple, tuple] = {}
    for r in records:
        normalized_url = (r.get("url") or "").strip() or None
        row = (
            _parse_date(r.get("cdate_stamped")),
            r.get("registrant_name"),
            r.get("registration_number"),
            r.get("document_type"),
            r.get("foreign_principal_name"),
            r.get("foreign_principal_country"),
            r.get("short_form_name"),
            normalized_url,
            json.dumps(r),
            r.get("source_file"),
        )
        if normalized_url:
            key = ("url", normalized_url)
        else:
            key = (
                "fallback",
                (r.get("registration_number") or "").strip(),
                (r.get("document_type") or "").strip(),
                (r.get("cdate_stamped") or "").strip(),
                (r.get("short_form_name") or "").strip(),
                (r.get("foreign_principal_name") or "").strip(),
            )
        keyed_values[key] = row
    values = list(keyed_values.values())
    if not values:
        cur.close()
        conn.close()
        return 0
    execute_values(
        cur,
        """
        INSERT INTO fara_registrant_docs (
            cdate_stamped, registrant_name, registration_number, document_type,
            foreign_principal_name, foreign_principal_country, short_form_name,
            url, raw_data, source_file
        ) VALUES %s
        ON CONFLICT (url) DO UPDATE SET
            cdate_stamped = EXCLUDED.cdate_stamped,
            registrant_name = EXCLUDED.registrant_name,
            registration_number = EXCLUDED.registration_number,
            document_type = EXCLUDED.document_type,
            foreign_principal_name = EXCLUDED.foreign_principal_name,
            foreign_principal_country = EXCLUDED.foreign_principal_country,
            short_form_name = EXCLUDED.short_form_name,
            raw_data = EXCLUDED.raw_data,
            source_file = EXCLUDED.source_file,
            imported_at = NOW()
    """,
        values,
        page_size=2000,
    )
    conn.commit()
    cur.close()
    conn.close()
    return len(values)


def update_inventory(total_count: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'data_inventory'
            ) THEN
                UPDATE data_inventory
                SET status = 'imported', actual_records = %s, last_updated = NOW()
                WHERE source_name = 'FARA (Foreign Agents Registration)';
            END IF;
        END $$;
    """,
        (total_count,),
    )
    conn.commit()
    cur.close()
    conn.close()


def _tag_source(rows: List[Dict], source_file: str) -> List[Dict]:
    for r in rows:
        r["source_file"] = source_file
    return rows


def _process_file(filepath: Path, batch_size: int) -> Dict[str, int]:
    name = filepath.name.lower()
    totals = {"registrations": 0, "principals": 0, "short_forms": 0, "docs": 0}

    if "registrants" in name and "docs" not in name:
        for batch in _batched(iter_rows(filepath), batch_size):
            totals["registrations"] += import_registrations(_tag_source(batch, filepath.name))
    elif "foreign_principals" in name:
        for batch in _batched(iter_rows(filepath), batch_size):
            totals["principals"] += import_foreign_principals(_tag_source(batch, filepath.name))
    elif "short_forms" in name:
        for batch in _batched(iter_rows(filepath), batch_size):
            totals["short_forms"] += import_short_forms(_tag_source(batch, filepath.name))
    elif "registrantdocs" in name:
        for batch in _batched(iter_rows(filepath), batch_size):
            totals["docs"] += import_registrant_docs(_tag_source(batch, filepath.name))
    else:
        logger.warning(f"Skipping unrecognized FARA file format: {filepath.name}")

    return totals


def main():
    parser = argparse.ArgumentParser(
        description="Import FARA bulk XML files to normalized PostgreSQL tables."
    )
    parser.add_argument(
        "--base-dir", default=str(BASE_DIR), help="Directory containing FARA XML files"
    )
    parser.add_argument("--batch-size", type=int, default=5000, help="Rows per DB batch")
    args = parser.parse_args()

    base_dir = Path(args.base_dir)

    logger.info("=" * 80)
    logger.info("FARA IMPORT")
    logger.info("=" * 80)

    create_tables()

    xml_files = sorted(base_dir.glob("*.xml"))
    if not xml_files:
        logger.warning("No XML files found")
        return

    logger.info(f"Found {len(xml_files)} XML files")

    totals = {"registrations": 0, "principals": 0, "short_forms": 0, "docs": 0}

    for xml_file in xml_files:
        logger.info(f"Processing {xml_file.name}...")
        file_totals = _process_file(xml_file, args.batch_size)
        for k, v in file_totals.items():
            totals[k] += v
        logger.info(
            "  Imported so far: registrations=%s principals=%s short_forms=%s docs=%s",
            totals["registrations"],
            totals["principals"],
            totals["short_forms"],
            totals["docs"],
        )

    grand_total = sum(totals.values())
    update_inventory(grand_total)

    logger.info("=" * 80)
    logger.info(
        "IMPORT COMPLETE: registrations=%s, principals=%s, short_forms=%s, docs=%s, total=%s",
        totals["registrations"],
        totals["principals"],
        totals["short_forms"],
        totals["docs"],
        grand_total,
    )
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
