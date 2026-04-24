#!/usr/bin/env python3
"""
Import Congress.gov data to PostgreSQL
Source: api.congress.gov
Tables: congress_members, congress_bills, congress_house_votes
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import psycopg2

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_congress_{datetime.now():%Y%m%d_%H%M%S}.log"
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

    # Congress members table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS congress_members (
            id SERIAL PRIMARY KEY,
            bioguide_id TEXT UNIQUE,
            member_name TEXT,
            first_name TEXT,
            last_name TEXT,
            state TEXT,
            party TEXT,
            chamber TEXT,
            congress_number INT,
            district INT,
            title TEXT,
            depiction_image_url TEXT,
            website TEXT,
            office_address TEXT,
            phone TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)

    # Congress bills table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS congress_bills (
            id SERIAL PRIMARY KEY,
            bill_number TEXT,
            bill_type TEXT,
            congress INT,
            title TEXT,
            introduced_date DATE,
            latest_action TEXT,
            latest_action_date DATE,
            sponsor_bioguide_id TEXT,
            sponsor_name TEXT,
            sponsor_party TEXT,
            sponsor_state TEXT,
            committees TEXT,
            policy_area TEXT,
            subjects TEXT,
            summary TEXT,
            url TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS congress_house_votes (
            id SERIAL PRIMARY KEY,
            identifier BIGINT UNIQUE,
            congress INT,
            session_number INT,
            roll_call_number INT,
            vote_type TEXT,
            result TEXT,
            legislation_type TEXT,
            legislation_number TEXT,
            legislation_url TEXT,
            amendment_type TEXT,
            amendment_number TEXT,
            amendment_author TEXT,
            source_data_url TEXT,
            api_url TEXT,
            start_date TIMESTAMPTZ,
            update_date TIMESTAMPTZ,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)

    # Create indexes
    cur.execute("""
        ALTER TABLE congress_members DROP CONSTRAINT IF EXISTS congress_members_bioguide_id_key;
        CREATE INDEX IF NOT EXISTS idx_cm_name ON congress_members (last_name);
        CREATE INDEX IF NOT EXISTS idx_cm_state ON congress_members (state);
        CREATE INDEX IF NOT EXISTS idx_cm_party ON congress_members (party);
        CREATE INDEX IF NOT EXISTS idx_cm_congress ON congress_members (congress_number);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_cm_bioguide_congress
            ON congress_members (bioguide_id, congress_number);

        CREATE INDEX IF NOT EXISTS idx_cb_type ON congress_bills (bill_type);
        CREATE INDEX IF NOT EXISTS idx_cb_congress ON congress_bills (congress);
        CREATE INDEX IF NOT EXISTS idx_cb_date ON congress_bills (introduced_date);
        CREATE INDEX IF NOT EXISTS idx_cb_sponsor ON congress_bills (sponsor_bioguide_id);
        CREATE INDEX IF NOT EXISTS idx_cb_bill_key ON congress_bills (congress, bill_type, bill_number);

        CREATE INDEX IF NOT EXISTS idx_chv_congress ON congress_house_votes (congress);
        CREATE INDEX IF NOT EXISTS idx_chv_roll_call ON congress_house_votes (roll_call_number);
        CREATE INDEX IF NOT EXISTS idx_chv_session ON congress_house_votes (session_number);
    """)

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables created/verified")


def payload_records(data, key: str) -> List[Dict]:
    """Return records from either a wrapped API payload or a raw list file."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get(key, [])
    return []


def infer_congress_number(filepath: Path, record: Dict) -> int:
    """Infer congress number from record data or the historical folder path."""
    if record.get("congress"):
        try:
            return int(record["congress"])
        except (TypeError, ValueError):
            pass
    for part in [filepath.stem, *filepath.parts]:
        digits = "".join(ch for ch in part if ch.isdigit())
        if digits and 1 <= len(digits) <= 3:
            value = int(digits)
            if 1 <= value <= 200:
                return value
    return 118


