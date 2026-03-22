# Tier 2: Architecture Decisions

> Key architectural choices. Read when working on DB, search, or UI.
> Rank: 2 (high priority).

## Database Architecture

- **PostgreSQL 16 + pgvector + tsvector/GIN** — one unified database
- **pgvector 0.6.0** (from apt): HNSW index handles 2.67M 768-dim vectors
- **42 tables:** 27 core DOJ + 6 Epstein Exposed + 2 FEC + 4 app + 3 system
- **10,894,625 total rows** across all tables
- **Why NOT ChromaDB/Qdrant:** Integrated into PostgreSQL, no extra infra, ACID transactions, can JOIN vector+text in one query
- **Why NOT Elasticsearch:** PostgreSQL FTS sufficient for 2.9M pages, 50-200ms latency acceptable

## PostgreSQL Configuration

- `shared_buffers = 32GB` (25% of 125GB RAM)
- `effective_cache_size = 96GB` (75% of RAM)
- `maintenance_work_mem = 8GB` (for HNSW index builds)
- `work_mem = 256MB` (for complex queries)
- `max_connections = 200`
- Config: `/etc/postgresql/16/main/postgresql.conf`

## Data Sources (Complete List)

| Source | Tables | Rows | Status |
|--------|--------|------|--------|
| DOJ EFTA (SQLite migration) | 27 | 10,889,161 | Complete |
| Epstein Exposed API | 6 | 5,464 | Partial (emails need retry) |
| FEC Open Data | 2 | 4,000 | Complete |
| HF Parquet (318GB) | — | — | On disk, not ingested |

## Epstein Exposed API

- Base: `https://epsteinexposed.com/api/v2`
- 27 endpoints, anonymous: 100 req/hr
- Bulk exports: persons, flights, locations, organizations (1 call each)
- Script: `scripts/fetch_epstein_exposed.py` (with --check, --force, --load-only)
- Remaining: 11,180 emails (paginated), network graph, DOJ audit, stats

## Processing Pipeline (Ready to Run)

| Command | Data | Status |
|---------|------|--------|
| `epstein-pipeline ocr` | 583K PDFs | Ready |
| `epstein-pipeline extract-entities` | 2.9M pages | Ready |
| `epstein-pipeline embed` | 2.9M pages | Ready (sentence-transformers installed) |
| `epstein-pipeline classify` | 2.9M pages | Ready |
| `epstein-pipeline transcribe` | Audio/video files | Ready (faster-whisper installed) |

## UI Stack

- **Datasette** on port 8001 (instant web UI over SQLite export)
- **Letta** on port 8283 (stateful AI agent with persistent memory)
- **OpenClaw** on port 18789 (multi-channel AI gateway)
