# AI Agent Master Index

> **Last Updated:** April 24, 2026
> **Purpose:** Central index for all AI agent documentation and procedures

---

## 📁 Agent Documentation Structure

```
docs/agents/
├── README.md                    # This file - Master index
├── ARCHITECTURE.md              # System architecture overview
├── DATA_SOURCES.md              # All data sources with ingestion procedures
├── INGESTION_GUIDES/            # Per-source detailed guides
│   ├── 01-doj-epstein-library.md
│   ├── 02-jmail-world.md
│   ├── 03-gdelt-news.md
│   ├── 04-icij-offshore-leaks.md
│   ├── 05-fec-contributions.md
│   ├── 06-huggingface-datasets.md
│   └── 07-third-party-repos.md
├── WORKER_AGENTS.md             # Specialized worker definitions
└── PROCEDURES/                  # Step-by-step procedures
    ├── data-collection.md
    ├── quality-assurance.md
    └── pipeline-orchestration.md
```

---

## 🎯 Quick Reference

### Data Source Agents

| Agent | Data Source | Status | Records | Guide |
|-------|-------------|--------|---------|-------|
| **DOJ Agent** | DOJ Epstein Library | ✅ | 1.4M docs | [INGESTION_GUIDES/01-doj-epstein-library.md](INGESTION_GUIDES/01-doj-epstein-library.md) |
| **jMail Agent** | jMail World Emails | ✅ | 1.78M emails | [INGESTION_GUIDES/02-jmail-world.md](INGESTION_GUIDES/02-jmail-world.md) |
| **GDELT Agent** | News Articles | 🟡 | 23,413+ | [INGESTION_GUIDES/03-gdelt-news.md](INGESTION_GUIDES/03-gdelt-news.md) |
| **ICIJ Agent** | Offshore Leaks | ✅ | 814K entities | [INGESTION_GUIDES/04-icij-offshore-leaks.md](INGESTION_GUIDES/04-icij-offshore-leaks.md) |
| **FEC Agent** | Campaign Finance | ✅ | 447.2M contributions (2000-2026) | [INGESTION_GUIDES/05-fec-contributions.md](INGESTION_GUIDES/05-fec-contributions.md) |
| **HF Agent** | HuggingFace Datasets | ✅ | 634 parquet files (318GB) | [INGESTION_GUIDES/06-huggingface-datasets.md](INGESTION_GUIDES/06-huggingface-datasets.md) |
| **GitHub Agent** | Third-Party Repos | 🟡 | Mixed (partially imported) | [INGESTION_GUIDES/07-third-party-repos.md](INGESTION_GUIDES/07-third-party-repos.md) |

### Government Ingestion Snapshot (Updated April 24, 2026 UTC)

| Dataset | Coverage | Count |
|---------|----------|-------|
| Federal Register | 2000-2024 | 737,940 |
| Congress Bills | 105th-119th | 368,651 |
| Congress Members | 105th-119th | 10,413 |
| Congress House Votes | 117th-119th | 2,738 |
| Congress Senate Votes | 106th-119th | 3,132 (partial, source 403 retries pending) |
| Congress Bill Text Versions | 113th-119th | 130,361 |
| White House Visitors | 2009-2024 | 2,544,984 |
| GovInfo Bulk Import Files | FR/BILLS/BILLSTATUS/BILLSUM | 246 complete |
| FARA Registrations | current bulk | 7,045 |
| FARA Foreign Principals | current bulk | 17,358 |
| FARA Short Forms | current bulk | 44,413 |
| FARA Registrant Docs | current bulk | 124,224 |

### Worker Agents

| Agent | Role | Tools | GPU |
|-------|------|-------|-----|
| **Download Worker** | DOJ file downloading | Playwright, aiohttp | - |
| **OCR Worker** | PDF text extraction | PyMuPDF, Surya, Docling | K80 |
| **NER Worker** | Entity extraction | spaCy, GLiNER | K80/K40m |
| **Transcribe Worker** | Audio/video transcription | faster-whisper | K80 |
| **Image Worker** | Image analysis | Vision models | K80 |
| **KG Worker** | Knowledge graph building | Neo4j, spaCy | CPU |

