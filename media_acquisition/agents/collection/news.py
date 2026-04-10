"""
News Collector Agent
Downloads and processes news articles using newspaper3k.
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Import base classes
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from media_acquisition.base import (
    CollectionAgent, AgentConfig, TaskResult,
    NewsArticleURL, StorageManager
)

logger = logging.getLogger(__name__)


class ArticleDownloader:
    """Download and extract article content using newspaper3k."""
    
    def __init__(self, storage_path: str = '/home/cbwinslow/workspace/epstein-data/media/articles/'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Cache for already downloaded articles
        self.downloaded_cache = set()
    
    def download_article(self, article_url: NewsArticleURL, use_wayback: bool = True) -> Optional[Dict[str, Any]]:
        """
        Download and extract article content.
        
        Args:
            article_url: NewsArticleURL with metadata
            use_wayback: Try Wayback Machine if direct download fails
            
        Returns:
            Dict with article content or None if failed
        """
        url = article_url.url
        
        # Check cache
        if url in self.downloaded_cache:
            logger.info(f"Skipping already downloaded: {url}")
            return None
        
        # Try direct download first
        result = self._download_with_newspaper(url, article_url)
        
        # If failed and Wayback URL available, try that
        if not result and use_wayback and article_url.metadata and article_url.metadata.get('wayback_url'):
            wayback_url = article_url.metadata['wayback_url']
            logger.info(f"Trying Wayback URL: {wayback_url}")
            result = self._download_with_newspaper(wayback_url, article_url, is_wayback=True)
        
        # If still failed, try with requests + BeautifulSoup fallback
        if not result:
            result = self._download_with_requests(url, article_url)
        
        if result:
            self.downloaded_cache.add(url)
        
        return result
    
    def _download_with_newspaper(self, url: str, article_url: NewsArticleURL, is_wayback: bool = False) -> Optional[Dict[str, Any]]:
        """Download using newspaper3k library."""
        try:
            from newspaper import Article, Config
            
            # Configure newspaper
            config = Config()
            config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            config.request_timeout = 30
            config.memoize_articles = False  # Don't cache
            
            article = Article(url, config=config)
            article.download()
            
            # Check if download succeeded
            if not article.html:
                logger.warning(f"No HTML content for: {url}")
                return None
            
            # Parse article
            article.parse()
            
            # Extract metadata
            result = {
                'url': article_url.url,
                'title': article.title or article_url.title,
                'authors': article.authors or [],
                'publish_date': article.publish_date,
                'content': article.text,
                'summary': article.summary,
                'keywords': article.keywords or [],
                'top_image': article.top_image,
                'movies': article.movies,
                'html': article.html[:10000] if article.html else None,  # Store partial HTML
                'is_wayback': is_wayback,
                'extraction_method': 'newspaper3k',
                'extraction_success': True,
                'word_count': len(article.text.split()) if article.text else 0,
                'discovered_at': datetime.now().isoformat(),
                'keywords_matched': article_url.keywords_matched or [],
                'discovery_method': article_url.discovery_method
            }
            
            logger.info(f"Downloaded: {result['title'][:60]} ({result['word_count']} words)")
            return result
            
        except Exception as e:
            logger.warning(f"newspaper3k failed for {url}: {e}")
            return None
    
    def _download_with_requests(self, url: str, article_url: NewsArticleURL) -> Optional[Dict[str, Any]]:
        """Fallback download using requests + BeautifulSoup."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else article_url.title
            
            # Extract article content (try common article containers)
            content_selectors = [
                'article',
                '[role="main"]',
                '.article-content',
                '.article-body',
                '.story-content',
                '.post-content',
                'main',
                '#content'
            ]
            
            content = ''
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    # Remove script and style elements
                    for script in element.find_all(['script', 'style']):
                        script.decompose()
                    content = element.get_text(separator='\n', strip=True)
                    if len(content) > 500:  # Minimum content length
                        break
            
            # If no content found, use body
            if not content:
                body = soup.find('body')
                if body:
                    for script in body.find_all(['script', 'style']):
                        script.decompose()
                    content = body.get_text(separator='\n', strip=True)
            
            # Extract authors (try meta tags)
            authors = []
            author_meta = soup.find('meta', attrs={'name': 'author'})
            if author_meta:
                authors = [author_meta.get('content', '')]
            
            # Extract publish date
            publish_date = None
            date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
            if date_meta:
                try:
                    publish_date = datetime.fromisoformat(date_meta.get('content', '').replace('Z', '+00:00'))
                except:
                    pass
            
            result = {
                'url': article_url.url,
                'title': title_text,
                'authors': authors,
                'publish_date': publish_date,
                'content': content,
                'summary': content[:500] if content else '',
                'keywords': [],
                'top_image': None,
                'movies': [],
                'html': None,
                'is_wayback': False,
                'extraction_method': 'requests+bs4',
                'extraction_success': len(content) > 100,
                'word_count': len(content.split()) if content else 0,
                'discovered_at': datetime.now().isoformat(),
                'keywords_matched': article_url.keywords_matched or [],
                'discovery_method': article_url.discovery_method
            }
            
            logger.info(f"Downloaded (fallback): {result['title'][:60]} ({result['word_count']} words)")
            return result
            
        except Exception as e:
            logger.error(f"Fallback download failed for {url}: {e}")
            return None
    
    def save_article(self, article_data: Dict[str, Any], article_id: int) -> str:
        """Save article content to file."""
        # Create filename from ID
        filename = f"article_{article_id:08d}.json"
        filepath = self.storage_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, indent=2, default=str)
        
        return str(filepath)


