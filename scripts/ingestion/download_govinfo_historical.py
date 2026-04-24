#!/usr/bin/env python3
"""
Download GovInfo.gov Historical Data (2000-2023)
Downloads Federal Register, Bills, Court Opinions, Committee Reports
"""
import argparse
import os
import requests
import json
import logging
import sys
import hashlib
import psycopg2
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_historical")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

BASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f"govinfo_historical_{datetime.now():%Y%m%d_%H%M%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load secrets if not already in environment
if not os.environ.get('GOVINFO_API_KEY'):
    import subprocess
    secrets_file = Path.home() / 'workspace' / 'epstein' / '.bash_secrets'
    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                if line.startswith('export '):
                    key_val = line[7:].strip().split('=', 1)
                    if len(key_val) == 2 and key_val[0] not in os.environ:
                        os.environ[key_val[0]] = key_val[1].strip('"\'')

API_KEY = os.environ.get('GOVINFO_API_KEY')
if not API_KEY:
    logger.error("GOVINFO_API_KEY not set")
    sys.exit(1)

BASE_URL = "https://api.govinfo.gov"
HEADERS = {'X-Api-Key': API_KEY}

# Database configuration for script tracking
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'epstein',
    'user': 'cbwinslow',
    'password': '123qweasd'
}

# Collections to download
COLLECTIONS = ['FR', 'BILLS', 'USCOURTS', 'CRPT']
COLLECTION_NAMES = {
    'FR': 'Federal Register',
    'BILLS': 'Bills',
    'USCOURTS': 'Court Opinions',
    'CRPT': 'Committee Reports'
}

# Official docs: use offsetMark and published pageSize can be large; regular keys support 40 req/sec
RATE_LIMIT_DELAY = 0.11
PAGE_SIZE = 1000
_rate_limit_lock = threading.Lock()
_next_request_time = 0.0
_thread_local = threading.local()


def parse_years(value):
    """Parse year selector like '2000', '2000-2024', or '2000,2005'."""
    years = set()
    for part in value.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start, end = part.split('-', 1)
            years.update(range(int(start), int(end) + 1))
        else:
            years.add(int(part))
    return sorted(years)


def parse_collections(value):
    """Parse collection selector and validate collection codes."""
    collections = [part.strip().upper() for part in value.split(',') if part.strip()]
    invalid = sorted(set(collections) - set(COLLECTIONS))
    if invalid:
        raise ValueError(f"Unknown GovInfo collections: {', '.join(invalid)}")
    return collections


def date_ranges_for_year(year, collection):
    """Return date windows. offsetMark handles deep pagination, so yearly windows are acceptable."""
    return [(f"{year}-01-01", f"{year}-12-31")]


def output_path(collection, year, start_date, end_date):
    """Build stable output path for a collection/year/date window."""
    collection_dir = BASE_DIR / collection.lower() / str(year)
    collection_dir.mkdir(parents=True, exist_ok=True)
    suffix = str(year) if start_date.endswith('-01-01') and end_date.endswith('-12-31') else f"{start_date}_{end_date}"
    return collection_dir / f"{collection}_{suffix}.json"


def existing_count(path):
    """Return existing package count for a completed output file."""
    if not path.exists() or path.name.endswith('_partial.json'):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            return len(data.get('packages', []))
        if isinstance(data, list):
            return len(data)
    except (OSError, json.JSONDecodeError):
        return None
    return None


def get_session():
    """Reuse a requests session per worker thread."""
    session = getattr(_thread_local, 'session', None)
    if session is None:
        session = requests.Session()
        session.headers.update(HEADERS)
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


def extract_offset_mark(next_page: str):
    """Extract GovInfo offsetMark from nextPage URL."""
    if not next_page:
        return None
    parsed = urlparse(next_page)
    values = parse_qs(parsed.query).get('offsetMark')
    return values[0] if values else None

