#!/usr/bin/env python3
"""
Epstein Article Collection with Trafilatura
Uses existing GoogleNewsScraper for discovery + Trafilatura for extraction.

This recreates the 9,700 article collection using the proven discovery method
with better content extraction (Trafilatura instead of newspaper3k/BeautifulSoup).

Usage:
    python collect_epstein_trafilatura.py --test          # Quick test (10 articles)
    python collect_epstein_trafilatura.py --full          # Full collection (2000-2025)
    python collect_epstein_trafilatura.py --year 2019     # Single year
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse

import psycopg2
import requests
from trafilatura import fetch_url, extract

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from media_acquisition.agents.discovery.google_news import GoogleNewsScraper
from media_acquisition.base import AgentConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URL = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'


def resolve_url(url: str) -> Optional[str]:
    """Follow redirects to get actual article URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        # Use GET for Google News (HEAD doesn't work for their redirects)
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=15, stream=True)
        response.close()  # Close connection without downloading full content
        
        if response.status_code == 200:
            final_url = response.url
            # Skip if still Google News
            if 'news.google.com' in final_url:
                return None
            return final_url
    except Exception as e:
        logger.debug(f"URL resolution failed: {e}")
    return None


class TrafilaturaExtractor:
    """Extract article content using Trafilatura."""
    
    def extract(self, url: str) -> Optional[Dict]:
        """Extract article content and metadata."""
        try:
            downloaded = fetch_url(url)
            if not downloaded:
                logger.warning(f"Failed to download: {url}")
                return None
            
            result = extract(
                downloaded,
                output_format='json',
                include_comments=False,
                include_tables=True,
                url=url
            )
            
            if result:
                data = eval(result)  # Safe since trafilatura returns JSON string
                content = data.get('text', '') or data.get('raw_text', '')
                
                return {
                    'url': url,
                    'title': data.get('title', ''),
                    'content': content,
                    'author': data.get('author'),
                    'publish_date': data.get('date'),
                    'word_count': len(content.split()) if content else 0,
                    'hostname': data.get('hostname', urlparse(url).netloc),
                    'description': data.get('description'),
                    'categories': data.get('categories', []),
                    'tags': data.get('tags', []),
                    'language': data.get('language', 'en'),
                    'fingerprint': data.get('fingerprint')
                }
        except Exception as e:
            logger.error(f"Extraction error for {url}: {e}")
        
        return None


def discover_articles(keywords: List[str], start_date: str, end_date: str, max_results: int = 1000) -> List[Dict]:
    """Discover articles using GoogleNewsScraper."""
    logger.info(f"Discovering articles: {keywords} ({start_date} to {end_date})")
    
    config = AgentConfig(agent_id="epstein_discovery")
    scraper = GoogleNewsScraper(config, delay=1.0)
    
    result = scraper.search(keywords, (start_date, end_date), max_results=max_results)
    
    articles = []
    if result.status == 'success' and result.output:
        for article in result.output:
            articles.append({
                'url': article.url,
                'title': article.title,
                'source': article.source_domain or urlparse(article.url).netloc,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None
            })
    
    logger.info(f"Discovered {len(articles)} articles")
    return articles


def store_article(article: Dict, keywords: List[str]) -> bool:
    """Store article in PostgreSQL."""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO media_news_articles (
                source_domain, source_name, article_url, title, authors,
                publish_date, content, summary, keywords, word_count,
                discovery_source, collected_at, all_topics
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
            ON CONFLICT (article_url) DO UPDATE SET
                content = EXCLUDED.content,
                word_count = EXCLUDED.word_count,
                collected_at = NOW()
            RETURNING id
        """, (
            article.get('hostname', 'unknown'),
            article.get('source', 'unknown'),
            article['url'],
            article.get('title', '')[:500],
            [article.get('author')] if article.get('author') else None,
            article.get('publish_date'),
            article.get('content', ''),
            article.get('description', '')[:1000],
            keywords,
            article.get('word_count', 0),
            'trafilatura_ingestion',
            str({
                'categories': article.get('categories', []),
                'tags': article.get('tags', []),
                'language': article.get('language', 'en'),
                'fingerprint': article.get('fingerprint')
            })
        ))
        
        article_id = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return article_id is not None
        
    except Exception as e:
        logger.error(f"Store error: {e}")
        return False


def collect_articles(keywords: List[str], start_year: int, end_year: int, max_articles: int = 100):
    """Main collection workflow."""
    logger.info("="*60)
    logger.info("EPSTEIN ARTICLE COLLECTION - Trafilatura Edition")
    logger.info("="*60)
    
    # Stats
    discovered = 0
    collected = 0
    failed = 0
    
    extractor = TrafilaturaExtractor()
    
    # Process year by year
    for year in range(start_year, end_year + 1):
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        logger.info(f"\n--- Processing {year} ---")
        
        # Discover
        articles = discover_articles(keywords, start_date, end_date, max_results=max_articles)
        discovered += len(articles)
        
        # Collect and store
        for i, article in enumerate(articles[:max_articles]):
            logger.info(f"  [{i+1}/{len(articles)}] {article['title'][:60]}...")
            
            # Resolve Google News redirect URL
            real_url = resolve_url(article['url'])
            if not real_url:
                logger.info("    ✗ Could not resolve URL")
                failed += 1
                continue
            
            logger.debug(f"    Resolved to: {real_url}")
            
            extracted = extractor.extract(real_url)
            
            if extracted and extracted.get('content'):
                if store_article(extracted, keywords):
                    collected += 1
                    logger.info(f"    ✓ Stored ({extracted.get('word_count', 0)} words)")
                else:
                    failed += 1
                    logger.info("    ✗ Store failed")
            else:
                failed += 1
                logger.info("    ✗ No content extracted")
            
            # Rate limiting
            asyncio.run(asyncio.sleep(1.0))
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("COLLECTION COMPLETE")
    logger.info("="*60)
    logger.info(f"Discovered: {discovered}")
    logger.info(f"Collected: {collected}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Success rate: {collected/max(discovered,1)*100:.1f}%")
    
    return {'discovered': discovered, 'collected': collected, 'failed': failed}


def main():
    parser = argparse.ArgumentParser(description='Collect Epstein articles with Trafilatura')
    parser.add_argument('--test', action='store_true', help='Quick test (2024, 10 articles)')
    parser.add_argument('--full', action='store_true', help='Full collection (2000-2025)')
    parser.add_argument('--year', type=int, help='Single year to collect')
    parser.add_argument('--max', type=int, default=100, help='Max articles per year')
    
    args = parser.parse_args()
    
    keywords = ['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell']
    
    if args.test:
        collect_articles(keywords, 2024, 2024, max_articles=10)
    elif args.full:
        collect_articles(keywords, 2000, 2025, max_articles=args.max)
    elif args.year:
        collect_articles(keywords, args.year, args.year, max_articles=args.max)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
