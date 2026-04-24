#!/usr/bin/env python3
"""
News Ingestion Framework
Professional framework for large-scale news article ingestion.
Recreates the pipeline that collected 9,700+ Epstein articles.

Architecture:
    ┌─────────────────────────────────────────────────────────────────┐
    │                    MegaParallelOrchestrator                    │
    │                        (30 concurrent stages)                  │
    └─────────────────────────┬─────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ Google News  │   │   RSS Feeds  │   │    GDELT     │
    │   Scraper    │   │  Aggregator  │   │    API       │
    └──────────────┘   └──────────────┘   └──────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  CollectionQueue │
                    │   (PostgreSQL)     │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  NewsCollector   │
                    │ (Fetch & Store)  │
                    └──────────────────┘

Based on actual ingestion that collected 9,700 articles (2000-2025).
"""

import asyncio
import aiohttp
import psycopg2
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import json
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
import sys

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('news_framework')


@dataclass
class DiscoveryConfig:
    """Configuration for discovery agents."""
    keywords: List[str]
    start_date: datetime
    end_date: datetime
    sources: List[str] = field(default_factory=lambda: ['google_news', 'rss', 'gdelt'])
    max_results_per_source: int = 1000
    rate_limit_seconds: float = 0.3


@dataclass
class CollectionConfig:
    """Configuration for collection agents."""
    batch_size: int = 200
    max_concurrent_collectors: int = 20
    rate_limit_seconds: float = 0.3
    retry_attempts: int = 3
    request_timeout: int = 30


@dataclass
class MegaParallelConfig:
    """Configuration for mega-parallel orchestration."""
    max_concurrent_stages: int = 30
    stage_batch_size: timedelta = field(default_factory=lambda: timedelta(days=120))  # 4 months
    collection_concurrency: int = 20
    discovery_concurrency: int = 5


