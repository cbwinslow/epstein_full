#!/usr/bin/env python3
"""
House & Senate Financial Disclosure Scraper
Direct scraping of disclosures-clerk.house.gov and disclosure.senate.gov
NO API KEY REQUIRED - Free public access
"""

import requests
from bs4 import BeautifulSoup
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
DATA_DIR = Path('/home/cbwinslow/workspace/epstein-data/raw-files/politicians')
DATA_DIR.mkdir(parents=True, exist_ok=True)

# URLs
HOUSE_SEARCH_URL = "https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure/ViewSearch"
SENATE_SEARCH_URL = "https://www.disclosure.senate.gov/"


class HouseDisclosureScraper:
    """Scrape House financial disclosures from disclosures-clerk.house.gov"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.delay = 1.0  # Be polite
    
    def search_members(self, last_name: str = None, state: str = None, year: int = None) -> List[Dict]:
        """
        Search for member financial disclosures
        Note: House site uses ASP.NET forms - requires form submission
        """
        try:
            # Get the search page first to extract form data
            response = self.session.get(HOUSE_SEARCH_URL, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract form data
            viewstate = soup.find('input', {'name': '__VIEWSTATE'})
            eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})
            
            if not viewstate or not eventvalidation:
                logger.error("Could not extract form data from House search page")
                return []
            
            # Build form data
            form_data = {
                '__VIEWSTATE': viewstate.get('value', ''),
                '__EVENTVALIDATION': eventvalidation.get('value', ''),
                'ctl00$ContentPlaceHolder1$txtLastName': last_name or '',
                'ctl00$ContentPlaceHolder1$ddlState': state or '',
                'ctl00$ContentPlaceHolder1$ddlYear': str(year) if year else '',
                'ctl00$ContentPlaceHolder1$btnSearch': 'Search'
            }
            
            # Submit search
            response = self.session.post(HOUSE_SEARCH_URL, data=form_data, timeout=30)
            response.raise_for_status()
            
            # Parse results
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Look for results table
            results_table = soup.find('table', {'id': 'ContentPlaceHolder1_gvResults'})
            if results_table:
                rows = results_table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        result = {
                            'name': cells[0].get_text(strip=True),
                            'state': cells[1].get_text(strip=True),
                            'office': cells[2].get_text(strip=True),
                            'year': cells[3].get_text(strip=True),
                            'link': None
                        }
                        
                        # Extract PDF link
                        link_tag = cells[0].find('a')
                        if link_tag and link_tag.get('href'):
                            result['link'] = f"https://disclosures-clerk.house.gov{link_tag['href']}"
                        
                        results.append(result)
            
            logger.info(f"Found {len(results)} House disclosure records")
            return results
            
        except Exception as e:
            logger.error(f"Error searching House disclosures: {e}")
            return []
    
    def download_disclosure(self, url: str, output_dir: Path) -> Optional[Path]:
        """Download a disclosure PDF"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Extract filename from URL or Content-Disposition
            filename = url.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename = f"house_disclosure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            output_file = output_dir / filename
            output_file.write_bytes(response.content)
            
            logger.info(f"Downloaded: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error downloading disclosure: {e}")
            return None


