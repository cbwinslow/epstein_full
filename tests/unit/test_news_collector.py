"""
Unit tests for NewsCollector.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

from media_acquisition.base import AgentConfig, NewsArticleURL, StorageManager
from media_acquisition.agents.collection.news import NewsCollector


class TestNewsCollector:
    """Test suite for NewsCollector."""
    
    def test_init(self, agent_config: AgentConfig, storage_manager: StorageManager):
        """Test NewsCollector initialization."""
        collector = NewsCollector(agent_config, storage_manager)
        
        assert collector is not None
        assert collector.config == agent_config
        assert collector.storage == storage_manager
        assert collector.AGENT_TYPE == 'collection'
    
    def test_process_article_method_exists(self, agent_config: AgentConfig, storage_manager: StorageManager):
        """Test that process_article method exists."""
        collector = NewsCollector(agent_config, storage_manager)
        
        assert hasattr(collector, 'process_article')
        assert callable(collector.process_article)
    
    @pytest.mark.asyncio
    async def test_process_article_with_valid_url(
        self,
        agent_config: AgentConfig,
        storage_manager: StorageManager,
        sample_news_article: NewsArticleURL
    ):
        """Test processing a valid article URL."""
        collector = NewsCollector(agent_config, storage_manager)
        
        # Mock the download to avoid network calls
        with patch.object(collector, '_download_article', new_callable=AsyncMock) as mock_download:
            mock_download.return_value = {
                'url': sample_news_article.url,
                'title': sample_news_article.title,
                'content': 'Test article content',
                'content_cleaned': 'Test article content cleaned',
                'source_domain': sample_news_article.source_domain,
                'word_count': 100,
                'extraction_method': 'test'
            }
            
            result = await collector.process_article(sample_news_article)
            
            assert result is not None
            assert isinstance(result, dict)
            assert result.get('success') is True
            assert result.get('url') == sample_news_article.url
            assert result.get('title') == sample_news_article.title
    
    @pytest.mark.asyncio
    async def test_process_article_with_invalid_url(
        self,
        agent_config: AgentConfig,
        storage_manager: StorageManager
    ):
        """Test processing an invalid article URL."""
        collector = NewsCollector(agent_config, storage_manager)
        
        invalid_article = NewsArticleURL(
            url='https://invalid-domain-that-does-not-exist.com/article',
            title='Invalid Article',
            source_domain='invalid-domain-that-does-not-exist.com',
            priority=5,
            keywords_matched=['test']
        )
        
        # Mock download to simulate failure
        with patch.object(collector, '_download_article', new_callable=AsyncMock) as mock_download:
            mock_download.return_value = None
            
            result = await collector.process_article(invalid_article)
            
            assert result is not None
            assert result.get('success') is False
            assert 'error' in result
    
    @pytest.mark.asyncio
    async def test_process_article_exception_handling(
        self,
        agent_config: AgentConfig,
        storage_manager: StorageManager,
        sample_news_article: NewsArticleURL
    ):
        """Test exception handling in process_article."""
        collector = NewsCollector(agent_config, storage_manager)
        
        # Mock to raise exception
        with patch.object(collector, '_download_article', new_callable=AsyncMock) as mock_download:
            mock_download.side_effect = Exception("Network error")
            
            result = await collector.process_article(sample_news_article)
            
            assert result is not None
            assert result.get('success') is False
            assert 'error' in result
            assert 'Network error' in result.get('error', '')
    
    @pytest.mark.asyncio
    async def test_collect_method_exists(
        self,
        agent_config: AgentConfig,
        storage_manager: StorageManager
    ):
        """Test that collect method exists."""
        collector = NewsCollector(agent_config, storage_manager)
        
        assert hasattr(collector, 'collect')
        assert callable(collector.collect)
    
    @pytest.mark.asyncio
    async def test_collect_returns_article_data(
        self,
        agent_config: AgentConfig,
        storage_manager: StorageManager,
        sample_news_article: NewsArticleURL
    ):
        """Test that collect returns article data."""
        collector = NewsCollector(agent_config, storage_manager)
        
        with patch.object(collector, '_download_article', new_callable=AsyncMock) as mock_download:
            mock_download.return_value = {
                'url': sample_news_article.url,
                'title': sample_news_article.title,
                'content': 'Test content',
                'content_cleaned': 'Test content cleaned',
                'source_domain': sample_news_article.source_domain,
                'word_count': 50,
                'extraction_method': 'test'
            }
            
            result = await collector.collect(sample_news_article)
            
            assert result is not None
            assert isinstance(result, dict)
            assert result.get('url') == sample_news_article.url
    
    def test_storage_integration(self, agent_config: AgentConfig, storage_manager: StorageManager):
        """Test that collector properly integrates with storage."""
        collector = NewsCollector(agent_config, storage_manager)
        
        assert collector.storage is not None
        assert hasattr(collector.storage, 'add_to_queue')
        assert hasattr(collector.storage, 'get_queue_summary')
    
    @pytest.mark.asyncio
    async def test_process_queue_batch(
        self,
        agent_config: AgentConfig,
        storage_manager: StorageManager
    ):
        """Test processing a batch of queued items."""
        collector = NewsCollector(agent_config, storage_manager)
        
        # Add items to queue
        for i in range(3):
            storage_manager.add_to_queue(
                media_type='news',
                source_url=f'https://example.com/batch-article-{i}',
                priority=5,
                keywords_matched=['Epstein'],
                discovered_by='test'
            )
        
        # Mock the download
        with patch.object(collector, '_download_article', new_callable=AsyncMock) as mock_download:
            mock_download.return_value = {
                'url': 'https://example.com/article',
                'title': 'Test Title',
                'content': 'Test content',
                'content_cleaned': 'Test content cleaned',
                'source_domain': 'example.com',
                'word_count': 100,
                'extraction_method': 'test'
            }
            
            results = await collector.process_queue(batch_size=3)
            
            assert isinstance(results, list)
            assert len(results) <= 3
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_collection_flow(
        self,
        agent_config: AgentConfig,
        storage_manager: StorageManager
    ):
        """Integration test: full collection flow with real storage."""
        collector = NewsCollector(agent_config, storage_manager)
        
        # Create test article
        test_article = NewsArticleURL(
            url='https://en.wikipedia.org/wiki/Jeffrey_Epstein',
            title='Jeffrey Epstein - Wikipedia',
            source_domain='wikipedia.org',
            publish_date=datetime.now(),
            priority=5,
            keywords_matched=['Epstein', 'Wikipedia'],
            discovery_method='test'
        )
        
        # Process article
        result = await collector.process_article(test_article)
        
        # Verify result structure
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'url' in result
        
        print(f"✓ Collection flow completed: success={result.get('success')}")
