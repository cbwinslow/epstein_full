#!/usr/bin/env python3
"""
Download Epstein datasets from HuggingFace
"""

import logging
import os
import subprocess
from datetime import datetime

DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/hf_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

DATASETS = [
    ("svetfm/epstein-fbi-files", "fbi-files"),
    ("genevera/FULL_EPSTEIN_INDEX", "full-epstein-index"),
    ("teyler/epstein-files-20k", "epstein-files-20k"),
]


def download_dataset(repo_id, local_name):
    """Download dataset from HuggingFace using huggingface-cli."""
    output_dir = f"{DATA_ROOT}/hf-datasets/{local_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    logging.info(f"Downloading {repo_id} to {output_dir}")
    
    # Try huggingface-cli first
    cmd = [
        "huggingface-cli", "download",
        repo_id,
        "--repo-type", "dataset",
        "--local-dir", output_dir,
        "--resume-download"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if result.returncode == 0:
            logging.info(f"✓ Downloaded {repo_id}")
            return True
        else:
            logging.error(f"Failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        logging.error(f"Error: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info("HUGGINGFACE DATASET DOWNLOAD")
    logging.info("=" * 60)
    
    success = 0
    for repo_id, local_name in DATASETS:
        if download_dataset(repo_id, local_name):
            success += 1
    
    logging.info(f"\nComplete: {success}/{len(DATASETS)} datasets downloaded")


if __name__ == "__main__":
    main()
