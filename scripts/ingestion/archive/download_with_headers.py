#!/usr/bin/env python3
"""
Download Epstein datasets with headers
"""

import os
import requests

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data/downloads"
os.makedirs(DATA_ROOT, exist_ok=True)

urls = [
    ("https://data.jmail.world/v1/emails-slim.parquet", "emails-slim.parquet"),
    ("https://www.courtlistener.com/api/rest/v3/?type=dockets&case_name__icontains=epstein&format=json", "courtlistener.json"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json,text/html",
}

session = requests.Session()
session.headers.update(headers)

for url, filename in urls:
    output_path = os.path.join(DATA_ROOT, filename)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000000:
        print(f"Already exists: {filename}")
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
