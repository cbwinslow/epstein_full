-- Epstein Media Acquisition Database Schema
-- Phase 22: Media Acquisition Infrastructure
-- Created: April 4, 2026

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text similarity search

-- ============================================================================
-- NEWS ARTICLES
-- ============================================================================

CREATE TABLE media_news_articles (
    id SERIAL PRIMARY KEY,
    
    -- Source information
    source_domain VARCHAR(100) NOT NULL,
    source_name VARCHAR(100),
    source_category VARCHAR(50),  -- mainstream, investigative, tabloid, blog, academic
    
    -- URLs
    article_url TEXT NOT NULL,
    wayback_url TEXT,
    canonical_url TEXT,
    
    -- Content metadata
    title TEXT NOT NULL,
    authors TEXT[],
    publish_date DATE,
    publish_timestamp TIMESTAMP,
    content TEXT,
    summary TEXT,
    keywords TEXT[],
    word_count INTEGER,
    
    -- Analysis
    sentiment_score FLOAT,  -- -1.0 to 1.0
    subjectivity_score FLOAT,  -- 0.0 to 1.0
    primary_topic VARCHAR(50),
    topic_confidence FLOAT,
    all_topics JSONB,
    
    -- Cross-references with our existing data
    entities_mentioned JSONB,  -- {persons: [], organizations: [], locations: []}
    related_person_ids INTEGER[],  -- FK to exposed_persons
    related_flight_ids INTEGER[],  -- FK to exposed_flights
    related_document_ids INTEGER[],  -- FK to documents
    
    -- Collection metadata
    discovery_source VARCHAR(50),  -- gdelt, wayback, rss, newsapi, manual
    collection_method VARCHAR(50),  -- direct, wayback, api
    extraction_method VARCHAR(50),  -- newspaper3k, news-please, readability
    extraction_confidence FLOAT,
    gdelt_event_id BIGINT,
    
    -- Timestamps
    discovered_at TIMESTAMP,
    collected_at TIMESTAMP DEFAULT NOW(),
    analyzed_at TIMESTAMP,
    
    -- Constraints
    CONSTRAINT unique_article_url UNIQUE (article_url)
);

-- Indexes for news articles
CREATE INDEX idx_news_articles_date ON media_news_articles(publish_date DESC);
CREATE INDEX idx_news_articles_source ON media_news_articles(source_domain);
CREATE INDEX idx_news_articles_topic ON media_news_articles(primary_topic);
CREATE INDEX idx_news_articles_gdelt ON media_news_articles(gdelt_event_id);

-- GIN indexes for JSON/Array searches
CREATE INDEX idx_news_entities ON media_news_articles USING GIN(entities_mentioned);
CREATE INDEX idx_news_persons ON media_news_articles USING GIN(related_person_ids);
CREATE INDEX idx_news_flights ON media_news_articles USING GIN(related_flight_ids);

-- Full-text search
CREATE INDEX idx_news_content_search ON media_news_articles 
    USING GIN(to_tsvector('english', COALESCE(content, '')));
CREATE INDEX idx_news_title_search ON media_news_articles 
    USING GIN(to_tsvector('english', COALESCE(title, '')));

-- Trigram index for fuzzy text search
CREATE INDEX idx_news_title_trgm ON media_news_articles 
    USING GIN(title gin_trgm_ops);

-- ============================================================================
-- VIDEOS
-- ============================================================================

CREATE TABLE media_videos (
    id SERIAL PRIMARY KEY,
    
    -- Video metadata
    video_id VARCHAR(50) NOT NULL,
    platform VARCHAR(50) NOT NULL,  -- youtube, vimeo, internet_archive
    title TEXT,
    description TEXT,
    url TEXT NOT NULL,
    upload_date DATE,
    upload_timestamp TIMESTAMP,
    duration_seconds INTEGER,
    view_count BIGINT,
    like_count INTEGER,
    
    -- Transcript
    transcript_text TEXT,
    transcript_path TEXT,  -- File path if stored separately
    transcript_source VARCHAR(50),  -- youtube_api, yt-dlp, whisper_local, whisper_api
    transcript_language VARCHAR(10) DEFAULT 'en',
    is_auto_transcript BOOLEAN DEFAULT TRUE,
    transcript_segments JSONB,  -- [{start: 0.0, end: 5.0, text: "..."}]
    
    -- Analysis
    entities_mentioned JSONB,
    related_person_ids INTEGER[],
    sentiment_score FLOAT,
    key_topics TEXT[],
    
    -- Collection metadata
    discovery_source VARCHAR(50),
    collected_at TIMESTAMP DEFAULT NOW(),
    transcript_collected_at TIMESTAMP,
    
    -- Unique constraint
    UNIQUE(video_id, platform)
);

