#!/usr/bin/env python3
"""
Import USA Spending Federal Awards to PostgreSQL
Source: api.usaspending.gov
Table: usa_spending_awards
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import psycopg2

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/usa_spending")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_usa_spending_{datetime.now():%Y%m%d_%H%M%S}.log"
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


def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usa_spending_awards (
            id SERIAL PRIMARY KEY,
            award_id TEXT,
            award_type TEXT,
            recipient_name TEXT,
            recipient_uei TEXT,
            recipient_parent_name TEXT,
            awarding_agency TEXT,
            awarding_sub_agency TEXT,
            program_title TEXT,
            award_amount DECIMAL(18, 2),
            award_date DATE,
            period_start DATE,
            period_end DATE,
            contract_award_type TEXT,
            grant_award_type TEXT,
            cfda_number TEXT,
            cfda_title TEXT,
            naics_code TEXT,
            naics_description TEXT,
            psc_code TEXT,
            psc_description TEXT,
            place_city TEXT,
            place_state TEXT,
            place_zip TEXT,
            place_congressional_district TEXT,
            generated_award_id TEXT UNIQUE,
            is_active BOOLEAN DEFAULT TRUE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_usa_recipient ON usa_spending_awards (recipient_name);
        CREATE INDEX IF NOT EXISTS idx_usa_agency ON usa_spending_awards (awarding_agency);
        CREATE INDEX IF NOT EXISTS idx_usa_date ON usa_spending_awards (award_date);
        CREATE INDEX IF NOT EXISTS idx_usa_amount ON usa_spending_awards (award_amount);
        CREATE INDEX IF NOT EXISTS idx_usa_type ON usa_spending_awards (award_type);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Table created/verified")


def parse_json_file(filepath: Path) -> List[Dict]:
    records = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for result in data.get('results', []):
            # Handle empty date strings by converting to None
            award_date = result.get('Award Date', result.get('period_of_performance_start_date', ''))
            period_start = result.get('Period of Performance Start Date', '')
            period_end = result.get('Period of Performance End Date', '')
            
            record = {
                'award_id': result.get('Award ID', result.get('generated_internal_id', '')),
                'award_type': result.get('award_type', 'contract'),
                'recipient_name': result.get('Recipient Name', result.get('recipient_name', '')),
                'recipient_uei': result.get('recipient_uei', ''),
                'recipient_parent_name': result.get('recipient_parent_name', ''),
                'awarding_agency': result.get('Awarding Agency', result.get('awarding_agency_name', '')),
                'awarding_sub_agency': result.get('Awarding Sub Agency', result.get('awarding_sub_agency_name', '')),
                'program_title': result.get('program_title', ''),
                'award_amount': result.get('Award Amount', result.get('award_amount', 0)),
                'award_date': award_date if award_date else None,
                'period_start': period_start if period_start else None,
                'period_end': period_end if period_end else None,
                'contract_award_type': result.get('contract_award_type', ''),
                'grant_award_type': result.get('grant_award_type', ''),
                'cfda_number': result.get('cfda_number', ''),
                'cfda_title': result.get('cfda_title', ''),
                'naics_code': result.get('naics_code', ''),
                'naics_description': result.get('naics_description', ''),
                'psc_code': result.get('product_or_service_code', ''),
                'psc_description': result.get('product_or_service_code_description', ''),
                'place_city': result.get('place_of_performance_city', ''),
                'place_state': result.get('place_of_performance_state', ''),
                'place_zip': result.get('place_of_performance_zip', ''),
                'place_congressional_district': result.get('place_of_performance_congressional_district', ''),
                'generated_award_id': result.get('generated_internal_id', result.get('Award ID', '')),
                'raw_data': json.dumps(result),
                'source_file': str(filepath.name)
            }
            records.append(record)
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def import_records(records: List[Dict]) -> int:
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    for r in records:
        try:
            cur.execute("""
                INSERT INTO usa_spending_awards (
                    award_id, award_type, recipient_name, recipient_uei, recipient_parent_name,
                    awarding_agency, awarding_sub_agency, program_title, award_amount, award_date,
                    period_start, period_end, contract_award_type, grant_award_type,
                    cfda_number, cfda_title, naics_code, naics_description, psc_code, psc_description,
                    place_city, place_state, place_zip, place_congressional_district,
                    generated_award_id, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (generated_award_id) DO NOTHING
            """, (
                r['award_id'], r['award_type'], r['recipient_name'], r['recipient_uei'],
                r['recipient_parent_name'], r['awarding_agency'], r['awarding_sub_agency'],
                r['program_title'], r['award_amount'], r['award_date'], r['period_start'],
                r['period_end'], r['contract_award_type'], r['grant_award_type'],
                r['cfda_number'], r['cfda_title'], r['naics_code'], r['naics_description'],
                r['psc_code'], r['psc_description'], r['place_city'], r['place_state'],
                r['place_zip'], r['place_congressional_district'], r['generated_award_id'],
                r['raw_data'], r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.error(f"Insert failed for {r.get('award_id')}: {e}")
            conn.rollback()
            cur.close()
            conn.close()
            return inserted
    
    conn.commit()
    cur.close()
    conn.close()
    
    return inserted


def update_inventory(count: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE data_inventory 
        SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'USA Spending Federal Awards'
    """, (count,))
    conn.commit()
    cur.close()
    conn.close()


def main():
    logger.info("=" * 80)
    logger.info("USA SPENDING IMPORT")
    logger.info("=" * 80)
    
    create_table()
    
    json_files = list(BASE_DIR.glob("*.json"))
    if not json_files:
        logger.warning("No JSON files found")
        return
    
    logger.info(f"Found {len(json_files)} JSON files")
    
    total_imported = 0
    for json_file in json_files:
        logger.info(f"Processing {json_file.name}...")
        records = parse_json_file(json_file)
        if records:
            imported = import_records(records)
            total_imported += imported
            logger.info(f"  Imported {imported}/{len(records)} records")
    
    update_inventory(total_imported)
    
    logger.info("=" * 80)
    logger.info(f"IMPORT COMPLETE: {total_imported} records")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
