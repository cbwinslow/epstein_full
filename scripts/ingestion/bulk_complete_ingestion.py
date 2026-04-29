#!/usr/bin/env python3
"""
Complete Bulk Financial Disclosure Ingestion - ALL Members, ALL Years

This script ingests ALL available financial disclosure data from CapitolGains
for ALL Congress members across ALL available years.

House: 1995-2026 (22 years)
Senate: 2012-2026 (15 years)

It processes every member in the database and attempts to retrieve all
disclosures for each year in their coverage period.
"""

import json
import logging
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import psycopg2

# CapitolGains imports
from capitolgains import Representative, Senator
from capitolgains.utils.representative_scraper import HouseDisclosureScraper
from capitolgains.utils.senator_scraper import SenateDisclosureScraper

# Configuration
RAW_FILES_DIR = Path("/home/cbwinslow/workspace/epstein/epstein-data/raw-files")
FINANCIAL_DIR = RAW_FILES_DIR / "financial_disclosures"
FINANCIAL_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = FINANCIAL_DIR / f"bulk_ingestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
CHECKPOINT_FILE = FINANCIAL_DIR / "bulk_checkpoint.json"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


# Database connection
def get_db_connection():
    return psycopg2.connect(dbname="epstein", user="postgres", host="localhost")


class BulkIngestionPipeline:
    """Pipeline for bulk ingestion of ALL financial disclosure data."""

    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

        # Statistics
        self.stats = {
            "start_time": datetime.now().isoformat(),
            "house_members_total": 0,
            "house_members_processed": 0,
            "house_members_failed": 0,
            "house_disclosures_found": 0,
            "house_disclosures_new": 0,
            "house_disclosures_duplicate": 0,
            "senate_members_total": 0,
            "senate_members_processed": 0,
            "senate_members_failed": 0,
            "senate_disclosures_found": 0,
            "senate_disclosures_new": 0,
            "senate_disclosures_duplicate": 0,
            "trading_records_found": 0,
            "trading_records_new": 0,
        }

        # House years: 1995-2026
        self.house_years = list(range(1995, 2027))
        # Senate years: 2012-2026
        self.senate_years = list(range(2012, 2027))

    def get_all_members_from_db(self) -> Tuple[List[Dict], List[Dict]]:
        """Get all Congress members from database."""
        # Get House members - use state_dst column (contains state+district like CA11)
        logger.info("Executing House members query...")
        self.cursor.execute("""
            SELECT DISTINCT last_name, first_name, state_dst
            FROM house_financial_disclosures
            ORDER BY state_dst, last_name
        """)
        house_rows = self.cursor.fetchall()
        logger.info(f"House query returned {len(house_rows)} rows")

        house_members = []
        for row in house_rows:
            state_district = row[2] or ""
            # Extract state (first 2 chars) and district (remaining)
            if len(state_district) >= 2:
                state = state_district[:2]
                district = state_district[2:] if len(state_district) > 2 else "00"
            else:
                state = state_district
                district = "00"
            house_members.append(
                {
                    "last_name": row[0],
                    "first_name": row[1] or "",
                    "state": state,
                    "district": district,
                }
            )

        # Get Senate members
        logger.info("Executing Senate members query...")
        self.cursor.execute("""
            SELECT DISTINCT last_name, first_name, office_name
            FROM senate_financial_disclosures
            ORDER BY last_name
        """)
        senate_rows = self.cursor.fetchall()
        logger.info(f"Senate query returned {len(senate_rows)} rows")

        senate_members = [
            {"last_name": row[0], "first_name": row[1] or "", "office_name": row[2]}
            for row in senate_rows
        ]

        # Also try to get from congress_members table if it exists
        try:
            self.cursor.execute("SELECT COUNT(*) FROM congress_members")
            if self.cursor.fetchone()[0] > 0:
                self.cursor.execute("""
                    SELECT member_name, last_name, first_name, state, chamber, district
                    FROM congress_members
                    ORDER BY chamber, state, district
                """)
                all_members = self.cursor.fetchall()
                house_members = []
                senate_members = []
                for row in all_members:
                    member_name, last_name, first_name, state, chamber, district = row
                    # If last_name is empty, parse from member_name (format: "Last, First")
                    if not last_name or last_name.strip() == "":
                        if member_name and "," in member_name:
                            parts = member_name.split(",", 1)
                            last_name = parts[0].strip()
                            first_name = parts[1].strip() if len(parts) > 1 else ""
                        else:
                            continue
                    if chamber == "House":
                        house_members.append(
                            {
                                "last_name": last_name,
                                "first_name": first_name or "",
                                "state": state,
                                "district": district or "00",
                            }
                        )
                    elif chamber == "Senate":
                        senate_members.append(
                            {"last_name": last_name, "first_name": first_name or "", "state": state}
                        )
                logger.info(
                    f"Loaded {len(house_members)} House and {len(senate_members)} Senate members from congress_members table"
                )
        except Exception as e:
            logger.warning(f"Could not query congress_members table: {e}")

        self.stats["house_members_total"] = len(house_members)
        self.stats["senate_members_total"] = len(senate_members)

        # State name to code mapping for CapitolGains
        self.state_codes = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "District of Columbia": "DC",
        }

        logger.info(f"Loaded {len(house_members)} House members from house_financial_disclosures")
        logger.info(
            f"Loaded {len(senate_members)} Senate members from senate_financial_disclosures"
        )

        return house_members, senate_members

    def check_duplicate(self, table: str, year: int, name: str, filing_date: str = None) -> bool:
        """Check if a disclosure already exists in database."""
        if table == "house_financial_disclosures":
            self.cursor.execute(
                """
                SELECT COUNT(*) FROM house_financial_disclosures
                WHERE year = %s AND last_name = %s
            """,
                (year, name.split(",")[0] if "," in name else name.split()[-1]),
            )
        elif table == "senate_financial_disclosures":
            self.cursor.execute(
                """
                SELECT COUNT(*) FROM senate_financial_disclosures
                WHERE report_year = %s AND last_name = %s
            """,
                (year, name.split(",")[0] if "," in name else name.split()[-1]),
            )
        elif table == "congress_trading":
            self.cursor.execute(
                """
                SELECT COUNT(*) FROM congress_trading
                WHERE politician_name = %s AND transaction_date >= %s
            """,
                (name, f"{year}-01-01"),
            )
        else:
            return False

        return self.cursor.fetchone()[0] > 0

    def insert_house_disclosure(self, disclosure: Dict) -> bool:
        """Insert a House disclosure into database."""
        try:
            self.cursor.execute(
                """
                INSERT INTO house_financial_disclosures (
                    filing_id, year, last_name, first_name, suffix,
                    filing_type, state_dst, pdf_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (filing_id) DO NOTHING
            """,
                (
                    disclosure.get("filing_id"),
                    disclosure.get("year"),
                    disclosure.get("last_name"),
                    disclosure.get("first_name"),
                    disclosure.get("suffix"),
                    disclosure.get("filing_type"),
                    disclosure.get("state"),
                    disclosure.get("pdf_url"),
                ),
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error inserting House disclosure: {e}")
            self.conn.rollback()
            return False

    def insert_senate_disclosure(self, disclosure: Dict) -> bool:
        """Insert a Senate disclosure into database."""
        try:
            self.cursor.execute(
                """
                INSERT INTO senate_financial_disclosures (
                    report_id, first_name, last_name, office_name,
                    filing_type, report_year, date_received, pdf_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (report_id) DO NOTHING
            """,
                (
                    disclosure.get("report_id"),
                    disclosure.get("first_name"),
                    disclosure.get("last_name"),
                    disclosure.get("office_name"),
                    disclosure.get("filing_type"),
                    disclosure.get("report_year"),
                    disclosure.get("date_received"),
                    disclosure.get("pdf_url"),
                ),
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error inserting Senate disclosure: {e}")
            self.conn.rollback()
            return False

    def insert_trading_record(self, trade: Dict) -> bool:
        """Insert a trading record into database."""
        try:
            self.cursor.execute(
                """
                INSERT INTO congress_trading (
                    politician_name, politician_party, politician_state,
                    transaction_date, ticker, asset_name, asset_type,
                    transaction_type, amount_low, amount_high,
                    description, data_source, filing_date, disclosure_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """,
                (
                    trade.get("politician_name"),
                    trade.get("politician_party"),
                    trade.get("politician_state"),
                    trade.get("transaction_date"),
                    trade.get("ticker"),
                    trade.get("asset_name"),
                    trade.get("asset_type"),
                    trade.get("transaction_type"),
                    trade.get("amount_low"),
                    trade.get("amount_high"),
                    trade.get("description"),
                    trade.get("data_source"),
                    trade.get("filing_date"),
                    trade.get("disclosure_url"),
                ),
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error inserting trading record: {e}")
            self.conn.rollback()
            return False

    def process_house_member(self, member: Dict, scraper: HouseDisclosureScraper) -> Dict:
        """Process a single House member for all years."""
        results = {
            "member": member,
            "disclosures_found": 0,
            "disclosures_new": 0,
            "trading_found": 0,
            "trading_new": 0,
            "errors": [],
        }

        last_name = member["last_name"]
        first_name = member.get("first_name", "")
        state = member["state"]
        district = member.get("district", "00")

        # Convert full state name to 2-letter code for CapitolGains
        state_code = self.state_codes.get(state, state)

        logger.info(f"Processing House member: {last_name}, {first_name} ({state}-{district})")

        try:
            rep = Representative(last_name, state=state_code, district=district)

            for year in self.house_years:
                try:
                    # Get all disclosures
                    disclosures = rep.get_disclosures(scraper, year=str(year))

                    # Process all disclosure types
                    for dtype in [
                        "annual",
                        "amendments",
                        "blind_trust",
                        "extension",
                        "new_filer",
                        "termination",
                        "other",
                    ]:
                        for disclosure in disclosures.get(dtype, []):
                            results["disclosures_found"] += 1

                            # Check for duplicate
                            if self.check_duplicate("house_financial_disclosures", year, last_name):
                                self.stats["house_disclosures_duplicate"] += 1
                                continue

                            # Insert disclosure
                            disclosure_data = {
                                "filing_id": disclosure.get(
                                    "filing_id",
                                    f"{last_name}_{year}_{disclosure.get('filing_type', 'unknown')}",
                                ),
                                "year": year,
                                "last_name": last_name,
                                "first_name": first_name,
                                "suffix": "",
                                "filing_type": disclosure.get("filing_type", "unknown"),
                                "state": state,
                                "pdf_url": disclosure.get("pdf_url", ""),
                            }

                            if self.insert_house_disclosure(disclosure_data):
                                results["disclosures_new"] += 1
                                self.stats["house_disclosures_new"] += 1

                            self.stats["house_disclosures_found"] += 1

                    # Process trades
                    for trade in disclosures.get("trades", []):
                        results["trading_found"] += 1

                        # Check for duplicate (simplified)
                        if self.check_duplicate("congress_trading", year, last_name):
                            continue

                        # Insert trade
                        trade_data = {
                            "politician_name": f"{first_name} {last_name}"
                            if first_name
                            else last_name,
                            "politician_party": "",  # Would need to lookup
                            "politician_state": state,
                            "transaction_date": trade.get("transaction_date", f"{year}-01-01"),
                            "ticker": trade.get("ticker", ""),
                            "asset_name": trade.get("asset_name", ""),
                            "asset_type": trade.get("asset_type", ""),
                            "transaction_type": trade.get("transaction_type", ""),
                            "amount_low": trade.get("amount_low"),
                            "amount_high": trade.get("amount_high"),
                            "description": trade.get("description", ""),
                            "data_source": "CapitolGains",
                            "filing_date": trade.get("filing_date", f"{year}-12-31"),
                            "disclosure_url": trade.get("disclosure_url", ""),
                        }

                        if self.insert_trading_record(trade_data):
                            results["trading_new"] += 1
                            self.stats["trading_records_new"] += 1

                        self.stats["trading_records_found"] += 1

                    # Small delay to be respectful
                    time.sleep(0.5)

                except Exception as e:
                    logger.warning(f"Error processing year {year} for {last_name}: {e}")
                    results["errors"].append(str(e))
                    continue

            results["success"] = True

        except Exception as e:
            logger.error(f"Error processing House member {last_name}: {e}")
            results["success"] = False
            results["errors"].append(str(e))

        return results

    def process_senate_member(self, member: Dict, scraper: SenateDisclosureScraper) -> Dict:
        """Process a single Senate member for all years."""
        results = {
            "member": member,
            "disclosures_found": 0,
            "disclosures_new": 0,
            "trading_found": 0,
            "trading_new": 0,
            "errors": [],
        }

        last_name = member["last_name"]
        first_name = member.get("first_name", "")
        state = member.get("state", "")

        # Extract state from office_name if not provided
        if not state and "office_name" in member:
            # office_name format: "Senator Last Name (State)"
            import re

            match = re.search(r"\(([A-Z]{2})\)", member["office_name"])
            if match:
                state = match.group(1)

        # Convert full state name to 2-letter code if needed
        if state and len(state) > 2:
            state = self.state_codes.get(state, state)

        logger.info(f"Processing Senate member: {last_name}, {first_name} ({state})")

        if not state or len(state) != 2:
            logger.warning(f"Skipping {last_name} - invalid state: {state}")
            results["errors"].append(f"Invalid state: {state}")
            results["success"] = False
            return results

        try:
            sen = Senator(last_name, first_name=first_name, state=state)

            for year in self.senate_years:
                try:
                    disclosures = sen.get_disclosures(scraper, year=str(year))

                    # Process annual reports
                    for disclosure in disclosures.get("annual", []):
                        results["disclosures_found"] += 1

                        if self.check_duplicate("senate_financial_disclosures", year, last_name):
                            self.stats["senate_disclosures_duplicate"] += 1
                            continue

                        disclosure_data = {
                            "report_id": disclosure.get(
                                "report_id", f"SEN_{last_name}_{year}_annual"
                            ),
                            "first_name": first_name,
                            "last_name": last_name,
                            "office_name": f"Senator {last_name} ({state})",
                            "filing_type": "annual",
                            "report_year": year,
                            "date_received": disclosure.get("date_received", f"{year}-12-31"),
                            "pdf_url": disclosure.get("report_url", ""),
                        }

                        if self.insert_senate_disclosure(disclosure_data):
                            results["disclosures_new"] += 1
                            self.stats["senate_disclosures_new"] += 1

                        self.stats["senate_disclosures_found"] += 1

                    # Process amendments
                    for disclosure in disclosures.get("amendments", []):
                        results["disclosures_found"] += 1

                        if self.check_duplicate("senate_financial_disclosures", year, last_name):
                            self.stats["senate_disclosures_duplicate"] += 1
                            continue

                        disclosure_data = {
                            "report_id": disclosure.get(
                                "report_id", f"SEN_{last_name}_{year}_amendment"
                            ),
                            "first_name": first_name,
                            "last_name": last_name,
                            "office_name": f"Senator {last_name} ({state})",
                            "filing_type": "amendment",
                            "report_year": year,
                            "date_received": disclosure.get("date_received", f"{year}-12-31"),
                            "pdf_url": disclosure.get("report_url", ""),
                        }

                        if self.insert_senate_disclosure(disclosure_data):
                            results["disclosures_new"] += 1
                            self.stats["senate_disclosures_new"] += 1

                        self.stats["senate_disclosures_found"] += 1

                    # Process trades
                    for trade in disclosures.get("trades", []):
                        results["trading_found"] += 1

                        if self.check_duplicate("congress_trading", year, last_name):
                            continue

                        trade_data = {
                            "politician_name": f"{first_name} {last_name}"
                            if first_name
                            else last_name,
                            "politician_party": "",
                            "politician_state": state,
                            "transaction_date": trade.get("transaction_date", f"{year}-01-01"),
                            "ticker": trade.get("ticker", ""),
                            "asset_name": trade.get("asset_name", ""),
                            "asset_type": trade.get("asset_type", ""),
                            "transaction_type": trade.get("transaction_type", ""),
                            "amount_low": trade.get("amount_low"),
                            "amount_high": trade.get("amount_high"),
                            "description": trade.get("description", ""),
                            "data_source": "CapitolGains",
                            "filing_date": trade.get("filing_date", f"{year}-12-31"),
                            "disclosure_url": trade.get("disclosure_url", ""),
                        }

                        if self.insert_trading_record(trade_data):
                            results["trading_new"] += 1
                            self.stats["trading_records_new"] += 1

                        self.stats["trading_records_found"] += 1

                    time.sleep(0.5)

                except Exception as e:
                    logger.warning(f"Error processing year {year} for {last_name}: {e}")
                    results["errors"].append(str(e))
                    continue

            results["success"] = True

        except Exception as e:
            logger.error(f"Error processing Senate member {last_name}: {e}")
            results["success"] = False
            results["errors"].append(str(e))

        return results

    def save_checkpoint(self):
        """Save current progress to checkpoint file."""
        checkpoint = {"stats": self.stats, "timestamp": datetime.now().isoformat()}

        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(checkpoint, f, indent=2)

        logger.info(f"Checkpoint saved: {CHECKPOINT_FILE}")

    def run(self):
        """Run the complete bulk ingestion pipeline."""
        logger.info("=" * 80)
        logger.info("BULK FINANCIAL DISCLOSURE INGESTION - ALL MEMBERS, ALL YEARS")
        logger.info("=" * 80)

        # Get all members
        logger.info("Loading members from database...")
        house_members, senate_members = self.get_all_members_from_db()

        logger.info(
            f"Found {len(house_members)} House members and {len(senate_members)} Senate members"
        )

        # Process House members
        if house_members:
            logger.info("\n" + "=" * 80)
            logger.info("PROCESSING HOUSE MEMBERS")
            logger.info("=" * 80)

            with HouseDisclosureScraper(headless=True) as house_scraper:
                for i, member in enumerate(house_members):
                    logger.info(
                        f"\n[{i + 1}/{len(house_members)}] Processing House member: {member['last_name']}"
                    )

                    results = self.process_house_member(member, house_scraper)

                    if results["success"]:
                        self.stats["house_members_processed"] += 1
                    else:
                        self.stats["house_members_failed"] += 1

                    # Save checkpoint every 10 members
                    if (i + 1) % 10 == 0:
                        self.save_checkpoint()

        # Process Senate members
        if senate_members:
            logger.info("\n" + "=" * 80)
            logger.info("PROCESSING SENATE MEMBERS")
            logger.info("=" * 80)

            with SenateDisclosureScraper(headless=True) as senate_scraper:
                for i, member in enumerate(senate_members):
                    logger.info(
                        f"\n[{i + 1}/{len(senate_members)}] Processing Senate member: {member['last_name']}"
                    )

                    results = self.process_senate_member(member, senate_scraper)

                    if results["success"]:
                        self.stats["senate_members_processed"] += 1
                    else:
                        self.stats["senate_members_failed"] += 1

                    # Save checkpoint every 5 members
                    if (i + 1) % 5 == 0:
                        self.save_checkpoint()

        # Final statistics
        self.stats["end_time"] = datetime.now().isoformat()
        self.save_checkpoint()

        self.print_summary()

    def print_summary(self):
        """Print final summary statistics."""
        logger.info("\n" + "=" * 80)
        logger.info("INGESTION COMPLETE - SUMMARY")
        logger.info("=" * 80)

        logger.info("\nHouse Members:")
        logger.info(f"  Total: {self.stats['house_members_total']}")
        logger.info(f"  Processed: {self.stats['house_members_processed']}")
        logger.info(f"  Failed: {self.stats['house_members_failed']}")
        logger.info(f"  Disclosures Found: {self.stats['house_disclosures_found']}")
        logger.info(f"  Disclosures New: {self.stats['house_disclosures_new']}")
        logger.info(f"  Disclosures Duplicate: {self.stats['house_disclosures_duplicate']}")

        logger.info("\nSenate Members:")
        logger.info(f"  Total: {self.stats['senate_members_total']}")
        logger.info(f"  Processed: {self.stats['senate_members_processed']}")
        logger.info(f"  Failed: {self.stats['senate_members_failed']}")
        logger.info(f"  Disclosures Found: {self.stats['senate_disclosures_found']}")
        logger.info(f"  Disclosures New: {self.stats['senate_disclosures_new']}")
        logger.info(f"  Disclosures Duplicate: {self.stats['senate_disclosures_duplicate']}")

        logger.info("\nTrading Records:")
        logger.info(f"  Found: {self.stats['trading_records_found']}")
        logger.info(f"  New: {self.stats['trading_records_new']}")

        logger.info(f"\nTime: {self.stats['start_time']} to {self.stats.get('end_time', 'N/A')}")
        logger.info("=" * 80)


if __name__ == "__main__":
    try:
        conn = get_db_connection()
        pipeline = BulkIngestionPipeline(conn)
        pipeline.run()
        conn.close()

        logger.info("\n✅ Bulk ingestion complete!")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
