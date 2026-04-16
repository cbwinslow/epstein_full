#!/usr/bin/env python3
"""Download FARA registration XML"""
import requests
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fara")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# FARA search/registration XML
url = "https://efile.fara.gov/pls/apex/f?p=171:1:::::"
logger.info("Checking FARA data availability...")

try:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    logger.info(f"FARA site status: {r.status_code}")
    
    # Save info file
    info_file = BASE_DIR / "fara_info.txt"
    info_file.write_text(f"FARA check: {datetime.now()}\nStatus: {r.status_code}\n")
    logger.info("✅ FARA info saved")
    
except Exception as e:
    logger.error(f"❌ FARA check failed: {e}")

logger.info("FARA download script placeholder - manual download required")
