#!/usr/bin/env python3
"""Download White House Visitor Logs"""
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/whitehouse")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Download 2024 CSV
urls = [
    "https://www.whitehouse.gov/wp-content/uploads/2024/01/WhiteHouse-WAVES-Access-Records-2023.csv",
    "https://www.whitehouse.gov/wp-content/uploads/2025/01/WhiteHouse-WAVES-Access-Records-2024.csv",
]

for url in urls:
    filename = url.split('/')[-1]
    output = BASE_DIR / filename
    
    if output.exists():
        logger.info(f"{filename} already exists, skipping")
        continue
    
    logger.info(f"Downloading {filename}...")
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
        r.raise_for_status()
        output.write_bytes(r.content)
        logger.info(f"✅ Downloaded {filename} ({len(r.content)/1024/1024:.1f} MB)")
    except Exception as e:
        logger.error(f"❌ Failed {filename}: {e}")

logger.info("White House download complete")