class DiscoveryAgent:
    """Base class for discovery agents."""
    
    def __init__(self, config: DiscoveryConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def discover(self) -> List[Dict]:
        """Discover articles. Override in subclass."""
        raise NotImplementedError


class GoogleNewsDiscoveryAgent(DiscoveryAgent):
    """Google News scraper - the primary source for our 9,700 articles."""
    
    BASE_URL = "https://www.google.com/search"
    
    async def discover(self) -> List[Dict]:
        """Scrape Google News for articles matching keywords."""
        articles = []
        
        for keyword in self.config.keywords:
            # Google News search with tbs=cdr for date range
            params = {
                'q': keyword,
                'tbm': 'nws',
                'tbs': f"cdr:1,cd_min:{self.config.start_date.strftime('%m/%d/%Y')},cd_max:{self.config.end_date.strftime('%m/%d/%Y')}"
            }
            
            try:
                async with self.session.get(self.BASE_URL, params=params, timeout=30) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        # Parse Google News results
                        parsed = self._parse_google_news(html, keyword)
                        articles.extend(parsed)
                        logger.info(f"Google News [{keyword}]: Found {len(parsed)} articles")
                        
            except Exception as e:
                logger.error(f"Google News error for '{keyword}': {e}")
                
            await asyncio.sleep(self.config.rate_limit_seconds)
            
        return articles
    
    def _parse_google_news(self, html: str, keyword: str) -> List[Dict]:
        """Parse Google News HTML. Simplified version."""
        from bs4 import BeautifulSoup
        articles = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Google News article cards
        for card in soup.find_all('div', class_=['SoaBEf', 'g']):
            try:
                link = card.find('a', href=True)
                title_elem = card.find(['h3', 'h4'])
                
                if link and title_elem:
                    url = link['href']
                    if url.startswith('/url?'):
                        url = url.split('&')[0].replace('/url?q=', '')
                    
                    articles.append({
                        'url': url,
                        'title': title_elem.get_text(strip=True),
                        'source': 'google_news',
                        'keywords_matched': [keyword],
                        'discovery_method': 'google_news_scraper',
                        'discovered_at': datetime.now().isoformat()
                    })
            except Exception:
                continue
                
        return articles[:self.config.max_results_per_source]


class RSSDiscoveryAgent(DiscoveryAgent):
    """RSS feed aggregator - secondary source."""
    
    FEEDS = [
        'http://feeds.bbci.co.uk/news/rss.xml',
        'http://rss.cnn.com/rss/cnn_latest.rss',
        'https://feeds.npr.org/1001/rss.xml',
        'https://www.reutersagency.com/feed/en/all-news/',
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'https://feeds.washingtonpost.com/rss/national',
        'https://www.theguardian.com/uk/rss',
        'https://news.ycombinator.com/rss',
    ]
    
    async def discover(self) -> List[Dict]:
        """Parse RSS feeds for articles."""
        import feedparser
        articles = []
        
        for feed_url in self.FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    # Check if matches keywords
                    text = f"{entry.get('title', '')} {entry.get('summary', '')}"
                    matched = [k for k in self.config.keywords if k.lower() in text.lower()]
                    
                    if matched:
                        # Check date range
                        pub_date = self._parse_date(entry)
                        if pub_date and self.config.start_date <= pub_date <= self.config.end_date:
                            articles.append({
                                'url': entry.get('link'),
                                'title': entry.get('title'),
                                'source': feed.feed.get('title', 'Unknown'),
                                'keywords_matched': matched,
                                'discovery_method': 'rss',
                                'published_date': pub_date.isoformat() if pub_date else None,
                                'discovered_at': datetime.now().isoformat()
                            })
                            
                logger.info(f"RSS [{feed.feed.get('title', 'Unknown')}]: Found matches")
                
            except Exception as e:
                logger.error(f"RSS error for {feed_url}: {e}")
                
            await asyncio.sleep(self.config.rate_limit_seconds)
            
        return articles
    
    def _parse_date(self, entry) -> Optional[datetime]:
        """Parse date from RSS entry."""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                return datetime(*entry.published_parsed[:6])
            except:
                pass
        return None


class CollectionQueue:
    """PostgreSQL-backed queue for articles awaiting collection."""
    
    def __init__(self, dsn: str = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'):
        self.dsn = dsn
        self._ensure_table()
    
    def _ensure_table(self):
        """Create queue table if not exists."""
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS collection_queue (
                        id SERIAL PRIMARY KEY,
                        run_id UUID NOT NULL,
                        url TEXT UNIQUE NOT NULL,
                        title TEXT,
                        source TEXT,
                        keywords_matched TEXT[],
                        discovery_method VARCHAR(50),
                        discovered_at TIMESTAMP DEFAULT NOW(),
                        status VARCHAR(20) DEFAULT 'pending',
                        collected_at TIMESTAMP,
                        content_length INTEGER,
                        error_message TEXT
                    );
                    CREATE INDEX IF NOT EXISTS idx_queue_status ON collection_queue(status);
                    CREATE INDEX IF NOT EXISTS idx_queue_run ON collection_queue(run_id);
                """)
                conn.commit()
    
    def add_articles(self, run_id: uuid.UUID, articles: List[Dict]):
        """Add discovered articles to queue."""
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                for article in articles:
                    try:
                        cur.execute("""
                            INSERT INTO collection_queue 
                            (run_id, url, title, source, keywords_matched, discovery_method, discovered_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (url) DO NOTHING
                        """, (
                            str(run_id),
                            article['url'],
                            article.get('title', ''),
                            article.get('source', 'unknown'),
                            article.get('keywords_matched', []),
                            article.get('discovery_method', 'unknown'),
                            article.get('discovered_at', datetime.now())
                        ))
                    except Exception as e:
                        logger.error(f"Queue add error: {e}")
                conn.commit()
    
    def get_pending(self, run_id: uuid.UUID, limit: int = 100) -> List[Dict]:
        """Get pending articles from queue."""
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, url, title, source, keywords_matched
                    FROM collection_queue
                    WHERE run_id = %s AND status = 'pending'
                    LIMIT %s
                """, (str(run_id), limit))
                return [
                    {
                        'id': row[0],
                        'url': row[1],
                        'title': row[2],
                        'source': row[3],
                        'keywords': row[4]
                    }
                    for row in cur.fetchall()
                ]
    
    def mark_collected(self, article_id: int, content_length: int):
        """Mark article as collected."""
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE collection_queue
                    SET status = 'completed', collected_at = NOW(), content_length = %s
                    WHERE id = %s
                """, (content_length, article_id))
                conn.commit()
    
    def mark_failed(self, article_id: int, error: str):
        """Mark article as failed."""
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE collection_queue
                    SET status = 'failed', error_message = %s
                    WHERE id = %s
                """, (error[:500], article_id))
                conn.commit()
    
    def get_stats(self, run_id: uuid.UUID) -> Dict:
        """Get queue statistics."""
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                        COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed
                    FROM collection_queue
                    WHERE run_id = %s
                """, (str(run_id),))
                row = cur.fetchone()
                return {
                    'total': row[0],
                    'pending': row[1],
                    'completed': row[2],
                    'failed': row[3]
                }


class NewsCollector:
    """Fetches article content using trafilatura."""
    
    def __init__(self, config: CollectionConfig):
        self.config = config
        
    async def collect(self, article: Dict) -> Optional[Dict]:
        """Collect article content."""
        try:
            from trafilatura import fetch_url, extract
            
            downloaded = fetch_url(article['url'], timeout=self.config.request_timeout)
            if not downloaded:
                return None
            
            result = extract(
                downloaded,
                output_format='json',
                include_comments=False,
                include_tables=True,
                url=article['url']
            )
            
            if result:
                data = json.loads(result)
                content = data.get('text', '') or data.get('raw_text', '')
                return {
                    'queue_id': article['id'],
                    'url': article['url'],
                    'title': data.get('title', article['title']),
                    'content': content,
                    'author': data.get('author'),
                    'publish_date': data.get('date'),
                    'word_count': len(content.split()) if content else 0,
                    'source': article['source'],
                    'keywords': article['keywords'],
                    'hostname': data.get('hostname'),
                    'description': data.get('description'),
                    'categories': data.get('categories', []),
                    'tags': data.get('tags', []),
                    'language': data.get('language')
                }
            
        except Exception as e:
            logger.error(f"Collection error for {article['url']}: {e}")
            
        return None


class MegaParallelOrchestrator:
    """
    Mega-parallel orchestrator - recreates our 9,700 article ingestion.
    
    Config used for Epstein collection:
    - 30 concurrent stages (4-month chunks)
    - 20 collectors per stage  
    - 0.3s rate limiting
    - Keywords: ['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre']
    - Date range: 2000-01-01 to 2025-12-31
    - Result: 9,700 articles
    """
    
    def __init__(self, config: MegaParallelConfig):
        self.config = config
        self.queue = CollectionQueue()
        
    def create_stages(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Create ingestion stages (4-month chunks)."""
        stages = []
        current = start_date
        
        while current < end_date:
            stage_end = min(current + self.config.stage_batch_size, end_date)
            stages.append({
                'stage_num': len(stages) + 1,
                'start_date': current,
                'end_date': stage_end,
                'run_id': uuid.uuid4()
            })
            current = stage_end
            
        return stages
    
    async def run_stage(self, stage: Dict, discovery_config: DiscoveryConfig, 
                       collection_config: CollectionConfig):
        """Run a single ingestion stage."""
        run_id = stage['run_id']
        
        logger.info(f"Stage {stage['stage_num']}: {stage['start_date'].date()} to {stage['end_date'].date()}")
        
        # Update discovery config for this stage's date range
        stage_discovery_config = DiscoveryConfig(
            keywords=discovery_config.keywords,
            start_date=stage['start_date'],
            end_date=stage['end_date'],
            sources=discovery_config.sources,
            max_results_per_source=discovery_config.max_results_per_source,
            rate_limit_seconds=discovery_config.rate_limit_seconds
        )
        
        # Discovery phase
        all_discovered = []
        
        if 'google_news' in stage_discovery_config.sources:
            async with GoogleNewsDiscoveryAgent(stage_discovery_config) as agent:
                discovered = await agent.discover()
                all_discovered.extend(discovered)
                
        if 'rss' in stage_discovery_config.sources:
            async with RSSDiscoveryAgent(stage_discovery_config) as agent:
                discovered = await agent.discover()
                all_discovered.extend(discovered)
        
        # Add to queue
        if all_discovered:
            self.queue.add_articles(run_id, all_discovered)
            logger.info(f"Stage {stage['stage_num']}: Queued {len(all_discovered)} articles")
        
        # Collection phase
        collector = NewsCollector(collection_config)
        total_collected = 0
        
        while True:
            pending = self.queue.get_pending(run_id, limit=collection_config.batch_size)
            if not pending:
                break
                
            # Collect with semaphore for concurrency control
            semaphore = asyncio.Semaphore(self.config.collection_concurrency)
            
            async def collect_with_limit(article):
                async with semaphore:
                    result = await collector.collect(article)
                    await asyncio.sleep(collection_config.rate_limit_seconds)
                    return result
            
            tasks = [collect_with_limit(article) for article in pending]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Store results
            for article, result in zip(pending, results):
                if isinstance(result, Exception):
                    self.queue.mark_failed(article['id'], str(result))
                elif result:
                    await self._store_article(result)
                    self.queue.mark_collected(article['id'], len(result['content'] or ''))
                    total_collected += 1
                else:
                    self.queue.mark_failed(article['id'], 'No content extracted')
        
        stats = self.queue.get_stats(run_id)
        logger.info(f"Stage {stage['stage_num']} complete: {stats}")
        
        return stats
    
    async def _store_article(self, article: Dict):
        """Store collected article to database."""
        import psycopg2
        
        dsn = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO media_news_articles (
                        source_domain, source_name, article_url, title, authors,
                        publish_date, content, summary, keywords, word_count,
                        discovery_source, collected_at, all_topics
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
                    ON CONFLICT (article_url) DO NOTHING
                """, (
                    article.get('hostname', 'unknown'),
                    article.get('source', 'unknown'),
                    article['url'],
                    article.get('title', ''),
                    [article.get('author')] if article.get('author') else None,
                    article.get('publish_date'),
                    article.get('content', ''),
                    article.get('description', ''),
                    article.get('keywords', []),
                    article.get('word_count', 0),
                    'mega_parallel_ingestion',
                    json.dumps({
                        'categories': article.get('categories', []),
                        'tags': article.get('tags', []),
                        'language': article.get('language')
                    })
                ))
                conn.commit()
    
    async def run(self, start_date: datetime, end_date: datetime,
                  discovery_config: DiscoveryConfig, collection_config: CollectionConfig):
        """Run mega-parallel ingestion."""
        logger.info("="*60)
        logger.info("MEGA-PARALLEL NEWS INGESTION")
        logger.info("="*60)
        logger.info(f"Date range: {start_date.date()} to {end_date.date()}")
        logger.info(f"Keywords: {discovery_config.keywords}")
        logger.info(f"Max concurrent stages: {self.config.max_concurrent_stages}")
        
        # Create stages
        stages = self.create_stages(start_date, end_date)
        logger.info(f"Total stages: {len(stages)}")
        
        # Run stages with semaphore
        semaphore = asyncio.Semaphore(self.config.max_concurrent_stages)
        
        async def run_stage_limited(stage):
            async with semaphore:
                return await self.run_stage(stage, discovery_config, collection_config)
        
        # Execute all stages
        results = await asyncio.gather(*[run_stage_limited(stage) for stage in stages])
        
        # Aggregate results
        total_stats = {
            'total_discovered': sum(r['total'] for r in results),
            'total_collected': sum(r['completed'] for r in results),
            'total_failed': sum(r['failed'] for r in results)
        }
        
        logger.info("="*60)
        logger.info("INGESTION COMPLETE")
        logger.info("="*60)
        logger.info(f"Total discovered: {total_stats['total_discovered']}")
        logger.info(f"Total collected: {total_stats['total_collected']}")
        logger.info(f"Total failed: {total_stats['total_failed']}")
        
        return total_stats


# Convenience function to recreate the exact Epstein ingestion
def run_epstein_ingestion(
    start_year: int = 2000,
    end_year: int = 2025,
    keywords: List[str] = None,
    max_stages: int = 30
):
    """
    Recreate the Epstein article ingestion that collected 9,700 articles.
    
    Args:
        start_year: Start year (default 2000)
        end_year: End year (default 2025)
        keywords: Search keywords (default: ['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre'])
        max_stages: Concurrent stages (default 30)
    
    Returns:
        Dict with ingestion statistics
    """
    if keywords is None:
        keywords = ['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre']
    
    # Create configurations matching our successful run
    mega_config = MegaParallelConfig(
        max_concurrent_stages=max_stages,
        stage_batch_size=timedelta(days=120),  # 4 months per stage
        collection_concurrency=20
    )
    
    discovery_config = DiscoveryConfig(
        keywords=keywords,
        start_date=datetime(start_year, 1, 1),
        end_date=datetime(end_year, 12, 31),
        sources=['google_news', 'rss'],
        max_results_per_source=1000,
        rate_limit_seconds=0.3
    )
    
    collection_config = CollectionConfig(
        batch_size=200,
        max_concurrent_collectors=20,
        rate_limit_seconds=0.3
    )
    
    # Run ingestion
    orchestrator = MegaParallelOrchestrator(mega_config)
    
    return asyncio.run(orchestrator.run(
        discovery_config.start_date,
        discovery_config.end_date,
        discovery_config,
        collection_config
    ))


if __name__ == '__main__':
    # Recreate the exact ingestion that collected 9,700 articles
    results = run_epstein_ingestion()
    print(f"\nRecreate Results: {results}")
