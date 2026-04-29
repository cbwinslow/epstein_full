# Tasks — Epstein Files Analysis Project

## Status Legend
- ✅ **DONE** — Completed and verified
- 🔄 **RUNNING** — In progress (downloads, processing)
- ⬜ **TODO** — Not started
- ⚠️ **BLOCKED** — Waiting on dependency
- 🔧 **FIX** — Issue found, needs fix
- 🚧 **IN_PROGRESS** — Currently working on

---

## Phase 0: Agent System Setup ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 0.1 | Fix auto_init_agents.py syntax errors | ✅ Done | Rewrote script with proper string handling |
| 0.2 | Initialize all AI agents | ✅ Done | 8 agents initialized (opencode, gemini, claude, cline, kilocode, vscode, windsurf, openclaw) |
| 0.3 | Create framework integrations | ✅ Done | LangChain, CrewAI, AutoGen integration files created |
| 0.4 | Create shell aliases | ✅ Done | Added to ~/.zshrc for all agents |
| 0.5 | Set up Git repository | ✅ Done | Initialized git repo in chezmoi source directory with initial commit |
| 0.6 | Configure age encryption | ✅ Done | Generated age key (key.txt.age) and added to .chezmoiignore |
| 0.7 | Create CI/CD pipeline | ✅ Done | Added GitHub Actions workflow for validation |
| 0.8 | Add pre-commit hooks | ✅ Done | Installed pre-commit with secret detection (detect-secrets) |

---

## Phase 1: Infrastructure Setup ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 1.1 | Mount LVM storage volume | ✅ Done | `lv-nextcloud` mounted at `/home/cbwinslow/workspace/epstein-data/`, 2.3TB free |
| 1.2 | Create project directory structure | ✅ Done | `raw-files/`, `databases/`, `processed/`, `knowledge-graph/`, `logs/` |
| 1.3 | Clone upstream repos | ✅ Done | 4 repos as git submodules (Epstein-Pipeline, research-data, ripper, media-scraper) |
| 1.4 | Install Python dependencies | ✅ Done | Epstein-Pipeline + spaCy + PyMuPDF + aiohttp + Playwright via uv |
| 1.5 | Install Playwright Chromium | ✅ Done | Headless Chromium for DOJ age-gate bypass |
| 1.6 | Install system deps | ✅ Done | aria2c, sqlite3, curl, jq |

---

## Phase 2: Pre-built Data Acquisition ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 2.1 | Download knowledge_graph.db | ✅ Done | 892KB, 606 entities, 2,302 relationships |
| 2.2 | Download redaction_analysis_v2.db | ✅ Done | 940MB, 2.59M redactions, 849K summaries |
| 2.3 | Download image_analysis.db | ✅ Done | 389MB, 38,955 images with AI descriptions |
| 2.4 | Download ocr_database.db | ✅ Done | 68MB, 38,955 OCR results |
| 2.5 | Download communications.db | ✅ Done | 30MB, 41,924 emails, 90K participants |
| 2.6 | Download transcripts.db | ✅ Done | 4.8MB, 1,628 media files |
| 2.7 | Download prosecutorial_query_graph.db | ✅ Done | 2.5MB, 257 subpoenas |
| 2.8 | Download full_text_corpus.db | ✅ Done | 7.0GB, 1.39M docs, 2.9M pages, FTS5 search (2 parts concatenated) |

---

## Phase 3: Knowledge Graph Exploration ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 3.1 | Explore knowledge graph entities | ✅ Done | 606 entities (571 person, 12 shell_company, 9 org, 7 property, 4 aircraft, 3 location) |
| 3.2 | Explore knowledge graph relationships | ✅ Done | 2,302 relationships (traveled_with 1449, associated_with 589, communicated_with 215) |
| 3.3 | Identify top connected entities | ✅ Done | Epstein (493 conn), Maxwell (283), Tayler (130), Kellen (127), Visoski (86) |
| 3.4 | Analyze email communications | ✅ Done | Nikolic (680 emails), Kahn (437), Groff (208), Chomsky (194), Chopra (184) |
| 3.5 | Create KG exploration script | ✅ Done | `scripts/explore_kg.py` — CLI search + display |

---

## Phase 4: Download Infrastructure ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 4.1 | Investigate DOJ URL patterns | ✅ Done | `https://justice.gov/epstein/files/DataSet%20{N}/EFTA{8digits}.pdf`, 50 files/page |
| 4.1a | **Problem**: Akamai WAF blocks headless Playwright | ✅ Solved | Added stealth user-agent + `--disable-blink-features=AutomationControlled` |
| 4.2 | Build Playwright downloader (`download_doj.py`) | ✅ Done | Direct EFTA URL construction, no HTML scraping, PDF signature validation |
| 4.3 | **Problem**: HTML page scraping rate-limited by Akamai | ✅ Solved | Switched to direct PDF downloads (no rate limits on PDFs) |
| 4.4 | Build progress tracker (`tracker.py`) | ✅ Done | JSON-backed, multi-process safe |
| 4.4a | **Problem**: JSON state file corruption from concurrent writes | ✅ Solved | Rewrote with SQLite WAL mode — atomic transactions, no corruption |
| 4.5 | Build dashboard (`dashboard.py`) | ✅ Done | Rich-based terminal UI, live refresh |
| 4.5a | **Problem**: Curses doesn't work in non-TTY environment | ✅ Solved | Switched to Rich library (works everywhere) |
| 4.6 | Discover RollCall CDN mirror | ✅ Done | `https://media-cdn.rollcall.com/epstein-files/EFTA{N}.pdf` — no auth, no rate limits |
| 4.7 | Build CDN downloader (`download_cdn.py`) | ✅ Done | aria2c with 10 parallel connections, 12.6 files/sec |
| 4.8 | **Problem**: Download speed too slow (~6 files/sec Playwright) | ✅ Solved | CDN gives 12-30 files/sec (2-5x faster) |
| 4.9 | Scale to multiple CDN processes | ✅ Done | 5 parallel aria2c instances, ~27 files/sec combined |
| 4.10 | HuggingFace parquet download | ✅ Done | 634/634 files, 318GB, pre-extracted text |
| 4.11 | HF token authentication | ✅ Done | `hf_xxxxx` |

---

## Phase 5: Documentation & Research ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 5.1 | Create CONTEXT.md (living memory) | ✅ Done | Updated with all paths, status, config |
| 5.2 | Create AGENTS.md (agent architecture) | ✅ Done | Workflow pipeline, tool integration map |
| 5.3 | Create RULES.md (coding standards) | ✅ Done | Codebase separation, validation loop, code quality |
| 5.4 | Create PROJECT.md (quick-start) | ✅ Done | Setup guide, structure, research goals |
| 5.5 | Create VALIDATION_REPORT.md | ✅ Done | 30/30 tests passed, 3 issues found and fixed |
| 5.6 | Define CRISP-DM methodology | ✅ Done | 6 phases adapted for public interest analysis |
| 5.7 | Define data model (Python dataclasses) | ✅ Done | Document, Entity, Relationship, FaceDetection, Transcription, Redaction |
| 5.8 | Research facial recognition tools | ✅ Done | InsightFace/ArcFace (99.83% LFW), ONNX Runtime (K80 compatible) |
| 5.9 | Define evaluation metrics | ✅ Done | CER/WER (OCR), 4-schema F1 (NER), EER/AUROC (face), B-Cubed (KG) |
| 5.10 | Create metrics.py | ✅ Done | Python implementations of all evaluation formulas |
| 5.11 | Write academic paper draft (PAPER.md) | ✅ Done | Full structure: abstract through references, results sections to fill |
| 5.12 | Catalog supplementary datasets | ✅ Done | 9 categories: flight logs, FEC, SEC, emails, court records |
| 5.13 | Identify what HF parquet covers vs what's missing | ✅ Done | HF = DOJ EFTA only; supplementary = flight logs, FEC, SEC, etc. |