def register_script():
    """Register this script in the download_scripts table"""
    script_path = Path(__file__)
    script_name = script_path.name

    # Read script content
    with open(script_path, 'r') as f:
        script_content = f.read()

    # Calculate hash
    script_hash = hashlib.sha256(script_content.encode()).hexdigest()

    # Connect to database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        # Check if script already exists
        cur.execute(
            "SELECT id, script_hash FROM download_scripts WHERE script_name = %s",
            (script_name,)
        )
        result = cur.fetchone()

        if result:
            existing_id, existing_hash = result
            # Check if content changed
            if existing_hash != script_hash:
                # Update script
                cur.execute("""
                    UPDATE download_scripts
                    SET script_content = %s, script_hash = %s,
                        script_path = %s, updated_at = NOW()
                    WHERE id = %s
                """, (script_content, script_hash, str(script_path), existing_id))
                logger.info(f"Updated script in database: {script_name} (content changed)")
            else:
                logger.info(f"Script already registered (no changes): {script_name}")
            conn.commit()
            return existing_id
        else:
            # Insert new script
            cur.execute("""
                INSERT INTO download_scripts
                (script_name, script_path, script_content, script_hash, description, version)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (script_name, str(script_path), script_content, script_hash,
                  "Download GovInfo.gov historical data (FR, BILLS, USCOURTS, CRPT) for 2000-2023",
                  "1.0.0"))
            script_id = cur.fetchone()[0]
            logger.info(f"Registered new script in database: {script_name} (ID: {script_id})")
            conn.commit()
            return script_id

    finally:
        cur.close()
        conn.close()

def download_collection_range(collection, year, start_date, end_date):
    """Download all packages for one collection/date range."""
    path = output_path(collection, year, start_date, end_date)
    count = existing_count(path)
    if count is not None:
        logger.info(f"  Skipping {COLLECTION_NAMES[collection]} {start_date}..{end_date}; existing file has {count} packages")
        return collection, year, count

    logger.info(f"Downloading {COLLECTION_NAMES[collection]} for {start_date}..{end_date}...")
    offset_mark = '*'
    page_count = 0
    total_packages = []
    max_retries = 3

    while True:
        retry_count = 0
        while retry_count < max_retries:
            try:
                url = f"{BASE_URL}/published/{start_date}/{end_date}"
                params = {'offsetMark': offset_mark, 'pageSize': PAGE_SIZE, 'collection': collection}
                throttle()
                response = get_session().get(url, params=params, timeout=60)
                response.raise_for_status()
                data = response.json()

                packages = data.get('packages', [])
                if not packages:
                    return collection, year, len(total_packages)

                total_packages.extend(packages)
                page_count += 1

                logger.info(f"  {COLLECTION_NAMES[collection]} {year}: Page {page_count}, {len(packages)} packages, total: {len(total_packages)}")

                # Check for next page
                next_page = data.get('nextPage')
                if not next_page:
                    # Save to JSON
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump({
                            'collection': collection,
                            'year': year,
                            'start_date': start_date,
                            'end_date': end_date,
                            'packages': total_packages,
                        }, f, indent=2)

                    logger.info(f"✅ Downloaded {len(total_packages)} packages for {COLLECTION_NAMES[collection]} {start_date}..{end_date} to {path}")
                    return collection, year, len(total_packages)

                offset_mark = extract_offset_mark(next_page)
                if not offset_mark:
                    raise RuntimeError(f"Missing offsetMark in nextPage for {collection} {start_date}..{end_date}")
                break

            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"  Retry {retry_count}/{max_retries} for {COLLECTION_NAMES[collection]} {year} at offsetMark {offset_mark}: {e}")
                    time.sleep(2 ** retry_count)
                else:
                    logger.error(f"  Failed to download {COLLECTION_NAMES[collection]} {year} at offsetMark {offset_mark} after {max_retries} retries: {e}")
                    # Save what we have
                    partial_path = path.with_name(path.stem + "_partial.json")
                    with open(partial_path, 'w', encoding='utf-8') as f:
                        json.dump({
                            'collection': collection,
                            'year': year,
                            'start_date': start_date,
                            'end_date': end_date,
                            'packages': total_packages,
                            'partial': True,
                        }, f, indent=2)
                    logger.info(f"  Saved partial download: {len(total_packages)} packages to {partial_path}")
                    return collection, year, len(total_packages)


def download_collection_year(collection, year):
    """Download all packages for a collection for a specific year."""
    total = 0
    for start_date, end_date in date_ranges_for_year(year, collection):
        _, _, count = download_collection_range(collection, year, start_date, end_date)
        total += count
    return collection, year, total

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--years', default='2000-2024', help="Years to download, e.g. '2000' or '2000-2024'")
    parser.add_argument('--collections', default=','.join(COLLECTIONS), help='Comma-separated GovInfo collection codes')
    parser.add_argument('--workers', type=int, default=4, help='Parallel collection/year workers')
    args = parser.parse_args()
    years = parse_years(args.years)
    collections = parse_collections(args.collections)

    logger.info("Starting GovInfo.gov historical data download (2000-2023)")
    logger.info(f"Years: {years}")
    logger.info(f"Collections: {collections}")
    logger.info("=" * 80)

    # Register this script in the database
    script_id = register_script()

    start_time = datetime.now()

    # Create all tasks
    tasks = []
    for collection in collections:
        for year in years:
            tasks.append((collection, year))

    # Use parallel processing
    max_workers = args.workers

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_collection_year, collection, year): (collection, year) for collection, year in tasks}

        for future in as_completed(futures):
            collection, year = futures[future]
            try:
                result = future.result()
                results.append(result)
                logger.info(f"✅ {COLLECTION_NAMES[collection]} {year} completed: {result[2]} packages")
            except Exception as e:
                logger.error(f"❌ {COLLECTION_NAMES[collection]} {year} failed: {e}")
                results.append((collection, year, 0))

    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    total_by_collection = {}
    for collection in collections:
        total_by_collection[collection] = sum(r[2] for r in results if r[0] == collection)

    total_packages = sum(r[2] for r in results)

    logger.info("=" * 80)
    logger.info("SUMMARY")
    logger.info("=" * 80)
    for collection in collections:
        logger.info(f"{COLLECTION_NAMES[collection]}: {total_by_collection[collection]:,} packages")
    logger.info(f"Total packages downloaded: {total_packages:,}")
    logger.info(f"Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    logger.info(f"Average speed: {total_packages/duration:.2f} packages/second")
    logger.info(f"Log file: {log_file}")

if __name__ == "__main__":
    main()
