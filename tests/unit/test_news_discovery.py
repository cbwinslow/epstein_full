"""
Unit tests for NewsDiscoveryAgent.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from media_acquisition.base import AgentConfig, NewsArticleURL
from media_acquisition.agents.discovery.news import NewsDiscoveryAgent


class TestNewsDiscoveryAgent:
    """Test suite for NewsDiscoveryAgent."""
    
    def test_init(self, agent_config: AgentConfig):
        """Test agent initialization."""
        agent = NewsDiscoveryAgent(agent_config)
        
        assert agent is not None
        assert agent.config == agent_config
        assert agent.AGENT_ID == 'news-discovery-v2'
    
    def test_search_method_exists(self, agent_config: AgentConfig):
        """Test that search method exists."""
        agent = NewsDiscoveryAgent(agent_config)
        
        assert hasattr(agent, 'search')
        assert callable(agent.search)
    
    @pytest.mark.asyncio
    @patch('media_acquisition.agents.discovery.news.requests.get')
    async def test_gdelt_search(self, mock_get, agent_config: AgentConfig, mock_gdelt_response):
        """Test GDELT search with mocked response."""
        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = mock_gdelt_response
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Execute
        agent = NewsDiscoveryAgent(agent_config)
        results = await agent.search(
            keywords=['Epstein'],
            date_range=('2024-01-01', '2024-01-31'),
            max_results=10
        )
        
        # Assert
        assert len(results) == 2
        assert isinstance(results[0], NewsArticleURL)
        assert results[0].url == 'https://example.com/article1'
        assert results[0].title == 'Test Article About Epstein'
        mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('media_acquisition.agents.discovery.news.requests.get')
    async def test_gdelt_empty_response(self, mock_get, agent_config: AgentConfig):
        """Test handling of empty GDELT response."""
        # Setup mock with empty response
        mock_response = Mock()
        mock_response.json.return_value = {"articles": []}
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Execute
        agent = NewsDiscoveryAgent(agent_config)
        results = await agent.search(
            keywords=['NonExistentKeyword12345'],
            max_results=10
        )
        
        # Assert
        assert isinstance(results, list)
        assert len(results) == 0
    
    @pytest.mark.asyncio
    @patch('media_acquisition.agents.discovery.news.requests.get')
    async def test_gdelt_rate_limit_handling(self, mock_get, agent_config: AgentConfig):
        """Test handling of rate limit errors."""
        # Setup mock to simulate rate limit
        from requests.exceptions import HTTPError
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("429 Client Error")
        mock_get.return_value = mock_response
        
        # Execute - should not raise, should return empty list or handle gracefully
        agent = NewsDiscoveryAgent(agent_config)
        results = await agent.search(
            keywords=['Epstein'],
            max_results=10
        )
        
        # Assert - should handle gracefully
        assert isinstance(results, list)
    
    @pytest.mark.asyncio
    @patch('media_acquisition.agents.discovery.news.requests.get')
    async def test_wayback_search(self, mock_get, agent_config: AgentConfig):
        """Test Wayback Machine search."""
        # Setup mock for Wayback API
        mock_response = Mock()
        mock_response.json.return_value = {
            "archived_snapshots": {
                "closest": {
                    "available": True,
                    "url": "https://web.archive.org/web/20240101120000/https://example.com/article",
                    "timestamp": "20240101120000"
                }
            }
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Execute
        agent = NewsDiscoveryAgent(agent_config)
        results = await agent._search_wayback(
            url='https://example.com/article',
            date='2024-01-01'
        )
        
        # Assert
        assert results is not None
    
    @pytest.mark.asyncio
    @patch('media_acquisition.agents.discovery.news.requests.get')
    async def test_article_structure_validation(self, mock_get, agent_config: AgentConfig, mock_gdelt_response):
        """Test that discovered articles have required fields."""
        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = mock_gdelt_response
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Execute
        agent = NewsDiscoveryAgent(agent_config)
        results = await agent.search(
            keywords=['Epstein'],
            max_results=10
        )
        
        # Assert - verify all required fields
        for article in results:
            assert hasattr(article, 'url')
            assert hasattr(article, 'title')
            assert hasattr(article, 'source_domain')
            assert hasattr(article, 'priority')
            assert hasattr(article, 'keywords_matched')
            
            assert article.url is not None
            assert article.url.startswith('http')
            assert len(article.keywords_matched) > 0
    
    def test_default_keywords(self):
        """Test that agent has default keywords."""
        agent = NewsDiscoveryAgent()
        
        assert hasattr(agent, 'DEFAULT_KEYWORDS')
        assert isinstance(agent.DEFAULT_KEYWORDS, list)
        assert len(agent.DEFAULT_KEYWORDS) > 0
        assert 'Epstein' in agent.DEFAULT_KEYWORDS
