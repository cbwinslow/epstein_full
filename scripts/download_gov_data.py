#!/usr/bin/env python3
"""
Free Government Data Download Script
Uses govinfo.gov, congress.gov, and data.gov APIs (all free with registration)
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import time

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
DATA_DIR = Path('/mnt/data/epstein-project/raw-files/government')
DATA_DIR.mkdir(parents=True, exist_ok=True)

# API Keys (get free at api.data.gov)
GOVINFO_API_KEY = os.environ.get('GOVINFO_API_KEY', 'DEMO_KEY')
CONGRESS_API_KEY = os.environ.get('CONGRESS_API_KEY', '')
DATAGOV_API_KEY = os.environ.get('DATAGOV_API_KEY', '')

# API Endpoints
GOVINFO_BASE = "https://api.govinfo.gov"
CONGRESS_BASE = "https://api.congress.gov/v3"
DATAGOV_BASE = "https://catalog.data.gov/api/3"


class GovInfoClient:
    """Client for GovInfo.gov API - FREE with api.data.gov key"""
    
    def __init__(self, api_key: str = GOVINFO_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'EpsteinResearch/1.0'
        })
        self.rate_limit_delay = 0.1  # 10 req/sec = 36,000/hour
    
    def get_collections(self) -> List[Dict]:
        """Get list of available collections"""
        url = f"{GOVINFO_BASE}/collections"
        params = {'api_key': self.api_key}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json().get('collections', [])
        except Exception as e:
            logger.error(f"Error getting collections: {e}")
            return []
    
    def search_financial_disclosures(self, member_name: str = None, start_date: str = None) -> List[Dict]:
        """
        Search for Congressional financial disclosure reports
        Collection codes: CPD (Congressional Publications), CREC (Congressional Record)
        """
        url = f"{GOVINFO_BASE}/search"
        
        # Build query for financial disclosures
        query_parts = ['collection:(CPD OR CREC)']
        
        if member_name:
            query_parts.append(f'"{member_name}"')
        
        query_parts.append('("financial disclosure" OR "periodic transaction" OR "stock trade")')
        
        payload = {
            'query': ' and '.join(query_parts),
            'pageSize': 100,
            'offsetMark': '*',
            'sorts': [{'field': 'dateIssued', 'sortOrder': 'DESC'}]
        }
        
        try:
            response = self.session.post(
                url,
                params={'api_key': self.api_key},
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            logger.error(f"Error searching disclosures: {e}")
            return []
    
    def get_collection_updates(self, collection_code: str, start_date: str, end_date: str = None) -> List[Dict]:
        """Get packages added/modified in a collection within date range"""
        url = f"{GOVINFO_BASE}/collections/{collection_code}/{start_date}"
        
        if end_date:
            url = f"{url}/{end_date}"
        
        params = {
            'api_key': self.api_key,
            'offsetMark': '*',
            'pageSize': 1000
        }
        
        packages = []
        
        while True:
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                packages.extend(data.get('packages', []))
                
                # Check for next page
                next_offset = data.get('nextPage', {}).get('offsetMark')
                if not next_offset or next_offset == params['offsetMark']:
                    break
                
                params['offsetMark'] = next_offset
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"Error getting collection updates: {e}")
                break
        
        return packages
    
    def download_package(self, package_id: str, output_dir: Path) -> Optional[Path]:
        """Download a package's content"""
        url = f"{GOVINFO_BASE}/packages/{package_id}/summary"
        params = {'api_key': self.api_key}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            summary = response.json()
            
            # Save summary
            output_file = output_dir / f"{package_id.replace('/', '_')}.json"
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            # Download content if available
            download_links = summary.get('download', [])
            for link in download_links:
                if link.get('mimetype') == 'text/html':
                    # Download HTML content
                    content_url = link.get('txtLink') or link.get('link')
                    if content_url:
                        content_response = self.session.get(content_url, timeout=30)
                        if content_response.status_code == 200:
                            content_file = output_dir / f"{package_id.replace('/', '_')}.txt"
                            content_file.write_text(content_response.text)
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error downloading package {package_id}: {e}")
            return None


