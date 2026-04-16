# Master Registry System Guide

> **Created:** April 16, 2026  
> **Purpose:** Centralized tracking system for all data sources, embeddings, and processing operations  
> **Location:** `/home/cbwinslow/workspace/epstein/scripts/processing/create_master_registry.sql`

---

## 📊 Overview

The Master Registry System provides a single source of truth for:
- **Data Sources:** What's been downloaded, imported, processed
- **File Tracking:** Individual files with SHA-256 hashes for deduplication
- **Embeddings:** Which models, dimensions, and coverage
- **Duplicates:** Tracking and resolution of duplicate content
- **Processing:** Logs of all operations with performance metrics

---

## 🗄️ Database Tables

### 1. `master_data_registry`
**Purpose:** Track all data sources (downloads, imports)

| Column | Type | Description |
|--------|------|-------------|
| `source_name` | VARCHAR(100) | e.g., "DOJ_Epstein_Library", "jMail_Emails" |
| `source_type` | VARCHAR(50) | "DOJ", "HuggingFace", "API", "ThirdParty" |
| `source_dataset_id` | VARCHAR(100) | Dataset identifier |
| `download_status` | VARCHAR(20) | pending, downloading, complete, failed |
| `import_status` | VARCHAR(20) | pending, importing, complete, failed, partial |
| `file_count` | INTEGER | Number of files |
| `imported_records` | INTEGER | Records in database |
| `content_hash` | VARCHAR(64) | SHA-256 for integrity |

**Current Data:**
```sql
SELECT source_name, import_status, imported_records 
FROM master_data_registry 
ORDER BY imported_records DESC;
```

| Source | Status | Records |
|--------|--------|---------|
| FEC_Contributions | complete | 5,420,940 |
| ICIJ_Offshore_Leaks | complete | 3,339,272 |
| HF_epstein_files_20k | complete | 2,136,420 |
| jMail_Emails | complete | 1,783,792 |
| jMail_Documents | complete | 1,413,417 |
| DOJ_Epstein_Library | complete | 1,392,869 |
| GDELT_News | complete | 23,413 |
| FBI_Vault | partial | 1,426 |

---

### 2. `file_registry_detail`
**Purpose:** Track individual files with hashes

| Column | Type | Description |
|--------|------|-------------|
| `registry_id` | INTEGER | Links to master_data_registry |
| `filename` | VARCHAR(255) | File name |
| `md5_hash` | VARCHAR(32) | Fast hash for comparison |
| `sha256_hash` | VARCHAR(64) | Secure hash for verification |
| `efta_number` | VARCHAR(20) | Links to documents.efta_number |
| `document_id` | INTEGER | Links to documents.id |
| `page_ids` | INTEGER[] | Array of linked page IDs |
| `is_valid` | BOOLEAN | File integrity check |
| `processing_status` | VARCHAR(20) | ocr_complete, embedded, failed |

---

### 3. `embedding_registry`
**Purpose:** Track all embeddings by model

| Column | Type | Description |
|--------|------|-------------|
| `registry_id` | INTEGER | Links to data source |
| `model_name` | VARCHAR(100) | e.g., "all-MiniLM-L6-v2" |
| `model_dimensions` | INTEGER | 384, 768, 1024 |
| `compute_device` | VARCHAR(50) | "RTX3060", "K80", "CPU" |
| `total_pages` | INTEGER | Total pages processed |
| `unique_pages` | INTEGER | Deduplicated count |
| `storage_table` | VARCHAR(100) | "page_embeddings", "pages" |
| `storage_column` | VARCHAR(100) | Column name if applicable |
| `generation_status` | VARCHAR(20) | pending, generating, complete |

**Current Embeddings:**

| Model | Dimensions | Device | Status | Pages | Storage |
|-------|------------|--------|--------|-------|---------|
| all-MiniLM-L6-v2 | 384 | K80 | complete | 1,561,755 | page_embeddings |
| HuggingFace (unknown) | 768 | Pre-computed | complete | 236,174 | fbi_embeddings |
| nomic-embed-text-v2-moe | 768 | RTX3060 | in_progress | 36,700 | pages.rtx3060_embedding |

---

### 4. `duplicate_registry`
**Purpose:** Track content duplicates

| Column | Type | Description |
|--------|------|-------------|
| `content_hash` | VARCHAR(64) | MD5/SHA256 of content |
| `duplicate_type` | VARCHAR(50) | exact_file, exact_text, near_duplicate |
| `canonical_page_id` | INTEGER | Master page to keep |
| `duplicate_page_ids` | JSONB | Array of duplicate IDs |
| `duplicate_count` | INTEGER | Number of duplicates |
| `space_saved_bytes` | BIGINT | Space if duplicates removed |
| `resolution_status` | VARCHAR(20) | identified, verified, resolved |

---

### 5. `processing_log`
**Purpose:** Log all processing operations

| Column | Type | Description |
|--------|------|-------------|
| `operation_name` | VARCHAR(100) | e.g., "OCR", "NER", "Embedding Generation" |
| `status` | VARCHAR(20) | started, running, completed, failed |
| `total_items` | INTEGER | Items to process |
| `processed_items` | INTEGER | Items completed |
| `duration_seconds` | INTEGER | Time taken |
| `items_per_second` | DECIMAL | Performance |
| `gpu_device` | VARCHAR(50) | GPU used |
| `error_count` | INTEGER | Errors encountered |

