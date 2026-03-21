# Epstein Files Analysis Project — CONTEXT (Living Document)

> Include this file in every prompt. Update after every session.
> Last updated: 2026-03-20

---

## Infrastructure

| Component | Details |
|-----------|---------|
| Server | Ubuntu, RAID5 md0 (5× drives, 4.4TB), LVM |
| Storage mount | `/mnt/data/epstein-project/` on `vg-data/lv-nextcloud` (2.5TB, 2.3TB free) |
| GPUs | 2× Tesla K80 (12GB, CUDA 11.4) + 1× Tesla K40m (11GB) — Kepler |
| Python | 3.12.3 at `/home/cbwinslow/workspace/epstein/venv/bin/python3` |
| Node | v24.14.0 |
| Workspace | `/home/cbwinslow/workspace/epstein/` |

---

## Project Directory Layout

```
/home/cbwinslow/workspace/epstein/
├── CONTEXT.md                  ← THIS FILE (living memory)
├── AGENTS.md                   ← Agent architecture, workflow pipeline
├── RULES.md                    ← Rules including codebase separation + validation loop
├── PROJECT.md                  ← Quick-start guide
├── VALIDATION_REPORT.md        ← Latest validation results (30/30 passed)
├── venv/                       ← Python venv (epstein-pipeline + deps installed)
├── scripts/                    ← OUR CODE (tracker.py, file_watcher.py, explore_kg.py)
├── Epstein-Pipeline/           ← UPSTREAM: processing pipeline (DO NOT MODIFY)
├── Epstein-research-data/      ← UPSTREAM: pre-built databases + tools (DO NOT MODIFY)
├── epstein-ripper/             ← UPSTREAM: DOJ downloader (DO NOT MODIFY)
├── EpsteinLibraryMediaScraper/ ← UPSTREAM: media URL scraper (DO NOT MODIFY)
└── ...                         ← Any new workers/tools WE write go in scripts/ or workers/

/mnt/data/epstein-project/
├── raw-files/                  ← Downloaded PDFs (data1/, data2/, ...)
├── databases/                  ← Pre-built SQLite databases (8.4GB)
├── processed/                  ← OCR output, entities, embeddings (empty, ready)
├── knowledge-graph/            ← Custom KG exports (empty, ready)
└── logs/                       ← progress.json + processing logs
```

---

## Installed Packages (in venv)

- `epstein-pipeline` (editable install from local clone)
- `spacy` + `en_core_web_sm` (NER ready, `en_core_web_trf` for GPU later)
- `pymupdf` (PDF text extraction)
- `aiohttp` (async HTTP)
- `playwright` + Chromium headless (DOJ age-gate bypass)
- Core: click, rich, pydantic, httpx, datasketch, rapidfuzz

Not yet installed (will need later):
- `surya-ocr` (GPU OCR, needs torch)
- `faster-whisper` (GPU transcription)
- `sentence-transformers` + `torch` (embeddings)
- `psycopg` + `pgvector` (Neon export)

---

## Databases Downloaded (8.4GB total)

| Database | Size | Rows | Key Content |
|----------|------|------|-------------|
| full_text_corpus.db | 7.0GB | 1,397,821 docs, 2,892,730 pages | Full OCR text, FTS5 search |
| redaction_analysis_v2.db | 940MB | 2.59M redactions, 849K summaries | Redaction detection, text recovery |
| image_analysis.db | 389MB | 38,955 images | AI descriptions of extracted images |
| ocr_database.db | 68MB | 38,955 OCR results | Per-page extraction data |
| communications.db | 30MB | 41,924 emails, 90K participants | Email threads, communication pairs |
| transcripts.db | 4.8MB | 1,628 media files | Audio/video transcriptions |
| prosecutorial_query_graph.db | 2.5MB | 257 subpoenas | Legal document tracking |
| knowledge_graph.db | 892KB | 606 entities, 2,302 relationships | Entity relationship graph |

---

## Knowledge Graph Summary

**Entity types:** person (571), shell_company (12), organization (9), property (7), aircraft (4), location (3)

**Relationship types:** traveled_with (1,449), associated_with (589), communicated_with (215), owned_by (23), victim_of (13), employed_by (7)

**Top entities by connections:**
1. Jeffrey Epstein: 493 connections, weight 4,789
2. Ghislaine Maxwell: 283 connections, weight 1,479
3. Emmy Tayler: 130 connections
4. Sarah Kellen: 127 connections
5. Larry Visoski (pilot): 86 connections

**Top email pairs:**
- Boris Nikolic ↔ Epstein: 680 emails (2009-2017)
- Richard Kahn ↔ Epstein: 437 emails (2011-2019)
- Lesley Groff ↔ Epstein: 208 emails (2014-2019)
- Noam Chomsky ↔ Epstein: 194 emails
- Deepak Chopra ↔ Epstein: 184 emails

---

## DOJ Data Structure

- **12 Data Sets** (DS1–DS12), ~2.8M pages, ~1.4M documents, ~218GB raw
- **URL pattern:** `https://www.justice.gov/epstein/files/DataSet%20{N}/EFTA{8digits}.pdf`
- **Pagination:** 50 files/page, `?page=N` (0-indexed)
- **Age gate:** JavaScript cookie required (Playwright handles this)
- **EFTA numbering:** Per-PAGE, not per-document. Multi-page docs consume consecutive numbers.

