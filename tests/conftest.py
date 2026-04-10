"""
Pytest configuration and fixtures for media acquisition tests.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Generator, AsyncGenerator, Optional

import pytest
import pytest_asyncio

# Add project root to path
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.base import (
    StorageManager, AgentConfig, NewsArticleURL, 
    VideoMetadata, TaskResult
)
from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.agents.discovery.video import VideoDiscoveryAgent
from media_acquisition.agents.collection.news import NewsCollector


# Database Configuration
TEST_DATABASE_URL = os.getenv(
    'TEST_DATABASE_URL',
    'postgresql://cbwinslow:123qweasd@localhost:5432/epstein_test'
)


@pytest.fixture(scope="session")
def database_url() -> str:
    """Get test database URL."""
    return TEST_DATABASE_URL


@pytest.fixture(scope="function")
def temp_media_dir() -> Generator[Path, None, None]:
    """Create temporary media directory for tests."""
    temp_dir = Path(tempfile.mkdtemp(prefix="media_test_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def storage_manager(database_url: str, temp_media_dir: Path) -> StorageManager:
    """Create StorageManager for testing."""
    return StorageManager(
        connection_string=database_url,
        base_path=str(temp_media_dir)
    )


@pytest.fixture(scope="function")
def agent_config() -> AgentConfig:
    """Create test agent configuration."""
    return AgentConfig(
        agent_id="test-agent",
        youtube_api_key="test_youtube_key",
        newsapi_key="test_newsapi_key"
    )


@pytest.fixture(scope="function")
def agent_config_no_api_keys() -> AgentConfig:
    """Create test agent configuration without API keys."""
    return AgentConfig(agent_id="test-agent-no-keys")


@pytest.fixture
def mock_gdelt_response() -> dict:
    """Sample GDELT API response."""
    return {
        "articles": [
            {
                "url": "https://example.com/article1",
                "title": "Test Article About Epstein",
                "seendate": "20240101120000",
                "domain": "example.com",
                "language": "en"
            },
            {
                "url": "https://example.com/article2",
                "title": "Another Epstein Story",
                "seendate": "20240102120000",
                "domain": "example.com",
                "language": "en"
            }
        ]
    }


@pytest.fixture
def sample_news_article() -> NewsArticleURL:
    """Create sample news article for testing."""
    return NewsArticleURL(
        url="https://example.com/test-article",
        title="Test Article",
        source_domain="example.com",
        publish_date=datetime.now(),
        priority=5,
        keywords_matched=["Epstein"],
        discovery_method="test",
        metadata={"author": "Test Author"}
    )


@pytest.fixture
def mock_youtube_response() -> list:
    """Sample YouTube API response."""
    return [
        {
            "video_id": "test123",
            "url": "https://youtube.com/watch?v=test123",
            "title": "Epstein Documentary",
            "platform": "youtube",
            "duration_seconds": 3600,
            "view_count": 100000,
            "upload_date": datetime.now(),
            "transcript_available": True,
            "discovery_method": "youtube_api"
        }
    ]


# Async fixtures
@pytest_asyncio.fixture
async def news_discovery_agent(agent_config: AgentConfig) -> NewsDiscoveryAgent:
    """Create NewsDiscoveryAgent for testing."""
    return NewsDiscoveryAgent(agent_config)


@pytest_asyncio.fixture
async def video_discovery_agent(agent_config: AgentConfig) -> VideoDiscoveryAgent:
    """Create VideoDiscoveryAgent for testing."""
    return VideoDiscoveryAgent(agent_config)


@pytest_asyncio.fixture
async def news_collector(agent_config: AgentConfig, storage_manager: StorageManager) -> NewsCollector:
    """Create NewsCollector for testing."""
    return NewsCollector(agent_config, storage_manager)


# Markers

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires database)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: mark test that requires API key"
    )
