# Epstein Files Analysis - Agent Configuration

> **Last Updated:** April 28, 2026
> **Purpose:** Master configuration for AI agents working on Epstein data analysis

## 📚 Documentation Structure

| Document | Purpose | Location |
|----------|---------|----------|
| **DATA_INVENTORY_FULL.md** | Complete data source catalog | `docs/DATA_INVENTORY_FULL.md` |
| **MASTER_INDEX.md** | Central index for all agents | `docs/agents/MASTER_INDEX.md` |
| **INGESTION_GUIDES/** | Per-source detailed procedures | `docs/agents/INGESTION_GUIDES/` |
| **GDELT_PIPELINE.md** | News ingestion pipeline | `docs/GDELT_PIPELINE.md` |
| **FINANCIAL_DISCLOSURES_SUMMARY.md** | Financial disclosure pipeline summary | `docs/FINANCIAL_DISCLOSURES_SUMMARY.md` |
| **INGESTION_STATUS_REPORT.md** | Current ingestion status | `docs/INGESTION_STATUS_REPORT.md` |
| **FINAL_INGESTION_STATUS.md** | Task completion summary | `docs/FINAL_INGESTION_STATUS.md` |

### Quick Links for AI Agents

- **Data Sources Overview:** See `docs/agents/MASTER_INDEX.md`
- **Ingestion Procedures:** See `docs/agents/INGESTION_GUIDES/`
- **Current Data Status:** See `docs/DATA_INVENTORY_FULL.md`
   - Senate votes: 6,474 rows in congress_senate_votes + 647,338 member votes (complete, 403 resolved) ✅
   - Email: 1,783,792 rows in jmail_emails_full (complete) ✅
   - SEC EDGAR: 254 rows in sec_insider_transactions (April 2026 only, 88 Form 4 insider transactions) ⚠️
   - FBI Vault: 22 docs (1,426 pages) in documents table (complete) ✅
   - FARA: 7,045 registrations + 17,358 principals (complete) ✅
   - House Financial Disclosures: 50,429 records (2008-2026) ✅
   - Senate Financial Disclosures: 2,602 records (2012-2026) ✅
   - Trading Transactions: 18,521 (across 326 politicians) ✅
   - FEC Contributions: 490,000 records (2024 only, missing 2000-2023) 🔴
   - LDA Lobbying: 30,600 filings (2015 only, missing 2000-2014, 2016-2026) 🔴
  - **Coverage Gaps:** SEC bulk historical data blocked (403 errors), FEC missing cycles, LDA incomplete, pre-107th Congress expansion path, pre-2009 White House logs

## Recent Updates (April 2026)

- **Issue #61**: Resolved Senate vote‑detail 403 blocks and completed backfill (see `docs/GOVERNMENT_DATA_PIPELINE.md`). ✅
- **Issue #102**: Initiated planning for pre‑107th Congress data expansion.
- **Issue #103**: Logged pending work for pre‑2009 White House logs ingestion.
- **Issue #FIN-001**: ✅ **COMPLETE** - Financial disclosure data ingestion pipeline operational. CapitolGains integration complete. 50,429 House + 2,602 Senate disclosures ingested. Cross-reference analysis with FEC (447M+ contributions) and LDA (30,600 lobbying filings) active. See `docs/FINANCIAL_DISCLOSURES_SUMMARY.md`.
- **Issue #SEC-001**: ⚠️ **PARTIAL** - SEC EDGAR Form 4 insider transactions imported (254 records, 88 actual Form 4 filings from April 2026). Bulk historical data blocked by SEC 403 errors. See `docs/INGESTION_STATUS_REPORT.md`.
- **Issue #FEC-001**: 🔴 **INCOMPLETE** - FEC contributions only 2024 cycle loaded (490K records). Missing 2000-2023 cycles (~447M total). Requires reload. See `docs/INGESTION_STATUS_REPORT.md`.
- **Issue #LDA-001**: 🔴 **INCOMPLETE** - LDA filings only 2015 data (30.6K records). Missing 2000-2014, 2016-2026. Requires bulk download. See `docs/INGESTION_STATUS_REPORT.md`.

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