-- Indexes for videos
CREATE INDEX idx_videos_date ON media_videos(upload_date DESC);
CREATE INDEX idx_videos_platform ON media_videos(platform);
CREATE INDEX idx_video_persons ON media_videos USING GIN(related_person_ids);
CREATE INDEX idx_video_entities ON media_videos USING GIN(entities_mentioned);

-- Full-text search on transcripts
CREATE INDEX idx_video_transcript_search ON media_videos 
    USING GIN(to_tsvector('english', COALESCE(transcript_text, '')));

-- ============================================================================
-- OFFICIAL DOCUMENTS
-- ============================================================================

CREATE TABLE media_documents (
    id SERIAL PRIMARY KEY,
    
    -- Document metadata
    source VARCHAR(50) NOT NULL,  -- court_listener, govinfo, pacer, foia, direct
    document_type VARCHAR(50),  -- filing, opinion, order, release, report
    document_subtype VARCHAR(50),  -- complaint, motion, brief, judgment, etc.
    title TEXT,
    docket_number VARCHAR(100),
    case_name TEXT,
    case_number VARCHAR(100),
    court VARCHAR(100),
    court_code VARCHAR(20),
    filing_date DATE,
    filing_timestamp TIMESTAMP,
    
    -- URLs and files
    url TEXT,
    file_path TEXT,
    original_filename TEXT,
    
    -- Content
    text_content TEXT,
    extracted_entities JSONB,
    summary TEXT,
    key_findings TEXT[],
    
    -- File info
    page_count INTEGER,
    file_size_bytes BIGINT,
    mime_type VARCHAR(50),
    checksum VARCHAR(64),  -- SHA-256
    
    -- Cross-references
    related_person_ids INTEGER[],
    related_case_ids INTEGER[],
    
    -- Collection metadata
    discovered_at TIMESTAMP,
    collected_at TIMESTAMP DEFAULT NOW(),
    analyzed_at TIMESTAMP,
    
    -- Unique constraint per source
    UNIQUE(source, docket_number, filing_date)
);

-- Indexes for documents
CREATE INDEX idx_documents_date ON media_documents(filing_date DESC);
CREATE INDEX idx_documents_source ON media_documents(source);
CREATE INDEX idx_documents_court ON media_documents(court);
CREATE INDEX idx_documents_type ON media_documents(document_type);
CREATE INDEX idx_doc_persons ON media_documents USING GIN(related_person_ids);
CREATE INDEX idx_doc_entities ON media_documents USING GIN(extracted_entities);

-- Full-text search
CREATE INDEX idx_doc_content_search ON media_documents 
    USING GIN(to_tsvector('english', COALESCE(text_content, '')));
CREATE INDEX idx_doc_title_search ON media_documents 
    USING GIN(to_tsvector('english', COALESCE(title, '')));

-- ============================================================================
-- INGESTION RUNS (Pipeline Execution Tracking)
-- ============================================================================

CREATE TABLE media_ingestion_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Run identification
    run_name VARCHAR(200),  -- Optional descriptive name
    run_type VARCHAR(50) DEFAULT 'news',  -- news, video, document, mixed

    -- Configuration
    keywords TEXT[],  -- Keywords used for discovery
    date_range_start DATE,
    date_range_end DATE,
    max_results_requested INTEGER,
    sources_used TEXT[],  -- Source domains/agents used

    -- Status and timing
    status VARCHAR(50) DEFAULT 'running',  -- running, completed, failed, cancelled
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    duration_seconds INTEGER,

    -- Results summary
    total_discovered INTEGER DEFAULT 0,
    total_queued INTEGER DEFAULT 0,
    total_collected INTEGER DEFAULT 0,
    total_failed INTEGER DEFAULT 0,

    -- Source breakdown
    google_news_count INTEGER DEFAULT 0,
    gdelt_count INTEGER DEFAULT 0,
    wayback_count INTEGER DEFAULT 0,
    rss_count INTEGER DEFAULT 0,

    -- Error tracking
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,

    -- Metadata
    config JSONB,  -- Full run configuration
    logs_path TEXT,  -- Path to detailed log file
    hostname VARCHAR(100),  -- Machine that ran the pipeline
    pid INTEGER,  -- Process ID

    -- Indexes
    CONSTRAINT valid_status CHECK (status IN ('running', 'completed', 'failed', 'cancelled'))
);

