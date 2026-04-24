#!/usr/bin/env python3
"""
Download FEC 2024 Individual Contributions
Source: https://www.fec.gov/files/bulk-downloads/2024/indiv24.zip
"""

import os
import sys
import zipfile
import logging
import requests
from pathlib import Path
from datetime import datetime

# Setup paths
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fec")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Logging
log_file = Path("/home/cbwinslow/workspace/epstein/logs/ingestion") / f"fec_2024_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
FEC_URL = "https://www.fec.gov/files/bulk-downloads/2024/indiv24.zip"
OUTPUT_ZIP = BASE_DIR / "indiv24.zip"
OUTPUT_DIR = BASE_DIR / "indiv24_extracted"
CHUNK_SIZE = 8192 * 1024  # 8 MB chunks


def download_file():
    """Download FEC 2024 file with progress"""
    if OUTPUT_ZIP.exists():
        current_size = OUTPUT_ZIP.stat().st_size
        logger.info(f"Resuming download from {current_size / 1024 / 1024:.1f} MB")
        headers = {"Range": f"bytes={current_size}-"}
    else:
        current_size = 0
        headers = {}
    
    logger.info(f"Downloading {FEC_URL}...")
    
    try:
        response = requests.get(FEC_URL, headers=headers, stream=True, timeout=300)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        if total_size == 0 and current_size > 0:
            logger.info("File already complete")
            return True
        
        total_size += current_size
        
        mode = 'ab' if current_size > 0 else 'wb'
        with open(OUTPUT_ZIP, mode) as f:
            downloaded = current_size
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        if int(percent) % 10 == 0:
                            logger.info(f"Downloaded: {downloaded / 1024 / 1024:.1f} MB ({percent:.1f}%)")
        
        logger.info(f"✅ Download complete: {OUTPUT_ZIP}")
        logger.info(f"   Size: {OUTPUT_ZIP.stat().st_size / 1024 / 1024:.1f} MB")
        return True
        
    except Exception as e:
        logger.error(f"❌ Download failed: {e}")
        return False


def verify_and_extract():
    """Verify zip file and extract contents"""
    logger.info("Verifying zip file...")
    
    try:
        with zipfile.ZipFile(OUTPUT_ZIP, 'r') as zf:
            # Test zip integrity
            bad_file = zf.testzip()
            if bad_file:
                logger.error(f"❌ Corrupt file in zip: {bad_file}")
                return False
            
            # List contents
            files = zf.namelist()
            logger.info(f"Zip contains {len(files)} files:")
            for f in files[:5]:  # Show first 5
                info = zf.getinfo(f)
                logger.info(f"  - {f}: {info.file_size / 1024 / 1024:.1f} MB")
            
            # Extract
            OUTPUT_DIR.mkdir(exist_ok=True)
            logger.info(f"Extracting to {OUTPUT_DIR}...")
            zf.extractall(OUTPUT_DIR)
            logger.info(f"✅ Extraction complete")
            
            # Verify extracted files
            extracted_files = list(OUTPUT_DIR.iterdir())
            logger.info(f"Extracted {len(extracted_files)} files/directories")
            
            return True
            
    except zipfile.BadZipFile:
        logger.error(f"❌ Bad zip file: {OUTPUT_ZIP}")
        return False
    except Exception as e:
        logger.error(f"❌ Extraction failed: {e}")
        return False


def update_inventory():
    """Update database inventory"""
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host='localhost',
            database='epstein',
            user='cbwinslow',
            password='123qweasd'
        )
        cur = conn.cursor()
        
        # Check file size
        file_size = OUTPUT_ZIP.stat().st_size if OUTPUT_ZIP.exists() else 0
        
        cur.execute("""
            UPDATE data_inventory 
            SET status = 'downloaded',
                actual_records = 0,
                last_updated = NOW(),
                metadata = jsonb_set(
                    jsonb_set(metadata, '{download_info}', '{}'::jsonb),
                    '{file_size_mb}',
                    to_jsonb(%s)
                )
            WHERE source_name = 'FEC 2024 Individual Contributions'
        """, (file_size / 1024 / 1024,))
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Inventory updated")
        
    except Exception as e:
        logger.error(f"⚠️ Failed to update inventory: {e}")


def main():
    """Main download process"""
    logger.info("=" * 80)
    logger.info("FEC 2024 INDIVIDUAL CONTRIBUTIONS DOWNLOAD")
    logger.info("=" * 80)
    logger.info(f"Target: {FEC_URL}")
    logger.info(f"Output: {OUTPUT_ZIP}")
    logger.info("=" * 80)
    
    # Download
    if not download_file():
        sys.exit(1)
    
    # Verify and extract
    if not verify_and_extract():
        sys.exit(1)
    
    # Update inventory
    update_inventory()
    
    logger.info("=" * 80)
    logger.info("✅ FEC 2024 DOWNLOAD COMPLETE")
    logger.info("=" * 80)
    logger.info(f"File: {OUTPUT_ZIP}")
    logger.info(f"Extracted: {OUTPUT_DIR}")
    logger.info("Next: Run import script to load to PostgreSQL")


if __name__ == "__main__":
    main()
