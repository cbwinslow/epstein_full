#!/usr/bin/env python3
"""
Download manager for all Epstein datasets
"""

import logging
import os
import subprocess
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data"
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/download_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

DOWNLOADS = [
    # ICIJ datasets
    ("https://offshoreleaks-data.icij.org/offshore_leaks_csv.2022-11-15.zip", "icij/offshore-leaks.zip"),
    ("https://offshoreleaks-data.icij.org/panama_papers_csv.2022-05-01.zip", "icij/panama-papers.zip"),
    ("https://offshoreleaks-data.icij.org/paradise_papers_csv.2017-11-05.zip", "icij/paradise-papers.zip"),
    # HuggingFace datasets (using wget for raw files)
    ("https://huggingface.co/datasets/genevera/FULL_EPSTEIN_INDEX/resolve/main/data/train-00000-of-00001.parquet", "hf/full-epstein-index.parquet"),
]

GIT_REPOS = [
    ("https://huggingface.co/datasets/teyler/epstein-files-20k", "hf/epstein-files-20k"),
    ("https://huggingface.co/datasets/svetfm/epstein-fbi-files", "hf/fbi-files-2"),
]


def download_wget(url, output_path):
    """Download using wget."""
    full_path = os.path.join(DATA_ROOT, "downloads", output_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    cmd = ["wget", "-c", "--timeout=60", "--tries=3", "-O", full_path, url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if result.returncode == 0:
            logging.info(f"✓ Downloaded {output_path}")
            return True
        else:
            logging.error(f"✗ Failed {output_path}: {result.stderr[:200]}")
            return False
    except Exception as e:
        logging.error(f"✗ Error {output_path}: {e}")
        return False


def download_git(repo_url, output_path):
    """Clone git repository."""
    full_path = os.path.join(DATA_ROOT, "downloads", output_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    if os.path.exists(full_path):
        logging.info(f"Already exists: {output_path}")
        return True
    
    cmd = ["git", "clone", "--depth", "1", repo_url, full_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if result.returncode == 0:
            logging.info(f"✓ Cloned {output_path}")
            return True
        else:
            logging.error(f"✗ Failed {output_path}: {result.stderr[:200]}")
            return False
    except Exception as e:
        logging.error(f"✗ Error {output_path}: {e}")
        return False


def main():
    logging.info("=" * 60)
    logging.info("DOWNLOAD ALL EPSTEIN DATASETS")
    logging.info("=" * 60)
    
    success = 0
    failed = 0
    
    # Download with wget
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(download_wget, url, path): path for url, path in DOWNLOADS}
        
        for future in as_completed(futures):
            path = futures[future]
            if future.result():
                success += 1
            else:
                failed += 1
    
    # Clone git repos
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(download_git, url, path): path for url, path in GIT_REPOS}
        
        for future in as_completed(futures):
            path = futures[future]
            if future.result():
                success += 1
            else:
                failed += 1
    
    logging.info("=" * 60)
    logging.info(f"COMPLETE: {success} success, {failed} failed")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()
