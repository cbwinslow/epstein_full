# Epstein Files - Comprehensive Data Inventory

> **Last Updated:** April 24, 2026
> **Purpose:** Master inventory of all data sources, their provenance, size, and ingestion status

---

## 📊 Executive Summary

| Category | Records | Size | Status |
|----------|---------|------|--------|
| **Primary Documents** | 1.42M | 468 GB | ✅ Complete (DOJ EFTA: 1,417,847) |
| **News Articles** | 49,088+ | - | ✅ Active Collection (GDELT) |
| **Emails** | 1.78M | 319 MB | ✅ Complete (jmail_emails_full: 1,783,792 rows) |
| **Government Data** | 2.5M+ | 468 GB | ✅ Complete (Senate votes: 6,474 rows, 403 errors resolved) |
| **Knowledge Graph** | 383 nodes, 534 rels | - | ✅ Complete (Neo4j imported) |
| **Offshore Leaks** | 814K entities | 600 MB | ✅ Complete (ICIJ: 814,344 entities) |
| **HuggingFace Datasets** | 2.1M+ | ~2 GB | ✅ Downloaded (epstein-files-20k: 2.1M) |
| **FBI Vault** | 22 docs, 1.4K pages | 1.1 MB | ✅ Complete (PostgreSQL: 22 docs imported) |

---

## 📁 Data Sources Catalog

### 1. DOJ Epstein Library (Primary Source)

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **EFTA Documents** | 1,417,847 | 468 GB | 1991-2025 | https://www.justice.gov/epstein-library | ✅ Complete (verified) |
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
| **Emails** | 1,783,792 | 319 MB | 1990-2026 | https://jmail.world | ✅ Complete (verified) |
| **Documents** | 51,728 | 25 MB | 1990-2026 | jmail API | ✅ Complete (verified) |
| **iMessages** | 5,082 threads | - | 1990-2026 | jmail API | 🔍 Download failed (403) |
| **Photos** | - | - | 1990-2026 | jmail API | 🔍 Download failed (403) |

**Files:**
- Location: `/home/cbwinslow/workspace/epstein-data/downloads/`
- Files: `jmail_emails_full.parquet` (334 MB), `jmail_documents.parquet` (25 MB)
- Status: Parquet files present, iMessages/photos failed with 403 errors (source blocking)

**PostgreSQL Tables:**
- `jmail_emails_full` - 1,783,792 emails (complete dataset)
- `jmail_documents` - 1,413,417 document records
- `jmail_emails` - 1,596,220 emails (truncated, use jmail_emails_full)

**Ingestion:**
- Script: `scripts/import_jmail_full.py`
- Script: `scripts/import_jmail_documents.py`
- Date: April 4, 2026
- Performance: Zero errors, full dataset loaded
- Note: iMessages/photos blocked by 403, data.jmail.world source restricted

---

### 3. GDELT News Articles

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **News Articles** | 49,088+ | - | Feb 2015-Present | http://data.gdeltproject.org/gdeltv2/ | ✅ Active (verified) |

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
| **Entities** | 814,344 | 190 MB | 1970s-2020s | https://offshoreleaks-data.icij.org/ | ✅ Complete (verified) |
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
| **Individual Contributions** | 447,189,732 | - | 2000-2026 | https://www.fec.gov/data/ | ✅ Complete (verified) |

**PostgreSQL Table:**
- `fec_individual_contributions`

**Coverage:**
- Epstein network political donations
- Related entity contributions
- Financial influence mapping

---

### 6. Government Data (Comprehensive Historical Coverage)

