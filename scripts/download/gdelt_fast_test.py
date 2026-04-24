#!/usr/bin/env python3
"""
Quick validation test for GDELT pipeline - uses just 2 days of data
"""

import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from datetime import datetime
from pathlib import Path
import pandas as pd

from gdeltnews.download import download
from gdeltnews.reconstruct import reconstruct
from gdeltnews.filtermerge import filtermerge

# Test with just 2 days around Epstein arrest (July 6-7, 2019)
TEST_START = "2019-07-06T00:00:00"
TEST_END = "2019-07-07T23:59:59"

data_dir = Path('/home/cbwinslow/workspace/epstein-data/gdelt/test')
raw_dir = data_dir / 'raw'
recon_dir = data_dir / 'reconstructed'
final_csv = data_dir / 'epstein_test.csv'

print("="*60)
print("GDELT PIPELINE VALIDATION TEST")
print("="*60)
print(f"Date range: {TEST_START} to {TEST_END}")
print(f"Data directory: {data_dir}")
print()

# 1. DOWNLOAD
print("Step 1: Downloading n-grams...")
raw_dir.mkdir(parents=True, exist_ok=True)
stats = download(TEST_START, TEST_END, outdir=str(raw_dir), decompress=True, show_progress=True)
print(f"Downloaded: {stats.files_downloaded if hasattr(stats, 'files_downloaded') else 'unknown'} files")
print()

# 2. RECONSTRUCT
print("Step 2: Reconstructing articles...")
recon_dir.mkdir(parents=True, exist_ok=True)
reconstruct(
    input_dir=str(raw_dir),
    output_dir=str(recon_dir),
    language="en",
    processes=4,
    verbose=True
)
recon_files = list(recon_dir.glob("*.csv"))
print(f"Reconstructed: {len(recon_files)} files")
print()

# 3. FILTER
print("Step 3: Filtering for Epstein content...")
query = '(Jeffrey Epstein OR Epstein OR "Ghislaine Maxwell")'
filtermerge(
    input_dir=str(recon_dir),
    output_file=str(final_csv),
    query=query,
    verbose=True
)

# 4. VALIDATE RESULTS
if final_csv.exists():
    df = pd.read_csv(final_csv)
    print(f"\n{'='*60}")
    print(f"RESULTS: {len(df)} Epstein-related articles found")
    print(f"{'='*60}")

    if len(df) > 0:
        print("\nSample articles:")
        for i, row in df.head(3).iterrows():
            print(f"\n{i+1}. {row.get('title', 'No title')[:80]}...")
            print(f"   URL: {row.get('url', 'No URL')[:60]}...")
            print(f"   Date: {row.get('date', 'No date')}")
            content = str(row.get('text', ''))
            print(f"   Words: {len(content.split())}")
else:
    print("\nNo results file created - no articles matched")

print(f"\n{'='*60}")
print("TEST COMPLETE")
print(f"{'='*60}")
