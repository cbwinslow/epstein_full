#!/usr/bin/env python3
"""
Alternative Historical Data Collection
Uses news APIs, RSS feeds, and sitemaps instead of Wayback
"""

import asyncio
import aiohttp
import feedparser
import json
import logging
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cbwinslow/workspace/epstein-data/logs/news_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('news_collection')


class NewsAPICollector:
    """Collect news from various sources using RSS and sitemaps."""
    
    # RSS feeds for major news sources
    RSS_FEEDS = {
        'reuters': 'https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best',
        'guardian': 'https://www.theguardian.com/us-news/rss',
        'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
        'cnn': 'http://rss.cnn.com/rss/edition.rss',
        'nyt': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'wapo': 'http://feeds.washingtonpost.com/rss/politics',
    }
    
    # Sitemap patterns
    SITEMAP_PATTERNS = {
        'nytimes': 'https://www.nytimes.com/sitemap/{year}/{month:02d}/01/sitemap.xml',
        'guardian': 'https://www.theguardian.com/sitemaps/news/{year}/{month:02d}.xml',
        'reuters': 'https://www.reuters.com/sitemap/{year}-{month:02d}.xml',
    }
    
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def fetch_rss(self, feed_name: str, feed_url: str, keywords: List[str]) -> List[Dict]:
        """Fetch and parse RSS feed."""
        try:
            async with self.session.get(feed_url, timeout=30, ssl=False) as response:
                if response.status != 200:
                    return []
                
                content = await response.text()
                
                # Parse RSS
                feed = feedparser.parse(content)
                
                articles = []
                for entry in feed.entries:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    
                    # Check if article matches keywords
                    content_text = f"{title} {summary}".lower()
                    if any(kw.lower() in content_text for kw in keywords):
                        articles.append({
                            'source': feed_name,
                            'title': title,
                            'url': entry.get('link', ''),
                            'published': entry.get('published', ''),
                            'summary': summary[:500],
                            'keywords_matched': [kw for kw in keywords if kw.lower() in content_text]
                        })
                
                logger.info(f"{feed_name}: Found {len(articles)} matching articles")
                return articles
                
        except Exception as e:
            logger.error(f"RSS fetch failed for {feed_name}: {e}")
            return []
    
    async def fetch_sitemap(self, source: str, year: int, month: int, keywords: List[str]) -> List[Dict]:
        """Fetch and parse sitemap."""
        if source not in self.SITEMAP_PATTERNS:
            return []
        
        url = self.SITEMAP_PATTERNS[source].format(year=year, month=month)
        
        try:
            async with self.session.get(url, timeout=30, ssl=False) as response:
                if response.status != 200:
                    return []
                
                content = await response.text()
                
                # Parse sitemap XML
                try:
                    root = ET.fromstring(content)
                except:
                    return []
                
                # Namespace handling
                ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                
                urls = []
                for url_elem in root.findall('ns:url', ns):
                    loc = url_elem.find('ns:loc', ns)
                    if loc is None:
                        continue
                    
                    article_url = loc.text
                    
                    # Check for news:title if available
                    news_title = url_elem.find('.//{http://www.google.com/schemas/sitemap-news/0.9}title')
                    title = news_title.text if news_title is not None else ''
                    
                    # Check keywords
                    if any(kw.lower() in article_url.lower() or kw.lower() in title.lower() 
                           for kw in keywords):
                        urls.append({
                            'source': source,
                            'url': article_url,
                            'title': title,
                            'year': year,
                            'month': month,
                            'keywords_matched': [kw for kw in keywords 
                                               if kw.lower() in article_url.lower() 
                                               or kw.lower() in title.lower()]
                        })
                
                logger.info(f"{source} sitemap {year}-{month:02d}: {len(urls)} matches")
                return urls
                
        except Exception as e:
            logger.warning(f"Sitemap fetch failed for {source}: {e}")
            return []
    
    async def collect_by_keywords(
        self,
        keywords: List[str],
        year_start: int,
        year_end: int
    ) -> List[Dict]:
        """Collect articles matching keywords across sources."""
        
        all_articles = []
        
        # Collect from RSS feeds (recent content)
        logger.info("Collecting from RSS feeds...")
        for name, url in self.RSS_FEEDS.items():
            articles = await self.fetch_rss(name, url, keywords)
            all_articles.extend(articles)
            await asyncio.sleep(self.rate_limit)
        
        # Collect from sitemaps (historical)
        logger.info("Collecting from sitemaps...")
        for year in range(year_start, year_end + 1):
            for month in range(1, 13):
                for source in ['nytimes', 'guardian', 'reuters']:
                    articles = await self.fetch_sitemap(source, year, month, keywords)
                    all_articles.extend(articles)
                    await asyncio.sleep(self.rate_limit)
        
        return all_articles


