# Epstein Files Analysis - Agent Configuration

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
/mnt/data/epstein-project/
├── raw-files/           # Downloaded PDFs and media
│   ├── data1/           # Dataset 1
│   ├── data2/           # Dataset 2
│   └── ...
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
└── logs/               # Download and processing logs
```

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
│  └─ Output: /mnt/data/epstein-project/raw-files/data{N}/      │
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
- `workers/` — background processing agents (future)
- Root level — config files, docs

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
