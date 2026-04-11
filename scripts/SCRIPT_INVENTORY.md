# Script Inventory - Ingestion Folder
## Generated: 2026-04-10
## Purpose: Catalog all scripts before cleanup

## WORKING / ACTIVE SCRIPTS (Keep)

### News Enrichment
- `enrich_with_trafilatura.py` - ✅ Current working enrichment script
- `article_ingestion_pipeline.py` - ✅ Existing metadata extraction

### Download Scripts (FEC/ICIJ/jMail)
- `download_fec_bulk.py` - FEC data downloader
- `download_icij.py` - ICIJ offshore leaks downloader
- `download_jmail_icij.py` - JMail data downloader
- `download_manager.py` - General download manager

### Import Scripts
- `import_fbi_files.py` - FBI vault file import
- `import_fbi_vault.py` - FBI vault import
- `import_all_json.py` - Generic JSON importer

### Batch Processing
- `batch_fec_ingest.py` / `batch_fec_ingest_parallel.py` - FEC data ingestion
- `batch_cm_ingest_parallel.py` - Committee data
- `batch_cn_ingest_parallel.py` - Candidate data
- `batch_ingest_historical.py` - Historical data batch ingest

### Collection
- `collect_news_sources.py` - News source discovery
- `fetch_epstein_exposed.py` - Epstein exposed data fetcher

---

## ARCHIVED SCRIPTS (Moved to archive/)

### Failed/Broken Frameworks
- `collect_epstein_trafilatura.py` - ❌ Broken (Google News redirect issue)
- `collect_epstein_articles.py` - ❌ Part of failed framework
- `news_ingestion_framework.py` - ❌ Over-engineered, didn't work
- `phase1_discovery.py` - ❌ Part of 3-phase pipeline, never worked
- `phase3_extraction.py` - ❌ Part of 3-phase pipeline, never worked
- `run_pipeline.py` - ❌ Orchestrator for broken pipeline

### Deprecated/Old Versions
- `collect_historical_data.py` - Old collection script
- `collect_historical_v2.py` - Old collection v2
- `run_full_collection.py` - Old orchestrator
- `run_news_ingestion.py` - Old runner
- `run_media_acquisition.py` - Old media runner
- `run_media_collection.py` - Old collection runner
- `staged_news_ingestion.py` - Staged approach (deprecated)

### Duplicate Download Scripts
- `download_cdn.py` - CDN download (duplicate)
- `download_chunked.py` - Chunked download (duplicate)
- `download_doj.py` - DOJ download (use download_manager)
- `download_hf.py` / `download_huggingface.py` - HuggingFace (duplicate)
- `download_icij_requests.py` / `download_icij_simple.py` - ICIJ variants
- `download_orchestrator.py` - Orchestrator (use download_manager)
- `download_with_headers.py` - Header download (duplicate)
- `download_more_datasets.py` / `download_new_hf_datasets.py` - Dataset variants
- `download_politicians_financial.py` - Financial data (old)
- `download_gov_data.py` - Generic gov data (old)
- `download_all_datasets.py` - All datasets (use specific scripts)
- `download_fbi_vault.py` - FBI vault (use import_fbi_vault)
- `download_jmail_with_headers.py` - JMail variant

### Other Deprecated
- `epstein_exposed_emails.py` - Old email fetcher
- `fec_downloader.py` - Old FEC downloader
- `fec_fast_ingest.py` - Old FEC ingest
- `fec_ingest_cm.py` / `fec_ingest_cn.py` - Old FEC variants
- `batch_json_ingest.py` - Old JSON ingest
- `import_kabasshouse.py` - Old import
- `import_local_data.py` - Old local import
- `import_sqlite_databases.py` / `import_sqlite_databases_v2.py` - Old SQLite imports
- `import_jmail_documents.py` / `import_jmail_emails.py` / `import_jmail_full.py` - Old JMail (use download_jmail_icij + batch)
- `import_jmail_supplementary.py` - Old supplementary
- `mega_parallel_ingestion.py` - Over-engineered
- `orchestrate_historical_collection.py` - Old orchestrator
- `postgresql_processor.py` - Old processor
- `run_downloads.py` - Old download runner

---

## UNCATEGORIZED (Need Review)

- `megaparse_content_ingestion.py` - ?
- `test_api.py` - Test script
- `update_content_pipeline.py` - Content pipeline
- `ingest_all_epstein_data.py` - Master ingest
- `verify_database.py` - Verification script

---

## CLEANUP RULES

### BEFORE ARCHIVING:
1. ✅ Check if script is referenced in AGENTS.md
2. ✅ Check if script is imported by other scripts
3. ✅ Check if script has been run recently
4. ✅ Make backup copy

### ARCHIVE LOCATION:
- `scripts/ingestion/archive/` for broken/deprecated
- `scripts/ingestion/legacy/` for old but potentially useful

### NEVER ARCHIVE:
- Scripts currently in use
- Scripts referenced in documentation
- Import dependencies of working scripts
