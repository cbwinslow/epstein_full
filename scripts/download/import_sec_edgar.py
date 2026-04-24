#!/usr/bin/env python3
"""
Import SEC EDGAR Form 4 Insider Trading to PostgreSQL
Source: SEC EDGAR daily index filings
Table: sec_insider_transactions
"""

import json
import logging
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import psycopg2

# Configuration
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/sec_edgar")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")
BATCH_SIZE = 5000

# Logging
log_file = LOG_DIR / f"import_sec_edgar_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(
        host="localhost", database="epstein", user="cbwinslow", password="123qweasd"
    )


def create_table():
    """Create sec_insider_transactions table"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sec_insider_transactions (
            id SERIAL PRIMARY KEY,
            accession_number TEXT,
            filing_date DATE,
            issuer_name TEXT,
            issuer_cik TEXT,
            ticker_symbol TEXT,
            owner_name TEXT,
            owner_cik TEXT,
            owner_title TEXT,
            transaction_date DATE,
            transaction_code TEXT,
            security_title TEXT,
            shares DECIMAL(18, 4),
            price_per_share DECIMAL(18, 4),
            transaction_value DECIMAL(18, 2),
            ownership_type TEXT,  -- D=direct, I=indirect
            nature_of_ownership TEXT,
            is_derivative BOOLEAN DEFAULT FALSE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)

    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sec_issuer ON sec_insider_transactions (issuer_cik);
        CREATE INDEX IF NOT EXISTS idx_sec_owner ON sec_insider_transactions (owner_cik);
        CREATE INDEX IF NOT EXISTS idx_sec_ticker ON sec_insider_transactions (ticker_symbol);
        CREATE INDEX IF NOT EXISTS idx_sec_date ON sec_insider_transactions (transaction_date);
        CREATE INDEX IF NOT EXISTS idx_sec_owner_name ON sec_insider_transactions (owner_name);
        DROP INDEX IF EXISTS uq_sec_accession;
        CREATE UNIQUE INDEX IF NOT EXISTS uq_sec_accession
            ON sec_insider_transactions (accession_number);
    """)

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Table and indexes created/verified")


def parse_atom_feed(filepath: Path) -> List[Dict]:
    """Parse SEC EDGAR Atom feed XML"""
    records = []

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Atom namespace
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        for entry in root.findall(".//atom:entry", ns):
            try:
                # Get filing info from entry
                title = entry.find("atom:title", ns)
                title_text = title.text if title is not None else ""
                entry_id = entry.find("atom:id", ns)
                updated = entry.find("atom:updated", ns)
                summary = entry.find("atom:summary", ns)
                link = entry.find("atom:link[@rel='alternate']", ns)

                id_text = entry_id.text if entry_id is not None else ""
                updated_text = updated.text if updated is not None else ""
                summary_text = summary.text if summary is not None else ""
                link_href = link.get("href", "") if link is not None else ""

                accession = ""
                m = re.search(r"accession-number=([0-9-]+)", id_text)
                if m:
                    accession = m.group(1)
                elif link_href:
                    m = re.search(r"/([0-9]{10}-[0-9]{2}-[0-9]{6})-", link_href)
                    if m:
                        accession = m.group(1)
                if not accession:
                    continue

                filing_date = None
                m = re.search(r"Filed:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", summary_text)
                if m:
                    filing_date = m.group(1)
                elif updated_text:
                    filing_date = updated_text[:10]

                issuer_name = title_text.split("(")[0].strip() if title_text else ""
                issuer_cik = ""
                m = re.search(r"\(([0-9]{5,10})\)", title_text)
                if m:
                    issuer_cik = m.group(1)

                record = {
                    "accession_number": accession or None,
                    "filing_date": filing_date,
                    "issuer_name": issuer_name,
                    "issuer_cik": issuer_cik or None,
                    "ticker_symbol": "",
                    "owner_name": "",
                    "owner_cik": "",
                    "owner_title": "",
                    "transaction_date": "",
                    "transaction_code": "",
                    "security_title": "",
                    "shares": None,
                    "price_per_share": None,
                    "transaction_value": None,
                    "ownership_type": "",
                    "nature_of_ownership": "",
                    "is_derivative": False,
                    "raw_data": json.dumps(
                        {
                            "title": title_text,
                            "id": id_text,
                            "updated": updated_text,
                            "summary": summary_text,
                            "link": link_href,
                        }
                    ),
                    "source_file": str(filepath.name),
                }
                records.append(record)
            except Exception as e:
                logger.debug(f"Entry parse error: {e}")

    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")

    return records


def import_records(records: List[Dict]) -> int:
    """Import records to PostgreSQL"""
    if not records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()

    inserted = 0

    def _date_or_none(value):
        if not value:
            return None
        value = str(value).strip()
        return value or None

    for r in records:
        try:
            cur.execute(
                """
                INSERT INTO sec_insider_transactions (
                    accession_number, filing_date, issuer_name, issuer_cik, ticker_symbol,
                    owner_name, owner_cik, owner_title, transaction_date, transaction_code,
                    security_title, shares, price_per_share, transaction_value,
                    ownership_type, nature_of_ownership, is_derivative, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (accession_number) DO UPDATE SET
                    filing_date = EXCLUDED.filing_date,
                    issuer_name = EXCLUDED.issuer_name,
                    issuer_cik = EXCLUDED.issuer_cik,
                    raw_data = EXCLUDED.raw_data,
                    source_file = EXCLUDED.source_file,
                    imported_at = NOW()
            """,
                (
                    r["accession_number"],
                    _date_or_none(r["filing_date"]),
                    r["issuer_name"],
                    r["issuer_cik"],
                    r["ticker_symbol"],
                    r["owner_name"],
                    r["owner_cik"],
                    r["owner_title"],
                    _date_or_none(r["transaction_date"]),
                    r["transaction_code"],
                    r["security_title"],
                    r["shares"],
                    r["price_per_share"],
                    r["transaction_value"],
                    r["ownership_type"],
                    r["nature_of_ownership"],
                    r["is_derivative"],
                    r["raw_data"],
                    r["source_file"],
                ),
            )
            inserted += cur.rowcount
        except Exception as e:
            logger.debug(f"Insert failed: {e}")

    conn.commit()
    cur.close()
    conn.close()

    return inserted


def update_inventory(count: int):
    """Update data_inventory table"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE data_inventory
        SET status = 'imported',
            actual_records = %s,
            last_updated = NOW()
        WHERE source_name = 'SEC EDGAR Form 4 Insider Trading'
    """,
        (count,),
    )

    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Inventory updated: {count} records")


def main():
    """Main import process"""
    logger.info("=" * 80)
    logger.info("SEC EDGAR FORM 4 IMPORT")
    logger.info("=" * 80)

    create_table()

    # Find all XML files
    xml_files = list(BASE_DIR.rglob("*.xml"))
    if not xml_files:
        logger.warning("No XML files found in " + str(BASE_DIR))
        return

    logger.info(f"Found {len(xml_files)} XML files")

    total_imported = 0
    total_files = 0

    for xml_file in xml_files:
        logger.info(f"Processing {xml_file.name}...")

        records = parse_atom_feed(xml_file)

        if records:
            imported = import_records(records)
            total_imported += imported
            logger.info(f"  Imported {imported}/{len(records)} records")
            total_files += 1
        else:
            logger.warning(f"  No records parsed from {xml_file.name}")

    update_inventory(total_imported)

    logger.info("=" * 80)
    logger.info("IMPORT COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Files processed: {total_files}")
    logger.info(f"Total records imported: {total_imported}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
