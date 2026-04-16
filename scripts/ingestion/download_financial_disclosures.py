#!/usr/bin/env python3
"""
Bulk Download House & Senate Financial Disclosures
Downloads personal financial disclosure statements
No API key required - bulk data from clerk.house.gov and senate.gov
"""

import requests
import zipfile
import logging
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/financial_disclosures")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"financial_disclosures_download_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BASE_DIR.mkdir(parents=True, exist_ok=True)

# House Financial Disclosures bulk data
HOUSE_URLS = {
    '2024': 'https://disclosures-clerk.house.gov/public_disc/privatelaw/2024.zip',
    '2023': 'https://disclosures-clerk.house.gov/public_disc/privatelaw/2023.zip',
    '2022': 'https://disclosures-clerk.house.gov/public_disc/privatelaw/2022.zip',
    '2021': 'https://disclosures-clerk.house.gov/public_disc/privatelaw/2021.zip',
    '2020': 'https://disclosures-clerk.house.gov/public_disc/privatelaw/2020.zip',
}

# Senate Financial Disclosures (requires different access pattern)
# Note: Senate data is harder to access in bulk, using year-specific pages
SENATE_BASE_URL = "https://www.senate.gov/legislative/FinancialDisclosure.htm"


def download_house_disclosures(year: str, url: str) -> int:
    """Download House financial disclosures for a year"""
    year_dir = BASE_DIR / "house" / year
    year_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"\n[Downloading House disclosures for {year}]")
    logger.info(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=300)
        
        if response.status_code == 200 and len(response.content) > 1000:
            # Save ZIP file
            zip_path = year_dir / f"house_{year}.zip"
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            size_mb = len(response.content) / (1024 * 1024)
            logger.info(f"Downloaded: {size_mb:.2f} MB")
            
            # Extract ZIP
            if zipfile.is_zipfile(BytesIO(response.content)):
                with zipfile.ZipFile(BytesIO(response.content)) as zf:
                    files = zf.namelist()
                    for filename in files:
                        extracted_path = year_dir / filename
                        with zf.open(filename) as src, open(extracted_path, 'wb') as dst:
                            dst.write(src.read())
                    logger.info(f"  Extracted {len(files)} files")
                    return len(files)
            else:
                logger.info(f"  Saved as ZIP: {zip_path.name}")
                return 1
        else:
            logger.warning(f"  No data or small response: {len(response.content)} bytes")
            return 0
            
    except Exception as e:
        logger.error(f"Error downloading {year}: {e}")
        return 0


def download_senate_info():
    """Download Senate financial disclosure info page"""
    senate_dir = BASE_DIR / "senate"
    senate_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("\n[Checking Senate Financial Disclosures]")
    logger.info(f"URL: {SENATE_BASE_URL}")
    
    try:
        response = requests.get(SENATE_BASE_URL, timeout=30)
        
        info_file = senate_dir / "senate_disclosure_info.html"
        info_file.write_text(response.text)
        logger.info(f"  Saved info page: {info_file.name}")
        
        # Note: Senate data requires individual member lookup or specific requests
        logger.info("  Note: Senate disclosures require member-specific access")
        
        return 1
        
    except Exception as e:
        logger.error(f"Error accessing Senate data: {e}")
        return 0


def main():
    logger.info("=" * 80)
    logger.info("FINANCIAL DISCLOSURES BULK DOWNLOAD")
    logger.info("=" * 80)
    logger.info(f"Output: {BASE_DIR}")
    logger.info("=" * 80)
    
    total_files = 0
    
    # Download House disclosures
    logger.info("\n--- HOUSE OF REPRESENTATIVES ---")
    for year, url in HOUSE_URLS.items():
        count = download_house_disclosures(year, url)
        total_files += count
        logger.info(f"✅ {year}: {count} files")
    
    # Download Senate info
    logger.info("\n--- SENATE ---")
    count = download_senate_info()
    total_files += count
    
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
            WHERE source_name = 'House/Senate Financial Disclosures'
        """, (total_files,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Inventory updated: {total_files} files")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


if __name__ == "__main__":
    main()
