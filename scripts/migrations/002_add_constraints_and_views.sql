-- Migration: Add foreign keys, additional indexes, and validation constraints
-- Version: 1.1.0
-- Date: 2026-04-06

-- ============================================
-- FOREIGN KEYS
-- ============================================

-- Link articles to queue items
ALTER TABLE media_news_articles
ADD CONSTRAINT fk_articles_queue 
FOREIGN KEY (queue_id) 
REFERENCES media_collection_queue(id) 
ON DELETE SET NULL;

-- Link videos to queue items
ALTER TABLE media_videos
ADD CONSTRAINT fk_videos_queue 
FOREIGN KEY (queue_id) 
REFERENCES media_collection_queue(id) 
ON DELETE SET NULL;

-- Link documents to queue items
ALTER TABLE media_documents
ADD CONSTRAINT fk_documents_queue 
FOREIGN KEY (queue_id) 
REFERENCES media_collection_queue(id) 
ON DELETE SET NULL;

-- Link entity mentions to entities
ALTER TABLE media_entity_mentions
ADD CONSTRAINT fk_mentions_entity 
FOREIGN KEY (entity_id) 
REFERENCES media_entities(id) 
ON DELETE CASCADE;

-- ============================================
-- ADDITIONAL INDEXES FOR PERFORMANCE
-- ============================================

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_articles_domain_date 
ON media_news_articles(source_domain, publication_date DESC);

CREATE INDEX IF NOT EXISTS idx_articles_status_date 
ON media_news_articles(processing_status, extraction_date DESC);

CREATE INDEX IF NOT EXISTS idx_videos_channel_date 
ON media_videos(channel_id, upload_date DESC);

CREATE INDEX IF NOT EXISTS idx_videos_status_date 
ON media_videos(download_status, upload_date DESC);

CREATE INDEX IF NOT EXISTS idx_documents_category_date 
ON media_documents(document_category, publish_date DESC);

CREATE INDEX IF NOT EXISTS idx_queue_priority_date 
ON media_collection_queue(priority, discovery_date) 
WHERE status = 'pending';

-- Partial indexes for common filters
CREATE INDEX IF NOT EXISTS idx_articles_high_quality 
ON media_news_articles(id) 
WHERE quality_score >= 0.7;

CREATE INDEX IF NOT EXISTS idx_videos_with_transcript 
ON media_videos(id) 
WHERE transcript_available = TRUE;

CREATE INDEX IF NOT EXISTS idx_documents_ocr_complete 
ON media_documents(id) 
WHERE ocr_performed = TRUE;

-- Index for array searches
CREATE INDEX IF NOT EXISTS idx_entities_sources 
ON media_entities USING GIN (sources);

-- ============================================
-- CHECK CONSTRAINTS (Validations)
-- ============================================

-- Validate priority ranges
ALTER TABLE media_collection_queue
ADD CONSTRAINT chk_queue_priority 
CHECK (priority >= 1 AND priority <= 10);

ALTER TABLE media_news_articles
ADD CONSTRAINT chk_article_priority 
CHECK (priority >= 1 AND priority <= 10);

ALTER TABLE media_videos
ADD CONSTRAINT chk_video_priority 
CHECK (priority >= 1 AND priority <= 10);

ALTER TABLE media_documents
ADD CONSTRAINT chk_document_priority 
CHECK (priority >= 1 AND priority <= 10);

-- Validate status values
ALTER TABLE media_collection_queue
ADD CONSTRAINT chk_queue_status 
CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'retry', 'archived'));

ALTER TABLE media_news_articles
ADD CONSTRAINT chk_article_status 
CHECK (processing_status IN ('discovered', 'collected', 'extracted', 'analyzed', 'archived', 'error'));

ALTER TABLE media_videos
ADD CONSTRAINT chk_video_status 
CHECK (download_status IN ('pending', 'downloading', 'completed', 'failed', 'retry'));

ALTER TABLE media_documents
ADD CONSTRAINT chk_document_status 
CHECK (download_status IN ('pending', 'downloading', 'completed', 'failed', 'retry'));

-- Validate sentiment scores
ALTER TABLE media_news_articles
ADD CONSTRAINT chk_sentiment_score 
CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0);

ALTER TABLE media_entity_mentions
ADD CONSTRAINT chk_mention_sentiment 
CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0);

-- Validate quality and confidence scores
ALTER TABLE media_news_articles
ADD CONSTRAINT chk_quality_score 
CHECK (quality_score >= 0.0 AND quality_score <= 1.0);

ALTER TABLE media_videos
ADD CONSTRAINT chk_video_quality 
CHECK (quality_score >= 0.0 AND quality_score <= 1.0);

ALTER TABLE media_entities
ADD CONSTRAINT chk_entity_confidence 
CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0);

