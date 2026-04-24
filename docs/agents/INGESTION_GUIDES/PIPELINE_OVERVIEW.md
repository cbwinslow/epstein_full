# Data Ingestion Pipeline Overview

> **Last Updated:** April 24, 2026
> **Purpose:** Comprehensive guide to the Epstein data ingestion pipeline - organized, repeatable, and reusable

---

## 🏗 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                        │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  PHASE 1  │   │  PHASE 2  │   │  PHASE 3  │
    │  DISCOVERY │   │  DOWNLOAD  │   │  INGEST   │
    └──────────┘   └──────────┘   └──────────┘
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ Sources    │   │  Raw      │   │  PostgreSQL │
    │ Identified │   │  Files    │   │  Database  │
    └──────────┘   └──────────┘   └──────────┘
                              │               │
                              ▼               ▼
                        ┌──────────┐   ┌──────────┐
                        │  PHASE 4  │   │  PHASE 5  │
                        │  PROCESS  │   │  ENRICH  │
                        └──────────┘   └──────────┘
                              │               │
                              ▼               ▼
                        ┌──────────┐   ┌──────────┐
                        │  OCR/NER  │   │  Embeddings│
                        │  Extract  │   │  Graph    │
                        └──────────┘   └──────────┘
```

---

## 📋 Pipeline Phases (in Order)

### Phase 1: Discovery & Planning
**Purpose:** Identify data sources, check availability, plan ingestion

| Step | Script | Status | Notes |
|------|--------|--------|-------|
| Inventory sources | `scripts/ingestion/check_inventory.py` | ✅ Complete | 421-line inventory |
| Check Gov status | `scripts/ingestion/check_gov_data_status.py` | ✅ Complete | GovInfo/FEC/Congress |
| Check ICJ schema | `scripts/ingestion/check_icij_schema.py` | ✅ Complete | Offshore leaks |
| Plan pipeline | `docs/DATA_INVENTORY_FULL.md` | ✅ Complete | Master inventory |

**Repeatable Usage:**
```bash
# Check what's available
python scripts/ingestion/check_inventory.py

# Verify government data status
python scripts/ingestion/check_gov_data_status.py

# Plan new ingestion
# 1. Read docs/DATA_INVENTORY_FULL.md
# 2. Check specific source guide in docs/agents/INGESTION_GUIDES/
# 3. Follow step-by-step procedure
```

---

### Phase 2: Download
**Purpose:** Download raw files from all sources

| Source | Script | Output Location | Status |
|--------|--------|-----------------|--------|
| DOJ Epstein Library | `epstein-ripper/auto_ep_rip.py` | `epstein-data/raw-files/data{1-12}/` | ✅ Complete (1.4M docs) |
| HuggingFace Datasets | `scripts/download/download_hf_*.py` | `epstein-data/huggingface/` | ✅ Complete (2.1M records) |
| Congress.gov Historical | `scripts/download/download_congress_historical.py` | `epstein-data/raw-files/congress_historical/` | ✅ Complete (105th-119th) |
| GovInfo Bulk | `scripts/download/download_govinfo_bulk.py` | `epstein-data/raw-files/govinfo_bulk/` | ✅ Complete (246 files) |
| GovInfo Historical | `scripts/download/download_govinfo_historical.py` | `epstein-data/raw-files/govinfo_historical/` | ✅ Complete (2000+) |
| White House Visitors | `scripts/download/download_whitehouse.py` | `epstein-data/raw-files/whitehouse_visitors/` | ✅ Complete (2.5M records) |
| FARA | `scripts/download/download_fara.py` | `epstein-data/raw-files/fara/` | ✅ Complete (7K+ records) |
| FEC | `scripts/download/download_fec_*.py` | `epstein-data/raw-files/fec/` | ✅ Complete (447M contributions) |
| GitHub Third-Party | `git clone` commands | `epstein-data/external_repos/` | ✅ Complete (dleeerdefi, etc.) |
| Senate Vote Details | `scripts/download/download_senate_vote_details.py` | `epstein-data/raw-files/senate_votes/` | 🔴 403 errors |
| SEC EDGAR | `scripts/download/download_sec_edgar_recent.py` | `epstein-data/raw-files/sec_edgar/` | 🔴 Needs bulk run |

**Repeatable Usage:**
```bash
# Download DOJ Epstein Library (uses Playwright)
cd epstein-ripper && python auto_ep_rip.py --dataset N

