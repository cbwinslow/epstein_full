# Media Acquisition Test Suite

## Overview

This directory contains comprehensive tests for the media acquisition system, including unit tests, integration tests, and end-to-end workflows.

## Structure

```
tests/
├── conftest.py              # Global fixtures and configuration
├── unit/                    # Unit tests (fast, isolated)
│   ├── test_storage_manager.py
│   ├── test_news_discovery.py
│   └── test_video_discovery.py
├── integration/             # Integration tests (requires database)
│   └── test_database.py
└── fixtures/                # Test data and mock responses
```

## Running Tests

### Install Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Unit Tests Only

```bash
pytest tests/unit -v
```

### Run Integration Tests

```bash
pytest tests/integration -v -m integration
```

### Run with Coverage

```bash
pytest tests/ --cov=media_acquisition --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/unit/test_video_discovery.py -v
```

### Run Specific Test

```bash
pytest tests/unit/test_video_discovery.py::TestVideoDiscoveryAgent::test_youtube_attribute_exists -v
```

## Test Categories

### Markers

- `unit`: Fast unit tests (default)
- `integration`: Tests requiring database/external services
- `slow`: Tests that take longer to run
- `requires_api_key`: Tests requiring API keys

### Running Tests by Marker

```bash
# Exclude integration tests
pytest tests/ -m "not integration"

# Run only integration tests
pytest tests/ -m integration

# Run slow tests
pytest tests/ -m slow
```

## Fixtures

### Available Fixtures

- `storage_manager`: Configured StorageManager instance
- `agent_config`: AgentConfig with test API keys
- `agent_config_no_api_keys`: AgentConfig without API keys
- `news_discovery_agent`: NewsDiscoveryAgent instance
- `video_discovery_agent`: VideoDiscoveryAgent instance
- `news_collector`: NewsCollector instance
- `sample_news_article`: Sample NewsArticleURL
- `temp_media_dir`: Temporary directory for media files

### Database Fixture

Tests requiring database access use the `TEST_DATABASE_URL` environment variable:

```bash
export TEST_DATABASE_URL="postgresql://user:pass@localhost:5432/epstein_test"
pytest tests/integration -v
```

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_my_feature.py
import pytest

class TestMyFeature:
    def test_something(self, storage_manager):
        # Use fixtures from conftest.py
        result = storage_manager.do_something()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_feature(self, news_discovery_agent):
        result = await news_discovery_agent.search(...)
        assert len(result) > 0
```

### Integration Test Example

```python
# tests/integration/test_feature.py
import pytest

@pytest.mark.integration
class TestDatabaseFeature:
    def test_database_operation(self, storage_manager):
        # This test requires database connection
        result = storage_manager.get_queue_summary()
        assert isinstance(result, dict)
```

## Mocking

### Mock External APIs

```python
from unittest.mock import Mock, patch

@patch('media_acquisition.agents.discovery.news.requests.get')
def test_gdelt_search(mock_get, agent_config):
    mock_response = Mock()
    mock_response.json.return_value = {"articles": []}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    agent = NewsDiscoveryAgent(agent_config)
    results = agent.search(...)
    assert len(results) == 0
```

## CI/CD

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main`

See `.github/workflows/test.yml` for configuration.

## Troubleshooting

### Database Connection Issues

1. Ensure PostgreSQL is running
2. Check database URL in environment variables
3. Verify database exists and is accessible

### Import Errors

1. Ensure project root is in PYTHONPATH
2. Install all dependencies: `pip install -r requirements.txt -r requirements-test.txt`

### Test Discovery Issues

1. Check file names start with `test_`
2. Check class names start with `Test`
3. Check function names start with `test_`

## Code Coverage

Current coverage targets:
- Overall: >80%
- Critical paths: >90%

View coverage report:
```bash
pytest tests/ --cov=media_acquisition --cov-report=html
open htmlcov/index.html
```