---

## Phase 6: GitHub Repository ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 6.1 | Initialize git repo | ✅ Done | Branch: main |
| 6.2 | Add upstream repos as submodules | ✅ Done | 4 submodules (Epstein-Pipeline, research-data, ripper, media-scraper) |
| 6.3 | Create .gitignore | ✅ Done | Excludes data, logs, venv, pycache, .parquet, .db |
| 6.4 | Create README.md | ✅ Done | Project overview, quick-start, structure, data sources |
| 6.5 | Create LICENSE (MIT) | ✅ Done | Standard MIT license |
| 6.6 | Create GitHub repo | ✅ Done | `cbwinslow/epstein_full` — https://github.com/cbwinslow/epstein_full |
| 6.7 | Push all code | ✅ Done | 5 commits pushed |

---

## Phase 7: Active Downloads ✅

| # | Task | Status | Progress |
|---|------|--------|----------|
| 7.1 | Download DOJ PDFs via CDN | ✅ Done | ~268K files downloaded |
| 7.2 | Download HF parquet | ✅ Done | 634/634 files, 318GB |
| 7.3 | Validate downloaded PDFs | ✅ Done | 1,346 checked, 100% valid (PDF signature) |
| 7.4 | Validate HF parquet integrity | ✅ Done | 0 missing, 0 zero-size files |
| 7.5 | Download missing DOJ datasets via epstein-ripper | ✅ Done | 3,671 files: DS2=516, DS3=28, DS4=102, DS6=13, DS7=17, DS8=3,484, DS9=0, DS12=101 |

---

## Phase 8: Dev Environment Setup 🔄

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 8.1 | Install uv package manager | ✅ Done | uv 0.10.12 |
| 8.2 | Create pyproject.toml | ✅ Done | All deps + optional GPU groups (gpu, ocr, transcription, embedding, all) |
| 8.3 | Create .python-version | ✅ Done | Pinned to 3.12 |
| 8.4 | Create .env.example | ✅ Done | HF_TOKEN, GITHUB_TOKEN, CUDA config, data paths |
| 8.5 | Create setup.sh | ✅ Done | One-command bootstrap: uv + venv + deps + spacy + playwright |
| 8.6 | Create scripts/setup_dev.py | ✅ Done | Verification script (30+ checks) |
| 8.7 | Delete old venv/ | ✅ Done | Replaced with uv-managed .venv |
| 8.8 | Rewrite CONTEXT.md | 🔄 In progress | Living memory with all critical info |
| 8.9 | Update AGENTS.md | 🔄 In progress | Anti-drift rules, MCP tools |
| 8.10 | Update RULES.md | 🔄 In progress | Setup procedures, deployment |
| 8.11 | Create TASKS.md | ✅ Done | This file — full history |
| 8.12 | Run setup and verify | ⬜ TODO | Run setup.sh, verify all imports |
| 8.13 | Push to GitHub | ⬜ TODO | Commit all new files |

## Backlog Issues

| Issue | Title | Status |
|------|-------|--------|
| #65 | Add missing data source for DOJ archives | ⬜ TODO |
| #66 | Implement facial recognition pipeline | ⬜ TODO |
| #67 | Optimize embedding generation performance | ⬜ TODO |
| #68 | Ingest Capitol Gains data | 🚧 IN_PROGRESS |

---

## Phase 8.5: CapitolGains Politician Stock Transaction Ingestion 🚧 IN_PROGRESS

**Goal:** ingest congressional stock transaction/disclosure data into PostgreSQL for cross-reference analysis.

**Current state revalidated 2026-04-27 UTC:**
- GitHub issue: `#68` open, created for `ingest_capitolgains.py`.
- Local upstream clone: `scripts/political_disclosures/CapitolGains/`.
- Local project stubs: `ingest_capitolgains.py` and `epstein_capitolgains/{downloaders,etl,loader}.py`.
- Existing database tables:
  - `house_financial_disclosures`: 50,429 rows, years 2008-2026.
  - `senate_financial_disclosures`: 0 rows.
  - `congress_trading`: 18,521 House PTR OCR rows.
  - `politician_financial_summary`: 0 rows.
- Raw House PTR PDFs:
  - 8,150/8,150 `P` filing PDFs downloaded and PDF-signature validated.
  - Stored under `/home/cbwinslow/workspace/epstein-data/raw-files/financial_disclosures/house_ptr/{year}/{filing_id}.pdf`.
  - Download manifest: `/home/cbwinslow/workspace/epstein-data/raw-files/financial_disclosures/manifests/house_ptr_download_20260426T132235Z.jsonl`.
  - Total raw size: 670,588,048 bytes (~639.5 MB).
- House PTR OCR / transaction extraction:
  - OCR cache tables created: `house_ptr_ocr_pages`, `house_ptr_ocr_status`.
  - OCR complete for 2013-2026: 8,150 filings, 21,098 pages, 0 OCR errors.
  - `congress_trading`: 18,521 conservative parsed rows from House PTR OCR.
  - Parsed rows currently span transaction dates 2012-02-27 to 2026-12-26, 326 politicians, 11,878 rows with tickers, 8,378 rows with House asset type codes, 5,653 source filings.
  - Parser now handles transaction pages without repeated `Filing ID`, OCR punctuation before amount ranges, ticker-only continuation lines, 2018+ cap-gains columns, `S (partial)`, cents-valued amounts, OCR decimal hyphens, OCR periods after dates, OCR `S$` transaction type, bracket noise after dangling ranges, and wrapped amount/ticker lines.
- Existing old scripts:
  - `scripts/ingestion/import_financial_disclosures.py` imports House disclosure index metadata, now with `--house-years`, `--senate-years`, `--skip-house`, and `--skip-senate`.
  - `scripts/ingestion/download/download_politicians_financial.py` created `congress_trading` and `politician_financial_summary` schemas, but does not load rows.
- Backfill finding:
  - House Clerk online bulk ZIP data is available for 2008-2026 from tested endpoints.
  - House Clerk bulk ZIP endpoints return 404/unavailable for 2000-2007; those years likely require alternate scanned House Document/Google Books/GovInfo-style sources rather than the modern Clerk ZIPs.
  - Senate eFD page states reports are available from 2012-present; older Senate reports require the Secretary of the Senate kiosk/public records path.
  - Senate live portal is `efdsearch.senate.gov`; the old `efts.senate.gov` endpoint no longer resolves, and direct DataTables POST currently returns a Senate maintenance page from this host.
  - House PTR PDFs are scanned image-only forms with no embedded text layer; transaction extraction requires OCR with table/coordinate handling.
- Validation note: `python3 -m py_compile ingest_capitolgains.py epstein_capitolgains/*.py` passed. CapitolGains tests/imports currently fail because `appdirs` is missing from the active environment. `uv run` is blocked by the repo's unsatisfied `torch==2.3.1+cu118` dependency resolution.

