# Data Gaps and Remaining Work

> **Status:** Active tracking document  
> **Created:** March 31, 2026  
> **Purpose:** Track what's downloaded vs loaded, identify gaps, plan remaining work

---

## Executive Summary

**Current State:**
- **78 tables** in PostgreSQL (~42GB)
- **~1.4M documents** loaded from datasets 1-12
- **~2.9M pages** with OCR text
- **~5.7M extracted entities**

**Major Gaps:**
- Missing **datasets 13-14** from DOJ (if released)
- **Embeddings** are mixed models (blocked - see EMBEDDING_STANDARDIZATION_PLAN.md)
- **Supplementary data** uses incompatible embedding models
- **Relationships/FKs** not enforced (data quality risk)

---

## Download Status: Raw Files

Location: `/home/cbwinslow/workspace/epstein-data/raw-files/`

| Dataset | Files Downloaded | In DB | Status | Notes |
|---------|-----------------|-------|--------|-------|
| data1 | 466,181 | 3,158 | ⚠️ Gap | Only 0.7% in DB |
| data2 | Unknown | 574 | ⚠️ Check | Need file count |
| data3 | Unknown | 67 | ⚠️ Check | Need file count |
| data4 | Unknown | 152 | ⚠️ Check | Need file count |
| data5 | Unknown | 120 | ⚠️ Check | Need file count |
| data6 | Unknown | 13 | ⚠️ Check | Need file count |
| data7 | Unknown | 17 | ⚠️ Check | Need file count |
| data8 | Unknown | 10,595 | ⚠️ Check | Need file count |
| data9 | ~500K | 531,284 | ✅ Good | ~100% loaded |
| data10 | ~500K | 503,154 | ✅ Good | ~100% loaded |
| data11 | ~331K | 331,655 | ✅ Good | ~100% loaded |
| data12 | 12K | 12,080 | ✅ Good | ~100% loaded |
| data13 | ? | - | ❓ Unknown | Check DOJ site |
| data14 | ? | - | ❓ Unknown | Check DOJ site |

**Action Needed:** Check if data13, data14 exist on DOJ site

---

## Database Views Created

File: `migrations/002_views_and_validation.sql`

### Views for Analysis

| View | Purpose | Use Case |
|------|---------|----------|
| `v_document_summary` | Doc + page count + embeddings | Dashboard overview |
| `v_pages_missing_embeddings` | Ready-to-embed pages | Batch processing |
| `v_entity_frequency` | Most common entities | Entity analysis |
| `v_email_document_links` | Emails mentioning docs | Cross-reference |
| `v_document_relationships` | Docs sharing entities | Relationship graph |
| `v_document_redactions` | Redaction stats per doc | Redaction analysis |
| `v_communication_network` | Email participant network | Network analysis |
| `v_dataset_status` | Completeness by dataset | Data quality check |
| `v_duplicate_candidates` | Potential duplicates | Deduplication |
| `v_cross_source_persons` | Persons in multiple sources | Entity resolution |
| `v_flight_analysis` | Flight passenger breakdown | Flight analysis |

### Validation Functions

| Function | Purpose |
|----------|---------|
| `validate_efta_number(efta)` | Check EFTA format (EFTA + 8 digits) |
| `check_document_completeness(id)` | Return validation status for doc |

---

## Data Quality Issues

### Critical Issues

1. **Mixed Embedding Models** (BLOCKS SEMANTIC SEARCH)
   - `page_embeddings`: 1.5M MiniLM + 2K nomic (incompatible)
   - `kabasshouse_chunk_embeddings`: 1.5M Gemini 768-dim
   - `house_oversight_embeddings`: 69K HuggingFace 768-dim
   - `fbi_embeddings`: 12K unknown model

2. **Missing Foreign Keys**
   - `pages.document_id` → `documents.id` (not enforced)
   - `document_entities.document_id` → `documents.id` (not enforced)
   - Risk: Orphaned records, referential integrity violations

3. **Data1 Under-represented**
   - 466K files downloaded, only 3K in DB
   - Need to re-import or check OCR status

### Medium Priority

4. **No Unique Constraints**
   - `documents.efta_number` allows duplicates
   - `pages.efta_number + page_number` not unique
   - Risk: Duplicate documents/pages

5. **Missing Required Fields**
   - Some documents lack `dataset` value
   - Some pages lack `text_content`
   - Need validation rules

---

## Remaining Downloads

### Potential Sources

1. **DOJ Datasets 13-14**
   - Check: https://www.justice.gov/usao-sdny/epstein-ghislaine-maxwell-unsealed-documents
   - May have been released after initial downloads
   - Need to check `epstein-ripper` status

2. **Media Files from DOJ Library**
   - Audio recordings (interviews, depositions)
   - Video files
   - High-resolution images
   - Location: Check `EpsteinLibraryMediaScraper` results

3. **FBI Vault Additional**
   - Current: 22 documents (1,344 pages)
   - Check if more released

