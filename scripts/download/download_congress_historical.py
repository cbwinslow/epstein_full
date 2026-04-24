#!/usr/bin/env python3
"""
Download Congress.gov Historical Data (107th-118th Congress, 2001-2024)
Downloads members, bills, and supported vote data for each congress with parallel processing
"""

import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import psycopg2
import requests

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress_historical")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")
IMPORT_SCRIPT = Path(__file__).with_name("import_congress.py")

BASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f"congress_historical_{datetime.now():%Y%m%d_%H%M%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

if not os.environ.get("CONGRESS_API_KEY"):
    secrets_file = Path.home() / "workspace" / "epstein" / ".bash_secrets"
    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                if line.startswith("export "):
                    key_val = line[7:].strip().split("=", 1)
                    if len(key_val) == 2 and key_val[0] not in os.environ:
                        os.environ[key_val[0]] = key_val[1].strip("\"'")

API_KEY = os.environ.get("CONGRESS_API_KEY")
if not API_KEY:
    logger.error("CONGRESS_API_KEY not set in environment")
    sys.exit(1)

base_url = "https://api.congress.gov/v3"
headers = {"X-API-Key": API_KEY}

# Database configuration for script tracking
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}

# Official docs: 5,000 requests/hour and max limit=250
RATE_LIMIT_DELAY = 0.75
PAGE_LIMIT = 250
_rate_limit_lock = threading.Lock()
_next_request_time = 0.0
_thread_local = threading.local()


def parse_congresses(value):
    """Parse congress selector like '107', '107-118', or '107,109,118'."""
    congresses = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            congresses.update(range(int(start), int(end) + 1))
        else:
            congresses.add(int(part))
    return sorted(congresses)


def parse_components(value):
    components = {part.strip().lower() for part in value.split(",") if part.strip()}
    valid = {"bills", "members", "votes"}
    invalid = sorted(components - valid)
    if invalid:
        raise ValueError(f"Unknown components: {', '.join(invalid)}")
    return components or valid


def load_existing_json(path):
    """Load an existing JSON file and return its record list if valid."""
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data.get("bills") or data.get("members") or []
        if isinstance(data, list):
            return data
    except (OSError, json.JSONDecodeError):
        return []
    return []


def get_session():
    """Reuse a requests session per worker thread."""
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        session.headers.update(headers)
        _thread_local.session = session
    return session


def throttle():
    """Apply a global process-wide request rate limit."""
    global _next_request_time
    with _rate_limit_lock:
        now = time.monotonic()
        if now < _next_request_time:
            time.sleep(_next_request_time - now)
            now = time.monotonic()
        _next_request_time = now + RATE_LIMIT_DELAY


def next_offset(current_offset, page_size):
    """Advance the numeric offset for Congress.gov pagination."""
    return current_offset + page_size