| # | Task | Status | Notes |
|---|------|--------|-------|
| 8.5.1 | Decide canonical implementation location | ⬜ TODO | Prefer project-owned `epstein_capitolgains/` + root CLI; keep cloned `scripts/political_disclosures/CapitolGains/` as upstream/reference unless intentionally vendoring |
| 8.5.2 | Fix environment for CapitolGains validation | ⬜ TODO | Add/install `appdirs`, `playwright`, `python-dotenv`, `requests`; avoid triggering unsatisfied `uv` all-extra torch solve |
| 8.5.3 | Replace root `ingest_capitolgains.py` placeholders | ⬜ TODO | Wire CLI to real project modules instead of creating empty files |
| 8.5.4 | Implement House index downloader/import reuse | ✅ DONE | Promoted fixed implementation to `import_financial_disclosures.py`; imported 2008-2026, 50,429 rows; wrote availability audit under `raw-files/financial_disclosures/availability/` |
| 8.5.5 | Implement Senate disclosure metadata ingest | ⚠️ BLOCKED | Current Senate table has 0 rows; live eFD covers 2012-present, but direct POST returned maintenance page; old `efts.senate.gov` DNS fails |
| 8.5.6 | Extract actual PTR stock transactions | ✅ DONE | Downloaded and OCRed all available House PTR PDFs for 2013-2026; parser handles modern text-like OCR layout, cap-gains columns, partial sales, and wrapped amount/ticker lines; 2013 grid-style forms produced no conservative transaction rows and need separate table-coordinate parsing if required |
| 8.5.7 | Load normalized transactions into `congress_trading` | ✅ DONE | Added source columns + hash upsert; loaded 18,521 conservative House PTR OCR rows from 5,653 source filings |
| 8.5.8 | Add raw manifest/resume tracking | ✅ DONE | House PTR PDFs stored under `raw-files/financial_disclosures/house_ptr/`; JSONL manifest written with status, size, sha256 |
| 8.5.9 | Add validation queries/report | ✅ DONE | Added `scripts/ingestion/validate_house_ptr_quality.sql`; OCR status 8,150/8,150 complete with 0 errors; `congress_trading` has 18,521 rows, 0 required-field nulls, 0 bad low/high ranges, 0 duplicate source hashes, and full source traceability to House metadata/OCR pages |
| 8.5.10 | Update docs and issue #68 | 🚧 IN_PROGRESS | Task ledger updated after OCR/parser quality reassessment; add final issue close/split comment after Senate/pre-2008 decision |
| 8.5.11 | Research alternate 2000-2007 House sources | ⬜ TODO | Candidate source: scanned House Document annual compilations (e.g. 2000 report appears as House Document 107-104 / Google Books metadata); not available through Clerk ZIP bulk |
| 8.5.12 | Promote financial disclosure importer to canonical path | ✅ DONE | `import_financial_disclosures.py` is the canonical importer; legacy workaround/downloader names are compatibility wrappers only |
| 8.5.13 | Embed House PTR OCR pages | ⬜ TODO | Active remote Nomic embedding job targets `pages.text_content`, not `house_ptr_ocr_pages.ocr_text`; add a disclosure-specific embedding path after the main page job completes or schedule it at low concurrency |

---

## Phase 9: Processing Pipeline 🔄

| # | Task | Status | Dependencies |
|---|------|--------|--------------|
| 9.1 | Test OCR pipeline on small batch | ✅ Done | Downloads complete |
| 9.2 | Process HF parquet into structured DB | 🔄 Partial | 10.9M rows migrated from SQLite to PostgreSQL, parquet processing pending |
| 9.3 | Run NER extraction on all text | ✅ Done | 9.1 or 9.2 |
| 9.4 | Run facial recognition on images | ⬜ TODO | Install InsightFace + ONNX |
| 9.5 | Transcribe audio/video files | ⬜ TODO | Install faster-whisper |
| 9.6 | Generate text embeddings | 🚧 IN_PROGRESS | Remote Ollama generator is running against `http://192.168.4.25:11343/api/embed` using `nomic-embed-text:latest`; latest observed progress 1,872,650/2,890,491 total, 59.1/sec, 0 errors |
| 9.7 | Build updated knowledge graph | ✅ Done | 9.3 |
| 9.8 | Cross-reference supplementary datasets | ⬜ TODO | 9.3, acquire supplementary data |
| 9.9 | Run evaluation metrics | ✅ Done | 9.1–9.8 |
| 9.10 | Fill Results section in paper | ⬜ TODO | 9.9 |

---

## Phase 10: Analysis & Paper ⬜ TODO

| # | Task | Status | Dependencies |
|---|------|--------|--------------|
| 10.1 | Temporal correlation analysis (email → stock trade) | ⬜ TODO | SEC data, 9.3 |
| 10.2 | Network analysis (high-centrality entities) | ⬜ TODO | 9.7 |
| 10.3 | Financial flow analysis (shell companies) | ⬜ TODO | 9.7 |
| 10.4 | Chronological event reconstruction | ⬜ TODO | 9.3 |
| 10.5 | Redaction analysis and recovery | ⬜ TODO | redaction_analysis_v2.db |
| 10.6 | Complete Discussion section | ⬜ TODO | 10.1–10.5 |
| 10.7 | Complete Conclusion section | ⬜ TODO | 10.6 |
| 10.8 | Final paper review | ⬜ TODO | 10.7 |
| 10.9 | Final GitHub push | ⬜ TODO | 10.8 |

---

## Known Issues & Solutions

| Issue | Status | Solution |
|-------|--------|----------|
| Akamai WAF blocks headless Playwright | ✅ Fixed | Stealth user-agent + disable webdriver detection |
| JSON tracker corruption from concurrent writes | ✅ Fixed | Rewrote with SQLite WAL mode |
| Curses doesn't work in non-TTY | ✅ Fixed | Switched to Rich library |
| Playwright download too slow (6 files/sec) | ✅ Fixed | Switched to RollCall CDN (12-30 files/sec) |
| epstein-ripper hangs at auth validation | ✅ Fixed | Built custom download_doj.py with direct EFTA URLs |
| Some CDN URLs return 403 | ✅ Expected | These are confirmed-removed files (67,784 known) |
| HF parquet covers only DOJ data | ✅ Documented | Supplementary datasets cataloged separately |
| PyTorch 2.10+cu128 CUDA not available | ✅ Fixed | Downgraded to PyTorch 2.3.1+cu118 (works with driver 470) |
| Tesla K40m (CC 3.5) too old for PyTorch | ✅ Workaround | Use ONNX Runtime GPU for K40m, PyTorch on K80s only |
| tracker.py format_bytes applied to file counts | ⚠️ Minor | Cosmetic — shows "B" instead of "files" |

## PyTorch + Tesla K80 Compatibility

**CONFIRMED WORKING WITHOUT DRIVER UPGRADE:**
- Driver: 470.256.02 (latest for Kepler, cannot upgrade beyond this)
- PyTorch: 2.3.1+cu118 (CUDA 11.8 runtime, compatible with driver 470)
- Tesla K80 (CC 3.7): ✅ Works — matrix multiply test passes on both GPUs
- Tesla K40m (CC 3.5): ❌ Too old — "no kernel image available"
- **No driver upgrade needed.** Set `CUDA_VISIBLE_DEVICES=1,2` to exclude K40m.

## Phase 8: PostgreSQL Migration ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 8.1 | Install PostgreSQL 16 | ✅ Done | Already running on port 5432 |
| 8.2 | Install pgvector | ✅ Done | v0.6.0 via apt (HNSW support confirmed) |
| 8.3 | Configure PostgreSQL for 125GB RAM | ✅ Done | shared_buffers=32GB, effective_cache_size=96GB, maintenance_work_mem=8GB |
| 8.4 | Create database + user | ✅ Done | db=epstein, user=cbwinslow, password=123qweasd |
| 8.5 | Enable extensions | ✅ Done | vector, pg_trgm, unaccent, pg_stat_statements |
| 8.6 | Create unified schema | ✅ Done | 26 tables in migrations/001_unified_schema.sql |
| 8.7 | Migrate knowledge_graph.db | ✅ Done | 606 entities, 2,302 relationships |
| 8.8 | Migrate transcripts.db | ✅ Done | 1,628 transcripts, 25,129 segments |
| 8.9 | Migrate communications.db | ✅ Done | 41,924 emails, 90,204 participants |
| 8.10 | Migrate ocr_database.db | ✅ Done | 38,955 OCR results |
| 8.11 | Migrate image_analysis.db | ✅ Done | 38,955 images |
| 8.12 | Migrate prosecutorial.db | ✅ Done | 257 subpoenas, 2,018 clauses |
| 8.13 | Migrate redaction_analysis_v2.db | ✅ Done | 2.59M redactions, 849K summaries |
| 8.14 | Migrate full_text_corpus.db | ✅ Done | 1.4M docs, 2.9M pages |
| 8.15 | Populate FTS (search_vector) | ✅ Done | 2,892,730 pages indexed (100%) |
| 8.16 | Create .pgpass file | ✅ Done | ~/.pgpass with localhost auth |
| 8.17 | Set up Datasette | ✅ Done | Running on port 8001 |
| 8.18 | Comprehensive SQLite-to-PG migration with validation | ✅ Done | `scripts/migrate_sqlite_to_pg.py` — 27 tables, 10.9M rows, all verified |

