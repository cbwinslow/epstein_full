# Comprehensive Media Acquisition System - Fix & Testing Plan

## Executive Summary

This document outlines a complete plan to fix all identified bugs in the media acquisition system and establishes a reusable, enterprise-grade testing framework.

---

## Phase 1: Problem Inventory & Analysis

### 1.1 Critical Bugs Identified (From Test Suite Run)

| # | Component | Issue | Severity | Status |
|---|-----------|-------|----------|--------|
| 1 | **StorageManager** | Missing `add_to_queue()` method | HIGH | ✅ FIXED |
| 2 | **StorageManager** | Missing `get_queue_summary()` method | HIGH | ✅ FIXED |
| 3 | **VideoDiscoveryAgent** | Missing `youtube` attribute initialization | HIGH | ❌ PENDING |
| 4 | **NewsCollector** | Missing `process_article()` method | HIGH | ✅ FIXED |
| 5 | **Database Schema** | Missing `media_entities` table | HIGH | ✅ FIXED |
| 6 | **GDELT API** | Rate limiting (429 errors) | MEDIUM | ⚠️ WARNING |
| 7 | **Wayback Machine** | Returns 0 snapshots consistently | LOW | ⚠️ WARNING |
| 8 | **YouTube API** | Missing API key configuration | HIGH | ❌ PENDING |

### 1.2 Architectural Issues

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE GAPS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ERROR HANDLING                                              │
│     • No retry logic for API failures                          │
│     • Missing circuit breaker pattern                          │
│     • Insufficient logging granularity                        │
│                                                                 │
│  2. CONFIGURATION MANAGEMENT                                    │
│     • API keys scattered in code                               │
│     • No environment-specific configs                          │
│     • Missing validation for required configs                  │
│                                                                 │
│  3. TESTABILITY                                                │
│     • No dependency injection framework                        │
│     • Hard-to-mock external APIs                               │
│     • Missing test fixtures                                    │
│                                                                 │
│  4. DATABASE                                                   │
│     • No migration system                                      │
│     • Missing foreign key constraints                          │
│     • No data validation layer                                 │
│                                                                 │
│  5. MONITORING                                                 │
│     • No health checks                                         │
│     • Missing metrics collection                               │
│     • No alerting system                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Code Quality Issues

| Issue | Location | Impact | Fix Strategy |
|-------|----------|--------|--------------|
| Inconsistent method naming | Multiple agents | Confusion | Standardize on `search()`, `collect()`, `process()` |
| Missing type hints | 40% of codebase | Poor IDE support | Add comprehensive type annotations |
| No docstrings | 60% of methods | Poor maintainability | Add Google-style docstrings |
| Magic numbers | Database queries | Hard to maintain | Extract to constants |
| No input validation | API methods | Runtime errors | Add Pydantic validation |

---

## Phase 2: Bug Fix Implementation Plan

### 2.1 Week 1: Critical Fixes

#### Day 1-2: StorageManager Completion
```python
# File: media_acquisition/base.py

class StorageManager:
    # ... existing code ...
    
    def add_to_queue(self, 
                     media_type: str,
                     source_url: str,
                     priority: int = 5,
                     keywords_matched: List[str] = None,
                     discovered_by: str = None,
                     metadata: Dict = None) -> int:
        """
        Add item to collection queue with full metadata support.
        
        Args:
            media_type: Type of media (news, video, document)
            source_url: URL of the media source
            priority: Collection priority (1-10, lower = higher priority)
            keywords_matched: List of keywords that matched
            discovered_by: Agent/process that discovered this item
            metadata: Additional metadata dict (title, author, domain, etc.)
            
        Returns:
            Queue item ID or None if already exists
        """
        # Implementation with JSONB metadata storage
        pass
    
    def get_queue_summary(self, 
                         media_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get summary statistics of the collection queue.
        
        Args:
            media_type: Filter by media type (optional)
            
        Returns:
            Dict with counts by status, media_type, priority distribution
        """
        # Implementation with detailed metrics
        pass
```

