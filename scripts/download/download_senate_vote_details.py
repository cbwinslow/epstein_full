#!/usr/bin/env python3
"""
Download and ingest Senate roll-call vote details into PostgreSQL.

Source:
- Vote menus:   https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_{congress}_{session}.xml
- Vote details: https://www.senate.gov/legislative/LIS/roll_call_votes/vote{congress}{session}/vote_{congress}_{session}_{vote:05d}.xml
"""

import argparse
import concurrent.futures
import logging
import re
import sys
import threading
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import psycopg2
import requests
from psycopg2.extras import Json

LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")
RAW_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/senate_votes")

LOG_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f"senate_vote_details_{datetime.now():%Y%m%d_%H%M%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}

_rate_lock = threading.Lock()
_next_request_time = 0.0
RATE_DELAY = 0.03
MAX_RETRIES = 5
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "application/xml,text/xml,*/*;q=0.8",
    "Referer": "https://www.senate.gov/legislative/votes_new.htm",
}


def throttle():
    global _next_request_time
    with _rate_lock:
        now = time.monotonic()
        if now < _next_request_time:
            time.sleep(_next_request_time - now)
            now = time.monotonic()
        _next_request_time = now + RATE_DELAY


def get_with_retry(url: str, timeout: int = 60) -> requests.Response:
    last_exc: Optional[Exception] = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            throttle()
            resp = requests.get(url, timeout=timeout, headers=REQUEST_HEADERS)
            if resp.status_code in (403, 429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                time.sleep(min(2.5, 0.25 * (2 ** (attempt - 1))))
                continue
            return resp
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt < MAX_RETRIES:
                time.sleep(min(2.5, 0.25 * (2 ** (attempt - 1))))
                continue
            raise
    if last_exc:
        raise last_exc
    raise RuntimeError(f"Request failed with no response: {url}")


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def create_tables():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS congress_senate_votes (
            id BIGSERIAL PRIMARY KEY,
            congress INT NOT NULL,
            session INT NOT NULL,
            vote_number INT NOT NULL,
            vote_date_text TEXT,
            modify_date_text TEXT,
            vote_question_text TEXT,
            vote_document_text TEXT,
            vote_result_text TEXT,
            question TEXT,
            vote_title TEXT,
            majority_requirement TEXT,
            vote_result TEXT,
            document_congress INT,
            document_type TEXT,
            document_number TEXT,
            document_name TEXT,
            document_title TEXT,
            yeas INT,
            nays INT,
            present_count INT,
            absent_count INT,
            source_url TEXT,
            raw_data JSONB,
            downloaded_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE (congress, session, vote_number)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS congress_senate_member_votes (
            id BIGSERIAL PRIMARY KEY,
            congress INT NOT NULL,
            session INT NOT NULL,
            vote_number INT NOT NULL,
            lis_member_id TEXT,
            member_name TEXT,
            last_name TEXT,
            party TEXT,
            state TEXT,
            vote_cast TEXT,
            source_url TEXT,
            raw_data JSONB,
            downloaded_at TIMESTAMPTZ DEFAULT NOW(),
            member_key TEXT GENERATED ALWAYS AS (
                COALESCE(NULLIF(lis_member_id, ''), COALESCE(last_name, '') || '|' || COALESCE(state, '') || '|' || COALESCE(member_name, ''))
            ) STORED,
            UNIQUE (congress, session, vote_number, member_key)
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_csv_congress_session_vote
            ON congress_senate_votes (congress, session, vote_number)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_csmv_congress_session_vote
            ON congress_senate_member_votes (congress, session, vote_number)
        """
    )
    conn.commit()
    cur.close()
    conn.close()


def parse_range(value: str) -> List[int]:
    result = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            result.update(range(int(start), int(end) + 1))
        else:
            result.add(int(part))
    return sorted(result)


def parse_vote_num(text: str) -> Optional[int]:
    if not text:
        return None
    m = re.search(r"\d+", text)
    return int(m.group(0)) if m else None


def read_text(el: Optional[ET.Element], tag: str) -> str:
    if el is None:
        return ""
    child = el.find(tag)
    if child is None or child.text is None:
        return ""
    return child.text.strip()


def get_menu_votes(congress: int, session: int) -> List[int]:
    url = (
        f"https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_{congress}_{session}.xml"
    )
    resp = get_with_retry(url, timeout=60)
    if resp.status_code == 404:
        logger.info("No menu for congress=%s session=%s", congress, session)
        return []
    resp.raise_for_status()

    target_dir = RAW_DIR / str(congress) / str(session)
    target_dir.mkdir(parents=True, exist_ok=True)
    menu_path = target_dir / f"vote_menu_{congress}_{session}.xml"
    menu_path.write_text(resp.text, encoding="utf-8")

    root = ET.fromstring(resp.content)
    votes = []
    for vote in root.findall(".//vote"):
        num = parse_vote_num(read_text(vote, "vote_number"))
        if num is not None:
            votes.append(num)
    votes = sorted(set(votes), reverse=True)
    logger.info("Menu congress=%s session=%s votes=%s", congress, session, len(votes))
    return votes


def fetch_vote_xml(
    congress: int, session: int, vote_number: int
) -> Tuple[int, int, int, Optional[bytes], Optional[str], str]:
    url = (
        "https://www.senate.gov/legislative/LIS/roll_call_votes/"
        f"vote{congress}{session}/vote_{congress}_{session}_{vote_number:05d}.xml"
    )
    try:
        resp = get_with_retry(url, timeout=60)
        if resp.status_code == 404:
            return congress, session, vote_number, None, "HTTP 404", url
        resp.raise_for_status()
        return congress, session, vote_number, resp.content, None, url
    except Exception as e:  # noqa: BLE001
        return congress, session, vote_number, None, str(e), url


def _to_int(text: str) -> Optional[int]:
    text = (text or "").strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def upsert_vote_detail(
    conn, congress: int, session: int, vote_number: int, root: ET.Element, source_url: str
):
    cur = conn.cursor()

    document = root.find("document")
    count = root.find("count")
    payload = ET.tostring(root, encoding="unicode")

    cur.execute(
        """
        INSERT INTO congress_senate_votes (
            congress, session, vote_number, vote_date_text, modify_date_text,
            vote_question_text, vote_document_text, vote_result_text, question,
            vote_title, majority_requirement, vote_result,
            document_congress, document_type, document_number, document_name, document_title,
            yeas, nays, present_count, absent_count, source_url, raw_data
        ) VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        ON CONFLICT (congress, session, vote_number) DO UPDATE SET
            vote_date_text = EXCLUDED.vote_date_text,
            modify_date_text = EXCLUDED.modify_date_text,
            vote_question_text = EXCLUDED.vote_question_text,
            vote_document_text = EXCLUDED.vote_document_text,
            vote_result_text = EXCLUDED.vote_result_text,
            question = EXCLUDED.question,
            vote_title = EXCLUDED.vote_title,
            majority_requirement = EXCLUDED.majority_requirement,
            vote_result = EXCLUDED.vote_result,
            document_congress = EXCLUDED.document_congress,
            document_type = EXCLUDED.document_type,
            document_number = EXCLUDED.document_number,
            document_name = EXCLUDED.document_name,
            document_title = EXCLUDED.document_title,
            yeas = EXCLUDED.yeas,
            nays = EXCLUDED.nays,
            present_count = EXCLUDED.present_count,
            absent_count = EXCLUDED.absent_count,
            source_url = EXCLUDED.source_url,
            raw_data = EXCLUDED.raw_data,
            downloaded_at = NOW()
        """,
        (
            congress,
            session,
            vote_number,
            read_text(root, "vote_date"),
            read_text(root, "modify_date"),
            read_text(root, "vote_question_text"),
            read_text(root, "vote_document_text"),
            read_text(root, "vote_result_text"),
            read_text(root, "question"),
            read_text(root, "vote_title"),
            read_text(root, "majority_requirement"),
            read_text(root, "vote_result"),
            _to_int(read_text(document, "document_congress")),
            read_text(document, "document_type"),
            read_text(document, "document_number"),
            read_text(document, "document_name"),
            read_text(document, "document_title"),
            _to_int(read_text(count, "yeas")),
            _to_int(read_text(count, "nays")),
            _to_int(read_text(count, "present")),
            _to_int(read_text(count, "absent")),
            source_url,
            Json({"xml": payload}),
        ),
    )
    cur.close()


def upsert_member_votes(
    conn, congress: int, session: int, vote_number: int, root: ET.Element, source_url: str
) -> int:
    members = root.findall(".//members/member")
    if not members:
        return 0

    cur = conn.cursor()
    inserted = 0
    for m in members:
        first_name = read_text(m, "first_name")
        last_name = read_text(m, "last_name")
        full_name = " ".join(part for part in [first_name, last_name] if part).strip()
        if not full_name:
            full_name = read_text(m, "member_full")
        lis_member_id = read_text(m, "lis_member_id")
        payload = ET.tostring(m, encoding="unicode")

        cur.execute(
            """
            INSERT INTO congress_senate_member_votes (
                congress, session, vote_number, lis_member_id, member_name, last_name,
                party, state, vote_cast, source_url, raw_data
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (congress, session, vote_number, member_key) DO UPDATE SET
                party = EXCLUDED.party,
                state = EXCLUDED.state,
                vote_cast = EXCLUDED.vote_cast,
                source_url = EXCLUDED.source_url,
                raw_data = EXCLUDED.raw_data,
                downloaded_at = NOW()
            """,
            (
                congress,
                session,
                vote_number,
                lis_member_id,
                full_name,
                last_name,
                read_text(m, "party"),
                read_text(m, "state"),
                read_text(m, "vote_cast"),
                source_url,
                Json({"xml": payload}),
            ),
        )
        inserted += 1

    cur.close()
    return inserted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--congresses", default="117-119", help="Congress selector, e.g. 117-119 or 118,119"
    )
    parser.add_argument("--sessions", default="1,2", help="Session selector, e.g. 1,2")
    parser.add_argument(
        "--concurrency", type=int, default=30, help="Parallel vote-detail fetch workers"
    )
    parser.add_argument(
        "--limit", type=int, default=0, help="Optional cap on vote details to process"
    )
    parser.add_argument(
        "--rate-delay", type=float, default=0.03, help="Minimum delay between HTTP requests"
    )
    parser.add_argument(
        "--max-retries", type=int, default=5, help="HTTP retry attempts for transient failures"
    )
    args = parser.parse_args()
    global RATE_DELAY, MAX_RETRIES
    RATE_DELAY = max(0.0, float(args.rate_delay))
    MAX_RETRIES = max(1, int(args.max_retries))

    create_tables()
    congresses = parse_range(args.congresses)
    sessions = parse_range(args.sessions)

    jobs: List[Tuple[int, int, int]] = []
    for congress in congresses:
        for session in sessions:
            try:
                votes = get_menu_votes(congress, session)
            except Exception as e:  # noqa: BLE001
                logger.warning("Failed menu congress=%s session=%s: %s", congress, session, e)
                continue
            for vote_number in votes:
                jobs.append((congress, session, vote_number))

    if args.limit and args.limit > 0:
        jobs = jobs[: args.limit]

    if not jobs:
        logger.info("No Senate vote jobs queued")
        return

    logger.info("Queued Senate vote details: %s", len(jobs))

    success = 0
    failed = 0
    member_rows = 0

    conn = get_conn()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
        futures = [executor.submit(fetch_vote_xml, c, s, v) for c, s, v in jobs]
        for fut in concurrent.futures.as_completed(futures):
            congress, session, vote_number, content, err, source_url = fut.result()
            if err:
                failed += 1
                logger.warning("Failed %s-%s-%s: %s", congress, session, vote_number, err)
                continue
            try:
                root = ET.fromstring(content)
                upsert_vote_detail(conn, congress, session, vote_number, root, source_url)
                count = upsert_member_votes(conn, congress, session, vote_number, root, source_url)
                conn.commit()
                success += 1
                member_rows += count
                logger.info(
                    "Imported Senate vote %s-%s-%s with %s member rows",
                    congress,
                    session,
                    vote_number,
                    count,
                )
            except Exception as e:  # noqa: BLE001
                conn.rollback()
                failed += 1
                logger.error("Import failed %s-%s-%s: %s", congress, session, vote_number, e)

    conn.close()

    logger.info("=" * 80)
    logger.info("SENATE VOTE DETAIL INGEST COMPLETE")
    logger.info("Successful vote rows: %s", success)
    logger.info("Failed vote rows: %s", failed)
    logger.info("Member vote rows processed: %s", member_rows)
    logger.info("Log file: %s", log_file)
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
