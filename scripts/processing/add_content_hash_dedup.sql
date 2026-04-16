-- Content Hash Deduplication System for Epstein Pages
-- Run this to add content hash and identify duplicates

-- 1. Add content_hash column to pages table
ALTER TABLE pages ADD COLUMN IF NOT EXISTS content_hash VARCHAR(64);

-- 2. Create index for fast duplicate lookup
CREATE INDEX IF NOT EXISTS idx_pages_content_hash ON pages(content_hash) 
WHERE content_hash IS NOT NULL;

-- 3. Populate content_hash for existing pages
-- Use MD5 for speed, SHA-256 for cryptographic security if needed
UPDATE pages 
SET content_hash = MD5(text_content) 
WHERE text_content IS NOT NULL 
  AND content_hash IS NULL;

-- 4. Create duplicate detection view
CREATE OR REPLACE VIEW v_duplicate_pages AS
SELECT 
    content_hash,
    COUNT(*) as duplicate_count,
    MIN(id) as canonical_page_id,
    ARRAY_AGG(id ORDER BY id) as all_page_ids,
    ARRAY_AGG(DISTINCT efta_number ORDER BY efta_number) as source_documents,
    LEFT(MAX(text_content), 200) as sample_text
FROM pages 
WHERE content_hash IS NOT NULL
GROUP BY content_hash
HAVING COUNT(*) > 1;

-- 5. Create view for pages that need embeddings (deduplicated)
CREATE OR REPLACE VIEW v_pages_need_embeddings AS
SELECT 
    p.id,
    p.efta_number,
    p.page_number,
    p.text_content,
    p.content_hash,
    CASE 
        WHEN pe.page_id IS NOT NULL THEN 'Has MiniLM embedding'
        WHEN p.rtx3060_embedding IS NOT NULL THEN 'Has Nomic embedding'
        ELSE 'No embedding'
    END as embedding_status,
    LENGTH(p.text_content) as text_length
FROM pages p
LEFT JOIN page_embeddings pe ON p.id = pe.page_id
WHERE p.text_content IS NOT NULL
  AND pe.page_id IS NULL  -- No MiniLM embedding
  AND p.rtx3060_embedding IS NULL  -- No Nomic embedding
  AND p.id IN (
      -- Only the canonical (first) page for each unique content
      SELECT MIN(id) 
      FROM pages 
      WHERE content_hash IS NOT NULL
      GROUP BY content_hash
  )
ORDER BY p.id;

-- 6. Create summary table for tracking
CREATE TABLE IF NOT EXISTS embedding_coverage_summary (
    snapshot_date TIMESTAMPTZ DEFAULT NOW(),
    total_pages INTEGER,
    unique_content_pages INTEGER,
    duplicate_pages INTEGER,
    with_minilm_embedding INTEGER,
    with_nomic_embedding INTEGER,
    with_both_embeddings INTEGER,
    needing_embeddings INTEGER
);

-- 7. Insert current snapshot
INSERT INTO embedding_coverage_summary (
    total_pages,
    unique_content_pages,
    duplicate_pages,
    with_minilm_embedding,
    with_nomic_embedding,
    with_both_embeddings,
    needing_embeddings
)
SELECT 
    (SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL),
    (SELECT COUNT(DISTINCT content_hash) FROM pages WHERE content_hash IS NOT NULL),
    (SELECT COUNT(*) - COUNT(DISTINCT content_hash) FROM pages WHERE content_hash IS NOT NULL),
    (SELECT COUNT(DISTINCT page_id) FROM page_embeddings),
    (SELECT COUNT(*) FROM pages WHERE rtx3060_embedding IS NOT NULL),
    (SELECT COUNT(*) FROM pages p JOIN page_embeddings pe ON p.id = pe.page_id WHERE p.rtx3060_embedding IS NOT NULL),
    (SELECT COUNT(*) FROM v_pages_need_embeddings);

-- 8. Report results
SELECT 'Content hash deduplication system created' as status;
SELECT * FROM embedding_coverage_summary ORDER BY snapshot_date DESC LIMIT 1;
