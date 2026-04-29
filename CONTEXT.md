# Epstein Files Analysis — CONTEXT (Living Document)

> **Include this file in every prompt.** Update after every session.
> This is the agent's persistent memory.

---

## Quick Reference

| Item | Value |
|------|-------|
| GitHub | https://github.com/cbwinslow/epstein_full |
| Project root | `/home/cbwinslow/workspace/epstein` |
| Data mount | `/home/cbwinslow/workspace/epstein-data/` |
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

/home/cbwinslow/workspace/epstein-data/
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
| PostgreSQL (epstein) | ✅ Complete | 42GB | 72 tables, 36.6M rows |
| Knowledge graph | ✅ Available | 892KB | 606 entities, 2,302 relationships |
| **jMail Emails** | ✅ **COMPLETE** | 334MB | **1,783,792 emails imported** |
| **jMail Documents** | ✅ **COMPLETE** | 25MB | **1,413,417 documents imported** |
| **ICIJ Entities** | ✅ **COMPLETE** | 600MB | **~2.0M entities imported (5/6 files)** |
| **ICIJ Relationships** | 🔄 **RUNNING** | — | **64% complete (2.14M/3.34M)** |
| Kabasshouse entities | ✅ Imported | ~100MB | 9.9M entities, PK: (document_id, entity_type, value) |
| Kabasshouse chunks | ✅ Imported | ~500MB | 1.9M chunks, PK: (document_id, chunk_index) |
| Kabasshouse embeddings | ✅ Imported | ~12GB | 1.5M 768-dim Gemini vectors, PK: chunk_id |
| Kabasshouse financial | ✅ Imported | ~5MB | 49.8K transactions, PK: id |
| House Oversight emails | ✅ Imported | ~10MB | 5K email threads, PK: thread_id |
| FBI Vault PDFs | 🔄 OCR running | 35MB | 16 PDFs, PyMuPDF + Tesseract |
| FTS search | ✅ Complete | — | 2,892,730 pages indexed (100%) |
| **File registry** | ✅ **COMPLETE** | — | 1,313,841 files with SHA-256 hashes |
| **Text content** | ✅ **COMPLETE** | — | 1,380,935 documents with consolidated text (98.8%) |
| **Entity extraction** | 🔄 **IN PROGRESS** | — | 2,146 entities extracted (3M expected) |
| **Nomic page embeddings** | 🔄 **RUNNING** | ETA ~4.8 hours observed | Remote Ollama on cbwwin `192.168.4.25:11343`, 1,872,650/2,890,491 total, 59.1/sec, 0 errors |
| **Qwen3 embeddings** | ⬜ **PENDING** | After Nomic review | 4096-dim, ~21 days estimated |
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

## Database Integrity Views

Created comprehensive views for data verification and validation:

| View | Purpose | Key Columns |
|------|---------|-------------|
| `documents_missing_content` | Documents without text content | id, efta_number, file_path, total_pages |
| `pages_missing_text` | Pages with insufficient text | id, efta_number, page_number |
| `embeddings_coverage` | Embedding model coverage stats | model_name, count_per_model, unique_pages |
| `entity_extraction_stats` | NER statistics by type | entity_type, count, avg_docs_per_entity |
| `redaction_analysis_summary` | Redaction patterns | redaction_type, count, avg_text_length, documents_affected |
| `knowledge_graph_stats` | Graph component counts | type, count |
| `file_registry_validation` | File integrity checks | source, hashed_files, validated_files, validation_pct |
| `embedding_datasets_comparison` | Compare embedding sources | dataset, chunks, model |

Query examples:
- `SELECT * FROM documents_missing_content LIMIT 10;` — Find gaps
- `SELECT * FROM embeddings_coverage;` — Check embedding completeness
- `SELECT * FROM redaction_analysis_summary ORDER BY count DESC;` — Top redaction types