def expected_congress_from_path(filepath: Path):
    """Return congress number encoded in a congress_N path, if present."""
    for part in filepath.parts:
        if part.startswith("congress_"):
            try:
                return int(part.split("_", 1)[1])
            except (IndexError, ValueError):
                return None
    return None


def parse_members_file(filepath: Path) -> List[Dict]:
    records = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        members_list = payload_records(data, "members")
        logger.info(f"Found {len(members_list)} members in {filepath.name}")

        skipped_invalid = 0
        for member in members_list:
            if not isinstance(member, dict):
                skipped_invalid += 1
                continue
            # Parse terms safely
            terms = member.get("terms", {})
            if isinstance(terms, dict):
                terms_list = terms.get("item", [])
            elif isinstance(terms, list):
                terms_list = terms
            else:
                terms_list = []

            latest_term = terms_list[-1] if terms_list else {}

            record = {
                "bioguide_id": member.get("bioguideId", ""),
                "member_name": member.get("name", ""),
                "first_name": member.get("firstName", ""),
                "last_name": member.get("lastName", ""),
                "state": member.get("state", ""),
                "party": member.get("partyName", ""),
                "chamber": "House" if member.get("district") else "Senate",
                "congress_number": infer_congress_number(filepath, member),
                "district": member.get("district", 0),
                "title": latest_term.get("memberType", ""),
                "depiction_image_url": member.get("depiction", {}).get("imageUrl", "")
                if member.get("depiction")
                else "",
                "website": member.get("officialWebsiteUrl", ""),
                "office_address": member.get("address", ""),
                "phone": member.get("phoneNumber", ""),
                "raw_data": json.dumps(member),
                "source_file": str(filepath.name),
            }
            records.append(record)
        if skipped_invalid:
            logger.warning(f"Skipped {skipped_invalid} invalid member records in {filepath.name}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {filepath}: {e}")
        logger.error(f"Error at line {e.lineno}, column {e.colno}")
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
        import traceback

        logger.error(traceback.format_exc())

    return records


def parse_bills_file(filepath: Path) -> List[Dict]:
    records = []
    try:
        with open(filepath, "r") as f:
            data = json.load(f)

        expected_congress = expected_congress_from_path(filepath)
        skipped = 0
        skipped_invalid = 0
        for bill in payload_records(data, "bills"):
            if not isinstance(bill, dict):
                skipped_invalid += 1
                continue
            if expected_congress is not None and bill.get("congress") != expected_congress:
                skipped += 1
                continue
            sponsors = bill.get("sponsors") if isinstance(bill.get("sponsors"), list) else []
            sponsor = sponsors[0] if sponsors and isinstance(sponsors[0], dict) else {}
            latest_action = (
                bill.get("latestAction") if isinstance(bill.get("latestAction"), dict) else {}
            )
            policy_area = bill.get("policyArea") if isinstance(bill.get("policyArea"), dict) else {}
            summary = bill.get("summary") if isinstance(bill.get("summary"), dict) else {}
            committees = [
                c.get("name", "") for c in bill.get("committees", []) if isinstance(c, dict)
            ]
            subjects = [s.get("name", "") for s in bill.get("subjects", []) if isinstance(s, dict)]

            record = {
                "bill_number": bill.get("number", ""),
                "bill_type": bill.get("type", ""),
                "congress": bill.get("congress", 118),
                "title": bill.get("title", ""),
                "introduced_date": bill.get("introducedDate") or None,
                "latest_action": latest_action.get("text", ""),
                "latest_action_date": latest_action.get("actionDate") or None,
                "sponsor_bioguide_id": sponsor.get("bioguideId", ""),
                "sponsor_name": sponsor.get("fullName", ""),
                "sponsor_party": sponsor.get("party", ""),
                "sponsor_state": sponsor.get("state", ""),
                "committees": ", ".join(committees),
                "policy_area": policy_area.get("name", ""),
                "subjects": ", ".join(subjects),
                "summary": summary.get("text", ""),
                "url": bill.get("url", ""),
                "raw_data": json.dumps(bill),
                "source_file": str(filepath.name),
            }
            records.append(record)
        if skipped:
            logger.warning(
                f"Skipped {skipped} bills in {filepath.name} that did not match congress {expected_congress}"
            )
        if skipped_invalid:
            logger.warning(f"Skipped {skipped_invalid} invalid bill records in {filepath.name}")
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")

    return records


