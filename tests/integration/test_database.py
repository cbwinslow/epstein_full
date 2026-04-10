"""
Integration tests for database operations.
"""

import pytest
import pytest_asyncio
from datetime import datetime


@pytest.mark.integration
class TestDatabaseOperations:
    """Integration tests requiring database connection."""
    
    def test_database_connection(self, storage_manager):
        """Test that database connection works."""
        try:
            summary = storage_manager.get_queue_summary()
            assert isinstance(summary, dict)
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")
    
    def test_media_entities_table_exists(self, storage_manager):
        """Test that media_entities table exists."""
        try:
            with storage_manager._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'media_entities'
                        )
                    """)
                    exists = cur.fetchone()[0]
                    assert exists, "media_entities table does not exist"
        except Exception as e:
            pytest.fail(f"Table check failed: {e}")
    
    def test_queue_workflow(self, storage_manager):
        """Test complete queue workflow: add, retrieve, update."""
        # Add item to queue
        queue_id = storage_manager.add_to_queue(
            media_type='news',
            source_url='https://example.com/test-workflow',
            priority=3,
            keywords_matched=['Epstein', 'test'],
            discovered_by='integration-test',
            metadata={'title': 'Test Workflow Article'}
        )
        
        assert queue_id is not None, "Failed to add item to queue"
        
        # Get queue summary
        summary = storage_manager.get_queue_summary()
        assert 'news' in summary
        assert summary['news']['pending'] >= 1
        
        # Get queued items
        items = storage_manager.get_queued_items(
            media_type='news',
            status='pending',
            limit=10
        )
        
        assert len(items) > 0
        assert any(item['id'] == queue_id for item in items)
    
    def test_news_article_storage(self, storage_manager, sample_news_article):
        """Test storing a news article."""
        # Store article
        article_id = storage_manager.store_news_article(
            url=sample_news_article.url,
            title=sample_news_article.title,
            content="Test article content for integration testing.",
            source_domain=sample_news_article.source_domain,
            publish_date=sample_news_article.publish_date,
            priority=sample_news_article.priority,
            keywords_matched=sample_news_article.keywords_matched,
            extraction_method='test',
            word_count=10,
            metadata=sample_news_article.metadata
        )
        
        assert article_id is not None
        
        # Retrieve article
        articles = storage_manager.get_news_articles(
            source_domain='example.com',
            limit=1
        )
        
        assert len(articles) > 0
        assert articles[0]['url'] == sample_news_article.url
    
    def test_video_metadata_storage(self, storage_manager):
        """Test storing video metadata."""
        video_data = {
            'video_id': 'test123',
            'url': 'https://youtube.com/watch?v=test123',
            'title': 'Test Video',
            'platform': 'youtube',
            'duration_seconds': 3600,
            'upload_date': datetime.now(),
            'view_count': 1000,
            'transcript_available': True,
            'keywords_matched': ['Epstein'],
            'discovery_method': 'test'
        }
        
        video_id = storage_manager.store_video_metadata(**video_data)
        assert video_id is not None
        
        # Retrieve
        videos = storage_manager.get_videos(
            platform='youtube',
            limit=1
        )
        
        assert len(videos) > 0
        assert videos[0]['video_id'] == 'test123'


@pytest.mark.integration
@pytest.mark.asyncio
class TestEndToEndWorkflow:
    """End-to-end integration tests."""
    
    async def test_full_discovery_and_collection(
        self,
        news_discovery_agent,
        news_collector,
        storage_manager,
        mocker
    ):
        """
        Test full workflow: discover -> queue -> collect.
        
        This test mocks the external API calls to avoid dependencies.
        """
        # Mock GDELT API response
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "articles": [
                {
                    "url": "https://example.com/e2e-test",
                    "title": "E2E Test Article",
                    "seendate": "20240101120000",
                    "domain": "example.com",
                    "language": "en"
                }
            ]
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = mocker.Mock()
        
        mocker.patch(
            'media_acquisition.agents.discovery.news.requests.get',
            return_value=mock_response
        )
        
        # Phase 1: Discovery
        discovered = await news_discovery_agent.search(
            keywords=['Epstein'],
            date_range=('2024-01-01', '2024-01-31'),
            max_results=10
        )
        
        assert len(discovered) > 0, "Should discover articles"
        
        # Phase 2: Queue
        for article in discovered:
            queue_id = storage_manager.add_to_queue(
                media_type='news',
                source_url=article.url,
                priority=article.priority,
                keywords_matched=article.keywords_matched,
                discovered_by='e2e-test',
                metadata={
                    'title': article.title,
                    'source_domain': article.source_domain
                }
            )
            assert queue_id is not None
        
        # Phase 3: Verify queue
        summary = storage_manager.get_queue_summary()
        assert summary['news']['pending'] > 0
        
        print(f"✓ E2E workflow completed: {len(discovered)} articles discovered and queued")
