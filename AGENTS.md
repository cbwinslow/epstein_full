# Epstein Files Analysis - Agent Configuration

> **Last Updated:** April 24, 2026
> **Purpose:** Master configuration for AI agents working on Epstein data analysis

## 📚 Documentation Structure

| Document | Purpose | Location |
|----------|---------|----------|
| **DATA_INVENTORY_FULL.md** | Complete data source catalog | `docs/DATA_INVENTORY_FULL.md` |
| **MASTER_INDEX.md** | Central index for all agents | `docs/agents/MASTER_INDEX.md` |
| **INGESTION_GUIDES/** | Per-source detailed procedures | `docs/agents/INGESTION_GUIDES/` |
| **GDELT_PIPELINE.md** | News ingestion pipeline | `docs/GDELT_PIPELINE.md` |

### Quick Links for AI Agents

- **Data Sources Overview:** See `docs/agents/MASTER_INDEX.md`
- **Ingestion Procedures:** See `docs/agents/INGESTION_GUIDES/`
- **Current Data Status:** See `docs/DATA_INVENTORY_FULL.md`
- **Coverage Gaps:** Senate vote-detail pipeline, pre-107th Congress expansion path, and pre-2009 White House logs

---

## Agent Architecture

### Worker Agents
We use a multi-agent architecture with specialized workers:

#### 1. Download Agent (`download-worker`)
- **Role**: Download files from DOJ website
- **Tools**: epstein-ripper (Playwright), aiohttp
- **Concurrency**: 5 parallel download workers per dataset
- **Rate Limit**: 0.75s between downloads, 0.5s between pages
- **Resume**: State files per dataset for resumable downloads
- **Validation**: PDF signature check, HTML/corruption detection

#### 2. OCR Agent (`ocr-worker`)
- **Role**: Extract text from PDFs
- **Tools**: PyMuPDF (instant), Surya (fast, GPU), Docling (fallback)
- **GPU**: Uses Tesla K80 for Surya OCR
- **Output**: JSON with per-page text + confidence scores

#### 3. NER Agent (`ner-worker`)
- **Role**: Extract named entities from OCR text
- **Tools**: spaCy en_core_web_trf, GLiNER zero-shot, regex patterns
- **Entities**: people, organizations, locations, dates, case numbers, flight IDs, financial amounts, Bates numbers
- **GPU**: Optional for transformer models

#### 4. Transcription Agent (`transcribe-worker`)
- **Role**: Transcribe audio/video files
- **Tools**: faster-whisper large-v3
- **GPU**: Tesla K80/K40m
- **Input**: .mp4, .avi, .m4a, .mp3, .wav files from datasets

#### 5. Image Analysis Agent (`image-worker`)
- **Role**: Analyze images extracted from PDFs
- **Tools**: Vision models, PIL, face detection
- **GPU**: Tesla K80
- **Output**: Image descriptions, face detection, object recognition

#### 6. Knowledge Graph Agent (`kg-worker`)
- **Role**: Build and update knowledge graph
- **Tools**: spaCy NER, co-occurrence analysis, relationship extraction
- **Storage**: SQLite + Neo4j (optional)
- **Output**: Entity relationships, confidence scores

### Command Structure

```
epstein-pipeline/
├── download doj --dataset N     # Download specific dataset
├── ocr ./raw-pdfs/ -o ./out/    # OCR processing
├── extract-entities ./out/      # NER extraction
├── transcribe ./media/          # Audio/video transcription
├── extract-images ./pdfs/       # Image extraction
├── build-graph ./processed/     # Knowledge graph building
├── dedup ./processed/           # Deduplication
├── embed ./processed/           # Embedding generation
├── export neon/JSON/CSV/SQLite  # Export formats
└── search "query"               # Semantic search
```

### Workflow Pipeline

```
[DOJ Website] → [Download Workers] → [Raw PDFs/Media]
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
            [OCR Worker]              [Transcription Worker]    [Image Extractor]
                    │                         │                         │
                    ▼                         ▼                         ▼
            [Text + Confidence]       [Speech + Timestamps]    [Images + Metadata]
                    │                         │                         │
                    └─────────────────────────┼─────────────────────────┘
                                              ▼
                                    [NER Extraction Worker]
                                              │
                                    ┌─────────┼─────────┐
                                    ▼         ▼         ▼
                              [Entities] [Dedup] [Classifier]
                                    │         │         │
                                    └─────────┼─────────┘
                                              ▼
                                    [Knowledge Graph Builder]
                                              │
                                    ┌─────────┼─────────┐
                                    ▼         ▼         ▼
                                 [SQLite]  [Neo4j]  [Export]
```

### GPU Allocation
- **Tesla K80 (0)**: OCR (Surya) + Image Analysis
- **Tesla K80 (1)**: Transcription (faster-whisper) + NER (spaCy trf)
- **Tesla K40m (2)**: Embeddings + Classification (overflow)

### Storage Layout

```
/home/cbwinslow/workspace/epstein-data/
├── raw-files/           # Downloaded PDFs and media
│   ├── data1/           # Dataset 1
│   ├── data2/           # Dataset 2
│   └── ...
│   ├── congress_historical/   # Congress.gov historical downloads (107th+)
│   └── govinfo_historical/    # GovInfo historical downloads (2000+)
├── databases/           # Pre-built SQLite databases
│   ├── knowledge_graph.db
│   ├── redaction_analysis_v2.db
│   ├── transcripts.db
│   ├── ocr_database.db
│   ├── communications.db
│   ├── prosecutorial_query_graph.db
│   └── full_text_corpus.db (downloading)
├── processed/           # OCR output, entities, embeddings
├── knowledge-graph/     # Custom KG exports
├── models/              # ML models (109GB)
├── downloads/           # Download staging area
├── logs/                # Download and processing logs
└── backups/             # PostgreSQL backups
```

**Note:** All scripts now use `scripts/epstein_config.py` for centralized path management. Legacy `/home/cbwinslow/workspace/epstein-data/` paths have been migrated to `/home/cbwinslow/workspace/epstein-data/`.

### Swarm Strategy
For parallel processing:
1. **Download phase**: 5 concurrent workers (one per dataset batch)
2. **OCR phase**: GPU-bound, 2 workers (one per K80)
3. **NER phase**: CPU-bound, 4 workers (spaCy small)
4. **Transcription**: GPU-bound, 1 worker (large-v3 model)
5. **KG building**: Single-threaded (SQLite writes)

### Monitoring
- Download progress: State files per dataset
- Processing progress: SQLite tracking table
- GPU utilization: nvidia-smi polling
- Disk usage: df monitoring with alerts at 90%

### Government Historical Ingestion Status

- **FEC historical coverage:** already present in PostgreSQL via `fec_individual_contributions` for cycles 2000-2026 (447,189,732 rows). Do not re-download unless validating source parity.
- **Congress historical pipeline:** use `scripts/ingestion/download_congress_historical.py`.
  - Correct endpoints are `/bill/{congress}` and `/member/congress/{congress}`.
  - Files are stored under `/home/cbwinslow/workspace/epstein-data/raw-files/congress_historical/congress_{N}/`.
  - Script is resumable and skips completed congress files.
- **GovInfo historical pipeline:** use `scripts/ingestion/download_govinfo_historical.py`.
  - Uses `offsetMark` pagination and larger page sizes per the official GovInfo API guidance.
  - Files are stored under `/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_historical/`.
- **GovInfo bulk-data pipeline:** use `scripts/ingestion/download_govinfo_bulk.py`.
  - Supports `FR` yearly ZIPs.
  - Supports `BILLSTATUS` ZIPs by congress and bill type.
  - Supports `BILLS` ZIPs by congress, session, and bill type.
  - Supports `BILLSUM` ZIPs by congress and bill type.
  - Saves JSON listing manifests next to every downloaded ZIP under `/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/`.
- **GovInfo Bill Status bulk import:** use `scripts/ingestion/import_govinfo_billstatus_bulk.py`.
  - Normalizes bill details into:
    - `congress_bill_titles`
    - `congress_bill_summaries`
    - `congress_bill_actions`
    - `congress_bill_cosponsors`
    - `congress_bill_related_bills`
    - `congress_bill_vote_references`
  - Enforces unique bill identity on `congress_bills (congress, bill_type, bill_number)`.
- **Government ingestion status (revalidated 2026-04-24 UTC):**
  - `congress_bills`: 368,651 (105th-119th)
  - `congress_members`: 10,413 (105th-119th)
  - `congress_house_votes`: 2,738 (117th-119th)
  - `congress_house_vote_details`: 2,738 (pending=0)
  - `congress_house_member_votes`: 1,185,626
  - `congress_senate_votes`: 3,132 (106th-119th, partial due upstream 403s)
  - `congress_senate_member_votes`: 313,176
  - `congress_bill_text_versions`: 130,361 (expanded with 119th BILLS bulk import)
  - `congress_bill_summaries`: 279,065
  - `congress_bill_actions`: 875,816
  - `congress_bill_cosponsors`: 2,064,763
  - `congress_bill_vote_references`: 11,546
  - `federal_register_entries`: 737,940 (2000-01-03 to 2024-12-31)
  - `court_opinions`: 31,544
  - `govinfo_packages`: 94,741
  - `govinfo_bulk_import_status`: 246 files complete
  - `fara_registrations`: 7,045
  - `fara_foreign_principals`: 17,358
  - `fara_short_forms`: 44,413
  - `fara_registrant_docs`: 124,224
  - `sec_insider_transactions`: 139 (recent feed import)
  - `whitehouse_visitors`: 2,544,984 total records (2009-2024)
    - Obama (2009-2017): 1,562,487
    - Biden (2021-2024): 937,744
    - Unique visitors: 1,038,898
  - Runtime note: latest high-concurrency GovInfo/Congress/FARA batch completed on 2026-04-24 UTC.
- **Residual government ingestion gaps to track:**
  - Senate vote-detail pipeline exists (`download_senate_vote_details.py`) but upstream `senate.gov` is intermittently returning HTTP 403 from this host; rerun/backfill required after access unblocks.
  - Pre-105th Congress expansion requires API-key path and alternate handling.
  - GitHub tracking: `#51` (closed), `#52` (GovInfo expansion), `#55` (SEC EDGAR), `#57` (FARA), plus sub-issues created for Senate backfill + FARA normalization.
- **Important schema note:** `congress_members` must be unique on `(bioguide_id, congress_number)`, not `bioguide_id` alone, or historical imports overwrite earlier congress membership.
- **GovInfo specialized tables:** `import_govinfo.py` fills summary-level rows for:
  - `federal_register_entries`
  - `court_opinions`
  - Verified current counts: `federal_register_entries=737,940`, `court_opinions=31,544`
- **Validated GovInfo bulk-data slice:** `BILLSTATUS-113-hjres.zip` imported cleanly with:
  - `131` bills
  - `350` titles
  - `178` summaries
  - `950` actions
  - `1,837` cosponsors
  - `217` related bill links
  - `49` vote references

### Error Handling
- HTML/corruption detection → quarantine + re-auth
- 404 errors → log + skip (DOJ removed files)
- GPU OOM → fallback to CPU
- Network errors → exponential backoff retry

---

## Tool Integration Map

### How the Upstream Repos Connect

```
┌─────────────────────────────────────────────────────────────────┐
│  DOWNLOAD LAYER                                                 │
│                                                                 │
│  epstein-ripper (auto_ep_rip.py)                                │
│  ├─ Playwright browser → handles DOJ age gate                  │
│  ├─ Scrapes paginated dataset pages                            │
│  ├─ Downloads PDFs via Playwright (bypasses JS requirements)   │
│  ├─ Validates PDF signature (rejects HTML poison)              │
│  └─ Output: /home/cbwinslow/workspace/epstein-data/raw-files/data{N}/      │
│        └── EFTA00000001.pdf, EFTA00000002.pdf, ...            │
│                                                                 │
│  EpsteinLibraryMediaScraper (scrape.js)                        │
│  ├─ Scrapes media file URLs (video, audio, images)             │
│  └─ Output: media file URLs for download                       │
└────────────────────────────┬────────────────────────────────────┘
                             │ PDF files on disk
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  PROCESSING LAYER (Epstein-Pipeline)                            │
│                                                                 │
│  epstein-pipeline ocr <dir> -o <out> --backend surya            │
│  ├─ PyMuPDF: instant text-layer extraction                     │
│  ├─ Surya: GPU-accelerated OCR for scanned pages               │
│  ├─ Docling: IBM fallback for complex layouts                  │
│  └─ Output: JSON files with per-page text + confidence         │
│                                                                 │
│  epstein-pipeline extract-entities <dir> -o <out>              │
│  ├─ spaCy NER (en_core_web_sm / en_core_web_trf)              │
│  ├─ GLiNER zero-shot entity extraction                         │
│  ├─ Regex patterns (dates, amounts, case numbers, Bates)       │
│  └─ Output: entities JSON with document cross-references       │
│                                                                 │
│  epstein-pipeline embed <dir> -o <out>                         │
│  ├─ nomic-embed-text-v2-moe (768-dim, Matryoshka 256-dim)     │
│  └─ Output: vector embeddings for semantic search              │
│                                                                 │
│  epstein-pipeline classify <dir>                               │
│  ├─ BART-large-mnli zero-shot classification                   │
│  └─ Output: document categories (court filings, depositions...) │
│                                                                 │
│  epstein-pipeline dedup <dir> --mode all                       │
│  ├─ SHA-256 hash (exact duplicates)                            │
│  ├─ MinHash/LSH (near-duplicates)                              │
│  └─ Semantic similarity (OCR variants)                         │
│                                                                 │
│  epstein-pipeline build-graph <dir> -o <out>                   │
│  ├─ Co-occurrence analysis                                     │
│  ├─ Relationship extraction                                    │
│  └─ Output: entities.json + relationships.json + GEXF          │
│                                                                 │
│  epstein-pipeline export sqlite <dir> -o <db>                  │
│  └─ Output: SQLite database with FTS5 search                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  PRE-BUILT DATA (Epstein-research-data)                         │
│                                                                 │
│  Already downloaded databases we can cross-reference:          │
│  ├─ full_text_corpus.db (7GB, 1.4M docs, FTS5 search)          │
│  ├─ redaction_analysis_v2.db (940MB, 2.59M redactions)         │
│  ├─ image_analysis.db (389MB, 38K image descriptions)          │
│  ├─ communications.db (30MB, 41K emails, communication pairs)  │
│  ├─ transcripts.db (4.8MB, 1.6K media transcriptions)          │
│  └─ knowledge_graph.db (892KB, 606 entities, 2.3K relations)   │
│                                                                 │
│  tools/ directory has Python scripts we can call:              │
│  ├─ build_knowledge_graph.py                                    │
│  ├─ build_person_registry.py                                    │
│  ├─ person_search.py (FTS5 cross-reference)                    │
│  ├─ redaction_detector_v2.py                                    │
│  └─ transcribe_media.py (faster-whisper)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  OUR EXTENSIONS (scripts/)                                      │
│                                                                 │
│  tracker.py — multi-process progress tracking                  │
│  file_watcher.py — filesystem-based progress updates           │
│  explore_kg.py — interactive knowledge graph queries           │
│  (future) — custom analysis, visualization, exports            │
└─────────────────────────────────────────────────────────────────┘
```

### Key Integration Points

| Step | Tool | Input | Output | Our Role |
|------|------|-------|--------|----------|
| 1. Download | `auto_ep_rip.py` | DOJ URLs | PDF files on disk | Call CLI, track progress |
| 2. OCR | `epstein-pipeline ocr` | PDF directory | OCR JSON files | Call CLI, configure workers |
| 3. Entities | `epstein-pipeline extract-entities` | OCR JSON | Entity JSON | Call CLI |
| 4. Embed | `epstein-pipeline embed` | OCR JSON | Vector embeddings | Call CLI |
| 5. Classify | `epstein-pipeline classify` | OCR JSON | Doc categories | Call CLI |
| 6. Dedup | `epstein-pipeline dedup` | All files | Duplicate groups | Call CLI |
| 7. KG Build | `epstein-pipeline build-graph` | Entities | KG JSON + GEXF | Call CLI, merge with pre-built |
| 8. Export | `epstein-pipeline export` | Processed data | SQLite/JSON/CSV | Call CLI |
| 9. Cross-ref | Our scripts | All databases | New insights | Our code |

### DO NOT MODIFY
- `Epstein-Pipeline/` — upstream, call via CLI or `import`
- `epstein-ripper/` — upstream, call via CLI
- `Epstein-research-data/` — upstream data, read only
- `EpsteinLibraryMediaScraper/` — upstream, call via Node

### Our code goes in
- `scripts/` — standalone tools
- `media_acquisition/` — Phase 22 media acquisition system
- `workers/` — background processing agents (future)
- Root level — config files, docs

## Memory Management

### Centralized Skills System
All memory operations use the centralized AI skills system located at `/home/cbwinslow/dotfiles/ai/skills/`.

**DO NOT** implement memory management logic directly in this project. Use the skills instead.

### Available Memory Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| `letta_server` | `~/dotfiles/ai/skills/letta_server/` | Core memory operations, advanced search |
| `cli_operations` | `~/dotfiles/ai/skills/cli_operations/` | CLI wrappers for Letta commands |
| `conversation_logging` | `~/dotfiles/ai/skills/conversation_logging/` | Conversation logging with decision extraction |
| `memory_sync` | `~/dotfiles/ai/skills/memory_sync/` | PostgreSQL to Letta server synchronization |
| `memory` | `~/dotfiles/ai/skills/memory/` | General memory management (Letta, PostgreSQL, SQLite) |

### Using Memory Skills

```python
# Import from skills, not from local scripts
from letta_server import store_conversation, advanced_memory_search
from cli_operations import run_letta_command, search_postgres_memories
from conversation_logging import log_conversation, extract_decisions
from memory_sync import sync_postgres_to_letta, backup_agent_data

# Store a conversation
log_conversation(
    messages=conversation_messages,
    agent_name="epstein_processor",
    tags=["processing", "decision"]
)

# Search memories
results = advanced_memory_search(
    query="entity extraction",
    search_type="semantic",
    limit=10
)

# Sync memories
sync_postgres_to_letta(
    agent_id="agent-xxx",
    memory_types=["conversation", "decision"]
)
```

### Memory Scripts (Legacy)
The following scripts in `scripts/` are **legacy** and should not be used for new development. They are being phased out in favor of the skills system:

- `letta_memory.py` — Use `letta_server` skill instead
- `memory_search.py` — Use `cli_operations` skill instead
- `search_letta_memories.py` — Use `cli_operations.search_postgres_memories` instead
- `sync_to_letta_server.py` — Use `memory_sync.sync_postgres_to_letta` instead
- `save_conversation_to_letta.py` — Use `conversation_logging.log_conversation` instead

### Agent Configuration
All agents use the centralized configuration at `/home/cbwinslow/dotfiles/ai/agents/opencode/config.yaml`. This includes:
- Memory backend configuration
- Skill paths
- Letta server settings
- Conversation logging preferences

---

## Data Storage Strategy

### What Goes Where

| Data Type | Storage | Format | Tool |
|-----------|---------|--------|------|
| Raw PDFs | Filesystem | PDF files | epstein-ripper |
| OCR text | SQLite + JSON | Per-page JSON + DB rows | epstein-pipeline ocr |
| Named entities | SQLite + JSON | Entity records with doc refs | epstein-pipeline extract-entities |
| Vector embeddings | SQLite (pgvector later) | 768-dim float arrays | epstein-pipeline embed |
| Knowledge graph | SQLite + GEXF + JSON | Entities + relationships | epstein-pipeline build-graph |
| Full-text search | SQLite FTS5 | Tokenized inverted index | Pre-built + our additions |
| Progress tracking | JSON | Shared state file | scripts/tracker.py |
| Transcriptions | SQLite | Per-file text + segments | Pre-built transcripts.db |
| Image descriptions | SQLite | AI-generated text | Pre-built image_analysis.db |
| News articles | PostgreSQL | media_news_articles table | NewsDiscoveryAgent + NewsCollector |
| Videos | PostgreSQL | media_videos table | VideoDiscoveryAgent + VideoTranscriber |
| Court docs | PostgreSQL | media_documents table | DocumentDiscoveryAgent |

### Vector Database Options (Future)

1. **SQLite + sqlite-vss** — simple, no infra, good for <10M vectors
2. **pgvector on Neon** — pipeline already supports this, cloud-hosted
3. **Qdrant/Weaviate** — if we need scale beyond 10M vectors
4. **FAISS flat index** — for local GPU-accelerated similarity search

Current plan: Start with SQLite (already have full_text_corpus.db with FTS5), add pgvector when we generate new embeddings.

### Knowledge Graph Merging Strategy

When we process new documents, we'll generate new entities and relationships.
These get merged into the existing knowledge graph via:

1. **Entity resolution** — fuzzy name matching (rapidfuzz) + alias matching
2. **Relationship dedup** — same source+target+type → increase weight
3. **New entity addition** — entities from new docs not in existing KG
4. **Cross-reference** — link new entities to EFTA numbers in full_text_corpus

---

## Anti-Drift Protocol

### Before Starting Any Task
1. **Read CONTEXT.md** — understand current state, paths, status
2. **Read TASKS.md** — check if task is already done or in progress
3. **Search existing code** — don't duplicate scripts or logic
4. **Check upstream repos** — don't reinvent what Epstein-Pipeline already does

### During Work
1. **Update TASKS.md** — set status to `in_progress`, log decisions
2. **Log to CONTEXT.md** — note any new paths, configs, or state changes
3. **Use same patterns** — match existing code style, imports, error handling
4. **Ask if uncertain** — don't assume, don't skip, don't guess

### After Work
1. **Update TASKS.md** — set status to `done` with solution/notes
2. **Update CONTEXT.md** — reflect new state
3. **Commit with descriptive message** — what changed and why
4. **Push to GitHub** — keep remote in sync

### Memory Preservation
| Mechanism | Purpose |
|-----------|---------|
| `CONTEXT.md` | Living memory — included in every prompt |
| `TASKS.md` | All tasks, status, solutions |
| `.python-version` | Pin Python version |
| `pyproject.toml` | Pin dependency versions |
| `.env.example` | Document required secrets |
| `setup.sh` | Reproducible environment bootstrap |

### Context Refresh Protocol
- **Re-read CONTEXT.md** at the start of every new session
- **Re-read TASKS.md** before starting any work
- **Update both** after any significant change
- **If confused**: re-read all .md files before proceeding

---

## Agent Boundaries

| Agent | Can Do | Cannot Do |
|-------|--------|-----------|
| Download | Run download scripts, monitor progress | Modify processing code |
| OCR | Run pipeline CLI on PDFs | Modify pipeline source |
| NER | Call spaCy/GLiNER | Retrain models |
| Face | Run InsightFace on images | Modify model weights |
| KG | Query/update SQLite graph | Delete upstream data |
| Eval | Run metrics.py | Modify evaluation formulas |

### What Counts as "Upstream"
- `Epstein-Pipeline/` — processing pipeline
- `epstein-ripper/` — DOJ downloader
- `Epstein-research-data/` — pre-built databases
- `EpsteinLibraryMediaScraper/` — media scraper

### What Counts as "Ours"
- `scripts/` — our download, tracking, analysis tools
- `media_acquisition/` — Phase 22 media acquisition system
- `docs/` — our documentation
- Root `.md` files — our project docs
- `pyproject.toml` — our dependency config
- `setup.sh` — our bootstrap script

---

## Validation Procedures

### After Every Code Change
1. Run the code with real inputs
2. Verify output structure and content
3. Check for errors/exceptions
4. Confirm side effects (files written, DB rows created)
5. Document pass/fail in the validation report

### Validation Hierarchy
| Priority | Method | When to Use |
|----------|--------|-------------|
| 1 | Execute and verify | Scripts, CLI tools, one-off commands |
| 2 | Smoke test | New modules, imports, initialization |
| 3 | Data verification | Database queries, file integrity checks |
| 4 | Integration test | Multi-step workflows, tool chains |
| 5 | Unit test | Reusable library functions we write |

### What NOT to Validate
- Upstream repo internals (their CI handles that)
- Third-party package behavior (assume pip install succeeded)
- Network availability (test with retries, don't block on connectivity)

### Validation Report Format
```markdown
## Validation Report — [date]
### Components Tested
- [x] component: method -> result
- [ ] component: method -> FAIL (reason)

### Summary
- X/Y passed
- Issues found: ...
- Fixes applied: ...
```

---

## Mandatory Memory Protocol

**EVERY agent MUST execute these steps automatically. No exceptions.**

### On Session Start (Before Any Work)
```python
# 1. Recall relevant memories
from autonomous_memory import recall
memories = recall("task description keywords", limit=5)
# Inject results into agent context before proceeding
```

### During Work (After Every Decision/Error/Discovery)
```python
from autonomous_memory import save_decision, save_error, save_discovery

# On decision
save_decision("Title", "Rationale and what was chosen", agent="agent_name")

# On error
save_error("Error message", "Context", "How it was fixed", agent="agent_name")

# On discovery
save_discovery("What was found", "Details", agent="agent_name")
```

### On Session End (After All Work Complete)
```python
from autonomous_memory import log_session

# Save full conversation
log_session(conversation_messages, "agent_name", "project_name")
```

### GitHub Issue Protocol
When closing issues, ALWAYS add a comment with:
1. What was done (specific actions)
2. Numbers/metrics (before/after)
3. Tables affected
4. Any remaining work

Example:
```
gh issue comment 37 --body "## Completed\n\n**Details:**\n- Removed 187K duplicates\n- Final count: 1.6M rows\n- Table: jmail_emails"
gh issue close 37 --comment "Completed - see details above."
```

### Memory Location
- Database: `letta` (PostgreSQL localhost:5432)
- Table: `letta_memories`
- Skill: `~/dotfiles/ai/skills/autonomous_memory/`
- Import: `from autonomous_memory import recall, store, log_session`

---

## Backup & Recovery

### Backup Location
- **Path**: `/home/cbwinslow/workspace/epstein-data/backups/`
- **Format**: PostgreSQL custom format (`.dump`), compressed level 9
- **Naming**: `epstein_YYYYMMDD_HHMMSS.dump`

### Current Backups
| File | Date | Size |
|------|------|------|
| `epstein_20260322_203141.dump` | 2026-03-22 | ~3GB |
| Latest auto-backup | Daily 2am cron | varies |

### Backup Command
```bash
# Manual backup
PGPASSWORD=123qweasd pg_dump -U cbwinslow -h localhost epstein \
  --format=custom --compress=9 \
  --file="/home/cbwinslow/workspace/epstein-data/backups/epstein_$(date +%Y%m%d_%H%M%S).dump"

# Restore from backup
pg_restore -U cbwinslow -h localhost -d epstein --clean \
  /home/cbwinslow/workspace/epstein-data/backups/epstein_YYYYMMDD_HHMMSS.dump
```

### Automated Backups
- **Cron**: Daily at 2am (system cron, see `crontab -l`)
- **Retention**: 7 days (old backups auto-cleaned)
- **Log**: `/home/cbwinslow/workspace/epstein/logs/backup.log`

### What Gets Backed Up
All 72 tables in the `epstein` database including:
- Core DOJ data (documents, pages, redactions, embeddings)
- Kabasshouse imports (entities, chunks, financial, embeddings)
- Epstein Exposed data (persons, flights, emails, organizations)
- FBI Vault OCR pages
- FEC donations (447M individual contributions)
- House Financial Disclosures (37,281 records, 2008-2024)
- Senate Financial Disclosures (not accessible - DNS error)
- Senate LDA (lobbying registrations and reports)
- DOJ alteration analysis
- House Oversight emails
- All indexes, constraints, and extensions (pgvector, pg_trgm)

### What Does NOT Get Backed Up
- Letta memories (stored in separate `letta` database)
- Downloaded files in `/home/cbwinslow/workspace/epstein-data/downloads/`
- Log files in `logs/`

### Recovery Procedure
1. Verify backup integrity: `pg_restore -l /path/to/backup.dump`
2. Stop any running import processes
3. Restore: `pg_restore -d epstein --clean /path/to/backup.dump`
4. Rebuild FTS indexes if needed: `UPDATE pages SET search_vector = to_tsvector('english', COALESCE(text_content, ''))`
5. Verify row counts against backup metadata

---

## News Ingestion Pipeline (3-Phase Workflow)

Professional workflow for collecting news articles from RSS feeds and extracting full content.

### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Phase 1        │────▶│  Phase 2         │────▶│  Phase 3        │
│  Discovery      │     │  Storage         │     │  Extraction     │
│  (RSS/News)     │     │  (Queue)         │     │  (Trafilatura)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
       ↓                                                    ↓
  article_discovery_queue                           media_news_articles
```

### Phase 1: URL Discovery Agent

**Script:** `scripts/ingestion/phase1_discovery.py`

**Purpose:** Search RSS feeds for article URLs matching keywords

**Input:**
- Keywords: `['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell']`
- Date range: `2024-01-01` to `2025-12-31`
- Sources: RSS feeds from major news outlets

**Output:**
- URLs saved to `article_discovery_queue` table
- Status: `pending`

**Usage:**
```bash
python scripts/ingestion/phase1_discovery.py \
  --keywords "Jeffrey Epstein" "Epstein case" \
  --start-date 2024-01-01 \
  --end-date 2025-12-31
```

**Sources Checked:**
- BBC News, CNN, NPR, Reuters
- HuffPost, NY Times, Washington Post
- The Guardian, Fortune, Vice

**Key Features:**
- Keyword matching in title + summary
- Date range filtering
- Duplicate detection (URL uniqueness)
- Source tracking

### Phase 2: URL Queue Storage

**Table:** `article_discovery_queue`

**Purpose:** Hold discovered URLs until processed

**Schema:**
```sql
CREATE TABLE article_discovery_queue (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    source TEXT,
    source_feed TEXT,
    published_date DATE,
    keywords_matched TEXT[],
    discovery_method VARCHAR(50),
    discovered_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending',  -- pending, completed, failed, duplicate
    processed_at TIMESTAMP
);
```

**States:**
- `pending`: Waiting for extraction
- `completed`: Successfully extracted
- `failed`: Extraction error
- `duplicate`: URL already exists

### Phase 3: Content Extraction Agent

**Script:** `scripts/ingestion/phase3_extraction.py`

**Purpose:** Fetch full article content from URLs using Trafilatura

**Tool:** [Trafilatura](https://trafilatura.readthedocs.io/)
- Extracts clean article text from HTML
- Removes ads, navigation, sidebars
- Returns: title, author, date, text, categories, tags, images

**Input:**
- URLs from `article_discovery_queue` (status=`pending`)

**Output:**
- Full articles saved to `media_news_articles` table
- Queue status updated
- Extraction metadata logged

**Usage:**
```bash
# Test mode (recommended first)
python scripts/ingestion/phase3_extraction.py --test --limit 10

# Bulk production run
python scripts/ingestion/phase3_extraction.py \
  --bulk \
  --batch-size 100 \
  --rate-limit 2.0
```

**Extraction Fields Stored:**
- `content`: Full article text
- `title`: Article headline
- `author`: Author(s)
- `publish_date`: Publication date
- `word_count`: Calculated from content
- `description`: Meta description
- `extraction_metadata`: JSON with categories, tags, hostname, fingerprint, image_url

### Pipeline Orchestrator

**Script:** `scripts/ingestion/run_pipeline.py`

**Purpose:** Run complete workflow in one command

**Usage:**
```bash
# Test run (small sample, recommended first)
python scripts/ingestion/run_pipeline.py --mode test

# Production run
python scripts/ingestion/run_pipeline.py --mode production \
  --start-date 2024-01-01 \
  --end-date 2025-12-31

# Run specific phase
python scripts/ingestion/run_pipeline.py --phase discovery
python scripts/ingestion/run_pipeline.py --phase extraction --test
```

### Prerequisites

**Required Packages:**
```bash
pip install trafilatura psycopg2-binary feedparser aiohttp
```

**Trafilatura Features:**
- Fast extraction (faster than newspaper3k)
- Handles JavaScript-heavy sites
- Built-in date extraction
- Language detection
- Duplicate detection via fingerprinting
- Respects robots.txt (with proper delays)

### Data Quality Validation

**Script:** `scripts/processing/review_dataset.py`

**Checks:**
- PII detection (emails, phone numbers, SSNs)
- Content quality (word count distribution)
- Duplicate detection
- Source credibility

**Usage:**
```bash
python scripts/processing/review_dataset.py
```

### Export to Hugging Face

**Script:** `scripts/processing/prepare_huggingface_dataset.py`

**Creates:**
- Structured JSON dataset
- Train/validation/test splits (80/10/10)
- Metadata and statistics

**Usage:**
```bash
python scripts/processing/prepare_huggingface_dataset.py
# Output: /tmp/epstein_news_dataset_YYYYMMDD.json
```

### Typical Workflow for AI Agents

1. **Initial Setup**
   ```bash
   # Verify prerequisites
   python scripts/ingestion/run_pipeline.py --mode test --limit 5
   ```

2. **Discovery Phase**
   ```bash
   python scripts/ingestion/phase1_discovery.py \
     --keywords "Jeffrey Epstein" \
     --start-date 2024-01-01 \
     --end-date 2025-12-31
   ```

3. **Review Discovered URLs**
   ```bash
   psql -d epstein -c "SELECT COUNT(*), source FROM article_discovery_queue WHERE status='pending' GROUP BY source"
   ```

4. **Extraction Phase (Test)**
   ```bash
   python scripts/ingestion/phase3_extraction.py --test --limit 10
   ```

5. **Validate Test Results**
   ```bash
   python scripts/processing/review_dataset.py
   ```

6. **Full Extraction (if test passes)**
   ```bash
   python scripts/ingestion/phase3_extraction.py --bulk --batch-size 100 --rate-limit 2.0
   ```

7. **Final Dataset Review**
   ```bash
   python scripts/processing/review_dataset.py
   python scripts/processing/prepare_huggingface_dataset.py
   ```

### Rate Limiting Guidelines

**Be Respectful:**
- Default: 2 seconds between requests
- RSS feeds: 1 second between feeds
- Batch processing: 100 URLs per batch
- Respect robots.txt

**Why:** Prevents IP bans and maintains good relationships with news sources.

### Error Handling

**Common Issues:**
- **Paywalls**: Marked as failed, logged for manual review
- **404 errors**: URL removed from queue
- **Timeout**: Retried once, then marked failed
- **Duplicate content**: Fingerprints compared, duplicates flagged

**Recovery:**
```bash
# Reset failed URLs for retry
psql -d epstein -c "UPDATE article_discovery_queue SET status='pending' WHERE status='failed'"
```

### Storage Estimates

| Phase | Records | Storage |
|-------|---------|---------|
| Discovery | ~10,000 URLs | ~2 MB |
| Extraction | ~8,000 articles | ~500 MB |
| With Metadata | ~8,000 articles | ~600 MB |

**Note:** Actual size depends on article length and metadata richness.

### Security & Ethics

- **PII Detection**: Automated scan before HF upload
- **Content Warnings**: Dataset covers sensitive criminal case
- **Terms Compliance**: Respect news source TOS (rate limits)
- **Academic Use**: Intended for research/analysis only

---

## News Ingestion Framework (Mega-Parallel)

Professional framework that recreates the 9,700 article ingestion. Built for large-scale historical news collection.

### Quick Start - Recreate Our Results

```bash
# Test run (2024 only, ~100 articles, ~30 min)
python scripts/ingestion/collect_epstein_articles.py --test

# Full collection (2000-2025, ~9,700 articles, ~24 hours)
python scripts/ingestion/collect_epstein_articles.py --full

# Check stats
python scripts/ingestion/collect_epstein_articles.py --stats
```

### Framework Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MegaParallelOrchestrator                    │
│                        (30 concurrent stages)                  │
└─────────────────────────┬─────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Google News  │ │   RSS Feeds  │ │    GDELT     │
    │   Scraper    │ │  Aggregator  │ │    (future)  │
    └──────────────┘ └──────────────┘ └──────────────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                ┌──────────────────┐
                │  CollectionQueue │
                │   (PostgreSQL)     │
                └──────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │  NewsCollector   │
                │ (Trafilatura)    │
                └──────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ media_news_articles│
                └──────────────────┘
```

### Core Components

#### 1. MegaParallelOrchestrator

**File:** `scripts/ingestion/news_ingestion_framework.py`

**Purpose:** Coordinates massive parallel ingestion using staged time chunks.

**How it works:**
1. Splits date range into 4-month chunks (stages)
2. Runs up to 30 stages concurrently
3. Each stage: Discover → Queue → Collect
4. Uses semaphores to control resource usage

**Config:**
```python
MegaParallelConfig(
    max_concurrent_stages=30,        # 30 stages at once
    stage_batch_size=timedelta(days=120),  # 4 months per stage
    collection_concurrency=20        # 20 collectors per stage
)
```

#### 2. Discovery Agents

**GoogleNewsDiscoveryAgent:**
- Scrapes Google News search results
- Uses date range filtering (`tbs=cdr`)
- Extracts URLs, titles from search results
- Rate limit: 0.3s between requests

**RSSDiscoveryAgent:**
- Parses 8 major news RSS feeds
- Keyword matching in title/summary
- Date range filtering
- Rate limit: 1s between feeds

**Usage:**
```python
from scripts.ingestion.news_ingestion_framework import (
    MegaParallelOrchestrator,
    DiscoveryConfig, CollectionConfig
)

# Configure discovery
discovery_config = DiscoveryConfig(
    keywords=['Jeffrey Epstein', 'Epstein'],
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2025, 12, 31),
    sources=['google_news', 'rss'],
    max_results_per_source=1000,
    rate_limit_seconds=0.3
)
```

#### 3. CollectionQueue

**Table:** `collection_queue`

**Purpose:** PostgreSQL-backed queue for discovered URLs.

**Schema:**
```sql
CREATE TABLE collection_queue (
    id SERIAL PRIMARY KEY,
    run_id UUID NOT NULL,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    source TEXT,
    keywords_matched TEXT[],
    discovery_method VARCHAR(50),
    discovered_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending',
    collected_at TIMESTAMP,
    content_length INTEGER,
    error_message TEXT
);
```

**States:** `pending` → `completed` / `failed` / `duplicate`

#### 4. NewsCollector

**Purpose:** Fetch full article content using Trafilatura.

**Extracts:**
- Title, author, publish date
- Full article text (cleaned)
- Word count
- Categories, tags
- Hostname, language
- Content fingerprint

**Rate limiting:** 0.3s between requests (respectful)

### Recreating the Exact 9,700 Article Ingestion

**Script:** `scripts/ingestion/collect_epstein_articles.py`

**Configuration used:**
```python
# Our successful run config
results = run_epstein_ingestion(
    start_year=2000,
    end_year=2025,
    keywords=[
        'Jeffrey Epstein',
        'Epstein',
        'Ghislaine Maxwell',
        'Virginia Giuffre'
    ],
    max_stages=30
)

# Expected results:
# - Discovered: ~10,000 URLs
# - Collected: ~9,700 articles
# - Time: ~24 hours
# - Storage: ~600 MB
```

**Breakdown by year (from our run):**
| Year | Articles | Notes |
|------|----------|-------|
| 2000-2010 | ~500 | Early coverage |
| 2011-2018 | ~1,500 | Pre-arrest coverage |
| 2019 | ~3,000 | Arrest, death peak |
| 2020-2022 | ~2,500 | Maxwell trial, fallout |
| 2023-2025 | ~2,200 | Document releases |

### Advanced Usage

#### Custom Keywords

```python
from scripts.ingestion.news_ingestion_framework import run_epstein_ingestion

# Custom topic
results = run_epstein_ingestion(
    start_year=2020,
    end_year=2024,
    keywords=['Donald Trump', 'election', 'campaign'],
    max_stages=20
)
```

#### Direct Framework Access

```python
from scripts.ingestion.news_ingestion_framework import (
    MegaParallelOrchestrator,
    MegaParallelConfig,
    DiscoveryConfig,
    CollectionConfig
)
from datetime import datetime, timedelta
import asyncio

# Custom configuration
mega_config = MegaParallelConfig(
    max_concurrent_stages=50,  # More aggressive
    stage_batch_size=timedelta(days=60),  # 2-month chunks
    collection_concurrency=30
)

discovery_config = DiscoveryConfig(
    keywords=['Climate Change', 'Global Warming'],
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 12, 31),
    sources=['google_news', 'rss'],
    rate_limit_seconds=0.5
)

collection_config = CollectionConfig(
    batch_size=100,
    max_concurrent_collectors=30,
    rate_limit_seconds=0.5
)

# Run
orchestrator = MegaParallelOrchestrator(mega_config)
results = asyncio.run(orchestrator.run(
    discovery_config.start_date,
    discovery_config.end_date,
    discovery_config,
    collection_config
))
```

### Performance Tuning

**Memory Usage:**
- 30 stages × 200 articles = 6,000 articles in memory
- ~1.2 GB RAM recommended minimum
- 16+ GB RAM for 75-stage runs

**Rate Limiting Guidelines:**
| Resource | Limit | Reason |
|----------|-------|--------|
| Google News | 0.3s | Avoid IP ban |
| RSS feeds | 1.0s | Respect servers |
| Article fetch | 0.3s | Be nice to publishers |
| Concurrent | 30 stages | RAM limits |

**Throughput:**
- Our run: ~25,000 articles/hour (discovery + collection)
- Google News only: ~15,000 articles/hour
- RSS only: ~5,000 articles/hour (limited sources)

### Error Handling & Recovery

**Common Failures:**
1. **Paywalls** (20-30%) - Marked as failed, logged
2. **404 errors** (5%) - URL removed
3. **Timeout** (10%) - Retried once
4. **Extraction fail** (5%) - No content found

**Recovery:**
```bash
# Reset failed articles for retry
psql -d epstein -c "UPDATE collection_queue SET status='pending' WHERE status='failed'"

# Re-run just extraction phase
python -c "
from scripts.ingestion.news_ingestion_framework import *
# ... re-run collection on pending queue
"
```

### Database Schema

**After ingestion, query results:**
```sql
-- Total collected
SELECT COUNT(*) FROM media_news_articles
WHERE discovery_source = 'mega_parallel_ingestion';

-- By year
SELECT EXTRACT(YEAR FROM publish_date) as year, COUNT(*)
FROM media_news_articles
WHERE discovery_source = 'mega_parallel_ingestion'
GROUP BY year ORDER BY year;

-- Word count distribution
SELECT
    CASE
        WHEN word_count < 100 THEN 'Short (<100)'
        WHEN word_count < 500 THEN 'Medium (100-500)'
        ELSE 'Long (500+)'
    END as size,
    COUNT(*)
FROM media_news_articles
GROUP BY 1;

-- Top sources
SELECT source_domain, COUNT(*)
FROM media_news_articles
GROUP BY source_domain
ORDER BY COUNT(*) DESC
LIMIT 10;
```

### Prerequisites

**Required packages:**
```bash
pip install trafilatura psycopg2-binary aiohttp feedparser beautifulsoup4
```

**Database:**
```bash
# Ensure media_news_articles table exists
psql -d epstein -f scripts/database/create_media_schema.sql
```

### AI Agent Instructions

**To recreate the 9,700 article ingestion:**

1. **Verify prerequisites:**
   ```bash
   python scripts/ingestion/collect_epstein_articles.py --test
   ```

2. **Check current stats:**
   ```bash
   python scripts/ingestion/collect_epstein_articles.py --stats
   ```

3. **Run full collection:**
   ```bash
   python scripts/ingestion/collect_epstein_articles.py --full
   ```

4. **Monitor progress:**
   ```bash
   # In another terminal
   watch -n 30 'psql -d epstein -c "SELECT COUNT(*) FROM media_news_articles"'
   ```

5. **Review results:**
   ```bash
   python scripts/processing/review_dataset.py
   ```

---

## Article Enrichment with Trafilatura (Active Workflow)

**Status:** Production Ready

**Purpose:** Add full article content + rich metadata to existing URL collection using Trafilatura.

### Quick Start

```bash
# Enrich articles without content (processes 50 at a time)
python scripts/ingestion/enrich_with_trafilatura.py

# Check progress
psql -d epstein -c "SELECT COUNT(*) as with_content FROM media_news_articles WHERE word_count > 100"
```

### What It Does

1. **Fetches existing URLs** from `media_news_articles` with missing/short content
2. **Downloads article HTML** using Trafilatura's fetcher
3. **Extracts rich metadata:**
   - Full article text (cleaned, no ads)
   - Title, author, publish date
   - Categories, tags, keywords
   - Language detection
   - Content fingerprint (for deduplication)
   - Hostname, description
4. **Stores everything** back to database

### Data Captured

**Content Fields:**
- `content` - Full article text
- `title` - Article headline
- `authors` - List of authors
- `publish_date` - Publication date
- `word_count` - Calculated word count
- `summary` - Meta description or first paragraph
- `language` - Detected language (en, es, etc.)

**Metadata Fields (stored in `all_topics` JSON):**
- `categories` - Article categories
- `tags` - Extracted tags
- `fingerprint` - Content hash for deduplication
- `hostname` - Source domain
- `description` - Meta description

### Quality Control

**Automatic Filtering:**
- Skips Google News redirect URLs
- Skips articles < 100 words (likely ads/errors)
- Handles paywalls gracefully (marked as failed)
- Retries on timeouts

**Manual Review:**
```bash
# Check recently enriched articles
psql -d epstein -c "SELECT title, word_count, source_domain FROM media_news_articles WHERE collected_at > NOW() - INTERVAL '1 hour' AND word_count > 0 ORDER BY word_count DESC"

# Find junk articles to remove
psql -d epstein -c "SELECT id, title, content FROM media_news_articles WHERE content LIKE '%cookie%' OR content LIKE '%GDPR%' OR content LIKE '%browser check%' LIMIT 10"
```

### Troubleshooting

**Issue: No content extracted**
- Likely paywall or Cloudflare protection
- Article marked as failed, will retry on next run

**Issue: Wrong person (e.g., "Michal Epstein" instead of Jeffrey)**
- Check `title` and `content` for false positives
- Delete with: `DELETE FROM media_news_articles WHERE id = XXX`

**Issue: Duplicate articles**
- Use fingerprint in `all_topics` to identify duplicates
- Trafilatura generates content hash automatically

### Full Enrichment Run

```bash
# Run multiple times to process all articles
for i in {1..200}; do
    echo "Batch $i"
    python scripts/ingestion/enrich_with_trafilatura.py
    sleep 5
done
```

### Verification

```bash
# Stats
echo "With content:" && psql -d epstein -c "SELECT COUNT(*) FROM media_news_articles WHERE word_count > 100"
echo "Without content:" && psql -d epstein -c "SELECT COUNT(*) FROM media_news_articles WHERE word_count IS NULL OR word_count < 100"
echo "Total:" && psql -d epstein -c "SELECT COUNT(*) FROM media_news_articles"

# Average word count
psql -d epstein -c "SELECT AVG(word_count), MAX(word_count), MIN(word_count) FROM media_news_articles WHERE word_count > 0"

# By source
psql -d epstein -c "SELECT source_domain, COUNT(*), AVG(word_count) FROM media_news_articles WHERE word_count > 0 GROUP BY source_domain ORDER BY COUNT(*) DESC LIMIT 10"
```

---
## 📚 Letta Log Hook (automatic)

All Hermes agents (including Kilocode) now run with the following hooks:

```json
{
  "pre_prompt_hook":  "~/dotfiles/ai/shared/skills/letta_log/scripts/hermes_hook.py prompt",
  "post_response_hook": "~/dotfiles/ai/shared/skills/letta_log/scripts/hermes_hook.py response",
  "error_hook": "~/dotfiles/ai/shared/skills/letta_log/scripts/hermes_hook.py error"
}
```

**What this does**

* **Prompt** → Logged as an archival memory entry with tags `hermes,prompt,YYYY‑MM‑DD`.
* **Response** → Logged with tags `hermes,response,YYYY‑MM‑DD`.
* **Error** → Logged with tags `hermes,error,YYYY‑MM‑DD`.

All entries are attached to the persistent **`agent‑log`** conversation and include:
- LLM and model name (`HERMIT_LLM`, `HERMIT_MODEL`),
- environment metadata (hostname, OS, user),
- optional `turn_id` for linking prompt ↔ response (enable via `HERMIT_LINK_TURN=1`),
- rate‑limiting to avoid duplicate records.

> **Tip:** Enable a dry‑run globally during development:
> ```bash
> export HERMIT_HOOK_DRY_RUN=1
> ```
> The hooks will then just print the JSON payload without inserting anything into Letta.

The hooks are active for **every** Hermes turn, ensuring a complete, searchable audit trail in the Letta memory system.
