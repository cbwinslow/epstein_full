#!/usr/bin/env python3
"""
Import Congress.gov data to PostgreSQL
Source: api.congress.gov
Tables: congress_members, congress_bills
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import psycopg2

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_congress_{datetime.now():%Y%m%d_%H%M%S}.log"
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
    
    # Congress members table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS congress_members (
            id SERIAL PRIMARY KEY,
            bioguide_id TEXT UNIQUE,
            member_name TEXT,
            first_name TEXT,
            last_name TEXT,
            state TEXT,
            party TEXT,
            chamber TEXT,
            congress_number INT,
            district INT,
            title TEXT,
            depiction_image_url TEXT,
            website TEXT,
            office_address TEXT,
            phone TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Congress bills table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS congress_bills (
            id SERIAL PRIMARY KEY,
            bill_number TEXT,
            bill_type TEXT,
            congress INT,
            title TEXT,
            introduced_date DATE,
            latest_action TEXT,
            latest_action_date DATE,
            sponsor_bioguide_id TEXT,
            sponsor_name TEXT,
            sponsor_party TEXT,
            sponsor_state TEXT,
            committees TEXT,
            policy_area TEXT,
            subjects TEXT,
            summary TEXT,
            url TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_cm_name ON congress_members (last_name);
        CREATE INDEX IF NOT EXISTS idx_cm_state ON congress_members (state);
        CREATE INDEX IF NOT EXISTS idx_cm_party ON congress_members (party);
        CREATE INDEX IF NOT EXISTS idx_cm_congress ON congress_members (congress_number);
        
        CREATE INDEX IF NOT EXISTS idx_cb_type ON congress_bills (bill_type);
        CREATE INDEX IF NOT EXISTS idx_cb_congress ON congress_bills (congress);
        CREATE INDEX IF NOT EXISTS idx_cb_date ON congress_bills (introduced_date);
        CREATE INDEX IF NOT EXISTS idx_cb_sponsor ON congress_bills (sponsor_bioguide_id);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables created/verified")


def parse_members_file(filepath: Path) -> List[Dict]:
    records = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for member in data.get('members', []):
            record = {
                'bioguide_id': member.get('bioguideId', ''),
                'member_name': member.get('name', ''),
                'first_name': member.get('firstName', ''),
                'last_name': member.get('lastName', ''),
                'state': member.get('state', ''),
                'party': member.get('partyName', ''),
                'chamber': 'House' if member.get('district') else 'Senate',
                'congress_number': int(filepath.stem.split('_')[1]) if '_' in filepath.stem else 118,
                'district': member.get('district', 0),
                'title': member.get('terms', [{}])[-1].get('memberType', ''),
                'depiction_image_url': member.get('depiction', {}).get('imageUrl', ''),
                'website': member.get('officialWebsiteUrl', ''),
                'office_address': member.get('address', ''),
                'phone': member.get('phoneNumber', ''),
                'raw_data': json.dumps(member),
                'source_file': str(filepath.name)
            }
            records.append(record)
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def parse_bills_file(filepath: Path) -> List[Dict]:
    records = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for bill in data.get('bills', []):
            sponsor = bill.get('sponsors', [{}])[0] if bill.get('sponsors') else {}
            
            record = {
                'bill_number': bill.get('number', ''),
                'bill_type': bill.get('type', ''),
                'congress': bill.get('congress', 118),
                'title': bill.get('title', ''),
                'introduced_date': bill.get('introducedDate') or None,
                'latest_action': bill.get('latestAction', {}).get('text', ''),
                'latest_action_date': bill.get('latestAction', {}).get('actionDate') or None,
                'sponsor_bioguide_id': sponsor.get('bioguideId', ''),
                'sponsor_name': sponsor.get('fullName', ''),
                'sponsor_party': sponsor.get('party', ''),
                'sponsor_state': sponsor.get('state', ''),
                'committees': ', '.join([c.get('name', '') for c in bill.get('committees', [])]),
                'policy_area': bill.get('policyArea', {}).get('name', ''),
                'subjects': ', '.join([s.get('name', '') for s in bill.get('subjects', [])]),
                'summary': bill.get('summary', {}).get('text', ''),
                'url': bill.get('url', ''),
                'raw_data': json.dumps(bill),
                'source_file': str(filepath.name)
            }
            records.append(record)
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def import_members(records: List[Dict]) -> int:
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    for r in records:
        try:
            cur.execute("""
                INSERT INTO congress_members (
                    bioguide_id, member_name, first_name, last_name, state, party,
                    chamber, congress_number, district, title, depiction_image_url,
                    website, office_address, phone, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (bioguide_id) DO UPDATE SET
                    member_name = EXCLUDED.member_name,
                    raw_data = EXCLUDED.raw_data,
                    imported_at = NOW()
            """, (
                r['bioguide_id'], r['member_name'], r['first_name'], r['last_name'],
                r['state'], r['party'], r['chamber'], r['congress_number'], r['district'],
                r['title'], r['depiction_image_url'], r['website'], r['office_address'],
                r['phone'], r['raw_data'], r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_bills(records: List[Dict]) -> int:
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    for r in records:
        try:
            cur.execute("""
                INSERT INTO congress_bills (
                    bill_number, bill_type, congress, title, introduced_date,
                    latest_action, latest_action_date, sponsor_bioguide_id, sponsor_name,
                    sponsor_party, sponsor_state, committees, policy_area, subjects,
                    summary, url, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                r['bill_number'], r['bill_type'], r['congress'], r['title'],
                r['introduced_date'], r['latest_action'], r['latest_action_date'],
                r['sponsor_bioguide_id'], r['sponsor_name'], r['sponsor_party'],
                r['sponsor_state'], r['committees'], r['policy_area'], r['subjects'],
                r['summary'], r['url'], r['raw_data'], r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def update_inventory(member_count: int, bill_count: int):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE data_inventory SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'Congress.gov Members & Votes'
    """, (member_count,))
    
    cur.execute("""
        UPDATE data_inventory SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'Congress.gov Bills & Legislation'
    """, (bill_count,))
    
    conn.commit()
    cur.close()
    conn.close()


def main():
    logger.info("=" * 80)
    logger.info("CONGRESS.GOV IMPORT")
    logger.info("=" * 80)
    
    create_tables()
    
    json_files = list(BASE_DIR.glob("*.json")) + list((BASE_DIR / "bills").glob("*.json"))
    if not json_files:
        logger.warning("No JSON files found")
        return
    
    logger.info(f"Found {len(json_files)} JSON files")
    
    total_members = 0
    total_bills = 0
    
    for json_file in json_files:
        logger.info(f"Processing {json_file.name}...")
        
        if 'members' in json_file.name:
            records = parse_members_file(json_file)
            if records:
                imported = import_members(records)
                total_members += imported
                logger.info(f"  Imported {imported} members")
        
        elif 'bills' in json_file.name or 'votes' in json_file.name:
            records = parse_bills_file(json_file)
            if records:
                imported = import_bills(records)
                total_bills += imported
                logger.info(f"  Imported {imported} bills")
    
    update_inventory(total_members, total_bills)
    
    logger.info("=" * 80)
    logger.info(f"IMPORT COMPLETE: {total_members} members, {total_bills} bills")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
