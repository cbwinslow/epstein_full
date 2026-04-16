#!/usr/bin/env python3
"""
Bulk Download FARA (Foreign Agents Registration Act) Data
Downloads registration statements, supplements, and amendments
No API key required - bulk XML from DOJ
"""

import requests
import zipfile
import logging
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fara")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"fara_download_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BASE_DIR.mkdir(parents=True, exist_ok=True)

# FARA bulk data URLs (publicly available)
FARA_URLS = {
    'registrations': 'https://efile.fara.gov/bulk/Registrations.xml.zip',
    'supplements': 'https://efile.fara.gov/bulk/Supplements.xml.zip',
    'amendments': 'https://efile.fara.gov/bulk/Amendments.xml.zip',
    'exhibits': 'https://efile.fara.gov/bulk/Exhibits.xml.zip',
    'foreign_principals': 'https://efile.fara.gov/bulk/ForeignPrincipals.xml.zip',
}


def download_and_extract(name: str, url: str) -> int:
    """Download ZIP and extract XML"""
    logger.info(f"\n[Downloading {name}]")
    logger.info(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=300, stream=True)
        response.raise_for_status()
        
        size_mb = len(response.content) / (1024 * 1024)
        logger.info(f"Downloaded: {size_mb:.2f} MB")
        
        # Extract ZIP
        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            xml_files = [f for f in zf.namelist() if f.endswith('.xml')]
            logger.info(f"XML files in archive: {len(xml_files)}")
            
            for xml_file in xml_files:
                extracted_path = BASE_DIR / f"{name}_{xml_file}"
                with zf.open(xml_file) as src, open(extracted_path, 'wb') as dst:
                    dst.write(src.read())
                logger.info(f"  Extracted: {extracted_path.name}")
        
        return len(xml_files)
        
    except Exception as e:
        logger.error(f"Error downloading {name}: {e}")
        return 0


def main():
    logger.info("=" * 80)
    logger.info("FARA BULK DOWNLOAD")
    logger.info("=" * 80)
    logger.info(f"Output: {BASE_DIR}")
    logger.info("=" * 80)
    
    total_files = 0
    
    for name, url in FARA_URLS.items():
        count = download_and_extract(name, url)
        total_files += count
        logger.info(f"✅ {name}: {count} files")
    
    logger.info("=" * 80)
    logger.info(f"DOWNLOAD COMPLETE: {total_files} XML files")
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
            WHERE source_name = 'FARA (Foreign Agents Registration)'
        """, (total_files,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Inventory updated: {total_files} files")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


if __name__ == "__main__":
    main()
