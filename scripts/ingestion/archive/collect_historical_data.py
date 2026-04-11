#!/usr/bin/env python3
"""
Historical Data Collection System for Epstein/9-11 Research
Fetches articles from 2001-2026 using Wayback Machine and news archives
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from urllib.parse import quote, urlparse
import os
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cbwinslow/workspace/epstein-data/logs/historical_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('historical_collection')

class WaybackCollector:
    """Collect historical URLs from Wayback Machine."""
    
    CDX_API = "https://web.archive.org/cdx/search/cdx"
    
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.last_request = 0
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _rate_limited_request(self, url: str, params: dict) -> Optional[dict]:
        """Make rate-limited request."""
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        
        try:
            async with self.session.get(url, params=params, timeout=30) as response:
                self.last_request = time.time()
                if response.status == 200:
                    text = await response.text()
                    return {'status': 200, 'text': text}
                else:
                    logger.warning(f"Wayback API returned {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    async def search_by_keyword(
        self,
        keyword: str,
        domain: str,
        start_date: str,  # YYYYMMDD
        end_date: str,    # YYYYMMDD
        limit: int = 100
    ) -> List[Dict]:
        """Search Wayback CDX for URLs matching keyword."""
        
        params = {
            'url': f"{domain}/*",
            'matchType': 'domain',
            'from': start_date,
            'to': end_date,
            'output': 'json',
            'fl': 'timestamp,original,statuscode,digest',
            'filter': f'~url:.*{keyword}.*',
            'limit': limit
        }
        
        result = await self._rate_limited_request(self.CDX_API, params)
        
        if not result:
            return []
        
        urls = []
        lines = result['text'].strip().split('\n')
        
        for line in lines[1:]:  # Skip header
            if not line:
                continue
            parts = line.split(' ')
            if len(parts) >= 3:
                timestamp = parts[0]
                original_url = parts[1]
                status = parts[2] if len(parts) > 2 else '200'
                
                if status == '200':
                    wayback_url = f"https://web.archive.org/web/{timestamp}/{original_url}"
                    urls.append({
                        'original_url': original_url,
                        'wayback_url': wayback_url,
                        'timestamp': timestamp,
                        'domain': domain,
                        'keyword_matched': keyword
                    })
        
        logger.info(f"Found {len(urls)} URLs for keyword '{keyword}' on {domain}")
        return urls
    
    async def search_date_range(
        self,
        domains: List[str],
        keywords: List[str],
        start_year: int,
        end_year: int,
        limit_per_query: int = 50
    ) -> List[Dict]:
        """Search multiple domains and keywords across date range."""
        
        all_urls = []
        
        for year in range(start_year, end_year + 1):
            start_date = f"{year}0101"
            end_date = f"{year}1231"
            
            logger.info(f"Searching year {year}...")
            
            for domain in domains:
                for keyword in keywords:
                    try:
                        urls = await self.search_by_keyword(
                            keyword=keyword,
                            domain=domain,
                            start_date=start_date,
                            end_date=end_date,
                            limit=limit_per_query
                        )
                        all_urls.extend(urls)
                        
                        # Small delay between queries
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"Error searching {domain} for '{keyword}': {e}")
                        continue
        
        return all_urls


class HistoricalCollectionManager:
    """Manages historical data collection with resume capability."""
    
    def __init__(self, state_file: str = '/home/cbwinslow/workspace/epstein-data/.collection_state.json'):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Load collection state from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'completed_batches': [],
            'failed_urls': [],
            'last_run': None,
            'total_collected': 0
        }
    
    def _save_state(self):
        """Save collection state to file."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def mark_batch_complete(self, batch_id: str, count: int):
        """Mark a batch as completed."""
        self.state['completed_batches'].append(batch_id)
        self.state['total_collected'] += count
        self.state['last_run'] = datetime.now().isoformat()
        self._save_state()
    
    def mark_url_failed(self, url: str, error: str):
        """Mark a URL as failed."""
        self.state['failed_urls'].append({
            'url': url,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        self._save_state()
    
    def is_batch_complete(self, batch_id: str) -> bool:
        """Check if batch was already completed."""
        return batch_id in self.state['completed_batches']
    
    def get_progress(self) -> dict:
        """Get current progress."""
        return {
            'completed_batches': len(self.state['completed_batches']),
            'failed_urls': len(self.state['failed_urls']),
            'total_collected': self.state['total_collected'],
            'last_run': self.state['last_run']
        }


async def collect_historical_data(
    domains: List[str],
    keywords: List[str],
    start_year: int,
    end_year: int,
    output_file: str
):
    """Main collection function."""
    
    logger.info(f"Starting historical collection: {start_year}-{end_year}")
    logger.info(f"Domains: {len(domains)}, Keywords: {len(keywords)}")
    
    manager = HistoricalCollectionManager()
    
    async with WaybackCollector(rate_limit=0.5) as collector:
        urls = await collector.search_date_range(
            domains=domains,
            keywords=keywords,
            start_year=start_year,
            end_year=end_year,
            limit_per_query=50
        )
    
    # Save discovered URLs
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(urls, f, indent=2)
    
    logger.info(f"Collection complete. Found {len(urls)} URLs")
    logger.info(f"Saved to: {output_file}")
    
    # Update state
    batch_id = f"{start_year}_{end_year}_{datetime.now().strftime('%Y%m%d')}"
    manager.mark_batch_complete(batch_id, len(urls))
    
    return urls


if __name__ == '__main__':
    import sys
    
    # Configuration
    from media_acquisition.config import TARGET_SOURCES, EPSTEIN_KEYWORDS, SEPT11_KEYWORDS
    
    # Combine all keywords
    all_keywords = list(set(EPSTEIN_KEYWORDS + SEPT11_KEYWORDS))
    
    # Command line args
    if len(sys.argv) > 1:
        start_year = int(sys.argv[1])
        end_year = int(sys.argv[2]) if len(sys.argv) > 2 else start_year
    else:
        start_year = 2001
        end_year = 2026
    
    output = f'/home/cbwinslow/workspace/epstein-data/urls_discovered_{start_year}_{end_year}.json'
    
    # Run collection
    urls = asyncio.run(collect_historical_data(
        domains=TARGET_SOURCES,
        keywords=all_keywords,
        start_year=start_year,
        end_year=end_year,
        output_file=output
    ))
    
    print(f"\n✅ Collection complete!")
    print(f"   Found: {len(urls)} URLs")
    print(f"   Saved: {output}")