# Download HuggingFace dataset
python scripts/download/download_hf_resume.py --dataset epstein-files-20k

# Download Congress historical data (105th-119th)
python scripts/download/download_congress_historical.py --congress 105

# Download GovInfo bulk (Federal Register, Bills, etc.)
python scripts/download/download_govinfo_bulk.py --type FR --year 2024

# Retry with rate limiting
python scripts/download/download_senate_vote_details.py --retry --delay 2.0
```

**Key Download Scripts (in `scripts/download/`):**
- `download_congress_bills.py` - Congress bills
- `download_congress_historical.py` - Historical Congress data (105th+)
- `download_fara.py` / `download_fara_bulk.py` - FARA registrations
- `download_fec_2024.py` / `download_fec_committees.py` - FEC data
- `download_govinfo_bulk.py` / `download_govinfo_historical.py` - GovInfo bulk/historical
- `download_house_vote_details.py` - House vote details
- `download_senate_vote_details.py` - Senate vote details (403 issues)
- `download_sec_edgar_recent.py` - SEC EDGAR (Form 4, 13F)
- `download_whitehouse.py` - White House visitor logs
- `download_hf_resume.py` - HuggingFace dataset downloads

---

### Phase 3: Import to PostgreSQL
**Purpose:** Import downloaded data into structured PostgreSQL tables

| Source | Script | Tables Created | Status |
|--------|--------|---------------|--------|
| jMail World Emails | `scripts/import/import_jmail_*.py` | `jmail_emails_full` (1.78M) | ✅ Complete |
| jMail World Documents | `scripts/import/import_jmail_documents.py` | `jmail_documents` (1.41M) | ✅ Complete |
| ICJ Offshore Leaks | `scripts/import/import_icij.py` | `icij_entities`, `icij_relationships` | ✅ Complete |
| FARA Bulk | `scripts/import/import_fara.py` | `fara_registrations`, `fara_foreign_principals` | ✅ Complete |
| GovInfo | `scripts/import/import_govinfo_*.py` | `federal_register_entries`, `court_opinions` | ✅ Complete |
| Congress | `scripts/import/import_congress.py` | `congress_bills`, `congress_members`, `congress_*_votes` | ✅ Complete |
| White House Visitors | `scripts/import/import_whitehouse_visitors.py` | `whitehouse_visitors` (2.5M) | ✅ Complete |
| HuggingFace epstein-files-20k | `scripts/import/import_hf_epstein_files_20k.py` | `hf_epstein_files_20k` (2.1M) | ✅ Complete |
| Black Book (GitHub) | `scripts/import/import_black_book_json.py` | `black_book_contacts` (1.2K) | ✅ Complete |
| Flight Logs (GitHub) | `scripts/import/import_flight_logs.py` | `flight_logs_github` (2K) | ✅ Complete |
| Neo4j Graph (GitHub) | `scripts/import/import_neo4j_graph.py` | `kg_persons`, `kg_relationships` | 🔴 Needs import |
| FEC Individual | `scripts/import/import_fec.py` | `fec_individual_contributions` (447M) | ✅ Complete |

**Repeatable Usage:**
```bash
# Import jMail emails to PostgreSQL
python scripts/import/import_jmail_full.py

# Import GitHub third-party data (Black Book)
python scripts/import/import_dleeerdefi_black_book.py

# Import HuggingFace dataset
python scripts/import/import_hf_epstein_files_20k.py

# Import Congress data
python scripts/import/import_congress.py --type bills --congress 119