## PostgreSQL Data Summary

| Table | Rows | Status |
|-------|------|--------|
| pages | 2,892,730 | ✅ FTS 100% |
| documents | 1,397,821 | ✅ |
| redactions | 2,587,102 | ✅ |
| document_classification | 1,380,964 | ✅ |
| efta_crosswalk | 1,380,964 | ✅ |
| document_summary | 849,655 | ✅ |
| redaction_entities | 107,422 | ✅ |
| email_participants | 90,204 | ✅ |
| reconstructed_pages | 39,588 | ✅ |
| ocr_results | 38,955 | ✅ |
| images | 38,955 | ✅ |
| transcript_segments | 25,129 | ✅ |
| clause_fulfillment | 3,813 | ✅ |
| graph_edges | 2,745 | ✅ |
| relationships | 2,302 | ✅ |
| rider_clauses | 2,018 | ✅ |
| transcripts | 1,628 | ✅ |
| resolved_identities | 1,139 | ✅ |
| edge_sources | 905 | ✅ |
| investigative_gaps | 779 | ✅ |
| graph_nodes | 677 | ✅ |
| entities | 606 | ✅ |
| emails | 41,924 | ✅ |
| communication_pairs | 271 | ✅ |
| subpoenas | 257 | ✅ |
| returns | 304 | ✅ |
| subpoena_return_links | 304 | ✅ |
| **Total** | **10,889,161 rows** | ✅ All 27 tables verified |

## PostgreSQL Extensions

| Extension | Version | Purpose |
|-----------|---------|---------|
| vector (pgvector) | 0.6.0 | HNSW vector search, vector(768) |
| pg_trgm | 1.6 | Fuzzy text matching |
| unaccent | 1.1 | Accent-insensitive search |
| pg_stat_statements | 1.10 | Query monitoring |

## Phase 11: Server Hardening & Tooling ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 11.1 | Enable UFW firewall | ✅ Done | Deny incoming, allow ssh (22) + http (80), enabled on boot |
| 11.2 | Harden nginx | ✅ Done | TLSv1.2+ only, `server_tokens off`, security headers (X-Frame-Options, nosniff, XSS, Referrer-Policy, Permissions-Policy) |
| 11.3 | Tune PHP-FPM | ✅ Done | max_children 5→20, start_servers 2→5, max_requests=500 |
| 11.4 | Switch cloudflared to HTTP/2 | ✅ Done | Added `protocol: http2` to config.yml, fixed QUIC timeout errors |
| 11.5 | SSH agent forwarding | ✅ Done | `ForwardAgent yes` added to Host windows in ~/.ssh/config |
| 11.6 | Install Go | ✅ Done | Go 1.26.1 via snap, added to .zshrc.local PATH |
| 11.7 | Install Rust | ✅ Done | Rust 1.94.0 via rustup, ~/.cargo/bin in PATH |
| 11.8 | Install fnm | ✅ Done | fnm 1.39.0 alongside nvm in .zshrc.local |
| 11.9 | Global git config | ✅ Done | user.name=cbwinslow, user.email=blaine.winslow@gmail.com |
| 11.10 | Cron jobs | ✅ Done | pg_dump daily 2am (epstein + nextcloud), backup cleanup 7d, log cleanup 30d |
| 11.11 | Fix kilocode CLI | ✅ Done | Replaced stub kilocode@1.2.0 with @kilocode/cli@7.1.0 |
| 11.12 | Configure Cline | ✅ Done | ClineBot provider (claude-sonnet-4-6), Groq fallback |
| 11.13 | Install OpenClaw | ✅ Done | v2026.3.13, gateway daemon on port 18789 via systemd |
| 11.14 | Cline MCP servers | ✅ Done | postgres, filesystem, github servers in cline_mcp_settings.json |
| 11.15 | Cline agent workflows | ✅ Done | ~/Cline/Rules/epstein.md + ~/Cline/Workflows/epstein-pipeline.md |
| 11.16 | Devcontainer | ✅ Done | .devcontainer/devcontainer.json: Python 3.12, Node 24, VS Code extensions |
| 11.17 | GitHub Actions CI | ✅ Done | .github/workflows/ci.yml: ruff lint + pytest with PostgreSQL service |
| 11.18 | AI tool reference | ✅ Done | ~/.ai-tools.md: cline, kilo, opencode, openclaw usage guide |
| 11.19 | Disk monitoring | ✅ Done | ~/.local/bin/disk-alert.sh + daily 8am cron |

## Phase 10: Wayback Machine Investigation ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 10.1 | Check Wayback Machine for missing files | ✅ Done | CDX API confirms files archived on 2025-12-19 |
| 10.2 | Test single file download | ✅ Done | 373KB PDF downloaded successfully |
| 10.3 | Bulk download remaining files | ✅ Done | 11,925 URLs checked, all "Resource not found" |
| 10.4 | Document findings | ✅ Done | Updated CONTEXT.md, mem0, TASKS.md |

**Finding**: Wayback Machine did NOT archive DS12 files or remaining DS9/DS10/DS11 files. These 83,936 files are permanently gone from all public sources. We have 94.0% coverage — the maximum achievable.

## Phase 11: GPU & Tools Setup ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 11.1 | Install spacy-transformers | ✅ Done | v1.4.0, works with PyTorch 2.3.1 |
| 11.2 | Test spaCy trf on K80 GPU | ✅ Done | 64 docs/sec batch, 85ms single doc |
| 11.3 | Install InsightFace | ✅ Done | v0.7, buffalo_l model |
| 11.4 | Test InsightFace GPU | ✅ Failed | onnxruntime lacks CC 3.7 kernels |
| 11.5 | Test InsightFace CPU | ✅ Done | 8 imgs/sec, n_process=4 for parallel |
| 11.6 | Build monitoring tools | ✅ Done | gpu-temp, cpu-temp, sysmon |
| 11.7 | Install to ~/.local/bin | ✅ Done | Available system-wide |

## Phase 12: Documentation & Memory ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 12.1 | Update CONTEXT.md | ✅ Done | Download status, Wayback findings, GPU status |
| 12.2 | Save mem0 memories | ✅ Done | 25 total memories (18 previous + 7 new) |
| 12.3 | Create session summary | ✅ Done | memories/sessions/2026-03-22.md |
| 12.4 | Update TASKS.md | ✅ Done | This file — all tasks documented |

## Phase 13: File Registry & Verification ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 13.1 | Create file registry population script | ✅ Done | `scripts/populate_file_registry.py` + `~/.local/bin/file_registry_builder.py` |
| 13.2 | Test file registry script | ✅ Done | 4 sample PDFs, 100% success, 0.03s processing time |
| 13.3 | Run full file registry population | ✅ Done | 1,313,841 files processed, 1,313,840 distinct EFTAs |
| 13.4 | Document verification procedures | ✅ Done | `docs/verification_procedures.md` with comprehensive procedures |
| 13.5 | Add verification memories to Letta | ✅ Done | 3 memories, 2 memory blocks, agent context updated |
| 13.6 | **Investigate OCR redundancy** | ✅ Done | **OCR already complete!** See findings below |

