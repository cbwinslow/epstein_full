# Epstein Data Pipeline Scripts

> **Last Updated:** April 24, 2026
> **Purpose:** Organized collection of all ingestion, import, processing, and enrichment scripts

---

## 📂 Directory Structure

```
scripts/
├── download/              # Phase 2: Download scripts (668 files)
│   ├── download_congress_bills.py
│   ├── download_congress_historical.py
│   ├── download_fara.py / download_fara_bulk.py
│   ├── download_fec_2024.py / download_fec_committees.py
│   ├── download_govinfo_bulk.py / download_govinfo_historical.py
│   ├── download_house_vote_details.py
│   ├── download_senate_vote_details.py  # 🔴 403 errors (Issue #58)
│   ├── download_sec_edgar_recent.py      # 🔴 Needs bulk run (Issue #55)
│   ├── download_whitehouse.py
│   └── download_hf_*.py               # HuggingFace downloads
│
├── import/               # Phase 3: Import scripts to PostgreSQL
│   ├── import_jmail_full.py / import_jmail_documents.py
│   ├── import_icij.py
│   ├── import_fara.py
│   ├── import_congress.py
│   ├── import_fec.py / import_fec_committees.py
│   ├── import_whitehouse_visitors.py
│   ├── import_hf_*.py                  # HuggingFace imports
│   ├── import_dleerdefi_*.py          # GitHub third-party imports
│   └── import_neo4j_graph.py           # 📍 Needs import
│
├── enrichment/          # Phase 5: Enrichment (embeddings, etc.)
│   ├── rtx3060_embeddings.py        # ✅ Complete (Issue #50)
│   ├── embed_*.py                   # Various embedding scripts
│   ├── batch_ner_extraction.py
│   ├── extract_entities.py
│   ├── load_supplementary.py           # 🔴 Needs run
│   └── generate_*.py                  # Generation scripts
│
├── processing/           # Phase 4-5: Processing scripts
│   ├── master_unify.py              # 🔴 Build knowledge graph (Issue #30)
│   ├── generate_*.py                 # Embeddings generation
│   ├── import_*.py                   # Embeddings import
│   ├── vectorize_documents.py
│   ├── optimized_postgresql_pipeline.py
│   └── deduplicate*.py
│
├── ingestion/            # Phase 1: Discovery + pipeline orchestration
│   ├── check_*.py                    # Inventory/status checks
│   ├── collect_epstein_*.py
│   ├── gdelt_*.py
│   └── phase1_discovery.py
│
├── archive/               # Legacy/reference scripts
│   ├── advanced_processing_demo.py
│   ├── ai_quality_agent.py
│   └── process_sample.py
│
├── config.py              # Centralized paths configuration
└── README.md              # This file
```

---

## 📋 Pipeline Phases

### Phase 1: Discovery & Planning
**Location:** `scripts/ingestion/`

| Script | Purpose | Status |
|--------|---------|--------|
| `check_inventory.py` | Inventory all data sources | ✅ Complete |
| `check_gov_data_status.py` | Verify GovInfo/EC/Congress | ✅ Complete |
| `check_icij_schema.py` | Verify ICJ schema | ✅ Complete |
| `phase1_discovery.py` | Initial discovery | ✅ Complete |

**Usage:**
```bash
# Check what's available
python scripts/ingestion/check_inventory.py

# Verify government data status
python scripts/ingestion/check_gov_data_status.py
```

---

### Phase 2: Download
**Location:** `scripts/download/` (668 scripts)

| Script | Source | Status |
|--------|--------|--------|
| `download_congress_historical.py` | Congress 105th-119th | ✅ Complete |
| `download_govinfo_bulk.py` | GovInfo bulk (FR, Bills) | ✅ Complete |
| `download_govinfo_historical.py` | GovInfo 2000+ | ✅ Complete |
| `download_whitehouse.py` | White House Visitors | ✅ Complete |
| `download_fara.py` / `download_fara_bulk.py` | FARA Registrations | ✅ Complete |
| `download_fec_*.py` | FEC Contributions | ✅ Complete |
| `download_hf_*.py` | HuggingFace Datasets | ✅ Complete |
| `download_senate_vote_details.py` | Senate Vote Details | 🔴 403 errors |
| `download_sec_edgar_recent.py` | SEC EDGAR | 🔴 Needs bulk run |

