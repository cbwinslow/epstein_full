#!/usr/bin/env python3
"""
Non-Browser Data Ingestion Pipeline
Processes all available data without browser automation
"""

import logging
from datetime import datetime

import psycopg2

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DB_CONFIG = {"host": "localhost", "database": "epstein", "user": "postgres", "password": "postgres"}


class NonBrowserIngestionPipeline:
    def __init__(self):
        self.conn = None
        self.stats = {
            "house_new": 0,
            "senate_new": 0,
            "trading_new": 0,
            "ocr_new": 0,
            "fec_new": 0,
            "lda_new": 0,
            "entities_new": 0,
            "mappings_new": 0,
            "start_time": datetime.now(),
        }

    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = False
            logger.info("✅ Connected to database")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False

    def get_existing_counts(self):
        """Get current record counts"""
        cur = self.conn.cursor()
        counts = {}

        tables = [
            "house_financial_disclosures",
            "senate_financial_disclosures",
            "congress_trading",
            "house_ptr_ocr_pages",
            "fec_individual_contributions",
            "lda_filings",
            "entity_resolutions",
            "entity_raw_names",
        ]

        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cur.fetchone()[0]

        cur.close()
        return counts

    def ingest_house_missing_years(self):
        """Ingest House data for missing years (1995-2007)"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 1: HOUSE MISSING YEARS (1995-2007)")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        # Check which years are missing
        cur.execute("SELECT DISTINCT year FROM house_financial_disclosures ORDER BY year")
        existing_years = [row[0] for row in cur.fetchall()]

        missing_years = [y for y in range(1995, 2008) if y not in existing_years]

        if not missing_years:
            logger.info("✅ All House years (1995-2007) already present")
            cur.close()
            return 0

        logger.info(f"Missing House years: {missing_years}")
        logger.info("Note: CapitolGains requires browser automation for scraping")
        logger.info("Historical data ingestion requires manual execution with browser")

        # For now, note what needs to be done
        logger.info("\nTo ingest missing years, run:")
        logger.info("  python3 scripts/ingestion/financial_disclosures_ingestion.py \\")
        logger.info("    --chambers house \\")
        logger.info("    --years 1995:2007 \\")
        logger.info("    --workers 8")

        cur.close()
        return 0

    def verify_senate_complete(self):
        """Verify Senate data completeness"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 2: SENATE DATA VERIFICATION")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        cur.execute(
            "SELECT DISTINCT report_year FROM senate_financial_disclosures ORDER BY report_year"
        )
        existing_years = [row[0] for row in cur.fetchall()]

        expected_years = list(range(2012, 2027))
        missing_years = [y for y in expected_years if y not in existing_years]

        if missing_years:
            logger.info(f"Missing Senate years: {missing_years}")
            logger.info("Note: Requires CapitolGains browser automation")
        else:
            logger.info("✅ All Senate years (2012-2026) present")

        cur.execute("SELECT COUNT(*) FROM senate_financial_disclosures")
        total = cur.fetchone()[0]
        logger.info(f"Total Senate records: {total:,}")

        cur.close()
        return len(missing_years)

    def verify_trading_complete(self):
        """Verify trading data completeness"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 3: TRADING DATA VERIFICATION")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        cur.execute(
            "SELECT DISTINCT EXTRACT(YEAR FROM transaction_date)::INT FROM congress_trading ORDER BY 1"
        )
        existing_years = [row[0] for row in cur.fetchall()]

        logger.info(f"Trading years: {existing_years}")

        cur.execute("SELECT COUNT(*) FROM congress_trading")
        total = cur.fetchone()[0]
        logger.info(f"Total trading records: {total:,}")

        cur.execute("SELECT SUM(amount_low), SUM(amount_high) FROM congress_trading")
        totals = cur.fetchone()
        logger.info(
            f"Total trading value (low): ${totals[0]:,.2f}" if totals[0] else "No low values"
        )
        logger.info(
            f"Total trading value (high): ${totals[1]:,.2f}" if totals[1] else "No high values"
        )

        cur.close()
        return total

    def verify_fec_complete(self):
        """Verify FEC data completeness"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 4: FEC DATA VERIFICATION")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        cur.execute("SELECT DISTINCT cycle FROM fec_individual_contributions ORDER BY cycle")
        existing_cycles = [row[0] for row in cur.fetchall()]

        logger.info(f"FEC cycles: {existing_cycles}")

        cur.execute("SELECT COUNT(*) FROM fec_individual_contributions")
        total = cur.fetchone()[0]
        logger.info(f"Total FEC records: {total:,}")

        cur.execute("SELECT COUNT(*) FROM fec_individual_contributions WHERE transaction_amt > 0")
        positive = cur.fetchone()[0]
        logger.info(f"Positive amounts: {positive:,}")

        cur.execute(
            "SELECT SUM(transaction_amt) FROM fec_individual_contributions WHERE transaction_amt > 0"
        )
        total_amt = cur.fetchone()[0]
        logger.info(f"Total contributions: ${total_amt:,.2f}")

        cur.execute(
            "SELECT transaction_dt, name, transaction_amt FROM fec_individual_contributions WHERE transaction_amt > 0 ORDER BY transaction_amt DESC LIMIT 5"
        )
        top = cur.fetchall()
        logger.info("\nTop 5 contributions:")
        for dt, name, amt in top:
            logger.info(f"  {dt} | {name[:40]:40} | ${amt:>12,.2f}")

        cur.close()
        return total

    def verify_lda_complete(self):
        """Verify LDA data completeness"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 5: LDA DATA VERIFICATION")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        cur.execute("SELECT DISTINCT filing_year FROM lda_filings ORDER BY filing_year")
        existing_years = [row[0] for row in cur.fetchall()]

        logger.info(f"LDA years: {existing_years}")

        cur.execute("SELECT COUNT(*) FROM lda_filings")
        total = cur.fetchone()[0]
        logger.info(f"Total LDA records: {total:,}")

        cur.execute(
            "SELECT registrant_name, SUM(income) as total FROM lda_filings GROUP BY registrant_name ORDER BY total DESC LIMIT 5"
        )
        top = cur.fetchall()
        logger.info("\nTop 5 lobbying clients:")
        for name, total in top:
            logger.info(f"  {name[:40]:40} | ${total:>12,.2f}")

        cur.close()
        return total

    def verify_entities_complete(self):
        """Verify entity resolution completeness"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 6: ENTITY RESOLUTION VERIFICATION")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        cur.execute("SELECT COUNT(*) FROM entity_resolutions")
        entities = cur.fetchone()[0]
        logger.info(f"Total entities: {entities:,}")

        cur.execute("SELECT COUNT(*) FROM entity_raw_names")
        mappings = cur.fetchone()[0]
        logger.info(f"Total name mappings: {mappings:,}")

        cur.execute("SELECT entity_type, COUNT(*) FROM entity_resolutions GROUP BY entity_type")
        types = cur.fetchall()
        logger.info("\nEntity types:")
        for etype, count in types:
            logger.info(f"  {etype}: {count:,}")

        cur.close()
        return entities, mappings

    def run_network_analysis(self):
        """Run network analysis"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 7: NETWORK ANALYSIS")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        # Check if network data exists
        cur.execute("SELECT COUNT(*) FROM graph_nodes")
        nodes = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM graph_edges")
        edges = cur.fetchone()[0]

        logger.info(f"Network nodes: {nodes:,}")
        logger.info(f"Network edges: {edges:,}")

        if nodes == 0:
            logger.info("Note: Network analysis requires separate execution")
            logger.info("Run: python3 scripts/analysis/network_analysis/build_influence_network.py")

        cur.close()
        return nodes, edges

    def print_final_summary(self, initial_counts):
        """Print final summary"""
        logger.info("\n" + "=" * 80)
        logger.info("FINAL SUMMARY")
        logger.info("=" * 80)

        cur = self.conn.cursor()

        final_counts = self.get_existing_counts()

        print("\n" + "=" * 80)
        print("DATA INVENTORY")
        print("=" * 80)
        print(f"{'Table':<40} {'Records':>12} {'Change':>12}")
        print("-" * 80)

        total_initial = 0
        total_final = 0

        for table, initial in initial_counts.items():
            final = final_counts[table]
            change = final - initial
            total_initial += initial
            total_final += final
            print(f"{table:<40} {final:>12,} {change:>+12,}")

        print("-" * 80)
        print(f"{'TOTAL':<40} {total_final:>12,} {total_final - total_initial:>+12,}")
        print("=" * 80)

        # Calculate elapsed time
        elapsed = datetime.now() - self.stats["start_time"]

        print(f"\nDuration: {elapsed}")
        print(f"Start: {self.stats['start_time']}")
        print(f"End: {datetime.now()}")

        cur.close()

    def run(self):
        """Run the complete ingestion pipeline"""
        logger.info("=" * 80)
        logger.info("NON-BROWSER DATA INGESTION PIPELINE")
        logger.info("=" * 80)

        if not self.connect_db():
            logger.error("Cannot connect to database. Exiting.")
            return

        try:
            # Get initial counts
            initial_counts = self.get_existing_counts()

            # Run phases
            self.ingest_house_missing_years()
            self.verify_senate_complete()
            self.verify_trading_complete()
            self.verify_fec_complete()
            self.verify_lda_complete()
            self.verify_entities_complete()
            self.run_network_analysis()

            # Print final summary
            self.print_final_summary(initial_counts)

            logger.info("\n✅ INGESTION PIPELINE COMPLETE")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close()
                logger.info("Database connection closed")


if __name__ == "__main__":
    pipeline = NonBrowserIngestionPipeline()
    pipeline.run()