---

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
- [x] Download and import kabasshouse supplementary data (10 new tables, ~13M rows)
- [x] Download House Oversight emails (5,082 threads)
- [x] Download FBI Vault PDFs (16 from Archive.org)
- [x] Save session memories to Letta
- [x] FBI Vault OCR complete (996 pages, 616,959 chars)
- [ ] Build knowledge graph from extracted entities
- [ ] Scale to remaining datasets (1-7, 9-10)
- [ ] Cross-database integration and analysis
- [ ] Advanced entity relationship mapping
- [ ] Comprehensive report generation
- [x] Validate corrected Congress historical download endpoints
- [x] Import Congress 107th historical slice (10,791 bills, 553 members)
- [x] Fix GovInfo historical offset-limit issue with split date windows
- [x] Import GovInfo 2000 historical slice (8,543 packages)
- [x] Government historical ingestion finalized (April 23, 2026)
  - `federal_register_entries=737,940` (2000-2024)
  - `congress_bills=359,467` (106th-119th)
  - `congress_members=9,864`
  - `congress_house_votes=2,738`
  - `congress_house_vote_details=2,738`
  - `congress_house_member_votes=1,185,626`
  - `whitehouse_visitors=2,544,984` (2009-2024)
  - `govinfo_bulk_import_status`: `FR=26`, `BILLSTATUS=52`, `BILLS=96`, `BILLSUM=48` completed

## Historical Ingestion Notes (2026-04-22)

- `download_congress_historical.py` previously used the wrong Congress.gov endpoints:
  - Wrong: `/bill?congress=N`, `/member?congress=N`
  - Correct: `/bill/N`, `/member/congress/N`
- Verified corrected Congress 107th download:
  - Bills: 10,791
  - Members: 553
  - Raw files: `/home/cbwinslow/workspace/epstein-data/raw-files/congress_historical/congress_107/`
- Verified corrected Congress 108th-109th download/import:
  - 108th: 10,669 bills, 544 members
  - 109th: 13,072 bills, 546 members
  - Import log: `/home/cbwinslow/workspace/epstein/logs/ingestion/congress_historical_batch_108_109_20260422.log`
- Cleaned stale `congress_bills` contamination from earlier bad imports:
  - Deleted 401 stray rows from test/current-snapshot files
  - Deleted 54,945 duplicate bill rows
  - Current `congress_bills` counts: 107th = 10,791, 108th = 10,669, 109th = 13,072, 118th = 19,315
  - Current `congress_members` counts: 107th = 553, 108th = 544, 109th = 546, 118th = 2,691
- `congress_members` required a schema fix for historical storage:
  - Dropped unique constraint on `bioguide_id`
  - Added unique index on `(bioguide_id, congress_number)`
- `download_govinfo_historical.py` originally hit GovInfo 500 errors at `offset=10000`.
  - Historical API downloader now follows the official GovInfo guidance and uses `offsetMark` pagination.
- Verified GovInfo 2000 historical download/import:
  - `BILLS`: 7,075
  - `CRPT`: 849
  - `FR`: 253
  - `USCOURTS`: 366
  - Total imported: 8,543
- FEC historical coverage is already present in PostgreSQL:
  - `fec_individual_contributions`: 447,189,732 rows
  - Cycles present: 2000-2026

## Historical Batch Status (2026-04-22)

- **Congress historical batch**
  - Scope: 108th-109th Congress
  - Status: completed and imported
  - Log: `/home/cbwinslow/workspace/epstein/logs/ingestion/congress_historical_batch_108_109_20260422.log`
- **Congress historical batch**
  - Scope: 110th-112th Congress
  - Status: download running with patched worker model; imports queued per congress directory after download
  - Worker model fix: process-wide rate limiter plus per-thread `requests.Session`, with bills and members downloaded concurrently inside each congress
  - Log: `/home/cbwinslow/workspace/epstein/logs/ingestion/congress_historical_batch_110_112_20260422.log`
- **GovInfo historical batch**
  - Scope: year 2001 for `FR,BILLS,USCOURTS,CRPT`
  - Status: completed and imported
  - Log: `/home/cbwinslow/workspace/epstein/logs/ingestion/govinfo_historical_batch_2001_20260422.log`
