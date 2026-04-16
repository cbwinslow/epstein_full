#!/usr/bin/env python3
"""
Bulk Download Lobbying Disclosure Act (LDA) Data
Downloads quarterly XML files from Senate LDA
No API key required - bulk downloads
"""

import requests
import zipfile
import logging
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/lobbying")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"lobbying_download_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BASE_DIR.mkdir(parents=True, exist_ok=True)

# Senate LDA bulk data URLs
# Years 2020-2024, quarterly files (Q1, Q2, Q3, Q4)
YEARS = [2020, 2021, 2022, 2023, 2024]
QUARTERS = ['1', '2', '3', '4']


def build_lobbying_url(year: int, quarter: str) -> str:
    """Build URL for lobbying disclosure quarterly file"""
    # Senate LDA format: YYYY_Q.zip
    return f"https://lda.senate.gov/filings/public/filing/do/filingHistoryByFilingYear?filingYear={year}"


def download_lobbying_filings(year: int) -> int:
    """Download all lobbying filings for a year"""
    url = f"https://lda.senate.gov/filings/public/filing/do/filingHistoryByFilingYear?filingYear={year}"
    
    logger.info(f"\n[Downloading lobbying data for {year}]")
    logger.info(f"URL: {url}")
    
    try:
        # Senate LDA website requires session/cookies for bulk download
        # Alternative: Download via their bulk XML export
        bulk_url = f"https://lda.senate.gov/filings/public/filing/do/downloadBulkData?format=xml&year={year}"
        
        response = requests.get(bulk_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=300)
        
        if response.status_code == 200 and len(response.content) > 1000:
            # Save ZIP file
            zip_path = BASE_DIR / f"lobbying_{year}.zip"
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            size_mb = len(response.content) / (1024 * 1024)
            logger.info(f"Downloaded: {size_mb:.2f} MB")
            
            # Extract if it's a ZIP
            if zipfile.is_zipfile(BytesIO(response.content)):
                with zipfile.ZipFile(BytesIO(response.content)) as zf:
                    xml_files = [f for f in zf.namelist() if f.endswith('.xml')]
                    for xml_file in xml_files:
                        extracted_path = BASE_DIR / f"{year}_{xml_file}"
                        with zf.open(xml_file) as src, open(extracted_path, 'wb') as dst:
                            dst.write(src.read())
                    logger.info(f"  Extracted {len(xml_files)} XML files")
                    return len(xml_files)
            else:
                # Save as single file
                xml_path = BASE_DIR / f"lobbying_{year}.xml"
                with open(xml_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"  Saved XML file")
                return 1
        else:
            logger.warning(f"  No data or small response: {len(response.content)} bytes")
            return 0
            
    except Exception as e:
        logger.error(f"Error downloading {year}: {e}")
        return 0


def download_ld2_filings():
    """Download LD-2 quarterly filings"""
    total_files = 0
    
    for year in YEARS:
        for quarter in QUARTERS:
            # LD-2 quarterly reports
            url = f"https://lda.senate.gov/filings/public/filing/do/downloadLd2Data?year={year}&quarter={quarter}"
            
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
                if response.status_code == 200 and len(response.content) > 1000:
                    file_path = BASE_DIR / f"LD2_{year}_Q{quarter}.xml"
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"  Downloaded LD2_{year}_Q{quarter}.xml ({len(response.content)/1024:.1f} KB)")
                    total_files += 1
                else:
                    logger.debug(f"  No data for {year} Q{quarter}")
            except Exception as e:
                logger.debug(f"  Error for {year} Q{quarter}: {e}")
    
    return total_files


def download_ld1_registrations():
    """Download LD-1 registration statements"""
    total_files = 0
    
    for year in YEARS:
        url = f"https://lda.senate.gov/filings/public/filing/do/downloadLd1Data?year={year}"
        
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
            if response.status_code == 200 and len(response.content) > 1000:
                file_path = BASE_DIR / f"LD1_{year}.xml"
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"  Downloaded LD1_{year}.xml ({len(response.content)/1024:.1f} KB)")
                total_files += 1
        except Exception as e:
            logger.debug(f"  Error for LD1 {year}: {e}")
    
    return total_files


def main():
    logger.info("=" * 80)
    logger.info("LOBBYING DISCLOSURE BULK DOWNLOAD")
    logger.info("=" * 80)
    logger.info(f"Output: {BASE_DIR}")
    logger.info("=" * 80)
    
    total_ld2 = download_ld2_filings()
    total_ld1 = download_ld1_registrations()
    
    total_files = total_ld2 + total_ld1
    
    logger.info("=" * 80)
    logger.info(f"DOWNLOAD COMPLETE: {total_files} files")
    logger.info(f"  LD-2 Quarterly Reports: {total_ld2}")
    logger.info(f"  LD-1 Registrations: {total_ld1}")
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
            WHERE source_name = 'Lobbying Disclosure'
        """, (total_files,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Inventory updated: {total_files} files")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


if __name__ == "__main__":
    main()
