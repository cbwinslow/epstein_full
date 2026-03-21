# Epstein Files Analysis — CONTEXT (Living Document)

> **Include this file in every prompt.** Update after every session.
> This is the agent's persistent memory.

---

## Quick Reference

| Item | Value |
|------|-------|
| GitHub | https://github.com/cbwinslow/epstein_full |
| Project root | `/home/cbwinslow/workspace/epstein` |
| Data mount | `/mnt/data/epstein-project/` |
| Python | 3.12 via uv (`.venv/`) |
| Package manager | `uv` (never pip directly) |
| GPUs | 2× Tesla K80 (12GB) + 1× Tesla K40m (11GB), CUDA 11.4 |

---

## Critical Paths

```
/home/cbwinslow/workspace/epstein/         # Project root
├── .venv/                                  # Python venv (uv-managed)
├── pyproject.toml                          # Dependencies, Python version, scripts
├── .python-version                         # Pins 3.12
├── .env.example                            # Environment variable template
├── setup.sh                                # One-command bootstrap
├── scripts/
│   ├── tracker.py                          # SQLite progress tracker
│   ├── dashboard.py                        # Rich terminal dashboard
│   ├── download_cdn.py                     # CDN downloader (aria2c)
│   ├── download_doj.py                     # Playwright downloader
│   ├── explore_kg.py                       # Knowledge graph explorer
│   ├── file_watcher.py                     # Filesystem monitor
│   ├── metrics.py                          # Evaluation metrics (CER, F1, EER)
│   └── setup_dev.py                        # Environment verification
├── docs/
│   ├── ARCHITECTURE.md                     # System design
│   ├── DATA_SOURCES.md                     # Data sources and URLs
│   ├── WORKFLOW.md                         # Processing pipeline
│   ├── METHODOLOGY.md                      # CRISP-DM, data model, stack
│   ├── PAPER.md                            # Academic paper draft
│   └── SUPPLEMENTARY_DATASETS.md           # Cross-reference sources
├── Epstein-Pipeline/                       # [submodule] Processing pipeline
├── Epstein-research-data/                  # [submodule] Pre-built databases
├── epstein-ripper/                         # [submodule] DOJ downloader
└── EpsteinLibraryMediaScraper/             # [submodule] Media scraper

/mnt/data/epstein-project/
├── raw-files/                              # Downloaded PDFs (~268K files)
│   ├── data1/ through data12/              # Per-dataset directories
├── databases/                              # Pre-built SQLite databases (8.4GB)
│   ├── full_text_corpus.db                 # 7.0GB, 1.4M docs, FTS5
│   ├── redaction_analysis_v2.db            # 940MB, 2.59M redactions
│   ├── image_analysis.db                   # 389MB, 38K images
│   ├── ocr_database.db                     # 68MB, 38K OCR results
│   ├── communications.db                   # 30MB, 41K emails
│   ├── transcripts.db                      # 4.8MB, 1.6K transcriptions
│   ├── prosecutorial_query_graph.db        # 2.5MB, 257 subpoenas
│   └── knowledge_graph.db                  # 892KB, 606 entities, 2.3K relationships
├── hf-parquet/                             # HuggingFace parquet (634 files, 318GB) ✅ COMPLETE
├── processed/                              # OCR output (empty, ready)
├── knowledge-graph/                        # KG exports (empty, ready)
└── logs/                                   # Download logs, state files
    ├── progress.db                         # SQLite tracker
    ├── aria2c.log                          # CDN download log
    └── download.log                        # General download log
```

---

## Data Status (Live)

| Source | Status | Size | Details |
|--------|--------|------|---------|
| HF Parquet | ✅ **COMPLETE** | 318GB | 634/634 files, 0 missing, pre-extracted text |
| CDN PDFs | 🔄 **RUNNING** | ~58GB | 268K+ files, aria2c active |
| Pre-built DBs | ✅ Complete | 8.4GB | 8 SQLite databases |
| Knowledge graph | ✅ Available | 892KB | 606 entities, 2,302 relationships |
| **Total disk** | **408GB used** | | **2.1TB free** |

---

## Environment

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.12 (system) | Managed by uv |
| uv | 0.10.12 | Package manager |
| Node | 24.14.0 | For JS tools |
| CUDA | 11.4 | Kepler architecture |
| aria2c | 1.37.0 | Parallel downloads |
| SQLite | 3.x | Built-in Python |

---

## Upstream Submodules

| Repo | Remote | Branch |
|------|--------|--------|
| Epstein-Pipeline | stonesalltheway1/Epstein-Pipeline | main |
| Epstein-research-data | rhowardstone/Epstein-research-data | v5.0 |
| epstein-ripper | prizmatik666/epstein-ripper | main |
| EpsteinLibraryMediaScraper | lukegosnellranken/EpsteinLibraryMediaScraper | main |

**DO NOT MODIFY** upstream repos. Call via CLI or import public APIs only.

---

## Current Focus

- [x] Dev environment setup (uv, pyproject.toml, setup.sh)
- [ ] Run setup.sh and verify
- [ ] Continue CDN PDF downloads
- [ ] Process HF parquet into structured database
- [ ] Begin OCR/NER pipeline

---

## Key Decisions

| Decision | Date | Rationale |
|----------|------|-----------|
| Use uv instead of pip | 2026-03-21 | Faster, reproducible, lock file support |
| Python 3.12 (not 3.11) | 2026-03-21 | Already on system, upstream supports it |
| RollCall CDN over Playwright | 2026-03-20 | 2-5x faster, no age-gate issues |
| SQLite tracker over JSON | 2026-03-20 | WAL mode handles concurrent writes |
| InsightFace/ArcFace for faces | 2026-03-20 | 99.83% LFW, ONNX Runtime (K80 compatible) |
| Rich over curses for dashboard | 2026-03-20 | Works in non-TTY environments |

---

## Rules Summary

1. **Never modify upstream repos** — extend via composition
2. **Always use uv** — `uv run python`, `uv add`, never `pip install`
3. **Update CONTEXT.md** after every significant change
4. **Update TASKS.md** with status and solutions
5. **Validate code** — execute, test, verify before marking done
6. **Parameterized SQL** — never string interpolation in queries
7. **Error handling** — try/except with specific types, cleanup in finally
8. **Docstrings** — every public function

---

## Tokens & Secrets

Stored in `.env` (git-ignored). See `.env.example` for template.
- HF_TOKEN: `hf_RnYDalp...` (in .env)
- GITHUB_TOKEN: `ghp_ktqW...` (in .env)
