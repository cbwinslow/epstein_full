# Epstein Files - Comprehensive Data Inventory

> **Last Updated:** April 10, 2026  
> **Purpose:** Master inventory of all data sources, their provenance, size, and ingestion status

---

## 📊 Executive Summary

| Category | Records | Size | Status |
|----------|---------|------|--------|
| **Primary Documents** | 1.4M | 20+ GB | ✅ Complete |
| **News Articles** | 23,413+ | - | ✅ Active Collection |
| **Emails** | 1.78M | 319 MB | ✅ Complete |
| **Financial Data** | 5.4M+ | - | ✅ Complete |
| **Knowledge Graph** | 3.3M relations | - | ✅ Complete |
| **Offshore Leaks** | 814K entities | 600 MB | ✅ Complete |
| **HuggingFace Datasets** | 2.1M+ | ~2 GB | ✅ Downloaded (Need Ingestion) |

---

## 📁 Data Sources Catalog

### 1. DOJ Epstein Library (Primary Source)

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **EFTA Documents** | 1,417,869 | 20+ GB | 1991-2025 | https://www.justice.gov/epstein-library | ✅ Complete |
| **Raw Files (data1-12)** | 260,000+ PDFs | 19.8 GB | All years | DOJ | ✅ Downloaded |
| **Images** | 38,000+ | - | All years | PDF extraction | ✅ Cataloged |

**Files:**
- Location: `/home/cbwinslow/workspace/epstein-data/raw-files/data{1-12}/`
- Catalog: `epstein-research-data/image_catalog.csv.gz`
- Key files: Black Book, Flight Logs, Emails, Court documents

**Ingestion:**
- Tool: `epstein-ripper/auto_ep_rip.py`
- Method: Playwright browser automation
- Status: All datasets downloaded

---

### 2. jMail World Emails

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **Emails** | 1,783,792 | 319 MB | 1990-2026 | https://jmail.world | ✅ Complete |
| **Documents** | 1,413,417 | 25 MB | 1990-2026 | jmail API | ✅ Complete |

**Files:**
- Location: `/home/cbwinslow/workspace/epstein-data/downloads/`
- Files: `jmail_emails_full.parquet`, `jmail_documents.parquet`

**PostgreSQL Tables:**
- `jmail_emails_full` - 1.78M emails with metadata
- `jmail_documents` - 1.41M document records

**Ingestion:**
- Script: `scripts/import_jmail_full.py`
- Script: `scripts/import_jmail_documents.py`
- Date: April 4, 2026
- Performance: Zero errors, ~5 hours total

---

### 3. GDELT News Articles

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **News Articles** | 23,413+ | - | Feb 2015-Present | http://data.gdeltproject.org/gdeltv2/ | ✅ Active |

**Coverage:**
- **2019-07-06**: 2,874 articles (Arrest day peak)
- **2019-07-10**: 2,768 articles (Breaking news)
- **2024-01-04**: 2,601 articles (Document release)
- **2024-2025**: ~2,000 articles (Recent civil suits)

**PostgreSQL Table:**
- `media_news_articles` - 23,413+ articles with entity metadata

**Pipeline:**
- Script: `epstein-pipeline/gdelt_ingestion_pipeline.py`
- Script: `epstein-pipeline/gdelt_parallel_swarm.py`
- Method: GKG 2.0 15-minute slices
- Entities: Persons, organizations, locations, themes
- Last Run: April 10, 2026

**⚠️ Limitation:** GDELT started Feb 2015. Pre-2015 era (9/11, early Wexner) NOT covered.

---

### 4. ICIJ Offshore Leaks

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **Entities** | 814,344 | 190 MB | 1970s-2020s | https://offshoreleaks-data.icij.org/ | ✅ Complete |
| **Officers** | 1.8M | 87 MB | All years | ICIJ | ✅ Complete |
| **Relationships** | 3,339,272 | 247 MB | All years | ICIJ | ✅ Complete |
| **Addresses** | 700,000 | 69 MB | All years | ICIJ | ✅ Complete |

**Coverage:**
- Panama Papers (2016)
- Paradise Papers (2017)
- Pandora Papers (2021)
- Bahamas Leaks (2016)
- Offshore Leaks (2013)

**PostgreSQL Tables:**
- `icij_entities`
- `icij_officers`
- `icij_addresses`
- `icij_intermediaries`
- `icij_others`
- `icij_relationships`

**Ingestion:**
- Script: `scripts/import_icij.py`
- Date: April 4, 2026
- License: Open Database License (ODbL)

---

### 5. FEC Campaign Contributions

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **Individual Contributions** | 5,420,940+ | - | 1999-2026 | https://www.fec.gov/data/ | ✅ Complete |

**PostgreSQL Table:**
- `fec_individual_contributions`

**Coverage:**
- Epstein network political donations
- Related entity contributions
- Financial influence mapping

