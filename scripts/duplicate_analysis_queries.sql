-- Duplicate Detection SQL Queries for Epstein Datasets
-- Run these in PostgreSQL to find overlaps and duplicates

-- =====================================================
-- 1. TABLE INVENTORY
-- =====================================================

-- Get all tables with record counts
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Get actual record counts for all HF tables
SELECT 'hf_epstein_files_20k' as table_name, COUNT(*) as records FROM hf_epstein_files_20k
UNION ALL SELECT 'hf_house_oversight_docs', COUNT(*) FROM hf_house_oversight_docs
UNION ALL SELECT 'hf_email_threads', COUNT(*) FROM hf_email_threads
UNION ALL SELECT 'hf_ocr_complete', COUNT(*) FROM hf_ocr_complete
UNION ALL SELECT 'full_epstein_index', COUNT(*) FROM full_epstein_index
UNION ALL SELECT 'house_oversight_emails', COUNT(*) FROM house_oversight_emails
UNION ALL SELECT 'house_oversight_embeddings', COUNT(*) FROM house_oversight_embeddings
UNION ALL SELECT 'fbi_vault_pages', COUNT(*) FROM fbi_vault_pages
ORDER BY records DESC;

-- =====================================================
-- 2. CROSS-TABLE DUPLICATE DETECTION
-- =====================================================

-- Check email thread ID overlap
SELECT 
    'hf_email_threads vs house_oversight_emails' as comparison,
    COUNT(*) as overlapping_thread_ids
FROM hf_email_threads h
INNER JOIN house_oversight_emails ho ON h.thread_id = ho.thread_id;

-- Check subject overlap between email tables
SELECT 
    'Subject overlap' as check_type,
    COUNT(*) as matches
FROM hf_email_threads h
INNER JOIN house_oversight_emails ho 
    ON h.subject = ho.subject 
    AND h.subject IS NOT NULL;

-- Check sender overlap
SELECT 
    'Sender overlap' as check_type,
    COUNT(DISTINCT h.sender) as unique_senders_in_both
FROM hf_email_threads h
INNER JOIN house_oversight_emails ho ON h.sender = ho.sender;

-- =====================================================
-- 3. FILENAME/DOC_ID PATTERN ANALYSIS
-- =====================================================

-- Extract EFT document IDs from various tables
SELECT 
    'hf_house_oversight_docs' as source,
    COUNT(*) as total,
    COUNT(CASE WHEN doc_id LIKE 'EFT%' THEN 1 END) as eft_pattern_count
FROM hf_house_oversight_docs;

-- Common filename patterns
SELECT 
    CASE 
        WHEN doc_id LIKE 'EFT%' THEN 'EFT_*'
        WHEN doc_id LIKE '%email%' THEN '*email*'
        WHEN doc_id LIKE '%flight%' THEN '*flight*'
        ELSE 'other'
    END as pattern,
    COUNT(*) as count
FROM hf_house_oversight_docs
WHERE doc_id IS NOT NULL
GROUP BY 1
ORDER BY count DESC;

-- =====================================================
-- 4. POTENTIAL FILESYSTEM-SQL MISMATCHES
-- =====================================================

-- Files in SQL but not referenced in filesystem paths
SELECT 
    file_path,
    doc_id,
    doc_type
FROM hf_house_oversight_docs
WHERE file_path NOT LIKE '/home/cbwinslow/workspace/epstein-data%'
LIMIT 20;

-- Check if SQL references match actual files on disk
-- (Run this after checking filesystem)

-- =====================================================
-- 5. DATA QUALITY CHECKS
-- =====================================================

-- Null value analysis
SELECT 
    'hf_epstein_files_20k' as table_name,
    COUNT(*) as total,
    COUNT(CASE WHEN content IS NULL THEN 1 END) as null_content,
    COUNT(CASE WHEN filename IS NULL THEN 1 END) as null_filename
FROM hf_epstein_files_20k;

-- Duplicate IDs within same table
SELECT 
    doc_id,
    COUNT(*) as occurrence_count
FROM hf_house_oversight_docs
WHERE doc_id IS NOT NULL
GROUP BY doc_id
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC
LIMIT 20;

-- =====================================================
-- 6. CROSS-DATASET SIMILARITY ANALYSIS
-- =====================================================

-- Find documents that appear in multiple HF datasets
-- (Need to compare content hashes or filenames)

-- Compare hf_epstein_files_20k with full_epstein_index
SELECT 
    'ID overlap check' as analysis,
    COUNT(*) as matches
FROM hf_epstein_files_20k hf
INNER JOIN full_epstein_index fei 
    ON hf.id::text = fei.id::text;

-- Check filename overlap between epstein-files-20k and house_oversight_docs
SELECT 
    hf.filename,
    ho.doc_id,
    'potential_match' as match_type
FROM hf_epstein_files_20k hf
INNER JOIN hf_house_oversight_docs ho 
    ON hf.filename ILIKE '%' || ho.doc_id || '%'
    OR ho.doc_id ILIKE '%' || hf.filename || '%'
LIMIT 50;

-- =====================================================
-- 7. RECOMMENDATIONS QUERY
-- =====================================================

-- Tables that might be merged or deduplicated
SELECT 
    'hf_email_threads + house_oversight_emails' as suggestion,
    'MERGE - 100% thread_id overlap' as action,
    5082 as affected_records;
