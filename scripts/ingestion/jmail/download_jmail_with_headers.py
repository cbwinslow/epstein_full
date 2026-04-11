#!/usr/bin/env python3
"""
Download jmail datasets with proper User-Agent headers.
"""
import os
import urllib.request
import ssl
from pathlib import Path

# Create SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

DATA_DIR = Path("/home/cbwinslow/workspace/epstein-data/downloads")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, output_path, description):
    """Download a file with proper headers."""
    print(f"\n[DOWNLOADING] {description}")
    print(f"  From: {url}")
    print(f"  To: {output_path}")
    
    # Create request with headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/octet-stream,application/x-parquet,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ssl_context, timeout=300) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        size = os.path.getsize(output_path)
        print(f"  ✓ Complete - {size / 1024 / 1024:.1f} MB")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

# Download jmail datasets
print("=" * 60)
print("JMAIL DATA DOWNLOAD (with headers)")
print("=" * 60)

jmail_files = [
    ("https://data.jmail.world/v1/emails.parquet", "jmail_emails_full.parquet"),
    ("https://data.jmail.world/v1/documents.parquet", "jmail_documents.parquet"),
]

for url, filename in jmail_files:
    download_file(url, DATA_DIR / filename, filename)

print("\n" + "=" * 60)
print("DOWNLOAD COMPLETE")
print("=" * 60)
print(f"Files saved to: {DATA_DIR}")