def register_script():
    """Register this script in the download_scripts table"""
    script_path = Path(__file__)
    script_name = script_path.name

    # Read script content
    with open(script_path, "r") as f:
        script_content = f.read()

    # Calculate hash
    script_hash = hashlib.sha256(script_content.encode()).hexdigest()

    # Connect to database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        # Check if script already exists
        cur.execute(
            "SELECT id, script_hash FROM download_scripts WHERE script_name = %s", (script_name,)
        )
        result = cur.fetchone()

        if result:
            existing_id, existing_hash = result
            # Check if content changed
            if existing_hash != script_hash:
                # Update script
                cur.execute(
                    """
                    UPDATE download_scripts
                    SET script_content = %s, script_hash = %s,
                        script_path = %s, updated_at = NOW()
                    WHERE id = %s
                """,
                    (script_content, script_hash, str(script_path), existing_id),
                )
                logger.info(f"Updated script in database: {script_name} (content changed)")
            else:
                logger.info(f"Script already registered (no changes): {script_name}")
            conn.commit()
            return existing_id
        else:
            # Insert new script
            cur.execute(
                """
                INSERT INTO download_scripts
                (script_name, script_path, script_content, script_hash, description, version)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
                (
                    script_name,
                    str(script_path),
                    script_content,
                    script_hash,
                    "Download Congress.gov historical data (members, bills, votes) for 107th-118th Congress",
                    "1.0.0",
                ),
            )
            script_id = cur.fetchone()[0]
            logger.info(f"Registered new script in database: {script_name} (ID: {script_id})")
            conn.commit()
            return script_id

    finally:
        cur.close()
        conn.close()


def download_bills_for_congress(congress):
    """Download all bills for a specific congress"""
    congress_dir = BASE_DIR / f"congress_{congress}" / "bills"
    congress_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading bills for Congress {congress}...")

    output_file = congress_dir / f"bills_{congress}.json"
    existing = load_existing_json(output_file)
    if existing and all(
        item.get("congress") == congress for item in existing if isinstance(item, dict)
    ):
        logger.info(
            f"  Skipping Congress {congress} bills; existing file has {len(existing)} records"
        )
        return congress, len(existing)

    offset = 0
    page_count = 0
    total_bills = 0
    bills = []
    max_retries = 3

    while True:
        retry_count = 0
        while retry_count < max_retries:
            try:
                url = f"{base_url}/bill/{congress}?offset={offset}&limit={PAGE_LIMIT}&format=json"
                throttle()
                r = get_session().get(url, timeout=60)
                r.raise_for_status()
                data = r.json()

                page_bills = data.get("bills", [])
                if not page_bills:
                    return congress, len(bills)

                bills.extend(page_bills)
                page_count += 1
                total_bills = data.get("pagination", {}).get("count", len(bills))

                logger.info(
                    f"  Congress {congress} bills: Page {page_count}, {len(page_bills)} bills, total: {len(bills)}/{total_bills}"
                )

                # Check if we have all bills
                if len(bills) >= total_bills:
                    # Save to JSON
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump({"congress": congress, "bills": bills}, f, indent=2)

                    logger.info(
                        f"✅ Downloaded {len(bills)} bills for Congress {congress} to {output_file}"
                    )
                    return congress, len(bills)

                offset = next_offset(offset, PAGE_LIMIT)
                break  # Success, exit retry loop

            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(
                        f"  Retry {retry_count}/{max_retries} for Congress {congress} bills at offset {offset}: {e}"
                    )
                    time.sleep(2**retry_count)  # Exponential backoff
                else:
                    logger.error(
                        f"  Failed to download bills for Congress {congress} at offset {offset} after {max_retries} retries: {e}"
                    )
                    # Save what we have
                    output_file = congress_dir / f"bills_{congress}_partial.json"
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(
                            {"congress": congress, "bills": bills, "partial": True}, f, indent=2
                        )
                    logger.info(f"  Saved partial download: {len(bills)} bills to {output_file}")
                    return congress, len(bills)


def download_members_for_congress(congress):
    """Download all members for a specific congress"""
    congress_dir = BASE_DIR / f"congress_{congress}" / "members"
    congress_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading members for Congress {congress}...")

    output_file = congress_dir / f"members_{congress}.json"
    existing = load_existing_json(output_file)
    if existing:
        logger.info(
            f"  Skipping Congress {congress} members; existing file has {len(existing)} records"
        )
        return congress, len(existing)

    offset = 0
    page_count = 0
    total_members = 0
    members = []
    max_retries = 3

    while True:
        retry_count = 0
        while retry_count < max_retries:
            try:
                url = f"{base_url}/member/congress/{congress}?offset={offset}&limit={PAGE_LIMIT}&format=json"
                throttle()
                r = get_session().get(url, timeout=60)
                r.raise_for_status()
                data = r.json()

                page_members = data.get("members", [])
                if not page_members:
                    return congress, len(members)

                members.extend(page_members)
                page_count += 1
                total_members = data.get("pagination", {}).get("count", len(members))

                logger.info(
                    f"  Congress {congress} members: Page {page_count}, {len(page_members)} members, total: {len(members)}/{total_members}"
                )

                # Check if we have all members
                if len(members) >= total_members:
                    # Save to JSON
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump({"congress": congress, "members": members}, f, indent=2)

                    logger.info(
                        f"✅ Downloaded {len(members)} members for Congress {congress} to {output_file}"
                    )
                    return congress, len(members)

                offset = next_offset(offset, PAGE_LIMIT)
                break  # Success, exit retry loop

            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(
                        f"  Retry {retry_count}/{max_retries} for Congress {congress} members at offset {offset}: {e}"
                    )
                    time.sleep(2**retry_count)  # Exponential backoff
                else:
                    logger.error(
                        f"  Failed to download members for Congress {congress} at offset {offset} after {max_retries} retries: {e}"
                    )
                    # Save what we have
                    output_file = congress_dir / f"members_{congress}_partial.json"
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(
                            {"congress": congress, "members": members, "partial": True}, f, indent=2
                        )
                    logger.info(
                        f"  Saved partial download: {len(members)} members to {output_file}"
                    )
                    return congress, len(members)


def download_house_votes_for_congress(congress):
    """Download House roll call vote list data for a congress when the endpoint exists."""
    congress_dir = BASE_DIR / f"congress_{congress}" / "votes"
    congress_dir.mkdir(parents=True, exist_ok=True)

    output_file = congress_dir / f"house_votes_{congress}.json"
    existing = load_existing_json(output_file)
    if existing:
        logger.info(
            f"  Skipping Congress {congress} House votes; existing file has {len(existing)} records"
        )
        return congress, len(existing)

    logger.info(f"Downloading House votes for Congress {congress}...")
    offset = 0
    page_count = 0
    total_votes = 0
    votes = []
    max_retries = 3

    while True:
        retry_count = 0
        while retry_count < max_retries:
            try:
                url = f"{base_url}/house-vote/{congress}?offset={offset}&limit={PAGE_LIMIT}&format=json"
                throttle()
                r = get_session().get(url, timeout=60)
                if r.status_code == 404:
                    logger.info(f"  House vote endpoint not available for Congress {congress}")
                    return congress, 0
                r.raise_for_status()
                data = r.json()

                page_votes = data.get("houseRollCallVotes", [])
                if not page_votes:
                    if votes:
                        with open(output_file, "w", encoding="utf-8") as f:
                            json.dump(
                                {"congress": congress, "houseRollCallVotes": votes}, f, indent=2
                            )
                    return congress, len(votes)

                votes.extend(page_votes)
                page_count += 1
                total_votes = data.get("pagination", {}).get("count", len(votes))

                logger.info(
                    f"  Congress {congress} House votes: Page {page_count}, {len(page_votes)} votes, total: {len(votes)}/{total_votes}"
                )

                if len(votes) >= total_votes:
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump({"congress": congress, "houseRollCallVotes": votes}, f, indent=2)

                    logger.info(
                        f"✅ Downloaded {len(votes)} House votes for Congress {congress} to {output_file}"
                    )
                    return congress, len(votes)

                offset = next_offset(offset, PAGE_LIMIT)
                break

            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(
                        f"  Retry {retry_count}/{max_retries} for Congress {congress} House votes at offset {offset}: {e}"
                    )
                    time.sleep(2**retry_count)
                else:
                    logger.error(
                        f"  Failed to download House votes for Congress {congress} at offset {offset} after {max_retries} retries: {e}"
                    )
                    partial_file = congress_dir / f"house_votes_{congress}_partial.json"
                    with open(partial_file, "w", encoding="utf-8") as f:
                        json.dump(
                            {"congress": congress, "houseRollCallVotes": votes, "partial": True},
                            f,
                            indent=2,
                        )
                    logger.info(
                        f"  Saved partial download: {len(votes)} House votes to {partial_file}"
                    )
                    return congress, len(votes)


def download_congress_data(congress, components):
    """Download selected Congress data components for a congress."""
    logger.info(f"=== Starting Congress {congress} ===")
    futures = {}
    with ThreadPoolExecutor(max_workers=max(1, len(components))) as executor:
        if "bills" in components:
            futures["bills"] = executor.submit(download_bills_for_congress, congress)
        if "members" in components:
            futures["members"] = executor.submit(download_members_for_congress, congress)
        if "votes" in components:
            futures["votes"] = executor.submit(download_house_votes_for_congress, congress)

        bills_count = 0
        members_count = 0
        house_votes_count = 0
        if "bills" in futures:
            _, bills_count = futures["bills"].result()
        if "members" in futures:
            _, members_count = futures["members"].result()
        if "votes" in futures:
            _, house_votes_count = futures["votes"].result()

    logger.info(
        f"=== Completed Congress {congress}: {bills_count} bills, {members_count} members, {house_votes_count} House votes ==="
    )
    return congress, bills_count, members_count, house_votes_count


def import_congress_directory(congress):
    """Import one congress directory immediately after its download completes."""
    congress_dir = BASE_DIR / f"congress_{congress}"
    cmd = [
        sys.executable,
        str(IMPORT_SCRIPT),
        "--base-dir",
        str(congress_dir),
        "--recursive",
    ]
    logger.info(f"Starting import for Congress {congress}: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        logger.info(result.stdout.rstrip())
    if result.returncode != 0:
        if result.stderr:
            logger.error(result.stderr.rstrip())
        raise RuntimeError(
            f"Import failed for Congress {congress} with exit code {result.returncode}"
        )
    logger.info(f"✅ Imported Congress {congress} from {congress_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--congresses",
        default="107-118",
        help="Congress numbers to download, e.g. '107', '107-118', or '107,108'",
    )
    parser.add_argument("--workers", type=int, default=4, help="Parallel congress workers")
    parser.add_argument(
        "--import-after-download",
        action="store_true",
        help="Import each congress immediately after its download finishes",
    )
    parser.add_argument(
        "--components",
        default="bills,members,votes",
        help="Comma-separated components to download: bills,members,votes",
    )
    args = parser.parse_args()
    congresses = parse_congresses(args.congresses)
    components = parse_components(args.components)

    logger.info("Starting Congress.gov historical data download (107th-118th Congress)")
    logger.info(f"Congresses: {congresses}")
    logger.info(f"Components: {sorted(components)}")
    logger.info("=" * 80)

    # Register this script in the database
    script_id = register_script()

    start_time = datetime.now()

    # Use parallel processing for congresses
    max_workers = args.workers  # Conservative to respect rate limits

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_congress_data, congress, components): congress
            for congress in congresses
        }

        for future in as_completed(futures):
            congress = futures[future]
            try:
                result = future.result()
                results.append(result)
                if args.import_after_download:
                    import_congress_directory(congress)
                logger.info(f"✅ Congress {congress} completed")
            except Exception as e:
                logger.error(f"❌ Congress {congress} failed: {e}")
                results.append((congress, 0, 0, 0))

    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    total_bills = sum(r[1] for r in results)
    total_members = sum(r[2] for r in results)
    total_house_votes = sum(r[3] for r in results)

    logger.info("=" * 80)
    logger.info("SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total Congresses processed: {len(results)}")
    logger.info(f"Total Bills downloaded: {total_bills:,}")
    logger.info(f"Total Members downloaded: {total_members:,}")
    logger.info(f"Total House votes downloaded: {total_house_votes:,}")
    logger.info(f"Duration: {duration:.2f} seconds ({duration / 60:.2f} minutes)")
    logger.info(
        f"Average speed: {(total_bills + total_members + total_house_votes) / duration:.2f} records/second"
    )
    logger.info(f"Log file: {log_file}")


if __name__ == "__main__":
    main()