---

### 6. FBI Vault

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **Documents** | 22 | 1,344 pages | Various | https://vault.fbi.gov/ | ✅ Available |

**Coverage:**
- FBI investigations
- Field office reports
- Released under FOIA

---

### 7. Third-Party Knowledge Graphs

#### dleerdefi/epstein-network-data
**Source:** https://github.com/dleerdefi/epstein-network-data

| Dataset | Records | Size | Status |
|---------|---------|------|--------|
| **Birthday Book** | 128 pages | ~244 MB | ✅ Available |
| **Black Book** | 1,252 contacts | ~79 MB | ✅ Available |
| **Flight Logs** | 118 pages (1991-2019) | ~797 MB | ✅ Available |
| **Neo4j Nodes** | 10,356 | - | ✅ Available |
| **Neo4j Relations** | 16,625+ | - | ✅ Available |

**Key Data:**
- **Persons:** 2,541 canonical persons
- **Flights:** 2,051 flight records
- **Airports:** 283 with IATA/ICAO codes
- **Phone Numbers:** 3,676 with geocoding
- **Email Addresses:** 385
- **Addresses:** 1,192 with lat/lon

**Files:**
- Location: Can be cloned from GitHub
- Format: CSV, JSON, PNG (scanned pages)
- License: Open source

---

### 8. HuggingFace Datasets

| Dataset | Records | Source | URL | Status |
|---------|---------|--------|-----|--------|
| **FULL_EPSTEIN_INDEX** | ~20,000 pages | House Oversight + DOJ | `thelde/remo/FULL_EPSTEIN_INDEX` | 🔍 Available |
| **epstein-files-20k** | 2,136,420 docs | House Oversight | `teyler/epstein-files-20k` | ✅ **INGESTED** |
| **epstein-data (v2.0)** | CC data | DOJ | `kabasshouse/epstein-data` | 🔍 Available |
| **epstein-emails** | 5,082 threads | House Oversight | `notesbymuneeb/epstein-emails` | 🔍 Available |
| **EPSTEIN_FILES_20K** | OCR + embeddings | House Oversight | `tensonaut/EPSTEIN_FILES_20K` | 🔍 Available |
| **epstein-fbi-files** | FBI docs | FBI Vault | `svetfm/epstein-fbi-files` | 🔍 Available |

**Download & Ingest Status:**
- **epstein-files-20k:** ✅ **COMPLETE & INGESTED**
  - Downloaded: 2,136,420 records (126.76 MB)
  - Table: `hf_epstein_files_20k` (2,136,420 rows)
  - Location: `/home/cbwinslow/workspace/epstein-data/huggingface/epstein_files_20k/`
  - Scripts: `download_hf_resume.py`, `import_hf_epstein_files_20k.py`

**✅ INGESTED - Next: Remaining datasets**

---

## 📈 Coverage Gaps

### Pre-2015 Era (9/11, Early Wexner)

| Era | Timeframe | Coverage | Solution |
|-----|-----------|----------|----------|
| **Wexner Money Mgmt** | 1999-2006 | ❌ None | Need court filings |
| **9/11 Connections** | 2001-2002 | ❌ None | Need FOIA requests |
| **First Investigation** | 2005-2008 | ⚠️ Limited | Palm Beach PD records |
| **Acosta Era** | 2008-2019 | ⚠️ Limited | Case file 09-347 |

**Alternative Sources Needed:**
- CourtListener RECAP for pre-2015 filings
- Wayback Machine for archived news
- LexisNexis (if available)
- Physical document requests

---

## 🔄 Ingestion Pipeline Status

### Active Pipelines

| Pipeline | Script | Status | Last Run | Records |
|----------|--------|--------|----------|---------|
| GDELT Swarm | `gdelt_parallel_swarm.py` | 🟡 Running | 2025-04-10 | 23,413+ |
| DOJ Ripper | `epstein-ripper/auto_ep_rip.py` | ✅ Complete | 2025-03 | 1.4M |
| jMail Import | `scripts/import_jmail_*.py` | ✅ Complete | 2025-04-04 | 3.2M |
| ICIJ Import | `scripts/import_icij.py` | ✅ Complete | 2025-04-04 | 3.3M |
| FEC Import | `scripts/import_fec.py` | ✅ Complete | 2025-03 | 5.4M |
| Black Book Import | `scripts/import_black_book_json.py` | ✅ Complete | 2025-04-11 | 2,327 contacts |
| Flight Logs Import | `scripts/import_flight_logs.py` | ✅ Complete | 2025-04-11 | 85 names |
| Neo4j Graph Import | `scripts/import_neo4j_graph.py` | ✅ Complete | 2025-04-11 | 383 nodes, 534 rels |

### Pending Pipelines