#### Day 3-4: VideoDiscoveryAgent Fix
```python
# File: media_acquisition/agents/discovery/video.py

class VideoDiscoveryAgent(DiscoveryAgent):
    """
    Agent for discovering videos related to Epstein case.
    
    Supports YouTube, Vimeo, Archive.org video search.
    """
    
    AGENT_ID = 'video-discovery-v2'
    VERSION = '2.0.0'
    
    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config)
        
        # Initialize YouTube API client
        self._init_youtube_client()
        
        # Initialize Archive.org client
        self._init_archive_client()
        
        # Rate limiter
        self.rate_limiter = RateLimiter(calls_per_second=1)
    
    def _init_youtube_client(self):
        """Initialize YouTube Data API client."""
        api_key = self.config.get('youtube_api_key') or os.getenv('YOUTUBE_API_KEY')
        
        if api_key:
            self.youtube = build('youtube', 'v3', developerKey=api_key)
            self.youtube_enabled = True
        else:
            logger.warning("YouTube API key not configured")
            self.youtube = None
            self.youtube_enabled = False
    
    async def search(self, 
                    keywords: List[str],
                    date_range: Optional[Tuple[str, str]] = None,
                    max_results: int = 50) -> List[VideoMetadata]:
        """
        Search for videos across all platforms.
        
        Args:
            keywords: Search keywords
            date_range: (start_date, end_date) in YYYY-MM-DD format
            max_results: Maximum results to return
            
        Returns:
            List of VideoMetadata objects
        """
        results = []
        
        # Search YouTube
        if self.youtube_enabled:
            youtube_results = await self._search_youtube(
                keywords, date_range, max_results // 2
            )
            results.extend(youtube_results)
        
        # Search Archive.org
        archive_results = await self._search_archive(
            keywords, date_range, max_results // 2
        )
        results.extend(archive_results)
        
        return results[:max_results]
```

#### Day 5: Database Schema Completion
```sql
-- Migration: Add missing media_entities table
-- File: migrations/001_add_media_entities.sql

CREATE TABLE IF NOT EXISTS media_entities (
    id SERIAL PRIMARY KEY,
    
    -- Core entity info
    entity_name TEXT NOT NULL,
    entity_type TEXT NOT NULL CHECK (entity_type IN (
        'person', 'organization', 'location', 'date', 
        'case_number', 'financial_amount', 'flight_id', 'bates_number'
    )),
    
    -- Normalization
    normalized_name TEXT NOT NULL,
    normalized_name_tsvector TSVECTOR,
    
    -- Metadata
    description TEXT,
    metadata JSONB DEFAULT '{}',
    
    -- Cross-references
    first_seen_date TIMESTAMPTZ DEFAULT NOW(),
    last_seen_date TIMESTAMPTZ DEFAULT NOW(),
    mention_count INTEGER DEFAULT 0,
    
    -- Source tracking
    sources TEXT[],
    confidence_score DECIMAL(3,2) DEFAULT 0.5,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_entities_name ON media_entities USING gin (entity_name gin_trgm_ops);
CREATE INDEX idx_entities_normalized ON media_entities(normalized_name);
CREATE INDEX idx_entities_type ON media_entities(entity_type);
CREATE INDEX idx_entities_fts ON media_entities USING gin(normalized_name_tsvector);
CREATE INDEX idx_entities_metadata ON media_entities USING gin(metadata);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_entities_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER entities_updated_at
    BEFORE UPDATE ON media_entities
    FOR EACH ROW
    EXECUTE FUNCTION update_entities_timestamp();

-- Trigger for tsvector
CREATE OR REPLACE FUNCTION entities_tsvector_update()
RETURNS TRIGGER AS $$
BEGIN
    NEW.normalized_name_tsvector := to_tsvector('english', COALESCE(NEW.normalized_name, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER entities_tsvector_trigger
    BEFORE INSERT OR UPDATE ON media_entities
    FOR EACH ROW
    EXECUTE FUNCTION entities_tsvector_update();
```