**Usage:**
```bash
# Download Congress historical data
python scripts/download/download_congress_historical.py --congress 105

# Download GovInfo bulk
python scripts/download/download_govinfo_bulk.py --type FR --year 2024

# Retry with rate limiting
python scripts/download/download_senate_vote_details.py --retry --delay 2.0
```

**Key Download Tools:**
- `epstein-ripper/auto_ep_rip.py` - DOJ Epstein Library (Playwright)
- `epstein-pipeline/gdelt_*.py` - GDELT news collection

---

### Phase 3: Import to PostgreSQL
**Location:** `scripts/import/`

| Script | Tables Created | Status |
|--------|---------------|--------|
| `import_jmail_full.py` | `jmail_emails_full` (1.78M) | ✅ Complete |
| `import_icij.py` | `icij_entities`, `icij_relationships` | ✅ Complete |
| `import_fara.py` | `fara_registrations`, `fara_foreign_principals` | ✅ Complete |
| `import_congress.py` | `congress_bills`, `congress_members`, `congress_*_votes` | ✅ Complete |
| `import_fec.py` | `fec_individual_contributions` (447M) | ✅ Complete |
| `import_whitehouse_visitors.py` | `whitehouse_visitors` (2.5M) | ✅ Complete |
| `import_hf_*.py` | `hf_epstein_files_20k` (2.1M) | ✅ Complete |
| `import_dleerdefi_*.py` | `black_book_contacts`, `flight_logs_github` | ✅ Complete |
| `import_neo4j_graph.py` | `kg_persons`, `kg_relationships` | 📍 Needs import |

**Usage:**
```bash
# Import jMail emails
python scripts/import/import_jmail_full.py

# Import GitHub third-party data
python scripts/import/import_dleerdefi_black_book.py

# Import Neo4j graph
python scripts/import/import_neo4j_graph.py
```

---

### Phase 4: Processing (OCR, NER)
**Location:** `epstein-pipeline/` + `scripts/processing/`

| Process | Script | Output | Status |
|---------|--------|--------|--------|
| OCR PDFs | `epstein-pipeline ocr` | `processed/ocr_output/` | ✅ Complete |
| Extract Entities | `epstein-pipeline extract-entities` | `processed/entities/` | ✅ Complete |
| Batch NER | `scripts/enrichment/batch_ner_extraction.py` | Entity JSON | ✅ Complete |
| Process Full Pages | `scripts/processing/epstein_full_pages_processor.py` | Processed text | ✅ Complete |

**Usage:**
```bash
# OCR PDFs with Surya (GPU)
epstein-pipeline ocr /home/cbwinslow/workspace/epstein-data/raw-files/data1/ \
  -o /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
  --backend surya

# Extract entities with spaCy
epstein-pipeline extract-entities \
  /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
  -o /home/cbwinslow/workspace/epstein-data/processed/entities/
```

---

### Phase 5: Enrichment (Embeddings, Knowledge Graph)
**Location:** `scripts/enrichment/` + `scripts/processing/`

| Process | Script | Output | Status |
|---------|--------|--------|--------|
| Generate Embeddings (RTX 3060) | `scripts/enrichment/rtx3060_embeddings.py` | Vectors | ✅ Complete |
| Generate Embeddings (pgvector) | `scripts/enrichment/embed_*.py` | pgvector | 🔴 In progress |
| Build Knowledge Graph | `scripts/processing/master_unify.py` | Neo4j/PostgreSQL | 🔴 Needs update |
| Cross-Reference | `scripts/enrichment/load_supplementary.py` | Relationships | 🔴 Needs run |
| Deduplicate | `scripts/processing/deduplicate*.py` | Cleaned data | ✅ Complete |

**Usage:**
```bash
# Generate embeddings with RTX 3060 (GPU)
python scripts/enrichment/rtx3060_embeddings.py \
  --input /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
  --output /home/cbwinslow/workspace/epstein-data/processed/embeddings/

# Build master knowledge graph
python scripts/processing/master_unify.py \
  --sources epstein,dleeerdefi,icij \
  --output /home/cbwinslow/workspace/epstein-data/knowledge-graph/
```

---

## 🔧 Open Issues (Where Codex Left Off)

