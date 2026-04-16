#!/usr/bin/env python3
"""
Download Congress.gov Bills Data
Uses Congress.gov API (key in .bash_secrets)
Downloads bills for 118th Congress (2023-2024)
"""

import os
import json
import time
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import requests

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"congress_bills_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load API key from secrets
API_KEY = None
def load_api_key():
    global API_KEY
    secrets_file = Path.home() / 'workspace' / 'epstein' / '.bash_secrets'
    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                if 'CONGRESS_API_KEY=' in line:
                    API_KEY = line.split('=')[1].strip().strip('"\'')
                    break
    if not API_KEY:
        logger.error("CONGRESS_API_KEY not found in .bash_secrets")
        sys.exit(1)

BASE_URL = "https://api.congress.gov/v3"
CONGRESS_NUMBER = 118  # 2023-2024


def fetch_bills(offset: int = 0, limit: int = 250) -> Dict:
    """Fetch bills from Congress.gov API"""
    url = f"{BASE_URL}/bill/{CONGRESS_NUMBER}"
    params = {
        'api_key': API_KEY,
        'format': 'json',
        'offset': offset,
        'limit': limit
    }
    
    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching bills at offset {offset}: {e}")
        return {'bills': [], 'pagination': {'count': 0}}


def fetch_bill_details(bill_type: str, bill_number: str) -> Dict:
    """Fetch detailed bill information including actions, cosponsors"""
    url = f"{BASE_URL}/bill/{CONGRESS_NUMBER}/{bill_type}/{bill_number}"
    params = {'api_key': API_KEY, 'format': 'json'}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.debug(f"Error fetching bill details for {bill_type}{bill_number}: {e}")
    
    return {}


def fetch_members() -> List[Dict]:
    """Fetch current Congress members"""
    members = []
    offset = 0
    limit = 250
    
    while True:
        url = f"{BASE_URL}/member"
        params = {
            'api_key': API_KEY,
            'format': 'json',
            'offset': offset,
            'limit': limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            batch = data.get('members', [])
            if not batch:
                break
            
            members.extend(batch)
            logger.info(f"  Fetched {len(batch)} members (total: {len(members)})")
            
            # Check if there are more
            count = data.get('pagination', {}).get('count', 0)
            if offset + limit >= count:
                break
            
            offset += limit
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            logger.error(f"Error fetching members at offset {offset}: {e}")
            break
    
    return members


def fetch_amendments(bill_type: str, bill_number: str) -> List[Dict]:
    """Fetch amendments for a bill"""
    url = f"{BASE_URL}/bill/{CONGRESS_NUMBER}/{bill_type}/{bill_number}/amendments"
    params = {'api_key': API_KEY, 'format': 'json'}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('amendments', [])
    except Exception as e:
        logger.debug(f"Error fetching amendments: {e}")
    
    return []


def download_all_bills():
    """Download all bills for 118th Congress"""
    logger.info("=" * 80)
    logger.info("CONGRESS.GOV BILLS DOWNLOAD")
    logger.info(f"Congress: {CONGRESS_NUMBER} (2023-2024)")
    logger.info("=" * 80)
    
    bills_dir = BASE_DIR / "bills"
    bills_dir.mkdir(parents=True, exist_ok=True)
    
    all_bills = []
    offset = 0
    limit = 250
    total_count = None
    chunk_num = 0
    
    while True:
        logger.info(f"Fetching bills offset={offset}...")
        data = fetch_bills(offset, limit)
        
        bills = data.get('bills', [])
        if not bills:
            break
        
        all_bills.extend(bills)
        
        if total_count is None:
            total_count = data.get('pagination', {}).get('count', 0)
            logger.info(f"Total bills to download: {total_count}")
        
        logger.info(f"  Downloaded {len(bills)} bills (total: {len(all_bills)})")
        
        # Save in chunks of 1000
        if len(all_bills) >= 1000:
            chunk_file = bills_dir / f"bills_{CONGRESS_NUMBER}_chunk_{chunk_num:04d}.json"
            with open(chunk_file, 'w') as f:
                json.dump({'bills': all_bills, 'congress': CONGRESS_NUMBER}, f, indent=2)
            logger.info(f"  Saved chunk {chunk_num}: {chunk_file.name}")
            all_bills = []
            chunk_num += 1
        
        # Check if done
        if len(bills) < limit:
            break
        
        offset += limit
        time.sleep(0.5)  # Rate limiting (5000 req/day = ~1 req/17 sec, but we can go faster)
    
    # Save remaining bills
    if all_bills:
        chunk_file = bills_dir / f"bills_{CONGRESS_NUMBER}_chunk_{chunk_num:04d}.json"
        with open(chunk_file, 'w') as f:
            json.dump({'bills': all_bills, 'congress': CONGRESS_NUMBER}, f, indent=2)
        logger.info(f"  Saved final chunk {chunk_num}: {chunk_file.name} ({len(all_bills)} bills)")
    
    # Count total
    total_saved = sum(1 for f in bills_dir.glob("*.json") 
                      for data in [json.load(open(f))] 
                      for _ in data.get('bills', []))
    
    logger.info(f"\nDownloaded {total_saved} bills total")
    return total_saved


def download_members():
    """Download all current Congress members"""
    logger.info("\n" + "=" * 80)
    logger.info("CONGRESS.GOV MEMBERS DOWNLOAD")
    logger.info("=" * 80)
    
    members = fetch_members()
    
    if not members:
        logger.warning("No members downloaded")
        return 0
    
    members_file = BASE_DIR / f"members_{CONGRESS_NUMBER}.json"
    with open(members_file, 'w') as f:
        json.dump({'members': members, 'congress': CONGRESS_NUMBER}, f, indent=2)
    
    logger.info(f"Saved {len(members)} members to {members_file.name}")
    return len(members)


def update_inventory(bill_count: int, member_count: int):
    """Update data inventory in database"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost', database='epstein',
            user='cbwinslow', password='123qweasd'
        )
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO data_inventory (source_name, status, actual_records, last_updated)
            VALUES ('Congress.gov Bills', 'downloaded', %s, NOW())
            ON CONFLICT (source_name) DO UPDATE SET
                status = 'downloaded',
                actual_records = %s,
                last_updated = NOW()
        """, (bill_count, bill_count))
        
        cur.execute("""
            INSERT INTO data_inventory (source_name, status, actual_records, last_updated)
            VALUES ('Congress.gov Members', 'downloaded', %s, NOW())
            ON CONFLICT (source_name) DO UPDATE SET
                status = 'downloaded',
                actual_records = %s,
                last_updated = NOW()
        """, (member_count, member_count))
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Inventory updated")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


def main():
    load_api_key()
    
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download members
    member_count = download_members()
    
    # Download bills
    bill_count = download_all_bills()
    
    # Update inventory
    update_inventory(bill_count, member_count)
    
    logger.info("\n" + "=" * 80)
    logger.info("DOWNLOAD COMPLETE")
    logger.info(f"  Members: {member_count}")
    logger.info(f"  Bills: {bill_count}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