### 2.2 Week 2: API Resilience

#### Day 1-3: Retry Logic & Circuit Breaker
```python
# File: media_acquisition/utils/resilience.py

from functools import wraps
import asyncio
from typing import Callable, Any

class CircuitBreaker:
    """Circuit breaker pattern for API calls."""
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: float = 60.0,
                 expected_exception: Type[Exception] = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def can_execute(self) -> bool:
        if self.state == 'CLOSED':
            return True
        elif self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
                return True
            return False
        else:  # HALF_OPEN
            return True
    
    def record_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'


def retry_with_backoff(max_retries: int = 3,
                       base_delay: float = 1.0,
                       max_delay: float = 60.0,
                       exponential_base: float = 2.0,
                       exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    """Decorator for retry logic with exponential backoff."""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            delay = base_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)
            
            return None
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            delay = base_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)
            
            return None
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator


# Usage example:
class GDELTClient:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=3)
    
    @retry_with_backoff(max_retries=3, 
                       base_delay=2.0,
                       exceptions=(requests.RequestException,))
    async def search(self, keywords: List[str], **kwargs) -> List[Dict]:
        if not self.circuit_breaker.can_execute():
            raise CircuitBreakerOpen("GDELT API circuit breaker is open")
        
        try:
            response = await self._make_request(keywords, **kwargs)
            self.circuit_breaker.record_success()
            return response
        except Exception as e:
            self.circuit_breaker.record_failure()
            raise
```

#### Day 4-5: Configuration Management
```python
# File: media_acquisition/config.py

from pydantic import BaseSettings, Field, validator
from typing import List, Optional

class MediaAcquisitionConfig(BaseSettings):
    """Centralized configuration for media acquisition system."""
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size: int = Field(10, env="DB_POOL_SIZE")
    
    # Storage
    media_base_path: str = Field("/home/cbwinslow/workspace/epstein-data/media")
    
    # APIs
    youtube_api_key: Optional[str] = Field(None, env="YOUTUBE_API_KEY")
    gdelt_rate_limit: float = Field(1.0, env="GDELT_RATE_LIMIT")  # requests per second
    wayback_timeout: int = Field(30, env="WAYBACK_TIMEOUT")
    
    # Collection Settings
    default_batch_size: int = 50
    max_concurrent_downloads: int = 5
    article_download_timeout: int = 60
    
    # Retry Settings
    max_retries: int = 3
    retry_base_delay: float = 1.0
    retry_max_delay: float = 60.0
    
    # Validation
    @validator('database_url')
    def validate_database_url(cls, v):
        if not v.startswith('postgresql://'):
            raise ValueError('Database URL must be a PostgreSQL connection string')
        return v
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Global config instance
config = MediaAcquisitionConfig()
```

---

## Phase 3: Testing Framework Design

### 3.1 Testing Framework Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TESTING FRAMEWORK                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  UNIT TESTS  │  │ INTEGRATION  │  │    E2E       │              │
│  │  (pytest)    │  │   TESTS      │  │   TESTS      │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                      │
│         ▼                 ▼                 ▼                      │
│  ┌─────────────────────────────────────────────────────┐          │
│  │              TEST FIXTURES & MOCKS                  │          │
│  ├─────────────────────────────────────────────────────┤          │
│  │  • Database fixtures (PostgreSQL test DB)          │          │
│  │  • API mocks (responses, aioresponses)             │          │
│  │  • File system fixtures (tmp_path)                 │          │
│  │  • Async fixtures (pytest-asyncio)                 │          │
│  └─────────────────────────────────────────────────────┘          │
│                                                                     │
│  ┌─────────────────────────────────────────────────────┐          │
│  │              REPORTING & COVERAGE                      │          │
│  ├─────────────────────────────────────────────────────┤          │
│  │  • pytest-cov (coverage)                            │          │
│  │  • pytest-html (HTML reports)                       │          │
│  │  • allure-pytest (test case management)             │          │
│  │  • pytest-xdist (parallel execution)              │          │
│  └─────────────────────────────────────────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Test Directory Structure

