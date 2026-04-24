#!/usr/bin/env python3
"""
Import GovInfo Federal Register bulk XML ZIPs into PostgreSQL.

This importer reads the official GovInfo bulk FR ZIPs and stores one row per
RULE/PRORULE/NOTICE article in federal_register_entries. It is resumable and
idempotent through govinfo_bulk_import_status and deterministic package IDs.
"""

import argparse
import json
import logging
import re
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

import psycopg2
from lxml import etree as ET

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/fr")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_govinfo_fr_bulk_{datetime.now():%Y%m%d_%H%M%S}.log"
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


def is_valid_zip(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            archive.testzip()
        return True
    except (zipfile.BadZipFile, OSError):
        return False


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_xml_root(xml_bytes: bytes, source_file: str):
    parser = ET.XMLParser(recover=True, huge_tree=True)
    root = ET.fromstring(xml_bytes, parser=parser)
    if root is None:
        raise ValueError(f"Could not parse XML for {source_file}")
    return root


def extract_plain_text(elem) -> str:
    if elem is None:
        return ""
    return clean_text(" ".join(text for text in elem.itertext() if text and text.strip()))


def parse_page_range(value: str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    if not value:
        return None, None, None
    parts = [int(part) for part in re.findall(r"\d+", value)]
    if not parts:
        return None, None, None
    if len(parts) == 1:
        return parts[0], parts[0], 1
    return parts[0], parts[-1], (parts[-1] - parts[0] + 1)


def parse_publication_date(member: str) -> Optional[str]:
    match = re.search(r"FR-(\d{4})-(\d{2})-(\d{2})\.xml$", member)
    if not match:
        return None
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"


def parse_fr_doc_number(value: str) -> str:
    if not value:
        return ""
    match = re.search(r"FR Doc\.?\s+([0-9-]+)", value)
    return match.group(1) if match else ""


def article_package_id(fr_doc_number: str, source_file: str) -> str:
    if fr_doc_number:
        return f"FR-{fr_doc_number}"
    digest = re.sub(r"[^A-Za-z0-9]+", "-", source_file).strip("-")
    return f"FR-SRC-{digest}"


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

            CREATE TABLE IF NOT EXISTS federal_register_entries (
                id SERIAL PRIMARY KEY,
                package_id TEXT UNIQUE,
                fr_doc_number TEXT,
                citation TEXT,
                title TEXT,
                abstract TEXT,
                dates TEXT,
                agencies TEXT,
                action TEXT,
                significant BOOLEAN DEFAULT FALSE,
                rindicators TEXT,
                pdf_url TEXT,
                html_url TEXT,
                mods_url TEXT,
                premis_url TEXT,
                date_published DATE,
                volume INT,
                page_start INT,
                page_end INT,
                number_of_pages INT,
                docket_ids TEXT,
                regulations_dot_gov_ids TEXT,
                correction_of_fr_doc_number TEXT,
                is_correction BOOLEAN DEFAULT FALSE,
                su_doc_class_number TEXT,
                original_content_type TEXT,
                raw_data JSONB,
                imported_at TIMESTAMPTZ DEFAULT NOW(),
                source_file TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_fr_date ON federal_register_entries (date_published);
            CREATE INDEX IF NOT EXISTS idx_fr_agencies ON federal_register_entries (agencies);
            CREATE INDEX IF NOT EXISTS idx_fr_doc ON federal_register_entries (fr_doc_number);
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
            ("FR", str(file_path), status, error_type, error_message, status),
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
                  AND dataset = 'FR'
                  AND status = 'completed'
            )
            """,
            (str(zip_path),),
        )
        return bool(cur.fetchone()[0])
    finally:
        cur.close()
        conn.close()


def build_contents_index(root) -> Dict[str, Dict[str, str]]:
    index: Dict[str, Dict[str, str]] = {}
    for entry in root.xpath(".//CNTNTS//*[FRDOCBP]"):
        fr_doc_number = clean_text(entry.findtext("./FRDOCBP"))
        if not fr_doc_number:
            continue

        title = ""
        for tag_name in ("DOC", "SJDOC", "SUBSJDOC"):
            title = clean_text(entry.findtext(f"./{tag_name}"))
            if title:
                break

        pages = clean_text(entry.findtext("./PGS"))
        category = clean_text(entry.xpath("string(ancestor::CAT[1]/HD[1])"))
        section_subject = clean_text(entry.xpath("string(ancestor::CAT[1]/SJ[1])"))
        subsection_subject = clean_text(entry.xpath("string(ancestor::CAT[1]/SUBSJ[1])"))
        agency = clean_text(entry.xpath("string(ancestor::AGCY[1]/HD[1])"))

        index[fr_doc_number] = {
            "title": title,
            "pages": pages,
            "category": category,
            "section_subject": section_subject,
            "subsection_subject": subsection_subject,
            "agency": agency,
        }

    return index


def import_zip(zip_path: Path) -> Dict[str, int]:
    stats = {"entries": 0}
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        with zipfile.ZipFile(zip_path) as archive:
            for member in archive.namelist():
                if not member.endswith(".xml"):
                    continue

                source_prefix = f"{zip_path}:{member}"
                xml_bytes = archive.read(member)
                root = parse_xml_root(xml_bytes, source_prefix)
                volume = int(re.sub(r"\D", "", clean_text(root.findtext("./VOL"))) or 0) or None
                date_published = parse_publication_date(member)
                contents_index = build_contents_index(root)

                for tag_name in ("RULE", "PRORULE", "NOTICE"):
                    for idx, article in enumerate(root.findall(f".//{tag_name}"), start=1):
                        preamb = article.find("./PREAMB")
                        fr_doc_text = clean_text(article.findtext("./FRDOC"))
                        fr_doc_number = parse_fr_doc_number(fr_doc_text)
                        content_meta = contents_index.get(fr_doc_number, {})

                        title = (
                            clean_text(preamb.findtext("./SUBJECT")) if preamb is not None else ""
                        ) or content_meta.get("title", "") or content_meta.get("section_subject", "")
                        abstract = clean_text(extract_plain_text(preamb.find("./SUM"))) if preamb is not None else ""
                        dates = (
                            clean_text(extract_plain_text(preamb.find("./EFFDATE"))) if preamb is not None else ""
                        ) or (clean_text(extract_plain_text(preamb.find("./DATES"))) if preamb is not None else "")
                        agencies = (
                            clean_text(preamb.findtext("./AGENCY")) if preamb is not None else ""
                        ) or (clean_text(extract_plain_text(preamb.find("./AGY"))) if preamb is not None else "") or content_meta.get("agency", "")
                        action = clean_text(extract_plain_text(preamb.find("./ACT"))) if preamb is not None else ""
                        rindicators = clean_text(preamb.findtext("./RIN")) if preamb is not None else ""
                        prtpage = preamb.find("./PRTPAGE") if preamb is not None else None
                        page_start = int(re.sub(r"\D", "", prtpage.get("P", "")) or 0) or None if prtpage is not None else None
                        page_end, number_of_pages = None, None
                        _, parsed_end, parsed_pages = parse_page_range(content_meta.get("pages", ""))
                        if parsed_end is not None:
                            page_end = parsed_end
                            number_of_pages = parsed_pages
                        elif page_start is not None:
                            page_end = page_start
                            number_of_pages = 1

                        citation = f"{volume} FR {page_start}" if volume and page_start else ""
                        correction_of = ""
                        correction_match = re.search(r"Correction to FR Doc\.?\s+([0-9-]+)", extract_plain_text(article), re.IGNORECASE)
                        if correction_match:
                            correction_of = correction_match.group(1)

                        package_id = article_package_id(fr_doc_number, f"{source_prefix}:{idx}")
                        raw_payload = {
                            "member": member,
                            "entry_index": idx,
                            "entry_type": tag_name,
                            "fr_doc_text": fr_doc_text,
                            "billing_code": clean_text(article.findtext("./BILCOD")),
                            "content_index": content_meta,
                            "source_xml_path": member,
                        }

                        cur.execute(
                            """
                            INSERT INTO federal_register_entries (
                                package_id, fr_doc_number, citation, title, abstract, dates, agencies, action,
                                significant, rindicators, pdf_url, html_url, mods_url, premis_url,
                                date_published, volume, page_start, page_end, number_of_pages, docket_ids,
                                regulations_dot_gov_ids, correction_of_fr_doc_number, is_correction,
                                su_doc_class_number, original_content_type, raw_data, source_file
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s::jsonb, %s
                            )
                            ON CONFLICT (package_id) DO UPDATE SET
                                citation = EXCLUDED.citation,
                                title = EXCLUDED.title,
                                abstract = EXCLUDED.abstract,
                                dates = EXCLUDED.dates,
                                agencies = EXCLUDED.agencies,
                                action = EXCLUDED.action,
                                significant = EXCLUDED.significant,
                                rindicators = EXCLUDED.rindicators,
                                date_published = EXCLUDED.date_published,
                                volume = EXCLUDED.volume,
                                page_start = EXCLUDED.page_start,
                                page_end = EXCLUDED.page_end,
                                number_of_pages = EXCLUDED.number_of_pages,
                                correction_of_fr_doc_number = EXCLUDED.correction_of_fr_doc_number,
                                is_correction = EXCLUDED.is_correction,
                                original_content_type = EXCLUDED.original_content_type,
                                raw_data = EXCLUDED.raw_data,
                                source_file = EXCLUDED.source_file,
                                imported_at = NOW()
                            """,
                            (
                                package_id,
                                fr_doc_number or None,
                                citation or None,
                                title or None,
                                abstract or None,
                                dates or None,
                                agencies or None,
                                action or None,
                                bool(rindicators),
                                rindicators or None,
                                None,
                                None,
                                None,
                                None,
                                date_published,
                                volume,
                                page_start,
                                page_end,
                                number_of_pages,
                                None,
                                None,
                                correction_of or None,
                                bool(correction_of),
                                clean_text(article.findtext("./BILCOD")) or None,
                                tag_name,
                                json.dumps(raw_payload),
                                f"{source_prefix}:{tag_name}:{idx}",
                            ),
                        )
                        stats["entries"] += 1

        conn.commit()
        return stats
    finally:
        cur.close()
        conn.close()


def process_zip(zip_path: Path, skip_imported: bool) -> Dict[str, object]:
    if not is_valid_zip(zip_path):
        mark_import_status(zip_path, "failed", "BadZipFile", "File is not a valid ZIP archive")
        return {"zip_path": str(zip_path), "status": "failed", "error_type": "BadZipFile"}
    if skip_imported and zip_already_imported(zip_path):
        return {"zip_path": str(zip_path), "status": "skipped"}

    stats = import_zip(zip_path)
    mark_import_status(zip_path, "completed")
    return {"zip_path": str(zip_path), "status": "completed", "stats": stats}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-dir", type=Path, default=BASE_DIR)
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--skip-imported", dest="skip_imported", action="store_true")
    parser.add_argument("--no-skip-imported", dest="skip_imported", action="store_false")
    parser.set_defaults(skip_imported=True)
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("GOVINFO FR BULK IMPORT")
    logger.info("=" * 80)
    create_tables()

    zip_files = sorted(args.base_dir.glob("**/*.zip" if args.recursive else "*.zip"))
    if not zip_files:
        logger.warning("No FR ZIP files found")
        return

    totals = {"entries": 0}
    failed = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(process_zip, zip_path, args.skip_imported): zip_path
            for zip_path in zip_files
        }
        for future in as_completed(futures):
            zip_path = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                logger.exception(f"Failed to import {zip_path}: {exc}")
                mark_import_status(zip_path, "failed", type(exc).__name__, str(exc))
                failed.append((str(zip_path), type(exc).__name__))
                continue

            if result["status"] == "skipped":
                logger.info(f"Skipping already imported ZIP: {zip_path}")
                continue
            if result["status"] == "failed":
                logger.error(f"Failed ZIP: {zip_path} ({result['error_type']})")
                failed.append((str(zip_path), result["error_type"]))
                continue

            stats = result["stats"]
            totals["entries"] += stats["entries"]
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
