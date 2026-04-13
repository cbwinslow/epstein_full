# Epstein Files Data Inventory

> **Last Updated:** April 4, 2026
> **Purpose:** Comprehensive inventory of all data sources, their locations, and current state

---

## Overview

This document provides a complete inventory of all data in the Epstein Files Analysis project. It compares our data with [epsteinexposed.com](https://epsteinexposed.com) to identify gaps and plan next steps.

**Recent Updates (April 13, 2026):**
- ✅ **HUGGINGFACE DATASETS IMPORTED:** 4M+ records from 9 HF datasets
- ✅ **Duplicate Detection:** Found and removed 5,082 duplicate email records
- ✅ **Filesystem Cleanup:** Deleted 1,260 .incomplete files (~10 GB freed)
- ✅ **ICIJ IMPORT COMPLETE:** 3,339,267 relationships imported
- ✅ **jMail email import COMPLETE:** 1.78M emails
- ✅ **Phase 22 Media Acquisition Infrastructure:** 5 agents created, schema deployed
- ✅ **NewsDiscoveryAgent tested:** Successfully found 10 Epstein articles via GDELT
- ✅ Downloaded jmail.world full datasets (318.9 MB emails, 24.2 MB documents)
- ✅ Downloaded ICIJ Offshore Leaks full database (69.7 MB)
- ✅ Extracted ICIJ data: 814,344 entities, 3.3M relationships, 1.8M officers
- ✅ SQLite imports complete: redactions (2.59M), reconstructed_pages (39K), extracted_entities (107K)
- ✅ jMail documents import COMPLETE (1.41M documents)

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
| **FEC Contributions** | N/A | 5,420,940+ (fec_individual_contributions) | N/A | 🆕 NEW |
| **Congress Trading** | N/A | 0 (congress_trading) | N/A | 🆕 NEW (awaiting API key) |

### Additional Data
- **FBI Vault:** 22 documents (1,344 pages total)
- **Embeddings:** 230,931 pages with 384-dim vectors (7.98% coverage)
- **Document Entities:** 5.7M NER-extracted entities

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

### Tables (44 total, ~15M rows)

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
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| document_entities | 5,709,659 | NER-extracted entities from documents | Our NER extraction |
| entities | 606 | Curated knowledge graph entities | knowledge_graph.db |
| relationships | 2,302 | Curated entity relationships | knowledge_graph.db |
| graph_nodes | 677 | Knowledge graph nodes | prosecutorial_query_graph.db |
| graph_edges | 2,745 | Knowledge graph edges | prosecutorial_query_graph.db |
| edge_sources | 905 | Edge source references | knowledge_graph.db |
| resolved_identities | 1,139 | Resolved person identities | communications.db |

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
| hf_email_threads | ~~5,082~~ | ~~Email threads~~ | ~~DUPLICATE - DROPPED~~ |
| hf_ocr_complete | TBD | OCR text data | tensonaut/EPSTEIN_FILES_20K_OCR |
| hf_embeddings | TBD | Vector embeddings (768-dim) | HF embeddings dataset |
| hf_epstein_data_text | TBD | Extracted text content | epstein-data-text |
| full_epstein_index | 8,531 | EFTA text extract index | HuggingFace theelderemo/FULL_EPSTEIN_INDEX |
| house_oversight_embeddings | 69,290 | House Oversight embeddings | HuggingFace svetfm/epstein-files-nov11-25 |
| fbi_embeddings | 236,174 | FBI file embeddings | HuggingFace svetfm/epstein-fbi-files |

**Total HF Records:** 4M+ (complete + importing)
**Filesystem Data:** 15.6 GB across 9 dataset directories
**Note:** `hf_email_threads` dropped due to 100% duplication with `house_oversight_emails`

#### FEC Bulk Campaign Finance Data (NEW)
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| fec_individual_contributions | 5,420,940+ | Individual campaign contributions (1980-2026) | FEC bulk downloads |
| fec_committees | 23,000+ | Committee master records | FEC bulk downloads |
| fec_candidates | 12,000+ | Candidate master records | FEC bulk downloads |
| fec_committee_contributions | 0 | Committee-to-committee transfers (pending) | FEC bulk downloads |
| fec_candidate_contributions | 0 | Committee-to-candidate transfers (pending) | FEC bulk downloads |
| fec_operating_expenditures | 0 | Committee operating expenses (pending) | FEC bulk downloads |
| fec_download_log | 146 | Download tracking | Our ingestion |

**File Types Downloaded:**
- `indiv*.zip` - Individual contributions (23 cycles, 1980-2026)
- `cm*.zip` - Committee master (23 cycles)
- `cn*.zip` - Candidate master (23 cycles)
- `ccl*.zip` - Candidate-committee linkage (partial)
- `oth*.zip` - Committee contributions (partial)
- `pas2*.zip` - Candidate contributions (partial)
- `oppexp*.zip` - Operating expenditures (partial)

**Storage:** `/home/cbwinslow/workspace/epstein-data/raw-files/fec/` (22GB, 146 files)

#### Politicians' Financial Disclosure Data (NEW - FREE Sources)
| Table | Rows | Description | Source |
|-------|------|-------------|--------|
| congress_trading | 0 | Congress member stock trades (via govinfo.gov - FREE) | GovInfo API (api.data.gov) |
| politician_financial_summary | 0 | Net worth, assets, liabilities (House/Senate scrape) | disclosures-clerk.house.gov |
| house_disclosures | 0 | House financial disclosure PDFs | Direct scraping (no API key) |
| senate_disclosures | 0 | Senate financial disclosure PDFs | disclosure.senate.gov |

**FREE Data Sources (No API key required for basic access):**

1. **GovInfo.gov API** (FREE - 36,000 req/hour)
   - URL: https://api.govinfo.gov
   - Key: Get free at https://api.data.gov/signup/
   - Collections: Congressional Bills, Congressional Record, Financial Disclosures
   - Rate: 36,000 requests/hour, 1,200/minute

2. **Congress.gov API** (FREE)
   - URL: https://api.congress.gov
   - Key: Get free at https://api.congress.gov/
   - Data: Members, bills, committees, nominations
   - Rate: Lower limits (be polite)

3. **Data.gov API** (FREE)
   - URL: https://catalog.data.gov/api/3
   - Key: Optional but recommended
   - Data: 250,000+ datasets including campaign finance, lobbying, contracts

4. **House Disclosures** (Direct Scraping - NO API)
   - URL: https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure
   - Access: Public search, PDF downloads
   - Coverage: All House members, annual + periodic transaction reports

5. **Senate Disclosures** (Direct Scraping - NO API)
   - URL: https://www.disclosure.senate.gov/
   - Access: Public search, PDF downloads
   - Coverage: All Senators, annual + periodic transaction reports

**Scripts Created:**
- `scripts/download_gov_data.py` - GovInfo/Congress.gov/Data.gov APIs
- `scripts/scrape_congress_disclosures.py` - House/Senate direct scraping
- `scripts/download_fec_bulk.py` - FEC bulk data (also FREE)
- `scripts/download_politicians_financial.py` - Quiver Quant (paid - not used)

**Note on Quiver Quant:** API requires paid subscription. Using FREE government sources instead.

#### System Tables
| Table | Rows | Description |
|-------|------|-------------|
| letta_memories | 16 | Letta memory system |
| letta_memory_blocks | 5 | Memory block storage |
| letta_agent_context | 8 | Agent context data |
| tasks | 0 | Task tracking |
| task_history | 0 | Task history |
| external_references | 0 | External reference links |

### Vector/Embedding Status
| Component | Status | Details |
|-----------|--------|---------|
| pgvector extension | ✅ Installed | v0.6.0 with HNSW support |
| pages.embedding column | ✅ Exists | vector(768) type |
| Embeddings generated | ❌ None | 0 of 2,892,730 pages |
| Vector indexes | ❌ None | Need to create after embedding generation |

**Action Required:** Generate embeddings for semantic search using `epstein embed` command.

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

## HuggingFace Parquet Data

Located at: `/home/cbwinslow/workspace/epstein-data/hf-parquet/`

| Metric | Value |
|--------|-------|
| Total files | 634 |
| Total size | 318GB |
| Rows per file | ~4,529 |
| Estimated total rows | ~2,870,000 |
| Columns | dataset_id, doc_id, file_name, file_type, online_url, text_content, audio, image, video, metadata, error |
| Text coverage | ~28.7% of rows have text_content |
| Average text length | 3,162 characters |
| Max text length | 216,707 characters |

**Status:** Downloaded and complete. Text content needs to be processed and migrated to PostgreSQL documents_content table.

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

## Epstein-research-data (Structured Exports)

Located at: `~/workspace/epstein/Epstein-research-data/`

| File | Records | Description | Imported to PG? |
|------|---------|-------------|-----------------|
| knowledge_graph_entities.json | 606 | Curated entities with aliases, metadata | ✅ Yes (entities table) |
| knowledge_graph_relationships.json | 2,302 | Entity relationships with weights, dates | ✅ Yes (relationships table) |
| persons_registry.json | 1,614 | Unified person registry from 9 sources | ⚠️ Partial (exposed_persons has 1,578) |
| extracted_entities_filtered.json | 8,085 | Filtered NER extractions (3,881 names, 116 orgs, 357 emails, 2,238 phones) | ❌ Not imported |
| extracted_names_multi_doc.csv | 3,881 | Names appearing in multiple documents | ❌ Not imported |
| image_catalog.csv.gz | 38,955 | Complete image catalog | ⚠️ Partial (images table exists) |
| image_catalog_notable.json.gz | 38,864 | Images with people/notable content | ❌ Not imported |
| reconstructed_pages_high_interest.json.gz | 39,588 | High-interest reconstructed pages | ⚠️ Partial (reconstructed_pages table exists) |
| document_summary.csv.gz | ~850K | Document summaries | ✅ Yes (document_summary table) |
| efta_dataset_mapping.csv | ~1.4M | EFTA to dataset mappings | ✅ Yes (efta_crosswalk table) |
| phone_numbers_enriched.csv | Unknown | Enriched phone number data | ❌ Not imported |
| NON_EFTA_VERIFICATION_URLS.csv | Unknown | Verification URLs | ❌ Not imported |

---

## Supplementary Data (Scraped from epsteinexposed.com)

Located at: `/home/cbwinslow/workspace/epstein-data/supplementary/`

| File | Records | Description | Imported to PG? |
|------|---------|-------------|-----------------|
| epstein_exposed_persons.json | 1,578 | Person profiles | ✅ Yes (exposed_persons) |
| epstein_exposed_flights.json | 3,615 | Flight log entries | ✅ Yes (exposed_flights) |
| epstein_exposed_emails.json | 5 | Email metadata (sample only) | ✅ Yes (exposed_emails has 100) |
| epstein_exposed_locations.json | Unknown | Location records | ✅ Yes (exposed_locations) |
| epstein_exposed_nonprofits.json | Unknown | Nonprofit records | ✅ Yes (exposed_nonprofits) |
| export_persons.json | 1,578 | Person profiles (alternate) | ❌ Not imported |
| export_flights.json | 3,615 | Flight logs (alternate) | ❌ Not imported |
| export_locations.json | Unknown | Locations (alternate) | ❌ Not imported |
| export_organizations.json | Unknown | Organizations (alternate) | ✅ Yes (exposed_organizations) |
| fec_donations.json | ~400 | FEC donation records | ✅ Yes (fec_donations) |
| fec_disbursements.json | ~3,600 | FEC disbursement records | ✅ Yes (fec_disbursements) |

---

## HuggingFace Supplementary Datasets (New)

Located at: `/home/cbwinslow/workspace/epstein-data/supplementary-datasets/`

Downloaded March 31, 2026 using `aria2c` direct CDN (bypassed HF API rate limits)

| Dataset | File | Records | Size | Description | PostgreSQL Table | Status |
|---------|------|---------|------|-------------|------------------|--------|
| **svetfm/epstein-fbi-files** | `embeddings/all_embeddings.jsonl` | 236,174 | 3.9 GB | FBI file embeddings (768-dim) | `fbi_embeddings` | ✅ Imported |
| **svetfm/epstein-fbi-files** | `ocr/all_ocr.jsonl` | OCR text | 317 MB | FBI file OCR text | (file only) | ✅ Downloaded |
| **svetfm/epstein-fbi-files** | `pdfs/` | 8,150 files | Variable | FBI PDF files | (file only) | ✅ Downloaded |
| **svetfm/epstein-files-nov11-25** | `train-00000-of-00001.parquet` | 69,290 | 341 MB | House Oversight embeddings (768-dim) | `house_oversight_embeddings` | ✅ Imported |
| **theelderemo/FULL_EPSTEIN_INDEX** | `dataset_text_extract.csv` | 8,531 | 3.2 MB | EFTA text extract index | `full_epstein_index` | ✅ Imported |
| **tensonaut/EPSTEIN_FILES_20K** | N/A | N/A | N/A | House Oversight source docs | N/A | ❌ Unavailable (404) |

**Total New Records:** 314,995 (236,174 + 69,290 + 8,531 + 1,000 OCR)

### Import Scripts Created

| Script | Purpose | Format | Records Imported |
|--------|---------|--------|------------------|
| `scripts/import_fbi_embeddings.py` | FBI embeddings → PostgreSQL | JSONL streaming | 236,174 |
| `scripts/import_house_oversight_embeddings.py` | House Oversight → PostgreSQL | Parquet | 69,290 |
| `scripts/import_full_epstein_index.py` | Full Index → PostgreSQL | CSV | 8,531 |

### Model Compatibility
All embedding datasets use **768-dimensional vectors** with `nomic-embed-text` model, fully compatible with existing kabasshouse data (2.1M embeddings).

---

## jmail.world Email Data (Primary Email Source)

**URL:** `https://data.jmail.world/v1/emails-slim.parquet`
**Size:** 38.8MB (1,783,792 emails)
**Status:** ✅ DOWNLOADED & IMPORTED TO POSTGRESQL

### Email Sources in jmail.world Data

| Source | Count | Description | PostgreSQL |
|--------|-------|-------------|------------|
| VOL00009-12 (DOJ EFTA) | 1,756,912 | Same DOJ docs, 42x better extraction (threaded parsing) | ✅ jmail_emails |
| yahoo_2 | 17,448 | **Epstein's personal Yahoo inbox** (`jeeproject@yahoo.com`) | ✅ jmail_emails |
| House Oversight | 8,374 | Congressional investigation releases (`jeevacation@gmail.com`) | ✅ jmail_emails |
| Ehud Barak | 1,058 | Former Israeli PM's email accounts (`ehbarak1@gmail.com`) | ✅ jmail_emails |

**Why 42x more DOJ emails?** Our extraction got 1-2 emails per PDF. Jmail extracts all emails from threaded conversations (some documents have 300+ individual emails).

### Import Details
- **Total emails imported:** 1,783,792
- **Epstein as sender:** 320,871 emails
- **Date range:** 1990-01-01 to 2026-10-07
- **Top sender:** Lesley Groff (126,336 emails)
- **Table:** `jmail_emails` with 7 indexes
- **Import scripts:** `scripts/import_jmail_emails.py`, `scripts/import_jmail_emails_fast.py`

### Other jmail.world Data Files

| File | Size | Description |
|------|------|-------------|
| `emails-slim.parquet` | 38.8MB | 1.78M emails |
| `imessage_conversations.parquet` | 3.6KB | 4,509 iMessage conversations |
| `imessage_messages.parquet` | 168KB | iMessage messages |
| `photos.parquet` | 1.0MB | 18K photos |
| `people.parquet` | 9.9KB | 473 people in photos |
| `photo_faces.parquet` | 57.7KB | 975 face detections |

---

## ICIJ Offshore Leaks Database

**URL:** `https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip`
**Downloaded:** April 3, 2026
**Size:** 69.7 MB (compressed), ~600 MB extracted
**Status:** ✅ EXTRACTED, ⏳ Import to PostgreSQL pending

### About ICIJ
**ICIJ** = International Consortium of Investigative Journalists  
A nonprofit coordinating global investigative journalism across 100+ countries.

### Coverage
- **Panama Papers** (2016): 11.5M documents from Mossack Fonseca
- **Paradise Papers** (2017): 13.4M documents from offshore law firms
- **Pandora Papers** (2021): 11.9M documents from 14 offshore service providers
- **Bahamas Leaks** (2016): 1.3M documents from Bahamian corporate registry
- **Offshore Leaks** (2013): Original offshore financial records

### Extracted Files

| File | Rows | Size | Description | Import Status |
|------|------|------|-------------|---------------|
| `nodes-entities.csv` | 814,617 | 190 MB | Companies/offshore entities | ⏳ Pending |
| `nodes-officers.csv` | ~1,800,000 | 87 MB | People/officers | ⏳ Pending |
| `nodes-addresses.csv` | ~700,000 | 69 MB | Addresses | ⏳ Pending |
| `nodes-intermediaries.csv` | ~38,000 | 3.8 MB | Intermediaries/brokers | ⏳ Pending |
| `nodes-others.csv` | ~4,000 | 389 KB | Other entities | ⏳ Pending |
| `relationships.csv` | 3,339,272 | 247 MB | Entity relationships | ⏳ Pending |

**Total Records:** ~5.7M entities + 3.3M relationships

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

### License
Open Database License (ODbL) - free to use, share, and modify

### Location
`/home/cbwinslow/workspace/epstein-data/downloads/icij_extracted/`

---

## epsteinexposed.com API Assessment

**Base URL:** `https://epsteinexposed.com/api/v2`
**Rate Limit:** 100 req/hr anonymous, 1,000 req/hr with issued key

### Bulk Export Endpoints (FREE)

| Endpoint | Records | Status |
|----------|---------|--------|
| `/export/persons` | 1,578 | ✅ Downloaded |
| `/export/flights` | 3,615 | ✅ Downloaded |
| `/export/locations` | 83 | ✅ Downloaded |
| `/export/organizations` | 55 | ✅ Downloaded |

### Paginated Endpoints (Multiple Requests)

| Endpoint | Total | Downloaded | Feasibility |
|----------|-------|------------|-------------|
| `/emails` | 11,280 | 100 | ⚠️ 113 pages needed |
| `/documents` | 2,146,580 | 0 | ❌ 21,466 pages = 9+ days |

**Conclusion:** API is NOT viable for bulk document downloads. Use jmail.world for emails instead.

---

## Data Gaps Analysis

### Critical Gaps (Must Fix)

1. **Emails (1.74M missing)**
   - Website claims: 1,783,792 emails
   - We have: 41,924 emails (extracted from OCR)
   - Gap: 1,741,868 emails
   - **Source:** jmail.world `emails-slim.parquet` (38.8MB, 1.78M emails)
   - **Action:** Download from `https://data.jmail.world/v1/emails-slim.parquet`

2. **Connections (49K missing)**
   - Website claims: 51,254 connections
   - We have: 2,302 relationships (curated) + 5.7M document_entities (NER)
   - Gap: 48,952 curated connections
   - **Source:** Build from document_entities, email co-occurrence, flight co-occurrence

3. **Documents (749K missing)**
   - Website claims: 2,146,580 documents
   - We have: 1,397,821 documents
   - Gap: 748,759 documents
   - **Source:** FBI Vault, CourtListener, House Oversight, Archive.org collections

### Secondary Gaps (Should Fix)

4. **Embeddings (0% complete)**
   - Need: 2,892,730 page embeddings
   - Have: 0 embeddings generated
   - Action: Run `epstein embed` pipeline

5. **Persons Registry (36 missing)**
   - persons_registry.json has 1,614 entries
   - exposed_persons has 1,578 entries
   - Gap: 36 persons not imported

6. **Extracted Entities (not imported)**
   - extracted_entities_filtered.json has 8,085 filtered entities
   - Not imported to PostgreSQL
   - Action: Import to supplement document_entities

---

## Missing Data Sources (Not Yet Acquired)

| Priority | Source | Records | Effort | Description |
|----------|--------|---------|--------|-------------|
| **1** | jmail.world emails | 1.78M | Easy (38.8MB) | Primary email source for epsteinexposed.com |
| **2** | jmail.world iMessages | 4,509 | Easy | Epstein's iMessage conversations |
| **3** | jmail.world photos | 18K | Easy | Photos with face detection |
| **4** | HF epstein-emails | 5,258 | Easy | Alternative email source |
| **5** | HF epstein-flight-logs | Unknown | Easy | Parsed flight log entries |
| **6** | HF epstein-black-book | Unknown | Easy | Contact entries |
| **7** | Kaggle Epstein Ranker | 23,700 | Medium | AI-analyzed documents |
| **8** | ICIJ Offshore Leaks | Large | Medium | Panama/Paradise/Pandora Papers |
| **9** | FBI Vault | Unknown | Medium | FBI investigative files |
| **10** | CourtListener | Unknown | Medium | Court records |
| **11** | OpenSanctions | N/A | Easy | Requires API key |
| **12** | IRS Form 990 | Unknown | Medium | Nonprofit financials |
| **13** | SEC EDGAR | Unknown | Medium | Insider trading filings |

---

## Datasets for Epstein Information Discovery & Parameter Generation

### Critical Datasets for Cross-Referencing

These datasets are essential for discovering connections, generating search parameters, and building a comprehensive picture of Epstein's network:

#### Tier 1: Essential for Network Analysis
| Dataset | Source | Status | Use Case |
|---------|--------|--------|----------|
| **FEC Contributions** | fec.gov | 🆕 Downloading (22GB) | Find political donations from Epstein associates |
| **Congress Trading** | Quiver Quant | ⏳ Needs API key | Track stock trades by politicians in Epstein's circle |
| **Offshore Leaks** | ICIJ | ❌ Not acquired | Panama/Paradise Papers for shell companies |
| **SEC Insider Trading** | EDGAR | ❌ Not acquired | Stock trades by executives connected to Epstein |
| **Flight Logs (Full)** | Multiple | ✅ 3,615 flights | Travel patterns, co-travelers |
| **Emails (Complete)** | jmail.world | ✅ 1.78M emails | Communication patterns, coordination |

#### Tier 2: Important for Context
| Dataset | Source | Status | Use Case |
|---------|--------|--------|----------|
| **FBI Vault Files** | FBI | ⚠️ Partial (22 docs) | Investigative documents |
| **Court Records** | CourtListener/PACER | ❌ Not acquired | Legal proceedings, testimony |
| **IRS 990 Forms** | IRS/CitizenAudit | ❌ Not acquired | Nonprofit financial flows |
| **Property Records** | County assessors | ❌ Not acquired | Real estate transactions |
| **Corporate Registrations** | OpenCorporates | ❌ Not acquired | Shell companies, business entities |
| **Lobbying Disclosures** | Senate LDA | ❌ Not acquired | Influence operations |

#### Tier 3: Supplementary Intelligence
| Dataset | Source | Status | Use Case |
|---------|--------|--------|----------|
| **Social Media Archives** | Wayback/Archive.org | ❌ Not acquired | Public statements, connections |
| **Academic Publications** | OpenAlex | ❌ Not acquired | Research affiliations |
| **Patent Records** | USPTO | ❌ Not acquired | Technology connections |
| **Trademark Records** | USPTO | ❌ Not acquired | Business branding |
| **Campaign Finance (State)** | FollowTheMoney | ❌ Not acquired | State-level political donations |
| **Contract Awards** | USASpending.gov | ❌ Not acquired | Government contracts to Epstein entities |

### Parameter Generation Sources

For automated discovery and cross-referencing:

#### Entity Resolution Parameters
```yaml
person_identifiers:
  - Full legal name variants
  - Known aliases (from persons_registry.json: 1,614 entries)
  - Maiden names
  - Spouse names (for joint transactions)
  
organization_identifiers:
  - IRS EIN numbers (from nonprofits table: 33 entities)
  - State registration IDs
  - FEC committee IDs (from fec_committees: 23,000+ committees)
  - Shell company patterns
  
location_identifiers:
  - Property addresses (from exposed_locations: 83 locations)
  - Zillow/Property records
  - Geocoded coordinates
  
financial_identifiers:
  - Bank routing patterns
  - Cryptocurrency wallets (if any)
  - Stock CUSIPs (from congress_trading when acquired)
  - Transaction amounts (from fec_individual_contributions)
```

#### Network Discovery Rules
```yaml
co_occurrence_triggers:
  - Same flight (exposed_flights: 3,615 flights)
  - Same document mention (document_entities: 5.7M entities)
  - Same email thread (jmail_emails: 1.78M emails)
  - Same property transaction
  - Same committee donation (fec_individual_contributions)
  - Same corporate board
  - Same nonprofit board (exposed_nonprofits: 33 orgs)
  
relationship_strength:
  - Direct: Co-traveler, co-signatory, mutual mention
  - Indirect: Common associate, shared location
  - Temporal: Overlapping activities
  - Financial: Transactional relationship
```

### Data Acquisition Priority Matrix

| Priority | Dataset | Estimated Size | Effort | Impact on Discovery |
|----------|---------|----------------|--------|---------------------|
| **P0** | Offshore Leaks (ICIJ) | 2-3TB | High | Critical - shell companies |
| **P0** | SEC EDGAR (Form 3/4/5) | 500GB | Medium | High - insider trades |
| **P1** | CourtListener | 200GB | Low | High - legal proceedings |
| **P1** | IRS 990 Forms | 100GB | Medium | Medium - nonprofit flows |
| **P1** | Property Records | 50GB | High | Medium - real estate |
| **P2** | OpenCorporates | 20GB | Low | Medium - entity resolution |
| **P2** | Lobbying Disclosures | 10GB | Low | Low - influence tracking |
| **P2** | Campaign Finance (State) | 5GB | Medium | Low - state politics |

---

## Recommended Next Steps

### Priority 1: Download jmail.emails (1.78M emails)
```bash
curl -o /home/cbwinslow/workspace/epstein-data/supplementary/emails-slim.parquet \
  "https://data.jmail.world/v1/emails-slim.parquet"
```
Then import to PostgreSQL using adapted `ingest-jmail.py` script.

### Priority 2: Generate Embeddings
- Run `epstein embed` on all 2.9M pages
- Create HNSW vector index for semantic search
- Enable semantic search functionality

### Priority 3: Build Connections Graph
- Analyze document_entities (5.7M rows) to build connections
- Cross-reference with flight logs and email data
- Build relationship graph matching website's 51K connections

### Priority 4: Import Missing Data
- Import persons_registry.json (36 missing persons)
- Import extracted_entities_filtered.json (8,085 entities)
- Import phone_numbers_enriched.csv

### Priority 5: Knowledge Graph Enhancement
- Expand from 606 entities to match 1,580 persons
- Build connections from document co-occurrence
- Add flight-based connections
- Add email-based connections

---

## File Locations Reference

| Data Type | Location | Size |
|-----------|----------|------|
| Raw PDFs | `/home/cbwinslow/workspace/epstein-data/raw-files/` | 177GB |
| HF Parquet | `/home/cbwinslow/workspace/epstein-data/hf-parquet/` | 318GB |
| SQLite DBs | `/home/cbwinslow/workspace/epstein-data/databases/` | 12GB |
| Supplementary | `/home/cbwinslow/workspace/epstein-data/supplementary/` | ~22MB |
| Research Data | `~/workspace/epstein/Epstein-research-data/` | ~28MB |
| Processed Output | `/home/cbwinslow/workspace/epstein-data/processed/` | (empty, ready) |
| Knowledge Graph | `/home/cbwinslow/workspace/epstein-data/knowledge-graph/` | (empty, ready) |
| Logs | `/home/cbwinslow/workspace/epstein-data/logs/` | Variable |

---

## PostgreSQL Connection

```bash
# Connect to database
PGPASSWORD=123qweasd psql -h localhost -U cbwinslow -d epstein

# Example queries
SELECT COUNT(*) FROM documents;
SELECT COUNT(*) FROM pages WHERE embedding IS NOT NULL;
SELECT * FROM exposed_persons LIMIT 10;
```

---

*This inventory should be updated as data is added or modified.*