CREATE INDEX idx_ingestion_runs_status ON media_ingestion_runs(status);
CREATE INDEX idx_ingestion_runs_started_at ON media_ingestion_runs(started_at DESC);
CREATE INDEX idx_ingestion_runs_type ON media_ingestion_runs(run_type);

-- Link queue items to ingestion runs
ALTER TABLE media_collection_queue
    ADD COLUMN IF NOT EXISTS ingestion_run_id UUID REFERENCES media_ingestion_runs(id);

CREATE INDEX idx_queue_ingestion_run ON media_collection_queue(ingestion_run_id);

-- ============================================================================
-- COLLECTION QUEUE
-- ============================================================================

CREATE TABLE media_collection_queue (
    id SERIAL PRIMARY KEY,
    
    -- Task info
    media_type VARCHAR(50) NOT NULL,  -- news, video, document
    source_url TEXT NOT NULL,
    source_platform VARCHAR(50),
    priority INTEGER DEFAULT 5,  -- 1 (high) to 10 (low)
    status VARCHAR(50) DEFAULT 'pending',  -- pending, processing, completed, failed, retry
    
    -- Discovery metadata
    discovered_by VARCHAR(50),  -- Agent ID
    discovery_date TIMESTAMP DEFAULT NOW(),
    keywords_matched TEXT[],
    metadata JSONB,  -- Additional discovery context
    
    -- Processing
    worker_id VARCHAR(100),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    
    -- Result
    result_id INTEGER,  -- ID in respective media table
    result_metadata JSONB,
    
    -- Unique constraint
    UNIQUE(source_url, media_type)
);

-- Indexes for queue
CREATE INDEX idx_queue_status ON media_collection_queue(status, priority, id);
CREATE INDEX idx_queue_type ON media_collection_queue(media_type, status);
CREATE INDEX idx_queue_worker ON media_collection_queue(worker_id, status);
CREATE INDEX idx_queue_discovered ON media_collection_queue(discovery_date DESC);

-- ============================================================================
-- COLLECTION STATISTICS
-- ============================================================================

CREATE TABLE media_collection_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    media_type VARCHAR(50) NOT NULL,
    agent_id VARCHAR(50),
    
    -- Discovery stats
    discovered_count INTEGER DEFAULT 0,
    
    -- Collection stats
    attempted_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failed_count INTEGER DEFAULT 0,
    
    -- Storage stats
    storage_bytes BIGINT DEFAULT 0,
    items_added INTEGER DEFAULT 0,
    
    -- Performance
    avg_processing_time_ms INTEGER,
    
    UNIQUE(date, media_type, agent_id)
);

CREATE INDEX idx_stats_date ON media_collection_stats(date DESC);
CREATE INDEX idx_stats_type ON media_collection_stats(media_type);

-- ============================================================================
-- MEDIA RELATIONSHIPS (Entity co-occurrence)
-- ============================================================================

CREATE TABLE media_entity_mentions (
    id SERIAL PRIMARY KEY,
    
    -- Source media
    media_type VARCHAR(50) NOT NULL,  -- news, video, document
    media_id INTEGER NOT NULL,
    
    -- Entity from our database
    entity_type VARCHAR(50) NOT NULL,  -- person, organization, location
    entity_id INTEGER NOT NULL,
    entity_name VARCHAR(255),
    
    -- Mention details
    mention_count INTEGER DEFAULT 1,
    first_mention_position INTEGER,
    mention_contexts TEXT[],  -- Surrounding text snippets
    
    -- Confidence
    match_confidence FLOAT,
    match_method VARCHAR(50),  -- exact, fuzzy, ml
    
    collected_at TIMESTAMP DEFAULT NOW(),
    
    -- Unique constraint
    UNIQUE(media_type, media_id, entity_type, entity_id)
);

-- Indexes for entity mentions
CREATE INDEX idx_mentions_entity ON media_entity_mentions(entity_type, entity_id);
CREATE INDEX idx_mentions_media ON media_entity_mentions(media_type, media_id);
CREATE INDEX idx_mentions_confidence ON media_entity_mentions(match_confidence DESC);

-- ============================================================================
-- VIEWS FOR ANALYSIS
-- ============================================================================