- **GovInfo historical batch**
  - Scope: years 2002-2003 for `FR,BILLS,USCOURTS,CRPT`
  - Status: completed and imported
  - Worker model fix: process-wide rate limiter plus per-thread `requests.Session`
  - Log: `/home/cbwinslow/workspace/epstein/logs/ingestion/govinfo_historical_batch_2002_2003_20260422.log`
- GitHub tracking issues:
  - Congress: `#51`
  - GovInfo: `#52`
  - SEC EDGAR: `#55`
  - FARA: `#57`
  - Senate vote retries/backfill: `#58`
  - FARA completion + reconciliation: `#59`
  - GovInfo 119 reconciliation: `#60`

## Government Ingestion Run (2026-04-24 UTC)

- Parallel workflows launched for:
  - Congress historical (105th-119th)
  - GovInfo bulk download/import (`BILLSTATUS`, `BILLS`, `BILLSUM`)
  - Senate vote details
  - FARA bulk normalization
- Revalidated current counts:
  - `congress_bills=368,651`
  - `congress_members=10,413`
  - `congress_house_votes=2,738`
  - `congress_senate_votes=3,132` (partial)
  - `congress_senate_member_votes=313,176` (partial)
  - `congress_bill_text_versions=130,361`
  - `govinfo_bulk_import_status=246`
  - `fara_registrations=7,045`
  - `fara_foreign_principals=17,358`
  - `fara_short_forms=44,413`
  - `fara_registrant_docs=124,224`
- Blocker:
  - `senate.gov` vote menus/details intermittently return HTTP 403 from this host; continue retry/backfill loop after source access recovers.

## GovInfo Specialized Tables (2026-04-22)

- `scripts/ingestion/import_govinfo.py` now populates:
  - `federal_register_entries`
  - `court_opinions`
- Current verified counts after backfilling available downloaded data:
  - `federal_register_entries`: 2,245
  - `court_opinions`: 31,544
- Year coverage currently visible:
  - Federal Register: 2000-2003, 2020-2024
  - Court opinions: 2000-2003, 2022-2024

## Official Bulk Data Alignment (2026-04-22)

- Cloned official upstream GovInfo/Congress support repos for reference:
  - `/home/cbwinslow/workspace/epstein/research/upstream_refs/api.congress.gov`
  - `/home/cbwinslow/workspace/epstein/research/upstream_refs/govinfo-api`
  - `/home/cbwinslow/workspace/epstein/research/upstream_refs/govinfo-bulk-data`
  - `/home/cbwinslow/workspace/epstein/research/upstream_refs/govinfo-bill-status`
  - `/home/cbwinslow/workspace/epstein/research/upstream_refs/govinfo-rss`
- Updated `download_govinfo_historical.py` to follow official GovInfo API guidance:
  - use `offsetMark`
  - use larger `pageSize`
- Updated `download_congress_historical.py` to follow official Congress API guidance:
  - `limit=250`
  - pace for the documented `5,000 requests/hour`
- Reworked `scripts/ingestion/download_govinfo_bulk.py` to use the actual GovInfo Bulk Data Repository instead of API package listing endpoints.
  - Supports yearly `FR` ZIPs
  - Supports per-congress/per-bill-type `BILLSTATUS` ZIPs
  - Supports per-congress/per-session/per-bill-type `BILLS` ZIPs
  - Supports per-congress/per-bill-type `BILLSUM` ZIPs
  - Saves GovInfo bulk listing manifests next to the downloaded ZIPs
- Added `scripts/ingestion/import_govinfo_billstatus_bulk.py` for GovInfo Bill Status XML ZIPs.
  - Creates normalized child tables:
    - `congress_bill_titles`
    - `congress_bill_summaries`
    - `congress_bill_actions`
    - `congress_bill_cosponsors`
    - `congress_bill_related_bills`
    - `congress_bill_vote_references`
  - Adds unique bill identity enforcement on `congress_bills (congress, bill_type, bill_number)`
  - Adds `govinfo_bulk_import_status` for per-ZIP idempotent import tracking