# Bulk import with progress tracking
python scripts/import/import_fara.py --bulk --track-progress
```

**Key Import Scripts (in `scripts/import/`):**
- `import_jmail_full.py` / `import_jmail_documents.py` - jMail World
- `import_icij.py` - ICJ Offshore Leaks
- `import_fara.py` - FARA registrations
- `import_congress.py` - Congress data
- `import_fec.py` / `import_fec_committees.py` - FEC data
- `import_whitehouse_visitors.py` - White House logs
- `import_hf_*.py` - HuggingFace datasets
- `import_black_book_json.py` / `import_dleeerdefi_*.py` - GitHub third-party
- `import_neo4j_graph.py` - Neo4j knowledge graph

---

### Phase 4: Processing (OCR, NER, etc.)
**Purpose:** Extract structured data from raw files

| Process | Script | Output | Status |
|---------|--------|--------|--------|
| OCR PDFs | `epstein-pipeline/ocr` CLI | `epstein-data/processed/ocr_output/` | ✅ Complete |
| Extract Entities | `epstein-pipeline/extract-entities` CLI | `epstein-data/processed/entities/` | ✅ Complete |
| Batch NER | `scripts/enrichment/batch_ner_extraction.py` | Entity JSON files | ✅ Complete |
| Process Full Pages | `scripts/enrichment/epstein_full_pages_processor.py` | Processed text | ✅ Complete |
| Extract Entities | `scripts/enrichment/extract_entities.py` | Entity database | 🔴 Needs full run |

**Repeatable Usage:**
```bash
# OCR PDFs with Surya (GPU)
epstein-pipeline ocr /home/cbwinslow/workspace/epstein-data/raw-files/data1/ \
  -o /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
  --backend surya

# Extract entities with spaCy
epstein-pipeline extract-entities \
  /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
  -o /home/cbwinslow/workspace/epstein-data/processed/entities/

# Batch NER extraction
python scripts/enrichment/batch_ner_extraction.py \
  --input /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
  --output /home/cbwinslow/workspace/epstein-data/processed/entities/
```

**Key Processing Scripts (in `scripts/enrichment/` and `scripts/processing/`):**
- `batch_ner_extraction.py` - Batch NER with spaCy/GLiNER
- `extract_entities.py` - Entity extraction
- `epstein_full_pages_processor.py` - Full page processing
- `full_processing_pipeline.py` - Complete processing pipeline
- `vectorize_documents.py` - Document vectorization

---

### Phase 5: Enrichment (Embeddings, Knowledge Graph)
**Purpose:** Generate embeddings, build knowledge graph, semantic search

| Process | Script | Output | Status |
|---------|--------|--------|--------|
| Generate Embeddings (RTX 3060) | `scripts/enrichment/rtx3060_embeddings.py` | ✅ Complete |
| Generate Embeddings (pgvector) | `scripts/enrichment/embed_*.py` | 🔴 In progress |
| Build Knowledge Graph | `scripts/processing/master_unify.py` | 🔴 Needs update |
| Cross-Reference | `scripts/enrichment/load_supplementary.py` | 🔴 Needs run |
| Deduplicate | `scripts/processing/optimized_postgresql_pipeline.py` | ✅ Complete |
| Generate News Embeddings | `scripts/processing/generate_news_embeddings*.py` | 🔴 In progress |

**Repeatable Usage:**
```bash
# Generate embeddings with RTX 3060 (GPU)
python scripts/enrichment/rtx3060_embeddings.py \
  --input /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
  --output /home/cbwinslow/workspace/epstein-data/processed/embeddings/

# Build master knowledge graph
python scripts/processing/master_unify.py \
  --sources epstein,dleeerdefi,icij \
  --output /home/cbwinslow/workspace/epstein-data/knowledge-graph/

# Cross-reference datasets
python scripts/enrichment/load_supplementary.py \
  --primary epstein --secondary jmail,icij,fec