ALTER TABLE media_entity_mentions
ADD CONSTRAINT chk_mention_confidence 
CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0);

-- Validate entity types
ALTER TABLE media_entities
ADD CONSTRAINT chk_entity_type 
CHECK (entity_type IN ('person', 'organization', 'location', 'case_number', 'financial_amount', 'date', 'email', 'phone', 'url', 'other'));

-- ============================================
-- VIEWS FOR ANALYTICS
-- ============================================

-- Daily ingestion statistics
CREATE OR REPLACE VIEW vw_daily_ingestion_stats AS
SELECT 
    DATE(extraction_date) as date,
    COUNT(*) as articles_ingested,
    COUNT(DISTINCT source_domain) as unique_sources,
    AVG(word_count) as avg_word_count,
    AVG(quality_score) as avg_quality,
    SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END) as positive_articles,
    SUM(CASE WHEN sentiment_label = 'negative' THEN 1 ELSE 0 END) as negative_articles,
    SUM(CASE WHEN sentiment_label = 'neutral' THEN 1 ELSE 0 END) as neutral_articles
FROM media_news_articles
WHERE extraction_date > NOW() - INTERVAL '30 days'
GROUP BY DATE(extraction_date)
ORDER BY date DESC;

-- Source reliability ranking
CREATE OR REPLACE VIEW vw_source_reliability AS
SELECT 
    source_domain,
    source_name,
    source_type,
    COUNT(*) as article_count,
    AVG(quality_score) as avg_quality,
    AVG(credibility_score) as avg_credibility,
    AVG(word_count) as avg_word_count,
    COUNT(DISTINCT authors) as unique_authors,
    MIN(publication_date) as first_seen,
    MAX(publication_date) as last_seen
FROM media_news_articles
WHERE source_domain IS NOT NULL
GROUP BY source_domain, source_name, source_type
HAVING COUNT(*) >= 5
ORDER BY avg_quality DESC NULLS LAST;

-- Keyword trends over time
CREATE OR REPLACE VIEW vw_keyword_trends AS
WITH keyword_mentions AS (
    SELECT 
        unnest(keywords) as keyword,
        DATE(publication_date) as mention_date
    FROM media_news_articles
    WHERE publication_date > NOW() - INTERVAL '90 days'
      AND keywords IS NOT NULL
)
SELECT 
    keyword,
    mention_date,
    COUNT(*) as mention_count
FROM keyword_mentions
WHERE keyword IS NOT NULL
GROUP BY keyword, mention_date
ORDER BY mention_count DESC;

-- Entity co-occurrence (which entities appear together)
CREATE OR REPLACE VIEW vw_entity_cooccurrence AS
SELECT 
    m1.entity_id as entity_1,
    e1.entity_name as entity_1_name,
    m2.entity_id as entity_2,
    e2.entity_name as entity_2_name,
    COUNT(*) as cooccurrence_count,
    MIN(m1.mentioned_at) as first_cooccurrence,
    MAX(m1.mentioned_at) as last_cooccurrence
FROM media_entity_mentions m1
JOIN media_entity_mentions m2 
    ON m1.media_type = m2.media_type 
    AND m1.media_id = m2.media_id 
    AND m1.entity_id < m2.entity_id
JOIN media_entities e1 ON m1.entity_id = e1.id
JOIN media_entities e2 ON m2.entity_id = e2.id
GROUP BY m1.entity_id, e1.entity_name, m2.entity_id, e2.entity_name
HAVING COUNT(*) >= 2
ORDER BY cooccurrence_count DESC;

-- Processing queue status with details
CREATE OR REPLACE VIEW vw_queue_status_detailed AS
SELECT 
    media_type,
    status,
    priority,
    COUNT(*) as item_count,
    MIN(discovery_date) as oldest_item,
    MAX(discovery_date) as newest_item,
    array_agg(DISTINCT discovered_by) as discovery_sources
FROM media_collection_queue
WHERE status IN ('pending', 'processing', 'failed', 'retry')
GROUP BY media_type, status, priority
ORDER BY priority, media_type, status;

-- Content freshness (how recent is our data)
CREATE OR REPLACE VIEW vw_content_freshness AS
SELECT 
    'news' as content_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN extraction_date > NOW() - INTERVAL '1 day' THEN 1 END) as last_24h,
    COUNT(CASE WHEN extraction_date > NOW() - INTERVAL '7 days' THEN 1 END) as last_7d,
    COUNT(CASE WHEN extraction_date > NOW() - INTERVAL '30 days' THEN 1 END) as last_30d,
    MAX(extraction_date) as most_recent
