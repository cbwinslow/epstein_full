#!/usr/bin/env python3
"""
Senate Financial Disclosures Bulk Ingestion using CapitolGains

This script performs bulk ingestion of Senate financial disclosures
using the CapitolGains library, which scrapes the Senate EFD portal
at efdsearch.senate.gov.

Usage:
    python3 senate_bulk_ingest.py [options]

Options:
    --years START:END    Year range (e.g., 2012:2026)
    --workers N          Concurrent workers (default: 4)
    --limit N            Limit senators for testing
    --senators FILE      File with senator list (last,first,state per line)
    --resume             Resume from checkpoint
    --validate-only      Only validate existing data
"""

import argparse
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import psycopg2
from capitolgains import Senator
from capitolgains.utils.senator_scraper import SenateDisclosureScraper

# Configuration
RAW_FILES_DIR = Path("/home/cbwinslow/workspace/epstein/epstein-data/raw-files")
FINANCIAL_DIR = RAW_FILES_DIR / "financial_disclosures"
CHECKPOINT_FILE = FINANCIAL_DIR / "senate_ingestion_checkpoint.json"
LOG_FILE = FINANCIAL_DIR / "senate_ingestion.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class SenateBulkIngestion:
    """Bulk ingestion of Senate financial disclosures using CapitolGains."""

    def __init__(self, db_conn, years=None, workers=4, limit=None, resume=False):
        """
        Initialize the bulk ingestion.

        Args:
            db_conn: PostgreSQL database connection
            years: Year range to process
            workers: Number of concurrent workers
            limit: Limit number of senators for testing
            resume: Resume from checkpoint
        """
        self.conn = db_conn
        self.years = years
        self.workers = workers
        self.limit = limit
        self.resume = resume
        self.checkpoint = self._load_checkpoint() if resume else {"processed": [], "failed": []}

        self.stats = {
            "senators_processed": 0,
            "senators_failed": 0,
            "disclosures_found": 0,
            "start_time": datetime.now().isoformat(),
        }

    def _load_checkpoint(self):
        """Load checkpoint from file."""
        if CHECKPOINT_FILE.exists():
            try:
                with open(CHECKPOINT_FILE) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load checkpoint: {e}")
        return {"processed": [], "failed": []}

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

            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_senate_year
                ON senate_financial_disclosures(report_year)
            """)

            self.conn.commit()
            logger.info("Database tables ensured")

    def get_senator_list(self):
        """
        Get list of all current US Senators.

        Returns list of dicts with keys: last_name, first_name, state
        """
        # Current 118th Congress Senators (as of 2026)
        # Source: Official Senate records
        senators = [
            # Alabama
            {"last_name": "Shelby", "first_name": "Richard", "state": "AL"},
            {"last_name": "Tuberville", "first_name": "Tommy", "state": "AL"},
            # Alaska
            {"last_name": "Murkowski", "first_name": "Lisa", "state": "AK"},
            {"last_name": "Sullivan", "first_name": "Dan", "state": "AK"},
            # Arizona
            {"last_name": "Sinema", "first_name": "Kyrsten", "state": "AZ"},
            {"last_name": "Kelly", "first_name": "Mark", "state": "AZ"},
            # Arkansas
            {"last_name": "Boozman", "first_name": "John", "state": "AR"},
            {"last_name": "Cotton", "first_name": "Tom", "state": "AR"},
            # California
            {"last_name": "Feinstein", "first_name": "Dianne", "state": "CA"},
            {"last_name": "Padilla", "first_name": "Alex", "state": "CA"},
            # Colorado
            {"last_name": "Bennet", "first_name": "Michael", "state": "CO"},
            {"last_name": "Hickenlooper", "first_name": "John", "state": "CO"},
            # Connecticut
            {"last_name": "Blumenthal", "first_name": "Richard", "state": "CT"},
            {"last_name": "Murphy", "first_name": "Chris", "state": "CT"},
            # Delaware
            {"last_name": "Carper", "first_name": "Thomas", "state": "DE"},
            {"last_name": "Coons", "first_name": "Christopher", "state": "DE"},
            # Florida
            {"last_name": "Rubio", "first_name": "Marco", "state": "FL"},
            {"last_name": "Scott", "first_name": "Rick", "state": "FL"},
            # Georgia
            {"last_name": "Warnock", "first_name": "Raphael", "state": "GA"},
            {"last_name": "Ossoff", "first_name": "Jon", "state": "GA"},
            # Hawaii
            {"last_name": "Schatz", "first_name": "Brian", "state": "HI"},
            {"last_name": "Hirono", "first_name": "Mazie", "state": "HI"},
            # Idaho
            {"last_name": "Crapo", "first_name": "Mike", "state": "ID"},
            {"last_name": "Risch", "first_name": "Jim", "state": "ID"},
            # Illinois
            {"last_name": "Durbin", "first_name": "Dick", "state": "IL"},
            {"last_name": "Duckworth", "first_name": "Tammy", "state": "IL"},
            # Indiana
            {"last_name": "Young", "first_name": "Todd", "state": "IN"},
            {"last_name": "Braun", "first_name": "Mike", "state": "IN"},
            # Iowa
            {"last_name": "Grassley", "first_name": "Chuck", "state": "IA"},
            {"last_name": "Ernst", "first_name": "Joni", "state": "IA"},
            # Kansas
            {"last_name": "Moran", "first_name": "Jerry", "state": "KS"},
            {"last_name": "Marshall", "first_name": "Roger", "state": "KS"},
            # Kentucky
            {"last_name": "McConnell", "first_name": "Mitch", "state": "KY"},
            {"last_name": "Paul", "first_name": "Rand", "state": "KY"},
            # Louisiana
            {"last_name": "Kennedy", "first_name": "John", "state": "LA"},
            {"last_name": "Cassidy", "first_name": "Bill", "state": "LA"},
            # Maine
            {"last_name": "Collins", "first_name": "Susan", "state": "ME"},
            {"last_name": "King", "first_name": "Angus", "state": "ME"},
            # Maryland
            {"last_name": "Cardin", "first_name": "Ben", "state": "MD"},
            {"last_name": "Van Hollen", "first_name": "Chris", "state": "MD"},
            # Massachusetts
            {"last_name": "Markey", "first_name": "Ed", "state": "MA"},
            {"last_name": "Warren", "first_name": "Elizabeth", "state": "MA"},
            # Michigan
            {"last_name": "Stabenow", "first_name": "Debbie", "state": "MI"},
            {"last_name": "Peters", "first_name": "Gary", "state": "MI"},
            # Minnesota
            {"last_name": "Klobuchar", "first_name": "Amy", "state": "MN"},
            {"last_name": "Smith", "first_name": "Tina", "state": "MN"},
            # Mississippi
            {"last_name": "Wicker", "first_name": "Roger", "state": "MS"},
            {"last_name": "Hyde-Smith", "first_name": "Cindy", "state": "MS"},
            # Missouri
            {"last_name": "Hawley", "first_name": "Josh", "state": "MO"},
            {"last_name": "Schmitt", "first_name": "Eric", "state": "MO"},
            # Montana
            {"last_name": "Tester", "first_name": "Jon", "state": "MT"},
            {"last_name": "Daines", "first_name": "Steve", "state": "MT"},
            # Nebraska
            {"last_name": "Fischer", "first_name": "Deb", "state": "NE"},
            {"last_name": "Sasse", "first_name": "Ben", "state": "NE"},
            # Nevada
            {"last_name": "Rosen", "first_name": "Jacky", "state": "NV"},
            {"last_name": "Cortez Masto", "first_name": "Catherine", "state": "NV"},
            # New Hampshire
            {"last_name": "Shaheen", "first_name": "Jeanne", "state": "NH"},
            {"last_name": "Hassan", "first_name": "Maggie", "state": "NH"},
            # New Jersey
            {"last_name": "Menendez", "first_name": "Bob", "state": "NJ"},
            {"last_name": "Booker", "first_name": "Cory", "state": "NJ"},
            # New Mexico
            {"last_name": "Lujan Grisham", "first_name": "Ben", "state": "NM"},
            {"last_name": "Heinrich", "first_name": "Martin", "state": "NM"},
            # New York
            {"last_name": "Schumer", "first_name": "Chuck", "state": "NY"},
            {"last_name": "Gillibrand", "first_name": "Kirsten", "state": "NY"},
            # North Carolina
            {"last_name": "Tillis", "first_name": "Thom", "state": "NC"},
            {"last_name": "Budd", "first_name": "Ted", "state": "NC"},
            # North Dakota
            {"last_name": "Cramer", "first_name": "Kevin", "state": "ND"},
            {"last_name": "Hoeven", "first_name": "John", "state": "ND"},
            # Ohio
            {"last_name": "Brown", "first_name": "Sherrod", "state": "OH"},
            {"last_name": "Vance", "first_name": "J.D.", "state": "OH"},
            # Oklahoma
            {"last_name": "Inhofe", "first_name": "Jim", "state": "OK"},
            {"last_name": "Lankford", "first_name": "James", "state": "OK"},
            # Oregon
            {"last_name": "Wyden", "first_name": "Ron", "state": "OR"},
            {"last_name": "Merkley", "first_name": "Jeff", "state": "OR"},
            # Pennsylvania
            {"last_name": "Casey", "first_name": "Bob", "state": "PA"},
            {"last_name": "Fetterman", "first_name": "John", "state": "PA"},
            # Rhode Island
            {"last_name": "Reed", "first_name": "Jack", "state": "RI"},
            {"last_name": "Whitehouse", "first_name": "Sheldon", "state": "RI"},
            # South Carolina
            {"last_name": "Graham", "first_name": "Lindsey", "state": "SC"},
            {"last_name": "Scott", "first_name": "Tim", "state": "SC"},
            # South Dakota
            {"last_name": "Thune", "first_name": "John", "state": "SD"},
            {"last_name": "Rounds", "first_name": "Mike", "state": "SD"},
            # Tennessee
            {"last_name": "Alexander", "first_name": "Lamar", "state": "TN"},
            {"last_name": "Blackburn", "first_name": "Marsha", "state": "TN"},
            # Texas
            {"last_name": "Cornyn", "first_name": "John", "state": "TX"},
            {"last_name": "Cruz", "first_name": "Ted", "state": "TX"},
            # Utah
            {"last_name": "Lee", "first_name": "Mike", "state": "UT"},
            {"last_name": "Romney", "first_name": "Mitt", "state": "UT"},
            # Vermont
            {"last_name": "Sanders", "first_name": "Bernard", "state": "VT"},
            {"last_name": "Leahy", "first_name": "Patrick", "state": "VT"},
            # Virginia
            {"last_name": "Warner", "first_name": "Mark", "state": "VA"},
            {"last_name": "Kaine", "first_name": "Tim", "state": "VA"},
            # Washington
            {"last_name": "Murray", "first_name": "Patty", "state": "WA"},
            {"last_name": "Cantwell", "first_name": "Maria", "state": "WA"},
            # West Virginia
            {"last_name": "Manchin", "first_name": "Joe", "state": "WV"},
            {"last_name": "Capito", "first_name": "Shelley", "state": "WV"},
            # Wisconsin
            {"last_name": "Baldwin", "first_name": "Tammy", "state": "WI"},
            {"last_name": "Johnson", "first_name": "Ron", "state": "WI"},
            # Wyoming
            {"last_name": "Barrasso", "first_name": "John", "state": "WY"},
            {"last_name": "Lummis", "first_name": "Cynthia", "state": "WY"},
        ]

        if self.limit:
            senators = senators[: self.limit]

        # Filter out already processed senators if resuming
        if self.resume:
            processed_keys = set(self.checkpoint.get("processed", []))
            senators = [
                s for s in senators if f"{s['last_name']}_{s['state']}" not in processed_keys
            ]

        return senators

    def process_senator(self, senator):
        """Process a single senator's disclosures."""
        result = {
            "name": f"{senator['first_name']} {senator['last_name']}",
            "state": senator["state"],
            "success": False,
            "disclosures": 0,
            "error": None,
        }

        try:
            with SenateDisclosureScraper(headless=True) as scraper:
                sen = Senator(
                    senator["last_name"], first_name=senator["first_name"], state=senator["state"]
                )

                # Get disclosures for all available years
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
                    self._save_disclosures(senator, all_disclosures)
                    result["success"] = True
                    result["disclosures"] = total
                    self.stats["disclosures_found"] += total

        except Exception as e:
            result["error"] = str(e)
            logger.debug(f"Failed to process {result['name']}: {e}")

        return result

    def _save_disclosures(self, senator, disclosures):
        """Save Senate disclosures to database."""
        with self.conn.cursor() as cur:
            rows = []
            for dtype, items in disclosures.items():
                for item in items:
                    # Parse date - it comes as MM/DD/YYYY from CapitolGains
                    date_received = item.get("date")
                    report_year = None
                    if date_received:
                        try:
                            # Date is in MM/DD/YYYY format
                            dt = datetime.strptime(date_received, "%m/%d/%Y")
                            report_year = dt.year
                        except:
                            # Fallback: extract year from string
                            import re

                            year_match = re.search(r"(\d{4})", date_received)
                            if year_match:
                                report_year = int(year_match.group(1))

                    # Generate report_id from URL since CapitolGains doesn't provide it
                    report_url = item.get("report_url", "")
                    report_id = None
                    if report_url:
                        # Extract UUID from URL path
                        import re

                        uuid_match = re.search(
                            r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
                            report_url,
                        )
                        if uuid_match:
                            report_id = uuid_match.group(1)
                        else:
                            # Fallback: use hash of URL
                            import hashlib

                            report_id = hashlib.md5(report_url.encode()).hexdigest()

                    if not report_id:
                        # Last resort: generate from all fields
                        import hashlib

                        report_id = hashlib.md5(
                            f"{item.get('last_name')}{item.get('first_name')}{date_received}{dtype}".encode()
                        ).hexdigest()

                    rows.append(
                        (
                            report_id,
                            item.get("first_name", ""),
                            item.get("last_name", ""),
                            item.get("office", ""),
                            dtype,
                            report_year,
                            date_received,
                            report_url,
                        )
                    )

            if rows:
                for row in rows:
                    try:
                        cur.execute(
                            """
                            INSERT INTO senate_financial_disclosures
                            (report_id, first_name, last_name, office_name, filing_type,
                             report_year, date_received, pdf_url)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
                            row,
                        )
                    except Exception as e:
                        logger.warning(f"Failed to insert row: {e}")
                        self.conn.rollback()
                        continue

                self.conn.commit()

    def run(self):
        """Run the bulk ingestion."""
        logger.info("=" * 80)
        logger.info("SENATE FINANCIAL DISCLOSURES BULK INGESTION")
        logger.info("=" * 80)

        # Ensure tables exist
        self._ensure_tables()

        # Get senator list
        senators = self.get_senator_list()
        if not senators:
            logger.warning("No senators to process!")
            return

        logger.info(f"Processing {len(senators)} senators across {self.workers} workers")
        logger.info(f"Year range: {self.years or 'all available (2012-present)'}")

        # Process senators in parallel
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {
                executor.submit(self.process_senator, senator): senator for senator in senators
            }

            for future in as_completed(futures):
                senator = futures[future]
                try:
                    result = future.result(timeout=120)
                    self.stats["senators_processed"] += 1

                    if result["success"]:
                        senator_key = f"{senator['last_name']}_{senator['state']}"
                        self.checkpoint.setdefault("processed", []).append(senator_key)
                        logger.info(
                            f"✓ {result['name']} ({result['state']}) - {result['disclosures']} disclosures"
                        )
                    else:
                        self.stats["senators_failed"] += 1
                        senator_key = f"{senator['last_name']}_{senator['state']}"
                        self.checkpoint.setdefault("failed", []).append(senator_key)
                        logger.warning(
                            f"✗ {result['name']} ({result['state']}) - {result['error']}"
                        )

                    # Save checkpoint periodically
                    if len(self.checkpoint.get("processed", [])) % 10 == 0:
                        self._save_checkpoint()

                except Exception as e:
                    logger.error(f"Future failed: {e}")
                    self.stats["senators_failed"] += 1

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
        logger.info(f"Senators processed: {self.stats['senators_processed']}")
        logger.info(f"Senators failed: {self.stats['senators_failed']}")
        logger.info(f"Total disclosures found: {self.stats['disclosures_found']}")
        logger.info(f"Start time: {self.stats['start_time']}")
        logger.info(f"End time: {self.stats['end_time']}")
        logger.info("=" * 80)

    def validate_data(self):
        """Validate existing Senate data."""
        logger.info("=" * 80)
        logger.info("SENATE DATA VALIDATION")
        logger.info("=" * 80)

        with self.conn.cursor() as cur:
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

        logger.info("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Senate Financial Disclosures Bulk Ingestion")
    parser.add_argument("--chambers", default="senate", help="Chambers to process")
    parser.add_argument("--years", help="Year range (e.g., 2012:2026)")
    parser.add_argument("--workers", type=int, default=4, help="Number of workers")
    parser.add_argument("--limit", type=int, help="Limit senators for testing")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--validate-only", action="store_true", help="Only validate existing data")

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
    pipeline = SenateBulkIngestion(
        db_conn=conn, years=years, workers=args.workers, limit=args.limit, resume=args.resume
    )

    if args.validate_only:
        pipeline.validate_data()
    else:
        if "senate" in chambers:
            pipeline.run()
            pipeline.validate_data()
        else:
            logger.info("No Senate chamber specified. Use --chambers senate")

    conn.close()
    logger.info("Pipeline completed")


if __name__ == "__main__":
    main()