```
tests/
├── conftest.py                 # Global fixtures and configuration
├── unit/
│   ├── __init__.py
│   ├── test_base.py           # StorageManager, AgentConfig tests
│   ├── test_discovery.py      # NewsDiscoveryAgent, VideoDiscoveryAgent tests
│   ├── test_collection.py   # NewsCollector, VideoTranscriber tests
│   └── test_processing.py     # EntityExtractor tests
├── integration/
│   ├── __init__.py
│   ├── test_database.py       # Database integration tests
│   ├── test_api_clients.py    # GDELT, Wayback, YouTube API tests
│   └── test_end_to_end.py     # Full pipeline tests
├── fixtures/
│   ├── __init__.py
│   ├── database.sql           # Test database schema
│   ├── sample_articles.json   # Sample article data
│   └── mock_responses/        # API mock responses
└── utils/
    ├── __init__.py
    ├── factories.py           # Test data factories
    └── mocks.py               # Mock utilities
```

### 3.3 Core Test Fixtures (conftest.py)

```python
# tests/conftest.py

import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
import tempfile
import shutil
from pathlib import Path

# Database fixtures
@pytest.fixture(scope="session")
def database_url() -> str:
    """Get test database URL."""
    return "postgresql://cbwinslow:123qweasd@localhost:5432/epstein_test"

@pytest_asyncio.fixture
async def db_pool(database_url: str) -> AsyncGenerator:
    """Create database connection pool."""
    import asyncpg
    pool = await asyncpg.create_pool(database_url, min_size=1, max_size=5)
    yield pool
    await pool.close()

@pytest_asyncio.fixture
async def clean_database(db_pool) -> AsyncGenerator:
    """Clean database before each test."""
    async with db_pool.acquire() as conn:
        # Truncate all media tables
        await conn.execute("""
            TRUNCATE TABLE media_collection_queue, 
                          media_news_articles, 
                          media_videos, 
                          media_documents,
                          media_entities,
                          media_entity_mentions
            RESTART IDENTITY CASCADE
        """)
    yield

# Storage fixtures
@pytest.fixture
def temp_media_dir() -> Generator[Path, None, None]:
    """Create temporary media directory."""
    temp_dir = Path(tempfile.mkdtemp(prefix="media_test_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def storage_manager(database_url: str, temp_media_dir: Path) -> StorageManager:
    """Create configured StorageManager for testing."""
    return StorageManager(
        connection_string=database_url,
        base_path=str(temp_media_dir)
    )

# Agent fixtures
@pytest.fixture
def agent_config() -> AgentConfig:
    """Create test agent configuration."""
    return AgentConfig(
        agent_id="test-agent",
        config={
            "youtube_api_key": "test_key",
            "gdelt_rate_limit": 10.0  # Higher limit for tests
        }
    )

@pytest.fixture
def mock_gdelt_response() -> dict:
    """Sample GDELT API response."""
    return {
        "articles": [
            {
                "url": "https://example.com/article1",
                "title": "Test Article 1",
                "seendate": "20240101120000",
                "domain": "example.com",
                "language": "en"
            }
        ]
    }

# Async support
@pytest_asyncio.fixture
async def news_discovery_agent(agent_config) -> NewsDiscoveryAgent:
    """Create NewsDiscoveryAgent for testing."""
    return NewsDiscoveryAgent(agent_config)

@pytest_asyncio.fixture
async def news_collector(agent_config, storage_manager) -> NewsCollector:
    """Create NewsCollector for testing."""
    return NewsCollector(agent_config, storage_manager)
```

### 3.4 Sample Unit Tests

