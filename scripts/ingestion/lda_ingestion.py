#!/usr/bin/env python3
"""
LDA Lobbying Filings Ingestion - All Years 2000-2026

This script performs bulk ingestion of LDA lobbying filings
using the LDA Senate API at https://lda.senate.gov/api/redoc/v1/
No authentication required for read access.

Usage:
    python3 lda_ingestion.py [--all-years] [--start-year YYYY] [--end-year YYYY]
"""

import argparse
import json
import sys
import time
from datetime import datetime

import requests
from psycopg2.extras import execute_batch

from config import RAW_FILES_DIR, get_db_connection, setup_file_logger

# Configuration
LOG_DIR = RAW_FILES_DIR / "logs" / "lda"
LOG_DIR.mkdir(parents=True, exist_ok=True)

BASE_API = "https://lda.senate.gov/api/v1"
PAGE_SIZE = 25  # LDA API is slow; keep small to avoid timeouts
MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds


def setup_logging():
    """Setup logging for LDA ingestion."""
    logger, log_file = setup_file_logger("lda_ingestion")
    return logger, log_file


def create_tables(conn):
    """Create LDA filings table if it doesn't exist."""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lda_filings (
            filing_uuid         TEXT PRIMARY KEY,
            filing_type         TEXT,
            filing_year         INT,
            filing_period       TEXT,
            registrant_name     TEXT,
            registrant_id       TEXT,
            client_name         TEXT,
            client_id           TEXT,
            lobbyist_names      JSONB,
            lobbying_activities JSONB,
            income              NUMERIC,
            expenses            NUMERIC,
            signed_date         DATE,
            url                 TEXT,
            updated_at          TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_lda_registrant ON lda_filings(registrant_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_lda_client ON lda_filings(client_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_lda_year ON lda_filings(filing_year);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_lda_signed_date ON lda_filings(signed_date);")
    conn.commit()
    cur.close()


def paginate_lda(endpoint, params=None, logger=None):
    """Paginate through LDA API results with retry logic."""
    params = params or {}
    params["page_size"] = PAGE_SIZE
    params["page"] = 1
    all_results = []

    while True:
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                response = requests.get(f"{BASE_API}/{endpoint}/", params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                break
            except requests.exceptions.RequestException as e:
                retry_count += 1
                if retry_count >= MAX_RETRIES:
                    if logger:
                        logger.error(
                            f"Failed to fetch {endpoint} page {params['page']} after {MAX_RETRIES} retries: {e}"
                        )
                    raise
                if logger:
                    logger.warning(
                        f"Request failed (attempt {retry_count}/{MAX_RETRIES}): {e}. Retrying in {RETRY_DELAY}s..."
                    )
                time.sleep(RETRY_DELAY)

        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)

        if logger and len(all_results) % 500 == 0:
            logger.info(f"  Fetched {len(all_results)} records so far...")

        if not data.get("next"):
            break

        params["page"] += 1

    return all_results


def get_existing_uuids(conn):
    """Get set of existing filing UUIDs to avoid duplicates."""
    cur = conn.cursor()
    cur.execute("SELECT filing_uuid FROM lda_filings")
    existing = {row[0] for row in cur.fetchall()}
    cur.close()
    return existing


def ingest_filings_by_year(conn, start_year, end_year, logger):
    """Ingest LDA filings for a range of years."""
    existing_uuids = get_existing_uuids(conn)
    total_new = 0
    total_existing = 0

    for year in range(start_year, end_year + 1):
        logger.info(f"  Processing year {year}...")

        try:
            filings = paginate_lda("filings", params={"filing_year": year}, logger=logger)
        except Exception as e:
            logger.error(f"  Failed to fetch filings for {year}: {e}")
            continue

        if not filings:
            logger.info(f"  No filings found for {year}")
            continue

        new_filings = []
        for filing in filings:
            uuid = filing.get("filing_uuid") or filing.get("id")
            if not uuid:
                continue

            if uuid in existing_uuids:
                total_existing += 1
                continue

            # Parse lobbyist names
            lobbyists = filing.get("lobbyists", [])
            lobbyist_names = []
            for lob in lobbyists:
                if isinstance(lob, dict):
                    name = f"{lob.get('first_name', '')} {lob.get('last_name', '')}".strip()
                    if name:
                        lobbyist_names.append(name)
                elif isinstance(lob, str):
                    lobbyist_names.append(lob)

            # Parse lobbying activities
            activities = filing.get("lobbying_activities", [])
            if isinstance(activities, str):
                try:
                    activities = json.loads(activities)
                except:
                    activities = []

            # Parse signed date
            signed_date = None
            if filing.get("signed_date"):
                try:
                    signed_date = datetime.strptime(filing["signed_date"][:10], "%Y-%m-%d").date()
                except:
                    pass

            new_filings.append(
                (
                    uuid,
                    filing.get("filing_type"),
                    filing.get("filing_year"),
                    filing.get("filing_period"),
                    filing.get("registrant_name"),
                    filing.get("registrant_id"),
                    filing.get("client_name"),
                    filing.get("client_id"),
                    json.dumps(lobbyist_names),
                    json.dumps(activities),
                    filing.get("income"),
                    filing.get("expenses"),
                    signed_date,
                    filing.get("url"),
                )
            )
            existing_uuids.add(uuid)
            total_new += 1

        if new_filings:
            cur = conn.cursor()
            execute_batch(
                cur,
                """
                INSERT INTO lda_filings (
                    filing_uuid, filing_type, filing_year, filing_period,
                    registrant_name, registrant_id, client_name, client_id,
                    lobbyist_names, lobbying_activities, income, expenses,
                    signed_date, url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                new_filings,
                page_size=100,
            )
            conn.commit()
            cur.close()
            logger.info(f"    Inserted {len(new_filings)} new filings for {year}")
        else:
            logger.info(f"    No new filings for {year}")

    return total_new, total_existing


def main():
    parser = argparse.ArgumentParser(description="Ingest LDA lobbying filings into PostgreSQL")
    parser.add_argument(
        "--all-years", action="store_true", help="Ingest all available years (2000-2026)"
    )
    parser.add_argument("--start-year", type=int, default=2000, help="Start year (default: 2000)")
    parser.add_argument("--end-year", type=int, default=2026, help="End year (default: 2026)")
    args = parser.parse_args()

    if args.all_years:
        start_year = 2000
        end_year = 2026
    else:
        start_year = args.start_year
        end_year = args.end_year

    logger, log_file = setup_logging()

    logger.info("=" * 80)
    logger.info("LDA LOBBYING FILINGS INGESTION")
    logger.info("=" * 80)
    logger.info(f"Start Time: {datetime.now().isoformat()}")
    logger.info(f"Year Range: {start_year} - {end_year}")
    logger.info(f"Log File: {log_file}")
    logger.info("=" * 80)

    conn = None
    try:
        conn = get_db_connection()
        logger.info("✅ Connected to database")

        create_tables(conn)
        logger.info("✅ Tables created/verified")

        logger.info(f"\n🚀 Starting ingestion for years {start_year}-{end_year}...")
        start_time = time.time()

        total_new, total_existing = ingest_filings_by_year(conn, start_year, end_year, logger)

        elapsed = time.time() - start_time

        logger.info("\n" + "=" * 80)
        logger.info("INGESTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"New filings inserted: {total_new:,}")
        logger.info(f"Existing filings skipped: {total_existing:,}")
        logger.info(f"Total elapsed time: {elapsed:.2f}s ({elapsed / 60:.2f} minutes)")
        logger.info("=" * 80)

        # Verify final count
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM lda_filings")
        total_count = cur.fetchone()[0]
        cur.close()
        logger.info(f"Total records in lda_filings: {total_count:,}")

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

    logger.info(f"\n✅ LDA Ingestion Complete at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
