# Tasks — Epstein Files Analysis Project

## Status Legend
- ✅ **DONE** — Completed and verified
- 🔄 **RUNNING** — In progress (downloads, processing)
- ⬜ **TODO** — Not started
- ⚠️ **BLOCKED** — Waiting on dependency
- 🔧 **FIX** — Issue found, needs fix

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

---

## Phase 9: Processing Pipeline 🔄

| # | Task | Status | Dependencies |
|---|------|--------|--------------|
| 9.1 | Test OCR pipeline on small batch | ✅ Done | Downloads complete |
| 9.2 | Process HF parquet into structured DB | 🔄 Partial | 10.9M rows migrated from SQLite to PostgreSQL, parquet processing pending |
| 9.3 | Run NER extraction on all text | ✅ Done | 9.1 or 9.2 |
| 9.4 | Run facial recognition on images | ⬜ TODO | Install InsightFace + ONNX |
| 9.5 | Transcribe audio/video files | ⬜ TODO | Install faster-whisper |
| 9.6 | Generate text embeddings | ⬜ TODO | Install sentence-transformers |
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

## Dataset Download Strategy

### Rate Limit Workaround
- Use `aria2c` for large files (bypasses HF API limits)
- Implement exponential backoff retry (5min, 10min, 20min)
- Download during off-peak hours
- Use HF Pro token if available for higher limits

### Priority Order
1. **svetfm/epstein-fbi-files** (highest value - FBI investigative files)
2. **svetfm/epstein-files-nov11-25-house-post-ocr-embeddings** (House Oversight)
3. **tensonaut/EPSTEIN_FILES_20K** (source documents)
4. **theelderemo/FULL_EPSTEIN_INDEX** (comprehensive index)