```

**Key Enrichment Scripts (in `scripts/enrichment/` and `scripts/processing/`):**
- `rtx3060_embeddings.py` - RTX 3060 embeddings (completed)
- `embed_*.py` - Various embedding scripts (CPU, GPU, fast)
- `master_unify.py` - Master knowledge graph unification
- `generate_*.py` - Various generation scripts (embeddings, news embeddings)
- `import_*.py` - Import scripts for embeddings
- `vectorize_documents.py` - Document vectorization

---

## 📂 Script Organization

### Directory Structure
```
scripts/
├── download/              # Phase 2: Download scripts (668 files)
│   ├── download_congress_*.py
│   ├── download_fara*.py
│   ├── download_fec*.py
│   ├── download_govinfo*.py
│   ├── download_hf_*.py
│   ├── download_senate_vote_details.py
│   ├── download_sec_edgar*.py
│   └── download_whitehouse.py
├── import/               # Phase 3: Import scripts
│   ├── import_jmail_*.py
│   ├── import_icij.py
│   ├── import_fara.py
│   ├── import_congress.py
│   ├── import_fec*.py
│   ├── import_whitehouse_visitors.py
│   ├── import_hf_*.py
│   ├── import_dleeerdefi_*.py
│   └── import_neo4j_graph.py
├── enrichment/          # Phase 5: Enrichment scripts
│   ├── rtx3060_embeddings.py
│   ├── embed_*.py
│   ├── batch_ner_extraction.py
│   ├── extract_entities.py
│   └── load_supplementary.py
├── processing/           # Phase 4-5: Processing scripts
│   ├── master_unify.py
│   ├── generate_*.py
│   ├── import_*.py
│   ├── vectorize_documents.py
│   ├── optimized_postgresql_pipeline.py
│   └── deduplicate*.py
├── ingestion/            # Phase 1: Discovery + pipeline orchestration
│   ├── check_*.py
│   ├── collect_epstein_*.py
│   ├── gdelt_*.py
│   └── phase1_discovery.py
├── archive/               # Legacy/reference scripts
│   ├── advanced_processing_demo.py
│   ├── ai_quality_agent.py
│   └── process_sample.py
└── README.md              # This file
```

---

## 🔧 procedures for Repeatable Pipeline

### Full Pipeline Run (from scratch)
```bash
# Step 1: Check inventory
python scripts/ingestion/check_inventory.py

# Step 2: Download all sources
./scripts/download/run_all_downloads.sh  # (create this wrapper)

# Step 3: Import to PostgreSQL
./scripts/import/run_all_imports.sh   # (create this wrapper)

# Step 4: Process (OCR, NER)
epstein-pipeline ocr --all
epstein-pipeline extract-entities --all

# Step 5: Enrich (embeddings, graph)
python scripts/processing/master_unify.py
python scripts/enrichment/rtx3060_embeddings.py --all
```

### Single Source Re-ingestion
```bash
# Example: Re-import Congress data after schema change
python scripts/import/import_congress.py --type bills --congress 119 --drop-existing
```

### Verify Data Integrity
```bash
# Check record counts
psql -d epstein -c "
SELECT 'congress_bills' as table, COUNT(*) FROM congress_bills
UNION ALL
SELECT 'jmail_emails', COUNT(*) FROM jmail_emails_full
UNION ALL
SELECT 'federal_register', COUNT(*) FROM federal_register_entries
"

