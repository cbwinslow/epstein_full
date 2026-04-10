# System Architecture

## Overview

The Epstein Research System is a multi-agent architecture for discovering, collecting, and analyzing media content related to Jeffrey Epstein. The system runs on a Linux server with GPU acceleration, with optional remote GPU endpoints for embeddings.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Linux Server (cbwinslow)                     │
│                   16 cores, 125GB RAM, Tesla K80/K40m          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │  File System │    │  GPU (Tesla) │
│  (Database)  │    │  (Storage)   │    │  (Incompatible│
│              │    │              │    │   with nomic)│
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Discovery   │    │  Collection  │    │  Processing  │
│  Agents      │    │  Agents      │    │  Agents      │
│              │    │              │    │              │
│ • GDELT      │    │ • News       │    │ • NER        │
│ • Wayback    │    │ • Video      │    │ • Embeddings │
│ • RSS        │    │ • Document   │    │ • Sentiment  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  Orchestrator│
                    │  (master.py) │
                    └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  Queue       │
                    │  (PostgreSQL)│
                    └──────────────┘
                              │
                              │ HTTP API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Windows Machine (RTX3060 GPU)                     │
│                    12GB VRAM, CUDA 11.8                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  Embeddings   │
                    │  Server       │
                    │  (FastAPI)    │
                    └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  nomic-embed  │
                    │  v2-moe       │
                    └──────────────┘
```

## Component Layers

### 1. Storage Layer
- **PostgreSQL**: Primary database for all data
  - Tables: media_news_articles, media_videos, media_documents
  - Extensions: pgvector for embeddings, pg_trgm for fuzzy search
  - Location: Separate partition on RAID array
  
- **File System**: Raw content storage
  - Path: `/home/cbwinslow/workspace/epstein-data/media/`
  - Subdirectories: articles/, videos/, documents/
  - RAID Array: 2.9TB total, 2.1TB free

### 2. Discovery Layer
Agents responsible for finding content:

- **NewsDiscoveryAgent** (`media_acquisition/agents/discovery/news.py`)
  - Sources: GDELT, Wayback Machine, 43 RSS feeds
  - Keywords: 50+ comprehensive terms
  - Output: Queued URLs in `media_collection_queue`

- **VideoDiscoveryAgent** (`media_acquisition/agents/discovery/video.py`)
  - Sources: YouTube API, Vimeo API, Internet Archive
  - Output: Video metadata in queue

- **DocumentDiscoveryAgent** (planned)
  - Sources: CourtListener, PACER, FOIA requests
  - Output: Document metadata in queue

### 3. Collection Layer
Agents responsible for downloading content:

- **NewsCollector** (`media_acquisition/agents/collection/news.py`)
  - Tools: newspaper3k, requests+BeautifulSoup
  - Output: Parsed articles in `media_news_articles`
  
- **VideoCollector** (`media_acquisition/agents/collection/video.py`)
  - Tools: yt-dlp, faster-whisper
  - Output: Videos with transcripts in `media_videos`

- **DocumentCollector** (planned)
  - Tools: PyMuPDF, OCR (Surya, Docling)
  - Output: Documents with text in `media_documents`

### 4. Processing Layer
Agents responsible for analyzing content:

- **NERAgent** (planned)
  - Tools: spaCy en_core_web_trf, GLiNER
  - Output: Entities in `entities_mentioned` JSONB
  
- **EmbeddingsAgent** (remote)
  - Tools: nomic-embed-text-v2-moe on Windows RTX3060
  - Output: 768-dim vectors in pgvector columns
  
- **SentimentAgent** (planned)
  - Tools: TextBlob, VADER
  - Output: sentiment_score, subjectivity_score
  
- **DeduplicationAgent** (planned)
  - Tools: MinHash/LSH, semantic clustering
  - Output: cluster_id, canonical_article_id

### 5. Orchestration Layer
- **MediaAcquisitionSystem** (`media_acquisition/master.py`)
  - Coordinates all agents
  - Manages queue processing
  - Handles error recovery
  - Tracks metrics

### 6. API Layer
- **Embeddings API** (Windows machine)
  - Framework: FastAPI
  - Endpoints: /embed, /embed/title, /embed/summary, /embed/content
  - Access: HTTP over LAN

## Data Flow

```
1. Discovery Phase:
   User/Script → NewsDiscoveryAgent → GDELT/Wayback/RSS 
   → media_collection_queue (status: pending)

2. Collection Phase:
   Orchestrator → NewsCollector → Download/Parse 
   → media_news_articles + file storage
   → media_collection_queue (status: completed)

3. Processing Phase:
   Orchestrator → EmbeddingsAgent (Windows GPU) 
   → media_news_articles (title_embedding, etc.)
   → NERAgent → media_news_articles (entities_mentioned)
   → SentimentAgent → media_news_articles (sentiment_score)
