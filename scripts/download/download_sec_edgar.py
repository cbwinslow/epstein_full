#!/usr/bin/env python3
"""
Download SEC EDGAR filings for insider trading analysis
Focus: Form 4 (insider transactions), Form 3 (initial ownership), Form 13F (institutional)
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import requests

DATA_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/sec_edgar")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SEC EDGAR requires proper User-Agent
HEADERS = {
    'User-Agent': 'Research Bot contact@epsteinresearch.org',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.sec.gov'
}

class SECEDGARDownloader:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.base_url = "https://www.sec.gov/Archives/edgar"
        self.daily_index_url = f"{self.base_url}/daily-index"
        
    def get_current_filings(self, form_type: str = "4", days_back: int = 30) -> List[Dict]:
        """Get recent filings of a specific form type"""
        filings = []
        
        for i in range(days_back):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y%m%d")
            
            # EDGAR master index for the date
            index_url = f"{self.daily_index_url}/master.{date_str}.idx"
            
            try:
                time.sleep(0.1)  # Rate limiting - 10 requests/sec max
                response = requests.get(index_url, headers=HEADERS, timeout=30)
                
                if response.status_code == 200:
                    # Parse index file
                    for line in response.text.split('\n'):
                        if f'Form {form_type}' in line:
                            parts = line.split('|')
                            if len(parts) >= 5:
                                filings.append({
                                    'cik': parts[0].strip(),
                                    'company_name': parts[1].strip(),
                                    'form_type': parts[2].strip(),
                                    'date': parts[3].strip(),
                                    'filename': parts[4].strip()
                                })
            except Exception as e:
                print(f"Error fetching {date_str}: {e}")
                continue
        
        return filings
    
    def download_filing(self, filename: str, output_dir: Path) -> bool:
        """Download a specific filing"""
        url = f"{self.base_url}/{filename}"
        output_file = output_dir / filename.replace('/', '_')
        
        if output_file.exists():
            return True
        
        try:
            time.sleep(0.1)  # Rate limiting
            response = requests.get(url, headers=HEADERS, timeout=30)
            
            if response.status_code == 200:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(response.text)
                return True
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
        
        return False
    
    def download_form4_batch(self, days: int = 7, max_filings: int = 1000):
        """Download batch of recent Form 4 filings"""
        print(f"Fetching Form 4 filings for past {days} days...")
        
        filings = self.get_current_filings("4", days)
        print(f"Found {len(filings)} Form 4 filings")
        
        # Limit to max_filings
        filings = filings[:max_filings]
        
        output_dir = self.data_dir / "form4" / datetime.now().strftime("%Y%m%d")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save index
        index_file = output_dir / "filings_index.json"
        with open(index_file, 'w') as f:
            json.dump(filings, f, indent=2)
        
        # Download filings
        downloaded = 0
        for i, filing in enumerate(filings):
            if self.download_filing(filing['filename'], output_dir):
                downloaded += 1
            
            if (i + 1) % 100 == 0:
                print(f"Downloaded {i+1}/{len(filings)}...")
        
        print(f"✅ Downloaded {downloaded} Form 4 filings to {output_dir}")
        return output_dir
    
    def get_company_cik(self, ticker: str) -> str:
        """Get CIK for a ticker symbol"""
        try:
            url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=4&dateb=&owner=only&count=40&output=xml"
            requests.get(url, headers=HEADERS, timeout=30)
            # Parse response for CIK
            # This is simplified - actual implementation would parse XML
            return ""
        except Exception:
            return ""

def main():
    """Download recent SEC EDGAR Form 4 filings"""
    downloader = SECEDGARDownloader()
    
    # Download last 7 days of Form 4 (insider trading)
    output_dir = downloader.download_form4_batch(days=7, max_filings=500)
    
    print(f"\nOutput directory: {output_dir}")
    print("Next steps:")
    print("1. Parse XML filings to extract transaction data")
    print("2. Load into PostgreSQL table: sec_insider_transactions")
    print("3. Cross-reference names with other datasets")

if __name__ == "__main__":
    main()
