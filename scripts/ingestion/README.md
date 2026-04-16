# Data Ingestion Pipeline

## Overview

This directory contains all scripts for downloading, importing, and processing data from various sources related to the Epstein case investigation.

## Directory Structure

```
ingestion/
├── README.md                    # This file
├── master_import_all.py         # Master orchestration script
├── quality_control_queries.sql  # Data quality validation queries
├── download/                    # Download scripts by source
├── import/                      # Import scripts by source
├── processing/                  # Data processing scripts
├── enrichment/                 # Content enrichment scripts
├── archive/                    # Archived/legacy scripts
└── {fec,jmail,misc}/           # Specialized subdirectories
```

## Data Sources

### Government Datasets (NEW - April 2026)

| Dataset | Source | Status | Records | Scripts |
|---------|--------|--------|---------|---------|
| **FEC Individual Contributions** | FEC.gov | ✅ Imported | 447M | `download_fec_2024.py`, `import_fec.py` |
| **GovInfo Federal Register** | GovInfo.gov | 🔄 Downloading | ~300K | `download_govinfo_bulk.py`, `import_govinfo.py` |
| **Congressional Bills** | Congress.gov | 🔄 Downloading | ~20K | `download_congress.py`, `import_congress.py` |
| **Court Opinions** | GovInfo.gov | 🔄 Downloading | ~50K | `download_govinfo_bulk.py`, `import_govinfo.py` |
| **FARA Registrations** | DOJ FARA | 🔄 Downloading | ~5K | `download_fara_bulk.py`, `import_fara.py` |
| **Lobbying Disclosure** | Senate LDA | 🔄 Downloading | ~200K | `download_lobbying.py`, `import_lobbying.py` |
| **FEC Candidates/Committees** | FEC.gov | 🔄 Downloading | ~30K | `download_fec_committees.py`, `import_fec.py` |
| **Financial Disclosures** | House/Senate | 🔄 Downloading | ~2K | `download_financial_disclosures.py`, `import_financial.py` |
| **White House Visitors** | White House | ✅ Sample | 8 | `download_whitehouse.py`, `import_whitehouse.py` |
| **SEC EDGAR** | SEC.gov | ✅ Placeholders | - | `download_sec_edgar.py`, `import_sec_edgar.py` |
| **USA Spending** | USASpending.gov | ✅ Sample | 100 | `download_usa_spending.py`, `import_usa_spending.py` |

### Cross-Reference Queries

Link entities across all datasets:

```sql
-- Politicians with lobbying + campaign finance + foreign representation
SELECT * FROM cross_ref_politicians WHERE politician_name ILIKE '%schumer%';

-- Foreign influence through lobbying
SELECT * FROM cross_ref_lobbyist_foreign_agents WHERE fara_country = 'Saudi Arabia';

-- Money flow: contributor → politician → lobbying
SELECT * FROM cross_ref_money_flow WHERE contributor_name ILIKE '%goldman%';
```

**Full query set**: `cross_reference_queries.sql`

### 1. DOJ Epstein Library
- **Source**: https://www.justice.gov/epstein-library
- **Type**: Official Government Documents
- **License**: Public Domain
- **Status**: ✅ Complete (260K+ PDFs downloaded)
- **Size**: 19.8 GB
- **Scripts**: `download/doj_epstein_library.py`, `import/doj_epstein_library.py`

### 2. jMail World Emails
- **Source**: https://jmail.world
- **Type**: Email Archive
- **License**: Public Records
- **Status**: ✅ Complete (1.78M emails + 1.41M documents)
- **Size**: 344 MB total
- **Scripts**: `download/jmail_world.py`, `import/jmail_world.py`

### 3. GDELT News Articles
- **Source**: http://data.gdeltproject.org/gdeltv2/
- **Type**: Global Knowledge Graph (GKG) 2.0
- **License**: Research Use
- **Status**: ✅ Active (23,413+ articles)
- **Coverage**: February 2015 - Present
- **Scripts**: `download/gdelt_news.py`, `import/gdelt_news.py`

### 4. ICIJ Offshore Leaks
- **Source**: https://offshoreleaks-data.icij.org/
- **Type**: Financial Data / Offshore Entities
- **License**: Open Database License (ODbL)
- **Status**: ✅ Complete (3.3M relationships imported)
- **Size**: ~600 MB extracted
- **Scripts**: `download/icij_offshore_leaks.py`, `import/icij_offshore_leaks.py`

### 5. HuggingFace Datasets
- **Source**: https://huggingface.co/datasets
- **Type**: Community Curated Collections
- **License**: Various (check per dataset)
- **Status**: ✅ 4M+ RECORDS INGESTED (April 13, 2026)
- **Scripts**: `download/huggingface_datasets.py`, `import/huggingface_datasets.py`

### 6. Third-Party GitHub Repositories
- **Source**: Various GitHub repositories
- **Type**: Community curated data and knowledge graphs
- **License**: Various Open Source
- **Status**: 🔴 Not Yet Ingested (10K+ nodes available)
- **Scripts**: `download/third_party_repos.py`, `import/third_party_repos.py`

## Workflow

### 1. Download Phase
```bash
# Download specific dataset
python3 download/doj_epstein_library.py --dataset data1

# Download all datasets
python3 download/doj_epstein_library.py --all

# Resume interrupted download
python3 download/doj_epstein_library.py --dataset data1 --resume
```

### 2. Import Phase
```bash
# Import downloaded data
python3 import/doj_epstein_library.py --dataset data1

# Import all datasets
python3 import/doj_epstein_library.py --all

# Import with validation
python3 import/doj_epstein_library.py --dataset data1 --validate
```

### 3. Processing Phase
```bash
# Run full processing pipeline
python3 processing/full_processing_pipeline.py

# Run specific processing steps
python3 processing/ocr_processing.py --dataset data1
python3 processing/entity_extraction.py --dataset data1
```

### 4. Enrichment Phase
```bash
# Enrich content with Trafilatura
python3 enrichment/news_enrichment.py --source gdelt

# Cross-reference entities
python3 enrichment/cross_reference.py --source doj
```

## Quality Control

### Data Validation
```bash
# Run data quality checks
python3 utils/data_quality_validator.py

# Check database integrity
python3 utils/db_integrity.py

# Generate quality metrics
python3 utils/metrics.py
```

### Progress Tracking
```bash
# Monitor progress
python3 utils/tracker.py watch

# Register new task
python3 utils/tracker.py register --id raw-ds1 --label "Dataset 1" --expected 15000

# Update progress
python3 utils/tracker.py update --id raw-ds1 --current 3200
```

## Configuration

All scripts use centralized configuration from `scripts/utils/epstein_config.py`:

```python
from scripts.utils.epstein_config import (
    DATA_ROOT, RAW_FILES_DIR, DATABASES_DIR,
    get_dataset_path, resolve_path
)
```

## License

All scripts are licensed under the MIT License unless otherwise specified in individual files.

## Contributing

1. Follow the existing code style and patterns
2. Add proper error handling and logging
3. Include validation and quality checks
4. Update documentation for new features
5. Test thoroughly before committing