| Dataset | EFTA Start | EFTA End | Est Files |
|---------|-----------|----------|-----------|
| 1 | 00000001 | 00003158 | ~3,158 |
| 2 | 00003159 | 00003857 | ~699 |
| 3 | 00003858 | 00005586 | ~1,729 |
| 4 | 00005705 | 00008320 | ~2,616 |
| 5 | 00008409 | 00008528 | ~120 |
| 6 | 00008529 | 00008998 | ~470 |
| 7 | 00009016 | 00009664 | ~649 |
| 8 | 00009676 | 00039023 | ~29,348 |
| 9 | 00039025 | 01262781 | ~103,608 |
| 10 | 01262782 | 02205654 | ~94,287 |
| 11 | 02205655 | 02730264 | ~52,459 |
| 12 | 02730265 | 02858497 | ~12,820 |

---

## Workflow: Download → OCR → Analyze → Knowledge Graph

### The Integration Plan

```
┌──────────────────────┐         ┌──────────────────────────┐
│   epstein-ripper     │         │   Epstein-Pipeline       │
│   (UPSTREAM)         │         │   (UPSTREAM)             │
│                      │         │                          │
│   Downloads PDFs     │───────▶│   ocr ./raw-files/data1/ │
│   from DOJ website   │  files  │   extract-entities ...   │
│   with Playwright    │  on     │   embed ...              │
│   age-gate bypass    │  disk   │   build-graph ...        │
│                      │         │   export sqlite ...      │
└──────────────────────┘         └──────────────────────────┘
         │                                  │
         ▼                                  ▼
  /mnt/data/epstein-project/        /mnt/data/epstein-project/
  raw-files/data{N}/                processed/
    ├── EFTA00000001.pdf              ├── ocr/
    ├── EFTA00000002.pdf              ├── entities/
    ├── ...                           ├── embeddings/
    └── index_data{N}.json            └── knowledge-graph/
```

### Commands (in order)

```bash
# 1. DOWNLOAD — epstein-ripper (NOT pipeline's broken download command)
cd /home/cbwinslow/workspace/epstein/epstein-ripper
python3 auto_ep_rip.py --datasets 1 --out-dir /mnt/data/epstein-project/raw-files

# 2. OCR — pipeline reads PDFs from disk, outputs JSON
epstein-pipeline ocr /mnt/data/epstein-project/raw-files/data1/ \
  -o /mnt/data/epstein-project/processed/ocr/data1/ \
  --backend surya --workers 4

# 3. ENTITY EXTRACTION — NER on OCR text
epstein-pipeline extract-entities /mnt/data/epstein-project/processed/ocr/data1/ \
  -o /mnt/data/epstein-project/processed/entities/

# 4. EMBEDDINGS — vector representations for semantic search
epstein-pipeline embed /mnt/data/epstein-project/processed/ocr/data1/ \
  -o /mnt/data/epstein-project/processed/embeddings/

# 5. KNOWLEDGE GRAPH — build from extracted entities
epstein-pipeline build-graph /mnt/data/epstein-project/processed/ \
  -o /mnt/data/epstein-project/knowledge-graph/

# 6. EXPORT — to SQLite/JSON/CSV
epstein-pipeline export sqlite /mnt/data/epstein-project/processed/ \
  -o /mnt/data/epstein-project/databases/processed_corpus.db
```

### Why This Works
- **epstein-ripper** saves standard PDF files to disk
- **Epstein-Pipeline's `ocr` command** accepts a directory of PDF files as input
- They don't need to know about each other — the filesystem is the interface
- We can swap downloaders or processors independently

---

## Our Custom Code (scripts/)

| File | Purpose |
|------|---------|
| `scripts/tracker.py` | Shared-state progress tracker (JSON-backed, multi-process safe) |
| `scripts/file_watcher.py` | Background file-size monitor that feeds tracker |
| `scripts/explore_kg.py` | Knowledge graph exploration CLI |

These are OUR code. They call upstream tools but don't modify them.

---

## Status

- [x] Storage mounted (2.3TB free)
- [x] All repos cloned (4 upstream repos)
- [x] Pipeline installed (core + spaCy + pymupdf + playwright)
- [x] All databases downloaded (8.4GB)
- [x] Knowledge graph explored (606 entities, 2,302 relationships)
- [x] Progress tracker built
- [x] Codebase separation rules defined
- [ ] DOJ file downloads started
- [ ] OCR processing pipeline tested
- [ ] GPU workers configured for surya/faster-whisper
- [ ] Embedding generation tested
- [ ] Custom knowledge graph extensions built

---

## Session Log

### 2026-03-20
- Mounted LVM volume, cloned 4 repos, installed pipeline + deps
- Downloaded 8 pre-built databases (8.4GB)
- Explored knowledge graph, communications, redaction data
- Built progress tracker (tracker.py + file_watcher.py)
- Established codebase separation rules
- Identified workflow: ripper downloads → pipeline processes → our scripts track/extend
- **Full validation completed**: 30/30 tests passed, 3 issues found and fixed
- Fixed: Playwright system deps, file_watcher glob patterns, pipeline CLI invocation
- Playwright confirmed working: navigated DOJ site, clicked age gate, extracted 50 PDF links
- Full validation report at `VALIDATION_REPORT.md`

### Next Session TODOs
- [ ] Start DOJ file downloads (epstein-ripper)
- [ ] Test OCR pipeline on small batch
- [ ] Install GPU packages (surya-ocr, faster-whisper, sentence-transformers)
