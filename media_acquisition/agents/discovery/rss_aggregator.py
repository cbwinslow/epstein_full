#!/usr/bin/env python3
"""
Multi-source RSS aggregator for comprehensive news discovery.
Fetches from 50+ RSS feeds with rate limiting and deduplication.
"""

import asyncio
import aiohttp
import feedparser
from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from urllib.parse import urlparse
import logging

from media_acquisition.base import AgentConfig, DiscoveryAgent, TaskResult, NewsArticleURL
from media_acquisition.sources.news_sources import get_sources_with_rss, NewsSource

logger = logging.getLogger(__name__)


@dataclass
class RSSArticle:
    """Article from RSS feed."""
    title: str
    url: str
    published: Optional[datetime]
    source: str
    summary: Optional[str] = None
    author: Optional[str] = None


class RSSAggregatorAgent(DiscoveryAgent):
    """
    Aggregate news from multiple RSS feeds.
    Supports 50+ news sources with intelligent rate limiting.
    """

    AGENT_ID = 'rss-aggregator-v1'
    VERSION = '1.0.0'

    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config)
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limits: Dict[str, datetime] = {}
        self.discovered_urls: Set[str] = set()

    async def _init_session(self):
        """Initialize aiohttp session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={'User-Agent': 'EpsteinResearchBot/1.0 (Research Project)'}
            )

    async def fetch_feed(self, source: NewsSource) -> List[RSSArticle]:
        """Fetch and parse a single RSS feed."""
        if not source.rss_url:
            return []

        # Check rate limit
        now = datetime.now()
        last_fetch = self.rate_limits.get(source.domain)
        if last_fetch:
            elapsed = (now - last_fetch).total_seconds()
            if elapsed < source.rate_limit_seconds:
                await asyncio.sleep(source.rate_limit_seconds - elapsed)

        try:
            await self._init_session()

            async with self.session.get(source.rss_url, timeout=30) as response:
                if response.status != 200:
                    logger.warning(f"RSS fetch failed for {source.name}: HTTP {response.status}")
                    return []

                content = await response.text()

            # Parse feed
            feed = feedparser.parse(content)
            articles = []

            for entry in feed.entries:
                # Extract URL
                url = entry.get('link', '')
                if not url or url in self.discovered_urls:
                    continue

                # Parse date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])

                articles.append(RSSArticle(
                    title=entry.get('title', ''),
                    url=url,
                    published=published,
                    source=source.name,
                    summary=entry.get('summary', '')[:500] if hasattr(entry, 'summary') else None,
                    author=entry.get('author', None)
                ))

                self.discovered_urls.add(url)

            # Update rate limit tracking
            self.rate_limits[source.domain] = datetime.now()

            logger.info(f"Fetched {len(articles)} articles from {source.name}")
            return articles

        except Exception as e:
            logger.warning(f"Failed to fetch RSS from {source.name}: {e}")
            return []

    def filter_by_keywords(self, articles: List[RSSArticle],
                          keywords: List[str]) -> List[RSSArticle]:
        """Filter articles by keywords in title or summary."""
        keyword_set = set(k.lower() for k in keywords)
        filtered = []

        for article in articles:
            text = f"{article.title} {article.summary or ''}".lower()
            if any(kw in text for kw in keyword_set):
                filtered.append(article)

        return filtered

    def filter_by_date(self, articles: List[RSSArticle],
                      start_date: Optional[datetime],
                      end_date: Optional[datetime]) -> List[RSSArticle]:
        """Filter articles by publication date range."""
        if not start_date and not end_date:
            return articles

        filtered = []
        for article in articles:
            if not article.published:
                # Include articles without dates (can't filter them out)
                filtered.append(article)
                continue

            if start_date and article.published < start_date:
                continue
            if end_date and article.published > end_date:
                continue

            filtered.append(article)

        return filtered

    async def discover(self,
                      keywords: List[str],
                      date_range: Optional[tuple] = None,
                      max_results: int = 1000,
                      max_sources: int = 50) -> TaskResult:
        """
        Discover articles from RSS feeds across multiple sources.

        Args:
            keywords: Search keywords
            date_range: (start_date, end_date) as datetime objects
            max_results: Maximum total results to return
            max_sources: Maximum number of RSS feeds to query

        Returns:
            TaskResult with list of NewsArticleURL objects
        """
        logger.info(f"RSS aggregation starting: {len(keywords)} keywords, max {max_results} results")

        # Get RSS-enabled sources
        sources = get_sources_with_rss()
        # Sort by priority and reliability
        sources.sort(key=lambda s: (s.priority, -s.reliability_score))
        sources = sources[:max_sources]

        logger.info(f"Querying {len(sources)} RSS feeds")

        # Fetch all feeds concurrently with semaphore for rate limiting
        semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests

        async def fetch_with_limit(source):
            async with semaphore:
                return await self.fetch_feed(source)

        # Fetch from all sources
        tasks = [fetch_with_limit(s) for s in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect all articles
        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.warning(f"RSS fetch error: {result}")

        logger.info(f"Fetched {len(all_articles)} total articles from RSS feeds")

        # Filter by keywords
        keyword_filtered = self.filter_by_keywords(all_articles, keywords)
        logger.info(f"After keyword filter: {len(keyword_filtered)} articles")

        # Filter by date range
        start_date, end_date = date_range if date_range else (None, None)
        date_filtered = self.filter_by_date(keyword_filtered, start_date, end_date)
        logger.info(f"After date filter: {len(date_filtered)} articles")

        # Convert to NewsArticleURL
        final_articles = date_filtered[:max_results]
        news_urls = []
        for article in final_articles:
            matched_keywords = [k for k in keywords if k.lower() in article.title.lower()]
            news_urls.append(NewsArticleURL(
                url=article.url,
                title=article.title,
                priority=3,  # Medium priority for RSS
                keywords_matched=matched_keywords,
                discovery_method=f"rss-{article.source.lower().replace(' ', '-')}"
            ))

        # Update metrics
        self.metrics['items_discovered'] = len(news_urls)
        self.metrics['sources_breakdown'] = {}

        logger.info(f"RSS discovery complete: {len(news_urls)} articles")

        return TaskResult(
            status='success',
            output=news_urls,
            metadata={'agent_id': self.AGENT_ID, 'metrics': self.metrics}
        )

    async def execute(self, task: Dict[str, any]) -> TaskResult:
        """Execute RSS aggregation task."""
        keywords = task.get("keywords", ["Jeffrey Epstein", "Epstein"])
        date_range = task.get("date_range")
        max_results = task.get("max_results", 1000)
        max_sources = task.get("max_sources", 50)

        return await self.discover(keywords, date_range, max_results, max_sources)

    async def close(self):
        """Close session and cleanup."""
        if self.session:
            try:
                await self.session.close()
                # Give time for connections to close
                await asyncio.sleep(0.5)
            except Exception:
                pass
            self.session = None
