#!/usr/bin/env python3
"""
Complete FEC Data Ingestion - All Cycles 2000-2026
"""

import logging
import os
from datetime import datetime

import psycopg2
from psycopg2.extras import execute_batch

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DB_CONFIG = {"host": "localhost", "database": "epstein", "user": "postgres", "password": "postgres"}


class FECIngestionPipeline:
    def __init__(self):
        self.conn = None
        self.stats = {"fec_records": 0, "start_time": datetime.now()}

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

    def get_existing_cycles(self):
        """Get cycles already present in fec_individual_contributions"""
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT cycle FROM fec_individual_contributions ORDER BY cycle")
        cycles = [row[0] for row in cur.fetchall()]
        cur.close()
        return cycles

    def get_fec_file_path(self, cycle):
        """Get path to FEC data file for given cycle"""
        base_dir = "/home/cbwinslow/workspace/epstein/epstein-data/raw-files/fec"

        # Check for different file naming conventions
        possible_files = [
            f"{base_dir}/indiv{cycle % 100:02d}.zip",
            f"{base_dir}/indiv{cycle % 100:02d}.txt",
            f"{base_dir}/itcont{cycle}.txt",
            f"{base_dir}/itcont{cycle}.zip",
        ]

        for f in possible_files:
            if os.path.exists(f):
                return f

        return None

    def ingest_fec_cycle(self, cycle):
        """Ingest FEC data for a specific cycle"""
        logger.info(f"Ingesting FEC cycle {cycle}...")

        file_path = self.get_fec_file_path(cycle)
        if not file_path:
            logger.warning(f"  No FEC file found for cycle {cycle}")
            return 0

        logger.info(f"  Found file: {file_path}")

        # Check if already ingested
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM fec_individual_contributions WHERE cycle = %s", (cycle,))
        existing = cur.fetchone()[0]

        if existing > 0:
            logger.info(f"  Cycle {cycle} already has {existing:,} records, skipping")
            cur.close()
            return 0

        # Read and parse the file
        records_inserted = 0

        try:
            # Handle ZIP files
            if file_path.endswith(".zip"):
                import zipfile

                with zipfile.ZipFile(file_path, "r") as zf:
                    # Find the .txt file inside
                    txt_files = [f for f in zf.namelist() if f.endswith(".txt")]
                    if not txt_files:
                        logger.warning(f"  No .txt file in zip {file_path}")
                        return 0

                    with zf.open(txt_files[0]) as f:
                        records_inserted = self._parse_fec_file(f, cycle, cur)
            else:
                # Plain text file
                with open(file_path, "r", encoding="latin-1", errors="ignore") as f:
                    records_inserted = self._parse_fec_file(f, cycle, cur)

            self.conn.commit()
            cur.close()

            logger.info(f"  Inserted {records_inserted:,} records for cycle {cycle}")
            return records_inserted

        except Exception as e:
            logger.error(f"  Error processing cycle {cycle}: {e}")
            self.conn.rollback()
            cur.close()
            return 0

    def _parse_fec_file(self, file_obj, cycle, cursor):
        """Parse FEC contribution file and insert into database"""
        records = []
        batch_size = 10000

        for line_num, line in enumerate(file_obj, 1):
            # Handle both bytes and string
            if isinstance(line, bytes):
                line = line.decode("latin-1", errors="ignore")

            line = line.rstrip("\n\r")

            # Skip header lines (starting with specific prefixes)
            if line.startswith("HDR") or line.startswith("FEC") or line.startswith("C"):
                continue

            # Parse fixed-width FEC format
            # See: https://www.fec.gov/campaign-finance-data/individual-contributions-file-description/
            try:
                record = {
                    "cmte_id": line[0:9].strip(),
                    "amndt_ind": line[9:10].strip(),
                    "rpt_tp": line[10:12].strip(),
                    "transaction_pgi": line[12:13].strip(),
                    "image_num": line[13:23].strip(),
                    "transaction_tp": line[23:25].strip(),
                    "entity_tp": line[25:27].strip(),
                    "name": line[27:76].strip(),
                    "city": line[76:116].strip(),
                    "state": line[116:118].strip(),
                    "zip_code": line[118:123].strip(),
                    "employer": line[123:163].strip(),
                    "occupation": line[163:203].strip(),
                    "transaction_dt": line[203:211].strip(),
                    "transaction_amt": line[211:222].strip(),
                    "other_id": line[222:232].strip(),
                    "tran_id": line[232:242].strip(),
                    "file_num": line[242:252].strip(),
                    "memo_cd": line[252:253].strip(),
                    "memo_text": line[253:258].strip(),
                    "sub_id": line[258:268].strip(),
                }

                # Parse transaction amount (in cents, can be negative)
                amt_str = record["transaction_amt"]
                if amt_str:
                    try:
                        # FEC amounts are in cents with implied decimal
                        amt_cents = int(amt_str)
                        amt_dollars = amt_cents / 100.0
                    except ValueError:
                        amt_dollars = 0.0
                else:
                    amt_dollars = 0.0

                # Parse transaction date (MMDDYYYY)
                dt_str = record["transaction_dt"]
                if dt_str and len(dt_str) == 8:
                    try:
                        trans_date = f"{dt_str[4:8]}-{dt_str[0:2]}-{dt_str[2:4]}"
                    except:
                        trans_date = None
                else:
                    trans_date = None

                records.append(
                    (
                        record["cmte_id"],
                        record["amndt_ind"],
                        record["rpt_tp"],
                        record["transaction_pgi"],
                        record["image_num"],
                        record["transaction_tp"],
                        record["entity_tp"],
                        record["name"],
                        record["city"],
                        record["state"],
                        record["zip_code"],
                        record["employer"],
                        record["occupation"],
                        trans_date,
                        amt_dollars,
                        record["other_id"],
                        record["tran_id"],
                        record["file_num"],
                        record["memo_cd"],
                        record["memo_text"],
                        record["sub_id"],
                        cycle,
                    )
                )

                # Batch insert
                if len(records) >= batch_size:
                    execute_batch(
                        cursor,
                        """
                        INSERT INTO fec_individual_contributions (
                            cmte_id, amndt_ind, rpt_tp, transaction_pgi,
                            image_num, transaction_tp, entity_tp, name,
                            city, state, zip_code, employer, occupation,
                            transaction_dt, transaction_amt, other_id,
                            tran_id, file_num, memo_cd, memo_text, sub_id, cycle
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """,
                        records,
                        page_size=batch_size,
                    )

                    records_inserted += len(records)
                    records = []

                    if records_inserted % 100000 == 0:
                        logger.info(f"    Processed {records_inserted:,} records...")

            except Exception as e:
                if line_num <= 10:
                    # Skip header/format lines
                    continue
                logger.debug(f"    Error parsing line {line_num}: {e}")
                continue

        # Insert remaining records
        if records:
            execute_batch(
                cursor,
                """
                INSERT INTO fec_individual_contributions (
                    cmte_id, amndt_ind, rpt_tp, transaction_pgi,
                    image_num, transaction_tp, entity_tp, name,
                    city, state, zip_code, employer, occupation,
                    transaction_dt, transaction_amt, other_id,
                    tran_id, file_num, memo_cd, memo_text, sub_id, cycle
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """,
                records,
                page_size=batch_size,
            )
            records_inserted += len(records)

        return records_inserted

    def run(self):
        """Run the complete FEC ingestion pipeline"""
        logger.info("=" * 80)
        logger.info("FEC COMPLETE INGESTION PIPELINE")
        logger.info("=" * 80)

        if not self.connect_db():
            logger.error("Cannot connect to database. Exiting.")
            return

        try:
            # Get existing cycles
            existing = self.get_existing_cycles()
            logger.info(f"Existing cycles in database: {existing}")

            # Cycles to ingest (2000-2026)
            all_cycles = list(range(2000, 2027))
            cycles_to_ingest = [c for c in all_cycles if c not in existing]

            if not cycles_to_ingest:
                logger.info("All cycles already ingested!")

                # Show summary
                cur = self.conn.cursor()
                cur.execute("SELECT COUNT(*) FROM fec_individual_contributions")
                total = cur.fetchone()[0]
                cur.execute(
                    "SELECT SUM(transaction_amt) FROM fec_individual_contributions WHERE transaction_amt > 0"
                )
                total_amt = cur.fetchone()[0]
                cur.close()

                logger.info(f"Total FEC records: {total:,}")
                logger.info(f"Total contributions: ${total_amt:,.2f}")
                return

            logger.info(f"Cycles to ingest: {cycles_to_ingest}")

            # Ingest each cycle
            total_inserted = 0
            for cycle in cycles_to_ingest:
                inserted = self.ingest_fec_cycle(cycle)
                total_inserted += inserted

            self.stats["fec_records"] = total_inserted

            # Final summary
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM fec_individual_contributions")
            total = cur.fetchone()[0]
            cur.execute(
                "SELECT COUNT(*) FROM fec_individual_contributions WHERE transaction_amt > 0"
            )
            positive = cur.fetchone()[0]
            cur.execute(
                "SELECT SUM(transaction_amt) FROM fec_individual_contributions WHERE transaction_amt > 0"
            )
            total_amt = cur.fetchone()[0]
            cur.close()

            elapsed = datetime.now() - self.stats["start_time"]

            print("\n" + "=" * 80)
            print("FEC INGESTION COMPLETE")
            print("=" * 80)
            print(f"Duration: {elapsed}")
            print(f"Records inserted in this run: {total_inserted:,}")
            print(f"Total FEC records: {total:,}")
            print(f"Positive amounts: {positive:,}")
            print(f"Total contributions: ${total_amt:,.2f}")
            print("=" * 80)

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close()
                logger.info("Database connection closed")


if __name__ == "__main__":
    pipeline = FECIngestionPipeline()
    pipeline.run()
