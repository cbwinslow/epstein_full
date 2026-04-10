"""
Epstein Media Acquisition Master Controller
Orchestrates all discovery, collection, and processing agents.
"""

import asyncio
import json
import logging
import signal
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/home/cbwinslow/workspace/epstein/logs/media_acquisition.log')
    ]
)
logger = logging.getLogger(__name__)

# Add project to path
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.base import (
    AgentConfig, StorageManager,
    NewsArticleURL, VideoMetadata, DocumentMetadata
)


class MediaAcquisitionSystem:
    """
    Master controller for all media acquisition operations.
    
    Usage:
        system = MediaAcquisitionSystem()
        
        # Run full historical collection
        system.run_historical_collection(
            start_date='1990-01-01',
            end_date='2025-12-31',
            media_types=['news', 'video', 'document']
        )
        
        # Run continuous monitoring
        system.run_continuous_monitoring()
    """
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.storage = StorageManager(
            connection_string=self.config.postgres_url,
            base_path=self.config.storage_path
        )
        
        # Import agents (lazy loading)
        self._discovery_agents = {}
        self._collection_agents = {}
        self._processing_agents = {}
        
        # State
        self.running = False
        self.stats = {
            'started_at': None,
            'items_discovered': 0,
            'items_collected': 0,
            'errors': 0
        }
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("MediaAcquisitionSystem initialized")
    
    def _load_config(self, config_path: str = None) -> AgentConfig:
        """Load configuration."""
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                config_dict = json.load(f)
                return AgentConfig(**config_dict)
        
        # Return default config
        return AgentConfig(
            agent_id='master-controller',
            postgres_url='postgresql://cbwinslow:123qweasd@localhost:5432/epstein',
            storage_path='/home/cbwinslow/workspace/epstein-data/media/'
        )
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def _get_discovery_agent(self, media_type: str):
        """Lazy load discovery agent."""
        if media_type not in self._discovery_agents:
            if media_type == 'news':
                from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
                self._discovery_agents[media_type] = NewsDiscoveryAgent(self.config)
            # elif media_type == 'video':
            #     from media_acquisition.agents.discovery.video import VideoDiscoveryAgent
            #     self._discovery_agents[media_type] = VideoDiscoveryAgent(self.config)
            # elif media_type == 'document':
            #     from media_acquisition.agents.discovery.document import DocumentDiscoveryAgent
            #     self._discovery_agents[media_type] = DocumentDiscoveryAgent(self.config)
            else:
                raise ValueError(f"Unknown media type: {media_type}")
        
        return self._discovery_agents[media_type]
    
    def _get_collection_agent(self, media_type: str):
        """Lazy load collection agent."""
        if media_type not in self._collection_agents:
            if media_type == 'news':
                from media_acquisition.agents.collection.news import NewsCollector
                self._collection_agents[media_type] = NewsCollector(self.config, self.storage)
            # elif media_type == 'video':
            #     from media_acquisition.agents.collection.video import VideoTranscriber
            #     self._collection_agents[media_type] = VideoTranscriber(self.config, self.storage)
            # elif media_type == 'document':
            #     from media_acquisition.agents.collection.document import DocumentDownloader
            #     self._collection_agents[media_type] = DocumentDownloader(self.config, self.storage)
            else:
                raise ValueError(f"Unknown media type: {media_type}")
        
        return self._collection_agents[media_type]
    
    async def run_historical_collection(self,
                                       start_date: str,
                                       end_date: str,
                                       media_types: List[str] = None,
                                       keywords: List[str] = None):
        """
        Run full historical collection for date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            media_types: ['news', 'video', 'document'] or None for all
            keywords: Custom keywords or None for defaults
        """
        media_types = media_types or ['news']  # Start with news only
        keywords = keywords or ['Epstein', 'Maxwell']
        
        self.running = True
        self.stats['started_at'] = datetime.now()
        
        logger.info(f"Starting historical collection: {start_date} to {end_date}")
        logger.info(f"Media types: {media_types}")
        logger.info(f"Keywords: {keywords}")
        
        for media_type in media_types:
            if not self.running:
                break
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing media type: {media_type}")
            logger.info(f"{'='*60}\n")
            
            try:
                # Phase 1: Discovery
                await self._run_discovery_phase(
                    media_type=media_type,
                    keywords=keywords,
                    date_range=(start_date, end_date)
                )
                
                # Phase 2: Collection
                await self._run_collection_phase(media_type)
                
                # Phase 3: Processing
                await self._run_processing_phase(media_type)
                
            except Exception as e:
                logger.error(f"Error processing {media_type}: {e}", exc_info=True)
                self.stats['errors'] += 1
        
        # Summary
        self._print_summary()
    
    async def _run_discovery_phase(self,
                                  media_type: str,
                                  keywords: List[str],
                                  date_range: tuple):
        """Run discovery phase for media type."""
        logger.info(f"[Discovery] Starting {media_type} discovery...")
        
        agent = self._get_discovery_agent(media_type)
        
        # Run discovery
        start_time = time.time()
        results = await agent.search(
            keywords=keywords,
            date_range=date_range
        )
        duration = time.time() - start_time
        
        logger.info(f"[Discovery] Found {len(results)} {media_type} items in {duration:.1f}s")
        
        # Queue for collection
        queued = 0
        for item in results:
            try:
                item_id = self.storage.queue_item(
                    media_type=media_type,
                    source_url=item.url,
                    priority=item.priority,
                    keywords_matched=item.keywords_matched,
                    discovered_by=agent.AGENT_ID
                )
                if item_id:
                    queued += 1
            except Exception as e:
                logger.warning(f"Failed to queue {item.url}: {e}")
        
        logger.info(f"[Discovery] Queued {queued} items for collection")
        self.stats['items_discovered'] += len(results)
    
    async def _run_collection_phase(self, media_type: str):
        """Run collection phase for media type."""
        logger.info(f"[Collection] Starting {media_type} collection...")
        
        agent = self._get_collection_agent(media_type)
        
        collected = 0
        failed = 0
        
        while self.running:
            # Get batch of pending items
            items = self.storage.get_queued_items(
                media_type=media_type,
                status='pending',
                limit=100
            )
            
            if not items:
                logger.info(f"[Collection] No more pending {media_type} items")
                break
            
            logger.info(f"[Collection] Processing batch of {len(items)} items...")
            
            # Process batch
            for item in items:
                if not self.running:
                    break
                
                try:
                    # Mark as processing
                    self.storage.update_queue_status(item['id'], 'processing')
                    
                    # Collect
                    if media_type == 'news':
                        article_url = NewsArticleURL(
                            url=item['source_url'],
                            title=item['metadata'].get('title') if item['metadata'] else None,
                            priority=item['priority'],
                            keywords_matched=item['keywords_matched'] or []
                        )
                        result = await agent.collect(article_url)
                    else:
                        # TODO: Implement for video and document
                        result = None
                    
                    if result:
                        self.storage.update_queue_status(
                            item['id'],
                            'completed',
                            result_id=result.get('id')
                        )
                        collected += 1
                    else:
                        self.storage.update_queue_status(
                            item['id'],
                            'failed',
                            error_message='Collection returned None'
                        )
                        failed += 1
                    
                except Exception as e:
                    logger.error(f"[Collection] Failed to collect {item['source_url']}: {e}")
                    self.storage.update_queue_status(
                        item['id'],
                        'failed',
                        error_message=str(e)[:500]
                    )
                    failed += 1
            
            logger.info(f"[Collection] Batch complete: {collected} collected, {failed} failed")
        
        logger.info(f"[Collection] Phase complete: {collected} collected, {failed} failed")
        self.stats['items_collected'] += collected
    
    async def _run_processing_phase(self, media_type: str):
        """Run NLP processing phase."""
        logger.info(f"[Processing] Starting {media_type} NLP processing...")
        
        # TODO: Implement entity extraction and text analysis
        # This would involve:
        # 1. Loading unprocessed items from database
        # 2. Running entity extraction
        # 3. Running text analysis
        # 4. Updating database with results
        
        logger.info(f"[Processing] Phase complete (placeholder)")
    
    async def run_continuous_monitoring(self, interval_hours: int = 24):
        """
        Continuously monitor for new media.
        
        Args:
            interval_hours: Hours between checks
        """
        self.running = True
        
        logger.info(f"Starting continuous monitoring (interval: {interval_hours}h)")
        
        while self.running:
            try:
                # Check for new content
                since_date = (datetime.now() - timedelta(hours=interval_hours)).strftime('%Y-%m-%d')
                
                await self.run_historical_collection(
                    start_date=since_date,
                    end_date=datetime.now().strftime('%Y-%m-%d'),
                    media_types=['news']  # Start with news
                )
                
                # Wait for next check
                logger.info(f"Sleeping for {interval_hours} hours...")
                await asyncio.sleep(interval_hours * 3600)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}", exc_info=True)
                await asyncio.sleep(300)  # 5 min on error
        
        logger.info("Continuous monitoring stopped")
    
    def _print_summary(self):
        """Print collection summary."""
        duration = datetime.now() - self.stats['started_at']
        
        print("\n" + "="*60)
        print("COLLECTION SUMMARY")
        print("="*60)
        print(f"Duration: {duration}")
        print(f"Items Discovered: {self.stats['items_discovered']}")
        print(f"Items Collected: {self.stats['items_collected']}")
        print(f"Errors: {self.stats['errors']}")
        print("="*60 + "\n")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Epstein Media Acquisition System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run historical collection for news articles
  python -m media_acquisition.master --mode historical --start-date 2024-01-01 --end-date 2024-01-31 --media-types news
  
  # Run continuous monitoring
  python -m media_acquisition.master --mode monitor --interval 24
  
  # Run with custom keywords
  python -m media_acquisition.master --mode historical --keywords Epstein Maxwell --start-date 2023-01-01
        """
    )
    
    parser.add_argument('--mode', choices=['historical', 'monitor', 'discover-only'],
                       default='historical',
                       help='Operation mode')
    parser.add_argument('--start-date', default='2024-01-01',
                       help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2024-12-31',
                       help='End date (YYYY-MM-DD)')
    parser.add_argument('--media-types', nargs='+', default=['news'],
                       choices=['news', 'video', 'document'],
                       help='Media types to collect')
    parser.add_argument('--keywords', nargs='+',
                       default=['Epstein', 'Maxwell'],
                       help='Search keywords')
    parser.add_argument('--interval', type=int, default=24,
                       help='Monitoring interval in hours')
    parser.add_argument('--config', help='Path to config file')
    
    args = parser.parse_args()
    
    # Create system
    system = MediaAcquisitionSystem(config_path=args.config)
    
    # Run based on mode
    if args.mode == 'historical':
        asyncio.run(system.run_historical_collection(
            start_date=args.start_date,
            end_date=args.end_date,
            media_types=args.media_types,
            keywords=args.keywords
        ))
    elif args.mode == 'monitor':
        asyncio.run(system.run_continuous_monitoring(
            interval_hours=args.interval
        ))
    elif args.mode == 'discover-only':
        # TODO: Implement discover-only mode
        logger.info("Discover-only mode not yet implemented")


if __name__ == '__main__':
    import os
    main()
