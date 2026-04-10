#!/usr/bin/env python3
"""
Media Acquisition Runner for Epstein Research
Starts news discovery, video discovery, and document collection.
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.agents.discovery.video import VideoDiscoveryAgent
from media_acquisition.agents.discovery.document import DocumentDiscoveryAgent
from media_acquisition.agents.collection.news import NewsCollector
from media_acquisition.base import StorageManager, AgentConfig

# Setup logging
log_dir = Path('/home/cbwinslow/workspace/epstein/logs')
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_dir / f'media_acquisition_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'
MEDIA_BASE_PATH = '/home/cbwinslow/workspace/epstein-data/media'

# Epstein-related keywords
EPSTEIN_KEYWORDS = [
    'Jeffrey Epstein',
    'Epstein',
    'Ghislaine Maxwell',
    'Virginia Giuffre',
    'Epstein Island',
    'Little Saint James',
    'Epstein victims',
    'Epstein trial',
    'Epstein files',
    'Epstein release',
    'Epstein documents',
    'Epstein case',
    'sex trafficking Epstein',
    'Epstein flight logs',
    'Epstein black book',
    'Epstein associates'
]


class MediaAcquisitionRunner:
    """Runner for media acquisition pipeline."""
    
    def __init__(self):
        self.storage = None
        self.config = None
        self.results = {
            'news_discovered': 0,
            'news_queued': 0,
            'news_collected': 0,
            'videos_discovered': 0,
            'documents_discovered': 0,
            'errors': []
        }
    
    async def initialize(self):
        """Initialize storage and configuration."""
        logger.info("Initializing Media Acquisition Pipeline...")
        
        self.storage = StorageManager(
            connection_string=DATABASE_URL,
            base_path=MEDIA_BASE_PATH
        )
        
        self.config = AgentConfig(
            agent_id='epstein-media-acquisition',
            # Add API keys here if available
            youtube_api_key=None,
            newsapi_key=None
        )
        
        # Ensure media directory exists
        Path(MEDIA_BASE_PATH).mkdir(parents=True, exist_ok=True)
        
        logger.info("✓ Storage initialized")
        logger.info(f"  Database: {DATABASE_URL}")
        logger.info(f"  Media path: {MEDIA_BASE_PATH}")
    
    async def discover_news(self, max_results=50):
        """Discover news articles about Epstein."""
        logger.info("\n" + "="*60)
        logger.info("PHASE 1: News Discovery (GDELT)")
        logger.info("="*60)
        
        agent = NewsDiscoveryAgent(self.config)
        
        # Search for articles from last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        for keyword in EPSTEIN_KEYWORDS[:5]:  # Start with top 5 keywords
            try:
                logger.info(f"\nSearching for: '{keyword}'")
                
                articles = await agent.search(
                    keywords=[keyword],
                    date_range=(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),
                    max_results=max_results
                )
                
                logger.info(f"  Found {len(articles)} articles")
                self.results['news_discovered'] += len(articles)
                
                # Queue articles for collection
                for article in articles:
                    try:
                        queue_id = self.storage.add_to_queue(
                            media_type='news',
                            source_url=article.url,
                            priority=article.priority,
                            keywords_matched=article.keywords_matched,
                            discovered_by='news-discovery-agent',
                            metadata={
                                'title': article.title,
                                'source_domain': article.source_domain,
                                'publish_date': article.publish_date.isoformat() if article.publish_date else None
                            }
                        )
                        
                        if queue_id:
                            self.results['news_queued'] += 1
                            
                    except Exception as e:
                        logger.warning(f"  Failed to queue {article.url}: {e}")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                error_msg = f"News discovery failed for '{keyword}': {e}"
                logger.error(error_msg)
                self.results['errors'].append(error_msg)
        
        logger.info(f"\n✓ News discovery complete: {self.results['news_discovered']} discovered, {self.results['news_queued']} queued")
    
    async def collect_news(self, batch_size=10):
        """Collect news articles from queue."""
        logger.info("\n" + "="*60)
        logger.info("PHASE 2: News Collection")
        logger.info("="*60)
        
        collector = NewsCollector(self.config, self.storage)
        
        # Get pending items from queue
        queue_items = self.storage.get_queued_items(
            media_type='news',
            status='pending',
            limit=batch_size
        )
        
        logger.info(f"Processing {len(queue_items)} articles from queue...")
        
        for item in queue_items:
            try:
                from media_acquisition.base import NewsArticleURL
                
                article = NewsArticleURL(
                    url=item['source_url'],
                    title=item['metadata'].get('title', 'Unknown'),
                    source_domain=item['metadata'].get('source_domain', 'unknown'),
                    priority=item['priority'],
                    keywords_matched=item['keywords_matched'],
                    discovery_method='queue'
                )
                
                result = await collector.process_article(article)
                
                if result.get('success'):
                    self.results['news_collected'] += 1
                    logger.info(f"  ✓ Collected: {result.get('title', 'Unknown')[:60]}...")
                else:
                    logger.warning(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
                
                # Small delay between articles
                await asyncio.sleep(0.5)
                
            except Exception as e:
                error_msg = f"Failed to collect article {item.get('source_url')}: {e}"
                logger.error(error_msg)
                self.results['errors'].append(error_msg)
        
        logger.info(f"\n✓ News collection complete: {self.results['news_collected']} articles collected")
    
    async def discover_videos(self, max_results=20):
        """Discover videos about Epstein."""
        logger.info("\n" + "="*60)
        logger.info("PHASE 3: Video Discovery")
        logger.info("="*60)
        
        agent = VideoDiscoveryAgent(self.config)
        
        for keyword in EPSTEIN_KEYWORDS[:3]:  # Start with top 3 keywords
            try:
                logger.info(f"\nSearching YouTube for: '{keyword}'")
                
                videos = await agent.search(
                    keywords=[keyword],
                    max_results=max_results
                )
                
                logger.info(f"  Found {len(videos)} videos")
                self.results['videos_discovered'] += len(videos)
                
                # Queue videos for collection
                for video in videos:
                    try:
                        self.storage.add_to_queue(
                            media_type='video',
                            source_url=video.url,
                            priority=video.priority,
                            keywords_matched=video.keywords_matched,
                            discovered_by='video-discovery-agent',
                            metadata={
                                'title': video.title,
                                'platform': video.platform,
                                'duration_seconds': getattr(video, 'duration_seconds', None),
                                'view_count': getattr(video, 'view_count', None)
                            }
                        )
                    except Exception as e:
                        logger.warning(f"  Failed to queue video {video.url}: {e}")
                
                await asyncio.sleep(1)
                
            except Exception as e:
                error_msg = f"Video discovery failed for '{keyword}': {e}"
                logger.error(error_msg)
                self.results['errors'].append(error_msg)
        
        logger.info(f"\n✓ Video discovery complete: {self.results['videos_discovered']} videos discovered")
    
    async def discover_documents(self, max_results=20):
        """Discover documents about Epstein."""
        logger.info("\n" + "="*60)
        logger.info("PHASE 4: Document Discovery")
        logger.info("="*60)
        
        agent = DocumentDiscoveryAgent(self.config)
        
        for keyword in EPSTEIN_KEYWORDS[:3]:
            try:
                logger.info(f"\nSearching for documents: '{keyword}'")
                
                documents = await agent.search(
                    keywords=[keyword],
                    max_results=max_results
                )
                
                logger.info(f"  Found {len(documents)} documents")
                self.results['documents_discovered'] += len(documents)
                
                # Queue documents for collection
                for doc in documents:
                    try:
                        self.storage.add_to_queue(
                            media_type='document',
                            source_url=doc.url,
                            priority=doc.priority,
                            keywords_matched=doc.keywords_matched,
                            discovered_by='document-discovery-agent',
                            metadata={
                                'title': doc.title,
                                'doc_type': getattr(doc, 'doc_type', 'unknown'),
                                'source_domain': doc.source_domain
                            }
                        )
                    except Exception as e:
                        logger.warning(f"  Failed to queue document {doc.url}: {e}")
                
                await asyncio.sleep(1)
                
            except Exception as e:
                error_msg = f"Document discovery failed for '{keyword}': {e}"
                logger.error(error_msg)
                self.results['errors'].append(error_msg)
        
        logger.info(f"\n✓ Document discovery complete: {self.results['documents_discovered']} documents discovered")
    
    def print_summary(self):
        """Print acquisition summary."""
        logger.info("\n" + "="*60)
        logger.info("MEDIA ACQUISITION SUMMARY")
        logger.info("="*60)
        logger.info(f"News Articles:")
        logger.info(f"  Discovered: {self.results['news_discovered']}")
        logger.info(f"  Queued:     {self.results['news_queued']}")
        logger.info(f"  Collected:  {self.results['news_collected']}")
        logger.info(f"Videos:")
        logger.info(f"  Discovered: {self.results['videos_discovered']}")
        logger.info(f"Documents:")
        logger.info(f"  Discovered: {self.results['documents_discovered']}")
        
        if self.results['errors']:
            logger.info(f"\nErrors ({len(self.results['errors'])}):")
            for error in self.results['errors'][:5]:  # Show first 5 errors
                logger.warning(f"  - {error}")
        
        # Queue summary
        queue_summary = self.storage.get_queue_summary()
        logger.info(f"\nCurrent Queue Status:")
        for media_type, statuses in queue_summary.items():
            for status, count in statuses.items():
                logger.info(f"  {media_type} [{status}]: {count}")
        
        logger.info("\n" + "="*60)
    
    async def run(self):
        """Run the full acquisition pipeline."""
        start_time = datetime.now()
        
        try:
            await self.initialize()
            
            # Phase 1: Discover news
            await self.discover_news(max_results=30)
            
            # Phase 2: Collect news
            await self.collect_news(batch_size=10)
            
            # Phase 3: Discover videos
            await self.discover_videos(max_results=10)
            
            # Phase 4: Discover documents
            await self.discover_documents(max_results=10)
            
            # Print summary
            self.print_summary()
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            return 1
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"\nPipeline completed in {duration}")
        
        return 0


async def main():
    """Main entry point."""
    runner = MediaAcquisitionRunner()
    return await runner.run()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
