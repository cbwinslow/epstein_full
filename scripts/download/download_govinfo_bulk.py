#!/usr/bin/env python3
"""
Download official GovInfo bulk-data ZIPs from the GovInfo Bulk Data Repository.

Supports:
- Federal Register yearly ZIPs (FR, 2000+)
- Bill Status ZIPs by congress and bill type (BILLSTATUS, 108+)
- Bill text ZIPs by congress/session/bill type (BILLS, 113+)
- Bill summary ZIPs by congress/bill type (BILLSUM, 113+)

This uses GovInfo's bulkdata/json listings rather than the API package-list endpoints.
"""

import argparse
import concurrent.futures
import hashlib
import json
import logging
import sys
import threading
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

import psycopg2
import requests

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

BASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f"govinfo_bulk_{datetime.now():%Y%m%d_%H%M%S}.log"
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

BULK_JSON_ROOT = "https://www.govinfo.gov/bulkdata/json"
DEFAULT_BILL_TYPES = ["hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", "sres"]
RATE_LIMIT_DELAY = 0.15

_rate_limit_lock = threading.Lock()
_next_request_time = 0.0
_thread_local = threading.local()


def get_session() -> requests.Session:
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        session.headers.update({"Accept": "application/json"})
        _thread_local.session = session
    return session


def throttle():
    global _next_request_time
    with _rate_limit_lock:
        now = time.monotonic()
        if now < _next_request_time:
            time.sleep(_next_request_time - now)
            now = time.monotonic()
        _next_request_time = now + RATE_LIMIT_DELAY


def parse_int_ranges(value: str) -> List[int]:
    values = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            values.update(range(int(start), int(end) + 1))
        else:
            values.add(int(part))
    return sorted(values)


def parse_bill_types(value: str) -> List[str]:
    items = [part.strip().lower() for part in value.split(",") if part.strip()]
    invalid = sorted(set(items) - set(DEFAULT_BILL_TYPES))
    if invalid:
        raise ValueError(f"Unknown bill types: {', '.join(invalid)}")
    return items


