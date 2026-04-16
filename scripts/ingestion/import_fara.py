#!/usr/bin/env python3
"""
Import FARA (Foreign Agents Registration Act) data to PostgreSQL
Tables: fara_registrations, fara_foreign_principals, fara_exhibits
"""

import xml.etree.ElementTree as ET
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import psycopg2

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fara")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_fara_{datetime.now():%Y%m%d_%H%M%S}.log"
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
    
    # FARA Registrations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fara_registrations (
            id SERIAL PRIMARY KEY,
            registration_number TEXT UNIQUE,
            registrant_name TEXT,
            registrant_address TEXT,
            registrant_city TEXT,
            registrant_state TEXT,
            registrant_zip TEXT,
            registrant_country TEXT,
            registration_date DATE,
            foreign_principal TEXT,
            foreign_principal_address TEXT,
            foreign_principal_city TEXT,
            foreign_principal_country TEXT,
            registration_purpose TEXT,
            signed_date DATE,
            document_url TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # FARA Foreign Principals table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fara_foreign_principals (
            id SERIAL PRIMARY KEY,
            registration_number TEXT,
            principal_name TEXT,
            principal_address TEXT,
            principal_city TEXT,
            principal_country TEXT,
            principal_type TEXT,
            foreign_government BOOLEAN DEFAULT FALSE,
            foreign_political_party BOOLEAN DEFAULT FALSE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fr_regnum ON fara_registrations (registration_number);
        CREATE INDEX IF NOT EXISTS idx_fr_name ON fara_registrations (registrant_name);
        CREATE INDEX IF NOT EXISTS idx_fp_regnum ON fara_foreign_principals (registration_number);
        CREATE INDEX IF NOT EXISTS idx_fp_country ON fara_foreign_principals (principal_country);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables and indexes created/verified")


def parse_registration_xml(filepath: Path) -> List[Dict]:
    """Parse FARA registration XML"""
    records = []
    
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Handle different XML structures
        for reg in root.findall('.//Registration'):
            record = {
                'registration_number': _get_text(reg, 'RegistrationNumber'),
                'registrant_name': _get_text(reg, 'Registrant/Name'),
                'registrant_address': _get_text(reg, 'Registrant/Address'),
                'registrant_city': _get_text(reg, 'Registrant/City'),
                'registrant_state': _get_text(reg, 'Registrant/State'),
                'registrant_zip': _get_text(reg, 'Registrant/Zip'),
                'registrant_country': _get_text(reg, 'Registrant/Country'),
                'registration_date': _get_text(reg, 'RegistrationDate'),
                'foreign_principal': _get_text(reg, 'ForeignPrincipal/Name'),
                'foreign_principal_address': _get_text(reg, 'ForeignPrincipal/Address'),
                'foreign_principal_city': _get_text(reg, 'ForeignPrincipal/City'),
                'foreign_principal_country': _get_text(reg, 'ForeignPrincipal/Country'),
                'registration_purpose': _get_text(reg, 'RegistrationPurpose'),
                'signed_date': _get_text(reg, 'SignedDate'),
                'source_file': str(filepath.name)
            }
            records.append(record)
            
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def parse_foreign_principals_xml(filepath: Path) -> List[Dict]:
    """Parse FARA foreign principals XML"""
    records = []
    
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        for fp in root.findall('.//ForeignPrincipal'):
            record = {
                'registration_number': _get_text(fp, 'RegistrationNumber'),
                'principal_name': _get_text(fp, 'Name'),
                'principal_address': _get_text(fp, 'Address'),
                'principal_city': _get_text(fp, 'City'),
                'principal_country': _get_text(fp, 'Country'),
                'principal_type': _get_text(fp, 'Type'),
                'foreign_government': _get_text(fp, 'ForeignGovernment') == 'true',
                'foreign_political_party': _get_text(fp, 'ForeignPoliticalParty') == 'true',
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
                INSERT INTO fara_registrations (
                    registration_number, registrant_name, registrant_address, registrant_city,
                    registrant_state, registrant_zip, registrant_country, registration_date,
                    foreign_principal, foreign_principal_address, foreign_principal_city,
                    foreign_principal_country, registration_purpose, signed_date, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (registration_number) DO UPDATE SET
                    registrant_name = EXCLUDED.registrant_name,
                    imported_at = NOW()
            """, (
                r['registration_number'], r['registrant_name'], r['registrant_address'],
                r['registrant_city'], r['registrant_state'], r['registrant_zip'],
                r['registrant_country'], r['registration_date'], r['foreign_principal'],
                r['foreign_principal_address'], r['foreign_principal_city'],
                r['foreign_principal_country'], r['registration_purpose'], r['signed_date'],
                r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_foreign_principals(records: List[Dict]) -> int:
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    for r in records:
        try:
            cur.execute("""
                INSERT INTO fara_foreign_principals (
                    registration_number, principal_name, principal_address, principal_city,
                    principal_country, principal_type, foreign_government,
                    foreign_political_party, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                r['registration_number'], r['principal_name'], r['principal_address'],
                r['principal_city'], r['principal_country'], r['principal_type'],
                r['foreign_government'], r['foreign_political_party'], r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def update_inventory(reg_count: int, fp_count: int):
    conn = get_db_connection()
    cur = conn.cursor()
    total = reg_count + fp_count
    cur.execute("""
        UPDATE data_inventory 
        SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'FARA (Foreign Agents Registration)'
    """, (total,))
    conn.commit()
    cur.close()
    conn.close()


def main():
    logger.info("=" * 80)
    logger.info("FARA IMPORT")
    logger.info("=" * 80)
    
    create_tables()
    
    xml_files = list(BASE_DIR.glob("*.xml"))
    if not xml_files:
        logger.warning("No XML files found")
        return
    
    logger.info(f"Found {len(xml_files)} XML files")
    
    total_registrations = 0
    total_principals = 0
    
    for xml_file in xml_files:
        logger.info(f"Processing {xml_file.name}...")
        
        if 'registration' in xml_file.name.lower():
            records = parse_registration_xml(xml_file)
            if records:
                imported = import_registrations(records)
                total_registrations += imported
                logger.info(f"  Imported {imported} registrations")
        
        elif 'principal' in xml_file.name.lower():
            records = parse_foreign_principals_xml(xml_file)
            if records:
                imported = import_foreign_principals(records)
                total_principals += imported
                logger.info(f"  Imported {imported} principals")
    
    update_inventory(total_registrations, total_principals)
    
    logger.info("=" * 80)
    logger.info(f"IMPORT COMPLETE: {total_registrations} registrations, {total_principals} principals")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
