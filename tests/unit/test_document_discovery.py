"""
Unit tests for DocumentDiscoveryAgent.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from media_acquisition.base import AgentConfig
from media_acquisition.agents.discovery.document import DocumentDiscoveryAgent, DocumentMetadata


class TestDocumentDiscoveryAgent:
    """Test suite for DocumentDiscoveryAgent."""
    
    def test_init(self, agent_config: AgentConfig):
        """Test agent initialization."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        assert agent is not None
        assert agent.config == agent_config
        assert agent.AGENT_ID == 'document-discovery-v2'
    
    def test_search_method_exists(self, agent_config: AgentConfig):
        """Test that search method exists."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        assert hasattr(agent, 'search')
        assert callable(agent.search)
    
    @pytest.mark.asyncio
    async def test_search_returns_documents(self, agent_config: AgentConfig):
        """Test that search returns document metadata."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        # Mock the internal search methods
        with patch.object(agent, '_search_court_listener') as mock_court:
            mock_court.return_value = [
                DocumentMetadata(
                    url='https://example.com/doc1.pdf',
                    title='Test Document 1',
                    doc_type='pdf',
                    source_domain='example.com',
                    priority=5,
                    keywords_matched=['Epstein']
                )
            ]
            
            with patch.object(agent, '_search_internet_archive') as mock_ia:
                mock_ia.return_value = [
                    DocumentMetadata(
                        url='https://archive.org/doc2.pdf',
                        title='Test Document 2',
                        doc_type='pdf',
                        source_domain='archive.org',
                        priority=5,
                        keywords_matched=['Epstein']
                    )
                ]
                
                results = await agent.search(
                    keywords=['Epstein'],
                    max_results=10
                )
                
                assert isinstance(results, list)
                assert len(results) > 0
                
                for doc in results:
                    assert isinstance(doc, DocumentMetadata)
                    assert hasattr(doc, 'url')
                    assert hasattr(doc, 'title')
                    assert hasattr(doc, 'doc_type')
    
    @pytest.mark.asyncio
    async def test_search_with_empty_results(self, agent_config: AgentConfig):
        """Test search with no results."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        with patch.object(agent, '_search_court_listener') as mock_court:
            mock_court.return_value = []
            
            with patch.object(agent, '_search_internet_archive') as mock_ia:
                mock_ia.return_value = []
                
                results = await agent.search(
                    keywords=['NonExistentKeyword12345'],
                    max_results=10
                )
                
                assert isinstance(results, list)
                assert len(results) == 0
    
    @pytest.mark.asyncio
    async def test_search_deduplication(self, agent_config: AgentConfig):
        """Test that duplicate documents are removed."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        # Create duplicate documents
        doc1 = DocumentMetadata(
            url='https://example.com/duplicate.pdf',
            title='Duplicate Document',
            doc_type='pdf',
            source_domain='example.com',
            priority=5,
            keywords_matched=['Epstein']
        )
        
        with patch.object(agent, '_search_court_listener') as mock_court:
            mock_court.return_value = [doc1]
            
            with patch.object(agent, '_search_internet_archive') as mock_ia:
                mock_ia.return_value = [doc1]  # Same document
                
                results = await agent.search(
                    keywords=['Epstein'],
                    max_results=10
                )
                
                # Should deduplicate
                assert len(results) == 1
    
    def test_default_keywords(self):
        """Test that agent has default keywords."""
        agent = DocumentDiscoveryAgent()
        
        assert hasattr(agent, 'DEFAULT_KEYWORDS')
        assert isinstance(agent.DEFAULT_KEYWORDS, list)
        assert len(agent.DEFAULT_KEYWORDS) > 0
        assert 'Epstein' in agent.DEFAULT_KEYWORDS
    
    def test_supported_doc_types(self, agent_config: AgentConfig):
        """Test supported document types."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        assert hasattr(agent, 'SUPPORTED_DOC_TYPES')
        assert isinstance(agent.SUPPORTED_DOC_TYPES, list)
        assert 'pdf' in agent.SUPPORTED_DOC_TYPES
        assert 'doc' in agent.SUPPORTED_DOC_TYPES
    
    @pytest.mark.asyncio
    async def test_court_listener_search(self, agent_config: AgentConfig):
        """Test CourtListener search functionality."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        with patch('media_acquisition.agents.discovery.document.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'results': [
                    {
                        'absolute_url': '/docket/12345/government-v-epstein/',
                        'date_created': '2024-01-01T00:00:00Z',
                        'description': 'Test case'
                    }
                ]
            }
            mock_response.status_code = 200
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            results = await agent._search_court_listener(
                keywords=['Epstein'],
                max_results=10
            )
            
            assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_internet_archive_search(self, agent_config: AgentConfig):
        """Test Internet Archive search functionality."""
        agent = DocumentDiscoveryAgent(agent_config)
        
        with patch('media_acquisition.agents.discovery.document.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'response': {
                    'docs': [
                        {
                            'identifier': 'epstein-files-001',
                            'title': 'Epstein Files',
                            'mediatype': 'texts'
                        }
                    ]
                }
            }
            mock_response.status_code = 200
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            results = await agent._search_internet_archive(
                keywords=['Epstein'],
                max_results=10
            )
            
            assert isinstance(results, list)
