#!/usr/bin/env python3
"""Test Congress.gov API for historical congress access"""
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

API_KEY = os.environ.get('CONGRESS_API_KEY')
if not API_KEY:
    logger.error("CONGRESS_API_KEY not set in environment")
    sys.exit(1)

base_url = "https://api.congress.gov/v3"
headers = {'X-API-Key': API_KEY}

# Test different congresses (107th = 2001-2002, 118th = 2023-2024)
test_congresses = [107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118]

logger.info("Testing Congress.gov API for historical data access...")
logger.info("=" * 60)

results = {}

for congress in test_congresses:
    logger.info(f"\nTesting Congress {congress}...")
    
    # Test bills
    try:
        url = f"{base_url}/bill?congress={congress}&limit=1&format=json"
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        bills_count = data.get('pagination', {}).get('count', 0)
        logger.info(f"  ✅ Bills: {bills_count:,} available")
        results[f"congress_{congress}_bills"] = bills_count
    except Exception as e:
        logger.error(f"  ❌ Bills: {e}")
        results[f"congress_{congress}_bills"] = None
    
    # Test members (use current congress endpoint with filter)
    try:
        url = f"{base_url}/member?congress={congress}&limit=1&format=json"
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        members_count = data.get('pagination', {}).get('count', 0)
        logger.info(f"  ✅ Members: {members_count} available")
        results[f"congress_{congress}_members"] = members_count
    except Exception as e:
        logger.error(f"  ❌ Members: {e}")
        results[f"congress_{congress}_members"] = None

logger.info("\n" + "=" * 60)
logger.info("SUMMARY")
logger.info("=" * 60)

# Calculate totals
total_bills = sum(v for k, v in results.items() if 'bills' in k and v is not None)
total_members = sum(v for k, v in results.items() if 'members' in k and v is not None)

logger.info(f"Total Bills (107th-118th): {total_bills:,}")
logger.info(f"Total Members (107th-118th): {total_members:,}")

# Save results
output_file = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress") / f"api_test_results_{datetime.now():%Y%m%d_%H%M%S}.json"
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)
logger.info(f"\nResults saved to {output_file}")