def parse_house_votes_file(filepath: Path) -> List[Dict]:
    records = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        votes = payload_records(data, "houseRollCallVotes")
        skipped_invalid = 0
        for vote in votes:
            if not isinstance(vote, dict):
                skipped_invalid += 1
                continue

            record = {
                "identifier": vote.get("identifier"),
                "congress": vote.get("congress") or infer_congress_number(filepath, vote),
                "session_number": vote.get("sessionNumber"),
                "roll_call_number": vote.get("rollCallNumber"),
                "vote_type": vote.get("voteType", ""),
                "result": vote.get("result", ""),
                "legislation_type": vote.get("legislationType", ""),
                "legislation_number": vote.get("legislationNumber", ""),
                "legislation_url": vote.get("legislationUrl", ""),
                "amendment_type": vote.get("amendmentType", ""),
                "amendment_number": vote.get("amendmentNumber", ""),
                "amendment_author": vote.get("amendmentAuthor", ""),
                "source_data_url": vote.get("sourceDataURL", ""),
                "api_url": vote.get("url", ""),
                "start_date": vote.get("startDate") or None,
                "update_date": vote.get("updateDate") or None,
                "raw_data": json.dumps(vote),
                "source_file": str(filepath.name),
            }
            records.append(record)

        if skipped_invalid:
            logger.warning(f"Skipped {skipped_invalid} invalid vote records in {filepath.name}")
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")

    return records


def import_members(records: List[Dict]) -> int:
    if not records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()

    inserted = 0
    for r in records:
        try:
            cur.execute(
                """
                INSERT INTO congress_members (
                    bioguide_id, member_name, first_name, last_name, state, party,
                    chamber, congress_number, district, title, depiction_image_url,
                    website, office_address, phone, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (bioguide_id, congress_number) DO UPDATE SET
                    member_name = EXCLUDED.member_name,
                    state = EXCLUDED.state,
                    party = EXCLUDED.party,
                    chamber = EXCLUDED.chamber,
                    district = EXCLUDED.district,
                    raw_data = EXCLUDED.raw_data,
                    imported_at = NOW()
            """,
                (
                    r["bioguide_id"],
                    r["member_name"],
                    r["first_name"],
                    r["last_name"],
                    r["state"],
                    r["party"],
                    r["chamber"],
                    r["congress_number"],
                    r["district"],
                    r["title"],
                    r["depiction_image_url"],
                    r["website"],
                    r["office_address"],
                    r["phone"],
                    r["raw_data"],
                    r["source_file"],
                ),
            )
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")

    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_bills(records: List[Dict]) -> int:
    if not records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()

    inserted = 0
    for r in records:
        try:
            cur.execute(
                """
                INSERT INTO congress_bills (
                    bill_number, bill_type, congress, title, introduced_date,
                    latest_action, latest_action_date, sponsor_bioguide_id, sponsor_name,
                    sponsor_party, sponsor_state, committees, policy_area, subjects,
                    summary, url, raw_data, source_file
                )
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM congress_bills
                    WHERE congress = %s AND bill_type = %s AND bill_number = %s
                )
            """,
                (
                    r["bill_number"],
                    r["bill_type"],
                    r["congress"],
                    r["title"],
                    r["introduced_date"],
                    r["latest_action"],
                    r["latest_action_date"],
                    r["sponsor_bioguide_id"],
                    r["sponsor_name"],
                    r["sponsor_party"],
                    r["sponsor_state"],
                    r["committees"],
                    r["policy_area"],
                    r["subjects"],
                    r["summary"],
                    r["url"],
                    r["raw_data"],
                    r["source_file"],
                    r["congress"],
                    r["bill_type"],
                    r["bill_number"],
                ),
            )
            inserted += cur.rowcount
        except Exception as e:
            logger.debug(f"Insert failed: {e}")

    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_house_votes(records: List[Dict]) -> int:
    if not records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()

    inserted = 0
    for r in records:
        try:
            cur.execute(
                """
                INSERT INTO congress_house_votes (
                    identifier, congress, session_number, roll_call_number, vote_type, result,
                    legislation_type, legislation_number, legislation_url, amendment_type,
                    amendment_number, amendment_author, source_data_url, api_url, start_date,
                    update_date, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (identifier) DO UPDATE SET
                    result = EXCLUDED.result,
                    vote_type = EXCLUDED.vote_type,
                    legislation_type = EXCLUDED.legislation_type,
                    legislation_number = EXCLUDED.legislation_number,
                    legislation_url = EXCLUDED.legislation_url,
                    amendment_type = EXCLUDED.amendment_type,
                    amendment_number = EXCLUDED.amendment_number,
                    amendment_author = EXCLUDED.amendment_author,
                    source_data_url = EXCLUDED.source_data_url,
                    api_url = EXCLUDED.api_url,
                    start_date = EXCLUDED.start_date,
                    update_date = EXCLUDED.update_date,
                    raw_data = EXCLUDED.raw_data,
                    source_file = EXCLUDED.source_file,
                    imported_at = NOW()
            """,
                (
                    r["identifier"],
                    r["congress"],
                    r["session_number"],
                    r["roll_call_number"],
                    r["vote_type"],
                    r["result"],
                    r["legislation_type"],
                    r["legislation_number"],
                    r["legislation_url"],
                    r["amendment_type"],
                    r["amendment_number"],
                    r["amendment_author"],
                    r["source_data_url"],
                    r["api_url"],
                    r["start_date"],
                    r["update_date"],
                    r["raw_data"],
                    r["source_file"],
                ),
            )
            inserted += 1
        except Exception as e:
            logger.debug(f"Vote insert failed: {e}")

    conn.commit()
    cur.close()
    conn.close()
    return inserted


