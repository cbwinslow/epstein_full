#!/usr/bin/env python3
"""
Unified Financial Disclosures Ingestion Pipeline using CapitolGains

This script provides a comprehensive pipeline for ingesting ALL available
financial disclosure data for US Congress members using the CapitolGains
library. It handles both House and Senate disclosures, with proper error
handling, progress tracking, and database integration.

The pipeline:
1. Retrieves all Congress members via Congress.gov API or database
2. Downloads ALL financial disclosures for each member (all years)
3. Processes and normalizes the data
4. Loads into PostgreSQL database
5. Tracks progress and validates data quality

Usage:
    python3 financial_disclosures_ingestion.py [options]

Options:
    --chambers HOUSE,SENATE    Chambers to process (default: both)
    --years START:END          Year range (default: all available)
    --workers N                Concurrent workers (default: 8)
    --limit N                  Limit members for testing
    --resume                   Resume from last checkpoint
    --validate-only            Only validate existing data
    --all-years                Process ALL available years (1995+ for House, 2012+ for Senate)
"""

import argparse
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import psycopg2
from capitolgains import Congress, Representative, Senator
from capitolgains.utils.representative_scraper import HouseDisclosureScraper
from capitolgains.utils.senator_scraper import SenateDisclosureScraper
from psycopg2.extras import execute_values

