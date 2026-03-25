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
| CDN PDFs | ✅ **COMPLETE** | 177GB | 1,313,861 files (94.0% of 1.4M EFTAs) |
| HF Parquet | ✅ **COMPLETE** | 318GB | 634/634 files, 0 missing, pre-extracted text |
| Pre-built DBs | ✅ Complete | 12GB | 27 tables, 10.9M rows in PostgreSQL |
| Knowledge graph | ✅ Available | 892KB | 606 entities, 2,302 relationships |
| FTS search | ✅ Complete | — | 2,892,730 pages indexed (100%) |
| **File registry** | ✅ **COMPLETE** | — | 1,313,841 files with SHA-256 hashes |
| **Text content** | ✅ **COMPLETE** | — | 1,380,935 documents with consolidated text (98.8%) |
| **Entity extraction** | 🔄 **IN PROGRESS** | — | 2,146 entities extracted (3M expected) |
| **Total disk** | **~500GB used** | | **~1.8TB free** |

### Download Coverage
- **Downloaded**: 1,313,861 / 1,397,796 EFTAs (94.0%)
- **Missing**: 83,936 files — gone from ALL public sources
  - RollCall CDN: 404
  - Wayback Machine: not archived (checked 2025-12-19 snapshot)
  - DOJ website: removed
- **HF parquet has text for ALL 1.4M documents** — missing PDFs only affect raw archival
- **PostgreSQL has full OCR text, NER, redaction analysis, KG for all documents**

### Wayback Machine Investigation (2026-03-22)
- Checked CDX API: DOJ PDFs were archived on 2025-12-19
- Test download worked: 1 PDF retrieved successfully (373KB)
- Bulk download: all 11,925 remaining URLs returned "Resource not found"
- Conclusion: Wayback Machine did NOT archive the DS12 files or remaining DS9 files
- These files are permanently gone from all public sources

---

## Environment

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.12 (system) | Managed by uv |
| uv | 0.10.12 | Package manager |
| Node | 24.14.0 | For JS tools |
| CUDA | 11.4 (driver 470.256.02) | Kepler architecture |
| PyTorch | 2.3.1+cu118 | Works on K80 (CC 3.7), NOT K40m (CC 3.5) |
| ONNX Runtime | GPU | Works on ALL GPUs (K80 + K40m) |
| aria2c | 1.37.0 | Parallel downloads |
| SQLite | 3.x | Built-in Python |

## GPU Configuration

| GPU | Device | Model | CC | PyTorch? | ONNX? | Use For |
|-----|--------|-------|-----|----------|-------|---------|
| 0 | cuda:0 | Tesla K40m | 3.5 | ❌ NO | ✅ Yes | ONNX only (InsightFace, Surya) |
| 1 | cuda:1 | Tesla K80 | 3.7 | ✅ Yes | ✅ Yes | PyTorch (spaCy, whisper, embeddings) |
| 2 | cuda:2 | Tesla K80 | 3.7 | ✅ Yes | ✅ Yes | PyTorch (spaCy, whisper, embeddings) |

**PyTorch 2.3.1+cu118 works on K80s WITHOUT driver upgrade.** Driver 470 supports CUDA 11.8 runtime. K40m (CC 3.5) is too old for PyTorch — use ONNX Runtime GPU for it.

**Set `CUDA_VISIBLE_DEVICES=1,2` to exclude K40m from PyTorch workloads.**

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
- [x] Run setup.sh and verify
- [x] Continue CDN PDF downloads (94% complete, 1.3M files)
- [x] Process HF parquet into structured database (318GB complete)
- [x] Begin OCR/NER pipeline (Dataset 8 complete)
- [x] PostgreSQL integration and memory system (45 tables migrated)
- [x] Dataset 8 processing (100% complete)
- [x] Letta memory management system (custom implementation)
- [x] File registry population script created and tested
- [x] Verification procedures documented (docs/verification_procedures.md)
- [x] Added verification memories to Letta memory system
- [x] **File registry population complete** (1,313,841 files with SHA-256 hashes)
- [x] **CRITICAL FINDING: OCR processing already complete!** No need to re-run OCR
- [x] **Text content population complete** (1,380,935 documents, 98.8% coverage)
- [x] **NER entity extraction in progress** (2,146 entities extracted so far)
- [x] **AI Skills Integration complete** - OpenCode configured with centralized skills from `/home/cbwinslow/dotfiles/ai/`
- [x] **Memory search protocols created** - `memory_search.py` with semantic, tag, text, recent, cross-agent search
- [x] **Conversation saving scripts created** - `save_conversation_to_letta.py` and `recall_conversation.py`
- [x] **Conversation saved to Letta memory** - AI skills integration session and decisions stored
- [ ] Build knowledge graph from extracted entities
- [ ] Scale to remaining datasets (1-7, 9-10)
- [ ] Cross-database integration and analysis
- [ ] Advanced entity relationship mapping
- [ ] Comprehensive report generation

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
| Centralized AI skills system | 2026-03-24 | Single source of truth for all AI agent configurations and skills |

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
