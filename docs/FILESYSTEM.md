# Filesystem Guide — Where Everything Is

## Project Root

```
/home/cbwinslow/workspace/epstein/          # Git repo root
```

## Configuration Files

| File | Description |
|------|-------------|
| `pyproject.toml` | Python project config: deps, scripts, tool settings |
| `.python-version` | Pinned to Python 3.12 |
| `.env` | Environment variables (git-ignored, tokens + paths) |
| `.env.example` | Template for .env (safe to commit) |
| `.gitignore` | Excludes data, logs, venv, pycache |
| `.gitmodules` | Git submodule references (4 upstream repos) |

## Documentation

| File | Description |
|------|-------------|
| `README.md` | Project overview, quick-start, structure |
| `CONTEXT.md` | **Living memory** — included in every prompt (paths, status, decisions) |
| `AGENTS.md` | Agent architecture, workflow pipeline, anti-drift rules |
| `RULES.md` | Coding standards, setup procedures, deployment checklist |
| `TASKS.md` | 100+ tasks with status, solutions, microgoals |
| `PROJECT.md` | Quick-start guide |
| `LICENSE` | MIT license |
| `VALIDATION_REPORT.md` | Last validation results (30/30 checks) |

## Documentation (docs/)

| File | Description |
|------|-------------|
| `docs/ARCHITECTURE.md` | System design, data flow, GPU allocation |
| `docs/DATA_SOURCES.md` | All data sources with URLs and access methods |
| `docs/WORKFLOW.md` | Step-by-step processing pipeline |
| `docs/METHODOLOGY.md` | CRISP-DM framework, data model, analysis stack |
| `docs/PAPER.md` | Academic paper draft (abstract through references) |
| `docs/SUPPLEMENTARY_DATASETS.md` | Cross-reference sources (flight logs, FEC, SEC) |
| `docs/KNOWLEDGE_BASE.md` | Compiled knowledge from all sources and projects |

## Scripts (scripts/)

| File | Description |
|------|-------------|
| `scripts/tracker.py` | SQLite-backed progress tracker (multi-process safe) |
| `scripts/dashboard.py` | Rich terminal dashboard (live refresh) |
| `scripts/download_cdn.py` | CDN downloader via aria2c (RollCall mirror) |
| `scripts/download_doj.py` | Playwright downloader (DOJ age-gate bypass) |
| `scripts/download_hf.py` | HuggingFace parquet downloader (aria2c + auth) |
| `scripts/download_chunked.py` | Chunked parallel downloader |
| `scripts/explore_kg.py` | Knowledge graph exploration CLI |
| `scripts/file_watcher.py` | Filesystem progress monitor |
| `scripts/metrics.py` | Evaluation metrics (CER, F1, EER, AUROC) |
| `scripts/setup_dev.py` | Environment verification (26 checks) |
| `scripts/run_downloads.py` | Download runner with monitoring |
| `scripts/launch_downloads.sh` | Multi-process launcher |

## Setup

| File | Description |
|------|-------------|
| `setup.sh` | One-command bootstrap (uv + venv + deps + spacy + playwright) |

## Virtual Environment

```
.venv/                                       # uv-managed Python 3.12 venv
├── bin/
│   ├── python                               # Python 3.12.3
│   ├── pip, uv                              # Package managers
│   ├── playwright                           # Browser automation
│   ├── epstein-pipeline                     # Pipeline CLI
│   └── aria2c                               # (system) Parallel downloader
└── lib/python3.12/site-packages/            # All installed packages
```

## Upstream Repos (Git Submodules — DO NOT MODIFY)

| Directory | Repo | Description |
|-----------|------|-------------|
| `Epstein-Pipeline/` | stonesalltheway1/Epstein-Pipeline | Processing pipeline (OCR, NER, embed, KG) |
| `Epstein-research-data/` | rhowardstone/Epstein-research-data | Pre-built databases + 38 analysis tools |
| `epstein-ripper/` | prizmatik666/epstein-ripper | DOJ downloader with Playwright |
| `EpsteinLibraryMediaScraper/` | lukegosnellranken/EpsteinLibraryMediaScraper | Media URL scraper (Node.js) |

