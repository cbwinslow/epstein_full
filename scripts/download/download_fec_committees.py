#!/usr/bin/env python3
"""
Bulk Download FEC Candidate & Committee Data
Downloads candidates, committees, and their metadata
No API key required - bulk CSV downloads
"""

import requests
import zipfile
import logging
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fec_committees")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"fec_committees_download_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load secrets if not already in environment
import os
if not os.environ.get('FEC_API_KEY'):
    secrets_file = Path.home() / 'workspace' / 'epstein' / '.bash_secrets'
    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                if line.startswith('export '):
                    key_val = line[7:].strip().split('=', 1)
                    if len(key_val) == 2 and key_val[0] not in os.environ:
                        os.environ[key_val[0]] = key_val[1].strip('"\'')

BASE_DIR.mkdir(parents=True, exist_ok=True)

# FEC bulk data URLs - Updated April 2026
FEC_URLS = {
    'candidates_2024': 'https://www.fec.gov/files/bulk-downloads/2024/weball24.zip',
    'candidates_2022': 'https://www.fec.gov/files/bulk-downloads/2022/weball22.zip',
    'candidates_2020': 'https://www.fec.gov/files/bulk-downloads/2020/weball20.zip',
    'committees_2024': 'https://www.fec.gov/files/bulk-downloads/2024/cm24.zip',
    'committees_2022': 'https://www.fec.gov/files/bulk-downloads/2022/cm22.zip',
    'committees_2020': 'https://www.fec.gov/files/bulk-downloads/2020/cm20.zip',
    'candidate_committee_links_2024': 'https://www.fec.gov/files/bulk-downloads/2024/ccl24.zip',
    'pac_summary_2024': 'https://www.fec.gov/files/bulk-downloads/2024/webk24.zip',
}


def download_and_extract(name: str, url: str) -> int:
    """Download ZIP and extract CSV"""
    logger.info(f"\n[Downloading {name}]")
    logger.info(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=300)
        response.raise_for_status()
        
        size_mb = len(response.content) / (1024 * 1024)
        logger.info(f"Downloaded: {size_mb:.2f} MB")
        
        # Extract ZIP
        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            csv_files = [f for f in zf.namelist() if f.endswith('.csv') or f.endswith('.txt')]
            logger.info(f"Files in archive: {len(csv_files)}")
            
            for csv_file in csv_files:
                extracted_path = BASE_DIR / f"{name}_{csv_file}"
                with zf.open(csv_file) as src, open(extracted_path, 'wb') as dst:
                    dst.write(src.read())
                logger.info(f"  Extracted: {extracted_path.name}")
        
        return len(csv_files)
        
    except Exception as e:
        logger.error(f"Error downloading {name}: {e}")
        return 0


def main():
    logger.info("=" * 80)
    logger.info("FEC CANDIDATES & COMMITTEES BULK DOWNLOAD")
    logger.info("=" * 80)
    logger.info(f"Output: {BASE_DIR}")
    logger.info("=" * 80)
    
    total_files = 0
    
    for name, url in FEC_URLS.items():
        count = download_and_extract(name, url)
        total_files += count
        logger.info(f"✅ {name}: {count} files")
    
    logger.info("=" * 80)
    logger.info(f"DOWNLOAD COMPLETE: {total_files} files")
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
            SET status = 'downloaded', actual_records = %s, last_updated = NOW()
            WHERE source_name = 'FEC Candidates & Committees'
        """, (total_files,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Inventory updated: {total_files} files")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


if __name__ == "__main__":
    main()
