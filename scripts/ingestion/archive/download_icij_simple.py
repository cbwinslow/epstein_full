#!/usr/bin/env python3
"""
Simple downloader for Epstein datasets
"""

import os
import urllib.request
import ssl

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data/icij-data"
os.makedirs(DATA_ROOT, exist_ok=True)

# Create SSL context that doesn't verify certs (for some sites)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

urls = [
    ("https://offshoreleaks-data.icij.org/offshore_leaks_csv.2022-11-15.zip", "offshore-leaks.zip"),
    ("https://offshoreleaks-data.icij.org/panama_papers_csv.2022-05-01.zip", "panama-papers.zip"),
    ("https://offshoreleaks-data.icij.org/paradise_papers_csv.2017-11-05.zip", "paradise-papers.zip"),
]

for url, filename in urls:
    output_path = os.path.join(DATA_ROOT, filename)
    if os.path.exists(output_path):
        print(f"Already exists: {filename}")
        continue
    
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"✓ Downloaded {filename}")
    except Exception as e:
        print(f"✗ Failed {filename}: {e}")

print("Done")