class NewsCollector(CollectionAgent):
    """
    Agent for collecting news articles.
    
    Uses newspaper3k for extraction with fallback to requests+BeautifulSoup.
    Supports Wayback Machine archives for articles no longer available.
    """
    
    AGENT_ID = 'news-collector-v2'
    VERSION = '2.0.0'
    
    def __init__(self, config: Optional[AgentConfig] = None, storage: Optional[StorageManager] = None):
        super().__init__(config, storage)

        self.downloader = ArticleDownloader(
            storage_path='/home/cbwinslow/workspace/epstein-data/media/articles/'
        )

        # Initialize metrics
        self.metrics = {
            'items_collected': 0,
            'errors': 0,
            'sources_breakdown': {}
        }
    
    def _validate_config(self):
        """Validate agent configuration."""
        pass
    
    async def process_article(self, article: NewsArticleURL) -> Optional[Dict[str, Any]]:
        """
        Process a single article - alias for collect() with standardized return format.
        
        Args:
            article: NewsArticleURL with URL and metadata
            
        Returns:
            Dict with article data and success status
        """
        try:
            result = await self.collect(article)
            if result:
                return {
                    'success': True,
                    'url': result.get('url'),
                    'title': result.get('title'),
                    'stored_id': result.get('stored_id'),
                    'word_count': result.get('word_count', 0),
                    'extraction_method': result.get('extraction_method')
                }
            else:
                return {
                    'success': False,
                    'url': article.url,
                    'error': 'Failed to download or process article'
                }
        except Exception as e:
            logger.error(f"process_article failed: {e}")
            return {
                'success': False,
                'url': article.url,
                'error': str(e)
            }
    
    async def collect(self, article: NewsArticleURL) -> Optional[Dict[str, Any]]:
        """
        Collect a single news article.
        
        Args:
            article: NewsArticleURL with URL and metadata
            
        Returns:
            Dict with article data and storage info
        """
        logger.info(f"Collecting article: {article.url}")
        
        # Download article
        article_data = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.downloader.download_article(article, use_wayback=True)
        )
        
        if not article_data:
            logger.warning(f"Failed to download: {article.url}")
            return None
        
        # Store in database
        if self.storage:
            try:
                import json
                logger.debug("article_data keys: %s", list(article_data.keys()) if article_data else None)
                logger.debug("article_data url: %s", article_data.get('url') if article_data else None)
                logger.debug("article.url: %s", article.url)
                article_dict = {
                    'source_domain': urlparse(article_data.get('url', article.url)).netloc,
                    'source_name': urlparse(article_data.get('url', article.url)).netloc,
                    'source_url': article_data.get('url', article.url),
                    'wayback_url': article_data.get('wayback_url'),
                    'title': article_data.get('title'),
                    'authors': article_data.get('authors', []),
                    'publish_date': article_data.get('publish_date'),
                    'content': article_data.get('content'),
                    'summary': article_data.get('summary'),
                    'keywords': article_data.get('keywords', []),
                    'sentiment_score': None,
                    'entities_mentioned': json.dumps({}),
                    'related_person_ids': [],
                    'collection_method': 'newspaper3k' if article_data.get('extraction_method') == 'newspaper3k' else 'requests'
                }
                logger.debug("article_dict source_url: %s", article_dict['source_url'])
                article_id = self.storage.store_article(article_dict)
                
                article_data['stored_id'] = article_id
                
                # Save to file
                filepath = self.downloader.save_article(article_data, article_id)
                article_data['filepath'] = filepath
                
            except Exception as e:
                logger.error(f"Failed to store article: {e}")
        
        # Update metrics
        if article_data.get('extraction_success'):
            self.metrics['items_collected'] += 1
        else:
            self.metrics['errors'] += 1
        
        return article_data
    
    async def process_queue(self, batch_size: int = 50) -> List[Dict[str, Any]]:
        """
        Process a batch of articles from the queue.
        
        Args:
            batch_size: Number of articles to process
            
        Returns:
            List of collection results
        """
        if not self.storage:
            raise ValueError("Storage manager required for queue processing")
        
        # Get pending items
        items = self.storage.get_queued_items(
            media_type='news',
            status='pending',
            limit=batch_size
        )
        
        results = []
        
        for item in items:
            try:
                # Mark as processing
                self.storage.update_queue_status(item['id'], 'processing')
                
                # Create NewsArticleURL
                metadata = item.get('metadata', {})
                article = NewsArticleURL(
                    url=item['source_url'],
                    title=metadata.get('title'),
                    source_domain=metadata.get('source_domain'),
                    priority=item['priority'],
                    keywords_matched=item['keywords_matched'] or [],
                    discovery_method=metadata.get('discovery_method', 'unknown')
                )
                
                # Collect
                result = await self.collect(article)
                
                # Update queue
                if result and result.get('stored_id'):
                    self.storage.update_queue_status(
                        item['id'],
                        'completed',
                        result_id=result['stored_id']
                    )
                    results.append(result)
                else:
                    self.storage.update_queue_status(
                        item['id'],
                        'failed',
                        error_message='Failed to collect article'
                    )
                    self.metrics['errors'] += 1
                
                # Rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to process queue item {item['id']}: {e}")
                self.storage.update_queue_status(
                    item['id'],
                    'failed',
                    error_message=str(e)[:500]
                )
                self.metrics['errors'] += 1
        
        return results
    
    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute collection task."""
        articles = task.get("articles", [])
        
        if not articles:
            return TaskResult(
                status="failure",
                error="No articles provided"
            )
        
        results = []
        
        for article_data in articles:
            try:
                article = NewsArticleURL(**article_data)
                result = await self.collect(article)
                if result:
                    results.append(result)
            except Exception as e:
                logger.error(f"Failed to collect article: {e}")
                self.metrics['errors'] += 1
        
        success_count = len(results)
        
        return TaskResult(
            status="success" if success_count > 0 else "failure",
            output=results,
            metrics=self.metrics
        )


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='News Collector Agent')
    parser.add_argument('url', help='Article URL to download')
    parser.add_argument('--wayback-url', help='Wayback Machine URL if available')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create agent
    agent = NewsCollector()
    
    # Create article
    article = NewsArticleURL(
        url=args.url,
        metadata={'wayback_url': args.wayback_url} if args.wayback_url else {}
    )
    
    # Collect
    print(f"Downloading: {args.url}")
    print("-" * 60)
    
    result = asyncio.run(agent.collect(article))
    
    if result:
        print(f"\n✅ SUCCESS!")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Authors: {', '.join(result.get('authors', []))}")
        print(f"Word Count: {result.get('word_count', 0)}")
        print(f"Extraction Method: {result.get('extraction_method')}")
        print(f"\nFirst 500 characters:")
        print(result.get('content', 'N/A')[:500])
    else:
        print("\n❌ FAILED: Could not download article")
