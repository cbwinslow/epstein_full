#!/usr/bin/env python3
"""
SEC EDGAR Insider Transaction Ingestion - All Years 2000-2026

This script ingests SEC Form 4 insider trading transactions
from the SEC EDGAR daily index filings.

Usage:
    python3 sec_insider_ingestion.py [--all-years] [--start-year YYYY] [--end-year YYYY]
"""

import argparse
import logging
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import psycopg2
from psycopg2.extras import execute_batch

from config import get_db_connection, setup_file_logger, RAW_FILES_DIR

# Configuration
SEC_DIR = RAW_FILES_DIR / "sec_edgar"
LOG_DIR = RAW_FILES_DIR / "logs" / "sec"
LOG_DIR.mkdir(parents=True, exist_ok=True)
SEC_DIR.mkdir(parents=True, exist_ok=True)

BATCH_SIZE = 5000


def setup_logging():
    """Setup logging for SEC ingestion."""
    logger, log_file = setup_file_logger("sec_insider_ingestion")
    return logger, log_file


def create_tables(conn):
    """Create SEC insider transactions table if it doesn't exist."""
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
            shares NUMERIC,
            price_per_share NUMERIC,
            transaction_value NUMERIC,
            ownership_type TEXT,
            nature_of_ownership TEXT,
            is_derivative BOOLEAN DEFAULT FALSE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sec_issuer_cik ON sec_insider_transactions(issuer_cik);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sec_owner_name ON sec_insider_transactions(owner_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sec_transaction_date ON sec_insider_transactions(transaction_date);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sec_filing_date ON sec_insider_transactions(filing_date);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sec_transaction_code ON sec_insider_transactions(transaction_code);")
    conn.commit()
    cur.close()


def get_existing_filings(conn):
    """Get set of already processed source files."""
    cur = conn.cursor()
    cur.execute("SELECT source_file FROM sec_insider_transactions WHERE source_file IS NOT NULL")
    existing = {row[0] for row in cur.fetchall()}
    cur.close()
    return existing


def parse_sec_xml_file(filepath: Path, logger) -> List[Dict]:
    """Parse a single SEC Form 4 XML file and extract transactions."""
    transactions = []
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Define namespaces
        ns = {
            'sec': 'http://www.sec.gov/edgar/thirteenffiler',
            '': 'http://www.sec.gov/edgar/thirteenffiler'
        }

        # Try to get CIK and company name
        cik = None
        company_name = None

        # Look for issuer CIK
        issuer_cik = root.find('.//issuerCik')
        if issuer_cik is not None and issuer_cik.text:
            cik = issuer_cik.text.strip()

        # Look for company name
        issuer_name = root.find('.//issuerName')
        if issuer_name is not None and issuer_name.text:
            company_name = issuer_name.text.strip()

        # Find all nonDerivativeTable entries (non-derivative transactions)
        non_derivative_entries = root.findall('.//nonDerivativeTable//nonDerivativeTransaction')

        for entry in non_derivative_entries:
            try:
                security_title_elem = entry.find('.//securityTitle')
                security_title = security_title_elem.text.strip() if security_title_elem is not None and security_title_elem.text else None

                transaction_date_elem = entry.find('.//transactionDate')
                transaction_date = None
                if transaction_date_elem is not None and transaction_date_elem.text:
                    transaction_date = datetime.strptime(transaction_date_elem.text.strip(), '%Y-%m-%d').date()

                transaction_code_elem = entry.find('.//transactionCode')
                transaction_code = transaction_code_elem.text.strip() if transaction_code_elem is not None and transaction_code_elem.text else None

                transaction_amounts = entry.find('.//transactionAmounts')
                shares_traded = None
                price_per_share = None
                shares_owned_after = None

                if transaction_amounts is not None:
                    shares_elem = transaction_amounts.find('.//transactionShares')
                    if shares_elem is not None and shares_elem.text:
                        shares_traded = shares_elem.text.strip()

                    price_elem = transaction_amounts.find('.//transactionPricePerShare')
                    if price_elem is not None and price_elem.text:
                        price_per_share = price_elem.text.strip()

                    owned_elem = transaction_amounts.find('.//sharesOwnedFollowingTransaction')
                    if owned_elem is not None and owned_elem.text:
                        shares_owned_after = owned_elem.text.strip()

                ownership_elem = entry.find('.//ownershipNature')
                direct_or_indirect = None
                nature_of_ownership = None
                if ownership_elem is not None:
                    direct_elem = ownership_elem.find('.//directOrIndirectOwnership')
                    if direct_elem is not None and direct_elem.text:
                        direct_or_indirect = direct_elem.text.strip()

                    nature_elem = ownership_elem.find('.//natureOfOwnership')
                    if nature_elem is not None and nature_elem.text:
                        nature_of_ownership = nature_elem.text.strip()

                reporting_owner = entry.find('.//reportingOwner')
                insider_name = None
                insider_title = None
                if reporting_owner is not None:
                    rpt_owner_name = reporting_owner.find('.//rptOwnerName')
                    if rpt_owner_name is not None and rpt_owner_name.text:
                        insider_name = rpt_owner_name.text.strip()

                    rpt_owner_title = reporting_owner.find('.//rptOwnerTitle')
                    if rpt_owner_title is not None and rpt_owner_title.text:
                        insider_title = rpt_owner_title.text.strip()

                 # Calculate transaction amount
                transaction_amount = None
                if shares_traded and price_per_share:
                    try:
                        transaction_amount = float(shares_traded) * float(price_per_share)
                    except ValueError:
                        pass

                transactions.append({
                    'accession_number': None,
                    'filing_date': None,
                    'issuer_name': company_name,
                    'issuer_cik': cik,
                    'ticker_symbol': None,
                    'owner_name': insider_name,
                    'owner_cik': None,
                    'owner_title': insider_title,
                    'transaction_date': transaction_date,
                    'transaction_code': transaction_code,
                    'security_title': security_title,
                    'shares': shares_traded,
                    'price_per_share': price_per_share,
                    'transaction_value': transaction_amount,
                    'ownership_type': direct_or_indirect,
                    'nature_of_ownership': nature_of_ownership,
                    'is_derivative': False,
                    'raw_data': None,
                    'source_file': xml_file.name
                })
                total_new += 1
            except Exception as e:
                logger.warning(f"    Warning parsing transaction in {filepath.name}: {e}")
                continue

            # Also check for derivative transactions
            derivative_entries = root.findall('.//derivativeTable//derivativeTransaction')
            for entry in derivative_entries:
                try:
                    security_title_elem = entry.find('.//securityTitle')
                    security_title = security_title_elem.text.strip() if security_title_elem is not None and security_title_elem.text else None

                    transaction_date_elem = entry.find('.//transactionDate')
                    transaction_date = None
                    if transaction_date_elem is not None and transaction_date_elem.text:
                        transaction_date = datetime.strptime(transaction_date_elem.text.strip(), '%Y-%m-%d').date()

                    transaction_code_elem = entry.find('.//transactionCode')
                    transaction_code = transaction_code_elem.text.strip() if transaction_code_elem is not None and transaction_code_elem.text else None

                    transaction_amounts = entry.find('.//transactionAmounts')
                    shares_traded = None
                    price_per_share = None
                    shares_owned_after = None

                    if transaction_amounts is not None:
                        shares_elem = transaction_amounts.find('.//transactionShares')
                        if shares_elem is not None and shares_elem.text:
                            shares_traded = shares_elem.text.strip()

                        price_elem = transaction_amounts.find('.//transactionPricePerShare')
                        if price_elem is not None and price_elem.text:
                            price_per_share = price_elem.text.strip()

                        owned_elem = transaction_amounts.find('.//sharesOwnedFollowingTransaction')
                        if owned_elem is not None and owned_elem.text:
                            shares_owned_after = owned_elem.text.strip()

                    reporting_owner = entry.find('.//reportingOwner')
                    insider_name = None
                    insider_title = None
                    if reporting_owner is not None:
                        rpt_owner_name = reporting_owner.find('.//rptOwnerName')
                        if rpt_owner_name is not None and rpt_owner_name.text:
                            insider_name = rpt_owner_name.text.strip()

                        rpt_owner_title = reporting_owner.find('.//rptOwnerTitle')
                        if rpt_owner_title is not None and rpt_owner_title.text:
                            insider_title = rpt_owner_title.text.strip()

                    # Calculate transaction amount
                    transaction_amount = None
                    if shares_traded and price_per_share:
                        try:
                            transaction_amount = float(shares_traded) * float(price_per_share)
                        except ValueError:
                            pass

                   transactions.append({
                        'accession_number': None,
                        'filing_date': None,
                        'issuer_name': company_name,
                        'issuer_cik': cik,
                        'ticker_symbol': None,
                        'owner_name': insider_name,
                        'owner_cik': None,
                        'owner_title': insider_title,
                        'transaction_date': transaction_date,
                        'transaction_code': transaction_code,
                        'security_title': security_title,
                        'shares': shares_traded,
                        'price_per_share': price_per_share,
                        'transaction_value': transaction_amount,
                        'ownership_type': 'indirect',
                        'nature_of_ownership': None,
                        'is_derivative': True,
                        'raw_data': None,
                        'source_file': xml_file.name
                    })
                    total_new += 1
                except Exception as e:
                    logger.warning(f"    Warning parsing derivative transaction in {filepath.name}: {e}")
                    continue

            existing_filings.add(xml_file.name)
            files_processed += 1

            # Add transactions to batch
            batch_transactions.extend(transactions)

            if len(batch_transactions) >= BATCH_SIZE:
                cur = conn.cursor()
                execute_batch(cur, """
                    INSERT INTO sec_insider_transactions (
                        accession_number, filing_date, issuer_name, issuer_cik,
                        ticker_symbol, owner_name, owner_cik, owner_title,
                        transaction_date, transaction_code, security_title,
                        shares, price_per_share, transaction_value,
                        ownership_type, nature_of_ownership, is_derivative,
                        raw_data, source_file
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, batch_transactions, page_size=100)
                conn.commit()
                cur.close()
                logger.info(f"    Inserted batch of {len(batch_transactions)} transactions ({files_processed}/{len(xml_files)} files)")
                batch_transactions = []

        # Insert remaining transactions
        if batch_transactions:
            cur = conn.cursor()
            execute_batch(cur, """
                INSERT INTO sec_insider_transactions (
                    accession_number, filing_date, issuer_name, issuer_cik,
                    ticker_symbol, owner_name, owner_cik, owner_title,
                    transaction_date, transaction_code, security_title,
                    shares, price_per_share, transaction_value,
                    ownership_type, nature_of_ownership, is_derivative,
                    raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, batch_transactions, page_size=100)
            conn.commit()
            cur.close()
            logger.info(f"    Inserted final batch of {len(batch_transactions)} transactions")

        return total_new, total_existing, total_files


def main():
    parser = argparse.ArgumentParser(
        description="Ingest SEC EDGAR insider transactions into PostgreSQL"
    )
    parser.add_argument(
        "--all-years",
        action="store_true",
        help="Ingest all available years (2000-2026)"
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=2000,
        help="Start year (default: 2000)"
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=2026,
        help="End year (default: 2026)"
    )
    args = parser.parse_args()

    if args.all_years:
        start_year = 2000
        end_year = 2026
    else:
        start_year = args.start_year
        end_year = args.end_year

    logger, log_file = setup_logging()

    logger.info("=" * 80)
    logger.info("SEC EDGAR INSIDER TRANSACTION INGESTION")
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

        total_new, total_existing, total_files = ingest_sec_files(
            conn, start_year, end_year, logger
        )

        elapsed = time.time() - start_time

        logger.info("\n" + "=" * 80)
        logger.info("INGESTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"XML files processed: {total_files}")
        logger.info(f"New transactions inserted: {total_new:,}")
        logger.info(f"Existing files skipped: {total_existing}")
        logger.info(f"Total elapsed time: {elapsed:.2f}s ({elapsed/60:.2f} minutes)")
        logger.info("=" * 80)

        # Verify final count
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM sec_insider_transactions")
        total_count = cur.fetchone()[0]
        cur.close()
        logger.info(f"Total records in sec_insider_transactions: {total_count:,}")

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

    logger.info(f"\n✅ SEC Ingestion Complete at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