---

## 📈 Views for Analysis

### `v_data_source_summary`
Summary by source type
```sql
SELECT * FROM v_data_source_summary;
```

### `v_embedding_coverage_summary`
Embedding coverage by model
```sql
SELECT * FROM v_embedding_coverage_summary;
```

### `v_duplicate_summary`
Duplicate statistics
```sql
SELECT * FROM v_duplicate_summary;
```

### `v_processing_dashboard`
Recent processing operations
```sql
SELECT * FROM v_processing_dashboard;
```

---

## 🔧 Helper Functions

### Register New Data Source
```sql
SELECT register_data_source(
    'New_HF_Dataset',           -- source_name
    'HuggingFace',              -- source_type
    'https://huggingface.co/...', -- source_url
    'dataset-id',               -- source_dataset_id
    '/path/to/files',           -- file_path
    50000,                      -- expected_records
    'Parquet',                  -- source_format
    'Description of dataset'    -- description
);
```

### Update Download Status
```sql
SELECT update_download_status(
    1,                          -- registry_id
    'complete',                 -- status
    1000,                       -- file_count
    10737418240,                -- size_bytes (10GB)
    'sha256_hash_here'          -- content_hash
);
```

### Update Import Status
```sql
SELECT update_import_status(
    1,                          -- registry_id
    'complete',                 -- status
    50000,                      -- imported_records
    0                           -- failed_records
);
```

### Register Embedding Generation
```sql
SELECT register_embedding_generation(
    1,                          -- registry_id
    'nomic-embed-text-v2-moe',  -- model_name
    768,                        -- model_dimensions
    'RTX3060',                  -- compute_device
    900000,                     -- total_pages
    'pages',                    -- storage_table
    'embedding_nomic'           -- storage_column
);
```

### Get Source Status
```sql
SELECT * FROM get_source_status('DOJ_Epstein_Library');
```

---

## 📝 Usage Examples

### Check All Data Sources
```sql
SELECT 
    source_name, 
    source_type,
    download_status,
    import_status,
    imported_records,
    (imported_records::FLOAT / NULLIF(expected_records, 0) * 100)::INT as completion_pct
FROM master_data_registry
ORDER BY imported_records DESC;
```

### Check Embedding Coverage
```sql
SELECT 
    model_name,
    model_dimensions,
    compute_device,
    generation_status,
    total_pages,
    unique_pages,
    ROUND(total_pages::numeric / 2892730 * 100, 2) as coverage_pct
FROM embedding_registry
ORDER BY total_pages DESC;
```

### Check for Duplicates
```sql
SELECT 
    duplicate_type,
    COUNT(*) as groups,
    SUM(duplicate_count) as total_duplicates,
    pg_size_pretty(SUM(space_saved_bytes)) as potential_savings
FROM duplicate_registry
WHERE resolution_status = 'identified'
GROUP BY duplicate_type;
```

### Recent Processing Activity
```sql
SELECT 
    operation_name,
    status,
    processed_items || '/' || total_items as progress,
    duration_seconds || 's' as duration,
    ROUND(items_per_second, 1) as rate,
    error_count
FROM processing_log
WHERE started_at > NOW() - INTERVAL '7 days'
ORDER BY started_at DESC;
```

---

## 🎯 Integration with Existing Systems

### With Data Inventory
The registry complements `DATA_INVENTORY_FULL.md` with:
- **Machine-readable status** (not just documentation)
- **Real-time updates** (not static snapshots)
- **Processing logs** (track what happened when)
- **Performance metrics** (track GPU hours, rates)

### With Embeddings
The registry tracks:
- **Which model** was used for each data source
- **Which pages** have embeddings vs not
- **GPU hours** spent on generation
- **Deduplication savings** (avoid embedding same content twice)

### With GitHub Issues
Link registry entries to issues:
```sql
-- Add a column for issue tracking
ALTER TABLE master_data_registry ADD COLUMN github_issue_number INTEGER;

-- Example: Link Issue #50 (RTX 3060 embeddings)
UPDATE master_data_registry 
SET github_issue_number = 50
WHERE source_name = 'DOJ_Epstein_Library';
```

---

## 🚀 Next Steps

1. **Populate file_registry_detail** - Run hash scans on raw files
2. **Run content deduplication** - Execute add_content_hash_dedup.sql
3. **Update embedding registry** - Log ongoing Nomic generation
4. **Create GitHub issue links** - Track which issues map to which sources
5. **Set up monitoring** - Alert when imports fail, embeddings stall

---

## 📚 Files Created

| File | Purpose |
|------|---------|
| `scripts/processing/create_master_registry.sql` | Creates all tables, views, functions |
| `scripts/processing/add_content_hash_dedup.sql` | Deduplication system for pages |
| `docs/EMBEDDING_MIGRATION_PLAN.md` | Strategy for handling mixed embeddings |
| `docs/MASTER_REGISTRY_GUIDE.md` | This guide |

---

*Last Updated: April 16, 2026*
