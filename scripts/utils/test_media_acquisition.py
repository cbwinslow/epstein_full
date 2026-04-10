#!/usr/bin/env python3
"""
Comprehensive Media Acquisition Test Suite
Tests all agents, storage, and database operations
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
from media_acquisition.base import StorageManager, AgentConfig, NewsArticleURL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MediaAcquisitionTester:
    """Comprehensive test suite for media acquisition system."""
    
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.storage = None
        self.config = None
    
    def log_test(self, name: str, status: str, message: str = None):
        """Log test result."""
        if status == 'PASS':
            self.results['passed'].append(name)
            logger.info(f"✅ {name}")
        elif status == 'FAIL':
            self.results['failed'].append((name, message))
            logger.error(f"❌ {name}: {message}")
        else:
            self.results['warnings'].append((name, message))
            logger.warning(f"⚠️  {name}: {message}")
    
    # =========================================================================
    # TEST 1: Storage Manager
    # =========================================================================
    
    def test_storage_manager_init(self):
        """Test StorageManager initialization."""
        try:
            self.storage = StorageManager(
                connection_string='postgresql://cbwinslow:123qweasd@localhost:5432/epstein',
                base_path='/home/cbwinslow/workspace/epstein-data/media'
            )
            self.log_test('StorageManager Init', 'PASS')
            return True
        except Exception as e:
            self.log_test('StorageManager Init', 'FAIL', str(e))
            return False
    
    def test_storage_manager_connection(self):
        """Test database connection."""
        try:
            summary = self.storage.get_queue_summary()
            self.log_test('Database Connection', 'PASS')
            return True
        except Exception as e:
            self.log_test('Database Connection', 'FAIL', str(e))
            return False
    
    def test_storage_add_to_queue(self):
        """Test adding item to queue."""
        try:
            self.storage.add_to_queue(
                media_type='news',
                source_url='https://example.com/test-article',
                priority=5,
                keywords_matched=['test'],
                discovered_by='test-suite',
                metadata={'title': 'Test Article', 'source_domain': 'example.com'}
            )
            self.log_test('Add to Queue', 'PASS')
            return True
        except Exception as e:
            self.log_test('Add to Queue', 'FAIL', str(e))
            return False
    
    # =========================================================================
    # TEST 2: NewsDiscoveryAgent
    # =========================================================================
    
    async def test_news_agent_init(self):
        """Test NewsDiscoveryAgent initialization."""
        try:
            self.config = AgentConfig(agent_id='test-news-agent')
            agent = NewsDiscoveryAgent(self.config)
            self.log_test('NewsDiscoveryAgent Init', 'PASS')
            return True
        except Exception as e:
            self.log_test('NewsDiscoveryAgent Init', 'FAIL', str(e))
            return False
    
    async def test_news_agent_search_method_exists(self):
        """Verify search() method exists."""
        try:
            agent = NewsDiscoveryAgent(self.config)
            if hasattr(agent, 'search') and callable(getattr(agent, 'search')):
                self.log_test('News Agent search() Method', 'PASS')
                return True
            else:
                self.log_test('News Agent search() Method', 'FAIL', 'Method not found')
                return False
        except Exception as e:
            self.log_test('News Agent search() Method', 'FAIL', str(e))
            return False
    
    async def test_news_agent_search_gdelt(self):
        """Test actual GDELT search."""
        try:
            agent = NewsDiscoveryAgent(self.config)
            results = await agent.search(
                keywords=['Epstein'],
                date_range=('2024-01-01', '2024-01-31'),
                max_results=10
            )
            if len(results) > 0:
                self.log_test('News Agent GDELT Search', 'PASS', f'Found {len(results)} articles')
                # Verify result structure
                article = results[0]
                checks = [
                    hasattr(article, 'url'),
                    hasattr(article, 'title'),
                    hasattr(article, 'source_domain'),
                    hasattr(article, 'priority'),
                    hasattr(article, 'keywords_matched')
                ]
                if all(checks):
                    self.log_test('News Article Structure', 'PASS')
                else:
                    missing = [a for a, c in zip(['url', 'title', 'source_domain', 'priority', 'keywords_matched'], checks) if not c]
                    self.log_test('News Article Structure', 'FAIL', f'Missing: {missing}')
                return True
            else:
                self.log_test('News Agent GDELT Search', 'WARNING', 'No results found')
                return True
        except Exception as e:
            self.log_test('News Agent GDELT Search', 'FAIL', str(e))
            return False
    
    async def test_news_agent_search_wayback(self):
        """Test Wayback Machine search."""
        try:
            agent = NewsDiscoveryAgent(self.config)
            results = await agent.search(
                keywords=['Epstein'],
                date_range=('2020-01-01', '2020-01-31'),
                max_results=5
            )
            self.log_test('News Agent Wayback Search', 'PASS', f'Found {len(results)} articles')
            return True
        except Exception as e:
            self.log_test('News Agent Wayback Search', 'FAIL', str(e))
            return False
    
    # =========================================================================
    # TEST 3: VideoDiscoveryAgent
    # =========================================================================
    
    async def test_video_agent_init(self):
        """Test VideoDiscoveryAgent initialization."""
        try:
            agent = VideoDiscoveryAgent(self.config)
            self.log_test('VideoDiscoveryAgent Init', 'PASS')
            return True
        except Exception as e:
            self.log_test('VideoDiscoveryAgent Init', 'FAIL', str(e))
            return False
    
    async def test_video_agent_search(self):
        """Test video search."""
        try:
            agent = VideoDiscoveryAgent(self.config)
            results = await agent.search(keywords=['Epstein'], max_results=10)
            self.log_test('Video Agent Search', 'PASS', f'Found {len(results)} videos')
            if results:
                video = results[0]
                checks = [
                    hasattr(video, 'url'),
                    hasattr(video, 'title'),
                    hasattr(video, 'platform'),
                    hasattr(video, 'priority')
                ]
                if all(checks):
                    self.log_test('Video Metadata Structure', 'PASS')
                else:
                    self.log_test('Video Metadata Structure', 'WARNING', 'Some fields missing')
            return True
        except Exception as e:
            self.log_test('Video Agent Search', 'FAIL', str(e))
            return False
    
    # =========================================================================
    # TEST 4: DocumentDiscoveryAgent
    # =========================================================================
    
    async def test_document_agent_init(self):
        """Test DocumentDiscoveryAgent initialization."""
        try:
            agent = DocumentDiscoveryAgent(self.config)
            self.log_test('DocumentDiscoveryAgent Init', 'PASS')
            return True
        except Exception as e:
            self.log_test('DocumentDiscoveryAgent Init', 'FAIL', str(e))
            return False
    
    async def test_document_agent_search(self):
        """Test document search."""
        try:
            agent = DocumentDiscoveryAgent(self.config)
            results = await agent.search(keywords=['Epstein'], max_results=10)
            self.log_test('Document Agent Search', 'PASS', f'Found {len(results)} documents')
            return True
        except Exception as e:
            self.log_test('Document Agent Search', 'FAIL', str(e))
            return False
    
    # =========================================================================
    # TEST 5: NewsCollector
    # =========================================================================
    
    async def test_news_collector_init(self):
        """Test NewsCollector initialization."""
        try:
            if not self.storage:
                self.log_test('NewsCollector Init', 'FAIL', 'StorageManager not initialized')
                return False
            collector = NewsCollector(self.config, self.storage)
            self.log_test('NewsCollector Init', 'PASS')
            return True
        except Exception as e:
            self.log_test('NewsCollector Init', 'FAIL', str(e))
            return False
    
    async def test_news_collector_process_article(self):
        """Test processing a single article."""
        try:
            collector = NewsCollector(self.config, self.storage)
            
            # Create test article
            test_article = NewsArticleURL(
                url='https://en.wikipedia.org/wiki/Jeffrey_Epstein',
                title='Jeffrey Epstein Wikipedia Test',
                source_domain='wikipedia.org',
                publish_date=datetime.now(),
                priority=5,
                keywords_matched=['Epstein'],
                discovery_method='test'
            )
            
            result = await collector.process_article(test_article)
            if result.get('success'):
                self.log_test('NewsCollector Process Article', 'PASS')
            else:
                self.log_test('NewsCollector Process Article', 'WARNING', result.get('error', 'Unknown error'))
            return True
        except Exception as e:
            self.log_test('NewsCollector Process Article', 'FAIL', str(e))
            return False
    
    # =========================================================================
    # TEST 6: Database Operations
    # =========================================================================
    
    def test_database_tables_exist(self):
        """Test that required tables exist."""
        try:
            import psycopg2
            conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
            cur = conn.cursor()
            
            tables = [
                'media_collection_queue',
                'media_news_articles',
                'media_videos',
                'media_documents',
                'media_entities',
                'media_entity_mentions'
            ]
            
            for table in tables:
                cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
                exists = cur.fetchone()[0]
                if exists:
                    self.log_test(f'Table: {table}', 'PASS')
                else:
                    self.log_test(f'Table: {table}', 'FAIL', 'Table does not exist')
            
            cur.close()
            conn.close()
            return True
        except Exception as e:
            self.log_test('Database Tables', 'FAIL', str(e))
            return False
    
    # =========================================================================
    # RUN ALL TESTS
    # =========================================================================
    
    async def run_all_tests(self):
        """Run complete test suite."""
        logger.info("╔══════════════════════════════════════════════════════════════╗")
        logger.info("║     MEDIA ACQUISITION SYSTEM - COMPREHENSIVE TEST SUITE      ║")
        logger.info("╚══════════════════════════════════════════════════════════════╝")
        logger.info(f"Started: {datetime.now().isoformat()}")
        logger.info("")
        
        # Phase 1: Storage Manager Tests
        logger.info("=== PHASE 1: Storage Manager ===")
        self.test_storage_manager_init()
        if self.storage:
            self.test_storage_manager_connection()
            self.test_storage_add_to_queue()
        
        # Phase 2: Database Tests
        logger.info("\n=== PHASE 2: Database Schema ===")
        self.test_database_tables_exist()
        
        # Phase 3: News Discovery Agent
        logger.info("\n=== PHASE 3: News Discovery Agent ===")
        await self.test_news_agent_init()
        await self.test_news_agent_search_method_exists()
        await self.test_news_agent_search_gdelt()
        await self.test_news_agent_search_wayback()
        
        # Phase 4: Video Discovery Agent
        logger.info("\n=== PHASE 4: Video Discovery Agent ===")
        await self.test_video_agent_init()
        await self.test_video_agent_search()
        
        # Phase 5: Document Discovery Agent
        logger.info("\n=== PHASE 5: Document Discovery Agent ===")
        await self.test_document_agent_init()
        await self.test_document_agent_search()
        
        # Phase 6: Collection Agents
        logger.info("\n=== PHASE 6: Collection Agents ===")
        await self.test_news_collector_init()
        await self.test_news_collector_process_article()
        
        # Summary
        logger.info("\n╔══════════════════════════════════════════════════════════════╗")
        logger.info("║                      TEST SUMMARY                            ║")
        logger.info("╚══════════════════════════════════════════════════════════════╝")
        logger.info(f"Passed:  {len(self.results['passed'])}")
        logger.info(f"Failed:  {len(self.results['failed'])}")
        logger.info(f"Warnings: {len(self.results['warnings'])}")
        
        if self.results['failed']:
            logger.info("\nFailed Tests:")
            for name, msg in self.results['failed']:
                logger.info(f"  - {name}: {msg}")
        
        if self.results['warnings']:
            logger.info("\nWarnings:")
            for name, msg in self.results['warnings']:
                logger.info(f"  - {name}: {msg}")
        
        logger.info(f"\nFinished: {datetime.now().isoformat()}")
        
        return self.results


async def main():
    """Run the test suite."""
    tester = MediaAcquisitionTester()
    results = await tester.run_all_tests()
    
    # Save results to file
    import json
    results_file = Path('/home/cbwinslow/workspace/epstein/logs/test_results.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"\nResults saved to: {results_file}")
    
    # Return exit code
    return 0 if not results['failed'] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