- Validated bulk downloads:
  - `FR-2004.zip` downloaded to `/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/fr/2004/`
  - `BILLSTATUS-113-hjres.zip` downloaded to `/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/billstatus/113/hjres/`
  - `BILLS-113-1-hjres.zip` and `BILLS-113-2-hjres.zip` downloaded to `/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/bills/113/`
  - `BILLSUM-113-hjres.zip` downloaded to `/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/billsum/113/hjres/`
  - both ZIPs pass `unzip -l` inspection
- Validated Bill Status bulk import:
  - `BILLSTATUS-113-hjres.zip` imported as:
    - `131` bills
    - `350` titles
    - `178` summaries
    - `950` actions
    - `1,837` cosponsors
    - `217` related bill links
    - `49` vote references
- Fixed a real production failure in GovInfo bulk ingestion:
  - Root cause: `download_govinfo_bulk.py` treated any existing nonzero ZIP as valid, so a corrupt `BILLSTATUS-113-hr.zip` blocked the whole Bill Status importer.
  - Fix: downloader now validates ZIP integrity, re-downloads corrupt ZIPs, and writes through `.part` temp files.
  - Fix: Bill Status importer now validates ZIPs before import, records per-file import status in `govinfo_bulk_import_status`, skips completed ZIPs, and continues past failed ZIPs instead of crashing the full run.
- Added `scripts/ingestion/import_govinfo_billsum_bulk.py`.
  - Imports GovInfo `BILLSUM` ZIPs into existing `congress_bill_summaries`
  - Reuses `congress_bills`
  - Reuses `govinfo_bulk_import_status` for per-ZIP idempotent tracking
  - Validated on `BILLSUM-113-hjres.zip` with `178` summaries imported

## Government Ingestion Finalized (2026-04-24)

- Historical/bulk ingestion reached stable completion for currently scoped government sources.
- Final validated GovInfo bulk import status:
  - `BILLSTATUS completed=52`
  - `BILLSUM completed=48`
  - `BILLS completed=96`
  - `FR completed=26`
- Final validated database counts after 2026-04-24 reruns:
  - `federal_register_entries=737,940` (`2000-01-03` to `2024-12-31`)
  - `congress_bills=359,467` (106th-119th)
  - `congress_members=9,864` (106th-119th)
  - `congress_bill_text_versions=113,106` (113th-118th currently present)
  - `congress_house_votes=2,738` (117th-119th)
  - `congress_house_vote_details=2,738` (`pending_vote_details=0`)
  - `congress_house_member_votes=1,185,626`
  - `whitehouse_visitors=2,544,984` (2009-2024)
- Reference logs:
  - `docs/SESSION_LOGS/government_data_ingestion_20260423.md`
  - `/home/cbwinslow/workspace/epstein/logs/ingestion/congress_historical_20260424_131710.log`
  - `/home/cbwinslow/workspace/epstein/logs/ingestion/house_vote_details_20260424_131136.log`
  - `/home/cbwinslow/workspace/epstein/logs/ingestion/house_vote_details_20260424_132859.log`

### Runtime Status (checked 2026-04-24)

- No active GovInfo/Congress/White House ingestion jobs required in steady state.

### Remaining Government Gaps

- Pre-107th Congress requires a Congress.gov API key and alternate pathing.
- Senate vote-detail pipeline and tables are not yet implemented.
- Pre-2009 White House visitor logs are not publicly disclosed for Bush/Trump terms.
- SEC EDGAR and FARA remain optional expansion tracks.

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
| Use aria2c for HF downloads | 2026-03-29 | hf_hub_download hangs on large files, aria2c gives 5-13MB/s |
| Disable autovacuum during bulk import | 2026-03-29 | Kills throughput on high-conflict ON CONFLICT inserts |
| Keep Letta tables in letta DB | 2026-03-29 | epstein DB is for document data only |

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
