#!/usr/bin/env python3
"""Download USA Spending data via API"""
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/usa_spending")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# USA Spending API - search for recent awards
url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
headers = {'Content-Type': 'application/json'}

# Search for recent awards (last 90 days)
payload = {
    "filters": {
        "time_period": [{"start_date": "2024-01-01", "end_date": "2024-12-31"}],
        "award_type_codes": ["A", "B", "C", "D"]  # Contracts, Grants, Loans
    },
    "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency"],
    "sort": "Award Amount",
    "order": "desc",
    "limit": 100
}

logger.info("Fetching USA Spending data...")

try:
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    
    output_file = BASE_DIR / f"usa_spending_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    results_count = len(data.get('results', []))
    logger.info(f"✅ Downloaded {results_count} awards to {output_file}")
    
except Exception as e:
    logger.error(f"❌ USA Spending download failed: {e}")

logger.info("USA Spending download complete")
