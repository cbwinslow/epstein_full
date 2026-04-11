#!/usr/bin/env python3
"""
Download ICIJ Offshore Leaks data
"""

import logging
import os
import subprocess
from datetime import datetime

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data"
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/icij_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

ICIJ_URLS = [
    # Offshore Leaks
    ("https://offshoreleaks-data.icij.org/offshore_leaks_csv.2022-11-15.zip", "offshore-leaks"),
    # Panama Papers
    ("https://offshoreleaks-data.icij.org/panama_papers_csv.2022-05-01.zip", "panama-papers"),
    # Paradise Papers
    ("https://offshoreleaks-data.icij.org/paradise_papers_csv.2017-11-05.zip", "paradise-papers"),
]


def download_icij():
    """Download ICIJ datasets using aria2c."""
    output_dir = f"{DATA_ROOT}/icij-data"
    os.makedirs(output_dir, exist_ok=True)
    
    for url, name in ICIJ_URLS:
        logging.info(f"Downloading {name} from {url}")
        
        cmd = [
            "aria2c",
            "-d", output_dir,
            "-o", f"{name}.zip",
            "--max-concurrent-downloads=4",
            "--split=16",
            "--continue=true",
            url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            if result.returncode == 0:
                logging.info(f"✓ Downloaded {name}")
            else:
                logging.error(f"Failed {name}: {result.stderr[:200]}")
        except Exception as e:
            logging.error(f"Error {name}: {e}")


def main():
    logging.info("=" * 60)
    logging.info("ICIJ OFFSHORE LEAKS DOWNLOAD")
    logging.info("=" * 60)
    
    download_icij()
    logging.info("Complete")


if __name__ == "__main__":
    main()
