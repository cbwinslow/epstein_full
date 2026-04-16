#!/usr/bin/env python3
"""
Import Lobbying Disclosure Act (LDA) data to PostgreSQL
Tables: lobbying_registrations, lobbying_quarterly_reports, lobbying_issues
"""

import xml.etree.ElementTree as ET
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import psycopg2

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/lobbying")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_lobbying_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg2.connect(
        host='localhost', database='epstein',
        user='cbwinslow', password='123qweasd'
    )


def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Lobbying registrations (LD-1)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lobbying_registrations (
            id SERIAL PRIMARY KEY,
            registration_id TEXT UNIQUE,
            registrant_name TEXT,
            registrant_address TEXT,
            registrant_city TEXT,
            registrant_state TEXT,
            registrant_zip TEXT,
            registrant_country TEXT,
            registrant_ppb_country TEXT,
            client_name TEXT,
            client_address TEXT,
            client_city TEXT,
            client_state TEXT,
            client_zip TEXT,
            client_country TEXT,
            client_ppb_country TEXT,
            foreign_entity_name TEXT,
            foreign_entity_address TEXT,
            foreign_entity_city TEXT,
            foreign_entity_country TEXT,
            foreign_entity_ppb TEXT,
            registration_date DATE,
            signature_date DATE,
            registrant_id TEXT,
            client_id TEXT,
            termination_date DATE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Lobbying quarterly reports (LD-2)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lobbying_quarterly_reports (
            id SERIAL PRIMARY KEY,
            report_id TEXT UNIQUE,
            registrant_name TEXT,
            client_name TEXT,
            lobbying_activity_period_start DATE,
            lobbying_activity_period_end DATE,
            income_amount TEXT,
            expenses_amount TEXT,
            termination_date DATE,
            issues TEXT,
            specific_issues TEXT,
            houses_and_agencies TEXT,
            foreign_entity_interest BOOLEAN DEFAULT FALSE,
            registrant_id TEXT,
            client_id TEXT,
            report_type TEXT,
            year INT,
            quarter TEXT,
            signature_date DATE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Lobbying issues detail
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lobbying_issues (
            id SERIAL PRIMARY KEY,
            report_id TEXT,
            issue_code TEXT,
            specific_issue TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_lr_registrant ON lobbying_registrations (registrant_name);
        CREATE INDEX IF NOT EXISTS idx_lr_client ON lobbying_registrations (client_name);
        CREATE INDEX IF NOT EXISTS idx_lqr_registrant ON lobbying_quarterly_reports (registrant_name);
        CREATE INDEX IF NOT EXISTS idx_lqr_client ON lobbying_quarterly_reports (client_name);
        CREATE INDEX IF NOT EXISTS idx_lqr_period ON lobbying_quarterly_reports (lobbying_activity_period_start);
        CREATE INDEX IF NOT EXISTS idx_li_report ON lobbying_issues (report_id);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables and indexes created/verified")


def parse_ld1_xml(filepath: Path) -> List[Dict]:
    """Parse LD-1 registration XML"""
    records = []
    
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        for filing in root.findall('.//Filing'):
            record = {
                'registration_id': _get_text(filing, 'ID'),
                'registrant_name': _get_text(filing, 'Registrant/Name'),
                'registrant_address': _get_text(filing, 'Registrant/Address'),
                'registrant_city': _get_text(filing, 'Registrant/City'),
                'registrant_state': _get_text(filing, 'Registrant/State'),
                'registrant_zip': _get_text(filing, 'Registrant/Zip'),
                'registrant_country': _get_text(filing, 'Registrant/Country'),
                'registrant_ppb_country': _get_text(filing, 'Registrant/PPBCountry'),
                'client_name': _get_text(filing, 'Client/Name'),
                'client_address': _get_text(filing, 'Client/Address'),
                'client_city': _get_text(filing, 'Client/City'),
                'client_state': _get_text(filing, 'Client/State'),
                'client_zip': _get_text(filing, 'Client/Zip'),
                'client_country': _get_text(filing, 'Client/Country'),
                'client_ppb_country': _get_text(filing, 'Client/PPBCountry'),
                'foreign_entity_name': _get_text(filing, 'ForeignEntity/Name'),
                'foreign_entity_address': _get_text(filing, 'ForeignEntity/Address'),
                'foreign_entity_city': _get_text(filing, 'ForeignEntity/City'),
                'foreign_entity_country': _get_text(filing, 'ForeignEntity/Country'),
                'foreign_entity_ppb': _get_text(filing, 'ForeignEntity/PPBCountry'),
                'registration_date': _get_text(filing, 'RegistrationDate'),
                'signature_date': _get_text(filing, 'SignatureDate'),
                'registrant_id': _get_text(filing, 'Registrant/RegistrantID'),
                'client_id': _get_text(filing, 'Client/ClientID'),
                'termination_date': _get_text(filing, 'TerminationDate'),
                'source_file': str(filepath.name)
            }
            records.append(record)
            
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def parse_ld2_xml(filepath: Path) -> List[Dict]:
    """Parse LD-2 quarterly report XML"""
    records = []
    
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        for filing in root.findall('.//Filing'):
            # Extract year and quarter from filename
            filename = filepath.name
            year = filename.split('_')[1] if '_' in filename else None
            quarter = filename.split('_')[2].split('.')[0] if len(filename.split('_')) > 2 else None
            
            record = {
                'report_id': _get_text(filing, 'ID'),
                'registrant_name': _get_text(filing, 'Registrant/Name'),
                'client_name': _get_text(filing, 'Client/Name'),
                'lobbying_activity_period_start': _get_text(filing, 'PeriodOfActivity/Start'),
                'lobbying_activity_period_end': _get_text(filing, 'PeriodOfActivity/End'),
                'income_amount': _get_text(filing, 'Income'),
                'expenses_amount': _get_text(filing, 'Expenses'),
                'termination_date': _get_text(filing, 'TerminationDate'),
                'issues': _get_text(filing, 'IssueAreas'),
                'specific_issues': _get_text(filing, 'SpecificIssues'),
                'houses_and_agencies': _get_text(filing, 'HousesAndAgencies'),
                'foreign_entity_interest': _get_text(filing, 'ForeignEntityInterest') == 'true',
                'registrant_id': _get_text(filing, 'Registrant/RegistrantID'),
                'client_id': _get_text(filing, 'Client/ClientID'),
                'report_type': _get_text(filing, 'ReportType'),
                'year': int(year) if year and year.isdigit() else None,
                'quarter': quarter,
                'signature_date': _get_text(filing, 'SignatureDate'),
                'source_file': str(filepath.name)
            }
            records.append(record)
            
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def _get_text(element, path: str) -> str:
    """Safely get text from XML element"""
    try:
        parts = path.split('/')
        current = element
        for part in parts:
            current = current.find(part)
            if current is None:
                return ''
        return current.text or ''
    except:
        return ''


def import_registrations(records: List[Dict]) -> int:
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    for r in records:
        try:
            cur.execute("""
                INSERT INTO lobbying_registrations (
                    registration_id, registrant_name, registrant_address, registrant_city,
                    registrant_state, registrant_zip, registrant_country, registrant_ppb_country,
                    client_name, client_address, client_city, client_state, client_zip, client_country,
                    client_ppb_country, foreign_entity_name, foreign_entity_address,
                    foreign_entity_city, foreign_entity_country, foreign_entity_ppb,
                    registration_date, signature_date, registrant_id, client_id,
                    termination_date, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (registration_id) DO UPDATE SET
                    registrant_name = EXCLUDED.registrant_name,
                    imported_at = NOW()
            """, (
                r['registration_id'], r['registrant_name'], r['registrant_address'],
                r['registrant_city'], r['registrant_state'], r['registrant_zip'],
                r['registrant_country'], r['registrant_ppb_country'], r['client_name'],
                r['client_address'], r['client_city'], r['client_state'], r['client_zip'],
                r['client_country'], r['client_ppb_country'], r['foreign_entity_name'],
                r['foreign_entity_address'], r['foreign_entity_city'], r['foreign_entity_country'],
                r['foreign_entity_ppb'], r['registration_date'], r['signature_date'],
                r['registrant_id'], r['client_id'], r['termination_date'], r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_quarterly_reports(records: List[Dict]) -> int:
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    for r in records:
        try:
            cur.execute("""
                INSERT INTO lobbying_quarterly_reports (
                    report_id, registrant_name, client_name, lobbying_activity_period_start,
                    lobbying_activity_period_end, income_amount, expenses_amount,
                    termination_date, issues, specific_issues, houses_and_agencies,
                    foreign_entity_interest, registrant_id, client_id, report_type,
                    year, quarter, signature_date, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (report_id) DO UPDATE SET
                    registrant_name = EXCLUDED.registrant_name,
                    imported_at = NOW()
            """, (
                r['report_id'], r['registrant_name'], r['client_name'],
                r['lobbying_activity_period_start'], r['lobbying_activity_period_end'],
                r['income_amount'], r['expenses_amount'], r['termination_date'],
                r['issues'], r['specific_issues'], r['houses_and_agencies'],
                r['foreign_entity_interest'], r['registrant_id'], r['client_id'],
                r['report_type'], r['year'], r['quarter'], r['signature_date'],
                r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def update_inventory(ld1_count: int, ld2_count: int):
    conn = get_db_connection()
    cur = conn.cursor()
    total = ld1_count + ld2_count
    cur.execute("""
        UPDATE data_inventory 
        SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'Lobbying Disclosure'
    """, (total,))
    conn.commit()
    cur.close()
    conn.close()


def main():
    logger.info("=" * 80)
    logger.info("LOBBYING DISCLOSURE IMPORT")
    logger.info("=" * 80)
    
    create_tables()
    
    xml_files = list(BASE_DIR.glob("*.xml"))
    if not xml_files:
        logger.warning("No XML files found")
        return
    
    logger.info(f"Found {len(xml_files)} XML files")
    
    total_ld1 = 0
    total_ld2 = 0
    
    for xml_file in xml_files:
        logger.info(f"Processing {xml_file.name}...")
        
        if 'LD1' in xml_file.name.upper() or 'registration' in xml_file.name.lower():
            records = parse_ld1_xml(xml_file)
            if records:
                imported = import_registrations(records)
                total_ld1 += imported
                logger.info(f"  Imported {imported} LD-1 registrations")
        
        elif 'LD2' in xml_file.name.upper() or 'quarterly' in xml_file.name.lower():
            records = parse_ld2_xml(xml_file)
            if records:
                imported = import_quarterly_reports(records)
                total_ld2 += imported
                logger.info(f"  Imported {imported} LD-2 quarterly reports")
    
    update_inventory(total_ld1, total_ld2)
    
    logger.info("=" * 80)
    logger.info(f"IMPORT COMPLETE: {total_ld1} LD-1, {total_ld2} LD-2")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
