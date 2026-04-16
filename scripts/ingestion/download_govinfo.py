#!/usr/bin/env python3
"""Download GovInfo.gov data via API"""
import os
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get('GOVINFO_API_KEY')
if not API_KEY:
    logger.error("GOVINFO_API_KEY not set in environment")
    sys.exit(1)

base_url = "https://api.govinfo.gov"
headers = {'X-Api-Key': API_KEY}

# Get recent Federal Register collections
logger.info("Fetching GovInfo collections...")

try:
    url = f"{base_url}/collections/FR/2024"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    
    output_file = BASE_DIR / f"govinfo_collections_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    packages_count = len(data.get('packages', []))
    logger.info(f"✅ Downloaded {packages_count} packages to {output_file}")
    
except Exception as e:
    logger.error(f"❌ GovInfo download failed: {e}")

logger.info("GovInfo.gov download complete")
