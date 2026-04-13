# Duplicate Analysis Report
**Date:** April 13, 2026  
**Purpose:** Find duplicates and overlaps across all Epstein datasets

---

## 📊 Summary

**Total Filesystem Data:** 17.41 GB across 2,092 files  
**Total SQL Records:** 4M+ records across multiple tables  
**Duplicate Issues Found:** 3 critical overlaps

---

## 🔍 Key Findings

### 1. CRITICAL: Email Threads = 100% Duplicate

| Table | Records | Overlap | Status |
|-------|---------|---------|--------|
| `hf_email_threads` | 5,082 | **5,082 (100%)** | **DELETE** - Same as house_oversight_emails |
| `house_oversight_emails` | 5,082 | **5,082 (100%)** | Keep - Original source |

**Evidence:**
- All 5,082 thread_ids exist in both tables
- Same subjects, senders, recipients
- Source: Both from `notesbymuneeb/epstein-emails` (different formats)

**Recommendation:** Drop `hf_email_threads`, keep `house_oversight_emails`

---

### 2. FILES BY EXTENSION (Filesystem)

| Extension | Count | Likely Content |
|-----------|-------|----------------|
| `.incomplete` | 1,260 | Failed/partial downloads |
| `.metadata` | 366 | Dataset metadata |
| `.pdf` | 355 | FBI files, documents |
| `.parquet` | 35 | Structured data tables |
| `.json` | 3 | Configuration/metadata |
| `.jsonl` | 3 | Line-delimited JSON |

**⚠️ Note:** 1,260 `.incomplete` files = 60% of filesystem = download artifacts

---

### 3. DATASET-BY-DATASET ANALYSIS

#### ✅ epstein-files-20k (teyler/epstein-files-20k)
**Filesystem:** 127 MB (2 files)  
**SQL:** `hf_epstein_files_20k` - 2,136,420 records  
**Status:** ✅ Complete, no duplicates

#### ✅ House Oversight TXT
**Filesystem:** 100.7 MB (7 files)  
**SQL:** `hf_house_oversight_docs` - 1,791,798 records  
**Status:** ✅ Complete, unique data

#### ⚠️ Email Threads (PARQUET)
**Filesystem:** 4.4 MB (7 files)  
**SQL:** `hf_email_threads` - 5,082 records  
**Status:** ❌ **DUPLICATE** - Same as house_oversight_emails  
**Action:** Drop table, keep files for reference only

#### 🔄 OCR Complete
**Filesystem:** 1,348.9 MB (1 file)  
**SQL:** `hf_ocr_complete` - Importing  
**Status:** 🔄 Running  
**Unique:** OCR text from 20K documents

#### 📁 Embeddings
**Filesystem:** 340.9 MB (1 file)  
**SQL:** ⏳ Not imported  
**Status:** Ready to import  
**Unique:** Vector embeddings (different from house_oversight_embeddings)

#### 📁 Epstein Data Text
**Filesystem:** 2,198.1 MB (17 files)  
**SQL:** ⏳ Not imported  
**Status:** Ready to import  
**Unique:** Extracted text content

#### 📁 Images (2 datasets)
**Filesystem:** 4,891.9 MB + 4,273.2 MB = 9.17 GB  
**SQL:** ⏳ Metadata not imported  
**Status:** Keep on disk, import metadata only  

#### 📁 FBI Files
**Filesystem:** 4,541.4 MB (355 PDFs + metadata)  
**SQL:** `fbi_vault_pages` - 1,426 records  
**Status:** ✅ Metadata in SQL, PDFs on disk

#### 📁 Full Index
**Filesystem:** 4.2 MB (32 files)  
**SQL:** `full_epstein_index` - 8,531 records  
**Status:** ✅ Already imported

---

## 🎯 POTENTIAL DUPLICATES TO INVESTIGATE

### Filename Pattern Overlaps:
1. **EFT-XXXXX pattern** - Document IDs appearing in:
   - `hf_house_oversight_docs.doc_id`
   - `full_epstein_index` (potentially)
   - Need to check overlap

2. **Content hash duplicates** - Same document, different sources:
   - OCR text vs original text
   - House Oversight vs DOJ releases
   - Need content similarity analysis

3. **Cross-reference duplicates**:
   - `hf_epstein_files_20k` contains 2M docs
   - `full_epstein_index` contains 8K docs
   - Likely overlap: Index is subset of 20K

---

## 📋 SQL QUERIES FOR DEEPER ANALYSIS

Run these to find more duplicates:

```sql
-- Check EFT document ID overlap
SELECT 
    doc_id,
    (SELECT COUNT(*) FROM full_epstein_index WHERE id::text = doc_id) as in_full_index
FROM hf_house_oversight_docs
WHERE doc_id LIKE 'EFT%'
LIMIT 100;

-- Content similarity check (sampling)
SELECT 
    hf.id,
    hf.content as content_20k,
    ho.title as content_ho
FROM hf_epstein_files_20k hf
JOIN hf_house_oversight_docs ho 
    ON hf.content ILIKE '%' || ho.title || '%'
LIMIT 10;

-- Check if OCR duplicates original text
SELECT 
    o.doc_id,
    o.ocr_text,
    e.content as original_text
FROM hf_ocr_complete o
JOIN hf_epstein_files_20k e ON o.doc_id = e.id::text
LIMIT 5;
```

---

## 🗑️ CLEANUP RECOMMENDATIONS

### Immediate Actions:
1. **Drop `hf_email_threads`** - 100% duplicate
   ```sql
   DROP TABLE hf_email_threads;
   ```

2. **Clean incomplete downloads:**
   ```bash
   find /home/cbwinslow/workspace/epstein-data -name "*.incomplete" -delete
   ```

3. **Remove 366 .metadata files** (if not needed):
   ```bash
   find /home/cbwinslow/workspace/epstein-data -name "*.metadata" -delete
   ```

### After Cleanup:
- **Filesystem:** ~6.5 GB actual data (from 17.4 GB)
- **SQL:** ~4M records (from 4M, after removing 5K duplicates)

---

## 📁 FILES CREATED

1. `scripts/duplicate_analysis_queries.sql` - SQL queries for analysis
2. `scripts/scan_filesystem.py` - Filesystem scanner
3. `scripts/analyze_duplicates.py` - Python duplicate detector
4. `/tmp/filesystem_scan.json` - Detailed filesystem data
5. `/tmp/duplicate_analysis.json` - SQL duplicate analysis

---

## 🔮 NEXT STEPS

1. Confirm deletion of `hf_email_threads`
2. Run content similarity analysis on samples
3. Check EFT ID overlaps between tables
4. Import remaining datasets (Embeddings, Epstein Data Text)
5. Clean up .incomplete and .metadata files
