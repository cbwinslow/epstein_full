# AI Agent Master Index

> **Last Updated:** April 10, 2026  
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
| **FEC Agent** | Campaign Finance | ✅ | 5.4M | [INGESTION_GUIDES/05-fec-contributions.md](INGESTION_GUIDES/05-fec-contributions.md) |
| **HF Agent** | HuggingFace Datasets | 🔴 | ~20K | [INGESTION_GUIDES/06-huggingface-datasets.md](INGESTION_GUIDES/06-huggingface-datasets.md) |
| **GitHub Agent** | Third-Party Repos | 🔴 | 10K+ nodes | [INGESTION_GUIDES/07-third-party-repos.md](INGESTION_GUIDES/07-third-party-repos.md) |

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
3. **Pick** an ingestion guide from `INGESTION_GUIDES/`
4. **Follow** the step-by-step procedures

### Before Starting Work

1. Check `DATA_INVENTORY_FULL.md` for current data status
2. Verify which sources are already ingested
3. Identify gaps or incomplete pipelines
4. Check `../DATA_INVENTORY_FULL.md` for coverage analysis

---

## 📊 Coverage Gaps (Priority Tasks)

### High Priority

1. **House Oversight 2024** (~20K docs) - HuggingFace datasets
2. **Black Book + Flight Logs** - From dleerdefi repo
3. **Neo4j Knowledge Graph** - 10K nodes, 16K relations

### Medium Priority

4. **Pre-2015 News** - CourtListener RECAP, Wayback Machine
5. **Birthday Book** - 128 pages from dleerdefi repo
6. **FBI Vault** - Complete document set

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

*Generated: April 10, 2026*
