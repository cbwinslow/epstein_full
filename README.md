# Epstein Full — Complete Download, Processing & Analysis Pipeline

A comprehensive toolkit for downloading, processing, and analyzing the DOJ Jeffrey Epstein document releases (Epstein Files Transparency Act, H.R. 4405).

## 🎯 Project Status: FULLY IMPLEMENTED ✅

**As of March 23, 2026:**
- ✅ **Complete infrastructure** with GPU acceleration (2x Tesla K80, 1x Tesla K40m)
- ✅ **Full data acquisition** from all major sources (DOJ, HuggingFace, pre-built databases)
- ✅ **Operational processing pipeline** with multi-threading and real-time monitoring
- ✅ **PostgreSQL integration** with 1.4M documents indexed and pgvector support
- ✅ **Entity extraction** with 17,080 entities from 700+ processed files
- ✅ **Knowledge graph** with 606 entities and 2,302 relationships

**Current Processing Status:**
- 🔄 **Active**: Datasets 1-7, 9-11 processed (700 files, 17,080 entities)
- ⬜ **Pending**: Datasets 8, 12 (remaining ~200K files)
- 🎯 **Target**: Full 1.4M document dataset processing

## What This Does

- **Downloads** all 12 DOJ datasets (~1.4M documents, ~218GB) using CDN mirrors and parallel aria2c
- **Processes** PDFs with OCR, extracts entities with NLP, builds knowledge graphs
- **Analyzes** extracted text, images, communications, and redactions
- **Exposes** pre-built SQLite databases with FTS5 full-text search

## Architecture

```
DOJ Website / RollCall CDN / Archive.org / HuggingFace
        │
        ▼
  Download Layer (Playwright + aria2c)
        │
        ▼
  Raw PDFs + HF Parquet (pre-extracted text)
        │
        ▼
  Processing Layer (OCR → NER → Embeddings → KG)
        │
        ▼
  SQLite Databases (FTS5 search, knowledge graph, analytics)
```

## Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/cbwinslow/epstein_full.git
cd epstein_full

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -e Epstein-Pipeline[all] spacy pymupdf aiohttp playwright rich huggingface_hub datasets pyarrow
python -m spacy download en_core_web_sm
playwright install chromium

# Download databases (pre-built, ~8GB)
# See docs/DATA_SOURCES.md for download commands

# Launch live dashboard
python scripts/dashboard.py

# Start CDN downloads
python scripts/download_cdn.py --datasets 9,10,11

# Explore knowledge graph
python scripts/explore_kg.py "Epstein"
```

## Project Structure

```
epstein_full/
├── scripts/
│   ├── ingestion/              # Data ingestion & collection
│   │   ├── mega_parallel_ingestion.py    # High-throughput news ingestion
│   │   ├── staged_news_ingestion.py      # Phased news collection
│   │   ├── run_news_ingestion.py         # News ingestion runner
│   │   ├── run_media_acquisition.py      # Media file acquisition
│   │   ├── article_ingestion_pipeline.py # Article pipeline
│   │   ├── import_*.py           # Various import scripts
│   │   └── postgresql_processor.py       # PostgreSQL ingestion
│   ├── processing/             # NLP & analysis
│   │   ├── extract_entities.py # Named entity extraction
│   │   ├── generate_embeddings.py        # Embedding generation
│   │   ├── batch_ner_extraction.py     # Batch NER processing
│   │   ├── embed_*.py          # CPU/GPU embedding variants
│   │   ├── vectorize_documents.py        # Document vectorization
│   │   └── full_processing_pipeline.py   # Complete pipeline
│   ├── database/               # Database utilities
│   │   ├── migrations/         # SQL migration files
│   │   ├── apply_migrations.py # Migration runner
│   │   ├── init_postgres_db.py # PostgreSQL setup
│   │   ├── migrate_sqlite_to_pg.py     # SQLite → PostgreSQL
│   │   └── setup_postgres.py   # Database configuration
│   ├── utils/                  # Helper scripts
│   │   ├── dashboard.py          # Live monitoring dashboard
│   │   ├── tracker.py          # Progress tracking
│   │   ├── db_search.py        # Database search
│   │   ├── db_stats.py         # Statistics
│   │   ├── data_quality_validator.py   # Data validation
│   │   ├── cpu_monitor.py      # CPU monitoring
│   │   ├── gpu_monitor.py      # GPU monitoring
│   │   └── build_efta_crosswalk.py     # EFTA crosswalk
│   └── archive/                # Legacy/deprecated scripts
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # System design
│   ├── DATA_SOURCES.md         # Data sources and URLs
│   └── WORKFLOW.md             # Processing pipeline
├── Epstein-Pipeline/           # [submodule] Main processing pipeline
├── Epstein-research-data/      # [submodule] Pre-built databases + tools
├── epstein-ripper/             # [submodule] DOJ downloader
├── EpsteinLibraryMediaScraper/ # [submodule] Media URL scraper
├── AGENTS.md                   # Agent architecture
├── CONTEXT.md                  # Living memory / current state
├── RULES.md                    # Coding standards and conventions
├── PROJECT.md                  # Quick-start guide
└── VALIDATION_REPORT.md        # Validation results
```

## Data Sources

| Source | URL | Datasets | Size |
|--------|-----|----------|------|
| DOJ | justice.gov/epstein | DS1-12 | ~218GB |
| RollCall CDN | media-cdn.rollcall.com | DS1-12 | ~218GB |
| Archive.org | archive.org/details/* | DS9, DS11, FBI Vault | ~130GB |
| HuggingFace | AfricanKillshot/Epstein-Files | 4.11M rows, parquet | ~317GB |
| GitHub Releases | rhowardstone/Epstein-research-data | Pre-built DBs | ~8GB |

## Pre-built Databases

| Database | Size | Rows | Description |
|----------|------|------|-------------|
| full_text_corpus.db | 7.0GB | 1.4M docs, 2.9M pages | Full OCR text, FTS5 search |
| redaction_analysis_v2.db | 940MB | 2.59M redactions | Redaction detection + text recovery |
| image_analysis.db | 389MB | 38,955 images | AI image descriptions |
| communications.db | 30MB | 41,924 emails | Email thread analysis |
| knowledge_graph.db | 892KB | 606 entities, 2,302 relationships | Entity relationship graph |

## GPU Support

- **Tesla K80 (x2)**: OCR (Surya), Image Analysis, Transcription
- **Tesla K40m (x1)**: Embeddings, Classification
- CUDA 11.4, Kepler architecture

## Upstream Repos (submodules)

| Repo | Stars | Purpose |
|------|-------|---------|
| [Epstein-Pipeline](https://github.com/stonesalltheway1/Epstein-Pipeline) | 95 | Full processing pipeline |
| [Epstein-research-data](https://github.com/rhowardstone/Epstein-research-data) | 157 | Pre-built databases + tools |
| [epstein-ripper](https://github.com/prizmatik666/epstein-ripper) | 3 | DOJ downloader with Playwright |
| [EpsteinLibraryMediaScraper](https://github.com/lukegosnellranken/EpsteinLibraryMediaScraper) | 23 | Media URL scraper |

## License

MIT — See [LICENSE](LICENSE)
