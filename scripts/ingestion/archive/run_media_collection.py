#!/usr/bin/env python3
"""
Epstein Media Collection Orchestrator
Runs all discovery agents and ingests data into PostgreSQL
"""

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.agents.discovery.video import VideoDiscoveryAgent
from media_acquisition.agents.discovery.document import DocumentDiscoveryAgent
from media_acquisition.agents.collection.news import NewsCollector
from media_acquisition.agents.collection.video import VideoTranscriber
from media_acquisition.agents.processing.entities import EntityExtractor
from media_acquisition.base import StorageManager, AgentConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cbwinslow/workspace/epstein/logs/collection_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CollectionOrchestrator:
    """Orchestrates media collection across all sources."""
    
    def __init__(self):
        self.storage = StorageManager(
            connection_string='postgresql://cbwinslow:123qweasd@localhost:5432/epstein',
            base_path='/home/cbwinslow/workspace/epstein-data/media'
        )
        
        # Initialize agents
        config = AgentConfig(agent_id='orchestrator')
        self.news_agent = NewsDiscoveryAgent(config)
        self.video_agent = VideoDiscoveryAgent(config)
        self.doc_agent = DocumentDiscoveryAgent(config)
        self.news_collector = NewsCollector(config, self.storage)
        self.video_transcriber = VideoTranscriber(config, self.storage)
        self.entity_extractor = EntityExtractor(config, self.storage)
        
        self.stats = {
            'news_discovered': 0,
            'news_collected': 0,
            'videos_discovered': 0,
            'videos_transcribed': 0,
            'docs_discovered': 0,
            'entities_extracted': 0,
            'errors': []
        }
    
    async def discover_all_news(self):
        """Discover news articles from all sources."""
        logger.info("=== STARTING NEWS DISCOVERY ===")
        
        date_ranges = [
            ('2020-01-01', '2020-06-30'),
            ('2020-07-01', '2020-12-31'),
            ('2021-01-01', '2021-06-30'),
            ('2021-07-01', '2021-12-31'),
            ('2022-01-01', '2022-06-30'),
            ('2022-07-01', '2022-12-31'),
            ('2023-01-01', '2023-06-30'),
            ('2023-07-01', '2023-12-31'),
            ('2024-01-01', '2024-06-30'),
            ('2024-07-01', '2024-12-31'),
            ('2025-01-01', '2025-04-04'),
        ]
        
        keywords_list = [
            ['Epstein', 'Jeffrey Epstein'],
            ['Maxwell', 'Ghislaine Maxwell'],
            ['Epstein', 'Virginia Giuffre'],
            ['Epstein', 'Little St James'],
            ['Epstein', 'flight logs'],
            ['Epstein', 'sex trafficking'],
            ['Epstein', 'Lolita Express'],
            ['Epstein', 'Pedophile Island'],
        ]
        
        for start_date, end_date in date_ranges:
            for keywords in keywords_list:
                try:
                    logger.info(f'News search: {keywords} ({start_date} to {end_date})')
                    results = await self.news_agent.search(
                        keywords=keywords,
                        date_range=(start_date, end_date),
                        max_results=100
                    )
                    
                    # Queue articles
                    for article in results:
                        try:
                            self.storage.add_to_queue(
                                media_type='news',
                                source_url=article.url,
                                priority=article.priority,
                                keywords_matched=article.keywords_matched,
                                discovered_by='news-discovery-v2',
                                metadata={
                                    'title': article.title,
                                    'source_domain': article.source_domain,
                                    'discovery_method': article.discovery_method,
                                    'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                                    'authors': getattr(article, 'authors', []),
                                    'summary': getattr(article, 'summary', None)
                                }
                            )
                        except Exception as e:
                            logger.warning(f'Queue failed: {e}')
                    
                    self.stats['news_discovered'] += len(results)
                    logger.info(f'  Found {len(results)} articles')
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f'News discovery error: {e}')
                    self.stats['errors'].append(f'News: {e}')
                    continue
        
        logger.info(f"News discovery complete: {self.stats['news_discovered']} articles")
    
    async def discover_all_videos(self):
        """Discover videos from YouTube and Internet Archive."""
        logger.info("=== STARTING VIDEO DISCOVERY ===")
        
        keywords_list = [
            'Epstein',
            'Ghislaine Maxwell',
            'Virginia Giuffre',
            'Epstein Island',
            'Epstein documentary',
            'Jeffrey Epstein case',
            'Epstein victims',
            'Epstein conspiracy',
        ]
        
        for keywords in keywords_list:
            try:
                logger.info(f'Video search: {keywords}')
                results = await self.video_agent.search(
                    keywords=keywords,
                    max_results=50
                )
                
                # Queue videos
                for video in results:
                    try:
                        self.storage.add_to_queue(
                            media_type='video',
                            source_url=video.url,
                            priority=video.priority,
                            keywords_matched=video.keywords_matched,
                            discovered_by='video-discovery-v2',
                            metadata={
                                'title': video.title,
                                'platform': getattr(video, 'platform', 'unknown'),
                                'video_id': getattr(video, 'video_id', None),
                                'description': getattr(video, 'description', None),
                                'upload_date': video.publish_date.isoformat() if video.publish_date else None,
                                'duration_seconds': getattr(video, 'duration_seconds', None),
                                'view_count': getattr(video, 'view_count', None)
                            }
                        )
                    except Exception as e:
                        logger.warning(f'Queue failed: {e}')
                
                self.stats['videos_discovered'] += len(results)
                logger.info(f'  Found {len(results)} videos')
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f'Video discovery error: {e}')
                self.stats['errors'].append(f'Video: {e}')
                continue
        
        logger.info(f"Video discovery complete: {self.stats['videos_discovered']} videos")
    
    async def discover_all_documents(self):
        """Discover court and government documents."""
        logger.info("=== STARTING DOCUMENT DISCOVERY ===")
        
        # Search CourtListener
        court_cases = [
            'Giuffre v. Maxwell',
            'US v. Maxwell',
            'Epstein',
            'Virginia Roberts',
        ]
        
        for case in court_cases:
            try:
                logger.info(f'Document search: {case}')
                results = await self.doc_agent.search(
                    keywords=case,
                    max_results=100
                )
                
                # Queue documents
                for doc in results:
                    try:
                        self.storage.add_to_queue(
                            media_type='document',
                            source_url=doc.url,
                            priority=doc.priority,
                            keywords_matched=doc.keywords_matched,
                            discovered_by='document-discovery-v2',
                            metadata={
                                'title': doc.title,
                                'source': getattr(doc, 'source', 'unknown'),
                                'document_type': getattr(doc, 'document_type', None),
                                'docket_number': getattr(doc, 'docket_number', None),
                                'case_name': getattr(doc, 'case_name', None),
                                'court': getattr(doc, 'court', None),
                                'filing_date': doc.publish_date.isoformat() if doc.publish_date else None,
                                'page_count': getattr(doc, 'page_count', None)
                            }
                        )
                    except Exception as e:
                        logger.warning(f'Queue failed: {e}')
                
                self.stats['docs_discovered'] += len(results)
                logger.info(f'  Found {len(results)} documents')
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f'Document discovery error: {e}')
                self.stats['errors'].append(f'Doc: {e}')
                continue
        
        logger.info(f"Document discovery complete: {self.stats['docs_discovered']} documents")
    
    async def collect_news_batch(self, batch_size: int = 50):
        """Collect queued news articles."""
        logger.info(f"=== COLLECTING NEWS (batch: {batch_size}) ===")
        
        try:
            results = await self.news_collector.process_queue(batch_size=batch_size)
            self.stats['news_collected'] += len(results)
            logger.info(f'Collected {len(results)} articles')
        except Exception as e:
            logger.error(f'News collection error: {e}')
            self.stats['errors'].append(f'News collect: {e}')
    
    async def process_entities_batch(self, batch_size: int = 50):
        """Extract entities from collected content."""
        logger.info(f"=== EXTRACTING ENTITIES (batch: {batch_size}) ===")
        
        try:
            results = await self.entity_extractor.process_unprocessed_media(batch_size=batch_size)
            self.stats['entities_extracted'] += sum(r.get('entity_count', 0) for r in results)
            logger.info(f'Processed {len(results)} items')
        except Exception as e:
            logger.error(f'Entity extraction error: {e}')
            self.stats['errors'].append(f'Entity: {e}')
    
    async def run_full_collection(self):
        """Run complete collection pipeline."""
        logger.info("╔══════════════════════════════════════════════════════════════╗")
        logger.info("║      EPSTEIN MEDIA COLLECTION - FULL PIPELINE                ║")
        logger.info("╚══════════════════════════════════════════════════════════════╝")
        logger.info(f"Started at: {datetime.now().isoformat()}")
        
        # Phase 1: Discovery
        await self.discover_all_news()
        await self.discover_all_videos()
        await self.discover_all_documents()
        
        # Phase 2: Collection
        # Collect news in batches
        for i in range(10):  # 10 batches
            await self.collect_news_batch(batch_size=50)
            await asyncio.sleep(5)
        
        # Phase 3: Processing
        for i in range(5):  # 5 batches
            await self.process_entities_batch(batch_size=50)
            await asyncio.sleep(2)
        
        # Final stats
        logger.info("\n╔══════════════════════════════════════════════════════════════╗")
        logger.info("║                   COLLECTION COMPLETE                        ║")
        logger.info("╚══════════════════════════════════════════════════════════════╝")
        logger.info(f"News discovered: {self.stats['news_discovered']}")
        logger.info(f"News collected: {self.stats['news_collected']}")
        logger.info(f"Videos discovered: {self.stats['videos_discovered']}")
        logger.info(f"Documents discovered: {self.stats['docs_discovered']}")
        logger.info(f"Entities extracted: {self.stats['entities_extracted']}")
        logger.info(f"Errors: {len(self.stats['errors'])}")
        logger.info(f"Finished at: {datetime.now().isoformat()}")
        
        return self.stats


async def main():
    """Main entry point."""
    orchestrator = CollectionOrchestrator()
    stats = await orchestrator.run_full_collection()
    
    # Save stats to file
    stats_file = Path('/home/cbwinslow/workspace/epstein/logs/collection_stats.json')
    import json
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    
    logger.info(f"Stats saved to: {stats_file}")
    return stats


if __name__ == "__main__":
    stats = asyncio.run(main())
    print(f"\nCollection complete!")
    print(f"News discovered: {stats['news_discovered']}")
    print(f"News collected: {stats['news_collected']}")
    print(f"Videos discovered: {stats['videos_discovered']}")
    print(f"Documents discovered: {stats['docs_discovered']}")