# Check for duplicates
python scripts/processing/deduplicate_records.py --check-only
```

---

## 📊 Current Gaps (Where Codex Left Off)

### Open Issues (Priority Order)

| Issue | Title | Status | Scripts Available | Next Action |
|--------|-------|--------|-------------------|--------------|
| #58 | Senate vote detail backfill | 🔴 OPEN | `download_senate_vote_details.py` | Fix 403 errors, retry with alternate user agents |
| #55 | SEC EDGAR bulk ingestion | 🔴 OPEN | `download_sec_edgar_recent.py` | Run bulk import for Form 4, 13F |
| #52 | GovInfo expansion | 🔴 OPEN | `download_govinfo_bulk.py` | Expand beyond current baseline |
| #39 | 749K missing documents | 🔴 OPEN | - | Identify gaps, re-download |
| #44 | FBI Vault text | 🔴 OPEN | - | Download FBI Vault, OCR, add to full_text_corpus |
| #30 | Knowledge graph connections | 🔴 OPEN | `master_unify.py` | Build from document co-occurrence |
| #29 | Text embeddings | 🔴 OPEN | `embed_*.py` | Expand coverage beyond RTX 3060 |
| #28 | jMail iMessages/photos | 🔴 OPEN | - | Download media from jmail.world |
| #12 | Updated knowledge graph | 🔴 OPEN | `master_unify.py` | Run with extracted entities |
| #9 | Process HF parquet | ✅ CLOSED | `import_hf_*.py` | Verify completion |
| #8 | OCR pipeline | ✅ CLOSED | `epstein-pipeline ocr` | Verify all PDFs processed |

---

## 📝 For AI Agents (Reusing This Pipeline)

### Before Starting Work
1. **Read** `docs/DATA_INVENTORY_FULL.md` - Understand what's already ingested
2. **Check** `docs/agents/MASTER_INDEX.md` - See all agent procedures
3. **Pick** a source guide from `docs/agents/INGESTION_GUIDES/` - Step-by-step instructions
4. **Verify** scripts exist in `scripts/` before writing new ones

### Creating a New Ingestion for a Source
```bash
# 1. Create download script
vim scripts/download/download_NEWSOURCE.py

# 2. Create import script
vim scripts/import/import_NEWSOURCE.py

# 3. Document in docs/agents/INGESTION_GUIDES/
vim docs/agents/INGESTION_GUIDES/XX-newsource.md

# 4. Update inventory
vim docs/DATA_INVENTORY_FULL.md
# Add to: "## X. NEW SOURCE"

# 5. Update master index
vim docs/agents/MASTER_INDEX.md
# Add to: "### Data Source Agents"
```

### Template for New Download Script
```python
#!/usr/bin/env python3
"""
Download NEWSOURCE data for Epstein research.
Usage: python scripts/download/download_NEWSOURCE.py --year 2024
"""
import argparse
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein/scripts')
from config import DATA_DIR

def download_NEWSOURCE(year):
    output_dir = DATA_DIR / 'raw-files/newsource'
    output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: Implement download logic
    print(f"Downloading NEWSOURCE for {year}...")
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int)
    args = parser.parse_args()
    download_NEWSOURCE(args.year)
```

### Template for New Import Script
```python
#!/usr/bin/env python3
"""
Import NEWSOURCE data into PostgreSQL.
Usage: python scripts/import/import_NEWSOURCE.py
"""
import asyncpg
import asyncio

async def import_NEWSOURCE():
    conn = await asyncpg.connect(
        "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
    )

    # Create table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS newsource_data (
            id SERIAL PRIMARY KEY,
            data TEXT,
            source TEXT DEFAULT 'NEWSOURCE'
        )
    """)

    # TODO: Implement import logic
    print("Importing NEWSOURCE...")

    await conn.close()

if __name__ == '__main__':
    asyncio.run(import_NEWSOURCE())
```

---

## 📚 References

- **Master Inventory:** `docs/DATA_INVENTORY_FULL.md`
- **Agent Index:** `docs/agents/MASTER_INDEX.md`
- **Ingestion Guides:** `docs/agents/INGESTION_GUIDES/` (01-07 .md files)
- **Procedure Guides:** `docs/agents/PROCEDURES/` (data-collection, quality-assurance, pipeline-orchestration)
- **Config File:** `scripts/config.py` (centralized paths)
- **External Tools:** `epstein-ripper/` (DOJ downloads), `epstein-pipeline/` (OCR, NER, etc.)

---

*Last Updated: April 24, 2026*
*Maintained by: Research Team*
*Status: Ready for Continuation*
