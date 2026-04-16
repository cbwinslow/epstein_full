#!/usr/bin/env python3
"""
Bulk Download GovInfo.gov Data
Downloads large amounts of Federal Register and other collections
Target: 100,000+ documents
"""

import os
import sys
import json
import time
import logging
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"govinfo_bulk_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load secrets if not already in environment
if not os.environ.get('GOVINFO_API_KEY'):
    import subprocess
    secrets_file = Path.home() / 'workspace' / 'epstein' / '.bash_secrets'
    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                if line.startswith('export '):
                    key_val = line[7:].strip().split('=', 1)
                    if len(key_val) == 2 and key_val[0] not in os.environ:
                        os.environ[key_val[0]] = key_val[1].strip('"\'')

API_KEY = os.environ.get('GOVINFO_API_KEY')
if not API_KEY:
    logger.error("GOVINFO_API_KEY not set")
    exit(1)

BASE_URL = "https://api.govinfo.gov"
HEADERS = {'X-Api-Key': API_KEY}


def fetch_collection_packages(collection: str, start_date: str, end_date: str, offset: int = 0) -> Dict:
    """Fetch packages from a collection for a date range"""
    # Use published endpoint instead of collections
    url = f"{BASE_URL}/published/{start_date}/{end_date}"
    params = {'offset': offset, 'pageSize': 100, 'collection': collection}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching {collection} at offset {offset}: {e}")
        return {'packages': [], 'nextPage': None}


def download_collection(collection: str, collection_name: str, years: List[int]):
    """Download all packages for a collection across multiple years"""
    collection_dir = BASE_DIR / collection.lower()
    collection_dir.mkdir(parents=True, exist_ok=True)
    
    total_packages = 0
    
    for year in years:
        # GovInfo API requires yyyy-MM-dd format
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        logger.info(f"Downloading {collection_name} for {year}...")
        
        offset = 0
        page_count = 0
        year_packages = []
        
        while True:
            data = fetch_collection_packages(collection, start_date, end_date, offset)
            packages = data.get('packages', [])
            
            if not packages:
                break
            
            year_packages.extend(packages)
            page_count += 1
            
            logger.info(f"  Page {page_count}: {len(packages)} packages (total: {len(year_packages)})")
            
            # Check for next page
            next_page = data.get('nextPage')
            if not next_page:
                break
            
            # Extract offset from nextPage URL
            try:
                offset = int(next_page.split('offset=')[1].split('&')[0])
            except:
                break
            
            # Rate limiting
            time.sleep(0.5)
            
            # Save every 1000 packages to avoid memory issues
            if len(year_packages) >= 1000:
                output_file = collection_dir / f"{collection.lower()}_{year}_{page_count:04d}.json"
                with open(output_file, 'w') as f:
                    json.dump({'packages': year_packages, 'year': year, 'page': page_count}, f, indent=2)
                logger.info(f"  Saved chunk: {output_file.name} ({len(year_packages)} packages)")
                year_packages = []
        
        # Save remaining packages
        if year_packages:
            output_file = collection_dir / f"{collection.lower()}_{year}_final.json"
            with open(output_file, 'w') as f:
                json.dump({'packages': year_packages, 'year': year}, f, indent=2)
            logger.info(f"  Saved final: {output_file.name} ({len(year_packages)} packages)")
        
        year_total = sum(1 for f in collection_dir.glob(f"{collection.lower()}_{year}*.json") 
                        for data in [json.load(open(f))] 
                        for _ in data.get('packages', []))
        logger.info(f"  {year} total: {year_total} packages")
        total_packages += year_total
        
        # Brief pause between years
        time.sleep(1)
    
    logger.info(f"{collection_name} complete: {total_packages} total packages")
    return total_packages


def download_granules(package_id: str, collection: str) -> List[Dict]:
    """Download granules (individual items) for a package"""
    url = f"{BASE_URL}/packages/{package_id}/granules"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('granules', [])
    except Exception as e:
        logger.debug(f"Error fetching granules for {package_id}: {e}")
    
    return []


def download_package_summary(package_id: str) -> Dict:
    """Download full package summary"""
    url = f"{BASE_URL}/packages/{package_id}/summary"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.debug(f"Error fetching summary for {package_id}: {e}")
    
    return {}


def download_related_documents(package_id: str, collection: str):
    """Download related documents for a package"""
    package_dir = BASE_DIR / collection.lower() / "related" / package_id.replace('/', '_')
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Download granules
    granules = download_granules(package_id, collection)
    if granules:
        granules_file = package_dir / "granules.json"
        with open(granules_file, 'w') as f:
            json.dump({'granules': granules}, f, indent=2)
        logger.info(f"  Saved {len(granules)} granules for {package_id}")
    
    # Download summary
    summary = download_package_summary(package_id)
    if summary:
        summary_file = package_dir / "summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)


def main():
    logger.info("=" * 80)
    logger.info("GOVINFO BULK DOWNLOAD")
    logger.info("=" * 80)
    logger.info(f"Target: Large volume of government documents")
    logger.info(f"Output: {BASE_DIR}")
    logger.info("=" * 80)
    
    total_count = 0
    
    # 1. Federal Register (2020-2024) - ~60,000 documents/year
    logger.info("\n[1/5] Federal Register (2020-2024)")
    count = download_collection('FR', 'Federal Register', [2020, 2021, 2022, 2023, 2024])
    total_count += count
    
    # 2. Congressional Bills (118th Congress, 2023-2024)
    logger.info("\n[2/5] Congressional Bills (118th Congress)")
    count = download_collection('BILLS', 'Congressional Bills', [2023, 2024])
    total_count += count
    
    # 3. Congressional Reports (2020-2024)
    logger.info("\n[3/5] Congressional Reports (2020-2024)")
    count = download_collection('CRPT', 'Congressional Reports', [2020, 2021, 2022, 2023, 2024])
    total_count += count
    
    # 4. USCOURTS (2022-2024)
    logger.info("\n[4/5] Court Opinions (2022-2024)")
    count = download_collection('USCOURTS', 'Court Opinions', [2022, 2023, 2024])
    total_count += count
    
    # 5. US Code (2020-2024)
    logger.info("\n[5/5] US Code (2020-2024)")
    count = download_collection('USCODE', 'US Code', [2020, 2021, 2022, 2023, 2024])
    total_count += count
    
    logger.info("=" * 80)
    logger.info(f"BULK DOWNLOAD COMPLETE")
    logger.info(f"Total packages downloaded: {total_count}")
    logger.info("=" * 80)
    
    # Update inventory
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost', database='epstein',
            user='cbwinslow', password='123qweasd'
        )
        cur = conn.cursor()
        cur.execute("""
            UPDATE data_inventory 
            SET status = 'downloaded',
                actual_records = %s,
                last_updated = NOW()
            WHERE source_name = 'GovInfo Federal Register'
        """, (total_count,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Inventory updated: {total_count} records")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


if __name__ == "__main__":
    main()
