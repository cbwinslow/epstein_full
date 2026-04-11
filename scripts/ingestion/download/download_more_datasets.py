#!/usr/bin/env python3
"""
Download additional Epstein datasets
"""

import os
import requests

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data/downloads"
os.makedirs(DATA_ROOT, exist_ok=True)

urls = [
    ("https://data.jmail.world/v1/emails-slim.parquet", "emails-slim.parquet"),
    ("https://oversight.house.gov/wp-content/uploads/2025/11/EPSTEIN-DATA.zip", "house-oversight.zip"),
]

session = requests.Session()

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