FROM media_news_articles
UNION ALL
SELECT 
    'videos' as content_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN discovery_date > NOW() - INTERVAL '1 day' THEN 1 END) as last_24h,
    COUNT(CASE WHEN discovery_date > NOW() - INTERVAL '7 days' THEN 1 END) as last_7d,
    COUNT(CASE WHEN discovery_date > NOW() - INTERVAL '30 days' THEN 1 END) as last_30d,
    MAX(discovery_date) as most_recent
FROM media_videos
UNION ALL
SELECT 
    'documents' as content_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN discovery_date > NOW() - INTERVAL '1 day' THEN 1 END) as last_24h,
    COUNT(CASE WHEN discovery_date > NOW() - INTERVAL '7 days' THEN 1 END) as last_7d,
    COUNT(CASE WHEN discovery_date > NOW() - INTERVAL '30 days' THEN 1 END) as last_30d,
    MAX(discovery_date) as most_recent
FROM media_documents;

-- ============================================
-- HELPER FUNCTIONS
-- ============================================

-- Function: Calculate content age in days
CREATE OR REPLACE FUNCTION content_age_days(publish_date TIMESTAMP WITH TIME ZONE)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(DAY FROM (NOW() - publish_date));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Extract domain from URL
CREATE OR REPLACE FUNCTION extract_domain(url TEXT)
RETURNS TEXT AS $$
DECLARE
    domain TEXT;
BEGIN
    -- Remove protocol
    domain := regexp_replace(url, '^https?://', '');
    -- Remove path
    domain := split_part(domain, '/', 1);
    -- Remove www prefix
    domain := regexp_replace(domain, '^www\.', '');
    RETURN domain;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Normalize entity name
CREATE OR REPLACE FUNCTION normalize_entity_name(name TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN lower(regexp_replace(name, '[^a-zA-Z0-9]', '', 'g'));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Calculate reading time from word count
CREATE OR REPLACE FUNCTION calculate_reading_time(word_count INTEGER)
RETURNS INTEGER AS $$
BEGIN
    -- Average reading speed: 200 words per minute
    RETURN GREATEST(1, word_count / 200);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Update entity mention count
CREATE OR REPLACE FUNCTION update_entity_mention_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE media_entities
    SET mention_count = (
        SELECT COUNT(*) 
        FROM media_entity_mentions 
        WHERE entity_id = NEW.entity_id
    ),
    last_seen_date = NOW()
    WHERE id = NEW.entity_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update mention counts
DROP TRIGGER IF EXISTS trigger_update_mention_count ON media_entity_mentions;
CREATE TRIGGER trigger_update_mention_count
    AFTER INSERT OR DELETE ON media_entity_mentions
    FOR EACH ROW
    EXECUTE FUNCTION update_entity_mention_count();

-- Function: Mark queue item as processing
CREATE OR REPLACE FUNCTION start_queue_processing(queue_id INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE media_collection_queue
    SET 
        status = 'processing',
        processing_started_at = NOW(),
        processing_attempts = processing_attempts + 1
    WHERE id = queue_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Complete queue item
CREATE OR REPLACE FUNCTION complete_queue_processing(
    queue_id INTEGER, 
    content_id INTEGER, 
    content_type TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE media_collection_queue
    SET 
        status = 'completed',
        processing_completed_at = NOW()
    WHERE id = queue_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Fail queue item with error
CREATE OR REPLACE FUNCTION fail_queue_processing(
    queue_id INTEGER, 
    error_message TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE media_collection_queue
    SET 
        status = CASE 
            WHEN processing_attempts >= 3 THEN 'failed'
            ELSE 'retry'
        END,
        last_error = error_message,
        last_error_at = NOW()
    WHERE id = queue_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- MATERIALIZED VIEWS (for performance)
-- ============================================

-- Materialized view: Top entities
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_top_entities AS
SELECT 
    e.id,
    e.entity_name,
    e.entity_type,
    e.mention_count,
    e.confidence_score,
    e.first_seen_date,
    e.last_seen_date,
    array_agg(DISTINCT m.media_type) as mentioned_in
FROM media_entities e
LEFT JOIN media_entity_mentions m ON e.id = m.entity_id
WHERE e.mention_count > 0
GROUP BY e.id, e.entity_name, e.entity_type, e.mention_count, 
         e.confidence_score, e.first_seen_date, e.last_seen_date
ORDER BY e.mention_count DESC;

-- Index on materialized view
CREATE INDEX IF NOT EXISTS idx_mv_top_entities_type 
ON mv_top_entities(entity_type);

-- Function to refresh materialized views
CREATE OR REPLACE FUNCTION refresh_materialized_views()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_top_entities;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- MIGRATION TRACKING
-- ============================================

INSERT INTO schema_migrations (version, name)
VALUES ('1.1.0', 'Add foreign keys, indexes, constraints, and views')
ON CONFLICT (version) DO NOTHING;

COMMIT;
