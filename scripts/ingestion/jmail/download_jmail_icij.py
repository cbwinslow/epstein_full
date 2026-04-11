#!/usr/bin/env python3
"""
Download jmail and ICIJ datasets using correct official URLs.
"""
import os
import urllib.request
import ssl
from pathlib import Path

# Create SSL context that allows us to download
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

DATA_DIR = Path("/home/cbwinslow/workspace/epstein-data/downloads")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, output_path, description):
    """Download a file with progress."""
    print(f"\n[DOWNLOADING] {description}")
    print(f"  From: {url}")
    print(f"  To: {output_path}")
    
    try:
        urllib.request.urlretrieve(url, output_path)
        size = os.path.getsize(output_path)
        print(f"  ✓ Complete - {size / 1024 / 1024:.1f} MB")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

# Download jmail datasets
print("=" * 60)
print("JMAIL DATA DOWNLOAD")
print("=" * 60)

jmail_files = [
    ("https://data.jmail.world/v1/emails.parquet", "jmail_emails_full.parquet"),
    ("https://data.jmail.world/v1/documents.parquet", "jmail_documents.parquet"),
    ("https://data.jmail.world/v1/photos.parquet", "jmail_photos.parquet"),
    ("https://data.jmail.world/v1/messages.parquet", "jmail_imessages.parquet"),
]

for url, filename in jmail_files:
    download_file(url, DATA_DIR / filename, filename)

# Download ICIJ Offshore Leaks
print("\n" + "=" * 60)
print("ICIJ OFFSHORE LEAKS DOWNLOAD")
print("=" * 60)

download_file(
    "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip",
    DATA_DIR / "icij_offshore_leaks_full.zip",
    "ICIJ Offshore Leaks Full Database"
)

print("\n" + "=" * 60)
print("DOWNLOAD COMPLETE")
print("=" * 60)
print(f"Files saved to: {DATA_DIR}")
print("\nTo import into PostgreSQL:")
print("  python3 import_jmail_full.py")
print("  python3 import_icij.py")
