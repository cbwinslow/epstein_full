"""
News Discovery Agent
Discovers Epstein-related news articles from GDELT, Wayback Machine, and RSS feeds.
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import aiohttp
import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Import base classes
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from media_acquisition.base import (
    DiscoveryAgent, AgentConfig, TaskResult,
    NewsArticleURL, MediaURL
)

# Import Google News scraper
from media_acquisition.agents.discovery.google_news import GoogleNewsScraper

logger = logging.getLogger(__name__)


class GdeltClient:
    """Client for GDELT Project API."""

    BASE_URL = "https://api.gdeltproject.org/api/v2"
    RATE_LIMIT_DELAY = 5.0  # Seconds between requests (GDELT requirement)

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.last_request_time = 0
        
    def query_events(self,
                    keywords: List[str],
                    date_range: Tuple[str, str],
                    max_records: int = 250) -> pd.DataFrame:
        """
        Query GDELT Event Database.
        
        Args:
            keywords: Search terms
            date_range: (start_date, end_date) as 'YYYY-MM-DD'
            max_records: Maximum records to return (max 250)
            
        Returns:
            DataFrame with events
        """
        import gdelt
        
        g = gdelt.gdelt()
        
        # Format dates for GDELT
        start = datetime.strptime(date_range[0], '%Y-%m-%d')
        end = datetime.strptime(date_range[1], '%Y-%m-%d')
        
        results = []
        
        # Query by date chunks (GDELT works best with specific dates)
        current = start
        while current <= end:
            date_str = current.strftime('%Y %m %d')
            
            try:
                events = g.Search(
                    [date_str],
                    table='events',
                    output='df',
                    coverage=False
                )
                
                if events is not None and len(events) > 0:
                    # Filter for Epstein-related events
                    keyword_str = '|'.join(keywords)
                    mask = (
                        events['Actor1Name'].str.contains(keyword_str, case=False, na=False) |
                        events['Actor2Name'].str.contains(keyword_str, case=False, na=False) |
                        events['Actor1CountryCode'].str.contains(keyword_str, case=False, na=False) |
                        events['Actor2CountryCode'].str.contains(keyword_str, case=False, na=False)
                    )
                    filtered = events[mask]
                    results.append(filtered)
                    
                    logger.info(f"GDELT {date_str}: Found {len(filtered)} events")
                    
            except Exception as e:
                logger.warning(f"GDELT query failed for {date_str}: {e}")
                
            current += pd.Timedelta(days=1)
            
            # Rate limiting
            time.sleep(0.5)
        
        if results:
            return pd.concat(results, ignore_index=True)
        return pd.DataFrame()
    
    def query_gkg(self,
                 keywords: List[str],
                 date_range: Tuple[str, str],
                 max_records: int = 250) -> List[Dict]:
        """
        Query GDELT Global Knowledge Graph for article URLs.
        
        Returns list of article URLs with metadata.
        """
        # Use GDELT Doc API for article discovery
        url = f"{self.BASE_URL}/doc/doc"
        
        articles = []
        
        # Format query
        query = ' OR '.join([f'"{k}"' for k in keywords])
        
        params = {
            'query': query,
            'mode': 'ArtList',
            'maxrecords': min(max_records, 250),
            'format': 'json',
            'startdatetime': date_range[0].replace('-', '') + '000000',
            'enddatetime': date_range[1].replace('-', '') + '235959'
        }
        
        try:
            # Rate limiting - ensure 5 second delay between requests
            elapsed = time.time() - self.last_request_time
            if elapsed < self.RATE_LIMIT_DELAY:
                sleep_time = self.RATE_LIMIT_DELAY - elapsed
                logger.debug(f"GDELT rate limiting: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)

            response = requests.get(url, params=params, timeout=self.timeout)
            self.last_request_time = time.time()

            if response.status_code == 429:
                logger.warning("GDELT rate limit hit (429), waiting 10s and retrying...")
                time.sleep(10)
                response = requests.get(url, params=params, timeout=self.timeout)
                self.last_request_time = time.time()

            response.raise_for_status()
            data = response.json()

            for item in data.get('articles', []):
                articles.append({
                    'url': item.get('url'),
                    'title': item.get('title'),
                    'publish_date': item.get('seendate'),
                    'source_domain': item.get('domain'),
                    'language': item.get('language'),
                    'sentiment': item.get('sentiment'),
                })

        except Exception as e:
            logger.error(f"GDELT GKG query failed: {e}")

        return articles


class WaybackSearcher:
    """Search Wayback Machine for archived news articles."""
    
    CDX_API = "https://web.archive.org/cdx/search/cdx"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        
    def find_snapshots(self,
                      domains: List[str],
                      keywords: List[str],
                      date_range: Tuple[str, str]) -> List[NewsArticleURL]:
        """
        Find Wayback Machine snapshots for news articles.
        
        Args:
            domains: News domains to search (e.g., ['cnn.com', 'nytimes.com'])
            keywords: Keywords to match in URLs
            date_range: (start_date, end_date) as 'YYYY-MM-DD'
            
        Returns:
            List of NewsArticleURL objects
        """
        results = []
        
        for domain in domains:
            try:
                domain_results = self._search_domain(
                    domain, keywords, date_range
                )
                results.extend(domain_results)
                logger.info(f"Wayback {domain}: Found {len(domain_results)} snapshots")
                
            except Exception as e:
                logger.warning(f"Wayback search failed for {domain}: {e}")
                
            # Rate limiting between domains
            time.sleep(self.delay)
        
        return results
    
    def _search_domain(self,
                      domain: str,
                      keywords: List[str],
                      date_range: Tuple[str, str]) -> List[NewsArticleURL]:
        """Search single domain on Wayback using keyword filtering."""

        results = []
        keyword_set = set(k.lower() for k in keywords)

        # Use domain-only search with larger limit, then filter by keyword
        params = {
            'url': f"{domain}/*",
            'output': 'json',
            'from': date_range[0].replace('-', ''),
            'to': date_range[1].replace('-', ''),
            'collapse': 'urlkey',
            'limit': 5000,
            'filter': 'statuscode:200'  # Only successful captures
        }

        try:
            response = self.session.get(
                self.CDX_API,
                params=params,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()

            # Parse CDX response (first row is header)
            if len(data) > 1:
                headers = data[0]
                seen_urls = set()

                for row in data[1:]:
                    entry = dict(zip(headers, row))
                    original_url = entry.get('original', '')

                    # Filter by keyword in URL
                    url_lower = original_url.lower()
                    if not any(k in url_lower for k in keyword_set):
                        continue

                    # Deduplicate URLs
                    if original_url in seen_urls:
                        continue
                    seen_urls.add(original_url)

                    # Build Wayback URL
                    timestamp = entry.get('timestamp', '')
                    wayback_url = f"https://web.archive.org/web/{timestamp}/{original_url}"

                    # Parse date
                    try:
                        snapshot_date = datetime.strptime(timestamp[:8], '%Y%m%d')
                    except:
                        snapshot_date = None

                    results.append(NewsArticleURL(
                        url=original_url,
                        title=None,
                        source_domain=domain,
                        publish_date=snapshot_date,
                        discovery_method='wayback',
                        priority=3,
                        keywords_matched=[k for k in keywords if k.lower() in url_lower],
                        metadata={
                            'wayback_timestamp': timestamp,
                            'wayback_url': wayback_url,
                            'status_code': entry.get('statuscode'),
                            'mimetype': entry.get('mimetype')
                        }
                    ))

        except Exception as e:
            logger.debug(f"Wayback domain search failed for {domain}: {e}")

        return results


class RSSCrawler:
    """Crawl historical RSS feeds for article discovery."""
    
    HISTORICAL_FEEDS = {
        # Mainstream US
        'cnn': 'http://rss.cnn.com/rss/cnn_topstories.rss',
        'cnn_world': 'http://rss.cnn.com/rss/cnn_world.rss',
        'cnn_us': 'http://rss.cnn.com/rss/cnn_us.rss',
        'nyt': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'nyt_world': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
        'nyt_us': 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
        'nyt_ny': 'https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml',
        'wapo': 'http://feeds.washingtonpost.com/rss/national',
        'wapo_world': 'http://feeds.washingtonpost.com/rss/world',
        'wapo_politics': 'http://feeds.washingtonpost.com/rss/politics',
        'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
        'bbc_world': 'http://feeds.bbci.co.uk/news/world/rss.xml',
        'bbc_us': 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
        'guardian': 'https://www.theguardian.com/us/rss',
        'guardian_world': 'https://www.theguardian.com/world/rss',
        'guardian_us': 'https://www.theguardian.com/us-news/rss',
        'reuters': 'https://www.reutersagency.com/feed/?best-topics=business-finance',
        'reuters_world': 'https://www.reuters.com/rssFeed/worldNews',
        'reuters_us': 'https://www.reuters.com/rssFeed/domesticNews',
        'ap': 'https://apnews.com/hub/rss',
        'ap_top': 'https://apnews.com/rss/apf-topnews',
        'ap_us': 'https://apnews.com/rss/apf-usnews',
        
        # Business
        'wsj': 'https://feeds.a.dj.com/rss/RSSWSJD.xml',
        'bloomberg': 'https://www.bloomberg.com/feed',
        'forbes': 'https://www.forbes.com/most-popular/feed/',
        'ft': 'https://www.ft.com/rss/home/world',
        'cnbc': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        
        # Investigative
        'propublica': 'https://www.propublica.org/feeds/articles',
        'buzzfeed_news': 'https://www.buzzfeednews.com/feed',
        'miami_herald': 'https://www.miamiherald.com/news/?widgetName=rssfeed&widgetContentId=712097',
        'miami_nt': 'https://www.miaminewtimes.com/news/rss',
        
        # Legal
        'law360': 'https://www.law360.com/newswire/rss',
        'above_law': 'https://abovethelaw.com/feed/',
        'scotusblog': 'https://www.scotusblog.com/feed/',
        
        # Tabloids (for breaking news)
        'nypost': 'https://nypost.com/feed/',
        'dailymail': 'https://www.dailymail.co.uk/news/index.rss',
        'sun': 'https://www.thesun.co.uk/news/?rss',
        
        # International
        'le_monde': 'https://www.lemonde.fr/rss/une.xml',
        'der_spiegel': 'https://www.spiegel.de/international/index.rss',
        'el_pais': 'https://feeds.elpais.com/mrss/epaper/epage/portada',
        'sydney_morning_herald': 'https://www.smh.com.au/rss/world.xml',
        'the_globe_and_mail': 'https://www.theglobeandmail.com/rss/world/',
        
        # Tech
        'techcrunch': 'https://techcrunch.com/feed/',
        'the_verge': 'https://www.theverge.com/rss/index.xml',
        'wired': 'https://www.wired.com/feed/',
        
        # Politics
        'politico': 'https://www.politico.com/rss/politics-news.xml',
        'the_hill': 'http://thehill.com/rss/feed/',
        'roll_call': 'https://www.rollcall.com/rss/',
        
        # Opinion/Analysis
        'the_atlantic': 'https://www.theatlantic.com/feed/',
        'vox': 'https://www.vox.com/rss/index.xml',
        'slate': 'https://slate.com/news-and-politics/rss.xml',
        
        # Local
        'palm_beach_post': 'https://www.palmbeachpost.com/news/?widgetName=rssfeed&widgetContentId=712097',
        'santa_fe_new_mexican': 'https://www.santafenewmexican.com/news?widgetName=rssfeed&widgetContentId=712097',
    }
    
    def __init__(self):
        self.session = requests.Session()
        
    def discover(self,
                feeds: List[str],
                keywords: List[str],
                date_range: Tuple[str, str]) -> List[NewsArticleURL]:
        """
        Crawl RSS feeds and filter for Epstein-related articles.
        
        Args:
            feeds: RSS feed URLs
            keywords: Keywords to match
            date_range: (start_date, end_date)
            
        Returns:
            List of NewsArticleURL objects
        """
        results = []
        keyword_set = set(k.lower() for k in keywords)
        
        start_date = datetime.strptime(date_range[0], '%Y-%m-%d')
        end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
        
        logger.info(f"Starting RSS discovery for {len(feeds)} feeds")
        
        for i, feed_url in enumerate(feeds, 1):
            logger.info(f"[{i}/{len(feeds)}] Checking RSS feed: {feed_url[:60]}...")
            try:
                # Fetch feed content with timeout to avoid hanging
                response = self.session.get(feed_url, timeout=15)
                response.raise_for_status()
                
                # Parse feed content
                parsed = feedparser.parse(response.content)
                
                logger.info(f"  Found {len(parsed.entries)} entries in feed")
                
                matched_count = 0
                for entry in parsed.entries:
                    # Check if article matches keywords
                    title = entry.get('title', '').lower()
                    summary = entry.get('summary', '').lower()
                    
                    if any(k in title or k in summary for k in keyword_set):
                        # Parse date
                        published = entry.get('published_parsed')
                        if published:
                            pub_date = datetime(*published[:6])
                        else:
                            pub_date = None
                        
                        # Check date range (allow articles within window)
                        # Note: RSS feeds only have recent articles, so be flexible
                        if pub_date and pub_date < start_date:
                            continue
                        
                        # Extract domain
                        link = entry.get('link', '')
                        domain = urlparse(link).netloc
                        
                        results.append(NewsArticleURL(
                            url=link,
                            title=entry.get('title'),
                            source_domain=domain,
                            publish_date=pub_date,
                            discovery_method='rss',
                            priority=2,
                            keywords_matched=[k for k in keywords if k in title or k in summary],
                            metadata={
                                'rss_feed': feed_url,
                                'summary': entry.get('summary', '')[:500]
                            }
                        ))
                        matched_count += 1
                
                if matched_count > 0:
                    logger.info(f"  ✓ Matched {matched_count} articles from this feed")
                        
            except Exception as e:
                logger.warning(f"  ✗ RSS crawl failed for {feed_url}: {e}")
        
        logger.info(f"RSS discovery complete: {len(results)} total articles found")
        return results


class NewsDiscoveryAgent(DiscoveryAgent):
    """
    Agent for discovering Epstein-related news articles.
    
    Uses multiple sources:
    1. GDELT Project (bulk historical data)
    2. Wayback Machine (archived articles)
    3. RSS feeds (recent articles)
    """
    
    AGENT_ID = 'news-discovery-v2'
    VERSION = '2.0.0'
    
    DEFAULT_KEYWORDS = [
        # Primary names
        'Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre',
        'Virginia Roberts', 'Sarah Ransome', 'Maria Farmer', 'Annie Farmer',
        
        # Case references
        'Epstein case', 'Epstein investigation', 'Epstein trial',
        'Epstein indictment', 'Epstein plea deal', 'Acosta Epstein',
        'SDNY Epstein', 'Southern District Epstein',
        
        # Locations
        'Little Saint James', 'Epstein Island', 'Great St James',
        'Palm Beach Epstein', 'Manhattan Epstein', 'Zorro Ranch',
        'New Mexico Epstein', 'US Virgin Islands Epstein',
        
        # Organizations
        'Mossack Fonseca Epstein', 'Epstein VI', 'Southern Trust',
        'Gratitude America', 'J Epstein & Co', 'Epstein Foundation',
        'Epstein Associates',
        
        # Legal terms
        'sex trafficking Epstein', 'sex offender Epstein',
        'non-prosecution agreement Epstein', 'Epstein plea',
        'civil lawsuit Epstein', 'Epstein criminal case',
        
        # Associated figures
        'Trump Epstein', 'Clinton Epstein', 'Prince Andrew Epstein',
        'Alan Dershowitz Epstein', 'Bill Gates Epstein',
        'Leslie Wexner Epstein', 'Leon Black Epstein',
        'Alexander Acosta', 'Cy Vance', 'Barry Krischer',
        
        # Jane Does
        'Jane Doe Epstein', 'Epstein victim', 'Epstein accuser',
        
        # Related topics
        'Lolita Express', 'Epstein flight logs', 'Epstein black book',
        'Epstein client list', 'Epstein associates',
        'Epstein network', 'Epstein conspiracy',
        
        # Document types
        'Epstein court documents', 'Epstein court filings',
        'Epstein deposition', 'Epstein lawsuit',
        
        # Case numbers
        '1:08-cr-00808', '1:15-cv-07433', 'Epstein docket',
        
        # Aftermath
        'Epstein death', 'Epstein autopsy', 'Epstein jail death',
        'Epstein documentary', 'Epstein investigation aftermath',
        
        # Financial
        'Epstein finances', 'Epstein money laundering',
        'Epstein tax evasion', 'Epstein offshore accounts',
        
        # International
        'Epstein France', 'Epstein UK', 'Epstein Caribbean',
    ]
    
    DEFAULT_SOURCES = [
        'cnn.com',
        'nytimes.com',
        'washingtonpost.com',
        'bbc.com',
        'theguardian.com',
        'reuters.com',
        'apnews.com',
        'foxnews.com',
        'wsj.com',
        'miamiherald.com',
        'vanityfair.com',
        'newyorker.com',
        'usatoday.com',
        'nbcnews.com',
        'abcnews.go.com',
        'cbsnews.com',
        'latimes.com',
        'chicagotribune.com',
        'bostonglobe.com',
        'politico.com',
        'thehill.com',
        'axios.com',
        'vox.com',
        'slate.com',
        'salon.com',
        'huffpost.com',
        'buzzfeednews.com',
        'dailybeast.com',
        'theatlantic.com',
        'newrepublic.com',
        'reason.com',
        'nationalreview.com'
    ]
    
    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config)

        # Initialize clients
        self.google_news = GoogleNewsScraper(delay=2.0)  # Primary source
        self.gdelt = GdeltClient(timeout=self.config.request_timeout)  # Secondary
        self.wayback = WaybackSearcher(delay=1.0)  # Disabled by default (too slow)
        self.rss = RSSCrawler()  # For recent articles only
        
    def _validate_config(self):
        """Validate agent configuration."""
        if not self.config:
            raise ValueError("Config required")
    
    def _initialize_resources(self):
        """Initialize resources."""
        logger.info(f"NewsDiscoveryAgent initialized with {len(self.DEFAULT_KEYWORDS)} keywords")
    
    async def search(self,
                    keywords: List[str] = None,
                    date_range: Tuple[str, str] = None,
                    sources: List[str] = None,
                    max_results: int = 10000,
                    **kwargs) -> List[NewsArticleURL]:
        """
        Search for news articles across all discovery sources.
        
        Args:
            keywords: Search terms (default: Epstein-related keywords)
            date_range: (start_date, end_date) as 'YYYY-MM-DD'
            sources: Specific news domains or None for defaults
            max_results: Maximum articles to discover
            
        Returns:
            List of NewsArticleURL objects
        """
        keywords = keywords or self.DEFAULT_KEYWORDS
        date_range = date_range or ('1990-01-01', '2025-12-31')
        sources = sources or self.DEFAULT_SOURCES
        
        all_results = []

        # 1. Google News Discovery (PRIMARY - fast, no limits, good coverage)
        logger.info(f"Starting Google News discovery for {len(keywords)} keywords")
        try:
            google_articles = await self._search_google_news(
                keywords, date_range, max_results=max_results
            )
            all_results.extend(google_articles)
            logger.info(f"Google News discovery complete: {len(google_articles)} articles")
        except Exception as e:
            logger.error(f"Google News discovery failed: {e}")

        # 2. GDELT Discovery (SECONDARY - historical, rate limited)
        # Only run if we need more articles and have quota
        if len(all_results) < max_results:
            logger.info(f"Starting GDELT discovery for {len(keywords)} keywords")
            try:
                gdelt_articles = await self._search_gdelt(
                    keywords, date_range, max_records=min(250, max_results - len(all_results))
                )
                all_results.extend(gdelt_articles)
                logger.info(f"GDELT discovery complete: {len(gdelt_articles)} articles")
            except Exception as e:
                logger.error(f"GDELT discovery failed: {e}")

        # 3. Wayback Machine Discovery (DISABLED - too slow, use only if explicitly enabled)
        # Skip by default due to timeout issues
        # logger.info(f"Starting Wayback discovery for {len(sources)} sources")
        # try:
        #     wayback_articles = await self._search_wayback(
        #         sources, keywords, date_range
        #     )
        #     all_results.extend(wayback_articles)
        #     logger.info(f"Wayback discovery complete: {len(wayback_articles)} articles")
        # except Exception as e:
        #     logger.error(f"Wayback discovery failed: {e}")

        # 4. RSS Feed Discovery (for very recent articles not yet indexed)
        # Only if date range includes recent dates
        end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
        if end_date.year >= datetime.now().year - 1:
            logger.info("Starting RSS discovery")
            try:
                rss_articles = await self._search_rss(
                    keywords, date_range
                )
                all_results.extend(rss_articles)
                logger.info(f"RSS discovery complete: {len(rss_articles)} articles")
            except Exception as e:
                logger.error(f"RSS discovery failed: {e}")
        
        # Deduplicate results
        deduplicated = self._deduplicate_results(all_results)
        
        # Limit results
        if len(deduplicated) > max_results:
            logger.info(f"Limiting results from {len(deduplicated)} to {max_results}")
            deduplicated = deduplicated[:max_results]
        
        self.metrics['total_discovered'] = len(all_results)
        self.metrics['unique_articles'] = len(deduplicated)
        self.metrics['sources_breakdown'] = {
            'google_news': len([a for a in all_results if a.discovery_method == 'google_news']),
            'gdelt': len([a for a in all_results if a.discovery_method == 'gdelt']),
            'wayback': len([a for a in all_results if a.discovery_method == 'wayback']),
            'rss': len([a for a in all_results if a.discovery_method == 'rss'])
        }
        
        return deduplicated
    
    async def _search_gdelt(self,
                           keywords: List[str],
                           date_range: Tuple[str, str],
                           max_records: int) -> List[NewsArticleURL]:
        """Search GDELT for articles."""
        # Run in thread pool to not block
        loop = asyncio.get_event_loop()
        
        # Try GKG (Global Knowledge Graph) for article URLs
        articles = await loop.run_in_executor(
            None,
            lambda: self.gdelt.query_gkg(keywords, date_range, max_records)
        )
        
        results = []
        for article in articles:
            # Parse GDELT date format (YYYYMMDD HHMMSS)
            date_str = article.get('publish_date', '')
            try:
                if len(date_str) >= 8:
                    pub_date = datetime.strptime(date_str[:8], '%Y%m%d')
                else:
                    pub_date = None
            except:
                pub_date = None
            
            results.append(NewsArticleURL(
                url=article['url'],
                title=article.get('title'),
                source_domain=article.get('source_domain'),
                publish_date=pub_date,
                discovery_method='gdelt',
                priority=1,  # High priority - direct source
                metadata={
                    'sentiment': article.get('sentiment'),
                    'language': article.get('language')
                }
            ))
        
        return results

    async def _search_google_news(self,
                                   keywords: List[str],
                                   date_range: Tuple[str, str],
                                   max_results: int) -> List[NewsArticleURL]:
        """Search Google News for articles."""
        loop = asyncio.get_event_loop()

        result = await loop.run_in_executor(
            None,
            lambda: self.google_news.search(keywords, date_range, max_results)
        )

        # Extract articles from TaskResult
        articles = result.output if result.output else []
        return articles if isinstance(articles, list) else []

    async def _search_wayback(self,
                             sources: List[str],
                             keywords: List[str],
                             date_range: Tuple[str, str]) -> List[NewsArticleURL]:
        """Search Wayback Machine for articles."""
        loop = asyncio.get_event_loop()
        
        results = await loop.run_in_executor(
            None,
            lambda: self.wayback.find_snapshots(sources, keywords, date_range)
        )
        
        return results
    
    async def _search_rss(self,
                         keywords: List[str],
                         date_range: Tuple[str, str]) -> List[NewsArticleURL]:
        """Search RSS feeds for articles."""
        # Get feed URLs from historical feeds
        feeds = list(RSSCrawler.HISTORICAL_FEEDS.values())
        
        loop = asyncio.get_event_loop()
        
        results = await loop.run_in_executor(
            None,
            lambda: self.rss.discover(feeds, keywords, date_range)
        )
        
        return results
    
    def _deduplicate_results(self, results: List[NewsArticleURL]) -> List[NewsArticleURL]:
        """Remove duplicate URLs."""
        seen = set()
        unique = []
        
        for result in results:
            # Normalize URL
            url = result.url.lower().rstrip('/')
            
            if url not in seen:
                seen.add(url)
                unique.append(result)
        
        return unique
    
    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute discovery task."""
        keywords = task.get("keywords", self.DEFAULT_KEYWORDS)
        date_range = task.get("date_range", ('1990-01-01', '2025-12-31'))
        sources = task.get("sources", self.DEFAULT_SOURCES)
        max_results = task.get("max_results", 10000)
        
        try:
            results = await self.search(
                keywords=keywords,
                date_range=date_range,
                sources=sources,
                max_results=max_results
            )
            
            return TaskResult(
                status="success",
                output=results,
                metrics=self.metrics
            )
            
        except Exception as e:
            return TaskResult(
                status="failure",
                error=str(e),
                retry_allowed=self._should_retry(e)
            )


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='News Discovery Agent')
    parser.add_argument('--keywords', nargs='+', default=NewsDiscoveryAgent.DEFAULT_KEYWORDS[:3])
    parser.add_argument('--start-date', default='2024-01-01')
    parser.add_argument('--end-date', default='2024-01-31')
    parser.add_argument('--max-results', type=int, default=100)
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create agent
    agent = NewsDiscoveryAgent()
    
    # Run discovery
    async def main():
        results = await agent.search(
            keywords=args.keywords,
            date_range=(args.start_date, args.end_date),
            max_results=args.max_results
        )
        
        print(f"\nDiscovered {len(results)} articles:")
        for i, article in enumerate(results[:10], 1):
            print(f"{i}. {article.title or 'N/A'}")
            print(f"   URL: {article.url}")
            print(f"   Date: {article.publish_date}")
            print(f"   Source: {article.discovery_method}")
            print()
    
    asyncio.run(main())
