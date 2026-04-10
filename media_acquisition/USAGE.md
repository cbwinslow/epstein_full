# Media Acquisition System - Usage Guide

## Overview

The Epstein Media Acquisition System is a comprehensive infrastructure for discovering, collecting, and processing Epstein-related media content including news articles, videos, and official documents.

## Quick Start

### 1. Test News Discovery

```bash
# Test GDELT discovery (free, no API key needed)
cd /home/cbwinslow/workspace/epstein
python -m media_acquisition.agents.discovery.news \
  --keywords Epstein Maxwell \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --max-results 50
```

### 2. Test Video Discovery

```bash
# Test YouTube + Internet Archive discovery
python -m media_acquisition.agents.discovery.video \
  --keywords Epstein \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --max-results 20
```

### 3. Test Document Discovery

```bash
# Test CourtListener + GovInfo discovery
python -m media_acquisition.agents.discovery.document \
  --keywords "Epstein Maxwell" \
  --start-date 2020-01-01 \
  --end-date 2025-12-31 \
  --max-results 100
```

### 4. Test Article Collection

```bash
# Download a specific article
python -m media_acquisition.agents.collection.news \
  "https://www.example.com/epstein-article"
```

### 5. Test Video Transcription

```bash
# Transcribe a YouTube video (uses yt-dlp captions or Whisper fallback)
python -m media_acquisition.agents.collection.video \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --strategy auto
```

### 6. Test Entity Extraction

```bash
# Analyze text for entities, sentiment, and topics
python -m media_acquisition.agents.processing.entities \
  "Jeffrey Epstein was arrested in July 2019 on federal charges..."
  --detailed
```

## Full Collection Run

### Option A: Using Master Orchestrator

```bash
# Run full historical collection
python -m media_acquisition.master \
  --mode historical \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --media-types news video document \
  --keywords Epstein Maxwell "Virginia Giuffre"
```

### Option B: Using Python API

```python
import asyncio
from media_acquisition import MediaAcquisitionSystem

async def main():
    # Initialize system
    system = MediaAcquisitionSystem()
    
    # Run collection
    await system.run_historical_collection(
        start_date='2024-01-01',
        end_date='2024-12-31',
        media_types=['news', 'video', 'document'],
        keywords=['Epstein', 'Maxwell']
    )

asyncio.run(main())
```

## Agent Reference

### Discovery Agents

| Agent | Purpose | Sources | Cost |
|-------|---------|---------|------|
| `NewsDiscoveryAgent` | Find news articles | GDELT, Wayback Machine, RSS | Free |
| `VideoDiscoveryAgent` | Find videos | YouTube, Internet Archive | Free |
| `DocumentDiscoveryAgent` | Find documents | CourtListener, GovInfo | Free |

### Collection Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| `NewsCollector` | Download articles | newspaper3k, requests+BS4 |
| `VideoTranscriber` | Transcribe videos | yt-dlp, faster-whisper |

### Processing Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| `EntityExtractor` | NER + analysis | spaCy, GLiNER, TextBlob |

## Database Schema

All media content is stored in PostgreSQL:

```sql
-- News articles
media_news_articles (id, title, content, source_domain, publish_date, ...)

-- Videos with transcripts
media_videos (id, video_id, title, transcript_text, transcript_source, ...)

-- Documents
media_documents (id, title, text_content, source, document_type, ...)

-- Collection queue
media_collection_queue (id, media_type, source_url, status, ...)

-- Entity mentions (cross-reference)
media_entity_mentions (media_type, media_id, entity_type, entity_id, ...)
```

## API Keys (Optional)

Some features work better with API keys but all agents have free alternatives:

| Service | API Key | Purpose | Free Alternative |
|---------|---------|---------|------------------|
| YouTube Data API | `YOUTUBE_API_KEY` | Better video metadata | Web scraping |
| CourtListener | `COURTLISTENER_API_KEY` | Higher rate limits | Unauthenticated (slower) |
| GovInfo | `GOVINFO_API_KEY` | Higher rate limits | Unauthenticated (slower) |

Add to `.env`:
```
YOUTUBE_API_KEY=your_key_here
COURTLISTENER_API_KEY=your_key_here
GOVINFO_API_KEY=your_key_here
```

## Troubleshooting

### Issue: No articles found
- Check date range is not too narrow
- Try different keywords
- Verify GDELT API is accessible

### Issue: Video transcription fails
- Install yt-dlp: `pip install yt-dlp`
- For Whisper fallback, install faster-whisper: `pip install faster-whisper`
- Check GPU availability for Whisper

### Issue: Database connection fails
- Verify PostgreSQL is running
- Check credentials in config
- Ensure media schema is deployed: `psql -f scripts/create_media_schema.sql`

## Monitoring Collection Progress

```sql
-- Check queue status
SELECT * FROM fn_get_queue_summary();

-- Check recent activity
SELECT * FROM v_recent_collection LIMIT 10;

-- Check media coverage timeline
SELECT * FROM v_media_coverage_timeline ORDER BY date DESC LIMIT 10;
```

## File Locations

```
media_acquisition/
├── base.py                  # Base classes
├── master.py               # Orchestrator
├── agents/
│   ├── discovery/
│   │   ├── news.py        # NewsDiscoveryAgent
│   │   ├── video.py       # VideoDiscoveryAgent
│   │   └── document.py    # DocumentDiscoveryAgent
│   ├── collection/
│   │   ├── news.py        # NewsCollector
│   │   └── video.py       # VideoTranscriber
│   └── processing/
│       └── entities.py    # EntityExtractor
└── storage/               # Storage utilities

Storage locations:
/home/cbwinslow/workspace/epstein-data/media/
├── articles/              # Downloaded articles (JSON)
├── videos/               # Video audio + transcripts
└── documents/            # Downloaded documents
```

## Next Steps

1. Run discovery to populate queue
2. Run collection to download content
3. Run processing to extract entities
4. Build cross-references to existing entities
5. Create analysis views