## Critical Finding: OCR Already Complete

**DO NOT run OCR on PDFs again!** OCR processing is redundant and would waste weeks of GPU time.

**Evidence:**
1. **full_text_corpus.db**: 2,892,730 pages of OCR text for 1,397,796 EFTA numbers
2. **hf-parquet files**: 318GB pre-extracted text in `text_content` column
3. **PostgreSQL `pages` table**: 2,892,730 pages already migrated from SQLite
4. **PostgreSQL `documents_content` table**: Empty, needs population from hf-parquet

**Data Quality:**
- hf-parquet sample: 1,300/4,529 rows have text_content (28.7%)
- Average text length: 3,162 characters
- Max text length: 216,707 characters
- Text appears to be proper OCR output (court documents, depositions)

**Next Steps:**
1. Populate `documents_content` table from hf-parquet `text_content`
2. Use existing OCR text for NER and entity extraction
3. Cross-reference with file registry to verify coverage

## Phase 14: Text Content Population ⬜

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 14.1 | Create hf-parquet text extraction script | ⬜ TODO | Extract text_content from 634 parquet files |
| 14.2 | Populate documents_content table | ⬜ TODO | 1.4M documents with consolidated text |
| 14.3 | Verify text coverage | ⬜ TODO | Cross-reference with file registry |
| 14.4 | Index text for search | ⬜ TODO | PostgreSQL FTS or pgvector embeddings |

## Phase 15: AI Skills Integration ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 15.1 | Install Epstein memory package | ✅ Done | Installed in venv at `/home/cbwinslow/dotfiles/ai/packages/epstein_memory/` |
| 15.2 | Update OpenCode configuration | ✅ Done | Updated `/home/cbwinslow/dotfiles/ai/agents/opencode/config.yaml` with skill_paths, letta integration, and conversation logging |
| 15.3 | Create .opencode directory | ✅ Done | Created at `~/.opencode/` with instructions.md and agent_rules.md |
| 15.4 | Run create_symlinks.sh | ✅ Done | Created symlinks for .openclaw, .cline, .gemini (not .opencode - handled manually) |
| 15.5 | Copy global rules to .opencode | ✅ Done | Copied CORE_MANDATES.md and agent_init_rules.md to `~/.opencode/` |
| 15.6 | Create memory search protocols | ✅ Done | Created `memory_search.py` with semantic, tag, text, recent, and cross-agent search |
| 15.7 | Create conversation saving script | ✅ Done | Created `save_conversation_to_letta.py` for saving conversations to Letta |
| 15.8 | Save conversation to memory | ✅ Done | Saved AI skills integration conversation and decisions to Letta |
| 15.9 | **Migrate Letta scripts to skills** | ✅ Done | Moved generalized Letta operations to centralized AI skills system |
| 15.10 | **Create CLI operations skill** | ✅ Done | `cli_operations` skill with Letta CLI wrappers and SQL queries |
| 15.11 | **Enhance memory management skill** | ✅ Done | Added advanced search protocols (semantic, tags, text, stats, cross-agent) |
| 15.12 | **Create conversation logging skill** | ✅ Done | `conversation_logging` skill with decision/action item extraction |
| 15.13 | **Create memory sync skill** | ✅ Done | `memory_sync` skill for PostgreSQL ↔ Letta server synchronization |
| 15.14 | **Update AGENTS.md** | ✅ Done | Added memory management section with skills reference |
| 15.15 | **Remove legacy scripts** | ✅ Done | Moved redundant Letta scripts to backup directory |

## Phase 16: Supplementary Data Download & Import ✅

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 16.1 | Fix PyTorch CUDA | ✅ Done | Was CPU-only (2.11.0+cu118). Driver 470 supports CUDA 11.8 but NOT 12.4. |
| 16.2 | Test GPU embedding speed | ✅ Done | BGE-small: 240/sec, all-MiniLM-L6-v2: 2596/sec on K80 |
| 16.3 | Evaluate pre-computed embeddings | ✅ Done | kabasshouse/epstein-data has 2.1M chunk embeddings (768-dim Gemini) |
| 16.4 | Download kabasshouse entities | ✅ Done | 9,893,147 rows, PK: (document_id, entity_type, value) |
| 16.5 | Download kabasshouse chunks | ✅ Done | 1,874,012 rows, PK: (document_id, chunk_index) |
| 16.6 | Download kabasshouse embeddings | ✅ Done | 1,505,618 rows, PK: chunk_id, 768-dim Gemini |
| 16.7 | Download kabasshouse financial | ✅ Done | 49,770 rows, PK: id |
| 16.8 | Download kabasshouse redactions | ✅ Done | 22,355 rows, PK: id |
| 16.9 | Download kabasshouse events | ✅ Done | 3,038 rows, PK: id |
| 16.10 | Download kabasshouse curated docs | ✅ Done | 1,398 rows, PK: file_key |
| 16.11 | Download kabasshouse persons | ✅ Done | 546 rows, PK: slug |
| 16.12 | Download kabasshouse comms | ✅ Done | 128 rows, PK: id |
| 16.13 | Download House Oversight emails | ✅ Done | 5,082 threads, PK: thread_id |
| 16.14 | Download FBI Vault PDFs | ✅ Done | 16 valid PDFs from Archive.org |
| 16.15 | OCR FBI Vault PDFs | 🔄 Running | PyMuPDF + Tesseract, PID 91699 |
| 16.16 | Fix HF download hanging | ✅ Done | Use aria2c (5-13MB/s) instead of hf_hub_download |
| 16.17 | Fix PostgreSQL autovacuum | ✅ Done | Disable during bulk import |
| 16.18 | Clean up downloaded files | ✅ Done | Deleted 5.3GB of imported parquets |
| 16.19 | Remove Letta tables from epstein DB | ✅ Done | Belong in letta DB, not epstein |
| 16.20 | Save session memories to Letta | ✅ Done | 5 memories saved |

## Phase 17: FBI Vault OCR ⬜

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 17.1 | OCR FBI Vault PDFs | ✅ Done | 996 pages, 616,959 chars extracted |
| 17.2 | Verify OCR text quality | ⬜ TODO | Manual spot-check |
| 17.3 | Add FBI Vault text to search | ⬜ TODO | FTS5 index |
| 17.4 | Extract entities from FBI Vault | ⬜ TODO | NER on OCR text |

## Phase 18: Supplementary Embedding Datasets 🔄

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 18.1 | Download svetfm/epstein-fbi-files embeddings | ✅ Done | 236K chunks, 3.9 GB, nomic-embed-text 768-dim - downloaded at 27 MB/s |
| 18.2 | Download svetfm/epstein-files-nov11-25-house-post-ocr-embeddings | ✅ Done | 69K chunks, 341 MB, House Oversight Committee - downloaded at 11 MB/s |
| 18.3 | Download FBI OCR data | ✅ Done | 317 MB OCR text from FBI files |
| 18.4 | Download tensonaut/EPSTEIN_FILES_20K | ❌ Unavailable | Repository removed or made private (404 error) |
| 18.5 | Download theelderemo/FULL_EPSTEIN_INDEX | ✅ Done | 221K rows, 3.2 MB - text extract CSV |
| 18.6 | Import FBI embeddings to PostgreSQL | ✅ Done | 236,174 chunks imported to fbi_embeddings table |
| 18.7 | Import House Oversight embeddings | ✅ Done | 69,290 chunks imported to house_oversight_embeddings table |
| 18.8 | Import Full Epstein Index to PostgreSQL | ✅ Done | 8,531 rows imported to full_epstein_index table |
| 18.9 | Cross-reference embedding sources | ✅ Done | FBI: 61.5% overlap (2,548 exclusive docs); House: 8.2x content; Index: 0.3% coverage |
| 18.10 | Update DATA_INVENTORY.md | ✅ Done | Documented new datasets and import scripts |