def update_inventory(member_count: int, bill_count: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE data_inventory SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'Congress.gov Members & Votes'
    """,
        (member_count,),
    )

    cur.execute(
        """
        UPDATE data_inventory SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'Congress.gov Bills & Legislation'
    """,
        (bill_count,),
    )

    conn.commit()
    cur.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-dir", type=Path, default=BASE_DIR, help="Directory containing Congress JSON files"
    )
    parser.add_argument("--recursive", action="store_true", help="Scan JSON files recursively")
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("CONGRESS.GOV IMPORT")
    logger.info("=" * 80)

    create_tables()

    json_files = sorted(args.base_dir.glob("**/*.json" if args.recursive else "*.json"))
    if not args.recursive:
        json_files += sorted((args.base_dir / "bills").glob("*.json"))
    if not json_files:
        logger.warning("No JSON files found")
        return

    logger.info(f"Found {len(json_files)} JSON files")

    total_members = 0
    total_bills = 0
    total_house_votes = 0

    for json_file in json_files:
        logger.info(f"Processing {json_file.name}...")

        if "members" in json_file.name:
            records = parse_members_file(json_file)
            if records:
                imported = import_members(records)
                total_members += imported
                logger.info(f"  Imported {imported} members")

        elif "house_votes" in json_file.name:
            records = parse_house_votes_file(json_file)
            if records:
                imported = import_house_votes(records)
                total_house_votes += imported
                logger.info(f"  Imported {imported} House votes")

        elif "bills" in json_file.name:
            records = parse_bills_file(json_file)
            if records:
                imported = import_bills(records)
                total_bills += imported
                logger.info(f"  Imported {imported} bills")

    update_inventory(total_members, total_bills)

    logger.info("=" * 80)
    logger.info(
        f"IMPORT COMPLETE: {total_members} members, {total_bills} bills, {total_house_votes} House votes"
    )
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