-- View: Media coverage timeline
CREATE OR REPLACE VIEW v_media_coverage_timeline AS
SELECT 
    publish_date as date,
    COUNT(DISTINCT CASE WHEN source_type = 'news' THEN id END) as news_count,
    COUNT(DISTINCT CASE WHEN source_type = 'video' THEN id END) as video_count,
    COUNT(DISTINCT CASE WHEN source_type = 'document' THEN id END) as document_count
FROM (
    SELECT id, publish_date, 'news' as source_type FROM media_news_articles WHERE publish_date IS NOT NULL
    UNION ALL
    SELECT id, upload_date, 'video' FROM media_videos WHERE upload_date IS NOT NULL
    UNION ALL
    SELECT id, filing_date, 'document' FROM media_documents WHERE filing_date IS NOT NULL
) combined
GROUP BY publish_date
ORDER BY publish_date;

-- View: Top mentioned persons across all media
CREATE OR REPLACE VIEW v_media_top_persons AS
SELECT 
    p.id as person_id,
    p.name,
    COUNT(DISTINCT me.media_id || '_' || me.media_type) as total_mentions,
    COUNT(DISTINCT CASE WHEN me.media_type = 'news' THEN me.media_id END) as news_mentions,
    COUNT(DISTINCT CASE WHEN me.media_type = 'video' THEN me.media_id END) as video_mentions,
    COUNT(DISTINCT CASE WHEN me.media_type = 'document' THEN me.media_id END) as document_mentions
FROM exposed_persons p
JOIN media_entity_mentions me ON me.entity_type = 'person' AND me.entity_id = p.id
GROUP BY p.id, p.name
ORDER BY total_mentions DESC;

-- View: Media source breakdown
CREATE OR REPLACE VIEW v_media_source_breakdown AS
SELECT 
    source_domain as source,
    'news' as media_type,
    COUNT(*) as total_articles,
    MIN(publish_date) as earliest_date,
    MAX(publish_date) as latest_date,
    AVG(sentiment_score) as avg_sentiment
FROM media_news_articles
GROUP BY source_domain

UNION ALL

SELECT 
    platform as source,
    'video' as media_type,
    COUNT(*) as total_videos,
    MIN(upload_date) as earliest_date,
    MAX(upload_date) as latest_date,
    NULL as avg_sentiment
FROM media_videos
GROUP BY platform

UNION ALL

SELECT 
    source,
    'document' as media_type,
    COUNT(*) as total_docs,
    MIN(filing_date) as earliest_date,
    MAX(filing_date) as latest_date,
    NULL as avg_sentiment
FROM media_documents
GROUP BY source;

-- View: Recent collection activity
CREATE OR REPLACE VIEW v_recent_collection AS
SELECT 
    mq.id,
    mq.media_type,
    mq.source_url,
    mq.status,
    mq.priority,
    mq.discovered_by,
    mq.discovery_date,
    mq.started_at,
    mq.completed_at,
    CASE 
        WHEN mq.completed_at IS NOT NULL AND mq.started_at IS NOT NULL 
        THEN EXTRACT(EPOCH FROM (mq.completed_at - mq.started_at))::INTEGER
        ELSE NULL 
    END as duration_seconds,
    mq.error_message,
    COALESCE(na.title, vd.title, md.title) as media_title
