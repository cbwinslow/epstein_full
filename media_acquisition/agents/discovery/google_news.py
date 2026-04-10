#!/usr/bin/env python3
"""Google News scraper for Epstein article discovery.

This module provides a scraper for Google News search results,
allowing bulk discovery of news articles without API rate limits.
"""

import logging
import time
from typing import List, Optional, Tuple
from urllib.parse import quote_plus, urlparse
import requests

from media_acquisition.base import DiscoveryAgent, AgentConfig, TaskResult, NewsArticleURL

logger = logging.getLogger(__name__)


class GoogleNewsScraper(DiscoveryAgent):
    """Scraper for Google News search results.

    Google News provides search results without API keys or rate limits.
    This scraper extracts article URLs, titles, and metadata from
    Google News search pages.
    """

    BASE_URL = "https://news.google.com/search"
    RSS_URL = "https://news.google.com/rss/search"

    def __init__(self, config: Optional[AgentConfig] = None, delay: float = 2.0):
        """Initialize Google News scraper.

        Args:
            config: Agent configuration
            delay: Seconds between requests to avoid being blocked
        """
        if config is None:
            config = AgentConfig(agent_id="google_news_scraper")
        super().__init__(config)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.last_request_time = 0

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            sleep_time = self.delay - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.1f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def search(self,
               keywords: List[str],
               date_range: Tuple[str, str],
               max_results: int = 1000) -> TaskResult:
        """Search Google News for articles.

        Args:
            keywords: Search terms
            date_range: (start_date, end_date) as 'YYYY-MM-DD'
            max_results: Maximum articles to retrieve

        Returns:
            TaskResult with discovered articles
        """
        logger.info(f"Starting Google News search for {len(keywords)} keywords")

        all_articles: List[NewsArticleURL] = []

        for keyword in keywords[:5]:  # Limit keywords to avoid excessive scraping
            articles = self._search_keyword(keyword, date_range, max_results // 5)
            all_articles.extend(articles)

            if len(all_articles) >= max_results:
                break

        # Deduplicate by URL
        seen_urls: set = set()
        unique_articles: List[NewsArticleURL] = []
        for article in all_articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)

        logger.info(f"Google News search complete: {len(unique_articles)} unique articles")

        status = 'success' if len(unique_articles) > 0 else 'failure'
        return TaskResult(
            status=status,
            output=unique_articles
        )

    def _search_keyword(self,
                       keyword: str,
                       date_range: Tuple[str, str],
                       max_results: int) -> List[NewsArticleURL]:
        """Search for a single keyword using RSS feed (more reliable than scraping)."""
        results = []

        # Google News RSS format
        # Use quotes for exact match, date range operators
        # Format: "Jeffrey Epstein" after:2024-01-01 before:2024-12-31
        query = f'"{keyword}" after:{date_range[0]} before:{date_range[1]}'
        encoded_query = quote_plus(query)

        rss_url = f"{self.RSS_URL}?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

        try:
            self._rate_limit()
            logger.debug(f"Fetching RSS: {rss_url[:100]}...")

            response = self.session.get(rss_url, timeout=30)
            response.raise_for_status()

            # Parse RSS XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(response.content)

            # Find all items
            items = root.findall('.//item')

            for item in items[:max_results]:
                title = item.findtext('title', '')
                link = item.findtext('link', '')
                pub_date = item.findtext('pubDate', '')
                description = item.findtext('description', '')

                # Use Google News URL directly
                # The article downloader will follow redirects when fetching content
                real_url = link if link else None

                if not real_url:
                    continue

                # Parse publish date
                try:
                    # Format: Mon, 07 Apr 2026 12:00:00 GMT
                    from email.utils import parsedate_to_datetime
                    publish_dt = parsedate_to_datetime(pub_date)
                except:
                    publish_dt = None

                # Extract source domain
                domain = urlparse(real_url).netloc

                results.append(NewsArticleURL(
                    url=real_url,
                    title=title,
                    source_domain=domain,
                    publish_date=publish_dt,
                    discovery_method='google_news',
                    priority=2,  # Higher priority than RSS
                    keywords_matched=[keyword],
                    metadata={
                        'description': description,
                        'rss_url': link
                    }
                ))

        except Exception as e:
            logger.warning(f"Google News RSS fetch failed for '{keyword}': {e}")

        logger.info(f"Found {len(results)} articles for keyword '{keyword}'")
        return results

    def _extract_real_url(self, google_url: str) -> Optional[str]:
        """Extract the real article URL from Google News redirect URL."""
        if not google_url:
            return None

        # If it's already a direct URL, return it
        if not ('news.google.com' in google_url or 'google.com/news' in google_url):
            return google_url

        try:
            # Follow the redirect to get the real URL
            self._rate_limit()
            response = self.session.head(google_url, allow_redirects=True, timeout=10)
            return response.url
        except:
            # Fallback: try to extract from URL parameters
            import urllib.parse
            parsed = urllib.parse.urlparse(google_url)
            params = urllib.parse.parse_qs(parsed.query)

            # Look for 'url' parameter
            if 'url' in params:
                return params['url'][0]

            return None

    def discover(self, keywords: List[str] = None, date_range: Tuple[str, str] = None) -> List[NewsArticleURL]:
        """Discovery interface for compatibility."""
        if keywords is None:
            keywords = []
        if date_range is None:
            date_range = ('2019-01-01', '2025-12-31')

        result = self.search(keywords, date_range)
        output = result.output if result.output else []
        return output if isinstance(output, list) else []
