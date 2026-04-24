#!/usr/bin/env python3
"""
Import GovInfo BILLSTATUS bulk XML ZIPs into PostgreSQL.

This importer enriches congress_bills and normalizes bill details into child tables:
- congress_bill_titles
- congress_bill_summaries
- congress_bill_actions
- congress_bill_cosponsors
- congress_bill_related_bills
- congress_bill_vote_references
"""

import argparse
import json
import logging
import re
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import psycopg2
from psycopg2 import errors

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/billstatus")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_govinfo_billstatus_bulk_{datetime.now():%Y%m%d_%H%M%S}.log"
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
    except zipfile.BadZipFile:
        return False
    except OSError:
        return False


def parse_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return value[:10]


def elem_text(elem: Optional[ET.Element], path: str, default: str = "") -> str:
    if elem is None:
        return default
    node = elem.find(path)
    if node is None or node.text is None:
        return default
    return node.text.strip()


def first_text(elem: Optional[ET.Element], *paths: str, default: str = "") -> str:
    for path in paths:
        value = elem_text(elem, path)
        if value:
            return value
    return default


def children(elem: Optional[ET.Element], path: str) -> List[ET.Element]:
    if elem is None:
        return []
    return list(elem.findall(path))


def extract_roll_call(url: str) -> Optional[int]:
    if not url:
        return None
    patterns = [
        r"roll[_-]?call[_-]?vote.*?[=/](\d+)",
        r"vote[_-]\d+[_-]\d+[_-](\d+)\.xml",
        r"roll(\d+)\.xml",
        r"Record Vote Number:\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
    return None


def normalize_bill_payload(root: ET.Element, source_file: str) -> Dict:
    bill = root.find("./bill")
    if bill is None:
        raise ValueError("Missing <bill> root child")

    titles_parent = bill.find("./titles")
    title_items = children(titles_parent, "./item")
    title = elem_text(title_items[0], "./title") if title_items else ""

    summaries_parent = bill.find("./summaries")
    summary_items = children(summaries_parent, "./summary") or children(
        summaries_parent, "./billSummaries/item"
    )
    latest_summary = summary_items[-1] if summary_items else None

    actions_parent = bill.find("./actions")
    action_items = children(actions_parent, "./item")
    latest_action = action_items[-1] if action_items else None

    sponsors_parent = bill.find("./sponsors")
    sponsor_items = children(sponsors_parent, "./item")
    sponsor = sponsor_items[0] if sponsor_items else None

    policy_area = elem_text(bill.find("./policyArea"), "./name")

    subject_names = []
    subjects_parent = bill.find("./subjects")
    for item in children(subjects_parent, "./legislativeSubjects/item") + children(
        subjects_parent, "./policyArea"
    ):
        name = elem_text(item, "./name")
        if name:
            subject_names.append(name)

    return {
        "congress": int(elem_text(bill, "./congress", "0") or 0),
        "bill_type": first_text(bill, "./billType", "./type").lower(),
        "bill_number": first_text(bill, "./billNumber", "./number"),
        "title": title,
        "introduced_date": parse_date(elem_text(bill, "./introducedDate")),
        "latest_action": elem_text(latest_action, "./text"),
        "latest_action_date": parse_date(elem_text(latest_action, "./actionDate")),
        "sponsor_bioguide_id": elem_text(sponsor, "./bioguideId"),
        "sponsor_name": elem_text(sponsor, "./fullName"),
        "sponsor_party": elem_text(sponsor, "./party"),
        "sponsor_state": elem_text(sponsor, "./state"),
        "policy_area": policy_area,
        "subjects": ", ".join(dict.fromkeys(subject_names)),
        "summary": elem_text(latest_summary, "./text"),
        "raw_data": ET.tostring(root, encoding="unicode"),
        "source_file": source_file,
    }


def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS congress_bill_titles (
            id BIGSERIAL PRIMARY KEY,
            bill_id BIGINT NOT NULL REFERENCES congress_bills(id) ON DELETE CASCADE,
            title_type TEXT,
            parent_title_type TEXT,
            title TEXT NOT NULL,
            chamber_code TEXT,
            chamber_name TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS congress_bill_summaries (
            id BIGSERIAL PRIMARY KEY,
            bill_id BIGINT NOT NULL REFERENCES congress_bills(id) ON DELETE CASCADE,
            version_code TEXT,
            action_date DATE,
            action_desc TEXT,
            update_date DATE,
            summary_text TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS congress_bill_actions (
            id BIGSERIAL PRIMARY KEY,
            bill_id BIGINT NOT NULL REFERENCES congress_bills(id) ON DELETE CASCADE,
            action_date DATE,
            action_time TEXT,
            action_code TEXT,
            action_type TEXT,
            action_text TEXT,
            source_system_code TEXT,
            source_system_name TEXT,
            committees_json JSONB,
            links_json JSONB,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS congress_bill_cosponsors (
            id BIGSERIAL PRIMARY KEY,
            bill_id BIGINT NOT NULL REFERENCES congress_bills(id) ON DELETE CASCADE,
            bioguide_id TEXT,
            full_name TEXT,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            party TEXT,
            state TEXT,
            district INT,
            sponsorship_date DATE,
            sponsorship_withdrawn_date DATE,
            is_original_cosponsor BOOLEAN,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS congress_bill_related_bills (
            id BIGSERIAL PRIMARY KEY,
            bill_id BIGINT NOT NULL REFERENCES congress_bills(id) ON DELETE CASCADE,
            related_congress INT,
            related_bill_type TEXT,
            related_bill_number TEXT,
            related_title TEXT,
            relationship_details_json JSONB,
            latest_action_date DATE,
            latest_action_text TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS congress_bill_vote_references (
            id BIGSERIAL PRIMARY KEY,
            bill_id BIGINT NOT NULL REFERENCES congress_bills(id) ON DELETE CASCADE,
            action_id BIGINT REFERENCES congress_bill_actions(id) ON DELETE CASCADE,
            chamber TEXT,
            congress INT,
            session INT,
            roll_call_number INT,
            vote_url TEXT NOT NULL,
            vote_name TEXT,
            action_date DATE,
            action_text TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        );

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

        CREATE INDEX IF NOT EXISTS idx_cbt_bill ON congress_bill_titles (bill_id);
        CREATE UNIQUE INDEX IF NOT EXISTS uq_congress_bills_key
            ON congress_bills (congress, bill_type, bill_number);
        CREATE INDEX IF NOT EXISTS idx_cbs_bill ON congress_bill_summaries (bill_id);
        CREATE INDEX IF NOT EXISTS idx_cba_bill ON congress_bill_actions (bill_id);
        CREATE INDEX IF NOT EXISTS idx_cba_date ON congress_bill_actions (action_date);
        CREATE INDEX IF NOT EXISTS idx_cbc_bill ON congress_bill_cosponsors (bill_id);
        CREATE INDEX IF NOT EXISTS idx_cbc_bioguide ON congress_bill_cosponsors (bioguide_id);
        CREATE INDEX IF NOT EXISTS idx_cbr_bill ON congress_bill_related_bills (bill_id);
        CREATE INDEX IF NOT EXISTS idx_cbv_bill ON congress_bill_vote_references (bill_id);
        CREATE INDEX IF NOT EXISTS idx_cbv_roll_call ON congress_bill_vote_references (roll_call_number);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_cbt_title
            ON congress_bill_titles (bill_id, COALESCE(title_type, ''), title);
        CREATE UNIQUE INDEX IF NOT EXISTS uq_cbs_summary
            ON congress_bill_summaries (bill_id, COALESCE(version_code, ''), COALESCE(action_date, DATE '1900-01-01'));
        CREATE UNIQUE INDEX IF NOT EXISTS uq_cba_action
            ON congress_bill_actions (bill_id, COALESCE(action_date, DATE '1900-01-01'), COALESCE(action_code, ''), COALESCE(action_text, ''));
        CREATE UNIQUE INDEX IF NOT EXISTS uq_cbc_cosponsor
            ON congress_bill_cosponsors (bill_id, COALESCE(bioguide_id, ''), COALESCE(full_name, ''));
        CREATE UNIQUE INDEX IF NOT EXISTS uq_cbr_related
            ON congress_bill_related_bills (bill_id, related_congress, COALESCE(related_bill_type, ''), COALESCE(related_bill_number, ''));
        CREATE UNIQUE INDEX IF NOT EXISTS uq_cbv_vote
            ON congress_bill_vote_references (bill_id, vote_url);
        """
    )

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables and indexes created/verified")


def upsert_bill(cur, payload: Dict) -> int:
    cur.execute(
        """
        SELECT id FROM congress_bills
        WHERE congress = %s AND bill_type = %s AND bill_number = %s
        """,
        (payload["congress"], payload["bill_type"], payload["bill_number"]),
    )
    row = cur.fetchone()
    if row:
        bill_id = row[0]
        cur.execute(
            """
            UPDATE congress_bills SET
                title = COALESCE(NULLIF(%s, ''), title),
                introduced_date = COALESCE(%s, introduced_date),
                latest_action = COALESCE(NULLIF(%s, ''), latest_action),
                latest_action_date = COALESCE(%s, latest_action_date),
                sponsor_bioguide_id = COALESCE(NULLIF(%s, ''), sponsor_bioguide_id),
                sponsor_name = COALESCE(NULLIF(%s, ''), sponsor_name),
                sponsor_party = COALESCE(NULLIF(%s, ''), sponsor_party),
                sponsor_state = COALESCE(NULLIF(%s, ''), sponsor_state),
                policy_area = COALESCE(NULLIF(%s, ''), policy_area),
                subjects = COALESCE(NULLIF(%s, ''), subjects),
                summary = COALESCE(NULLIF(%s, ''), summary),
                raw_data = %s::jsonb,
                source_file = %s,
                imported_at = NOW()
            WHERE id = %s
            """,
            (
                payload["title"],
                payload["introduced_date"],
                payload["latest_action"],
                payload["latest_action_date"],
                payload["sponsor_bioguide_id"],
                payload["sponsor_name"],
                payload["sponsor_party"],
                payload["sponsor_state"],
                payload["policy_area"],
                payload["subjects"],
                payload["summary"],
                json.dumps({"billstatus_xml": payload["raw_data"]}),
                payload["source_file"],
                bill_id,
            ),
        )
        return bill_id

    cur.execute(
        """
        INSERT INTO congress_bills (
            bill_number, bill_type, congress, title, introduced_date, latest_action,
            latest_action_date, sponsor_bioguide_id, sponsor_name, sponsor_party,
            sponsor_state, committees, policy_area, subjects, summary, url, raw_data, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s)
        RETURNING id
        """,
        (
            payload["bill_number"],
            payload["bill_type"],
            payload["congress"],
            payload["title"],
            payload["introduced_date"],
            payload["latest_action"],
            payload["latest_action_date"],
            payload["sponsor_bioguide_id"],
            payload["sponsor_name"],
            payload["sponsor_party"],
            payload["sponsor_state"],
            "",
            payload["policy_area"],
            payload["subjects"],
            payload["summary"],
            "",
            json.dumps({"billstatus_xml": payload["raw_data"]}),
            payload["source_file"],
        ),
    )
    return cur.fetchone()[0]


def insert_titles(cur, bill_id: int, bill: ET.Element, source_file: str):
    for item in children(bill.find("./titles"), "./item"):
        title = elem_text(item, "./title")
        if not title:
            continue
        cur.execute(
            """
            INSERT INTO congress_bill_titles (bill_id, title_type, parent_title_type, title, chamber_code, chamber_name, source_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                bill_id,
                elem_text(item, "./titleType"),
                elem_text(item, "./parentTitleType"),
                title,
                elem_text(item, "./chamberCode"),
                elem_text(item, "./chamberName"),
                source_file,
            ),
        )


def insert_summaries(cur, bill_id: int, bill: ET.Element, source_file: str):
    summaries_parent = bill.find("./summaries")
    items = children(summaries_parent, "./summary") or children(
        summaries_parent, "./billSummaries/item"
    )
    for item in items:
        summary_text = elem_text(item, "./text")
        if not summary_text:
            continue
        cur.execute(
            """
            INSERT INTO congress_bill_summaries (bill_id, version_code, action_date, action_desc, update_date, summary_text, source_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                bill_id,
                elem_text(item, "./versionCode"),
                parse_date(elem_text(item, "./actionDate")),
                elem_text(item, "./actionDesc"),
                parse_date(elem_text(item, "./updateDate")),
                summary_text,
                source_file,
            ),
        )


def insert_actions_and_votes(cur, bill_id: int, bill: ET.Element, congress: int, source_file: str):
    for item in children(bill.find("./actions"), "./item"):
        committees = []
        for committee in children(item.find("./committees"), "./item") + children(
            item, "./committees/committee"
        ):
            committees.append(
                {
                    "name": elem_text(committee, "./name"),
                    "systemCode": elem_text(committee, "./systemCode"),
                    "activity": elem_text(committee, "./activity"),
                }
            )

        links = []
        for link in children(item.find("./links"), "./link"):
            links.append({"name": elem_text(link, "./name"), "url": elem_text(link, "./url")})

        cur.execute(
            """
            INSERT INTO congress_bill_actions (
                bill_id, action_date, action_time, action_code, action_type, action_text,
                source_system_code, source_system_name, committees_json, links_json, source_file
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s)
            ON CONFLICT DO NOTHING
            RETURNING id
            """,
            (
                bill_id,
                parse_date(elem_text(item, "./actionDate")),
                elem_text(item, "./actionTime"),
                elem_text(item, "./actionCode"),
                elem_text(item, "./type"),
                elem_text(item, "./text"),
                elem_text(item, "./sourceSystem/code"),
                elem_text(item, "./sourceSystem/name"),
                json.dumps(committees),
                json.dumps(links),
                source_file,
            ),
        )
        row = cur.fetchone()
        if row:
            action_id = row[0]
        else:
            cur.execute(
                """
                SELECT id FROM congress_bill_actions
                WHERE bill_id = %s
                  AND COALESCE(action_date, DATE '1900-01-01') = COALESCE(%s, DATE '1900-01-01')
                  AND COALESCE(action_code, '') = COALESCE(%s, '')
                  AND COALESCE(action_text, '') = COALESCE(%s, '')
                """,
                (
                    bill_id,
                    parse_date(elem_text(item, "./actionDate")),
                    elem_text(item, "./actionCode"),
                    elem_text(item, "./text"),
                ),
            )
            match = cur.fetchone()
            action_id = match[0] if match else None

        for link in links:
            url = link.get("url", "")
            name = link.get("name", "")
            if not url:
                continue
            if (
                any(token in url.lower() for token in ["roll", "vote"])
                or "Record Vote Number" in name
            ):
                chamber = (
                    "House"
                    if "house" in url.lower() or "clerk.house.gov" in url.lower()
                    else ("Senate" if "senate" in url.lower() else "")
                )
                cur.execute(
                    """
                    INSERT INTO congress_bill_vote_references (
                        bill_id, action_id, chamber, congress, session, roll_call_number,
                        vote_url, vote_name, action_date, action_text, source_file
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (
                        bill_id,
                        action_id,
                        chamber,
                        congress,
                        None,
                        extract_roll_call(url) or extract_roll_call(name),
                        url,
                        name,
                        parse_date(elem_text(item, "./actionDate")),
                        elem_text(item, "./text"),
                        source_file,
                    ),
                )

        for vote in children(item.find("./recordedVotes"), "./recordedVote"):
            vote_url = elem_text(vote, "./url")
            if not vote_url:
                continue
            cur.execute(
                """
                INSERT INTO congress_bill_vote_references (
                    bill_id, action_id, chamber, congress, session, roll_call_number,
                    vote_url, vote_name, action_date, action_text, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    bill_id,
                    action_id,
                    elem_text(vote, "./chamber"),
                    int(first_text(vote, "./congress", default=str(congress)) or congress),
                    int(elem_text(vote, "./sessionNumber", "0") or 0) or None,
                    int(elem_text(vote, "./rollNumber", "0") or 0) or extract_roll_call(vote_url),
                    vote_url,
                    "Recorded Vote",
                    parse_date(elem_text(vote, "./date")),
                    elem_text(item, "./text"),
                    source_file,
                ),
            )


def insert_cosponsors(cur, bill_id: int, bill: ET.Element, source_file: str):
    for item in children(bill.find("./cosponsors"), "./item"):
        cur.execute(
            """
            INSERT INTO congress_bill_cosponsors (
                bill_id, bioguide_id, full_name, first_name, middle_name, last_name, party,
                state, district, sponsorship_date, sponsorship_withdrawn_date,
                is_original_cosponsor, source_file
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULLIF(%s, '')::int, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                bill_id,
                elem_text(item, "./bioguideId"),
                elem_text(item, "./fullName"),
                elem_text(item, "./firstName"),
                elem_text(item, "./middleName"),
                elem_text(item, "./lastName"),
                elem_text(item, "./party"),
                elem_text(item, "./state"),
                elem_text(item, "./district"),
                parse_date(elem_text(item, "./sponsorshipDate")),
                parse_date(elem_text(item, "./sponsorshipWithdrawnDate")),
                elem_text(item, "./isOriginalCosponsor").lower() == "true",
                source_file,
            ),
        )


def insert_related_bills(cur, bill_id: int, bill: ET.Element, source_file: str):
    for item in children(bill.find("./relatedBills"), "./item"):
        details = []
        for rel in children(item.find("./relationshipDetails"), "./item") + children(
            item.find("./relationshipDetails"), "./relationshipDetail"
        ):
            details.append(
                {
                    "type": elem_text(rel, "./type"),
                    "identifiedBy": elem_text(rel, "./identifiedBy"),
                }
            )
        cur.execute(
            """
            INSERT INTO congress_bill_related_bills (
                bill_id, related_congress, related_bill_type, related_bill_number, related_title,
                relationship_details_json, latest_action_date, latest_action_text, source_file
            ) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                bill_id,
                int(elem_text(item, "./congress", "0") or 0),
                elem_text(item, "./type"),
                elem_text(item, "./number"),
                elem_text(item, "./title"),
                json.dumps(details),
                parse_date(elem_text(item, "./latestAction/actionDate")),
                elem_text(item, "./latestAction/text"),
                source_file,
            ),
        )


def iter_xml_from_zip(zip_path: Path):
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if not member.endswith(".xml"):
                continue
            with archive.open(member) as handle:
                try:
                    yield member, ET.parse(handle).getroot()
                except ET.ParseError as exc:
                    logger.warning(f"Skipping malformed XML {member} in {zip_path.name}: {exc}")


def import_zip(zip_path: Path) -> Dict[str, int]:
    stats = {
        "bills": 0,
        "titles": 0,
        "summaries": 0,
        "actions": 0,
        "cosponsors": 0,
        "related_bills": 0,
        "vote_refs": 0,
    }
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        for member_name, root in iter_xml_from_zip(zip_path):
            source_file = f"{zip_path}:{member_name}"
            payload = normalize_bill_payload(root, source_file)
            if not payload["bill_type"] or not payload["bill_number"]:
                raise ValueError(f"Missing bill identity fields in {source_file}")
            bill_id = upsert_bill(cur, payload)
            stats["bills"] += 1

            bill = root.find("./bill")
            if bill is None:
                continue

            insert_titles(cur, bill_id, bill, source_file)
            insert_summaries(cur, bill_id, bill, source_file)
            insert_actions_and_votes(cur, bill_id, bill, payload["congress"], source_file)
            insert_cosponsors(cur, bill_id, bill, source_file)
            insert_related_bills(cur, bill_id, bill, source_file)

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
            "SELECT count(*) FROM congress_bill_titles WHERE source_file LIKE %s",
            (f"{zip_path}:%",),
        )
        stats["titles"] = verify_cur.fetchone()[0]
        verify_cur.execute(
            "SELECT count(*) FROM congress_bill_summaries WHERE source_file LIKE %s",
            (f"{zip_path}:%",),
        )
        stats["summaries"] = verify_cur.fetchone()[0]
        verify_cur.execute(
            "SELECT count(*) FROM congress_bill_actions WHERE source_file LIKE %s",
            (f"{zip_path}:%",),
        )
        stats["actions"] = verify_cur.fetchone()[0]
        verify_cur.execute(
            "SELECT count(*) FROM congress_bill_cosponsors WHERE source_file LIKE %s",
            (f"{zip_path}:%",),
        )
        stats["cosponsors"] = verify_cur.fetchone()[0]
        verify_cur.execute(
            "SELECT count(*) FROM congress_bill_related_bills WHERE source_file LIKE %s",
            (f"{zip_path}:%",),
        )
        stats["related_bills"] = verify_cur.fetchone()[0]
        verify_cur.execute(
            "SELECT count(*) FROM congress_bill_vote_references WHERE source_file LIKE %s",
            (f"{zip_path}:%",),
        )
        stats["vote_refs"] = verify_cur.fetchone()[0]
    finally:
        verify_cur.close()
        verify_conn.close()

    return stats


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
            ("BILLSTATUS", str(file_path), status, error_type, error_message, status),
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
                  AND dataset = 'BILLSTATUS'
                  AND status = 'completed'
            )
            """,
            (str(zip_path),),
        )
        tracked = bool(cur.fetchone()[0])
        if tracked:
            return True
        cur.execute(
            "SELECT EXISTS (SELECT 1 FROM congress_bills WHERE source_file LIKE %s LIMIT 1)",
            (f"{zip_path}:%",),
        )
        return bool(cur.fetchone()[0])
    finally:
        cur.close()
        conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-dir", type=Path, default=BASE_DIR)
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--skip-imported", dest="skip_imported", action="store_true")
    parser.add_argument("--no-skip-imported", dest="skip_imported", action="store_false")
    parser.set_defaults(skip_imported=True)
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("GOVINFO BILLSTATUS BULK IMPORT")
    logger.info("=" * 80)
    create_tables()

    zip_files = sorted(args.base_dir.glob("**/*.zip" if args.recursive else "*.zip"))
    if not zip_files:
        logger.warning("No BILLSTATUS ZIP files found")
        return

    totals = {
        "bills": 0,
        "titles": 0,
        "summaries": 0,
        "actions": 0,
        "cosponsors": 0,
        "related_bills": 0,
        "vote_refs": 0,
    }
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