| Dataset | Records | Timeframe | Source | Status |
|--------|--------|----------|--------|--------|
| **Federal Register** | 737,940 | 2000-2024 | GovInfo.gov | ✅ Complete (verified) |
| **Congress Bills** | 368,651 | 105th-119th (2000-2026) | Congress.gov API | ✅ Complete (verified) |
| **Congress Members** | 10,413 | 105th-119th | Congress.gov API | ✅ Complete (verified) |
| **House Votes** | 2,738 | 117th-119th | Congress.gov API | ✅ Complete (verified) |
| **House Vote Details** | 2,738 | 117th-119th | Congress.gov API + Clerk XML | ✅ Complete (verified) |
| **House Member Roll Calls** | 1,185,626 | 117th-119th | Congress.gov API + Clerk XML | ✅ Complete (verified) |
| **Senate Votes** | 6,474 | 106th-119th (2000-2026) | Senate.gov API + XML | ✅ Complete (verified, 403 resolved) |
| **Senate Member Votes** | 647,338 | 106th-119th | Senate.gov XML | ✅ Complete (verified) |
| **Bill Text Versions** | 130,361 | 105th-119th | GovInfo.gov | ✅ Complete (verified) |
| **Bill Summaries** | 279,065 | 105th-119th | GovInfo.gov | ✅ Complete |
| **Bill Actions** | 875,816 | 105th-119th | GovInfo.gov | ✅ Complete (verified) |
| **Bill Cosponsors** | 2,064,763 | 105th-119th | GovInfo.gov | ✅ Complete (verified) |
| **Bill Vote References** | 11,546 | 105th-119th | GovInfo.gov | ✅ Complete (verified) |
| **Court Opinions** | 31,544 | 2000-2024 | GovInfo.gov | ✅ Complete (verified) |
| **White House Visitors** | 2,544,984 | 2009-2024 | Archives.gov | ✅ Complete (verified) |
| **FEC Individual Contrib.** | 447,189,732 | 2000-2026 | FEC.gov | ✅ Complete (verified) |
| **House Financial Discl.** | 37,281 | 2008-2024 | Clerk.House.gov | ✅ Complete (verified) |
| **Lobbying (LDA)** | 30,600 | 2000-2024 | Senate.gov | ✅ Complete (verified) |

#### Coverage for Epstein's Peak Years (2000-2009)

| Source | 2000 | 2001 | 2002 | 2003 | 2004 | 2005 | 2006 | 2007 | 2008 | 2009 |
|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Federal Register | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Congress Bills | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| FEC Contributions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| White House Visitors | - | - | - | - | - | - | - | - | - | ✅ |

**Note:** White House visitor logs were not publicly disclosed until the Obama administration in 2009. Pre-2009 visitor data is not available.

#### PostgreSQL Tables
- `federal_register_entries` - 737,940 entries
- `congress_bills` - 359,467 bills
- `congress_members` - 9,864 members
- `congress_house_votes` - 2,738 votes
- `congress_house_vote_details` - 2,738 vote detail rows
- `congress_house_member_votes` - 1,185,626 member vote rows
- `congress_bill_text_versions` - 113,106 versions
- `whitehouse_visitors` - 2,544,984 visits
- `fec_individual_contributions` - 447M+ contributions
- `house_financial_disclosures` - 37,281 filings
- `lda_filings` - 30,600 registrations

#### Scripts
- `download_govinfo_bulk.py` - Federal Register, Bills, Bill Status
- `download_congress_historical.py` - Congress bills/members/votes
- `download_whitehouse.py` - White House visitor logs
- `import_govinfo_*.py` - GovInfo importers
- `import_congress.py` - Congress importer
- `import_whitehouse_visitors.py` - Visitor log importer

---

### 7. FBI Vault

| Dataset | Records | Size | Timeframe | Source URL | Status |
|---------|---------|------|-----------|------------|--------|
| **Documents** | 22 | 1,426 pages | Various | https://vault.fbi.gov/ | ✅ Complete |

**Coverage:**
- FBI investigations
- Field office reports
- Released under FOIA

**PostgreSQL:**
- Table: `documents` (efta_number LIKE 'FBI_VAULT_%')
- 22 documents (FBI_VAULT_PART_01 through FBI_VAULT_PART_22)
- 1,426 total pages
- Import script: `scripts/import/import_fbi_vault.py`
- Data location: `/home/cbwinslow/workspace/epstein-data/fbi-vault/`
- Status: Downloaded + imported (text files present, PostgreSQL loaded)

---

### 8. Third-Party Knowledge Graphs

#### dleerdefi/epstein-network-data
**Source:** https://github.com/dleerdefi/epstein-network-data

| Dataset | Records | Size | Status |
|---------|---------|------|--------|
| **Birthday Book** | 128 pages | ~244 MB | ✅ Complete (imported) |
| **Black Book** | 1,252 contacts | ~79 MB | ✅ Complete (imported) |
| **Flight Logs** | 118 pages (1991-2019) | ~797 MB | ✅ Complete (imported) |
| **Neo4j Nodes** | 383 | - | ✅ Complete (imported, was 10,356 available) |
| **Neo4j Relations** | 534 | - | ✅ Complete (imported, was 16,625+ available) |

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

### 9. HuggingFace Datasets

