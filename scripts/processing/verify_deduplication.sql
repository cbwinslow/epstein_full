-- Deduplication Verification Script
-- Run this BEFORE trusting deduplication results

-- ============================================
-- 1. CHECK FOR PROBLEMATIC DUPLICATE PATTERNS
-- ============================================

-- 1a. Find "suspicious" duplicates (same hash, different EFTA numbers)
-- These might be legitimate duplicates OR false positives
CREATE OR REPLACE VIEW v_suspicious_duplicates AS
SELECT 
    MD5(p1.text_content) as content_hash,
    p1.id as page1_id,
    p1.efta_number as efta1,
    p1.page_number as page_num1,
    p2.id as page2_id,
    p2.efta_number as efta2,
    p2.page_number as page_num2,
    LENGTH(p1.text_content) as text_length,
    LEFT(p1.text_content, 100) as sample_text,
    CASE 
        WHEN p1.efta_number = p2.efta_number THEN 'SAME_DOCUMENT'
        ELSE 'DIFFERENT_DOCUMENTS'
    END as duplicate_type
FROM pages p1
JOIN pages p2 ON MD5(p1.text_content) = MD5(p2.text_content)
WHERE p1.id < p2.id  -- Avoid duplicates in the result
    AND p1.text_content IS NOT NULL
    AND LENGTH(p1.text_content) > 10  -- Not blank/empty
LIMIT 1000;

-- 1b. Find very short text that might be boilerplate
CREATE OR REPLACE VIEW v_short_text_duplicates AS
SELECT 
    MD5(text_content) as content_hash,
    COUNT(*) as occurrence_count,
    MIN(LENGTH(text_content)) as text_length,
    STRING_AGG(DISTINCT efta_number, ', ') as sample_efta_numbers,
    LEFT(MAX(text_content), 200) as sample_text
FROM pages
WHERE text_content IS NOT NULL
    AND LENGTH(text_content) < 100  -- Very short text
GROUP BY MD5(text_content)
HAVING COUNT(*) > 10  -- Appears more than 10 times
ORDER BY COUNT(*) DESC;

-- 1c. Find "identical except page number" patterns
CREATE OR REPLACE VIEW v_page_number_duplicates AS
SELECT 
    p1.efta_number,
    p1.page_number as page1,
    p2.page_number as page2,
    LENGTH(p1.text_content) as text_length,
    MD5(p1.text_content) as hash1,
    MD5(p2.text_content) as hash2,
    CASE 
        WHEN p1.text_content = p2.text_content THEN 'EXACT_MATCH'
        ELSE 'NEAR_MATCH'
    END as match_type
FROM pages p1
JOIN pages p2 ON p1.efta_number = p2.efta_number 
    AND p1.text_content IS NOT NULL
    AND p2.text_content IS NOT NULL
    AND p1.page_number < p2.page_number
    AND LENGTH(p1.text_content) > 50
WHERE MD5(p1.text_content) = MD5(p2.text_content)
ORDER BY p1.efta_number, p1.page_number
LIMIT 100;

-- ============================================
-- 2. STATISTICAL VALIDATION
-- ============================================

-- 2a. Hash collision probability check
-- With 2.9M pages, collision probability is ~2^-128 (negligible)
-- But let's verify no MD5 collisions on different text
CREATE OR REPLACE VIEW v_md5_collision_check AS
SELECT 
    MD5(text_content) as content_hash,
    COUNT(DISTINCT text_content) as unique_text_variants,
    COUNT(*) as total_pages,
    STRING_AGG(DISTINCT LEFT(text_content, 50), ' | ') as samples
FROM pages
WHERE text_content IS NOT NULL
GROUP BY MD5(text_content)
HAVING COUNT(DISTINCT text_content) > 1;

-- 2b. Distribution analysis - are duplicates evenly distributed?
CREATE OR REPLACE VIEW v_duplicate_distribution AS
SELECT 
    dataset,
    COUNT(*) as total_pages,
    COUNT(DISTINCT MD5(text_content)) as unique_hashes,
    COUNT(*) - COUNT(DISTINCT MD5(text_content)) as duplicate_count,
    ROUND((COUNT(*) - COUNT(DISTINCT MD5(text_content)))::numeric / COUNT(*) * 100, 2) as dup_pct
FROM pages
WHERE text_content IS NOT NULL
    AND dataset IS NOT NULL
GROUP BY dataset
ORDER BY duplicate_count DESC;

-- ============================================
-- 3. SAMPLING FOR MANUAL VERIFICATION
-- ============================================

-- 3a. Get random sample of duplicates for manual review
CREATE OR REPLACE VIEW v_duplicate_sample_for_review AS
SELECT 
    MD5(p.text_content) as content_hash,
    p.id,
    p.efta_number,
    p.page_number,
    p.dataset,
    LENGTH(p.text_content) as text_length,
    p.text_content
FROM pages p
WHERE p.text_content IS NOT NULL
    AND MD5(p.text_content) IN (
        -- Subquery: find hashes that appear more than once
        SELECT MD5(text_content)
        FROM pages
        WHERE text_content IS NOT NULL
            AND LENGTH(text_content) > 50  -- Skip very short
        GROUP BY MD5(text_content)
        HAVING COUNT(*) > 1
    )
ORDER BY MD5(p.text_content), p.efta_number, p.page_number
LIMIT 100;

-- ============================================
-- 4. SAFE DEDUPLICATION STRATEGY
-- ============================================

