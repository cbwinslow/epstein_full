#!/usr/bin/env python3
"""Download Congress.gov data via API"""
import os
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get('CONGRESS_API_KEY')
if not API_KEY:
    logger.error("CONGRESS_API_KEY not set in environment")
    sys.exit(1)

base_url = "https://api.congress.gov/v3"
headers = {'X-API-Key': API_KEY}

# Get recent bills (118th Congress)
logger.info("Fetching Congress bills...")

try:
    url = f"{base_url}/bill?congress=118&limit=100&format=json"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    
    output_file = BASE_DIR / f"congress_bills_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    bills_count = len(data.get('bills', []))
    logger.info(f"✅ Downloaded {bills_count} bills to {output_file}")
    
except Exception as e:
    logger.error(f"❌ Congress download failed: {e}")

logger.info("Congress.gov download complete")