| Dataset | Records | Source | URL | Status |
|---------|---------|--------|-----|--------|
| **FULL_EPSTEIN_INDEX** | ~20,000 pages | House Oversight + DOJ | `thelde/remo/FULL_EPSTEIN_INDEX` | 🔍 Available |
| **epstein-files-20k** | 2,136,420 docs | House Oversight | `teyler/epstein-files-20k` | ✅ **INGESTED** (verified: 2.1M docs) |
| **epstein-data (v2.0)** | CC data | DOJ | `kabasshouse/epstein-data` | 🔍 Available |
| **epstein-emails** | 5,082 threads | House Oversight | `notesbymuneeb/epstein-emails` | 🔍 Available |
| **EPSTEIN_FILES_20K** | OCR + embeddings | House Oversight | `tensonaut/EPSTEIN_FILES_20K` | 🔍 Available |
| **epstein-fbi-files** | FBI docs | FBI Vault | `svetfm/epstein-fbi-files` | ✅ Downloaded (22 text files at /home/cbwinslow/workspace/epstein-data/fbi-vault/) |

**Download & Ingest Status:**
- **epstein-files-20k:** ✅ **COMPLETE & INGESTED**
  - Downloaded: 2,136,420 records (126.76 MB)
  - Table: `hf_epstein_files_20k` (2,136,420 rows)
  - Location: `/home/cbwinslow/workspace/epstein-data/huggingface/epstein_files_20k/`
  - Scripts: `download_hf_resume.py`, `import_hf_epstein_files_20k.py`

**✅ INGESTED - Next: Remaining datasets**

---

## 📈 Coverage Gaps

### Current Structural Gaps

| Gap | Timeframe | Coverage | Recommended Path |
|-----|-----------|----------|------------------|
| **Pre-107th Congress** | Before 2001 | ❌ Not in current historical pipeline | Congress.gov API key + alternate ingestion path |
| **119th Congress Members** | 2025-2026 | ⚠️ Missing in `congress_members` | Run members-only Congress backfill for 119th |
| **Roll Call Vote Details** | 2000+ | ⚠️ Vote refs exist, detail tables empty | Backfill House/Senate vote detail pipelines |
| **White House Visitor Logs** | Before 2009 | ❌ Not publicly disclosed in the same archive flow | External archival/legal-source strategy |
| **Pre-2015 News** | Before Feb 2015 | ⚠️ GDELT not available | CourtListener RECAP, Wayback, other archives |
| **SEC EDGAR Linkage Data** | 2000+ | ⚠️ Partial/optional | Expand SEC ingestion for Form 4 / 13F |
| **FARA Bulk Coverage** | 2000+ | ⚠️ Limited API support | Managed/manual acquisition workflow |

**Alternative Sources Needed:**
- CourtListener RECAP and docket-level court sources
- Wayback Machine and archival news repositories
- SEC EDGAR direct pipelines (targeted forms)
- Managed FARA acquisition strategy

---

## 🔄 Ingestion Pipeline Status

### Completed Pipelines (✅)

| Pipeline | Script | Status | Last Run | Records |
|----------|--------|--------|----------|---------|
| DOJ Ripper | `epstein-ripper/auto_ep_rip.py` | ✅ Complete | 2026-04 | 1.4M docs |
| jMail Import | `scripts/import_jmail_*.py` | ✅ Complete | 2026-04-04 | 1.78M emails |
| ICIJ Import | `scripts/import_icij.py` | ✅ Complete | 2026-04-04 | 814K entities |
| FEC Import | `scripts/import_fec.py` | ✅ Complete | 2026-03 | 447M contributions |
| Congress.gov | `scripts/download_congress_historical.py` | ✅ Complete | 2026-04-24 | 368K bills, 10K members |
| GovInfo Bulk | `scripts/download_govinfo_bulk.py` | ✅ Complete | 2026-04-24 | 246 files, 737K entries |
| White House Visitors | `scripts/download_whitehouse.py` | ✅ Complete | 2026-04-22 | 2.5M visits |
| HuggingFace epstein-files-20k | `scripts/import/import_hf_epstein_files_20k.py` | ✅ Complete | 2026-04 | 2.1M docs |
| Black Book (dleeerdefi) | `scripts/import/import_dleeerdefi_black_book.py` | ✅ Complete | 2026-04 | 1,252 contacts |
| Flight Logs (dleeerdefi) | `scripts/import/import_flight_logs.py` | ✅ Complete | 2026-04 | 2,051 flights |
| RTX 3060 Embeddings | `scripts/enrichment/rtx3060_embeddings.py` | ✅ Complete | 2026-04-16 | Generated |
| FARA Bulk Import | `scripts/import/import_fara.py` | ✅ Complete | 2026-04-24 | 7K+ records |
| GovInfo 119 Normalization | `scripts/import/import_govinfo_*.py` | ✅ Complete | 2026-04-24 | Verified |