def register_script():
    script_path = Path(__file__)
    script_name = script_path.name
    script_content = script_path.read_text()
    script_hash = hashlib.sha256(script_content.encode()).hexdigest()

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO download_scripts
            (script_name, script_path, script_content, script_hash, description, version)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (script_name) DO UPDATE SET
                script_path = EXCLUDED.script_path,
                script_content = EXCLUDED.script_content,
                script_hash = EXCLUDED.script_hash,
                description = EXCLUDED.description,
                version = EXCLUDED.version,
                updated_at = NOW()
            RETURNING id
            """,
            (
                script_name,
                str(script_path),
                script_content,
                script_hash,
                "Download official GovInfo bulk-data ZIPs for FR and BILLSTATUS from govinfo.gov/bulkdata",
                "1.0.0",
            ),
        )
        script_id = cur.fetchone()[0]
        conn.commit()
        logger.info(f"Registered or updated script in database: {script_name} (ID: {script_id})")
        return script_id
    finally:
        cur.close()
        conn.close()


def fetch_listing_json(url: str) -> Dict:
    throttle()
    response = get_session().get(url, timeout=60)
    response.raise_for_status()
    return response.json()


def save_manifest(target_dir: Path, name: str, data: Dict):
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / name).write_text(json.dumps(data, indent=2), encoding="utf-8")


def find_zip_entry(listing: Dict) -> Dict:
    zip_entry = next(
        (
            item
            for item in listing.get("files", [])
            if not item.get("folder") and item.get("fileExtension") == "zip"
        ),
        None,
    )
    if not zip_entry:
        raise RuntimeError("No ZIP entry found in listing")
    return zip_entry


def is_valid_zip(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            archive.testzip()
        return True
    except zipfile.BadZipFile:
        return False
    except OSError:
        return False


def download_file(url: str, destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        if destination.suffix.lower() == ".zip" and not is_valid_zip(destination):
            logger.warning(f"  Existing ZIP is corrupt; re-downloading: {destination}")
            destination.unlink()
        else:
            logger.info(f"  Skipping existing file: {destination}")
            return destination.stat().st_size

    throttle()
    temp_path = destination.with_suffix(destination.suffix + ".part")
    if temp_path.exists():
        temp_path.unlink()

    with get_session().get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with temp_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)

    temp_path.replace(destination)

    if destination.suffix.lower() == ".zip" and not is_valid_zip(destination):
        destination.unlink(missing_ok=True)
        raise zipfile.BadZipFile(f"Downloaded corrupt ZIP: {destination}")

    size = destination.stat().st_size
    logger.info(f"  Downloaded {destination.name} ({size:,} bytes)")
    return size


def download_fr_year(year: int) -> Dict:
    listing_url = f"{BULK_JSON_ROOT}/FR/{year}"
    listing = fetch_listing_json(listing_url)
    year_dir = BASE_DIR / "fr" / str(year)
    save_manifest(year_dir, f"FR_{year}_listing.json", listing)

    zip_entry = find_zip_entry(listing)
    zip_path = year_dir / zip_entry["name"]
    size = download_file(zip_entry["link"], zip_path)
    return {"kind": "FR", "year": year, "file": zip_path.name, "bytes": size}


def download_billstatus_congress(congress: int, bill_types: Iterable[str]) -> Dict:
    congress_listing_url = f"{BULK_JSON_ROOT}/BILLSTATUS/{congress}"
    congress_listing = fetch_listing_json(congress_listing_url)
    congress_dir = BASE_DIR / "billstatus" / str(congress)
    save_manifest(congress_dir, f"BILLSTATUS_{congress}_listing.json", congress_listing)

    available = {
        item["name"]: item for item in congress_listing.get("files", []) if item.get("folder")
    }
    results = []
    total_bytes = 0

    for bill_type in bill_types:
        if bill_type not in available:
            logger.warning(f"  Skipping unavailable bill type {bill_type} for Congress {congress}")
            continue

        type_listing_url = available[bill_type]["link"]
        type_listing = fetch_listing_json(type_listing_url)
        type_dir = congress_dir / bill_type
        save_manifest(type_dir, f"BILLSTATUS_{congress}_{bill_type}_listing.json", type_listing)

        try:
            zip_entry = find_zip_entry(type_listing)
        except RuntimeError:
            logger.warning(
                f"  No ZIP found for Congress {congress} {bill_type}; leaving manifest only"
            )
            continue

        zip_path = type_dir / zip_entry["name"]
        size = download_file(zip_entry["link"], zip_path)
        total_bytes += size
        results.append(zip_path.name)

    return {"kind": "BILLSTATUS", "congress": congress, "files": results, "bytes": total_bytes}


def download_bills_congress(congress: int, bill_types: Iterable[str]) -> Dict:
    congress_listing_url = f"{BULK_JSON_ROOT}/BILLS/{congress}"
    congress_listing = fetch_listing_json(congress_listing_url)
    congress_dir = BASE_DIR / "bills" / str(congress)
    save_manifest(congress_dir, f"BILLS_{congress}_listing.json", congress_listing)

    sessions = {
        item["name"]: item for item in congress_listing.get("files", []) if item.get("folder")
    }
    results = []
    total_bytes = 0

    for session_name in sorted(sessions):
        session_listing = fetch_listing_json(sessions[session_name]["link"])
        session_dir = congress_dir / session_name
        save_manifest(session_dir, f"BILLS_{congress}_{session_name}_listing.json", session_listing)
        available = {
            item["name"]: item for item in session_listing.get("files", []) if item.get("folder")
        }

        for bill_type in bill_types:
            if bill_type not in available:
                logger.warning(
                    f"  Skipping unavailable BILLS type {bill_type} for Congress {congress} session {session_name}"
                )
                continue

            type_listing = fetch_listing_json(available[bill_type]["link"])
            type_dir = session_dir / bill_type
            save_manifest(
                type_dir, f"BILLS_{congress}_{session_name}_{bill_type}_listing.json", type_listing
            )

            try:
                zip_entry = find_zip_entry(type_listing)
            except RuntimeError:
                logger.warning(
                    f"  No BILLS ZIP found for Congress {congress} session {session_name} {bill_type}"
                )
                continue

            zip_path = type_dir / zip_entry["name"]
            size = download_file(zip_entry["link"], zip_path)
            total_bytes += size
            results.append(zip_path.name)

    return {"kind": "BILLS", "congress": congress, "files": results, "bytes": total_bytes}


def download_billsum_congress(congress: int, bill_types: Iterable[str]) -> Dict:
    congress_listing_url = f"{BULK_JSON_ROOT}/BILLSUM/{congress}"
    congress_listing = fetch_listing_json(congress_listing_url)
    congress_dir = BASE_DIR / "billsum" / str(congress)
    save_manifest(congress_dir, f"BILLSUM_{congress}_listing.json", congress_listing)

    available = {
        item["name"]: item for item in congress_listing.get("files", []) if item.get("folder")
    }
    results = []
    total_bytes = 0

    for bill_type in bill_types:
        if bill_type not in available:
            logger.warning(
                f"  Skipping unavailable BILLSUM type {bill_type} for Congress {congress}"
            )
            continue

        type_listing = fetch_listing_json(available[bill_type]["link"])
        type_dir = congress_dir / bill_type
        save_manifest(type_dir, f"BILLSUM_{congress}_{bill_type}_listing.json", type_listing)

        try:
            zip_entry = find_zip_entry(type_listing)
        except RuntimeError:
            logger.warning(f"  No BILLSUM ZIP found for Congress {congress} {bill_type}")
            continue

        zip_path = type_dir / zip_entry["name"]
        size = download_file(zip_entry["link"], zip_path)
        total_bytes += size
        results.append(zip_path.name)

    return {"kind": "BILLSUM", "congress": congress, "files": results, "bytes": total_bytes}


def download_votes_congress(congress: int) -> Dict:
    congress_listing_url = f"{BULK_JSON_ROOT}/VOTES/{congress}"
    try:
        congress_listing = fetch_listing_json(congress_listing_url)
    except Exception as e:
        logger.warning(f"  Votes not available for Congress {congress}: {e}")
        return {"kind": "VOTES", "congress": congress, "files": [], "bytes": 0}

    congress_dir = BASE_DIR / "votes" / str(congress)
    save_manifest(congress_dir, f"VOTES_{congress}_listing.json", congress_listing)

    chambers = {
        item["name"]: item for item in congress_listing.get("files", []) if item.get("folder")
    }
    results = []
    total_bytes = 0

    for chamber_name in sorted(chambers):
        chamber_listing = fetch_listing_json(chambers[chamber_name]["link"])
        chamber_dir = congress_dir / chamber_name
        save_manifest(chamber_dir, f"VOTES_{congress}_{chamber_name}_listing.json", chamber_listing)

        try:
            zip_entry = find_zip_entry(chamber_listing)
        except RuntimeError:
            logger.warning(f"  No VOTES ZIP found for Congress {congress} {chamber_name}")
            continue

        zip_path = chamber_dir / zip_entry["name"]
        size = download_file(zip_entry["link"], zip_path)
        total_bytes += size
        results.append(zip_path.name)

    return {"kind": "VOTES", "congress": congress, "files": results, "bytes": total_bytes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        choices=["fr", "billstatus", "bills", "billsum", "votes", "all"],
        default="all",
        help="Which GovInfo bulk dataset to download",
    )
    parser.add_argument("--years", default="2000-2024", help="FR years, e.g. 2004 or 2004-2005")
    parser.add_argument(
        "--congresses", default="108-118", help="Congress range for BILLSTATUS/BILLS/BILLSUM/VOTES"
    )
    parser.add_argument(
        "--bill-types",
        default=",".join(DEFAULT_BILL_TYPES),
        help="Comma-separated bill types for BILLSTATUS/BILLS/BILLSUM",
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Parallel download workers across congresses/years"
    )
    args = parser.parse_args()

    register_script()

    results = []
    start_time = datetime.now()
    bill_types = parse_bill_types(args.bill_types)
    congresses = parse_int_ranges(args.congresses)
    jobs = []

    if args.dataset in {"fr", "all"}:
        for year in parse_int_ranges(args.years):
            logger.info(f"Queueing GovInfo FR bulk ZIP for {year}...")
            jobs.append(("FR", year, lambda year=year: download_fr_year(year)))

    if args.dataset in {"billstatus", "all"}:
        for congress in congresses:
            logger.info(f"Queueing GovInfo BILLSTATUS bulk ZIPs for Congress {congress}...")
            jobs.append(
                (
                    "BILLSTATUS",
                    congress,
                    lambda congress=congress: download_billstatus_congress(congress, bill_types),
                )
            )

    if args.dataset in {"bills", "all"}:
        for congress in [c for c in congresses if c >= 113]:
            logger.info(f"Queueing GovInfo BILLS bulk ZIPs for Congress {congress}...")
            jobs.append(
                (
                    "BILLS",
                    congress,
                    lambda congress=congress: download_bills_congress(congress, bill_types),
                )
            )

    if args.dataset in {"billsum", "all"}:
        for congress in [c for c in congresses if c >= 113]:
            logger.info(f"Queueing GovInfo BILLSUM bulk ZIPs for Congress {congress}...")
            jobs.append(
                (
                    "BILLSUM",
                    congress,
                    lambda congress=congress: download_billsum_congress(congress, bill_types),
                )
            )

    if args.dataset in {"votes", "all"}:
        for congress in congresses:
            logger.info(f"Queueing GovInfo VOTES bulk ZIPs for Congress {congress}...")
            jobs.append(
                (
                    "VOTES",
                    congress,
                    lambda congress=congress: download_votes_congress(congress),
                )
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        future_to_job = {executor.submit(job_fn): (kind, value) for kind, value, job_fn in jobs}
        for future in concurrent.futures.as_completed(future_to_job):
            kind, value = future_to_job[future]
            try:
                result = future.result()
                results.append(result)
                logger.info(f"Completed {kind} {value}: {result}")
            except Exception as exc:
                logger.exception(f"Failed {kind} {value}: {exc}")

    duration = (datetime.now() - start_time).total_seconds()
    total_bytes = sum(item.get("bytes", 0) for item in results)

    logger.info("=" * 80)
    logger.info("GOVINFO BULK DOWNLOAD COMPLETE")
    logger.info("=" * 80)
    for item in results:
        logger.info(item)
    logger.info(f"Total downloaded bytes: {total_bytes:,}")
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info(f"Log file: {log_file}")


if __name__ == "__main__":
    main()