# Configuration
RAW_FILES_DIR = Path("/home/cbwinslow/workspace/epstein/epstein-data/raw-files")
FINANCIAL_DIR = RAW_FILES_DIR / "financial_disclosures"
CHECKPOINT_FILE = FINANCIAL_DIR / "ingestion_checkpoint.json"
LOG_FILE = FINANCIAL_DIR / "ingestion.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class FinancialDisclosurePipeline:
    """Unified pipeline for ingesting financial disclosure data."""

    def __init__(self, db_conn, chambers=None, years=None, workers=8, limit=None):
        """
        Initialize the pipeline.

        Args:
            db_conn: PostgreSQL database connection
            chambers: List of chambers to process ('house', 'senate')
            years: Year range to process
            workers: Number of concurrent workers
            limit: Limit number of members for testing
        """
        self.conn = db_conn
        self.chambers = chambers or ["house", "senate"]
        self.years = years
        self.workers = workers
        self.limit = limit
        self.checkpoint = self._load_checkpoint()

        # Statistics
        self.stats = {
            "members_processed": 0,
            "members_failed": 0,
            "disclosures_downloaded": 0,
            "disclosures_failed": 0,
            "house_disclosures": 0,
            "senate_disclosures": 0,
            "start_time": datetime.now().isoformat(),
        }

    def _load_checkpoint(self) -> Dict:
        """Load checkpoint from file."""
        if CHECKPOINT_FILE.exists():
            try:
                with open(CHECKPOINT_FILE) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load checkpoint: {e}")
        return {"processed_members": [], "failed_members": []}

    def _save_checkpoint(self):
        """Save checkpoint to file."""
        try:
            with open(CHECKPOINT_FILE, "w") as f:
                json.dump(self.checkpoint, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save checkpoint: {e}")

    def _ensure_tables(self):
        """Ensure required database tables exist."""
        with self.conn.cursor() as cur:
            # House financial disclosures
            cur.execute("""
                CREATE TABLE IF NOT EXISTS house_financial_disclosures (
                    filing_id TEXT PRIMARY KEY,
                    year INT,
                    last_name TEXT,
                    first_name TEXT,
                    suffix TEXT,
                    filing_type TEXT,
                    state_dst TEXT,
                    pdf_url TEXT,
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            # Senate financial disclosures
            cur.execute("""
                CREATE TABLE IF NOT EXISTS senate_financial_disclosures (
                    report_id TEXT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    office_name TEXT,
                    filing_type TEXT,
                    report_year INT,
                    date_received DATE,
                    pdf_url TEXT,
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            # House PTR OCR pages
            cur.execute("""
                CREATE TABLE IF NOT EXISTS house_ptr_ocr_pages (
                    filing_id TEXT NOT NULL,
                    year INT,
                    page_number INT NOT NULL,
                    image_width INT,
                    image_height INT,
                    rotation INT,
                    ocr_text TEXT,
                    words JSONB,
                    avg_confidence NUMERIC,
                    ocr_engine TEXT DEFAULT 'tesseract',
                    ocr_config TEXT,
                    source_pdf TEXT,
                    updated_at TIMESTAMPTZ DEFAULT NOW(),
                    PRIMARY KEY (filing_id, page_number)
                )
            """)

            # House PTR OCR status
            cur.execute("""
                CREATE TABLE IF NOT EXISTS house_ptr_ocr_status (
                    filing_id TEXT PRIMARY KEY,
                    year INT,
                    pdf_path TEXT,
                    page_count INT,
                    pages_ocr INT,
                    status TEXT,
                    error TEXT,
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            # Congress trading (transactions)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS congress_trading (
                    id SERIAL PRIMARY KEY,
                    politician_name TEXT,
                    politician_state TEXT,
                    politician_district TEXT,
                    transaction_date DATE,
                    ticker TEXT,
                    asset_name TEXT,
                    asset_type TEXT,
                    transaction_type TEXT,
                    amount_low NUMERIC,
                    amount_high NUMERIC,
                    amount_text TEXT,
                    description TEXT,
                    data_source TEXT,
                    filing_date DATE,
                    disclosure_url TEXT,
                    source_filing_id TEXT,
                    source_page_number INT,
                    source_row_hash TEXT,
                    source_raw_text TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            # Create indexes
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_house_year
                ON house_financial_disclosures(year)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_senate_year
                ON senate_financial_disclosures(report_year)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_trading_date
                ON congress_trading(transaction_date)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_trading_source
                ON congress_trading(source_filing_id)
            """)

            self.conn.commit()
            logger.info("Database tables ensured")

    def get_all_members(self) -> List:
        """Retrieve all Congress members."""
        logger.info("Retrieving Congress members...")
        try:
            # Use CapitolGains Congress class
            congress = Congress(api_key="U71JFZEqNsiSranCdbrj4pZaobtoMtAnl18cIJc2")
            members = congress.get_all_members()
            logger.info(f"Retrieved {len(members)} Congress members")
            return members
        except Exception as e:
            logger.error(f"Failed to retrieve members via API: {e}")
            logger.info("Falling back to manual member list...")
            return self._get_manual_member_list()

    def _get_manual_member_list(self) -> List:
        """Get member list from database or manual list."""
        members = []
        try:
            with self.conn.cursor() as cur:
                # Get unique members from existing data
                cur.execute("""
                    SELECT DISTINCT last_name, first_name, state_dst, district
                    FROM house_financial_disclosures
                    WHERE year >= 2020
                """)
                for row in cur.fetchall():
                    members.append(
                        {
                            "name": f"{row[1]} {row[0]}" if row[1] else row[0],
                            "last_name": row[0],
                            "first_name": row[1],
                            "state": row[2],
                            "district": row[3],
                            "chamber": "House",
                        }
                    )

                cur.execute("""
                    SELECT DISTINCT last_name, first_name, state_dst
                    FROM senate_financial_disclosures
                    WHERE report_year >= 2020
                """)
                for row in cur.fetchall():
                    members.append(
                        {
                            "name": f"{row[1]} {row[0]}" if row[1] else row[0],
                            "last_name": row[0],
                            "first_name": row[1],
                            "state": row[2],
                            "chamber": "Senate",
                        }
                    )
        except Exception as e:
            logger.warning(f"Could not get members from DB: {e}")

        return members

    def process_house_member(self, member: Dict) -> Dict:
        """Process a single House member."""
        result = {
            "name": member.get("name", ""),
            "state": member.get("state", ""),
            "district": member.get("district", ""),
            "success": False,
            "disclosures": 0,
            "error": None,
        }

        try:
            with HouseDisclosureScraper(headless=True) as scraper:
                rep = Representative(
                    member.get("last_name") or member.get("name", "").split()[-1],
                    state=member.get("state"),
                    district=member.get("district"),
                )

                # Get disclosures for all years or specific range
                years_to_check = self.years or range(2013, datetime.now().year + 1)
                if isinstance(years_to_check, range):
                    years_to_check = [str(y) for y in years_to_check]

                all_disclosures = {}
                for year in years_to_check:
                    try:
                        disclosures = rep.get_disclosures(scraper, year=year)
                        for dtype, items in disclosures.items():
                            if dtype not in all_disclosures:
                                all_disclosures[dtype] = []
                            all_disclosures[dtype].extend(items)
                    except Exception as e:
                        logger.debug(f"Year {year} failed for {result['name']}: {e}")

                total = sum(len(v) for v in all_disclosures.values())
                if total > 0:
                    self._save_house_disclosures(member, all_disclosures)
                    result["success"] = True
                    result["disclosures"] = total
                    self.stats["house_disclosures"] += total

        except Exception as e:
            result["error"] = str(e)
            logger.debug(f"Failed to process House member {result['name']}: {e}")

        return result

    def process_senate_member(self, member: Dict) -> Dict:
        """Process a single Senate member."""
        result = {
            "name": member.get("name", ""),
            "state": member.get("state", ""),
            "success": False,
            "disclosures": 0,
            "error": None,
        }

        try:
            with SenateDisclosureScraper(headless=True) as scraper:
                # Note: Senator class internally validates state codes
                # Some states like DC, territories won't work - skip them
                state = member.get("state", "")
                if not state or len(state) != 2:
                    logger.debug(f"Skipping {result['name']} - invalid state: {state}")
                    result["error"] = f"Invalid state: {state}"
                    return result

                sen = Senator(
                    member.get("last_name") or member.get("name", "").split()[-1],
                    first_name=member.get("first_name", ""),
                    state=state,
                )

                # Get disclosures for all years or specific range
                years_to_check = self.years or range(2012, datetime.now().year + 1)
                if isinstance(years_to_check, range):
                    years_to_check = [str(y) for y in years_to_check]

                all_disclosures = {}
                for year in years_to_check:
                    try:
                        disclosures = sen.get_disclosures(scraper, year=year)
                        for dtype, items in disclosures.items():
                            if dtype not in all_disclosures:
                                all_disclosures[dtype] = []
                            all_disclosures[dtype].extend(items)
                    except Exception as e:
                        logger.debug(f"Year {year} failed for {result['name']}: {e}")

                total = sum(len(v) for v in all_disclosures.values())
                if total > 0:
                    self._save_senate_disclosures(member, all_disclosures)
                    result["success"] = True
                    result["disclosures"] = total
                    self.stats["senate_disclosures"] += total

        except Exception as e:
            result["error"] = str(e)
            logger.debug(f"Failed to process Senate member {result['name']}: {e}")

        return result

    def _save_house_disclosures(self, member: Dict, disclosures: Dict):
        """Save House disclosures to database."""
        with self.conn.cursor() as cur:
            rows = []
            for dtype, items in disclosures.items():
                for item in items:
                    rows.append(
                        (
                            item.get("filing_id", ""),
                            int(item.get("year", 0)),
                            item.get("last_name", ""),
                            item.get("first_name", ""),
                            item.get("suffix", ""),
                            dtype,
                            item.get("state_dst", ""),
                            item.get("pdf_url", ""),
                        )
                    )

            if rows:
                execute_values(
                    cur,
                    """
                    INSERT INTO house_financial_disclosures
                    (filing_id, year, last_name, first_name, suffix, filing_type, state_dst, pdf_url)
                    VALUES %s
                    ON CONFLICT (filing_id) DO UPDATE SET
                        year = EXCLUDED.year,
                        last_name = EXCLUDED.last_name,
                        first_name = EXCLUDED.first_name,
                        suffix = EXCLUDED.suffix,
                        filing_type = EXCLUDED.filing_type,
                        state_dst = EXCLUDED.state_dst,
                        pdf_url = EXCLUDED.pdf_url,
                        updated_at = NOW()
                    """,
                    rows,
                )
                self.conn.commit()

    def _save_senate_disclosures(self, member: Dict, disclosures: Dict):
        """Save Senate disclosures to database."""
        with self.conn.cursor() as cur:
            rows = []
            for dtype, items in disclosures.items():
                for item in items:
                    rows.append(
                        (
                            item.get("report_id", ""),
                            item.get("first_name", ""),
                            item.get("last_name", ""),
                            item.get("office_name", ""),
                            dtype,
                            int(item.get("report_year", 0)),
                            item.get("date_received"),
                            item.get("pdf_url", ""),
                        )
                    )

            if rows:
                execute_values(
                    cur,
                    """
                    INSERT INTO senate_financial_disclosures
                    (report_id, first_name, last_name, office_name, filing_type, report_year, date_received, pdf_url)
                    VALUES %s
                    ON CONFLICT (report_id) DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        office_name = EXCLUDED.office_name,
                        filing_type = EXCLUDED.filing_type,
                        report_year = EXCLUDED.report_year,
                        date_received = EXCLUDED.date_received,
                        pdf_url = EXCLUDED.pdf_url,
                        updated_at = NOW()
                    """,
                    rows,
                )
                self.conn.commit()

    def run(self):
        """Run the complete ingestion pipeline."""
        logger.info("=" * 80)
        logger.info("FINANCIAL DISCLOSURES INGESTION PIPELINE STARTED")
        logger.info("=" * 80)

        # Ensure tables exist
        self._ensure_tables()

        # Get all members
        members = self.get_all_members()
        if self.limit:
            members = members[: self.limit]

        if not members:
            logger.warning("No members to process!")
            return

        logger.info(f"Processing {len(members)} members across chambers: {self.chambers}")

        # Process members in parallel
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = []

            for member in members:
                # Handle both dict and CongressMember objects
                if hasattr(member, "bioguide_id"):
                    # CongressMember object
                    member_dict = {
                        "name": member.name,
                        "last_name": member.name.split(",")[0]
                        if "," in member.name
                        else member.name.split()[-1],
                        "first_name": member.name.split(",")[1].strip()
                        if "," in member.name
                        else (member.name.split()[0] if len(member.name.split()) > 1 else ""),
                        "state": member.state,
                        "district": member.district,
                        "chamber": member.chamber,
                    }
                else:
                    # Dict object
                    member_dict = member

                # Skip already processed members if resuming
                member_key = f"{member_dict.get('last_name', '')}_{member_dict.get('state', '')}"
                if member_key in self.checkpoint.get("processed_members", []):
                    continue

                chamber = member_dict.get("chamber", "").lower()
                if chamber in self.chambers or not chamber:
                    if "house" in self.chambers and chamber in ["house", ""]:
                        future = executor.submit(self.process_house_member, member_dict)
                        futures.append((future, "house", member_dict))
                    elif "senate" in self.chambers and chamber in ["senate", ""]:
                        future = executor.submit(self.process_senate_member, member_dict)
                        futures.append((future, "senate", member_dict))
                        futures.append((future, "senate", member))

            # Collect results
            for future, chamber, member in futures:
                try:
                    result = future.result(timeout=120)
                    self.stats["members_processed"] += 1

                    if result["success"]:
                        member_key = f"{member.get('last_name', '')}_{member.get('state', '')}"
                        self.checkpoint.setdefault("processed_members", []).append(member_key)
                        logger.info(
                            f"✓ {chamber.upper()}: {result['name']} - {result['disclosures']} disclosures"
                        )
                    else:
                        self.stats["members_failed"] += 1
                        member_key = f"{member.get('last_name', '')}_{member.get('state', '')}"
                        self.checkpoint.setdefault("failed_members", []).append(member_key)
                        logger.warning(f"✗ {chamber.upper()}: {result['name']} - {result['error']}")

                    # Save checkpoint periodically
                    if len(self.checkpoint.get("processed_members", [])) % 10 == 0:
                        self._save_checkpoint()

                except Exception as e:
                    logger.error(f"Future failed: {e}")
                    self.stats["members_failed"] += 1

        # Final checkpoint
        self._save_checkpoint()

        # Print summary
        self.stats["end_time"] = datetime.now().isoformat()
        self._print_summary()

    def _print_summary(self):
        """Print ingestion summary."""
        logger.info("\n" + "=" * 80)
        logger.info("INGESTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Members processed: {self.stats['members_processed']}")
        logger.info(f"Members failed: {self.stats['members_failed']}")
        logger.info(f"House disclosures: {self.stats['house_disclosures']}")
        logger.info(f"Senate disclosures: {self.stats['senate_disclosures']}")
        logger.info(
            f"Total disclosures: {self.stats['house_disclosures'] + self.stats['senate_disclosures']}"
        )
        logger.info(f"Start time: {self.stats['start_time']}")
        logger.info(f"End time: {self.stats['end_time']}")
        logger.info("=" * 80)

    def validate_data(self):
        """Validate existing data in database."""
        logger.info("=" * 80)
        logger.info("DATA VALIDATION")
        logger.info("=" * 80)

        with self.conn.cursor() as cur:
            # House data
            cur.execute("""
                SELECT year, COUNT(*), COUNT(DISTINCT filing_id)
                FROM house_financial_disclosures
                GROUP BY year
                ORDER BY year
            """)
            house_data = cur.fetchall()

            logger.info("\nHouse Financial Disclosures:")
            total_house = 0
            for year, count, filings in house_data:
                logger.info(f"  {year}: {count} records, {filings} unique filings")
                total_house += filings
            logger.info(f"  Total: {total_house} unique filings")

            # Senate data
            cur.execute("""
                SELECT report_year, COUNT(*), COUNT(DISTINCT report_id)
                FROM senate_financial_disclosures
                GROUP BY report_year
                ORDER BY report_year
            """)
            senate_data = cur.fetchall()

            logger.info("\nSenate Financial Disclosures:")
            total_senate = 0
            for year, count, filings in senate_data:
                logger.info(f"  {year}: {count} records, {filings} unique filings")
                total_senate += filings
            logger.info(f"  Total: {total_senate} unique filings")

            # Check for missing years
            cur.execute("""
                SELECT MIN(year), MAX(year) FROM house_financial_disclosures
            """)
            house_min, house_max = cur.fetchone()

            cur.execute("""
                SELECT MIN(report_year), MAX(report_year) FROM senate_financial_disclosures
            """)
            senate_min, senate_max = cur.fetchone()

            logger.info(f"\nHouse year range: {house_min} - {house_max}")
            logger.info(f"Senate year range: {senate_min or 'N/A'} - {senate_max or 'N/A'}")

        logger.info("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Financial Disclosures Ingestion Pipeline")
    parser.add_argument("--chambers", default="house,senate", help="Chambers to process")
    parser.add_argument("--years", help="Year range (e.g., 2015:2025)")
    parser.add_argument("--workers", type=int, default=8, help="Number of workers")
    parser.add_argument("--limit", type=int, help="Limit members for testing")
    parser.add_argument("--validate-only", action="store_true", help="Only validate existing data")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")

    args = parser.parse_args()

    # Parse chambers
    chambers = [c.strip().lower() for c in args.chambers.split(",")]

    # Parse years
    years = None
    if args.years:
        if ":" in args.years:
            start, end = map(int, args.years.split(":"))
            years = range(start, end + 1)
        else:
            years = [args.years]

    # Connect to database
    try:
        conn = psycopg2.connect(dbname="epstein", user="cbwinslow", host="localhost")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        sys.exit(1)

    # Create and run pipeline
    pipeline = FinancialDisclosurePipeline(
        db_conn=conn, chambers=chambers, years=years, workers=args.workers, limit=args.limit
    )

    if args.validate_only:
        pipeline.validate_data()
    else:
        pipeline.run()
        pipeline.validate_data()

    conn.close()
    logger.info("Pipeline completed")


if __name__ == "__main__":
    main()
