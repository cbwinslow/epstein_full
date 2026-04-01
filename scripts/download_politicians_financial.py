#!/usr/bin/env python3
"""
Download politicians' financial disclosure data from multiple sources:
1. House Financial Disclosures (clerk.house.gov)
2. Senate Financial Disclosures (senate.gov)
3. Quiver Quant API (Congressional trading data)
4. GovInfo.gov (Financial Disclosure Reports)
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import logging
import time
from typing import List, Dict, Optional

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
DATA_DIR = Path('/mnt/data/epstein-project/raw-files/politicians')
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Data sources
HOUSE_DISCLOSURE_URL = "https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure"
SENATE_DISCLOSURE_URL = "https://www.disclosure.senate.gov/"
QUIVER_API_URL = "https://api.quiverquant.com/beta"


class PoliticiansFinancialData:
    """Download and manage politicians' financial disclosure data"""
    
    def __init__(self, quiver_api_key: Optional[str] = None):
        self.quiver_api_key = quiver_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_house_disclosures(self, year: int) -> List[Path]:
        """
        Download House financial disclosure reports
        Note: House requires manual search or bulk request
        API endpoint: https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure
        """
        logger.info(f"Downloading House disclosures for {year}")
        
        # House uses a search-based system
        # We'll create a manifest of available reports
        base_url = f"https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure"
        
        try:
            response = self.session.get(base_url, timeout=30)
            if response.status_code == 200:
                # Save the search page
                output_file = DATA_DIR / f"house_disclosures_{year}.html"
                output_file.write_text(response.text)
                logger.info(f"Saved House disclosures page: {output_file}")
                
                # Extract report links (would need HTML parsing)
                # House reports are typically PDFs linked from search results
                
                return [output_file]
        except Exception as e:
            logger.error(f"Error downloading House disclosures: {e}")
        
        return []
    
    def download_senate_disclosures(self, year: int) -> List[Path]:
        """
        Download Senate financial disclosure reports
        Senate has a searchable database at disclosure.senate.gov
        """
        logger.info(f"Downloading Senate disclosures for {year}")
        
        # Senate search endpoint
        search_url = f"{SENATE_DISCLOSURE_URL}/search"
        
        try:
            response = self.session.get(search_url, timeout=30)
            if response.status_code == 200:
                output_file = DATA_DIR / f"senate_disclosures_{year}.html"
                output_file.write_text(response.text)
                logger.info(f"Saved Senate disclosures page: {output_file}")
                return [output_file]
        except Exception as e:
            logger.error(f"Error downloading Senate disclosures: {e}")
        
        return []
    
    def download_quiver_congress_trading(self, ticker: Optional[str] = None) -> Path:
        """
        Download congressional trading data from Quiver Quant API
        Requires API key for full access
        Free tier available with limited requests
        """
        logger.info("Downloading Quiver Quant congressional trading data")
        
        if not self.quiver_api_key:
            logger.warning("No Quiver API key provided. Using free tier (limited data)")
        
        headers = {}
        if self.quiver_api_key:
            headers['Authorization'] = f'Bearer {self.quiver_api_key}'
        
        # Endpoints
        endpoints = {
            'congress_trading': f'{QUIVER_API_URL}/live/congresstrading',
            'senate_trading': f'{QUIVER_API_URL}/live/senatetrading',
            'house_trading': f'{QUIVER_API_URL}/live/housetrading',
        }
        
        downloaded_files = []
        
        for name, url in endpoints.items():
            try:
                logger.info(f"Fetching {name} from {url}")
                
                params = {}
                if ticker:
                    params['ticker'] = ticker
                
                response = self.session.get(url, headers=headers, params=params, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Save JSON
                    output_file = DATA_DIR / f'quiver_{name}_{datetime.now().strftime("%Y%m%d")}.json'
                    with open(output_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    logger.info(f"Saved {len(data) if isinstance(data, list) else 'N/A'} records to {output_file}")
                    downloaded_files.append(output_file)
                    
                elif response.status_code == 429:
                    logger.warning(f"Rate limited on {name}. Sleeping...")
                    time.sleep(60)
                else:
                    logger.error(f"Failed to fetch {name}: {response.status_code}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching {name}: {e}")
        
        return downloaded_files
    
    def download_propublica_financial(self, api_key: str) -> Path:
        """
        Download financial data from ProPublica Congress API
        Includes financial disclosures and personal finance data
        """
        logger.info("Downloading ProPublica financial data")
        
        # ProPublica Congress API
        base_url = "https://api.propublica.org/congress/v1"
        
        headers = {
            'X-API-Key': api_key
        }
        
        # Get list of members
        try:
            # 118th Congress (2023-2025)
            response = self.session.get(
                f"{base_url}/118/senate/members.json",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                output_file = DATA_DIR / f'propublica_senate_118_{datetime.now().strftime("%Y%m%d")}.json'
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                logger.info(f"Saved ProPublica Senate data: {output_file}")
                return output_file
                
        except Exception as e:
            logger.error(f"Error downloading ProPublica data: {e}")
        
        return None
    
    def create_database_tables(self, db_config: Dict):
        """Create PostgreSQL tables for politicians' financial data"""
        import psycopg2
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Congress trading table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS congress_trading (
                id SERIAL PRIMARY KEY,
                politician_name VARCHAR(200),
                politician_party VARCHAR(10),
                politician_state VARCHAR(2),
                politician_district VARCHAR(10),
                transaction_date DATE,
                ticker VARCHAR(20),
                asset_name TEXT,
                asset_type VARCHAR(50),
                transaction_type VARCHAR(20),  -- Purchase, Sale, Exchange
                amount_low NUMERIC(14,2),
                amount_high NUMERIC(14,2),
                amount_text VARCHAR(50),
                description TEXT,
                data_source VARCHAR(50),  -- Quiver, House, Senate
                filing_date DATE,
                disclosure_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_congress_trading_politician 
            ON congress_trading(politician_name);
            CREATE INDEX IF NOT EXISTS idx_congress_trading_ticker 
            ON congress_trading(ticker);
            CREATE INDEX IF NOT EXISTS idx_congress_trading_date 
            ON congress_trading(transaction_date);
        """)
        
        # Financial disclosures summary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS politician_financial_summary (
                id SERIAL PRIMARY KEY,
                politician_name VARCHAR(200),
                year INTEGER,
                office VARCHAR(50),  -- House, Senate
                state VARCHAR(2),
                district VARCHAR(10),
                total_assets_low NUMERIC(16,2),
                total_assets_high NUMERIC(16,2),
                total_liabilities_low NUMERIC(16,2),
                total_liabilities_high NUMERIC(16,2),
                net_worth_low NUMERIC(16,2),
                net_worth_high NUMERIC(16,2),
                disclosure_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_financial_summary_politician 
            ON politician_financial_summary(politician_name);
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("Politicians financial tables created")


def main():
    """Main entry point"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Download politicians financial data')
    parser.add_argument('--quiver-key', help='Quiver Quant API key')
    parser.add_argument('--propublica-key', help='ProPublica API key')
    parser.add_argument('--year', type=int, default=datetime.now().year, help='Year for disclosures')
    parser.add_argument('--setup-db', action='store_true', help='Create database tables')
    
    args = parser.parse_args()
    
    # Get API keys from environment if not provided
    quiver_key = args.quiver_key or os.environ.get('QUIVER_API_KEY')
    propublica_key = args.propublica_key or os.environ.get('PROPUBLICA_API_KEY')
    
    # Database config
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'epstein',
        'user': 'cbwinslow',
        'password': '123qweasd'
    }
    
    downloader = PoliticiansFinancialData(quiver_api_key=quiver_key)
    
    if args.setup_db:
        downloader.create_database_tables(db_config)
        return
    
    # Download all sources
    logger.info("Starting politicians' financial data download...")
    
    # 1. House disclosures
    house_files = downloader.download_house_disclosures(args.year)
    logger.info(f"Downloaded {len(house_files)} House files")
    
    # 2. Senate disclosures
    senate_files = downloader.download_senate_disclosures(args.year)
    logger.info(f"Downloaded {len(senate_files)} Senate files")
    
    # 3. Quiver Quant trading data (if API key available)
    if quiver_key:
        quiver_files = downloader.download_quiver_congress_trading()
        logger.info(f"Downloaded {len(quiver_files)} Quiver files")
    else:
        logger.info("Skipping Quiver data (no API key)")
    
    # 4. ProPublica data
    if propublica_key:
        propublica_file = downloader.download_propublica_financial(propublica_key)
        if propublica_file:
            logger.info(f"Downloaded ProPublica data: {propublica_file}")
    else:
        logger.info("Skipping ProPublica data (no API key)")
    
    logger.info(f"\nAll downloads complete! Data saved to: {DATA_DIR}")


if __name__ == '__main__':
    main()
