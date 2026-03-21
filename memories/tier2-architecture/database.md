# Tier 2: Architecture Decisions

> Key architectural choices. Read when working on DB, search, or UI.
> Rank: 2 (high priority).

## Database Architecture

- **PostgreSQL 16 + pgvector + tsvector/GIN** — one unified database
- **pgvector 0.6.0** (from apt): HNSW index handles 2.67M 768-dim vectors
- **Why NOT ChromaDB/Qdrant:** Integrated into PostgreSQL, no extra infra, ACID transactions, can JOIN vector+text in one query
- **Why NOT Elasticsearch:** PostgreSQL FTS sufficient for 2.9M pages, 50-200ms latency acceptable
- **Why NOT Apache Kafka/Spark/Druid:** Scale doesn't justify complexity
- **Why NOT Supabase/Neon:** 600GB+ data = $75-210/mo cloud cost vs $0 self-hosted

## PostgreSQL Configuration

- `shared_buffers = 32GB` (25% of 125GB RAM)
- `effective_cache_size = 96GB` (75% of RAM)
- `maintenance_work_mem = 8GB` (for HNSW index builds)
- `work_mem = 256MB` (for complex queries)
- `max_connections = 200`
- Config: `/etc/postgresql/16/main/postgresql.conf`

## UI Stack

- **Current:** Datasette on port 8001 (instant web UI over SQLite export)
- **Upgrade path:** Streamlit → React/shadcn (when needed)
- Datasette uses SQLite export, not direct PostgreSQL connection

## Data Coverage

- **full_text_corpus.db:** 1.4M docs, 2.9M pages (most comprehensive)
- **HF parquet:** Subset of SQLite databases (not worth migrating separately)
- **Pre-built DBs:** 8 SQLite databases migrated to PostgreSQL
- **CDN downloads:** Raw PDFs for archival (separate from processed data)

## Memory System

- **mem0 cloud:** 18 ranked memories stored (semantic search across sessions)
- **Folder-based:** `memories/` directory (git-trackable, structured)
- Both systems active — mem0 for search, folders for structured reference