---

## 🚀 Getting Started for AI Agents  

### New Agent Onboarding  

1. **Read** `ARCHITECTURE.md` - Understand the system  
2. **Read** `DATA_SOURCES.md` - Know all data sources  
3. **Read** `INGESTION_GUIDES/PIPELINE_OVERVIEW.md` - Understand pipeline phases  
4. **Pick** a source guide from `INGESTION_GUIDES/`  
5. **Follow** the step-by-step procedures in `PROCEDURES/`  

### Before Starting Work  

1. Check `DATA_INVENTORY_FULL.md` for current data status  
2. Verify which sources are already ingested  
3. Identify gaps or incomplete pipelines  
4. Check `../DATA_INVENTORY_FULL.md` for coverage analysis  
5. Read `scripts/README.md` to understand script organization  

---

## 📊 Coverage Gaps (Where Codex Left Off - Open Issues)  

### High Priority (🚨 Urgent)  

1. **Issue #58** - Senate vote details backfill (403 errors) - `download_senate_vote_details.py` 🔴  
2. **Issue #55** - SEC EDGAR bulk ingestion (Form 4/13F) - `download_sec_edgar_recent.py` 🔴  
3. **Issue #39** - 749K missing documents gap identification 🔴  
4. **Issue #44** - FBI Vault text addition to full-text index 🔴  
5. **Issue #30** - Knowledge graph connections from document co-occurrence 📍  

### Medium Priority  

6. **Issue #52** - GovInfo expansion beyond current bulk baseline 🔴  
7. **Issue #29** - Text embeddings expansion beyond RTX 3060 🔴  
8. **Issue #28** - jMail iMessages/photos download 🔴  
9. **Issue #12** - Updated knowledge graph from extracted entities 📍  

### Completed Recently (✅ Closed April 2026)  

10. **Issue #60** - GovInfo 119 normalization reconciliation ✅  
11. **Issue #59** - FARA normalized bulk import ✅  
12. **Issue #51** - Congress.gov completion (106th-119th) ✅  
13. **Issue #56/#54** - White House visitor logs ingestion ✅  
14. **Issue #50/#47** - RTX 3060 Embeddings + Phase 22 Media ✅  
15. **Issue #46/#45/#40** - Fill data gaps, Epstein Exposed emails, SEC EDGAR ✅  
16. **Issue #38/#35/#34** - FBI Vault, persons registry, jMail import ✅  
17. **Issue #33/#32/#31** - FBI Vault, ICJ Offshore, HuggingFace ✅  
18. **Issue #27/#9/#8** - jMail dataset, Process HF parquet, OCR pipeline ✅  

### Medium Priority

4. **Pre-2015 news coverage** - expand CourtListener/Wayback/news archives
5. **Pre-107th Congress strategy** - requires Congress.gov API key + alternative pathing
6. **Pre-2009 White House data alternatives** - constrained by public disclosure limits

### Low Priority

7. **Image Analysis** - 38K images from PDFs
8. **Embeddings** - 100% document coverage

---

## 🔗 Key Files

| File | Purpose |
|------|---------|
| `../../DATA_INVENTORY_FULL.md` | Complete data inventory |
| `../../docs/GDELT_PIPELINE.md` | GDELT ingestion docs |
| `../../epstein-pipeline/` | Processing scripts |
| `../../scripts/` | Import scripts |

---

## 📝 Notes for AI Agents

- **Always** check current status before starting work
- **Verify** data doesn't already exist (check PostgreSQL)
- **Document** any new procedures you create
- **Update** this index when adding new sources
- **Respect** rate limits and terms of service

---

*Generated: April 24, 2026*
