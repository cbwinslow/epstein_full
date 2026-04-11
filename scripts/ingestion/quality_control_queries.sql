-- Quality Control Queries for Enriched Articles
-- Run these to verify data quality after enrichment

-- 1. Overall Statistics
SELECT 
    COUNT(*) as total_articles,
    COUNT(CASE WHEN word_count > 100 THEN 1 END) as enriched,
    COUNT(CASE WHEN word_count IS NULL OR word_count < 100 THEN 1 END) as pending,
    ROUND(COUNT(CASE WHEN word_count > 100 THEN 1 END) * 100.0 / COUNT(*), 1) as enrichment_rate,
    AVG(word_count) as avg_word_count,
    MAX(word_count) as max_word_count,
    MIN(word_count) as min_word_count
FROM media_news_articles;

-- 2. Articles by Word Count Category
SELECT 
    CASE 
        WHEN word_count < 100 THEN 'Short (<100)'
        WHEN word_count BETWEEN 100 AND 500 THEN 'Medium (100-500)'
        WHEN word_count BETWEEN 501 AND 2000 THEN 'Long (500-2000)'
        ELSE 'Very Long (2000+)'
    END as size_category,
    COUNT(*) as article_count,
    AVG(word_count) as avg_words
FROM media_news_articles
WHERE word_count > 0
GROUP BY 1
ORDER BY MIN(word_count);

-- 3. Find Junk/Ad Articles (to remove)
SELECT id, title, word_count, source_domain, LEFT(content, 200) as content_preview
FROM media_news_articles
WHERE content LIKE '%cookie%' 
   OR content LIKE '%GDPR%' 
   OR content LIKE '%browser check%'
   OR content LIKE '%ad blocker%'
   OR content LIKE '%subscribe%'
   OR content LIKE '%paywall%'
   OR title LIKE '%cookie%'
   OR title LIKE '%browser check%'
LIMIT 20;

-- 4. Find Wrong Person Articles (false positives)
SELECT id, title, word_count, source_domain, content
FROM media_news_articles
WHERE (title ILIKE '%michal epstein%' 
   OR title ILIKE '%theo epstein%'
   OR title ILIKE '%boris epstein%'
   OR title ILIKE '%epstein island%'
   OR content ILIKE '%michal epstein%'
   OR content ILIKE '%theo epstein%'
   OR content ILIKE '%fenway%')
AND title NOT ILIKE '%jeffrey%';

-- 5. Articles Missing Critical Metadata
SELECT id, title, word_count, authors, publish_date, language
FROM media_news_articles
WHERE word_count > 100
  AND (authors IS NULL OR authors = '{}')
  AND publish_date IS NULL
ORDER BY word_count DESC
LIMIT 20;

-- 6. Check for Duplicates by Fingerprint
SELECT 
    all_topics->>'fingerprint' as fingerprint,
    COUNT(*) as count,
    STRING_AGG(DISTINCT title, ' | ' ORDER BY title) as titles
FROM media_news_articles
WHERE word_count > 100
  AND all_topics->>'fingerprint' IS NOT NULL
GROUP BY all_topics->>'fingerprint'
HAVING COUNT(*) > 1
LIMIT 20;

-- 7. Articles by Source Domain (top 20)
SELECT 
    source_domain,
    COUNT(*) as article_count,
    AVG(word_count) as avg_words,
    COUNT(CASE WHEN word_count > 100 THEN 1 END) as enriched_count
FROM media_news_articles
GROUP BY source_domain
ORDER BY article_count DESC
LIMIT 20;

-- 8. Articles by Language
SELECT 
    COALESCE(language, 'unknown') as lang,
    COUNT(*) as count,
    AVG(word_count) as avg_words
FROM media_news_articles
WHERE word_count > 100
GROUP BY language
ORDER BY count DESC;

-- 9. Recent Enrichments (last hour)
SELECT 
    id, 
    title, 
    word_count, 
    authors, 
    language,
    source_domain,
    collected_at
FROM media_news_articles
WHERE collected_at > NOW() - INTERVAL '1 hour'
  AND word_count > 100
ORDER BY collected_at DESC
LIMIT 20;

-- 10. Articles with Images
SELECT 
    id,
    title,
    word_count,
    all_topics->>'image_url' as image_url,
    all_topics->>'hostname' as hostname
FROM media_news_articles
WHERE word_count > 100
  AND (all_topics->>'image_url' IS NOT NULL OR all_topics->>'image_urls' != '[]')
LIMIT 20;

-- 11. Quality Score Distribution
-- High quality = >500 words, has author, has date
SELECT 
    CASE 
        WHEN word_count > 500 AND authors IS NOT NULL AND publish_date IS NOT NULL THEN 'High Quality'
        WHEN word_count > 200 AND (authors IS NOT NULL OR publish_date IS NOT NULL) THEN 'Medium Quality'
        WHEN word_count > 100 THEN 'Basic Quality'
        ELSE 'Low Quality'
    END as quality_tier,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM media_news_articles WHERE word_count > 100), 1) as percentage
FROM media_news_articles
WHERE word_count > 100
GROUP BY 1
ORDER BY MIN(word_count) DESC;

-- 12. Delete Commands for Junk Articles (review first!)
-- Uncomment and run after reviewing:
-- DELETE FROM media_news_articles 
-- WHERE content LIKE '%cookie%' 
--    OR content LIKE '%browser check%'
--    OR content LIKE '%GDPR%'
--    OR title ILIKE '%michal epstein%'
--    OR title ILIKE '%theo epstein%'
--    OR title ILIKE '%browser check%';

-- 13. Export Quality Report
-- \copy (SELECT id, title, word_count, source_domain, authors, language, all_topics->>'extraction_method' as method FROM media_news_articles WHERE word_count > 100) TO '/tmp/enriched_articles_report.csv' CSV HEADER;