FROM media_collection_queue mq
LEFT JOIN media_news_articles na ON mq.media_type = 'news' AND mq.result_id = na.id
LEFT JOIN media_videos vd ON mq.media_type = 'video' AND mq.result_id = vd.id
LEFT JOIN media_documents md ON mq.media_type = 'document' AND mq.result_id = md.id
ORDER BY mq.id DESC
LIMIT 1000;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function: Get queue summary
CREATE OR REPLACE FUNCTION fn_get_queue_summary()
RETURNS TABLE (
    media_type VARCHAR,
    pending BIGINT,
    processing BIGINT,
    completed BIGINT,
    failed BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        mq.media_type,
        COUNT(*) FILTER (WHERE mq.status = 'pending') as pending,
        COUNT(*) FILTER (WHERE mq.status = 'processing') as processing,
        COUNT(*) FILTER (WHERE mq.status = 'completed') as completed,
        COUNT(*) FILTER (WHERE mq.status = 'failed') as failed
    FROM media_collection_queue mq
    GROUP BY mq.media_type;
END;
$$ LANGUAGE plpgsql;

-- Function: Add to queue (with deduplication)
CREATE OR REPLACE FUNCTION fn_add_to_queue(
    p_media_type VARCHAR,
    p_source_url TEXT,
    p_priority INTEGER DEFAULT 5,
    p_keywords_matched TEXT[] DEFAULT NULL,
    p_discovered_by VARCHAR DEFAULT NULL,
    p_metadata JSONB DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO media_collection_queue (
        media_type, source_url, priority, keywords_matched,
        discovered_by, metadata, status, discovery_date
    ) VALUES (
        p_media_type, p_source_url, p_priority, p_keywords_matched,
        p_discovered_by, p_metadata, 'pending', NOW()
    )
    ON CONFLICT (source_url, media_type) DO NOTHING
    RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Get next batch from queue
CREATE OR REPLACE FUNCTION fn_get_queue_batch(
    p_media_type VARCHAR,
    p_limit INTEGER DEFAULT 100
)
RETURNS TABLE (
    id INTEGER,
    source_url TEXT,
    keywords_matched TEXT[],
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    UPDATE media_collection_queue
    SET status = 'processing', started_at = NOW()
    WHERE id IN (
        SELECT mq.id
        FROM media_collection_queue mq
        WHERE mq.media_type = p_media_type
          AND mq.status = 'pending'
        ORDER BY mq.priority ASC, mq.id ASC
        LIMIT p_limit
    )
    RETURNING media_collection_queue.id, 
              media_collection_queue.source_url,
              media_collection_queue.keywords_matched,
              media_collection_queue.metadata;
END;
$$ LANGUAGE plpgsql;

-- Function: Search across all media
CREATE OR REPLACE FUNCTION fn_search_media(p_query TEXT)
RETURNS TABLE (
    media_type VARCHAR,
    media_id INTEGER,
    title TEXT,
    url TEXT,
    rank REAL
) AS $$
BEGIN
    -- Search news articles
    RETURN QUERY
    SELECT 
        'news'::VARCHAR as media_type,
        na.id as media_id,
        na.title,
        na.article_url as url,
        ts_rank(to_tsvector('english', na.title || ' ' || COALESCE(na.content, '')), 
                plainto_tsquery('english', p_query)) as rank
    FROM media_news_articles na
    WHERE to_tsvector('english', na.title || ' ' || COALESCE(na.content, ''))
          @@ plainto_tsquery('english', p_query)
    ORDER BY rank DESC
    LIMIT 50;
    
    -- Search videos
    RETURN QUERY
    SELECT 
        'video'::VARCHAR as media_type,
        vd.id as media_id,
        vd.title,
        vd.url,
        ts_rank(to_tsvector('english', COALESCE(vd.transcript_text, '')),
                plainto_tsquery('english', p_query)) as rank
    FROM media_videos vd
    WHERE to_tsvector('english', COALESCE(vd.transcript_text, ''))
          @@ plainto_tsquery('english', p_query)
    ORDER BY rank DESC
    LIMIT 50;
    
    -- Search documents
    RETURN QUERY
    SELECT 
        'document'::VARCHAR as media_type,
        md.id as media_id,
        md.title,
        md.url,
        ts_rank(to_tsvector('english', COALESCE(md.text_content, '')),
                plainto_tsquery('english', p_query)) as rank
    FROM media_documents md
    WHERE to_tsvector('english', COALESCE(md.text_content, ''))
          @@ plainto_tsquery('english', p_query)
    ORDER BY rank DESC
    LIMIT 50;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- GRANTS
-- ============================================================================

-- Grant permissions (adjust user as needed)
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO cbwinslow;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO cbwinslow;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE media_news_articles IS 'News articles about Epstein case from various sources';
COMMENT ON TABLE media_videos IS 'Video content with transcripts';
COMMENT ON TABLE media_documents IS 'Official documents, court filings, government releases';
COMMENT ON TABLE media_collection_queue IS 'Queue for pending media collection tasks';
COMMENT ON TABLE media_collection_stats IS 'Daily collection statistics by agent';
COMMENT ON TABLE media_entity_mentions IS 'Cross-reference between media and our entity database';

-- ============================================================================
-- INITIAL DATA (Optional)
-- ============================================================================

-- Insert initial stats row for today
INSERT INTO media_collection_stats (date, media_type, agent_id)
SELECT CURRENT_DATE, 'news', 'init'
WHERE NOT EXISTS (
    SELECT 1 FROM media_collection_stats 
    WHERE date = CURRENT_DATE AND media_type = 'news'
);