### Key Files in Upstream Repos

**Epstein-Pipeline/src/epstein_pipeline/:**
```
cli.py              CLI entry points (download, ocr, entities, embed, export)
config.py           All configuration defaults and settings
models/             Pydantic data models (Document, Person, Entity)
downloaders/        DOJ, Kaggle, HuggingFace, Archive.org downloaders
processors/         OCR, NER, dedup, classify, chunk, embed
exporters/          JSON, CSV, SQLite, Neon Postgres exporters
validators/         Schema and cross-reference validation
utils/              Shared utilities
```

**Epstein-Pipeline/docs/:**
```
ARCHITECTURE.md     System design
DATA_SOURCES.md     Download sources and URLs
PROCESSORS.md       Processing pipeline details
CONTRIBUTING.md     Contribution guidelines
```

**Epstein-research-data/tools/ (38 scripts):**
```
build_knowledge_graph.py        KG construction from evidence DB
build_person_registry.py        Unified person registry (9 sources)
person_search.py                FTS5 cross-reference + co-occurrence
redaction_detector_v2.py        Spatial redaction analysis
transcribe_media.py             GPU transcription (faster-whisper)
document_classifier.py          14-type rule-based classification
congressional_scorer.py         Priority scoring for congressional reading
extract_subpoena_riders.py      Grand Jury subpoena catalog
search_gov_officials.py         Government official search
search_judicial.py              Federal judge search
mirror_coverage.py              CDN mirror coverage map
populate_evidence_db.py         Populate evidence DB
find_missing_efta.py            Gap detection
... (25 more scripts)
```

**Epstein-research-data/doj_audit/:**
```
CONFIRMED_REMOVED.csv           67,784 docs confirmed removed (404)
FLAGGED_documents.csv           96,112 flagged documents
FLAGGED_documents_details.csv   102,223 with metadata
SIZE_MISMATCHES.csv             23,989 size mismatches
sample_verification_results.csv 500 statistical sample results
sample_verify.py                Playwright verification script
```

## Data Storage (/mnt/data/epstein-project/)

| Directory | Contents | Size |
|-----------|----------|------|
| `raw-files/` | Downloaded PDFs (data1/ through data12/) | ~100GB (growing) |
| `databases/` | 8 pre-built SQLite databases | 8.4GB |
| `hf-parquet/` | HuggingFace parquet (634 files) | 318GB |
| `processed/` | OCR output (empty, ready for processing) | 0 |
| `knowledge-graph/` | Custom KG exports (empty, ready) | 0 |
| `logs/` | Download logs, state files, tracker DB | ~1GB |

### Databases Detail

| File | Size | Content |
|------|------|---------|
| `full_text_corpus.db` | 7.0GB | 1.4M docs, 2.9M pages, FTS5 search |
| `redaction_analysis_v2.db` | 940MB | 2.59M redactions, 849K summaries |
| `image_analysis.db` | 389MB | 38,955 AI image descriptions |
| `ocr_database.db` | 68MB | 38,955 OCR results |
| `communications.db` | 30MB | 41,924 emails, 90K participants |
| `transcripts.db` | 4.8MB | 1,628 media transcriptions |
| `prosecutorial_query_graph.db` | 2.5MB | 257 subpoenas |
| `knowledge_graph.db` | 892KB | 606 entities, 2,302 relationships |

## Logs (/mnt/data/epstein-project/logs/)

| File | Description |
|------|-------------|
| `progress.db` | SQLite tracker (tasks, history) |
| `aria2c.log` | CDN download log |
| `download.log` | General download log |
| `hf_aria2c.log` | HuggingFace download log |
| `cdn_urls.txt` | Generated URL list for aria2c |
| `efta_to_download.json` | Remaining EFTAs to download |
| `hf_urls.txt` | Generated HF URL list |
| `ds*_state.json` | Per-dataset resume state |

## GitHub

| Item | Value |
|------|-------|
| Repo | https://github.com/cbwinslow/epstein_full |
| Branch | main |
| Commits | 7+ (check `git log --oneline`) |
| Submodules | 4 (Epstein-Pipeline, research-data, ripper, media-scraper) |
