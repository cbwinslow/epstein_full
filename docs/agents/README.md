# Agents Documentation

This directory contains comprehensive documentation for all agents in the Epstein Research System.

## Structure

```
docs/agents/
├── README.md                    # This file
├── discovery/                   # Discovery agents (find content)
│   ├── news.md                  # News discovery agent
│   ├── video.md                 # Video discovery agent
│   └── document.md             # Document discovery agent
├── collection/                 # Collection agents (download content)
│   ├── news.md                  # News collection agent
│   ├── video.md                 # Video collection agent
│   └── document.md             # Document collection agent
└── processing/                 # Processing agents (analyze content)
    ├── ner.md                   # Named Entity Recognition
    ├── embeddings.md            # Vector embeddings
    ├── sentiment.md             # Sentiment analysis
    └── deduplication.md        # Duplicate detection
```

## Agent Categories

### Discovery Agents
Agents responsible for finding and discovering content from various sources:
- **NewsDiscoveryAgent**: Discovers news articles from GDELT, Wayback Machine, RSS feeds
- **VideoDiscoveryAgent**: Discovers videos from YouTube, Vimeo, Internet Archive
- **DocumentDiscoveryAgent**: Discovers court documents, government releases, FOIA documents

### Collection Agents
Agents responsible for downloading and extracting content:
- **NewsCollector**: Downloads and parses news articles using newspaper3k, requests+BeautifulSoup
- **VideoCollector**: Downloads videos and transcribes audio using faster-whisper
- **DocumentCollector**: Downloads PDFs and extracts text using OCR

### Processing Agents
Agents responsible for analyzing and processing collected content:
- **NERAgent**: Extracts named entities (persons, organizations, locations)
- **EmbeddingsAgent**: Generates vector embeddings for semantic search
- **SentimentAgent**: Analyzes sentiment and subjectivity of content
- **DeduplicationAgent**: Detects and removes duplicate content

## Agent Configuration

All agents use the `AgentConfig` class for configuration:

```python
from media_acquisition.base import AgentConfig

config = AgentConfig(
    agent_id='my-agent',
    database_url='postgresql://user:pass@localhost:5432/db',
    storage_path='/path/to/storage',
    request_timeout=30,
    max_retries=3,
    log_level='INFO'
)
```

## Agent Execution

Agents can be executed individually or orchestrated via the `MediaAcquisitionSystem`:

```python
from media_acquisition.master import MediaAcquisitionSystem

system = MediaAcquisitionSystem(config)
results = await system.run_pipeline(
    discovery_agent='news',
    collection_agent='news',
    processing_agents=['ner', 'embeddings']
)
```

## Performance Considerations

- **Discovery**: CPU-bound, can run multiple agents in parallel
- **Collection**: I/O-bound, rate limiting required
- **Processing**: GPU-bound for embeddings and NER, CPU-bound for sentiment/dedup

## Monitoring

All agents emit metrics that can be tracked:
- `total_discovered`: Number of items discovered
- `total_collected`: Number of items successfully collected
- `total_failed`: Number of items that failed
- `processing_time_ms`: Total processing time
- `success_rate`: Percentage of successful operations

## Troubleshooting

See individual agent documentation for specific troubleshooting guides.

## Related Documentation

- [Architecture Overview](../architecture/README.md)
- [API Documentation](../api/README.md)
- [User Guides](../guides/README.md)
