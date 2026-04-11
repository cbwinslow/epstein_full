#!/usr/bin/env python3
"""
Phase 1: URL Discovery Agent

Purpose: Search RSS feeds and news sources for article URLs matching keywords.

Input:
  - Keywords (e.g., ['Jeffrey Epstein', 'Epstein case'])
  - Date range (e.g., 2024-01-01 to 2025-12-31)
  - Sources (RSS feeds, Google News)

Output:
  - Discovered URLs saved to `article_discovery_queue` table
  - Metadata: source, discovery_date, keywords_matched

Usage:
  python phase1_discovery.py --keywords "Jeffrey Epstein" --start-date 2024-01-01 --end-date 2025-12-31

This script ONLY discovers URLs. Does NOT download article content.
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, date
from typing import List, Dict, Optional
import feedparser
import aiohttp

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discovery')


class RSSDiscoveryAgent:
    """
    Agent for discovering article URLs from RSS feeds.
    
    Workflow:
      1. Load RSS feed URLs
      2. Parse feeds for articles
      3. Filter by date range and keywords
      4. Return discovered URLs with metadata
    """
    
    def __init__(self, keywords: List[str], start_date: date, end_date: date):
        self.keywords = [k.lower() for k in keywords]
        self.start_date = start_date
        self.end_date = end_date
        self.discovered = []
        
    def load_rss_feeds(self) -> List[str]:
        """Load RSS feed URLs to check."""
        # Major news RSS feeds
        return [
            'http://feeds.bbci.co.uk/news/rss.xml',
            'http://rss.cnn.com/rss/cnn_latest.rss',
            'https://feeds.npr.org/1001/rss.xml',
            'https://www.reutersagency.com/feed/en/all-news/',
            'https://feeds.huffpost.com/huffingtonpost/raw_news',
            'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            'https://feeds.washingtonpost.com/rss/national',
            'https://www.theguardian.com/uk/rss',
            'https://feeds.fortune.com/fortune/headlines',
            'https://www.vice.com/en/rss',
        ]
    
    def matches_keywords(self, text: str) -> bool:
        """Check if text matches any keyword."""
        if not text:
            return False
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.keywords)
    
    def parse_date(self, entry) -> Optional[date]:
        """Extract date from RSS entry."""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                return datetime(*entry.parsed[:6]).date()
            except:
                pass
        if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            try:
                return datetime(*entry.updated_parsed[:6]).date()
            except:
                pass
        return None
    
    def discover_from_feed(self, feed_url: str) -> List[Dict]:
        """Discover URLs from a single RSS feed."""
        discovered = []
        
        try:
            logger.info(f"Parsing feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                # Get entry details
                title = getattr(entry, 'title', '')
                link = getattr(entry, 'link', '')
                summary = getattr(entry, 'summary', '')
                
                if not link:
                    continue
                
                # Check keywords
                text_to_check = f"{title} {summary}"
                if not self.matches_keywords(text_to_check):
                    continue
                
                # Check date
                entry_date = self.parse_date(entry)
                if entry_date:
                    if entry_date < self.start_date or entry_date > self.end_date:
                        continue
                
                # Found matching article
                discovered.append({
                    'url': link,
                    'title': title,
                    'source': feed.feed.get('title', 'Unknown'),
                    'source_feed': feed_url,
                    'published_date': entry_date.isoformat() if entry_date else None,
                    'keywords_matched': [k for k in self.keywords if k in text_to_check.lower()],
                    'discovery_method': 'rss',
                    'discovered_at': datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"Error parsing feed {feed_url}: {e}")
        
        logger.info(f"  Found {len(discovered)} matching articles")
        return discovered
    
    async def discover_all(self) -> List[Dict]:
        """Run discovery on all feeds."""
        feeds = self.load_rss_feeds()
        all_discovered = []
        
        logger.info(f"Starting discovery with {len(feeds)} feeds")
        logger.info(f"Keywords: {self.keywords}")
        logger.info(f"Date range: {self.start_date} to {self.end_date}")
        
        for feed_url in feeds:
            discovered = self.discover_from_feed(feed_url)
            all_discovered.extend(discovered)
            await asyncio.sleep(1)  # Rate limiting
        
        logger.info(f"Discovery complete: {len(all_discovered)} total URLs found")
        return all_discovered


def save_to_discovery_queue(discovered: List[Dict]):
    """Save discovered URLs to database queue."""
    import psycopg2
    
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()
    
    # Create queue table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS article_discovery_queue (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            source TEXT,
            source_feed TEXT,
            published_date DATE,
            keywords_matched TEXT[],
            discovery_method VARCHAR(50),
            discovered_at TIMESTAMP DEFAULT NOW(),
            status VARCHAR(20) DEFAULT 'pending',
            processed_at TIMESTAMP
        )
    """)
    
    saved = 0
    duplicates = 0
    
    for item in discovered:
        try:
            cur.execute("""
                INSERT INTO article_discovery_queue 
                (url, title, source, source_feed, published_date, keywords_matched, discovery_method)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            """, (
                item['url'],
                item['title'],
                item['source'],
                item['source_feed'],
                item['published_date'],
                item['keywords_matched'],
                item['discovery_method']
            ))
            
            if cur.rowcount > 0:
                saved += 1
            else:
                duplicates += 1
                
        except Exception as e:
            logger.error(f"Error saving URL {item['url']}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    logger.info(f"Saved {saved} new URLs to queue ({duplicates} duplicates skipped)")
    return saved


async def main():
    parser = argparse.ArgumentParser(description='Phase 1: Discover article URLs from RSS feeds')
    parser.add_argument('--keywords', nargs='+', default=['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell'],
                        help='Keywords to search for')
    parser.add_argument('--start-date', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
                        default=date(2024, 1, 1), help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
                        default=date(2025, 12, 31), help='End date (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, help='Optional: Save results to JSON file')
    
    args = parser.parse_args()
    
    # Run discovery
    agent = RSSDiscoveryAgent(args.keywords, args.start_date, args.end_date)
    discovered = await agent.discover_all()
    
    # Save to database
    if discovered:
        saved = save_to_discovery_queue(discovered)
        
        # Optional: Save to JSON for review
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(discovered, f, indent=2)
            logger.info(f"Results saved to: {args.output}")
    else:
        logger.warning("No URLs discovered")
    
    logger.info("Phase 1 complete. Run phase2_fetch_content.py to extract article content.")


if __name__ == '__main__':
    asyncio.run(main())