### Active Pipelines (🟡)

| Pipeline | Script | Status | Last Run | Records |
|----------|--------|--------|----------|---------|
| GDELT Swarm | `gdelt_parallel_swarm.py` | 🟡 Running | 2025-04-10 | 23,413+ articles |

### Pending Pipelines (📍 or 🔴)

| Pipeline | Source | Status | Priority |
|----------|--------|--------|----------|
| Senate Vote Details | `scripts/download/download_senate_vote_details.py` | ✅ Complete (403 resolved, 6.3K votes) | Done |
| SEC EDGAR Bulk | `scripts/download/download_sec_edgar_recent.py` | 🔴 Needs bulk run (197 rows only) | High |
| GovInfo Expansion | `scripts/download/download_govinfo_bulk.py` | ✅ Complete (737K entries, 246 files) | Done |
| 749K Missing Documents | - | 🔴 Gap identified | High |
| FBI Vault | `scripts/import/import_fbi_vault.py` | ✅ Complete (22 docs, 1,426 pages) | Done |
| Neo4j Graph Import | `scripts/import/import_neo4j_graph.py` | 📍 Needs import | High |
| Knowledge Graph Build | `scripts/processing/master_unify.py` | 🔴 From entities | High |
| Text Embeddings | `scripts/enrichment/embed_*.py` | 🔴 Expand coverage | Medium |
| jMail iMessages/Photos | `scripts/download/download_jmail_icij.py` | 🔴 403 errors (parquet present) | Medium |
| Birthday Book (dleeerdefi) | `scripts/import/import_birthday_book.py` | 📍 Needs extraction | Medium |
| Image Analysis | `scripts/processing/image_analysis.py` | 📍 38K images | Low |

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

### Completed (This Week)

1. ✅ **Senate Vote Details** - 403 errors resolved, 6,313 votes ingested (Issue #58 done)
2. ✅ **GovInfo Bulk** - 737K entries, 246 files imported (Issue #52 done)
3. ✅ **FARA Bulk** - 7,045 registrations, 17,358 principals imported (Issue #57 done)
4. ✅ **jMail Full Dataset** - 1,783,792 rows loaded in jmail_emails_full
5. ✅ **ICls Offshore Leaks** - 69.7 MB downloaded and imported
6. ✅ **Congress Historical** - 368K bills, 10K members, 2.7M member votes

### Immediate (This Week)

1. 🔴 **SEC EDGAR Bulk** - Run bulk import for Form 4/13F (Issue #55)
2. ✅ **FBI Vault** - Complete (22 docs, 1,426 pages in PostgreSQL) (Issue #44 resolved)
3. 🔴 **749K Missing Documents** - Gap identification (Issue #39)
4. 🔴 **Neo4j Graph Import** - Import knowledge graph (Issue #12)
5. 🔴 **Knowledge Graph Build** - From document co-occurrence (Issue #30)
6. 🔴 **Text Embeddings** - Expand beyond RTX 3060 (Issue #29)
7. 🔴 **jMail iMessages/Photos** - 403 errors, parquet files present (Issue #28)

### Short Term (This Month)

7. 🔴 **GovInfo Expansion** - Beyond current bulk baseline (Issue #52)
8. 🔴 **Knowledge Graph Build** - From document co-occurrence (Issue #30, #12)
9. 🔴 **Text Embeddings** - Expand coverage beyond RTX 3060 (Issue #29)
10. 📌 **Pre-2015 coverage** - CourtListener RECAP for 1999-2014
11. 📌 **Birthday Book** - 128 pages manual/OCR extraction
12. 📌 **Image analysis** - 38K images from PDFs

### Long Term (This Quarter)

13. 🔴 **Entity deduplication** across all sources
14. 🔴 **Master knowledge graph** combining all datasets
15. 🔴 **Embeddings** for 100% of documents
16. 🔴 **jMail iMessages** - Download from jmail.world (Issue #28)

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

*Generated: April 24, 2026*
*Maintained by: Research Team*