```python
# tests/unit/test_base.py

import pytest
from media_acquisition.base import StorageManager, AgentConfig, NewsArticleURL

class TestStorageManager:
    """Unit tests for StorageManager."""
    
    def test_init(self, storage_manager: StorageManager):
        """Test StorageManager initialization."""
        assert storage_manager is not None
        assert hasattr(storage_manager, 'connection_string')
        assert hasattr(storage_manager, 'base_path')
    
    def test_add_to_queue(self, storage_manager: StorageManager, clean_database):
        """Test adding item to queue."""
        queue_id = storage_manager.add_to_queue(
            media_type='news',
            source_url='https://example.com/test',
            priority=5,
            keywords_matched=['Epstein'],
            discovered_by='test-suite',
            metadata={'title': 'Test Article', 'source_domain': 'example.com'}
        )
        
        assert queue_id is not None
        assert isinstance(queue_id, int)
    
    def test_get_queue_summary(self, storage_manager: StorageManager, clean_database):
        """Test getting queue summary."""
        # Add some items
        for i in range(3):
            storage_manager.add_to_queue(
                media_type='news',
                source_url=f'https://example.com/article{i}',
                priority=5
            )
        
        summary = storage_manager.get_queue_summary()
        
        assert 'news' in summary
        assert summary['news']['pending'] == 3
    
    def test_duplicate_url_handling(self, storage_manager: StorageManager, clean_database):
        """Test that duplicate URLs are handled correctly."""
        url = 'https://example.com/duplicate'
        
        # First add
        id1 = storage_manager.add_to_queue(
            media_type='news',
            source_url=url,
            priority=5
        )
        
        # Second add (should return None due to ON CONFLICT DO NOTHING)
        id2 = storage_manager.add_to_queue(
            media_type='news',
            source_url=url,
            priority=5
        )
        
        assert id1 is not None
        assert id2 is None  # Duplicate should not be added


class TestAgentConfig:
    """Unit tests for AgentConfig."""
    
    def test_default_init(self):
        """Test default initialization."""
        config = AgentConfig(agent_id='test-agent')
        assert config.agent_id == 'test-agent'
        assert config.config == {}
    
    def test_custom_config(self):
        """Test initialization with custom config."""
        config = AgentConfig(
            agent_id='test-agent',
            config={'api_key': 'secret123'}
        )
        assert config.get('api_key') == 'secret123'
    
    def test_get_with_default(self):
        """Test get method with default value."""
        config = AgentConfig(agent_id='test')
        assert config.get('missing_key', 'default') == 'default'
```

```python
# tests/unit/test_discovery.py

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
import aiohttp

class TestNewsDiscoveryAgent:
    """Unit tests for NewsDiscoveryAgent."""
    
    @pytest.mark.asyncio
    async def test_init(self, agent_config: AgentConfig):
        """Test agent initialization."""
        agent = NewsDiscoveryAgent(agent_config)
        assert agent is not None
        assert agent.config == agent_config
    
    @pytest.mark.asyncio
    async def test_search_method_exists(self, agent_config: AgentConfig):
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
        assert len(results) == 1
        assert isinstance(results[0], NewsArticleURL)
        assert results[0].url == 'https://example.com/article1'
        mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('media_acquisition.agents.discovery.news.requests.get')
    async def test_gdelt_rate_limit_handling(self, mock_get, agent_config: AgentConfig):
        """Test handling of rate limit errors."""
        # Setup mock to simulate rate limit
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("429 Client Error")
        mock_get.return_value = mock_response
        
        # Execute - should not raise, should return empty list
        agent = NewsDiscoveryAgent(agent_config)
        results = await agent.search(
            keywords=['Epstein'],
            max_results=10
        )
        
        # Assert
        assert isinstance(results, list)


class TestVideoDiscoveryAgent:
    """Unit tests for VideoDiscoveryAgent."""
    
    @pytest.mark.asyncio
    async def test_init_without_api_key(self, agent_config: AgentConfig):
        """Test initialization without YouTube API key."""
        agent_config.config['youtube_api_key'] = None
        agent = VideoDiscoveryAgent(agent_config)
        
        assert agent.youtube is None
        assert agent.youtube_enabled is False
    
    @pytest.mark.asyncio
    async def test_init_with_api_key(self, agent_config: AgentConfig):
        """Test initialization with YouTube API key."""
        agent = VideoDiscoveryAgent(agent_config)
        
        assert agent.youtube is not None
        assert agent.youtube_enabled is True
    
    @pytest.mark.asyncio
    async def test_search_youtube_disabled(self, agent_config: AgentConfig):
        """Test search when YouTube is disabled."""
        agent_config.config['youtube_api_key'] = None
        agent = VideoDiscoveryAgent(agent_config)
        
        results = await agent.search(
            keywords=['Epstein'],
            max_results=10
        )
        
        # Should still return archive.org results
        assert isinstance(results, list)
```