| Pipeline | Source | Records | Priority |
|----------|--------|---------|----------|
| HuggingFace epstein-files-20k | HuggingFace | 2.1M docs (Need Ingestion) | High |
| House Oversight 2024 (FULL_EPSTEIN_INDEX) | HuggingFace | ~20,000 | High |
| Black Book | GitHub/dleerdefi | 2,327 contacts ✅ Ingested | High |
| Flight Logs | GitHub/dleerdefi | 85 names, flights parsed ✅ Ingested | High |
| Birthday Book | GitHub/dleerdefi | 128 pages | Medium |
| Neo4j Graph Import | GitHub/dleerdefi | 383 nodes, 534 relationships ✅ Ingested | High |

---

## 📂 File Locations

### Primary Storage

```
/home/cbwinslow/workspace/epstein-data/
├── raw-files/
│   ├── data1-12/           # DOJ EFTA documents (260K PDFs, 19.8 GB)
│   └── fec/                # FEC data
├── downloads/
│   ├── jmail_emails_full.parquet      (319 MB, 1.78M records)
│   ├── jmail_documents.parquet        (25 MB, 1.41M records)
│   ├── icij_extracted/                (600 MB, 3.3M relations)
│   └── gdelt/                         # Raw GKG slices
├── databases/
│   ├── full_text_corpus.db            (7 GB, 1.4M docs)
│   ├── redaction_analysis_v2.db       (940 MB, 2.59M redactions)
│   ├── knowledge_graph.db               (892 KB, 606 entities)
│   └── ...
└── processed/
    ├── ocr_output/         # Extracted text
    ├── entities/           # NER extractions
    └── embeddings/         # Vector embeddings
```

### Project Code

```
/home/cbwinslow/workspace/epstein/
├── epstein-ripper/         # DOJ download automation
├── epstein-pipeline/       # Processing pipelines
│   ├── gdelt_ingestion_pipeline.py
│   └── gdelt_parallel_swarm.py
├── Epstein-research-data/  # Analysis outputs
│   ├── knowledge_graph_entities.json
│   └── tools/              # Helper scripts
├── scripts/                # Import scripts
└── media_acquisition/      # Media agents
```

---

## 🔗 External References

### Comparison Sites

| Site | URL | Purpose |
|------|-----|---------|
| epsteinexposed.com | https://epsteinexposed.com | Document browser |
| jmail.world | https://jmail.world | Email archive |
| DOJ Library | https://www.justice.gov/epstein-library | Official source |
| ICIJ | https://offshoreleaks-data.icij.org | Financial data |

### GitHub Repositories

| Repo | URL | Purpose |
|------|-----|---------|
| epstein-network-data | dleerdefi/epstein-network-data | Knowledge graph |
| epsteinbase | white-roz3/epsteinbase | DOJ ingestion |
| epstein-pipeline | (local) | Our processing pipeline |

### HuggingFace Datasets

| Dataset | URL | Records |
|---------|-----|---------|
| FULL_EPSTEIN_INDEX | thelde/remo/FULL_EPSTEIN_INDEX | ~20K pages |
| epstein-files-20k | teyler/epstein-files-20k | 20K docs |
| epstein-fbi-files | svetfm/epstein-fbi-files | FBI docs |

---

## 📋 Next Steps

### Immediate (This Week)

1. ✅ **Ingest House Oversight 2024 documents** from HuggingFace
2. ✅ **Import Black Book + Flight Logs** from dleerdefi repo
3. ✅ **Import Neo4j knowledge graph** (10K nodes, 16K relations)

### Short Term (This Month)

4. 📌 **Pre-2015 coverage** - CourtListener RECAP for 1999-2014
5. 📌 **Birthday Book** - 128 pages manual/OCR extraction
6. 📌 **Image analysis** - 38K images from PDFs

### Long Term (This Quarter)

7. 📌 **Entity deduplication** across all sources
8. 📌 **Master knowledge graph** combining all datasets
9. 📌 **Embeddings** for 100% of documents

---

## 📚 License Summary

| Source | License | Commercial Use |
|--------|---------|----------------|
| DOJ Documents | Public Domain | ✅ Yes |
| jMail | Public Records | ✅ Yes |
| GDELT | Research Use | ✅ Yes |
| ICIJ | ODbL | ✅ Yes |
| FEC | Public Domain | ✅ Yes |
| FBI Vault | Released Records | ✅ Yes |
| GitHub Repos | Various Open | ✅ Yes |

---

## 📝 Notes

- **GDELT Limitation:** No news before Feb 2015 (entity extraction started then)
- **9/11 Era:** Need alternative sources (court filings, archived news)
- **Wexner Money:** Need financial records from 1999-2006 (not in GDELT)
- **Coverage:** Post-2015 is comprehensive; pre-2015 requires targeted collection

---

*Generated: April 10, 2026*  
*Maintained by: Research Team*
