#!/usr/bin/env python3
"""
Historical Data Collection - Direct Archive Access
Fetches articles from Wayback using direct URL construction
"""

import asyncio
import aiohttp
import json
import logging
import os
import time
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import quote

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cbwinslow/workspace/epstein-data/logs/historical_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('historical_collection')

# Target URLs for 9/11 and Epstein content
TARGET_URLS = {
    '9/11 Coverage': [
        # Major news sites - 9/11 anniversary and investigation coverage
        ('nytimes.com', ['september-11', '9-11', 'world-trade-center', 'terrorist-attack']),
        ('washingtonpost.com', ['september-11', '9-11', 'terrorism', 'al-qaeda']),
        ('cnn.com', ['september-11', '9-11', 'ground-zero', 'terror-attack']),
        ('bbc.com', ['september-11', '9-11-attacks', 'twin-towers']),
    ],
    'Epstein Coverage': [
        # Major outlets with significant Epstein coverage
        ('nytimes.com', ['jeffrey-epstein', 'ghislaine-maxwell', 'epstein-victims']),
        ('miamiherald.com', ['jeffrey-epstein', 'perversion-of-justice', 'epstein-sex-trafficking']),
        ('washingtonpost.com', ['jeffrey-epstein', 'epstein-palm-beach', 'epstein-federal']),
        ('theguardian.com', ['jeffrey-epstein', 'ghislaine-maxwell', 'epstein-island']),
        ('vanityfair.com', ['jeffrey-epstein', 'epstein-network']),
        ('politico.com', ['jeffrey-epstein', 'epstein-politicians']),
    ]
}

# Date ranges by period
DATE_RANGES = {
    '9/11_immediate': ('20010911', '20051231'),
    '9/11_investigation': ('20060101', '20101231'),
    'epstein_early': ('20050101', '20081231'),
    'epstein_palm_beach': ('20050101', '20091231'),
    'epstein_federal': ('20060101', '20081231'),
    'epstein_recent': ('20190101', '20241231'),
}

class DirectWaybackCollector:
    """Collect URLs using direct Wayback archive access."""
    
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.last_request = 0
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _rate_limited_fetch(self, url: str) -> Optional[Dict]:
        """Fetch URL with rate limiting."""
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        
        try:
            async with self.session.get(url, timeout=30, ssl=False) as response:
                self.last_request = time.time()
                
                if response.status == 200:
                    text = await response.text()
                    return {
                        'status': 200,
                        'url': str(response.url),
                        'text': text[:50000],  # First 50KB
                        'content_type': response.headers.get('Content-Type', '')
                    }
                else:
                    return {'status': response.status, 'url': str(response.url)}
                    
        except Exception as e:
            logger.warning(f"Fetch failed for {url[:60]}: {e}")
            return None
    
    def construct_wayback_url(self, original_url: str, timestamp: str) -> str:
        """Construct Wayback Machine URL."""
        return f"https://web.archive.org/web/{timestamp}/{original_url}"
    
    async def get_available_snapshots(
        self,
        original_url: str,
        from_date: str,
        to_date: str
    ) -> List[str]:
        """Get list of available snapshots from CDX API."""
        
        # Use CDX API with collapse to get one snapshot per month
        cdx_url = (
            f"https://web.archive.org/cdx/search/cdx"
            f"?url={quote(original_url)}"
            f"&from={from_date}&to={to_date}"
            f"&output=json"
            f"&collapse=timestamp:6"  # One per month
            f"&fl=timestamp"
        )
        
        try:
            async with self.session.get(cdx_url, timeout=30) as response:
                if response.status != 200:
                    return []
                
                text = await response.text()
                lines = text.strip().split('\n')
                
                timestamps = []
                for line in lines[1:]:  # Skip header
                    if line:
                        parts = line.split(' ')
                        if parts:
                            timestamps.append(parts[0])
                
                return timestamps
                
        except Exception as e:
            logger.error(f"CDX query failed: {e}")
            return []
    
    async def collect_from_source(
        self,
        domain: str,
        keywords: List[str],
        date_range: Tuple[str, str],
        max_per_keyword: int = 10
    ) -> List[Dict]:
        """Collect articles from a source for given keywords."""
        
        from_date, to_date = date_range
        results = []
        
        for keyword in keywords:
            # Construct search URL pattern
            search_url = f"https://{domain}/search?q={keyword.replace('-', '+')}"
            
            # Get snapshots
            timestamps = await self.get_available_snapshots(
                search_url, from_date, to_date
            )
            
            logger.info(f"{domain}/{keyword}: {len(timestamps)} snapshots")
            
            for ts in timestamps[:max_per_keyword]:
                wayback_url = self.construct_wayback_url(search_url, ts)
                
                results.append({
                    'domain': domain,
                    'keyword': keyword,
                    'original_url': search_url,
                    'wayback_url': wayback_url,
                    'timestamp': ts,
                    'year': ts[:4]
                })
            
            await asyncio.sleep(0.5)  # Rate limiting
        
        return results


async def run_historical_collection(
    category: str,
    output_file: str,
    max_per_source: int = 50
):
    """Run collection for a category."""
    
    logger.info(f"Starting collection: {category}")
    
    if category not in TARGET_URLS:
        logger.error(f"Unknown category: {category}")
        return []
    
    sources = TARGET_URLS[category]
    all_results = []
    
    async with DirectWaybackCollector(rate_limit=1.0) as collector:
        for domain, keywords in sources:
            logger.info(f"Processing {domain}...")
            
            # Determine date range based on category
            if '9/11' in category:
                date_range = DATE_RANGES['9/11_immediate']
            else:
                # Mix of ranges for Epstein
                date_range = DATE_RANGES['epstein_recent']
            
            results = await collector.collect_from_source(
                domain=domain,
                keywords=keywords,
                date_range=date_range,
                max_per_keyword=10
            )
            
            all_results.extend(results)
            logger.info(f"  Found {len(results)} URLs from {domain}")
    
    # Save results
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    logger.info(f"Saved {len(all_results)} URLs to {output_file}")
    return all_results


if __name__ == '__main__':
    import sys
    
    category = sys.argv[1] if len(sys.argv) > 1 else 'Epstein Coverage'
    output = f'/home/cbwinslow/workspace/epstein-data/urls/{category.replace("/", "_").replace(" ", "_")}.json'
    
    results = asyncio.run(run_historical_collection(category, output))
    
    print(f"\n✅ Collection complete!")
    print(f"   Category: {category}")
    print(f"   URLs found: {len(results)}")
    print(f"   Saved to: {output}")
