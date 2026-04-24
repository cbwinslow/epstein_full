#!/usr/bin/env python3
"""
Download 2025 FEC individual contribution data
URL: https://www.fec.gov/files/bulk-downloads/2025/indiv25.zip
"""

import requests
import os
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fec")
DATA_DIR.mkdir(parents=True, exist_ok=True)

FEC_URL = "https://www.fec.gov/files/bulk-downloads/2025/indiv25.zip"
OUTPUT_FILE = DATA_DIR / "indiv25.zip"

def download_file(url, output_path):
    """Download file with progress bar"""
    print(f"Downloading {url}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; DataResearch/1.0)'
    }
    
    response = requests.get(url, headers=headers, stream=True, timeout=300)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f:
        if total_size > 0:
            with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        else:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    
    print(f"✅ Downloaded to {output_path}")
    print(f"Size: {output_path.stat().st_size / (1024**3):.2f} GB")

if __name__ == "__main__":
    if OUTPUT_FILE.exists():
        print(f"⚠️  File already exists: {OUTPUT_FILE}")
        print(f"Size: {OUTPUT_FILE.stat().st_size / (1024**3):.2f} GB")
        overwrite = input("Overwrite? (y/n): ").lower() == 'y'
        if not overwrite:
            print("Skipping download")
            exit(0)
    
    try:
        download_file(FEC_URL, OUTPUT_FILE)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