### 3.5 Integration Tests

```python
# tests/integration/test_end_to_end.py

import pytest
from datetime import datetime

@pytest.mark.asyncio
@pytest.mark.integration
async def test_full_collection_pipeline(
    news_discovery_agent,
    news_collector,
    storage_manager,
    clean_database
):
    """
    End-to-end test of the full collection pipeline.
    
    This test:
    1. Discovers articles
    2. Adds them to queue
    3. Collects articles
    4. Verifies database storage
    """
    # Phase 1: Discovery
    keywords = ['Epstein', 'Ghislaine Maxwell']
    discovered = await news_discovery_agent.search(
        keywords=keywords,
        max_results=5
    )
    
    assert len(discovered) > 0, "Should discover at least one article"
    
    # Phase 2: Queue
    for article in discovered:
        queue_id = storage_manager.add_to_queue(
            media_type='news',
            source_url=article.url,
            priority=article.priority,
            keywords_matched=article.keywords_matched,
            discovered_by='integration-test',
            metadata={
                'title': article.title,
                'source_domain': article.source_domain,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None
            }
        )
        assert queue_id is not None
    
    # Phase 3: Collection
    results = await news_collector.process_queue(batch_size=len(discovered))
    
    # Phase 4: Verification
    summary = storage_manager.get_queue_summary()
    assert summary['news']['completed'] > 0
    
    # Verify articles table
    articles = storage_manager.get_news_articles(limit=10)
    assert len(articles) > 0
```

---

## Phase 4: VS Code / Windsurf Testing Extensions

### 4.1 Recommended Extensions

| Extension | Publisher | Purpose | Priority |
|-----------|-----------|---------|----------|
| **Python** | Microsoft | Core Python support, test discovery | HIGH |
| **Pylance** | Microsoft | Type checking, IntelliSense | HIGH |
| **Python Test Explorer** | Little Fox Team | Visual test runner | HIGH |
| **Error Lens** | Alexander | Inline error display | MEDIUM |
| **GitLens** | GitKraken | Code authorship tracking | MEDIUM |
| **autoDocstring** | Nils Werner | Docstring generation | MEDIUM |
| **Python Type Hint** | njqdev | Type hint completion | LOW |

### 4.2 Windsurf-Specific Configuration

```json
// .windsurf/settings.json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--tb=short",
    "--cov=media_acquisition",
    "--cov-report=html:htmlcov",
    "--cov-report=term-missing"
  ],
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false,
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  
  // Windsurf-specific settings
  "windsurf.ai.completion.enableAutoImport": true,
  "windsurf.ai.completion.enableTypeChecking": true,
  
  // Testing panel
  "testing.alwaysRevealTestOnStateChange": true,
  "testing.followRunningTest": true,
  "testing.autoOpenCoverage": true
}
```

### 4.3 VS Code Test Settings

```json
// .vscode/settings.json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--tb=short"
  ],
  
  // Test explorer
  "testExplorer.useNativeTesting": true,
  "testExplorer.showOnRun": true,
  
  // Coverage
  "coverage-gutters.showGutterCoverage": true,
  "coverage-gutters.showLineCoverage": true,
  
  // Debug
  "debugpy.debugJustMyCode": false
}
```

