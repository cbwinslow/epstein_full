#!/usr/bin/env python3
"""
Download ICIJ datasets using requests
"""

import os
import requests
from urllib.parse import urlparse

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data/icij-data"
os.makedirs(DATA_ROOT, exist_ok=True)

urls = [
    ("https://offshoreleaks-data.icij.org/offshore_leaks_csv.2022-11-15.zip", "offshore-leaks.zip"),
    ("https://offshoreleaks-data.icij.org/panama_papers_csv.2022-05-01.zip", "panama-papers.zip"),
    ("https://offshoreleaks-data.icij.org/paradise_papers_csv.2017-11-05.zip", "paradise-papers.zip"),
]

session = requests.Session()

for url, filename in urls:
    output_path = os.path.join(DATA_ROOT, filename)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000000:
        print(f"Already exists: {filename} ({os.path.getsize(output_path) / 1024 / 1024:.1f} MB)")
        continue
    
    print(f"Downloading {filename}...")
    try:
        response = session.get(url, stream=True, timeout=300)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        size = os.path.getsize(output_path) / 1024 / 1024
        print(f"✓ Downloaded {filename} ({size:.1f} MB)")
    except Exception as e:
        print(f"✗ Failed {filename}: {e}")

print("Done")