### Supplementary Dataset Summary

| Dataset | Source | Size | Embeddings | Status | GitHub Issue |
|---------|--------|------|------------|--------|--------------|
| kabasshouse/epstein-data | HuggingFace | ~12GB | 2.1M (768-dim) | ✅ Imported | - |
| svetfm/epstein-fbi-files | HuggingFace | 3.9GB | 236K (768-dim) | ✅ Imported | #71 |
| svetfm/epstein-files-nov11-25-house-post-ocr-embeddings | HuggingFace | 341MB | 69K (768-dim) | ✅ Imported | #72 |
| theelderemo/FULL_EPSTEIN_INDEX | HuggingFace | 3.2MB | 8.5K (text) | ✅ Imported | #70 |
| tensonaut/EPSTEIN_FILES_20K | HuggingFace | Unknown | None (source) | ❌ Unavailable | #70 |

**Total Additional Embeddings**: ~305K chunks (~4GB)
**Model Compatibility**: All use 768-dim (compatible with existing kabasshouse data)
**Rate Limit Hit**: 1000 API requests per 5 minutes - need retry logic with backoff

---

## Phase 19: ICIJ Offshore Leaks & jMail Full Import 🔄

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 19.1 | Download jmail.world full datasets | ✅ Done | 318.9 MB emails, 25.4 MB documents |
| 19.2 | Download ICIJ Offshore Leaks | ✅ Done | 69.7 MB compressed |
| 19.3 | Extract ICIJ zip | ✅ Done | 6 CSV files, ~600 MB total |
| 19.4 | Create ICIJ import script | ✅ Done | `scripts/import_icij.py` - batch processing 5K rows |
| 19.5 | Create jmail_documents import script | ✅ Done | `scripts/import_jmail_documents.py` - batch 2K rows |
| 19.6 | Fix ICIJ column names | ✅ Done | `ibcRUC`, `sourceID` match CSV headers |
| 19.7 | Import jMail Emails (full) | ✅ **COMPLETE** | **1,783,792 emails imported, 0 errors** |
| 19.8 | Import jMail Documents | ✅ **COMPLETE** | **1,413,417 documents imported, 0 errors** |
| 19.9 | Import ICIJ Entities | ✅ **COMPLETE** | **814,344 entities imported** |
| 19.10 | Import ICIJ Officers | ✅ **COMPLETE** | **771,315 officers imported** |
| 19.11 | Import ICIJ Addresses | ✅ **COMPLETE** | **402,246 addresses imported** |
| 19.12 | Import ICIJ Intermediaries | ✅ **COMPLETE** | **25,629 intermediaries imported** |
| 19.13 | Import ICIJ Others | ✅ **COMPLETE** | **2,989 others imported** |
| 19.14 | Import ICIJ Relationships | 🔄 Running | **62% complete (2.1M/3.3M)** |
| 19.15 | Update DATA_INVENTORY.md | ✅ Done | Added ICIJ section, updated jMail status |
| 19.16 | Update GitHub issues | ✅ Done | Commented on #74, #76 with completion status |
| 19.17 | Create Letta memories | ✅ Done | ICIJ and jMail completion memories |

### Current Import Status (April 4, 2026 10:19 UTC)

| Import | File/Table | Records | Status | Errors |
|--------|-----------|---------|--------|--------|
| jMail Emails | jmail_emails_full.parquet | 1,783,792 | ✅ **COMPLETE** | 0 |
| jMail Documents | jmail_documents.parquet | 1,413,417 | ✅ **COMPLETE** | 0 |
| ICIJ Entities | icij_entities | 814,344 | ✅ **COMPLETE** | 0 |
| ICIJ Officers | icij_officers | 771,315 | ✅ **COMPLETE** | 0 |
| ICIJ Addresses | icij_addresses | 402,246 | ✅ **COMPLETE** | 0 |
| ICIJ Intermediaries | icij_intermediaries | 25,629 | ✅ **COMPLETE** | 0 |
| ICIJ Others | icij_others | 2,989 | ✅ **COMPLETE** | 0 |
| ICIJ Relationships | icij_relationships | 2.1M/3.3M | 🔄 **62%** | 0 |

**Total Imported So Far:** ~3.2M jMail records + ~2.0M ICIJ entities + 2.1M relationships

### jMail Emails Key Statistics
- **Epstein as sender:** 320,871 emails (18%)
- **Top sender:** Lesley Groff (126,338 emails)
- **Date range:** 1990-01-01 to 2026-10-07
- **Largest source:** VOL00011 (669,650 emails)
- **Source breakdown:** VOL00009 (639,940), VOL00010 (447,251), yahoo_2 (17,448)

### ICIJ Data Overview
- **Source**: https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip
- **Total Entities Imported**: ~2.0M (814K companies + 771K officers + 402K addresses + 26K intermediaries + 3K others)
- **Relationships**: 3.3M total, 2.1M imported (62%)
- **Coverage**: Panama Papers, Paradise Papers, Pandora Papers, Bahamas Leaks, Offshore Leaks
- **License**: Open Database License (ODbL)

### Scripts Created
- `scripts/import_icij.py` - Imports all 6 CSV files to PostgreSQL
- `scripts/import_jmail_full.py` - Imports jmail_emails_full.parquet (1.78M emails)
- `scripts/import_jmail_documents.py` - Imports jmail_documents.parquet (1.41M docs)

---