4. **House Oversight**
   - Current: ~69K embeddings imported
   - Raw documents available?

---

## Referential Integrity Plan

### Tables Needing Foreign Keys

```sql
-- Priority 1: Core relationships
ALTER TABLE pages 
    ADD CONSTRAINT fk_pages_documents 
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;

ALTER TABLE document_entities 
    ADD CONSTRAINT fk_doc_entities_documents 
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;

ALTER TABLE page_embeddings 
    ADD CONSTRAINT fk_page_embeddings_pages 
    FOREIGN KEY (page_id) REFERENCES pages(id) ON DELETE CASCADE;

ALTER TABLE redactions 
    ADD CONSTRAINT fk_redactions_documents 
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;

-- Priority 2: Supporting tables
ALTER TABLE document_classification 
    ADD CONSTRAINT fk_doc_class_documents 
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;

ALTER TABLE document_summary 
    ADD CONSTRAINT fk_doc_summary_documents 
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;
```

### Validation Steps Before Adding FKs

```sql
-- Check for orphaned pages
SELECT COUNT(*) FROM pages p
WHERE NOT EXISTS (SELECT 1 FROM documents d WHERE d.id = p.document_id);

-- Check for orphaned entities
SELECT COUNT(*) FROM document_entities de
WHERE NOT EXISTS (SELECT 1 FROM documents d WHERE d.id = de.document_id);

-- Check for orphaned embeddings
SELECT COUNT(*) FROM page_embeddings pe
WHERE NOT EXISTS (SELECT 1 FROM pages p WHERE p.id = pe.page_id);
```

---

## Next Steps (Priority Order)

### Immediate (This Week)

1. **Check for data13, data14**
   ```bash
   # Run from epstein-ripper directory
   python active_watcher.py --check-new-datasets
   ```

2. **Validate orphaned records**
   ```sql
   -- Run the 3 orphan check queries above
   -- Fix any issues before adding FKs
   ```

3. **Apply database views**
   ```bash
   psql -f migrations/002_views_and_validation.sql
   ```

4. **Check data1 import status**
   ```sql
   SELECT dataset, COUNT(*) FROM documents WHERE dataset = 1 GROUP BY dataset;
   SELECT COUNT(*) FROM file_registry WHERE path LIKE '%/data1/%';
   ```

### Short-term (Next 2 Weeks)

5. **Add foreign key constraints**
   - After verifying no orphans
   - Start with non-critical tables
   - Test deletes work as expected

6. **Add unique constraints**
   ```sql
   -- Example
   CREATE UNIQUE INDEX idx_unique_efta 
   ON documents(efta_number) 
   WHERE efta_number IS NOT NULL;
   ```

7. **Enable document validation trigger**
   - Uncomment in `002_views_and_validation.sql`
   - Test with INSERT/UPDATE

### Medium-term (After Data Complete)

8. **Standardize embeddings**
   - See `EMBEDDING_STANDARDIZATION_PLAN.md`
   - Regenerate ALL with nomic 384-dim
   - Use RTX 3060 (overnight run)

9. **Download media files**
   - Audio/video from DOJ
   - Run transcription
   - Add to `transcripts` table

10. **Final validation**
    - Run `check_document_completeness()` on sample
    - Verify all documents have text
    - Verify all pages have embeddings

---

## Metrics to Track

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Documents in DB | ~1.4M | All datasets | ⚠️ 66% |
| Pages with text | 2.9M | 100% | ✅ Good |
| Pages with embeddings | 1.5M | 100% | ⚠️ 51% |
| Embeddings unified | No | Yes (nomic) | ❌ Blocked |
| FKs enforced | 0 | 5+ | ❌ Not started |
| Views created | 0 | 11 | ✅ Done |

---

## Files/Scripts Status

| File | Purpose | Status |
|------|---------|--------|
| `migrations/002_views_and_validation.sql` | Views, functions, FKs | ✅ Ready to apply |
| `docs/EMBEDDING_STANDARDIZATION_PLAN.md` | Embedding migration | ✅ Documented |
| `docs/DATA_INVENTORY.md` | Full data inventory | ⚠️ Needs update |
| `scripts/generate_page_embeddings_v2.py` | Linux K80 version | ✅ Ready |
| `C:\Users\blain\epstein_scripts\generate_embeddings.py` | Windows RTX 3060 | ✅ Ready |
| `epstein-ripper/active_watcher.py` | DOJ downloader | ❓ Check status |

---

## Notes

- **RTX 3060 machine**: `192.168.4.25` (user: `blain`, Python 3.11, PyTorch CUDA 12.1 ready)
- **PostgreSQL**: `192.168.4.101:5432` (configured for Windows access)
- **Raw files**: `/home/cbwinslow/workspace/epstein-data/raw-files/` (datasets 1-12 present)
- **Total DB size**: ~42GB (78 tables, ~36M rows across all tables)