-- 4a. Conservative deduplication (only within same EFTA, same text)
-- This is 100% safe - same document, same text = definitely duplicate
CREATE OR REPLACE VIEW v_safe_duplicates_same_doc AS
SELECT 
    efta_number,
    MD5(text_content) as content_hash,
    MIN(id) as canonical_page_id,
    ARRAY_AGG(id ORDER BY id) as all_page_ids,
    COUNT(*) - 1 as duplicate_count,  -- Exclude canonical
    MIN(page_number) as first_page,
    MAX(page_number) as last_page
FROM pages
WHERE text_content IS NOT NULL
GROUP BY efta_number, MD5(text_content)
HAVING COUNT(*) > 1;

-- 4b. Aggressive deduplication (across different EFTA numbers)
-- Review this carefully - might be false positives
CREATE OR REPLACE VIEW v_aggressive_duplicates_across_docs AS
SELECT 
    MD5(text_content) as content_hash,
    MIN(id) as canonical_page_id,
    ARRAY_AGG(id ORDER BY id) as all_page_ids,
    COUNT(*) - 1 as duplicate_count,
    STRING_AGG(DISTINCT efta_number, ', ' ORDER BY efta_number) as source_documents,
    COUNT(DISTINCT efta_number) as num_source_docs,
    MIN(LENGTH(text_content)) as text_length,
    LEFT(MAX(text_content), 100) as sample_text
FROM pages
WHERE text_content IS NOT NULL
    AND LENGTH(text_content) > 100  -- Skip very short text (likely boilerplate)
GROUP BY MD5(text_content)
HAVING COUNT(*) > 1
    AND COUNT(DISTINCT efta_number) > 1;  -- Across different documents

-- ============================================
-- 5. RECOMMENDATION QUERY
-- ============================================

-- Create a final recommendation view
CREATE OR REPLACE VIEW v_dedup_recommendation AS
WITH stats AS (
    SELECT 
        COUNT(*) as total_pages,
        COUNT(DISTINCT MD5(text_content)) as unique_hashes,
        COUNT(*) - COUNT(DISTINCT MD5(text_content)) as total_duplicates
    FROM pages
    WHERE text_content IS NOT NULL
),
safe_dedup AS (
    SELECT SUM(duplicate_count) as safe_to_remove
    FROM v_safe_duplicates_same_doc
),
aggressive_dedup AS (
    SELECT SUM(duplicate_count) as aggressive_remove
    FROM v_aggressive_duplicates_across_docs
)
SELECT 
    s.total_pages,
    s.unique_hashes,
    s.total_duplicates,
    ROUND(s.total_duplicates::numeric / s.total_pages * 100, 2) as dup_percentage,
    sd.safe_to_remove,
    ad.aggressive_remove,
    CASE 
        WHEN sd.safe_to_remove > 0 THEN 'SAFE: Remove ' || sd.safe_to_remove || ' duplicates (same document)'
        ELSE 'SAFE: No same-document duplicates found'
    END as safe_recommendation,
    CASE 
        WHEN ad.aggressive_remove > 0 THEN 'REVIEW: ' || ad.aggressive_remove || ' duplicates across documents - verify manually'
        ELSE 'No cross-document duplicates found'
    END as aggressive_recommendation
FROM stats s
CROSS JOIN safe_dedup sd
CROSS JOIN aggressive_dedup ad;

-- ============================================
-- 6. RUN VERIFICATION QUERIES
-- ============================================

-- Run these to verify before trusting deduplication:

-- Q1: How many "safe" duplicates (same document)?
-- SELECT SUM(duplicate_count) FROM v_safe_duplicates_same_doc;

-- Q2: How many "suspicious" duplicates (across documents)?
-- SELECT COUNT(*) FROM v_aggressive_duplicates_across_docs;

-- Q3: What's the sample text of suspicious duplicates?
-- SELECT * FROM v_aggressive_duplicates_across_docs LIMIT 10;

-- Q4: Overall recommendation
-- SELECT * FROM v_dedup_recommendation;

-- Q5: Short text duplicates (likely boilerplate)
-- SELECT * FROM v_short_text_duplicates LIMIT 20;

-- ============================================
-- 7. FINAL SAFE DEDUPLICATION VIEW
-- ============================================

-- This is the CONSERVATIVE approach - only dedup within same document
CREATE OR REPLACE VIEW v_pages_need_embeddings_safe AS
SELECT 
    p.id,
    p.efta_number,
    p.page_number,
    p.text_content,
    MD5(p.text_content) as content_hash,
    CASE 
        WHEN pe.page_id IS NOT NULL THEN 'Has MiniLM'
        WHEN p.rtx3060_embedding IS NOT NULL THEN 'Has Nomic'
        ELSE 'Needs embedding'
    END as status
FROM pages p
LEFT JOIN page_embeddings pe ON p.id = pe.page_id
WHERE p.text_content IS NOT NULL
    AND pe.page_id IS NULL  -- No MiniLM
    AND p.rtx3060_embedding IS NULL  -- No Nomic
    AND p.id IN (
        -- Only include pages that are "canonical" for their hash within same EFTA
        SELECT MIN(id)
        FROM pages
        WHERE text_content IS NOT NULL
        GROUP BY efta_number, MD5(text_content)
    )
ORDER BY p.id;

-- Show verification header
SELECT 'Deduplication verification views created' as status;
SELECT 'Run these queries to verify before trusting dedup:' as instruction;
SELECT '1. SELECT * FROM v_dedup_recommendation;' as query;
SELECT '2. SELECT * FROM v_short_text_duplicates LIMIT 10;' as query;
SELECT '3. SELECT * FROM v_aggressive_duplicates_across_docs LIMIT 10;' as query;