class GoogleNewsCollector:
    """Collect from Google News search."""
    
    async def search_google_news(
        self,
        query: str,
        year_start: int,
        year_end: int
    ) -> List[Dict]:
        """Search Google News for historical articles."""
        
        # Google News RSS with date range
        # Format: https://news.google.com/rss/search?q=QUERY+after:YYYY-MM-DD+before:YYYY-MM-DD
        
        start_date = f"{year_start}-01-01"
        end_date = f"{year_end}-12-31"
        
        search_url = (
            f"https://news.google.com/rss/search?q="
            f"{query.replace(' ', '+')}"
            f"+after:{start_date}+before:{end_date}"
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, timeout=30) as response:
                    if response.status != 200:
                        return []
                    
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    articles = []
                    for entry in feed.entries:
                        articles.append({
                            'source': 'google_news',
                            'title': entry.get('title', ''),
                            'url': entry.get('link', ''),
                            'published': entry.get('published', ''),
                            'search_query': query
                        })
                    
                    return articles
                    
        except Exception as e:
            logger.error(f"Google News search failed: {e}")
            return []


async def run_collection(
    keywords: List[str],
    year_start: int,
    year_end: int,
    output_file: str
):
    """Run full collection."""
    
    logger.info(f"Starting collection: {year_start}-{year_end}")
    logger.info(f"Keywords: {keywords}")
    
    all_articles = []
    
    # Method 1: News API/RSS collection
    async with NewsAPICollector(rate_limit=1.0) as collector:
        articles = await collector.collect_by_keywords(
            keywords=keywords,
            year_start=year_start,
            year_end=year_end
        )
        all_articles.extend(articles)
    
    # Method 2: Google News
    google_collector = GoogleNewsCollector()
    for keyword in keywords[:3]:  # Limit to avoid rate limits
        articles = await google_collector.search_google_news(
            query=keyword,
            year_start=year_start,
            year_end=year_end
        )
        all_articles.extend(articles)
        await asyncio.sleep(2.0)
    
    # Save results
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(all_articles, f, indent=2)
    
    logger.info(f"Collection complete: {len(all_articles)} articles")
    logger.info(f"Saved to: {output_file}")
    
    return all_articles


if __name__ == '__main__':
    import sys
    
    # Keywords for collection
    EPSTEIN_KEYWORDS = [
        'jeffrey epstein', 'ghislaine maxwell', 'epstein island',
        'epstein victims', 'epstein sex trafficking'
    ]
    
    SEPT11_KEYWORDS = [
        'september 11', '9/11', 'world trade center',
        'terrorist attack 2001', 'ground zero'
    ]
    
    # Determine what to collect
    if len(sys.argv) > 1 and sys.argv[1] == 'epstein':
        keywords = EPSTEIN_KEYWORDS
        name = 'epstein'
    elif len(sys.argv) > 1 and sys.argv[1] == 'sept11':
        keywords = SEPT11_KEYWORDS
        name = 'sept11'
    else:
        keywords = EPSTEIN_KEYWORDS + SEPT11_KEYWORDS
        name = 'combined'
    
    # Date range
    year_start = int(sys.argv[2]) if len(sys.argv) > 2 else 2001
    year_end = int(sys.argv[3]) if len(sys.argv) > 3 else 2026
    
    output = f'/home/cbwinslow/workspace/epstein-data/urls/{name}_{year_start}_{year_end}.json'
    
    results = asyncio.run(run_collection(keywords, year_start, year_end, output))
    
    print(f"\n✅ Collection complete!")
    print(f"   Articles: {len(results)}")
    print(f"   Output: {output}")
