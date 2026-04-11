#!/usr/bin/env python3
"""
Download manager - controlled parallel downloads with rate limiting
"""

import json
import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")
LOG_DIR = f"{DATA_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Rate limiting config
MAX_CONCURRENT = 2  # Don't overwhelm bandwidth
DELAY_BETWEEN_DOWNLOADS = 2  # seconds

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/download_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

DOWNLOAD_QUEUES = {
    "fbi_vault": {
        "dir": f"{DATA_ROOT}/downloads/fbi_vault",
        "urls": [
            ("https://vault.fbi.gov/Epstein%20Jeffrey/Epstein%20Jeffrey%20Part%2001%20of%2001/view", "fbi_part_01.pdf"),
        ],
        "priority": "high",
        "active": True
    },
    "icij_offshore": {
        "dir": f"{DATA_ROOT}/downloads/icij",
        "urls": [
            ("https://offshoreleaks.icij.org/nodes/80136410", "epstein_offshore_links.json"),
        ],
        "priority": "medium",
        "active": False  # Skip for now - very large
    },
    "courtlistener": {
        "dir": f"{DATA_ROOT}/downloads/courtlistener",
        "urls": [],  # Will be populated from search
        "priority": "medium",
        "active": False
    }
}


def download_with_aria2c(url, dest_path, max_retries=3):
    """Download using aria2c with resume support."""
    for attempt in range(max_retries):
        try:
            cmd = [
                "aria2c",
                "-x", "4", "-s", "4",  # 4 connections
                "--continue=true",
                "--max-tries=3",
                "--retry-wait=5",
                "--timeout=60",
                "--connect-timeout=30",
                "-d", str(Path(dest_path).parent),
                "-o", str(Path(dest_path).name),
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 or "download completed" in result.stdout.lower():
                logging.info(f"✓ Downloaded: {url}")
                return True
            else:
                logging.warning(f"Download attempt {attempt+1} failed for {url}: {result.stderr[:200]}")
                time.sleep(5)
                
        except subprocess.TimeoutExpired:
            logging.warning(f"Download timeout for {url}")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Download error for {url}: {e}")
            time.sleep(5)
    
    return False


def download_with_wget(url, dest_path):
    """Fallback to wget for problematic URLs."""
    try:
        cmd = ["wget", "-q", "--show-progress", "-O", dest_path, url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return result.returncode == 0
    except Exception as e:
        logging.error(f"wget failed: {e}")
        return False


def process_queue(queue_name, queue_config):
    """Process a single download queue."""
    if not queue_config["active"]:
        logging.info(f"Skipping inactive queue: {queue_name}")
        return 0
    
    os.makedirs(queue_config["dir"], exist_ok=True)
    downloaded = 0
    failed = 0
    
    logging.info(f"Starting queue: {queue_name} ({len(queue_config['urls'])} files)")
    
    for url, filename in queue_config["urls"]:
        dest_path = os.path.join(queue_config["dir"], filename)
        
        # Skip if already exists and not empty
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
            logging.info(f"Skipping (exists): {filename}")
            continue
        
        logging.info(f"Downloading: {filename}")
        
        if download_with_aria2c(url, dest_path):
            downloaded += 1
        else:
            # Try wget fallback
            logging.info(f"Trying wget fallback for: {filename}")
            if download_with_wget(url, dest_path):
                downloaded += 1
            else:
                failed += 1
                logging.error(f"Failed to download: {filename}")
        
        time.sleep(DELAY_BETWEEN_DOWNLOADS)
    
    logging.info(f"Queue {queue_name} complete: {downloaded} downloaded, {failed} failed")
    return downloaded


def main():
    logging.info("=" * 60)
    logging.info("DOWNLOAD MANAGER - Starting controlled downloads")
    logging.info("=" * 60)
    
    total_downloaded = 0
    
    # Process by priority
    priorities = ["high", "medium", "low"]
    
    for priority in priorities:
        logging.info(f"\nProcessing {priority} priority queues...")
        
        for queue_name, queue_config in DOWNLOAD_QUEUES.items():
            if queue_config.get("priority") == priority and queue_config.get("active"):
                count = process_queue(queue_name, queue_config)
                total_downloaded += count
    
    logging.info("\n" + "=" * 60)
    logging.info(f"DOWNLOAD MANAGER COMPLETE: {total_downloaded} files downloaded")
    logging.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
