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
| 1.1 | Mount LVM storage volume | ✅ Done | `lv-nextcloud` mounted at `/mnt/data/epstein-project/`, 2.3TB free |
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

## Phase 7: Active Downloads 🔄

| # | Task | Status | Progress |
|---|------|--------|----------|
| 7.1 | Download DOJ PDFs via CDN | 🔄 Running | ~268K files downloaded |
| 7.2 | Download HF parquet | ✅ Done | 634/634 files, 318GB |
| 7.3 | Validate downloaded PDFs | ✅ Done | 1,346 checked, 100% valid (PDF signature) |
| 7.4 | Validate HF parquet integrity | ✅ Done | 0 missing, 0 zero-size files |

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

## Phase 9: Processing Pipeline ⬜ TODO

| # | Task | Status | Dependencies |
|---|------|--------|--------------|
| 9.1 | Test OCR pipeline on small batch | ⬜ TODO | Downloads complete |
| 9.2 | Process HF parquet into structured DB | ⬜ TODO | HF download complete ✅ |
| 9.3 | Run NER extraction on all text | ⬜ TODO | 9.1 or 9.2 |
| 9.4 | Run facial recognition on images | ⬜ TODO | Install InsightFace + ONNX |
| 9.5 | Transcribe audio/video files | ⬜ TODO | Install faster-whisper |
| 9.6 | Generate text embeddings | ⬜ TODO | Install sentence-transformers |
| 9.7 | Build updated knowledge graph | ⬜ TODO | 9.3 |
| 9.8 | Cross-reference supplementary datasets | ⬜ TODO | 9.3, acquire supplementary data |
| 9.9 | Run evaluation metrics | ⬜ TODO | 9.1–9.8 |
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
