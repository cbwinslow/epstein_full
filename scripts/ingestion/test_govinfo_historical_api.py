#!/usr/bin/env python3
"""Test GovInfo.gov API for historical data access"""
import os
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load secrets if not already in environment
if not os.environ.get('GOVINFO_API_KEY'):
    import subprocess
    secrets_file = Path.home() / 'workspace' / 'epstein' / '.bash_secrets'
    if secrets_file.exists():
        with open(secrets_file) as f:
            for line in f:
                if line.startswith('export '):
                    key_val = line[7:].strip().split('=', 1)
                    if len(key_val) == 2 and key_val[0] not in os.environ:
                        os.environ[key_val[0]] = key_val[1].strip('"\'')

API_KEY = os.environ.get('GOVINFO_API_KEY')
if not API_KEY:
    logger.error("GOVINFO_API_KEY not set")
    sys.exit(1)

BASE_URL = "https://api.govinfo.gov"
HEADERS = {'X-Api-Key': API_KEY}

# Test collections and date ranges
collections = ['FR', 'BILLS', 'USCOURTS', 'CRPT']
collection_names = {
    'FR': 'Federal Register',
    'BILLS': 'Bills',
    'USCOURTS': 'Court Opinions',
    'CRPT': 'Committee Reports'
}

# Test different years
test_years = [2000, 2005, 2010, 2015, 2020, 2023]

logger.info("Testing GovInfo.gov API for historical data access...")
logger.info("=" * 60)

results = {}

for collection in collections:
    collection_name = collection_names[collection]
    logger.info(f"\nTesting {collection_name} ({collection})...")
    
    for year in test_years:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        try:
            url = f"{BASE_URL}/published/{start_date}/{end_date}"
            params = {'offset': 0, 'pageSize': 100, 'collection': collection}
            response = requests.get(url, headers=HEADERS, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            packages = data.get('packages', [])
            count = len(packages)
            
            # Get total count from metadata if available
            total_count = data.get('count', count)
            
            logger.info(f"  ✅ {year}: {total_count} packages available (sampled {count})")
            results[f"{collection}_{year}"] = total_count
            
        except Exception as e:
            logger.error(f"  ❌ {year}: {e}")
            results[f"{collection}_{year}"] = None

logger.info("\n" + "=" * 60)
logger.info("SUMMARY")
logger.info("=" * 60)

# Calculate totals by collection
for collection in collections:
    collection_name = collection_names[collection]
    total = sum(v for k, v in results.items() if k.startswith(collection) and v is not None)
    logger.info(f"{collection_name} (2000, 2005, 2010, 2015, 2020, 2023): {total} packages")

# Save results
output_file = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo") / f"api_test_results_{datetime.now():%Y%m%d_%H%M%S}.json"
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)
logger.info(f"\nResults saved to {output_file}")