class SenateDisclosureScraper:
    """Scrape Senate financial disclosures from disclosure.senate.gov"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.delay = 1.0
    
    def get_public_disclosures(self) -> List[Dict]:
        """
        Get list of publicly available Senate disclosures
        """
        try:
            response = self.session.get(SENATE_SEARCH_URL, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Senate site structure varies - look for disclosure links
            results = []
            
            # Look for links to disclosure files
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                
                # Check if it's a disclosure-related link
                if any(x in href.lower() for x in ['disclosure', 'financial', 'report']) and \
                   any(x in href.lower() for x in ['.pdf', '.txt']):
                    results.append({
                        'text': text,
                        'url': href if href.startswith('http') else f"https://www.disclosure.senate.gov{href}",
                        'source': 'senate'
                    })
            
            logger.info(f"Found {len(results)} Senate disclosure links")
            return results
            
        except Exception as e:
            logger.error(f"Error getting Senate disclosures: {e}")
            return []
    
    def search_by_name(self, name: str) -> List[Dict]:
        """
        Search Senate disclosures by member name
        Note: Senate site may require form submission
        """
        # Senate search URL
        search_url = f"https://www.disclosure.senate.gov/search?q={name}"
        
        try:
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            
            # Parse results
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Extract disclosure entries
            # Senate site structure varies
            for item in soup.find_all(['div', 'tr'], class_=lambda x: x and 'result' in x.lower()):
                result = {
                    'name': name,
                    'text': item.get_text(strip=True),
                    'link': None
                }
                
                link = item.find('a', href=True)
                if link:
                    href = link['href']
                    result['link'] = href if href.startswith('http') else f"https://www.disclosure.senate.gov{href}"
                
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching Senate disclosures: {e}")
            return []


class PeriodicTransactionScraper:
    """
    Scrape periodic transaction reports (stock trades)
    These are filed within 45 days of trades > $1,000
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_house_transactions(self, member_name: str = None) -> List[Dict]:
        """
        Get House periodic transaction reports
        Available at: https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure/ViewMemberSearch
        """
        url = "https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure/ViewMemberSearch"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for transaction reports
            transactions = []
            
            # Parse the members list
            select = soup.find('select', {'id': 'ContentPlaceHolder1_ddlMembers'})
            if select:
                for option in select.find_all('option'):
                    if option.get('value'):
                        member_info = {
                            'name': option.get_text(strip=True),
                            'value': option['value']
                        }
                        transactions.append(member_info)
            
            return transactions
            
        except Exception as e:
            logger.error(f"Error getting House transactions: {e}")
            return []
    
    def get_senate_transactions(self) -> List[Dict]:
        """
        Get Senate periodic transaction reports
        Available at: https://www.disclosure.senate.gov/ (via search)
        """
        # Senate PTRs are often in separate database
        url = "https://www.disclosure.senate.gov/"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Look for PTR links
            soup = BeautifulSoup(response.text, 'html.parser')
            ptrs = []
            
            for link in soup.find_all('a', href=True):
                text = link.get_text(strip=True).lower()
                if 'periodic' in text or 'transaction' in text or 'ptr' in text:
                    ptrs.append({
                        'text': link.get_text(strip=True),
                        'url': link['href']
                    })
            
            return ptrs
            
        except Exception as e:
            logger.error(f"Error getting Senate transactions: {e}")
            return []


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape House/Senate financial disclosures')
    parser.add_argument('--house', action='store_true', help='Scrape House disclosures')
    parser.add_argument('--senate', action='store_true', help='Scrape Senate disclosures')
    parser.add_argument('--transactions', action='store_true', help='Get periodic transaction reports')
    parser.add_argument('--name', help='Search by member name')
    parser.add_argument('--state', help='Filter by state')
    parser.add_argument('--year', type=int, help='Filter by year')
    
    args = parser.parse_args()
    
    if args.house or (not args.house and not args.senate and not args.transactions):
        logger.info("Scraping House disclosures...")
        scraper = HouseDisclosureScraper()
        results = scraper.search_members(
            last_name=args.name,
            state=args.state,
            year=args.year
        )
        
        output_file = DATA_DIR / f'house_disclosures_{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved {len(results)} House disclosures to {output_file}")
    
    if args.senate:
        logger.info("Scraping Senate disclosures...")
        scraper = SenateDisclosureScraper()
        results = scraper.get_public_disclosures()
        
        if args.name:
            name_results = scraper.search_by_name(args.name)
            results.extend(name_results)
        
        output_file = DATA_DIR / f'senate_disclosures_{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved {len(results)} Senate disclosures to {output_file}")
    
    if args.transactions:
        logger.info("Getting periodic transaction reports...")
        scraper = PeriodicTransactionScraper()
        
        house_trans = scraper.get_house_transactions(args.name)
        senate_trans = scraper.get_senate_transactions()
        
        results = {
            'house': house_trans,
            'senate': senate_trans
        }
        
        output_file = DATA_DIR / f'periodic_transactions_{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved {len(house_trans)} House and {len(senate_trans)} Senate PTRs")
    
    logger.info("Scraping complete!")


if __name__ == '__main__':
    main()