class CongressGovClient:
    """Client for Congress.gov API - FREE with api.data.gov key"""
    
    def __init__(self, api_key: str = CONGRESS_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'EpsteinResearch/1.0'
        })
        self.rate_limit_delay = 0.5  # Congress.gov has stricter limits
    
    def get_members(self, congress: int = 118) -> List[Dict]:
        """Get list of members for a Congress"""
        url = f"{CONGRESS_BASE}/member/congress/{congress}"
        params = {'api_key': self.api_key, 'limit': 250}
        
        members = []
        offset = 0
        
        while True:
            params['offset'] = offset
            
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                batch = data.get('members', [])
                if not batch:
                    break
                
                members.extend(batch)
                
                # Check if there are more results
                if len(batch) < params['limit']:
                    break
                
                offset += params['limit']
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"Error getting members: {e}")
                break
        
        return members
    
    def get_member_details(self, bioguide_id: str) -> Optional[Dict]:
        """Get detailed information about a member"""
        url = f"{CONGRESS_BASE}/member/{bioguide_id}"
        params = {'api_key': self.api_key}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting member details: {e}")
            return None
    
    def search_bills(self, query: str, congress: int = 118) -> List[Dict]:
        """Search for bills"""
        url = f"{CONGRESS_BASE}/bill"
        params = {
            'api_key': self.api_key,
            'congress': congress,
            'q': query,
            'limit': 100
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json().get('bills', [])
        except Exception as e:
            logger.error(f"Error searching bills: {e}")
            return []


class DataGovClient:
    """Client for Data.gov API - FREE"""
    
    def __init__(self, api_key: str = DATAGOV_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'EpsteinResearch/1.0'
        })
    
    def search_datasets(self, query: str, rows: int = 100) -> List[Dict]:
        """Search for datasets on data.gov"""
        url = f"{DATAGOV_BASE}/action/package_search"
        params = {
            'q': query,
            'rows': rows
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('result', {}).get('results', [])
        except Exception as e:
            logger.error(f"Error searching data.gov: {e}")
            return []
    
    def get_relevant_datasets(self) -> Dict[str, List[Dict]]:
        """Get datasets relevant to Epstein research"""
        searches = {
            'campaign_finance': 'campaign finance contributions',
            'lobbying': 'lobbying disclosures',
            'elections': 'fec elections',
            'contracts': 'federal contracts spending',
            'nonprofits': 'nonprofit 990 forms',
            'securities': 'sec enforcement actions'
        }
        
        results = {}
        for name, query in searches.items():
            logger.info(f"Searching data.gov for: {query}")
            results[name] = self.search_datasets(query, rows=20)
            time.sleep(0.5)  # Be polite
        
        return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download free government data')
    parser.add_argument('--govinfo-key', help='GovInfo API key (get free at api.data.gov)')
    parser.add_argument('--congress-key', help='Congress.gov API key')
    parser.add_argument('--datagov-key', help='Data.gov API key')
    parser.add_argument('--search-disclosures', action='store_true', help='Search financial disclosures')
    parser.add_argument('--get-members', action='store_true', help='Get Congress members')
    parser.add_argument('--search-datasets', action='store_true', help='Search data.gov datasets')
    parser.add_argument('--collections', action='store_true', help='List GovInfo collections')
    
    args = parser.parse_args()
    
    # Use provided keys or environment variables
    govinfo_key = args.govinfo_key or GOVINFO_API_KEY
    congress_key = args.congress_key or CONGRESS_API_KEY
    datagov_key = args.datagov_key or DATAGOV_API_KEY
    
    if args.collections:
        logger.info("Listing GovInfo collections...")
        client = GovInfoClient(govinfo_key)
        collections = client.get_collections()
        
        output_file = DATA_DIR / 'govinfo_collections.json'
        with open(output_file, 'w') as f:
            json.dump(collections, f, indent=2)
        
        logger.info(f"Saved {len(collections)} collections to {output_file}")
        
        # Print relevant collections
        for c in collections:
            code = c.get('collectionCode', '')
            name = c.get('collectionName', '')
            if any(x in code.lower() or x in name.lower() for x in ['congress', 'house', 'senate', 'court']):
                print(f"  - {code}: {name} ({c.get('packageCount', 0)} packages)")
    
    if args.search_disclosures:
        if govinfo_key == 'DEMO_KEY':
            logger.warning("Using DEMO_KEY - get your free key at https://api.data.gov/signup/")
        
        logger.info("Searching for financial disclosure documents...")
        client = GovInfoClient(govinfo_key)
        results = client.search_financial_disclosures()
        
        output_file = DATA_DIR / f'financial_disclosures_{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Found {len(results)} disclosure documents, saved to {output_file}")
    
    if args.get_members:
        if not congress_key:
            logger.error("Congress.gov API key required. Get free at https://api.congress.gov/")
            return
        
        logger.info("Getting Congress members...")
        client = CongressGovClient(congress_key)
        members = client.get_members(congress=118)
        
        output_file = DATA_DIR / f'congress_members_118_{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(members, f, indent=2)
        
        logger.info(f"Saved {len(members)} members to {output_file}")
    
    if args.search_datasets:
        logger.info("Searching data.gov for relevant datasets...")
        client = DataGovClient(datagov_key)
        results = client.get_relevant_datasets()
        
        output_file = DATA_DIR / f'datagov_datasets_{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        total = sum(len(v) for v in results.values())
        logger.info(f"Found {total} datasets across {len(results)} categories")


if __name__ == '__main__':
    main()
