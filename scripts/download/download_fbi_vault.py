#!/usr/bin/env python3
"""
Download FBI Vault Epstein files
"""

import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")
DEST_DIR = f"{DATA_ROOT}/fbi-vault"
os.makedirs(DEST_DIR, exist_ok=True)

LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/fbi_vault_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

# FBI Vault URLs - from DATA_INVENTORY.md
FBI_URLS = [
    # Main Epstein files
    ("https://vault.fbi.gov/Epstein%20Jeffrey/Epstein%20Jeffrey%20Part%2001%20of%2001/view", "epstein_part_01.pdf"),
    # Additional files if available
    ("https://vault.fbi.gov/Epstein%20Jeffrey%20Jeffrey%20Epstein%20Part%201%20of%202%20/view", "epstein_part_1_1.pdf"),
    ("https://vault.fbi.gov/Epstein%20Jeffrey%20Jeffrey%20Epstein%20Part%202%20of%202%20/view", "epstein_part_1_2.pdf"),
]


def download_file(url, dest_path, max_retries=3):
    """Download file with retry logic."""
    for attempt in range(max_retries):
        try:
            # Try aria2c first
            cmd = [
                "aria2c",
                "-x", "4", "-s", "4",
                "--continue=true",
                "--max-tries=3",
                "--retry-wait=5",
                "-d", str(Path(dest_path).parent),
                "-o", str(Path(dest_path).name),
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logging.info(f"✓ Downloaded: {url}")
                return True
            else:
                # FBI Vault often requires special handling - try wget
                logging.info(f"Trying wget for: {url}")
                cmd = ["wget", "-q", "-O", dest_path, url]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0 and os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
                    logging.info(f"✓ Downloaded via wget: {url}")
                    return True
                
                logging.warning(f"Download attempt {attempt+1} failed for {url}")
                time.sleep(5)
                
        except Exception as e:
            logging.error(f"Error downloading {url}: {e}")
            time.sleep(5)
    
    return False


def main():
    logging.info("=" * 60)
    logging.info("FBI VAULT DOWNLOAD STARTING")
    logging.info("=" * 60)
    
    downloaded = 0
    failed = 0
    skipped = 0
    
    for url, filename in FBI_URLS:
        dest_path = os.path.join(DEST_DIR, filename)
        
        # Skip if already exists
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
            logging.info(f"Skipping (exists): {filename} ({os.path.getsize(dest_path)} bytes)")
            skipped += 1
            continue
        
        logging.info(f"Downloading: {filename}")
        logging.info(f"  URL: {url}")
        
        if download_file(url, dest_path):
            file_size = os.path.getsize(dest_path) if os.path.exists(dest_path) else 0
            logging.info(f"  ✓ Saved to {dest_path} ({file_size} bytes)")
            downloaded += 1
        else:
            logging.error(f"  ✗ Failed to download: {filename}")
            failed += 1
        
        time.sleep(2)  # Be polite to FBI servers
    
    logging.info("\n" + "=" * 60)
    logging.info(f"FBI VAULT DOWNLOAD COMPLETE: {downloaded} downloaded, {skipped} skipped, {failed} failed")
    logging.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
