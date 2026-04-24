#!/usr/bin/env python3
"""
Downloads individual House roll call vote detail records including member votes.
Endpoint: /house-vote/{congress}/{session}/{roll-number}
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import aiohttp
import psycopg2
import requests

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress_historical/")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"house_vote_details_{datetime.now():%Y%m%d_%H%M%S}.log"
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

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS congress_house_vote_details (
            id SERIAL PRIMARY KEY,
            congress INTEGER NOT NULL,
            roll_call_number INTEGER NOT NULL,
            session INTEGER NOT NULL,
            vote_date DATE NOT NULL,
            bill_id TEXT,
            description TEXT,
            vote_result TEXT,
            yea_count INTEGER,
            nay_count INTEGER,
            present_count INTEGER,
            not_voting_count INTEGER,
            raw_data JSONB,
            downloaded_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(congress, session, roll_call_number)
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS congress_house_member_votes (
            id SERIAL PRIMARY KEY,
            congress INTEGER NOT NULL,
            session INTEGER NOT NULL,
            roll_call_number INTEGER NOT NULL,
            bioguide_id TEXT NOT NULL,
            member_name TEXT,
            state TEXT,
            district TEXT,
            party TEXT,
            vote TEXT NOT NULL,
            vote_position INTEGER,
            raw_data JSONB,
            UNIQUE(congress, session, roll_call_number, bioguide_id)
        );
    """
    )

    # Migrate older schema to session-aware uniqueness.
    cur.execute(
        """
        ALTER TABLE congress_house_member_votes
        ADD COLUMN IF NOT EXISTS session INTEGER;
    """
    )
    cur.execute(
        """
        UPDATE congress_house_member_votes m
        SET session = d.session
        FROM congress_house_vote_details d
        WHERE m.session IS NULL
          AND m.congress = d.congress
          AND m.roll_call_number = d.roll_call_number;
    """
    )
    cur.execute(
        """
        ALTER TABLE congress_house_vote_details
        DROP CONSTRAINT IF EXISTS congress_house_vote_details_congress_roll_call_number_key;
    """
    )
    cur.execute(
        """
        ALTER TABLE congress_house_vote_details
        DROP CONSTRAINT IF EXISTS congress_house_vote_details_congress_session_roll_key;
    """
    )
    cur.execute(
        """
        ALTER TABLE congress_house_vote_details
        ADD CONSTRAINT congress_house_vote_details_congress_session_roll_key
        UNIQUE (congress, session, roll_call_number);
    """
    )
    cur.execute(
        """
        ALTER TABLE congress_house_member_votes
        DROP CONSTRAINT IF EXISTS congress_house_member_votes_congress_roll_call_number_bioguide_id_key;
    """
    )
    cur.execute(
        """
        ALTER TABLE congress_house_member_votes
        DROP CONSTRAINT IF EXISTS congress_house_member_votes_congress_roll_call_number_biogu_key;
    """
    )
    cur.execute(
        """
        ALTER TABLE congress_house_member_votes
        DROP CONSTRAINT IF EXISTS congress_house_member_votes_congress_session_roll_bio_key;
    """
    )
    cur.execute(
        """
        ALTER TABLE congress_house_member_votes
        ADD CONSTRAINT congress_house_member_votes_congress_session_roll_bio_key
        UNIQUE (congress, session, roll_call_number, bioguide_id);
    """
    )
    cur.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM congress_house_member_votes
                WHERE session IS NULL
            ) THEN
                ALTER TABLE congress_house_member_votes
                ALTER COLUMN session SET NOT NULL;
            END IF;
        END $$;
    """
    )

    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_chvd_congress_session_roll ON congress_house_vote_details (congress, session, roll_call_number);"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_chmv_bioguide ON congress_house_member_votes (bioguide_id);"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_chmv_congress_session_roll ON congress_house_member_votes (congress, session, roll_call_number);"
    )

    conn.commit()
    cur.close()
    conn.close()


def get_pending_votes(congress_filter: Optional[int] = None):
    conn = get_db_connection()
    cur = conn.cursor()

    sql = """
        SELECT chv.congress, chv.roll_call_number, chv.session_number, chv.start_date
        FROM congress_house_votes chv
        LEFT JOIN congress_house_vote_details chvd
            ON chv.congress = chvd.congress
           AND chv.session_number = chvd.session
           AND chv.roll_call_number = chvd.roll_call_number
        WHERE chvd.id IS NULL
    """
    params = []
    if congress_filter is not None:
        sql += " AND chv.congress = %s"
        params.append(congress_filter)

    sql += " ORDER BY chv.congress DESC, chv.roll_call_number DESC"
    cur.execute(sql, params)

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _extract_vote_detail_payload(data: Dict) -> Dict:
    """Support both legacy and current response keys."""
    if isinstance(data.get("houseRollCallVote"), dict):
        return data["houseRollCallVote"]
    if isinstance(data.get("houseVote"), dict):
        return data["houseVote"]
    return {}


def _sum_vote_party_total(vote_party_total: List[Dict], key: str) -> int:
    total = 0
    for row in vote_party_total or []:
        total += _safe_int(row.get(key)) or 0
    return total


def _parse_house_vote_xml(source_url: str) -> List[Dict]:
    """Fetch and parse House Clerk XML recorded-vote entries."""
    if not source_url:
        return []

    try:
        resp = requests.get(source_url, timeout=30)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
    except Exception:
        return []

    vote_data = root.find("vote-data")
    if vote_data is None:
        return []

    rows: List[Dict] = []
    for rec in vote_data.findall("recorded-vote"):
        legislator = rec.find("legislator")
        vote_text = rec.findtext("vote")
        if legislator is None:
            continue
        rows.append(
            {
                "bioguide_id": legislator.attrib.get("name-id"),
                "member_name": legislator.attrib.get("unaccented-name")
                or legislator.attrib.get("sort-field"),
                "state": legislator.attrib.get("state"),
                "district": legislator.attrib.get("district"),
                "party": legislator.attrib.get("party"),
                "vote": vote_text,
            }
        )
    return rows


async def fetch_vote_detail(
    session: aiohttp.ClientSession,
    congress: int,
    session_number: int,
    roll_call: int,
    expected_vote_date: Optional[str],
    semaphore: asyncio.Semaphore,
):
    url = f"https://api.congress.gov/v3/house-vote/{congress}/{session_number}/{roll_call}?format=json"

    async with semaphore:
        try:
            async with session.get(url, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return congress, session_number, roll_call, expected_vote_date, data, None
                return (
                    congress,
                    session_number,
                    roll_call,
                    expected_vote_date,
                    None,
                    f"HTTP {resp.status}",
                )
        except Exception as e:
            return congress, session_number, roll_call, expected_vote_date, None, str(e)


def import_vote_detail(
    congress: int,
    roll_call: int,
    expected_session: int,
    expected_vote_date: Optional[str],
    data: Dict,
):
    conn = get_db_connection()
    cur = conn.cursor()

    vote = _extract_vote_detail_payload(data)
    session_num = _safe_int(vote.get("sessionNumber")) or expected_session
    start_date = vote.get("startDate") or vote.get("voteDate")
    vote_date = start_date[:10] if isinstance(start_date, str) and len(start_date) >= 10 else None
    if vote_date is None:
        vote_date = (
            expected_vote_date[:10]
            if isinstance(expected_vote_date, str) and len(expected_vote_date) >= 10
            else "1900-01-01"
        )
    legislation_type = vote.get("legislationType") or ""
    legislation_number = vote.get("legislationNumber") or ""
    bill_id = (
        f"{legislation_type}{legislation_number}".strip()
        if (legislation_type or legislation_number)
        else None
    )
    vote_result = vote.get("result") or vote.get("voteResult")
    vote_question = vote.get("voteQuestion") or vote.get("voteDescription")
    vote_type = vote.get("voteType") or ""
    description = " - ".join([x for x in [vote_question, vote_type] if x]) or None

    vote_party_total = vote.get("votePartyTotal", [])
    yea_count = _sum_vote_party_total(vote_party_total, "yeaTotal")
    nay_count = _sum_vote_party_total(vote_party_total, "nayTotal")
    present_count = _sum_vote_party_total(vote_party_total, "presentTotal")
    not_voting_count = _sum_vote_party_total(vote_party_total, "notVotingTotal")

    cur.execute(
        """
        INSERT INTO congress_house_vote_details
        (congress, roll_call_number, session, vote_date, bill_id, description, vote_result,
         yea_count, nay_count, present_count, not_voting_count, raw_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (congress, session, roll_call_number) DO NOTHING
    """,
        (
            congress,
            roll_call,
            session_num,
            vote_date,
            bill_id,
            description,
            vote_result,
            yea_count,
            nay_count,
            present_count,
            not_voting_count,
            json.dumps(data),
        ),
    )

    member_votes = _parse_house_vote_xml(vote.get("sourceDataURL", ""))
    if member_votes:
        for pos in member_votes:
            cur.execute(
                """
                INSERT INTO congress_house_member_votes
                (congress, session, roll_call_number, bioguide_id, member_name, state, district, party, vote, vote_position, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (congress, session, roll_call_number, bioguide_id) DO NOTHING
            """,
                (
                    congress,
                    session_num,
                    roll_call,
                    pos.get("bioguide_id"),
                    pos.get("member_name"),
                    pos.get("state"),
                    pos.get("district"),
                    pos.get("party"),
                    pos.get("vote"),
                    None,
                    json.dumps(pos),
                ),
            )

    conn.commit()
    cur.close()
    conn.close()

    return len(member_votes) if member_votes else 0


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--congress", type=int, help="Specific congress number")
    parser.add_argument("--limit", type=int, default=100, help="Batch limit")
    parser.add_argument("--concurrency", type=int, default=5, help="Concurrent downloads")
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("HOUSE VOTE DETAIL DOWNLOADER")
    logger.info("=" * 80)

    create_tables()

    pending = get_pending_votes(args.congress)

    if not pending:
        logger.info("No pending vote details to download")
        return

    logger.info(f"Found {len(pending)} pending vote details")

    if args.limit and len(pending) > args.limit:
        pending = pending[: args.limit]
        logger.info(f"Processing first {args.limit} votes")

    semaphore = asyncio.Semaphore(args.concurrency)
    timeout = aiohttp.ClientTimeout(total=60)
    headers = {"User-Agent": "EpsteinResearchBot/1.0 (+https://github.com/Kilo-Org/kilocode)"}

    congress_api_key = os.getenv("CONGRESS_API_KEY")
    if congress_api_key:
        headers["X-Api-Key"] = congress_api_key

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        tasks = []
        for congress, roll_call, session_number, start_date in pending:
            expected_vote_date = start_date.isoformat() if start_date else None
            tasks.append(
                fetch_vote_detail(
                    session,
                    congress,
                    session_number,
                    roll_call,
                    expected_vote_date,
                    semaphore,
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

    total_members = 0
    successful = 0
    failed = 0

    for res in results:
        if isinstance(res, Exception):
            failed += 1
            logger.error(f"Task error: {res}")
            continue

        congress, session_number, roll_call, expected_vote_date, data, err = res
        if err:
            failed += 1
            logger.warning(f"Vote {congress}-{session_number}-{roll_call} failed: {err}")
            continue

        try:
            count = import_vote_detail(
                congress, roll_call, session_number, expected_vote_date, data
            )
            total_members += count
            successful += 1
            logger.info(f"Imported {congress}-{session_number}-{roll_call}: {count} member votes")
        except Exception as e:
            failed += 1
            logger.error(f"Failed to import {congress}-{session_number}-{roll_call}: {e}")

    logger.info("=" * 80)
    logger.info(f"COMPLETE: {successful} successful, {failed} failed")
    logger.info(f"Total member votes imported: {total_members:,}")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