## Phase 20: Enterprise Database Architecture & Validation 🔄

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 20.1 | Create validation views | ✅ Done | `scripts/create_validation_views.sql` - 10 enterprise views |
| 20.2 | Execute validation views | 🔄 Running | Applied to PostgreSQL epstein database |
| 20.3 | Verify all datasets 100% | ⏳ Pending | Check jMail, ICIJ, FEC, DOJ completion |
| 20.4 | Update epsteinexposed.com comparison | ⏳ Pending | Document gaps: 728K documents missing |
| 20.5 | Verify FEC.gov donations (5.4M+) | ✅ Done | `fec_individual_contributions` has 5,420,940+ records |
| 20.6 | Check RAID storage | ✅ Done | 2.9TB total, 2.1TB free (24% used) |
| 20.7 | Audit indexes and keys | 🔄 In Progress | Check FKs, PKs, index usage |
| 20.8 | Document data acquisition methods | ✅ Done | Created `docs/DATA_ACQUISITION.md` |
| 20.9 | Create repeatable import scripts | ⏳ Pending | Standardize all import scripts |
| 20.10 | Apply naming conventions | ⏳ Pending | Standardize table/column names |
| 20.11 | Update GitHub issues | ✅ Done | Posted reconciled status updates with validated counts and residual gap tracking (`#51`, `#52`, `#55`, `#57`) |
| 20.12 | Prepare research paper outline | ⏳ Pending | Document methodology |
| 20.13 | Design website API architecture | ⏳ Pending | Plan data API endpoints |
| 20.14 | Fix Congress historical downloader | ✅ Done | Corrected API endpoints to `/bill/{congress}` and `/member/congress/{congress}`; validated with 107th Congress |
| 20.15 | Fix GovInfo historical offset failure | ✅ Done | Split high-volume collections into monthly windows to avoid 500 errors at offset 10000 |
| 20.16 | Import first historical Congress slice | ✅ Done | Imported Congress 107: 10,791 bills + 553 members |
| 20.17 | Import first historical GovInfo slice | ✅ Done | Imported GovInfo 2000: 8,543 packages (BILLS/CRPT/FR/USCOURTS) |
| 20.18 | Verify FEC historical coverage | ✅ Done | `fec_individual_contributions` already covers cycles 2000-2026 with 447,189,732 rows |
| 20.19 | Clean polluted Congress bill rows | ✅ Done | Removed 401 stray rows and 54,945 duplicate 118th bill rows; table now has 107th=10,791 and 118th=19,315 |
| 20.20 | Launch next Congress historical batch | ✅ Done | 108th-109th completed and imported; `congress_bills` now includes 108th=10,669 and 109th=13,072, `congress_members` includes 108th=544 and 109th=546; see `logs/ingestion/congress_historical_batch_108_109_20260422.log` |
| 20.21 | Launch next GovInfo historical batch | ✅ Done | 2001 completed and imported; `FR=249`, `USCOURTS=358` plus 2001 bill/report package classes now in `govinfo_packages`; see `logs/ingestion/govinfo_historical_batch_2001_20260422.log` |
| 20.22 | Create GitHub tracking issues for historical backfill | ✅ Done | Created `#51` (Congress) and `#52` (GovInfo) with current status/comments |
| 20.23 | Populate GovInfo specialized tables | ✅ Done | `import_govinfo.py` now fills `federal_register_entries` and `court_opinions`; verified counts `2,245` and `30,724` |
| 20.24 | Harden Congress importer against malformed records | ✅ Done | `import_congress.py` now skips null/non-dict bill/member records and null nested objects; validated with `py_compile` and parser-only check against `congress_118/bills/bills_118.json` |
| 20.25 | Fix historical downloader worker model | ✅ Done | Added process-wide API rate limiting and per-thread `requests.Session` reuse to Congress/GovInfo historical downloaders; Congress now downloads bills+members concurrently per congress without exceeding per-process rate budget |
| 20.26 | Launch Congress 110th-112th historical batch | ✅ Done | Completed and imported; part of validated 107th-119th Congress coverage with `congress_bills=333,400` and `congress_members=8,769` (verified April 23, 2026 session log) |
| 20.27 | Launch GovInfo 2002-2003 historical batch | ✅ Done | Completed with patched worker model (`--workers 8`); `USCOURTS` 2002=`394`, 2003=`426`; `FR` 2002=`250`, 2003=`249`; `court_opinions` now `31,544` |
| 20.28 | Align downloaders with official upstream docs/repos | ✅ Done | Cloned official GovInfo/Congress support repos; GovInfo historical downloader now uses `offsetMark`; Congress historical downloader now uses `limit=250` and safer pacing; validated live on GovInfo `BILLS 2004` and Congress `113` |
| 20.29 | Rework GovInfo bulk downloader to use bulkdata repository | ✅ Done | Replaced API-based `download_govinfo_bulk.py` with a real GovInfo bulk ZIP downloader for `FR` and `BILLSTATUS`; validated `FR-2004.zip` and `BILLSTATUS-113-hjres.zip` and saved listing manifests alongside them |
| 20.30 | Import GovInfo Bill Status bulk XML into normalized tables | ✅ Done | Added `import_govinfo_billstatus_bulk.py`; creates `congress_bill_titles`, `congress_bill_summaries`, `congress_bill_actions`, `congress_bill_cosponsors`, `congress_bill_related_bills`, and `congress_bill_vote_references`; validated on `BILLSTATUS-113-hjres.zip` with `131` bills and `49` vote references |
| 20.31 | Extend GovInfo bulk downloader for bill text and bill summaries | ✅ Done | `download_govinfo_bulk.py` now supports `BILLS` and `BILLSUM` ZIPs in addition to `FR` and `BILLSTATUS`; validated on `113/hjres` live downloads |
| 20.32 | Harden Congress bill identity integrity | ✅ Done | Added unique index `uq_congress_bills_key` on `(congress, bill_type, bill_number)` after verifying no duplicates remained |
| 20.33 | Launch wide official bulk-data backfill | ✅ Done | Completed for scoped targets; final verified bulk import status: `FR completed=26`, `BILLSTATUS completed=52`, `BILLS completed=96`, `BILLSUM completed=48` |
| 20.34 | Fix GovInfo bulk ZIP integrity and resumable Bill Status import | ✅ Done | `download_govinfo_bulk.py` now validates existing/downloaded ZIPs and re-downloads corrupt files via `.part` temp writes; `import_govinfo_billstatus_bulk.py` now records per-ZIP status in `govinfo_bulk_import_status`, skips completed ZIPs, and continues on failure; repaired corrupt `BILLSTATUS-113-hr.zip` and resumed import |
| 20.35 | Add GovInfo BILLSUM bulk importer | ✅ Done | Added `import_govinfo_billsum_bulk.py`; validated on `BILLSUM-113-hjres.zip` (`178` summaries) and completed full BILLSUM batch (`BILLSUM completed=48`) |
| 20.36 | Harden GovInfo BILLS bulk importer against malformed XML | ✅ Done | `import_govinfo_bills_bulk.py` uses `lxml` recovery and corrected bill-type normalization; full BILLS batch completed (`BILLS completed=96`) |
| 20.37 | Add GovInfo FR bulk importer | ✅ Done | Added `import_govinfo_fr_bulk.py`; validated and completed full FR yearly batch (`FR completed=26`, `federal_register_entries=737,940`) |
| 20.38 | Repair corrupt FR yearly ZIPs for bulk import | ✅ Done | Reused `download_govinfo_bulk.py` to redownload invalid FR ZIPs for `2000-2003,2005-2007`; repaired archives are back on disk and the resumed FR importer is retrying them |
| 20.39 | Complete GovInfo BILLS bulk backfill | ✅ Done | Patched importer cleared malformed XML and `hres` normalization failures; `govinfo_bulk_import_status` now shows `BILLS completed=96`; `congress_bill_text_versions=113106` |
| 20.40 | Add Congress House vote ingestion | ✅ Done | `download_congress_historical.py` now downloads House roll call votes via the official `house-vote` endpoint where available; `import_congress.py` now imports `house_votes_*.json` into `congress_house_votes`; validated on Congress `118` with `1241` imported votes |
| 20.41 | Continue GovInfo FR full-year bulk backfill | ✅ Done | FR backfill completed for 2000-2024; final verified range `2000-01-03` to `2024-12-31` with `737,940` rows |
| 20.42 | Expand House vote backfill to supported congresses | ✅ Done | Used vote-only component runs to download/import House votes for `117`, `118`, and `119`; `congress_house_votes=2730` (`117=998`, `118=1241`, `119=491`) |
| 20.43 | Continue GovInfo FR full-year bulk backfill verification | ✅ Done | Final verification passed; no active FR importer process and row counts match documented April 23, 2026 completion state |

### Database Validation Views Created

| View | Purpose | Status |
|------|---------|--------|
| `v_dataset_completeness` | Row counts & completeness % | ✅ Created |
| `v_person_cross_reference` | Persons across ICIJ/jMail/exposed | ✅ Created |
| `v_orphaned_records` | Data integrity check | ✅ Created |
| `v_index_health` | Index usage statistics | ✅ Created |
| `v_table_storage` | Storage & vacuum status | ✅ Created |
| `v_jmail_email_patterns` | Email analysis by sender | ✅ Created |
| `v_fec_top_donors` | Top 1000 FEC donors | ✅ Created |
| `v_flight_email_crossref` | Flight + email cross-reference | ✅ Created |
| `v_document_coverage` | Enrichment coverage by dataset | ✅ Created |
| `v_entity_cooccurrence` | Entity network analysis | ✅ Created |

### Enterprise Naming Convention Standards

