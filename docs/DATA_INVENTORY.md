# Epstein Files Data Inventory

> **Last Updated:** April 22, 2026
> **Purpose:** Comprehensive inventory of all data sources, their locations, and current state

---

## Overview

This document provides a complete inventory of all data in the Epstein Files Analysis project. It compares our data with [epsteinexposed.com](https://epsteinexposed.com) to identify gaps and plan next steps.

**Recent Updates (April 22, 2026):**
- ✅ **Congress Historical 107th:** 10,791 bills + 553 members imported after fixing the historical API endpoints
- ✅ **Congress Historical 108th-109th Imported:** 108th = 10,669 bills + 544 members, 109th = 13,072 bills + 546 members
- ✅ **GovInfo Historical 2000:** 8,543 packages imported (`BILLS=7,075`, `CRPT=849`, `FR=253`, `USCOURTS=366`)
- ✅ **GovInfo Historical 2001:** package summaries imported; `FR=249`, `USCOURTS=358`
- ✅ **Congress Bills Cleanup:** Removed 54,945 duplicate 118th rows and 401 stray snapshot/test rows
- ✅ **FEC Historical Coverage Verified:** `fec_individual_contributions` already contains 447,189,732 rows across cycles 2000-2026

**Previous Updates (April 18, 2026):**
- ✅ **DATA PIPELINE TRACKING SYSTEM:** Created `data_pipeline_tracking` table for systematic tracking of downloads/ingestion
- ✅ **ICIJ Offshore Leaks:** 5,355,790 records imported (814K entities, 771K officers, 402K addresses, 25K intermediaries, 3K others, 3.3M relationships)
- ✅ **USA Spending Awards:** 100 records imported (sample data from 2 JSON files)
- 🔄 **GOVERNMENT HISTORICAL BACKFILL IN PROGRESS:** Congress.gov and GovInfo.gov corrected and resumed
- ✅ **Congress.gov:** 107th + 118th slices verified in PostgreSQL
- ✅ **FEC.gov Committees/Candidates:** 91,011 records (11,989 candidates, 59,021 committees, 8,623 links, 12,378 PAC records)
- ✅ **GovInfo.gov:** current-era packages plus historical 2000 slice imported into `govinfo_packages`
- ✅ **FEC Individual Contributions Script:** Created for indiv24.zip (90M estimated records, 11GB) - import running in background
- ✅ **Centralized Config:** Created config.py for all import scripts
- ✅ **House Financial Disclosures:** 37,281 records (2008-2024) imported via workaround script
- 🔄 **Senate Financial Disclosures:** Not accessible from server (DNS resolution error for efts.senate.gov)
- 🔄 **Senate LDA:** Not downloaded yet (tables don't exist)
- 🔄 **FEC Individual Import:** In progress (90M records, 11GB)

**Previous Updates (April 14, 2026):**
- 🔄 **GOVERNMENT DATA INTEGRATION IN PROGRESS:** Adding FEC, Congress, Lobbying, FARA, GovInfo datasets
- 🔄 **BULK DOWNLOADS RUNNING:** 400K+ GovInfo documents, 200K lobbying reports, 30K FEC records
- 🔄 **CROSS-REFERENCE QUERIES CREATED:** 10 SQL views linking entities across datasets
- 🔄 **DOCUMENTATION UPDATED:** PROJECT_OVERVIEW.md, ROADMAP.md created
- ✅ **IMPORT SCRIPTS CREATED:** 10+ Python scripts for government data ingestion
- ✅ **KNOWLEDGE GRAPH PLAN:** Neo4j schema designed for entity relationships
- ✅ **HUGGINGFACE PUBLISHING PLAN:** Open dataset strategy defined
- ✅ **PHASE 22 Media Acquisition Infrastructure:** 5 agents created, schema deployed
- ✅ **NewsDiscoveryAgent tested:** Successfully found 10 Epstein articles via GDELT
- ✅ **Downloaded jmail.world full datasets (318.9 MB emails, 24.2 MB documents)**
- ✅ **Downloaded ICIJ Offshore Leaks full database (69.7 MB)**
- ✅ **SQLite imports complete:** redactions (2.59M), reconstructed_pages (39K), extracted_entities (107K)
- ✅ **jMail documents import COMPLETE (1.41M documents)**

---

## Data Pipeline Tracking System

**Table:** `data_pipeline_tracking` in PostgreSQL

**Purpose:** Systematic tracking of all data sources through download and ingestion pipeline

**Schema:**
```sql
CREATE TABLE data_pipeline_tracking (
    id SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,  -- 'government', 'financial', 'legal', 'media', 'research'
    source_url TEXT,

    -- Download tracking
    download_status TEXT DEFAULT 'pending',  -- 'pending', 'downloading', 'completed', 'failed'
    download_started_at TIMESTAMPTZ,
    download_completed_at TIMESTAMPTZ,
    download_error TEXT,
    download_size_bytes BIGINT,
    download_files_count INT,
    download_path TEXT,

    -- Ingestion tracking
    ingestion_status TEXT DEFAULT 'pending',  -- 'pending', 'in_progress', 'completed', 'failed'
    ingestion_started_at TIMESTAMPTZ,
    ingestion_completed_at TIMESTAMPTZ,
    ingestion_error TEXT,
    records_imported BIGINT DEFAULT 0,
    target_table TEXT,

    -- Metadata
    description TEXT,
    priority TEXT DEFAULT 'medium',  -- 'high', 'medium', 'low'
    notes TEXT,
    last_checked_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Query Pipeline Status:**
```bash
python3 scripts/ingestion/query_pipeline_status.py
```

**Current Status (April 18, 2026):**
- **Completed:** 11 datasets (downloaded + ingested)
- **In Progress:** 1 dataset (FEC Individual Contributions - 90M records)
- **Pending:** 5 datasets (blocked by network errors or not yet downloaded)

**Advantages of Database Tracking:**
- Programmatic access for queries and updates
- Can use triggers for automatic state tracking
- Easy to filter by status, priority, or source type
- Scalable as project grows
- Can generate reports and dashboards

---

## Quick Reference: epsteinexposed.com vs Our Data

| Metric | epsteinexposed.com | Our PostgreSQL | Gap | Status |
|--------|-------------------|----------------|-----|--------|
| **Documents** | 2,146,580 | 1,417,869 | -728,711 | ⚠️ 66.1% coverage |
| **Persons** | 1,580 | 1,578 (exposed_persons) | -2 | ✅ 99.9% match |
| **Flights** | 3,615 | 3,615 (exposed_flights) | 0 | ✅ 100% match |
| **Emails** | 1,783,792 | 1,783,792 (jmail_emails) | 0 | ✅ 100% match |
| **Connections** | 51,254 | 157,111 (cooccurrence_connections) | +105,857 | ✅ 307% match |
| **Locations** | Unknown | 83 (exposed_locations) | Unknown | ❓ |
| **Organizations** | Unknown | 55 (exposed_organizations) | Unknown | ❓ |
| **Nonprofits** | Unknown | 33 (exposed_nonprofits) | Unknown | ❓ |
| **FEC Contributions** | N/A | 447M (2000-2026) | N/A | 🆕 NEW |
| **Congress Trading** | N/A | 0 (congress_trading) | N/A | 🆕 NEW (awaiting API key) |

### Government Datasets (April 22, 2026)
| Dataset | Source | Records | Status | Schema |
|---------|--------|---------|--------|--------|
| **Congress Members** | Congress.gov | 4,334 | Imported (107th, 108th, 109th, 118th) | congress_members |
| **Congress Bills** | Congress.gov | 53,847 | Imported (107th, 108th, 109th, 118th) | congress_bills |
| **FEC Candidates** | FEC.gov | 11,989 | Imported | fec_candidates |
| **FEC Committees** | FEC.gov | 59,021 | Imported | fec_committees |
| **FEC Candidate-Committee Links** | FEC.gov | 8,623 | Imported | fec_candidate_committee_links |
| **FEC PAC Summary** | FEC.gov | 12,378 | Imported | fec_pac_summary |
| **FEC Individual Contributions** | FEC.gov | 447,189,732 | Imported | fec_individual_contributions |
| **GovInfo Packages** | GovInfo.gov | 62,161 | Imported | govinfo_packages |
| **Federal Register** | GovInfo.gov | 2,245 | Imported from package summaries | federal_register_entries |
| **Court Opinions** | GovInfo.gov | 30,724 | Imported from package summaries | court_opinions |
| **Committee Reports** | GovInfo.gov | 849 historical + current-era packages | Imported into `govinfo_packages` | govinfo_packages |
| **FARA Registrations** | DOJ FARA | ~5K | Downloading | fara_registrations, fara_foreign_principals |
| **Lobbying Registrations** | Senate LDA | ~5K | 🔄 Ingesting | lobbying_registrations |
| **Lobbying Reports** | Senate LDA | ~200K | 🔄 Ingesting | lobbying_quarterly_reports |
| **White House Visitors** | White House | 8 | ✅ Sample | whitehouse_visitors |
| **SEC Insider Transactions** | SEC EDGAR | Placed | ✅ Schema | sec_insider_transactions |
| **USA Spending Awards** | USASpending.gov | 100 | ✅ Sample | usa_spending_awards |
| **House Financial Disclosures** | House Clerk | 37,281 | ✅ Imported | house_financial_disclosures |
| **Senate Financial Disclosures** | Senate eFD | 0 | ❌ DNS error | senate_financial_disclosures |

**Total Government Records Ingested:** 447M+ plus current Congress/GovInfo/FD support tables; historical backfill remains in progress for Congress.gov and GovInfo.gov

### Additional Data
- **FBI Vault:** 22 documents (1,344 pages total)
- **Embeddings:** 230,931 pages with 384-dim vectors (7.98% coverage)
- **Document Entities:** 5.7M NER-extracted entities
- **Cross-Reference Queries:** 10 SQL views linking entities across datasets

---

## Data Storage Locations

### Primary Data Mount
```
/home/cbwinslow/workspace/epstein-data/          # 508GB total
├── raw-files/                      # 177GB - Downloaded PDFs (1.3M files)
├── hf-parquet/                     # 318GB - HuggingFace parquet (634 files)
├── databases/                      # 12GB - Pre-built SQLite databases
├── processed/                      # OCR output (ready for processing)
├── knowledge-graph/                # KG exports (ready)
├── supplementary/                  # Scraped data from epsteinexposed.com
└── logs/                           # Download and processing logs
```

### Workspace (Code & Config)
```
~/workspace/epstein/                # 15GB - Project root
├── Epstein-Pipeline/               # [submodule] Processing pipeline
├── Epstein-research-data/          # [submodule] Pre-built databases & exports
├── epstein-ripper/                 # [submodule] DOJ downloader
├── EpsteinLibraryMediaScraper/     # [submodule] Media scraper
└── scripts/                        # Our custom scripts
```

---

## PostgreSQL Database (Primary Data Store)

**Connection:** `postgresql://cbwinslow:123qweasd@localhost:5432/epstein`

### Extensions Enabled
| Extension | Version | Purpose |
|-----------|---------|---------|
| vector (pgvector) | 0.6.0 | HNSW vector search, vector(768) |
| pg_trgm | 1.6 | Fuzzy text matching |
| unaccent | 1.1 | Accent-insensitive search |
| pg_stat_statements | 1.10 | Query monitoring |

### Tables (53 total, ~462M rows)

#### Core Document Tables
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| documents | 1,397,821 | Main document registry | full_text_corpus.db |
| pages | 2,892,730 | OCR text per page with FTS | full_text_corpus.db |
| documents_content | 1,380,346 | Consolidated document text | HF parquet |
| document_classification | 1,380,964 | Document categories | full_text_corpus.db |
| efta_crosswalk | 1,380,964 | EFTA number mappings | full_text_corpus.db |
| file_registry | 1,313,844 | SHA-256 hashes, file metadata | Our population script |

#### Media Acquisition Tables (Phase 22)
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| media_news_articles | 0 | News articles from GDELT, Wayback, RSS | Pending collection |
| media_videos | 0 | Video content with transcripts | Pending collection |
| media_documents | 0 | Court documents, government releases | Pending collection |
| media_collection_queue | 0 | Task queue for media acquisition | Ready for use |
| media_collection_stats | 1 | Daily collection statistics | Initialized |
| media_entity_mentions | 0 | Cross-reference media to entities | Ready for use |

#### Email & Communication Tables
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| emails | 41,924 | Emails extracted from OCR text | communications.db |
| email_participants | 90,204 | Email participant records | communications.db |
| communication_pairs | 271 | Communication relationships | communications.db |

#### Redaction & Reconstruction Tables
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| redactions | 2,587,447 | Redacted sections identified | redaction_analysis_v2.db |
| document_summary | 849,655 | Document summaries | redaction_analysis_v2.db |
| reconstructed_pages | 39,588 | Pages with recovered text | redaction_analysis_v2.db |
| redaction_entities | 107,422 | Entities extracted from redactions | redaction_analysis_v2.db |

#### Media Tables
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| images | 38,955 | Image metadata from PDFs | image_analysis.db |
| ocr_results | 38,955 | OCR processing results | ocr_database.db |
| transcripts | 1,628 | Audio/video transcripts | transcripts.db |
| transcript_segments | 25,129 | Transcript time segments | transcripts.db |

#### Legal & Subpoena Tables
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| subpoenas | 257 | Subpoena records | prosecutorial_query_graph.db |
| rider_clauses | 2,018 | Subpoena rider clauses | prosecutorial_query_graph.db |
| returns | 304 | Subpoena returns | prosecutorial_query_graph.db |
| subpoena_return_links | 304 | Subpoena-return relationships | prosecutorial_query_graph.db |
| clause_fulfillment | 3,813 | Clause fulfillment tracking | prosecutorial_query_graph.db |
| investigative_gaps | 779 | Identified investigative gaps | prosecutorial_query_graph.db |

#### Financial Tables
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| fec_donations | 400 | FEC donation records | Supplementary data |
| fec_disbursements | 3,600 | FEC disbursement records | Supplementary data |

#### Government Tables (April 22, 2026)
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| congress_members | 4,334 | Congressional member data (107th, 108th, 109th, 118th) | Congress.gov |
| congress_bills | 53,847 | Congressional bills | Congress.gov |
| fec_candidates | 11,989 | FEC candidate records (2020, 2022, 2024) | FEC.gov |
| fec_committees | 59,021 | FEC committee records (2020, 2022, 2024) | FEC.gov |
| fec_candidate_committee_links | 8,623 | Links between candidates and committees | FEC.gov |
| fec_pac_summary | 12,378 | PAC financial summaries | FEC.gov |
| govinfo_packages | 53,618 | GovInfo.gov packages (bills, reports, opinions) | GovInfo.gov |
| federal_register_entries | 2,245 | Federal Register entries | GovInfo.gov |
| court_opinions | 30,724 | Court opinions | GovInfo.gov |

#### epsteinexposed.com Mirror Tables
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| exposed_persons | 1,578 | Person profiles | Scraped from website |
| exposed_flights | 3,615 | Flight log entries | Scraped from website |
| exposed_emails | 100 | Email metadata (sample) | Scraped from website |
| exposed_locations | 83 | Location records | Scraped from website |
| exposed_organizations | 55 | Organization records | Scraped from website |
| exposed_nonprofits | 33 | Nonprofit records | Scraped from website |

#### HuggingFace Datasets (April 13, 2026)
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| hf_epstein_files_20k | 2,136,420 | Main HF dataset (20K docs) | HuggingFace teyler/epstein-files-20k |
| hf_house_oversight_docs | 1,791,798 | House Oversight document references | notesbymuneeb/epstein-emails (TXT) |
| hf_ocr_complete | TBD | OCR text data | tensonaut/EPSTEIN_FILES_20K_OCR |
| hf_embeddings | TBD | Vector embeddings (768-dim) | HF embeddings dataset |
| hf_epstein_data_text | TBD | Extracted text content | epstein-data-text |
| full_epstein_index | 8,531 | EFTA text extract index | HuggingFace theelderemo/FULL_EPSTEIN_INDEX |
| house_oversight_embeddings | 69,290 | House Oversight embeddings (768-dim) | HuggingFace svetfm/epstein-files-nov11-25 |
| fbi_embeddings | 236,174 | FBI file embeddings | HuggingFace svetfm/epstein-fbi-files |

**Total HF Records:** 4M+ (complete + importing)

---

## SQLite Databases (Pre-built Sources)

Located at: `/home/cbwinslow/workspace/epstein-data/databases/`

| Database | Size | Tables | Key Content | Migrated to PG? |
|----------|------|--------|-------------|-----------------|
| full_text_corpus.db | 7.0GB | 9 | 1.4M docs, 2.9M pages, FTS5 search | ✅ Yes |
| redaction_analysis_v2.db | 940MB | 4 | 2.59M redactions, 849K summaries | ✅ Yes |
| image_analysis.db | 389MB | 7 | 38,955 images with AI descriptions | ✅ Yes |
| ocr_database.db | 68MB | 7 | 38,955 OCR results | ✅ Yes |
| communications.db | 30MB | 4 | 41,924 emails, 90K participants | ✅ Yes |
| transcripts.db | 4.8MB | 7 | 1,628 media transcriptions | ✅ Yes |
| prosecutorial_query_graph.db | 2.5MB | 7 | 257 subpoenas | ✅ Yes |
| knowledge_graph.db | 892KB | 4 | 606 entities, 2,302 relationships | ✅ Yes |

**Migration Status:** All 8 SQLite databases have been migrated to PostgreSQL (10.9M rows total).

---

## Raw PDF Files

Located at: `/home/cbwinslow/workspace/epstein-data/raw-files/`

| Dataset | Size | Description |
|---------|------|-------------|
| data1 | 1.3GB | DOJ Dataset 1 |
| data2 | 632MB | DOJ Dataset 2 |
| data3 | 598MB | DOJ Dataset 3 |
| data4 | 359MB | DOJ Dataset 4 |
| data5 | 62MB | DOJ Dataset 5 |
| data6 | 54MB | DOJ Dataset 6 |
| data7 | 99MB | DOJ Dataset 7 |
| data8 | 1.8GB | DOJ Dataset 8 |
| data9 | 76GB | DOJ Dataset 9 |
| data10 | 68GB | DOJ Dataset 10 |
| data11 | 28GB | DOJ Dataset 11 |
| data12 | 127MB | DOJ Dataset 12 |
| **Total** | **177GB** | **1,313,861 files** |

**Coverage:** 94.0% of 1,397,796 EFTA numbers (83,936 files permanently missing from public sources).

---

## ICIJ Offshore Leaks Database

**URL:** `https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip`
**Downloaded:** April 3, 2026
**Size:** 69.7 MB (compressed), ~600 MB extracted
**Status:** ✅ Extracted, ⏳ Import to PostgreSQL pending

### Data Schema (entities)
```csv
node_id,name,original_name,former_name,jurisdiction,jurisdiction_description,
company_type,address,internal_id,incorporation_date,inactivation_date,
struck_off_date,dorm_date,status,service_provider,ibcRUC,country_codes,
countries,sourceID,valid_until,note
```

### Data Schema (relationships)
```csv
node_id_start,node_id_end,rel_type,link,status,start_date,end_date,sourceID
```

**Location:** `/home/cbwinslow/workspace/epstein-data/downloads/icij_extracted/`

---

## jmail.world Email Data (Primary Email Source)

**URL:** `https://data.jmail.world/v1/emails-slim.parquet`
**Size:** 38.8 MB (1,783,792 emails)
**Status:** ✅ Downloaded & imported to PostgreSQL (`jmail_emails` table)

### Email Sources in jmail.world Data

| Source | Count | Description | PostgreSQL |
|--------|-------|-------------|------------|
| VOL00009-12 (DOJ EFTA) | 1,756,912 | Same DOJ docs, 42× better extraction (threaded parsing) | ✅ `jmail_emails` |
| yahoo_2 | 17,448 | Epstein's personal Yahoo inbox (`jeeproject@yahoo.com`) | ✅ `jmail_emails` |
| House Oversight | 8,374 | Congressional investigation releases (`jeevacation@gmail.com`) | ✅ `jmail_emails` |
| Ehud Barak | 1,058 | Former Israeli PM's email accounts (`ehbarak1@gmail.com`) | ✅ `jmail_emails` |

**Why 42× more DOJ emails?** Our extraction got 1‑2 emails per PDF. jmail extracts all emails from threaded conversations (some documents have 300+ individual emails).

---

## ICIJ Offshore Leaks Summary

| File | Rows | Size | Description | Import Status |
|------|------|------|-------------|---------------|
| `nodes-entities.csv` | 814,617 | 190 MB | Companies/offshore entities | ⏳ Pending |
| `nodes-officers.csv` | ~1.8M | 87 MB | People/officers | ⏳ Pending |
| `nodes-addresses.csv` | ~700k | 69 MB | Addresses | ⏳ Pending |
| `nodes-intermediaries.csv` | ~38k | 3.8 MB | Intermediaries/brokers | ⏳ Pending |
| `relationships.csv` | 3,339,272 | 247 MB | Entity relationships | ⏳ Pending |

**Total Records:** ~5.7 M entities + 3.3 M relationships

---

## Data Gaps Analysis

### Critical Gaps (Must Fix)

1. **Emails (1.74 M missing)**
   - Website claims: 1,783,792 emails
   - We have: 41,924 emails (extracted from OCR)
   - Gap: 1,741,868 emails
   - **Source:** jmail.world `emails-slim.parquet` (38.8 MB, 1.78 M emails)

2. **Connections (49 K missing)**
   - Website claims: 51,254 connections
   - We have: 2,302 curated relationships + 5.7 M document_entities
   - Gap: 48,952 curated connections
   - **Source:** Build from document_entities, email co-occurrence, flight co-occurrence

3. **Documents (749 K missing)**
   - Website claims: 2,146,580 documents
   - We have: 1,397,821 documents
   - Gap: 748,759 documents
   - **Source:** FBI Vault, CourtListener, House Oversight, Archive.org collections

### Secondary Gaps (Should Fix)

4. **Embeddings (0 % complete)**
   - Need: 2,892,730 page embeddings
   - Have: 0 embeddings generated
   - Action: Run `epstein embed` pipeline

5. **Persons Registry (36 missing)**
   - `persons_registry.json` has 1,614 entries
   - `exposed_persons` has 1,578 entries
   - Gap: 36 persons not imported

6. **Extracted Entities (not imported)**
   - `extracted_entities_filtered.json` has 8,085 filtered entities
   - Not imported to PostgreSQL

---

## Recommended Next Steps

### Priority 1: Download jmail.emails (1.78 M emails)
```bash
curl -o /home/cbwinslow/workspace/epstein-data/supplementary/emails-slim.parquet \
  "https://data.jmail.world/v1/emails-slim.parquet"
```
Then import to PostgreSQL using the existing `import_jmail_emails.py` script.

### Priority 2: Generate Embeddings
- Run `epstein embed` on all 2.9 M pages
- Create HNSW vector index for semantic search
- Enable semantic search functionality

### Priority 3: Build Connections Graph
- Analyze `document_entities` (5.7 M rows) to build connections
- Cross‑reference with flight logs and email data
- Build relationship graph matching website's 51 K connections

### Priority 4: Import Missing Data
- Import `persons_registry.json` (36 missing persons)
- Import `extracted_entities_filtered.json` (8,085 entities)
- Import phone numbers, supplemental CSVs as needed

### Priority 5: Knowledge Graph Enhancement
- Expand from 606 entities to match 1,580 persons
- Add flight‑based and email‑based connections
- Populate `entities` and `relationships` tables accordingly

---

## File Locations Reference

### Workspace Structure
```
~/workspace/
├── epstein/                    # Code, scripts, documentation (~15 GB)
├── epstein-data/              # Data storage (~500+ GB)
└── epstein-pipeline/           # Pipeline submodule
```

### Core Data Locations

| Data Type | Location | Size | Status |
|-----------|----------|------|--------|
| **Raw PDFs (DOJ)** | `/home/cbwinslow/workspace/epstein-data/raw-files/` | 177 GB | 1.3 M files |
| **HF Parquet** | `/home/cbwinslow/workspace/epstein-data/hf-parquet/` | 318 GB | 634 files |
| **SQLite DBs** | `/home/cbwinslow/workspace/epstein-data/databases/` | 12 GB | 8 databases |
| **ML Models** | `/home/cbwinslow/workspace/epstein-data/models/` | 109 GB | Processing models |

### HuggingFace Dataset Locations (April 13 2026)

| Dataset | Location | Size | SQL Table | Status |
|---------|----------|------|-----------|--------|
| epstein-files-20k | `hf-epstein-files-20k/` | 127 MB | `hf_epstein_files_20k` | ✅ Complete |
| House Oversight TXT | `hf-house-oversight/` | 101 MB | `hf_house_oversight_docs` | ✅ Complete |
| OCR Complete | `hf-ocr-complete/data/` | 1.3 GB | `hf_ocr_complete` | 🔄 Importing |
| Embeddings | `hf-embeddings/data/` | 341 MB | `hf_embeddings` | ⏳ Pending |
| Epstein Data Text | `hf-new-datasets/epstein-data-text/` | 2.2 GB | `hf_epstein_data_text` | ⏳ Pending |
| FBI Files | `hf-datasets/fbi-files/` | 4.5 GB | `fbi_vault_pages` | ✅ Metadata |
| Full Index | `hf-datasets/full-index/` | 4 MB | `full_epstein_index` | ✅ Complete |

### Other Data Locations

| Data Type | Location | Size |
|-----------|----------|------|
| Supplementary | `supplementary/` | ~22 MB |
| Research Data | `~/workspace/epstein/Epstein-research-data/` | ~28 MB |
| Downloads | `downloads/` | Variable |
| Logs | `logs/` | Variable |
| Backups | `backups/` | ~2 GB |

---

## PostgreSQL Quick Queries

```sql
-- Count documents
SELECT COUNT(*) FROM documents;

-- Check embeddings status
SELECT COUNT(*) FROM pages WHERE embedding IS NOT NULL;

-- Sample persons
SELECT * FROM exposed_persons LIMIT 10;
```

---

*This inventory should be updated as data is added or modified.*
