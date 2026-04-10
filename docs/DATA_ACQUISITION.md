# Data Acquisition Methods Documentation

> **Document Version:** 1.0  
> **Last Updated:** April 4, 2026  
> **Purpose:** Document all data acquisition techniques for reproducibility and research transparency

---

## Table of Contents

1. [Overview](#overview)
2. [Data Sources](#data-sources)
3. [Acquisition Scripts](#acquisition-scripts)
4. [Methodology](#methodology)
5. [Storage & Organization](#storage--organization)
6. [Quality Assurance](#quality-assurance)
7. [Reproducibility](#reproducibility)

---

## Overview

This project uses a **multi-source data acquisition strategy** combining:
- **Public government datasets** (DOJ, FEC, FBI)
- **Investigative journalism databases** (ICIJ Offshore Leaks)
- **Scraped web data** (epsteinexposed.com, jmail.world)
- **Academic/NGO repositories** (HuggingFace datasets)

All acquisition methods follow **industry best practices**:
- Respect rate limits
- Document provenance
- Verify data integrity
- Enable reproducibility

---

## Data Sources

### 1. DOJ EFTA Datasets (Primary)

**Source:** https://www.justice.gov/epstein-epstein-grand-jury-documents  
**Method:** Automated browser-based download (Playwright)  
**Total Files:** 1,313,861 PDFs (177GB)  
**Coverage:** 94% of 1.4M EFTA numbers

**Acquisition Steps:**
```bash
# Use epstein-ripper submodule
python3 epstein-ripper/auto_ep_rip.py --dataset N

# Verify downloads
find /home/cbwinslow/workspace/epstein-data/raw-files/ -name "*.pdf" | wc -l
```

**Script:** `scripts/download_doj_efta.py`

---

### 2. FEC Campaign Finance Data

**Source:** https://www.fec.gov/data/browse-data/?tab=bulk-data  
**Method:** Bulk file download via `wget` / `curl`  
**Total Records:** 5,420,940+ individual contributions  
**Coverage:** 1980-2026 (23 election cycles)

**Acquisition Steps:**
```bash
# Download bulk files
for year in {1980..2026}; do
  wget -P /home/cbwinslow/workspace/epstein-data/raw-files/fec/ \
    "https://www.fec.gov/files/bulk-downloads/${year}/indiv${year: -2}.zip"
done

# Extract and process
python3 scripts/download_fec_bulk.py
```

**Script:** `scripts/download_fec_bulk.py`

**File Types Downloaded:**
- `indiv*.zip` - Individual contributions (23 cycles)
- `cm*.zip` - Committee master
- `cn*.zip` - Candidate master
- `ccl*.zip` - Candidate-committee linkage

---

### 3. ICIJ Offshore Leaks

**Source:** https://offshoreleaks-data.icij.org/  
**Method:** Direct zip download + extraction  
**Size:** 69.7 MB (compressed), ~600 MB extracted  
**License:** Open Database License (ODbL)

**Acquisition Steps:**
```bash
# Download full database
curl -o /home/cbwinslow/workspace/epstein-data/downloads/icij_offshore_leaks.zip \
  "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip"

# Extract
unzip icij_offshore_leaks.zip -d icij_extracted/

# Import to PostgreSQL
python3 scripts/import_icij.py
```

**Script:** `scripts/download_jmail_icij.py`

**Coverage:**
- Panama Papers (2016): 11.5M documents
- Paradise Papers (2017): 13.4M documents  
- Pandora Papers (2021): 11.9M documents
- Bahamas Leaks (2016): 1.3M documents
- Offshore Leaks (2013): Original records

---

### 4. jmail.world Email Data

**Source:** https://jmail.world/  
**API Endpoint:** `https://data.jmail.world/v1/emails-slim.parquet`  
**Method:** Direct parquet download  
**Size:** 38.8 MB (1.78M emails)

**Acquisition Steps:**
```bash
# Download emails
curl -o /home/cbwinslow/workspace/epstein-data/downloads/jmail_emails_full.parquet \
  "https://data.jmail.world/v1/emails-slim.parquet"

# Download documents
curl -o /home/cbwinslow/workspace/epstein-data/downloads/jmail_documents.parquet \
  "https://data.jmail.world/v1/documents.parquet"

# Import to PostgreSQL
python3 scripts/import_jmail_full.py
python3 scripts/import_jmail_documents.py
```

**Script:** `scripts/download_jmail_icij.py`

**Sources in Dataset:**
- VOL00009-12 (DOJ EFTA): 1,756,912 emails
- yahoo_2 (Epstein's Yahoo): 17,448 emails
- House Oversight: 8,374 emails
- Ehud Barak: 1,058 emails

---

### 5. HuggingFace Datasets

**Source:** https://huggingface.co/datasets  
**Method:** Direct download via CDN (aria2c)  
**Datasets:** 4 HuggingFace datasets (395,995 records)

**Acquisition Steps:**
```bash
# Use aria2c for faster parallel downloads
aria2c -x 16 -s 16 -d /home/cbwinslow/workspace/epstein-data/hf-parquet/ \
  "https://huggingface.co/datasets/AfricanKillshot/Epstein-Files/resolve/main/train-00000-of-00634.parquet"

# Import scripts
python3 scripts/import_fbi_embeddings.py
python3 scripts/import_house_oversight_embeddings.py
```

**Datasets Downloaded:**
| Dataset | Records | Size |
|---------|---------|------|
| `svetfm/epstein-fbi-files` | 236,174 | 3.9 GB |
| `svetfm/epstein-files-nov11-25` | 69,290 | 341 MB |
| `theelderemo/FULL_EPSTEIN_INDEX` | 8,531 | 3.2 MB |
| `AfricanKillshot/Epstein-Files` | ~2.87M | 318 GB |

---

### 6. epsteinexposed.com Scraping

**Source:** https://epsteinexposed.com/api/v2  
**Method:** REST API calls (respecting rate limits)  
**Rate Limit:** 100 req/hr anonymous, 1,000 req/hr with key

**Acquisition Steps:**
```bash
# Request API key from epsteinexposed.com
# Then scrape with proper headers
python3 scripts/scrape_epstein_exposed.py

# Or use bulk export endpoints (no rate limit)
curl "https://epsteinexposed.com/api/v2/export/persons" -o epstein_exposed_persons.json
```

**Bulk Export Endpoints (FREE):**
- `/export/persons` - 1,578 records ✅
- `/export/flights` - 3,615 records ✅
- `/export/locations` - 83 records ✅
- `/export/organizations` - 55 records ✅

---

## Acquisition Scripts

### Script Inventory

| Script | Purpose | Reproducibility |
|--------|---------|-----------------|
| `scripts/download_doj_efta.py` | DOJ PDF downloads | ✅ Fully automated |
| `scripts/download_fec_bulk.py` | FEC bulk data | ✅ Fully automated |
| `scripts/download_jmail_icij.py` | jMail + ICIJ data | ✅ Fully automated |
| `scripts/import_icij.py` | ICIJ to PostgreSQL | ✅ Fully automated |
| `scripts/import_jmail_full.py` | jMail to PostgreSQL | ✅ Fully automated |
| `scripts/import_fbi_embeddings.py` | FBI embeddings | ✅ Fully automated |
| `scripts/import_house_oversight.py` | House Oversight data | ✅ Fully automated |
| `scripts/scrape_epstein_exposed.py` | Web scraping | ⚠️ Rate limited |

### Standardized Import Pattern

All import scripts follow this pattern:

```python
"""
Reusable Import Script Template

Usage: python import_dataset.py --input <path> --batch-size <n>
"""

import psycopg2
import pandas as pd
from pathlib import Path

# Configuration
BATCH_SIZE = 5000
CONFLICT_STRATEGY = "ON CONFLICT DO NOTHING"

# Connection
DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

def import_data(input_path: str, table_name: str):
    """
    Standardized import with:
    - Batch processing
    - Progress tracking
    - Conflict handling
    - Error logging
    """
    # Implementation...
    pass

if __name__ == "__main__":
    import_data(args.input, args.table)
```

---

## Methodology

### Data Acquisition Principles

1. **Provenance Tracking**
   - Source URL documented
   - Download timestamp recorded
   - SHA-256 checksums calculated
   - Original filenames preserved

2. **Rate Limiting**
   - Respect robots.txt
   - Add delays between requests
   - Use appropriate User-Agent headers
   - Cache results to avoid re-download

3. **Data Integrity**
   - Verify file signatures (PDF, ZIP)
   - Check row counts match expected
   - Validate schema compatibility
   - Test imports in transaction blocks

4. **Reproducibility**
   - All scripts version controlled
   - Dependencies documented
   - Configuration externalized
   - Logs maintained for audits

### Storage Organization

```
/home/cbwinslow/workspace/epstein-data/
├── raw-files/
│   ├── data1-12/           # DOJ EFTA PDFs
│   ├── fec/                # FEC bulk downloads
│   └── fbi-vault/          # FBI Vault PDFs
├── hf-parquet/
│   └── *.parquet           # HuggingFace datasets
├── databases/
│   └── *.db                # SQLite sources
├── downloads/
│   ├── jmail_*.parquet     # jMail data
│   └── icij_*.csv          # ICIJ extracted
├── supplementary/
│   └── *.json              # Scraped data
└── logs/
    └── *.log               # Download/processing logs
```

---

## Quality Assurance

### Validation Checks

1. **Row Count Validation**
   ```sql
   SELECT 'documents' as table_name, COUNT(*) as row_count 
   FROM documents 
   HAVING COUNT(*) BETWEEN 1390000 AND 1400000;
   ```

2. **Checksum Validation**
   ```bash
   # Verify file integrity
   sha256sum -c checksums.sha256
   ```

3. **Schema Validation**
   ```python
   # Verify columns match expected
   assert set(df.columns) == EXPECTED_COLUMNS
   ```

4. **Referential Integrity**
   ```sql
   -- Check for orphaned records
   SELECT * FROM pages p
   LEFT JOIN documents d ON p.document_id = d.id
   WHERE d.id IS NULL;
   ```

---

## Reproducibility

### To Reproduce This Dataset:

1. **Clone Repository**
   ```bash
   git clone --recurse-submodules https://github.com/cbwinslow/epstein.git
   cd epstein
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # or
   uv pip install -r requirements.txt
   ```

3. **Set Up Storage**
   ```bash
   # Ensure /home/cbwinslow/workspace/epstein-data/ is mounted
   # Requires 3TB available space
   ```

4. **Run Acquisition Scripts**
   ```bash
   # In order of dependency
   python3 scripts/download_doj_efta.py --all
   python3 scripts/download_fec_bulk.py --all
   python3 scripts/download_jmail_icij.py
   python3 scripts/download_hf_datasets.py
   ```

5. **Import to PostgreSQL**
   ```bash
   # Run all import scripts
   for script in scripts/import_*.py; do
     python3 "$script"
   done
   ```

6. **Verify Installation**
   ```bash
   # Check views
   psql -c "SELECT * FROM v_dataset_completeness;"
   ```

---

## Citation

When using this data, cite as:

```
Epstein Files Analysis Database (2026).
Data aggregated from DOJ EFTA releases, FEC.gov, ICIJ Offshore Leaks,
jmail.world, and HuggingFace community datasets.
Repository: https://github.com/cbwinslow/epstein
```

---

## License Compliance

| Data Source | License | Usage Rights |
|-------------|---------|--------------|
| DOJ EFTA | Public Domain | ✅ Free use |
| FEC.gov | Public Domain | ✅ Free use |
| ICIJ | ODbL | ✅ ShareAlike |
| jMail.world | Unknown | ⚠️ Research only |
| HF Datasets | Apache 2.0 / MIT | ✅ Free use |

---

*This document is maintained as part of the Epstein Files Analysis project.*