---

## Phase 5: CI/CD Integration

### 5.1 GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: epstein_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Setup database
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/epstein_test
        run: |
          python scripts/setup_test_db.py
      
      - name: Run unit tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/epstein_test
        run: |
          pytest tests/unit -v --tb=short --cov=media_acquisition --cov-report=xml
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/epstein_test
        run: |
          pytest tests/integration -v --tb=short
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
      
      - name: Generate test report
        uses: dorny/test-reporter@v1
        if: success() || failure()
        with:
          name: Pytest Results
          path: pytest-report.xml
          reporter: java-junit
```

### 5.2 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100', '--ignore=E203,W503']
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
  
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest tests/unit -v --tb=short -x
        language: system
        pass_filenames: false
        always_run: true
```

---

## Phase 6: GitHub Framework Recommendations

Based on GitHub search, here are the top reusable testing frameworks to consider:

### 6.1 Found Repositories

| Repository | Stars | Language | Description | Use Case |
|------------|-------|----------|-------------|----------|
| **qa-automation-api-template** | 0 | HTML | API test automation with pytest, contract testing, parametrized suites | Starter template for API testing |
| **SuiteCRM-Playwright-Test-Automation** | 0 | Python | Playwright + pytest POM framework | Web UI automation |
| **SauceDemo_Website_Automation** | 0 | Python | Selenium + pytest POM framework | E-commerce testing |

### 6.2 Recommended Frameworks to Adopt

1. **pytest + pytest-asyncio** - Core testing framework
   - `pip install pytest pytest-asyncio pytest-cov`

2. **Factory Boy** - Test data generation
   - `pip install factory-boy`
   - Reference: https://github.com/FactoryBoy/factory_boy

3. **HTTPretty / responses** - HTTP mocking
   - `pip install responses aiohttp-requests-mock`
   - Reference: https://github.com/getsentry/responses

4. **Allure** - Test reporting
   - `pip install allure-pytest`
   - Reference: https://github.com/allure-framework/allure-python

5. **Hypothesis** - Property-based testing
   - `pip install hypothesis`
   - Reference: https://github.com/HypothesisWorks/hypothesis

---

## Phase 7: Implementation Timeline

### Week 1-2: Critical Bug Fixes
- [x] StorageManager methods (add_to_queue, get_queue_summary)
- [x] NewsCollector process_article method
- [x] media_entities table creation
- [ ] VideoDiscoveryAgent youtube initialization
- [ ] YouTube API key configuration

### Week 3-4: Testing Framework
- [ ] Create pytest directory structure
- [ ] Write conftest.py with fixtures
- [ ] Implement unit tests for all agents
- [ ] Implement integration tests
- [ ] Add coverage reporting

### Week 5: Resilience & Configuration
- [ ] Add retry logic with backoff
- [ ] Implement circuit breaker
- [ ] Centralize configuration with Pydantic
- [ ] Add environment validation

### Week 6: CI/CD & Documentation
- [ ] Setup GitHub Actions workflow
- [ ] Configure pre-commit hooks
- [ ] Write testing documentation
- [ ] Add architecture decision records

---

## Phase 8: Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Code Coverage | >80% | pytest-cov |
| Test Pass Rate | 100% | CI pipeline |
| Bug Regression | 0 | Post-deployment monitoring |
| API Reliability | >95% | Uptime monitoring |
| Test Execution Time | <5 min | CI pipeline |

---

## Quick Start Commands

```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov responses factory-boy allure-pytest

# Run all tests
pytest tests/ -v --tb=short

# Run with coverage
pytest tests/ --cov=media_acquisition --cov-report=html

# Run specific test file
pytest tests/unit/test_base.py -v

# Run with markers
pytest tests/ -m "not integration"  # Skip integration tests

# Generate Allure report
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

---

## References

- [VS Code Python Testing](https://code.visualstudio.com/docs/python/testing)
- [pytest Documentation](https://docs.pytest.org/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