```

## Database Schema

### Core Tables

```sql
media_news_articles
├── id (SERIAL PRIMARY KEY)
├── source_domain, source_name
├── article_url (TEXT NOT NULL, UNIQUE)
├── title, authors, publish_date
├── content, summary, keywords
├── title_embedding (vector(768))
├── summary_embedding (vector(768))
├── content_embedding (vector(768))
├── entities_mentioned (JSONB)
├── related_person_ids (INTEGER[])
├── collection_method, extraction_method
└── timestamps

media_collection_queue
├── id (SERIAL PRIMARY KEY)
├── media_type, source_url
├── status (pending/processing/completed/failed)
├── priority, retry_count
├── discovered_by, discovery_date
└── result_id, result_metadata

media_authors
├── id (SERIAL PRIMARY KEY)
├── name, email, twitter_handle
├── affiliation, bio, beat
├── total_articles, epstein_articles
├── credibility_score
└── timestamps

media_article_authors
├── article_id (FK)
├── author_id (FK)
├── author_role, contribution_type
└── UNIQUE(article_id, author_id)
```

## Network Configuration

### Linux Server
- **Hostname**: cbwinslow/workspace/epstein
- **IP**: 192.168.1.X (LAN)
- **PostgreSQL**: localhost:5432
- **Storage**: /home/cbwinslow/workspace/epstein-data/

### Windows Machine
- **GPU**: RTX3060 (12GB VRAM)
- **IP**: 192.168.1.X (LAN)
- **Embeddings API**: http://0.0.0.0:8000
- **Model**: nomic-ai/nomic-embed-text-v2-moe

### Communication
- **Protocol**: HTTP/1.1
- **Format**: JSON
- **Authentication**: None (LAN-only)
- **Rate Limiting**: Client-side (batch requests)

## GPU Allocation

### Linux Server (Tesla K80/K40m)
- **K80 (0)**: OCR (Surya) + Image Analysis
- **K80 (1)**: Transcription (faster-whisper) + NER (spaCy trf)
- **K40m (2)**: Embeddings + Classification (overflow)
- **Issue**: Incompatible with nomic-embed-text-v2-moe

### Windows Machine (RTX3060)
- **Primary**: Embeddings generation (nomic-embed-text-v2-moe)
- **Performance**: ~50x faster than CPU
- **Access**: HTTP API from Linux server

## Performance Characteristics

### Discovery
- **RSS Feeds**: 100-500 articles/minute
- **GDELT**: 250 records/query (rate-limited)
- **Wayback**: Variable (rate-limited)

### Collection
- **News**: 20-50 articles/minute (newspaper3k)
- **Video**: 5-10 videos/minute (yt-dlp + transcription)
- **Documents**: 10-30 documents/minute (OCR)

### Processing
- **Embeddings (CPU)**: 5-10 seconds/article
- **Embeddings (RTX3060)**: 0.1-0.2 seconds/article
- **NER (GPU)**: 1-2 seconds/article
- **Sentiment**: <0.1 seconds/article

## Scalability

### Current Capacity
- **Discovery**: 10,000+ articles per run
- **Collection**: 5,000+ articles per day
- **Storage**: 2.1TB available (can store 10M+ articles)

### Bottlenecks
1. **GDELT Rate Limits**: 429 errors
2. **GPU Compatibility**: Tesla K80 too old for modern models
3. **Network Latency**: Linux to Windows for embeddings
4. **Database I/O**: Large writes during collection

### Scaling Solutions
1. **Add NewsAPI.org**: 150K+ sources
2. **Add Common Crawl**: Billions of pages
3. **Multiple GPU Workers**: Additional Windows machines
4. **Database Sharding**: Partition by date/source
5. **Queue Workers**: Celery for distributed processing

## Monitoring

### Metrics Tracked
- Articles discovered/collected/failed
- Processing time per article
- GPU utilization (nvidia-smi)
- Disk usage (df monitoring)
- Queue depth (pending items)

### Logging
- **Location**: `/home/cbwinslow/workspace/epstein/logs/`
- **Format**: JSON structured logs
- **Retention**: 30 days
- **Levels**: DEBUG, INFO, WARNING, ERROR

## Security

### Database
- **User**: cbwinslow
- **Password**: 123qweasd (CHANGE IN PRODUCTION)
- **SSL**: Disabled (LAN-only)
- **Backups**: pg_dump daily

### Network
- **LAN-only**: No external exposure
- **Firewall**: Windows port 8000 allowed
- **Authentication**: None (trusted LAN)

### Data
- **PII**: Minimal (public news articles)
- **Encryption**: None (LAN-only)
- **Access**: Single user (cbwinslow)

## Future Architecture

### Phase 2 (Short-term)
- [ ] Add NewsAPI.org integration
- [ ] Implement NER pipeline
- [ ] Add sentiment analysis
- [ ] Implement near-duplicate detection

### Phase 3 (Medium-term)
- [ ] Add Common Crawl integration
- [ ] Add social media monitoring
- [ ] Build real-time monitoring system
- [ ] Add fact-checking integration

### Phase 4 (Long-term)
- [ ] Add LexisNexis/Factiva integration
- [ ] Build ML-based duplicate detection
- [ ] Add automated summarization
- [ ] Build trend analysis dashboard
