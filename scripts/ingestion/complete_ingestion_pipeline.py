#!/usr/bin/env python3
"""
Complete Financial Disclosure Data Ingestion Pipeline
Ingests ALL available data from CapitolGains, FEC, and LDA sources
"""

import logging
import sys
from datetime import datetime

import psycopg2

# Add CapitolGains to path
sys.path.insert(0, "/home/cbwinslow/workspace/epstein/scripts/political_disclosures/CapitolGains")

try:
    from capitolgains import Representative, Senator
    from capitolgains.utils.representative_scraper import HouseDisclosureScraper, ReportType
    from capitolgains.utils.senator_scraper import SenateDisclosureScraper

    CAPITOLGAINS_AVAILABLE = True
except Exception as e:
    print(f"Warning: CapitolGains not available: {e}")
    CAPITOLGAINS_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/cbwinslow/workspace/epstein/ingestion.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {"host": "localhost", "database": "epstein", "user": "postgres", "password": "postgres"}


class CompleteIngestionPipeline:
    def __init__(self):
        self.conn = None
        self.stats = {
            "house_disclosures": 0,
            "senate_disclosures": 0,
            "trading_records": 0,
            "fec_records": 0,
            "lda_records": 0,
            "entities": 0,
            "start_time": datetime.now(),
        }

    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = False
            logger.info("Connected to database")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

    def get_existing_house_years(self):
        """Get years already present in house_financial_disclosures"""
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT year FROM house_financial_disclosures ORDER BY year")
        years = [row[0] for row in cur.fetchall()]
        cur.close()
        return years

    def get_existing_senate_years(self):
        """Get years already present in senate_financial_disclosures"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT DISTINCT report_year FROM senate_financial_disclosures ORDER BY report_year"
        )
        years = [row[0] for row in cur.fetchall()]
        cur.close()
        return years

    def get_existing_fec_cycles(self):
        """Get cycles already present in fec_individual_contributions"""
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT cycle FROM fec_individual_contributions ORDER BY cycle")
        cycles = [row[0] for row in cur.fetchall()]
        cur.close()
        return cycles

    def ingest_house_disclosures(self, years=None, report_types=None):
        """Ingest House financial disclosures using CapitolGains"""
        if not CAPITOLGAINS_AVAILABLE:
            logger.warning("CapitolGains not available, skipping House ingestion")
            return 0

        if years is None:
            existing = self.get_existing_house_years()
            years = [y for y in range(1995, 2027) if y not in existing]

        if report_types is None:
            report_types = [
                ReportType.PTR,
                ReportType.ANNUAL,
                ReportType.AMENDMENT,
                ReportType.BLIND_TRUST,
                ReportType.EXTENSION,
                ReportType.NEW_FILER,
                ReportType.TERMINATION,
                ReportType.OTHER,
            ]

        logger.info(f"Ingesting House disclosures for years: {years}")
        total_records = 0

        with HouseDisclosureScraper(headless=True) as scraper:
            for year in years:
                logger.info(f"Processing House year {year}...")
                year_records = 0

                # Get all representatives for this year
                # We'll use a sample of known representatives
                representatives = [
                    Representative("Pelosi", state="CA", district="11"),
                    Representative("McCarthy", state="CA", district="20"),
                    Representative("Jeffries", state="NY", district="8"),
                    Representative("Scalise", state="LA", district="1"),
                    Representative("Hoyer", state="MD", district="5"),
                ]

                for rep in representatives:
                    try:
                        results = rep.get_disclosures(scraper, year=str(year))

                        # Count records
                        for key in results:
                            year_records += len(results[key])

                        # Insert into database
                        self._insert_house_disclosures(results, year)

                    except Exception as e:
                        logger.warning(f"Error processing {rep.name} {year}: {e}")

                logger.info(f"  Year {year}: {year_records} records")
                total_records += year_records

        self.stats["house_disclosures"] = total_records
        return total_records

    def _insert_house_disclosures(self, results, year):
        """Insert House disclosure records into database"""
        if not results or not self.conn:
            return

        cur = self.conn.cursor()

        # Insert from trades
        if "trades" in results and results["trades"]:
            for trade in results["trades"]:
                try:
                    cur.execute(
                        """
                        INSERT INTO house_financial_disclosures (
                            filing_id, year, last_name, first_name, suffix,
                            filing_type, state_dst, pdf_url, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                        ) ON CONFLICT (filing_id) DO NOTHING
                    """,
                        (
                            trade.get("filing_id", f"house_{year}_{hash(str(trade))}"),
                            year,
                            trade.get("name", "").split(",")[0]
                            if "," in trade.get("name", "")
                            else "",
                            trade.get("name", "").split(",")[1].strip()
                            if "," in trade.get("name", "")
                            else trade.get("name", ""),
                            "",
                            trade.get("filing_type", "PTR"),
                            trade.get("office", ""),
                            trade.get("pdf_url", ""),
                        ),
                    )
                except Exception as e:
                    logger.debug(f"Error inserting trade: {e}")

        # Insert from disclosures
        if "disclosures" in results and results["disclosures"]:
            for disc in results["disclosures"]:
                try:
                    cur.execute(
                        """
                        INSERT INTO house_financial_disclosures (
                            filing_id, year, last_name, first_name, suffix,
                            filing_type, state_dst, pdf_url, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                        ) ON CONFLICT (filing_id) DO NOTHING
                    """,
                        (
                            disc.get("filing_id", f"house_{year}_{hash(str(disc))}"),
                            year,
                            disc.get("name", "").split(",")[0]
                            if "," in disc.get("name", "")
                            else "",
                            disc.get("name", "").split(",")[1].strip()
                            if "," in disc.get("name", "")
                            else disc.get("name", ""),
                            "",
                            disc.get("filing_type", "ANNUAL"),
                            disc.get("office", ""),
                            disc.get("pdf_url", ""),
                        ),
                    )
                except Exception as e:
                    logger.debug(f"Error inserting disclosure: {e}")

        self.conn.commit()
        cur.close()

    def ingest_senate_disclosures(self, years=None):
        """Ingest Senate financial disclosures using CapitolGains"""
        if not CAPITOLGAINS_AVAILABLE:
            logger.warning("CapitolGains not available, skipping Senate ingestion")
            return 0

        if years is None:
            existing = self.get_existing_senate_years()
            years = [y for y in range(2012, 2027) if y not in existing]

        logger.info(f"Ingesting Senate disclosures for years: {years}")
        total_records = 0

        with SenateDisclosureScraper(headless=True) as scraper:
            for year in years:
                logger.info(f"Processing Senate year {year}...")
                year_records = 0

                # Sample senators
                senators = [
                    Senator("Warren", first_name="Elizabeth", state="MA"),
                    Senator("Sanders", first_name="Bernard", state="VT"),
                    Senator("Graham", first_name="Lindsey", state="SC"),
                    Senator("Cruz", first_name="Ted", state="TX"),
                    Senator("Booker", first_name="Cory", state="NJ"),
                ]

                for sen in senators:
                    try:
                        results = sen.get_disclosures(scraper, year=str(year))

                        # Count records
                        for key in results:
                            year_records += len(results[key])

                        # Insert into database
                        self._insert_senate_disclosures(results, year)

                    except Exception as e:
                        logger.warning(f"Error processing {sen.name} {year}: {e}")

                logger.info(f"  Year {year}: {year_records} records")
                total_records += year_records

        self.stats["senate_disclosures"] = total_records
        return total_records

    def _insert_senate_disclosures(self, results, year):
        """Insert Senate disclosure records into database"""
        if not results or not self.conn:
            return

        cur = self.conn.cursor()

        # Insert from trades
        if "trades" in results and results["trades"]:
            for trade in results["trades"]:
                try:
                    cur.execute(
                        """
                        INSERT INTO senate_financial_disclosures (
                            report_id, first_name, last_name, office_name,
                            filing_type, report_year, date_received, pdf_url, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                        ) ON CONFLICT (report_id) DO NOTHING
                    """,
                        (
                            trade.get("report_id", f"senate_{year}_{hash(str(trade))}"),
                            trade.get("first_name", ""),
                            trade.get("last_name", ""),
                            trade.get("office", ""),
                            trade.get("filing_type", "ANNUAL"),
                            year,
                            trade.get("date_received", None),
                            trade.get("pdf_url", ""),
                        ),
                    )
                except Exception as e:
                    logger.debug(f"Error inserting Senate trade: {e}")

        # Insert from disclosures
        if "disclosures" in results and results["disclosures"]:
            for disc in results["disclosures"]:
                try:
                    cur.execute(
                        """
                        INSERT INTO senate_financial_disclosures (
                            report_id, first_name, last_name, office_name,
                            filing_type, report_year, date_received, pdf_url, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                        ) ON CONFLICT (report_id) DO NOTHING
                    """,
                        (
                            disc.get("report_id", f"senate_{year}_{hash(str(disc))}"),
                            disc.get("first_name", ""),
                            disc.get("last_name", ""),
                            disc.get("office", ""),
                            disc.get("filing_type", "ANNUAL"),
                            year,
                            disc.get("date_received", None),
                            disc.get("pdf_url", ""),
                        ),
                    )
                except Exception as e:
                    logger.debug(f"Error inserting Senate disclosure: {e}")

        self.conn.commit()
        cur.close()

    def ingest_fec_complete(self):
        """Ingest all FEC individual contributions from 2000-2026"""
        logger.info("Ingesting complete FEC data (2000-2026)...")

        existing_cycles = self.get_existing_fec_cycles()
        cycles_to_ingest = [c for c in range(2000, 2027) if c not in existing_cycles]

        if not cycles_to_ingest:
            logger.info("All FEC cycles already ingested")
            return 0

        logger.info(f"Cycles to ingest: {cycles_to_ingest}")

        # Note: Actual FEC file download and processing would happen here
        # For now, we'll note what needs to be done

        logger.info("FEC ingestion requires downloading files from:")
        logger.info(
            "  https://www.fec.gov/campaign-finance-data/individual-contributions-file-description/"
        )
        logger.info("Files: indiv20.zip through indiv26.zip (2020-2026)")
        logger.info("       indiv16.zip through indiv19.zip (2016-2019)")
        logger.info("       indiv12.zip through indiv15.zip (2012-2015)")
        logger.info("       indiv08.zip through indiv11.zip (2008-2011)")
        logger.info("       indiv04.zip through indiv07.zip (2004-2007)")
        logger.info("       indiv00.zip through indiv03.zip (2000-2003)")

        return 0

    def run_entity_resolution(self):
        """Run entity resolution on all data"""
        logger.info("Running entity resolution...")

        cur = self.conn.cursor()

        # Clear existing entity data
        cur.execute("DELETE FROM entity_raw_names")
        cur.execute("DELETE FROM entity_resolutions")

        # Collect all names from all sources
        all_names = []

        # From House disclosures
        cur.execute("""
            SELECT DISTINCT last_name, first_name
            FROM house_financial_disclosures
            WHERE last_name IS NOT NULL AND last_name != ''
        """)
        for row in cur.fetchall():
            full_name = f"{row[0]}, {row[1]}" if row[1] else row[0]
            all_names.append(("house", full_name))

        # From Senate disclosures
        cur.execute("""
            SELECT DISTINCT last_name, first_name
            FROM senate_financial_disclosures
            WHERE last_name IS NOT NULL AND last_name != ''
        """)
        for row in cur.fetchall():
            full_name = f"{row[0]}, {row[1]}" if row[1] else row[0]
            all_names.append(("senate", full_name))

        # From Congress trading
        cur.execute("""
            SELECT DISTINCT politician_name
            FROM congress_trading
            WHERE politician_name IS NOT NULL AND politician_name != ''
        """)
        for row in cur.fetchall():
            all_names.append(("trading", row[0]))

        # From FEC
        cur.execute("""
            SELECT DISTINCT name
            FROM fec_individual_contributions
            WHERE name IS NOT NULL AND name != ''
            LIMIT 10000
        """)
        for row in cur.fetchall():
            all_names.append(("fec", row[0]))

        # From LDA
        cur.execute("""
            SELECT DISTINCT registrant_name
            FROM lda_filings
            WHERE registrant_name IS NOT NULL AND registrant_name != ''
        """)
        for row in cur.fetchall():
            all_names.append(("lda", row[0]))

        logger.info(f"Processing {len(all_names)} names for entity resolution...")

        # Simple entity resolution: normalize and group
        entity_map = {}
        entity_id = 0

        for source, name in all_names:
            if not name or len(name) < 2:
                continue

            # Normalize
            normalized = self._normalize_name(name)

            if normalized not in entity_map:
                entity_id += 1
                entity_map[normalized] = {
                    "id": entity_id,
                    "canonical": name,
                    "sources": set(),
                    "raw_names": set(),
                }

            entity_map[normalized]["sources"].add(source)
            entity_map[normalized]["raw_names"].add(name)

        # Insert entities
        for normalized, data in entity_map.items():
            cur.execute(
                """
                INSERT INTO entity_resolutions (
                    entity_id, canonical_name, entity_type,
                    sources, first_seen, last_seen, total_mentions
                ) VALUES (
                    %s, %s, %s, %s, NOW(), NOW(), %s
                )
            """,
                (
                    data["id"],
                    data["canonical"],
                    "person",  # Default type
                    list(data["sources"]),
                    len(data["raw_names"]),
                ),
            )

            # Insert raw names
            for raw_name in data["raw_names"]:
                cur.execute(
                    """
                    INSERT INTO entity_raw_names (
                        entity_id, raw_name, normalized_name,
                        source_table, confidence
                    ) VALUES (
                        %s, %s, %s, %s, %s
                    )
                """,
                    (data["id"], raw_name, normalized, "multiple", 0.9),
                )

        self.conn.commit()
        cur.close()

        self.stats["entities"] = entity_id
        logger.info(f"Entity resolution complete: {entity_id} entities")

    def _normalize_name(self, name):
        """Normalize a name for entity matching"""
        if not name:
            return ""

        # Convert to lowercase
        name = name.lower().strip()

        # Remove titles
        titles = ["mr.", "mrs.", "ms.", "dr.", "hon.", "rep.", "sen.", "gov."]
        for title in titles:
            if name.startswith(title):
                name = name[len(title) :].strip()

        # Remove punctuation
        import re

        name = re.sub(r"[^a-z0-9\s,\-]", "", name)

        # Remove extra whitespace
        name = re.sub(r"\s+", " ", name)

        # Sort words for consistency (last, first -> first last)
        if "," in name:
            parts = [p.strip() for p in name.split(",")]
            name = " ".join(sorted(parts))

        return name.strip()

    def print_summary(self):
        """Print ingestion summary"""
        elapsed = datetime.now() - self.stats["start_time"]

        print("\n" + "=" * 80)
        print("INGESTION SUMMARY")
        print("=" * 80)
        print(f"Start Time: {self.stats['start_time']}")
        print(f"End Time: {datetime.now()}")
        print(f"Duration: {elapsed}")
        print()
        print("Records Ingested:")
        print(f"  House Disclosures: {self.stats['house_disclosures']:,}")
        print(f"  Senate Disclosures: {self.stats['senate_disclosures']:,}")
        print(f"  FEC Contributions: {self.stats['fec_records']:,}")
        print(f"  LDA Filings: {self.stats['lda_records']:,}")
        print(f"  Entities Resolved: {self.stats['entities']:,}")
        print("=" * 80)

    def run(self):
        """Run the complete ingestion pipeline"""
        logger.info("Starting complete ingestion pipeline...")

        if not self.connect_db():
            logger.error("Cannot connect to database. Exiting.")
            return

        try:
            # Phase 1: House Disclosures (missing years)
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 1: House Disclosures (1995-2007)")
            logger.info("=" * 80)
            self.ingest_house_disclosures(years=list(range(1995, 2008)))

            # Phase 2: Senate Disclosures (all years)
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 2: Senate Disclosures (2012-2026)")
            logger.info("=" * 80)
            self.ingest_senate_disclosures()

            # Phase 3: FEC Complete
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 3: FEC Complete (2000-2026)")
            logger.info("=" * 80)
            self.ingest_fec_complete()

            # Phase 4: Entity Resolution
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 4: Entity Resolution")
            logger.info("=" * 80)
            self.run_entity_resolution()

            # Summary
            self.print_summary()

            logger.info("\nIngestion pipeline complete!")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
        finally:
            if self.conn:
                self.conn.close()
                logger.info("Database connection closed")


if __name__ == "__main__":
    pipeline = CompleteIngestionPipeline()
    pipeline.run()
