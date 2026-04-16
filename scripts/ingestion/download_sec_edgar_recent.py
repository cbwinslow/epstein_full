#!/usr/bin/env python3
"""Download recent SEC EDGAR Form 4 filings"""
import requests
import time
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/sec_edgar")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Research Bot contact@example.com',
    'Accept-Encoding': 'gzip, deflate',
}

# Get last 7 days of Form 4
base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
output_dir = BASE_DIR / f"form4_{datetime.now().strftime('%Y%m%d')}"
output_dir.mkdir(exist_ok=True)

for i in range(7):
    date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    logger.info(f"Fetching Form 4 for {date}...")
    
    try:
        time.sleep(0.2)  # Rate limiting
        url = f"{base_url}?action=getcurrent&type=4&date={date}&count=100&output=atom"
        r = requests.get(url, headers=HEADERS, timeout=30)
        
        if r.status_code == 200:
            output_file = output_dir / f"form4_{date}.xml"
            output_file.write_text(r.text)
            logger.info(f"✅ Saved {output_file.name}")
        else:
            logger.warning(f"⚠️ Status {r.status_code} for {date}")
            
    except Exception as e:
        logger.error(f"❌ Error for {date}: {e}")

logger.info(f"SEC EDGAR download complete. Files in: {output_dir}")