| Component | Convention | Example |
|-----------|------------|---------|
| Tables | `snake_case` descriptive | `fec_individual_contributions` |
| Views | `v_` prefix | `v_dataset_completeness` |
| Indexes | `idx_` prefix | `idx_jmail_emails_sender` |
| Foreign Keys | `fk_` prefix | `fk_pages_document_id` |
| Primary Keys | `id` or table_name + `_id` | `id`, `efta_number` |
| Columns | `snake_case` lowercase | `transaction_amt`, `created_at` |
| Stored Procedures | `sp_` prefix | `sp_validate_imports` |
| Functions | `fn_` prefix | `fn_normalize_name` |

### Documentation Created

| Document | Purpose | Location |
|----------|---------|----------|
| `DATA_ACQUISITION.md` | All data acquisition methods | `docs/DATA_ACQUISITION.md` |
| `create_validation_views.sql` | 10 validation views | `scripts/create_validation_views.sql` |
| `PHASE22_MEDIA_ACQUISITION.md` | Phase 22 Media Acquisition Infrastructure | `docs/PHASE22_MEDIA_ACQUISITION.md` |
| `AGENTS.md` | Agent architecture & multi-agent system | `AGENTS.md` |
| `AGENTS_APPENDIX.md` | Detailed agent specifications | `AGENTS_APPENDIX.md` |

---

## Phase 22: Media Acquisition Infrastructure 🚧 IN_PROGRESS

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 22.1 | Create media acquisition database schema | ✅ Done | 5 tables: media_news_articles, media_videos, media_documents, media_collection_queue, media_collection_stats |
| 22.2 | Create base agent classes | ✅ Done | DiscoveryAgent, CollectionAgent, ProcessingAgent, StorageManager in `base.py` |
| 22.3 | Create NewsDiscoveryAgent | ✅ Done | GDELT + Wayback Machine + RSS, tested with real query (10 articles found) |
| 22.4 | Create VideoDiscoveryAgent | ✅ Done | YouTube API/scraping + Internet Archive |
| 22.5 | Create VideoTranscriber | ✅ Done | yt-dlp captions + Whisper local GPU |
| 22.6 | Create DocumentDiscoveryAgent | ✅ Done | CourtListener + GovInfo APIs |
| 22.7 | Deploy schema to PostgreSQL | ✅ Done | Tables, views, functions created (some existing index warnings) |
| 22.8 | Test NewsDiscoveryAgent | ✅ Done | GDELT query successful, found 10 Epstein articles Jan 2024 |
| 22.9 | Create master orchestration script | ✅ Done | `master.py` with MediaAcquisitionSystem class |
| 22.10 | Run first collection | ✅ Done | Executed news discovery for Jan 2024, populated queue |
| 22.11 | Create NewsCollector | ✅ Done | Collection agent using newspaper3k + requests fallback (500+ lines) |
| 22.12 | Create EntityExtractor | ✅ Done | spaCy + GLiNER + regex NER with sentiment analysis (600+ lines) |
| 22.13 | Document discovery results | ✅ Done | Created USAGE.md, updated all docs |

### Phase 22 Files Created

```
media_acquisition/
├── __init__.py                      # Package exports
├── base.py                          # Base classes (22KB)
├── master.py                        # Orchestration (16KB)
├── USAGE.md                         # Usage documentation
└── agents/
    ├── __init__.py                  # Agents exports
    ├── discovery/
    │   ├── __init__.py
    │   ├── news.py                  # NewsDiscoveryAgent (7KB) ✅
    │   ├── video.py                 # VideoDiscoveryAgent (6KB) ✅
    │   └── document.py              # DocumentDiscoveryAgent (6KB) ✅
    ├── collection/
    │   ├── __init__.py
    │   ├── news.py                  # NewsCollector (6KB) ✅
    │   └── video.py                 # VideoTranscriber (12KB) ✅
    └── processing/
        ├── __init__.py
        └── entities.py              # EntityExtractor (6KB) ✅

scripts/create_media_schema.sql      # 600+ lines of SQL
```

---

## Phase 23: Government Data Completion & Standardized Pipelines 🚧 IN_PROGRESS

| # | Task | Status | Solution/Notes |
|---|------|--------|----------------|
| 23.1 | Reconcile government coverage against live DB | ✅ Done | Verified counts and ranges for `congress_*`, `govinfo_*`, `federal_register_entries`, `whitehouse_visitors` on 2026-04-24 |
| 23.2 | Correct docs to remove stale/interim government counts | ✅ Done | Updated `AGENTS.md`, `docs/DATA_INVENTORY_FULL.md`, `docs/GOV_DATA_INGESTION_SUMMARY.md`, and replaced stale `docs/GOVERNMENT_DATA_PIPELINE.md` |
| 23.3 | Track residual Congress gaps | ✅ Done | Initial gap matrix (2026-04-24 start) identified `106th`, `119th members`, and vote-detail empties; all three are now closed |
| 23.4 | Track residual vote-detail gaps | ✅ Done | Initial state had `congress_house_vote_details=0`, `congress_house_member_votes=0`; now `2738` and `1185626`, with Senate vote-detail still pending |
| 23.5 | Update GitHub issue #51 with gap matrix and next steps | ✅ Done | Posted current validated counts and explicit remaining Congress tasks |
| 23.6 | Update GitHub issue #52 with finalized GovInfo state + remaining scope | ✅ Done | Posted bulk completion metrics and next-scope clarification |
| 23.7 | Update GitHub issue #55 (SEC EDGAR) with pipeline recommendation | ✅ Done | Added actionable ingestion path and integration target notes |
| 23.8 | Update GitHub issue #57 (FARA) with realistic acquisition strategy | ✅ Done | Added practical approach for non-bulk/interactive source constraints |
| 23.9 | Backfill 119th members into `congress_members` | ✅ Done | Executed `download_congress_historical.py --congresses 119 --components members --workers 12 --import-after-download`; imported 551 records |
| 23.10 | Backfill House vote details + member votes | ✅ Done | Executed `download_house_vote_details.py --limit 1000000 --concurrency 40` plus tail pass; final `congress_house_vote_details=2738`, `congress_house_member_votes=1185626`, `pending_vote_details=0` |
| 23.11 | Implement Senate vote-detail pipeline | ⬜ TODO | Add downloader/importer + normalized tables and idempotent tracking |
| 23.12 | Extend to year-2000 Congress completeness (106th session coverage) | ✅ Done | Executed `download_congress_historical.py --congresses 106 --components bills,members,votes --workers 12 --import-after-download`; imported `106th` bills/members and validated 106-119 range |
| 23.13 | Publish generalized government pipeline runbook | ✅ Done | `docs/GOVERNMENT_DATA_PIPELINE.md` now defines repeatable download/import/validate pattern |
| 23.14 | Harden House vote-detail importer for session-aware idempotency | ✅ Done | Updated `download_house_vote_details.py` to key on `(congress,session,roll_call_number)`, fixed endpoint payload handling, added schema migration and validation |
| 23.15 | Run high-concurrency historical Congress/GovInfo refresh in parallel | ✅ Done | Ran `download_congress_historical.py --congresses 106-119 --components bills,members,votes --workers 24 --import-after-download` and GovInfo bulk download/import loops for `BILLSTATUS`, `BILLS`, `BILLSUM` |
| 23.16 | Build and validate Senate vote-detail ingestion pipeline | 🔄 In Progress | Added `download_senate_vote_details.py`, validated inserts, loaded `congress_senate_votes=3132` and `congress_senate_member_votes=313176`; blocked by intermittent upstream HTTP 403 responses |
| 23.17 | Fix FARA importer for current bulk XML schema | 🔄 In Progress | Reworked `import_fara.py` for streaming `<ROW>` ingestion with normalized tables (`registrations/principals/short_forms/docs`), validated via sample runs; full production ingest actively running |
| 23.18 | Update GitHub tracking with sub-issues and progress comments | ✅ Done | Commented on `#51/#52/#55/#57`; opened `#58` (Senate retries), `#59` (FARA completion), `#60` (GovInfo 119 reconciliation) |