### High Priority (🚨 Urgent)

| Issue | Title | Script | Status |
|--------|-------|--------|--------|
| #58 | Senate vote detail backfill | `download_senate_vote_details.py` | 🔴 403 errors |
| #55 | SEC EDGAR bulk ingestion | `download_sec_edgar_recent.py` | 🔴 Needs bulk run |
| #39 | 749K missing documents | - | 🔴 Gap identified |
| #44 | FBI Vault text | `download_fbi_vault.py` | 🔴 Need ingest |
| #30 | Knowledge graph connections | `master_unify.py` | 🔴 Needs build |

### Medium Priority

| Issue | Title | Script | Status |
|--------|-------|--------|--------|
| #52 | GovInfo expansion | `download_govinfo_bulk.py` | 🔴 Beyond baseline |
| #29 | Text embeddings | `embed_*.py` | 🔴 Expand coverage |
| #28 | jMail iMessages | - | 🔴 Need download |
| #12 | Updated knowledge graph | `master_unify.py` | 🔴 From entities |

---

## 📝 Configuration

### Centralized Config
**File:** `scripts/config.py`

```python
# Key paths (all scripts use this)
DATA_DIR = Path('/home/cbwinslow/workspace/epstein-data')
SCRIPTS_DIR = Path('/home/cbwinslow/workspace/epstein/scripts')
EPSTEIN_RIPPER_DIR = Path('/home/cbwinslow/workspace/epstein/epstein-ripper')
EPSTEIN_PIPELINE_DIR = Path('/home/cbwinslow/workspace/epstein/epstein-pipeline')
```

**Usage in scripts:**
```python
import sys
sys.path.insert(0, str(SCRIPTS_DIR))
from config import DATA_DIR, EPSTEIN_RIPPER_DIR
```

---

## 📊 How to Add a New Data Source

### Step 1: Create Download Script
```bash
# Create in scripts/download/
vim scripts/download/download_newsource.py
```

**Template:**
```python
#!/usr/bin/env python3
"""
Download NEWSOURCE data for Epstein research.
Usage: python scripts/download/download_newsource.py --year 2024
"""
import argparse
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein/scripts')
from config import DATA_DIR

def download_newsource(year):
    output_dir = DATA_DIR / 'raw-files/newsource'
    output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: Implement download logic
    print(f"Downloading NEWSOURCE for {year}...")
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int)
    args = parser.parse_args()
    download_newsource(args.year)
```

### Step 2: Create Import Script
```bash
vim scripts/import/import_newsource.py
```

### Step 3: Document in docs/agents/INGESTION_GUIDES/
```bash
vim docs/agents/INGESTION_GUIDES/XX-newsource.md
```

### Step 4: Update Inventory
```bash
vim docs/DATA_INVENTORY_FULL.md
# Add to: "## 7. NEW SOURCE"
```

### Step 5: Update Master Index
```bash
vim docs/agents/MASTER_INDEX.md
# Add to: "### Data Source Agents"
```

---

## 📌 Reusing This Pipeline

### For Another Project

1. **Copy the structure:**
   ```bash
   cp -r scripts/ myproject/
   cp -r docs/ myproject/
   ```

2. **Update `config.py` with new paths:**
   ```python
   DATA_DIR = Path('/home/user/myproject-data')
   SCRIPTS_DIR = Path('/home/user/myproject/scripts')
   ```

3. **Follow the templates** in Section "How to Add a New Data Source"

### For Another Researcher

1. **Clone the repo:**
   ```bash
   git clone https://github.com/YOURNAME/epstein.git
   cd epstein
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline:**
   ```bash
   # Follow docs/AGENTS.md for step-by-step
   ```

---

## 📚 References

- **Master Inventory:** `docs/DATA_INVENTORY_FULL.md`
- **Agent Index:** `docs/agents/MASTER_INDEX.md`
- **Ingestion Guides:** `docs/agents/INGESTION_GUIDES/` (01-07 .md files)
- **Procedures:** `docs/agents/PROCEDURES/` (data-collection, quality-assurance, pipeline-orchestration)
- **Config File:** `scripts/config.py`

---

*Last Updated: April 24, 2026*
*Status: Ready for Continuation*
*Maintained by: Research Team*
