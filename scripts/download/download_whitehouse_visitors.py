#!/usr/bin/env python3
"""
Download White House Visitor Logs
Source: https://www.whitehouse.gov/disclosures/visitor-logs/
"""

import requests
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/whitehouse_visitors")
DATA_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.whitehouse.gov/wp-json/whitehouse/v1/visitor-logs"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)',
    'Accept': 'application/json'
}

def download_visitor_logs(year: int = None):
    """Download White House visitor logs"""
    if year is None:
        year = datetime.now().year
    
    print(f"Fetching White House visitor logs for {year}...")
    
    # API endpoint for visitor logs
    params = {
        'year': year,
        'per_page': 100,
        'page': 1
    }
    
    all_visitors = []
    page = 1
    
    while True:
        params['page'] = page
        
        try:
            response = requests.get(
                BASE_URL,
                headers=HEADERS,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if not data or 'visitors' not in data or not data['visitors']:
                break
            
            visitors = data['visitors']
            all_visitors.extend(visitors)
            
            print(f"Page {page}: Retrieved {len(visitors)} visitors")
            
            if len(visitors) < params['per_page']:
                break
            
            page += 1
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    
    print(f"\nTotal visitors retrieved: {len(all_visitors)}")
    
    # Save to file
    output_file = DATA_DIR / f"whitehouse_visitors_{year}.json"
    with open(output_file, 'w') as f:
        json.dump(all_visitors, f, indent=2)
    
    print(f"✅ Saved to {output_file}")
    return output_file

def download_historical_csv():
    """Download CSV files from whitehouse.gov disclosures page"""
    csv_urls = [
        "https://www.whitehouse.gov/wp-content/uploads/2024/01/WhiteHouse-WAVES-Access-Records-2023.csv",
        "https://www.whitehouse.gov/wp-content/uploads/2023/01/WhiteHouse-WAVES-Access-Records-2022.csv",
    ]
    
    for url in csv_urls:
        filename = url.split('/')[-1]
        output_file = DATA_DIR / filename
        
        if output_file.exists():
            print(f"⚠️  {filename} already exists, skipping")
            continue
        
        try:
            print(f"Downloading {filename}...")
            response = requests.get(url, headers=HEADERS, timeout=60)
            response.raise_for_status()
            
            output_file.write_bytes(response.content)
            print(f"✅ Downloaded {filename} ({len(response.content) / 1024:.1f} KB)")
            
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")

def main():
    """Download White House visitor logs"""
    print("="*60)
    print("WHITE HOUSE VISITOR LOGS DOWNLOADER")
    print("="*60)
    
    # Download current year API data
    download_visitor_logs(2025)
    
    # Download historical CSV files
    print("\nDownloading historical CSV files...")
    download_historical_csv()
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    print(f"\nOutput directory: {DATA_DIR}")
    print("\nNext steps:")
    print("1. Load JSON/CSV into PostgreSQL")
    print("2. Extract visitor names for cross-referencing")
    print("3. Cross-reference with FEC, SEC, ICIJ datasets")

if __name__ == "__main__":
    main()
