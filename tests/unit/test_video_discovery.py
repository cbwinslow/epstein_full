"""
Unit tests for VideoDiscoveryAgent.
"""

import pytest
from media_acquisition.base import AgentConfig
from media_acquisition.agents.discovery.video import VideoDiscoveryAgent


class TestVideoDiscoveryAgent:
    """Test suite for VideoDiscoveryAgent."""
    
    def test_init_with_api_key(self, agent_config: AgentConfig):
        """Test agent initialization with API key."""
        agent = VideoDiscoveryAgent(agent_config)
        
        assert agent is not None
        assert hasattr(agent, 'youtube')
        assert agent.youtube is not None
        assert hasattr(agent, 'internet_archive')
    
    def test_init_without_api_key(self, agent_config_no_api_keys: AgentConfig):
        """Test agent initialization without API key."""
        agent = VideoDiscoveryAgent(agent_config_no_api_keys)
        
        assert agent is not None
        assert hasattr(agent, 'youtube')
        # Should still have youtube searcher, just without API key
        assert agent.youtube is not None
    
    def test_youtube_attribute_exists(self, agent_config: AgentConfig):
        """Test that youtube attribute exists after initialization."""
        agent = VideoDiscoveryAgent(agent_config)
        
        # This is the key test that was failing
        assert hasattr(agent, 'youtube')
        assert agent.youtube is not None
    
    def test_internet_archive_attribute_exists(self, agent_config: AgentConfig):
        """Test that internet_archive attribute exists."""
        agent = VideoDiscoveryAgent(agent_config)
        
        assert hasattr(agent, 'internet_archive')
        assert agent.internet_archive is not None
    
    def test_default_keywords(self):
        """Test that agent has default keywords."""
        agent = VideoDiscoveryAgent()
        
        assert hasattr(agent, 'DEFAULT_KEYWORDS')
        assert isinstance(agent.DEFAULT_KEYWORDS, list)
        assert len(agent.DEFAULT_KEYWORDS) > 0
        assert 'Epstein' in agent.DEFAULT_KEYWORDS
        assert 'Ghislaine Maxwell' in agent.DEFAULT_KEYWORDS
    
    def test_agent_id_and_version(self, agent_config: AgentConfig):
        """Test agent metadata."""
        agent = VideoDiscoveryAgent(agent_config)
        
        assert agent.AGENT_ID == 'video-discovery-v2'
        assert agent.VERSION == '2.0.0'
    
    @pytest.mark.asyncio
    async def test_search_method_exists(self, agent_config: AgentConfig):
        """Test that search method exists and is callable."""
        agent = VideoDiscoveryAgent(agent_config)
        
        assert hasattr(agent, 'search')
        assert callable(agent.search)
