-- Migration: Create media acquisition tables with rich metadata
-- Version: 1.0.0
-- Date: 2026-04-06

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search

-- ============================================
-- CORE MEDIA TABLES
-- ============================================

-- Media Collection Queue
CREATE TABLE IF NOT EXISTS media_collection_queue (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    
    -- Content identification
    media_type VARCHAR(50) NOT NULL,  -- news, video, document, audio
    source_url TEXT NOT NULL,
    canonical_url TEXT,  -- Resolved/canonical URL
    
    -- Priority and status
    priority INTEGER DEFAULT 5 CHECK (priority >= 1 AND priority <= 10),
    status VARCHAR(50) DEFAULT 'pending',  -- pending, processing, completed, failed, retry
    
    -- Discovery metadata
    keywords_matched TEXT[],
    discovered_by VARCHAR(100),  -- agent name
    discovery_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    discovery_method VARCHAR(100),  -- gdelt, youtube_api, wayback, rss, manual
    
    -- Processing metadata
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processing_completed_at TIMESTAMP WITH TIME ZONE,
    processing_attempts INTEGER DEFAULT 0,
    last_error TEXT,
    last_error_at TIMESTAMP WITH TIME ZONE,
    
    -- Content fingerprinting
    url_hash VARCHAR(64) GENERATED ALWAYS AS (encode(digest(source_url, 'sha256'), 'hex')) STORED,
    content_hash VARCHAR(64),  -- Filled after download
    
    -- JSON metadata
    metadata JSONB DEFAULT '{}',
    
    -- Constraints
    CONSTRAINT unique_url_media_type UNIQUE (source_url, media_type)
);

-- Indexes for queue
CREATE INDEX idx_queue_status ON media_collection_queue(status);
CREATE INDEX idx_queue_media_type ON media_collection_queue(media_type);
CREATE INDEX idx_queue_priority ON media_collection_queue(priority) WHERE status = 'pending';
CREATE INDEX idx_queue_discovery_date ON media_collection_queue(discovery_date);
CREATE INDEX idx_queue_url_hash ON media_collection_queue(url_hash);
CREATE INDEX idx_queue_metadata ON media_collection_queue USING GIN (metadata);

-- ============================================
-- NEWS ARTICLES TABLE (Rich Metadata)
-- ============================================

CREATE TABLE IF NOT EXISTS media_news_articles (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    queue_id INTEGER REFERENCES media_collection_queue(id) ON DELETE SET NULL,
    
    -- Core content
    url TEXT NOT NULL UNIQUE,
    canonical_url TEXT,
    title TEXT,
    subtitle TEXT,
    content TEXT,
    content_cleaned TEXT,
    content_summary TEXT,
    
    -- Author and attribution
    authors TEXT[],
    author_emails TEXT[],
    author_twitter_handles TEXT[],
    byline TEXT,
    
    -- Publication metadata
    source_domain TEXT,
    source_name TEXT,
    source_type VARCHAR(50),  -- mainstream, independent, blog, government, academic
    publication_name TEXT,
    publication_date TIMESTAMP WITH TIME ZONE,
    publication_modified_date TIMESTAMP WITH TIME ZONE,
    
    -- Network metadata
    ip_address INET,
    server_location JSONB,  -- {country, city, region, coordinates}
    hosting_provider TEXT,
    cdn_provider TEXT,
    
    -- Content analysis
    word_count INTEGER,
    char_count INTEGER,
    reading_time_minutes INTEGER,
    readability_score DECIMAL(5,2),  -- Flesch-Kincaid
    sentiment_score DECIMAL(4,3),  -- -1.0 to 1.0
    sentiment_label VARCHAR(20),  -- positive, negative, neutral
    
    -- Content classification
    language VARCHAR(10) DEFAULT 'en',
    topics TEXT[],
    categories TEXT[],
    tags TEXT[],
    keywords TEXT[],
    entities_mentioned TEXT[],
    
    -- Quality metrics
    credibility_score DECIMAL(3,2),  -- 0.0 to 1.0
    fact_check_status VARCHAR(50),  -- verified, disputed, false, unverified
    bias_indicator VARCHAR(50),  -- left, center-left, center, center-right, right, unknown
    
    -- Technical metadata
    extraction_method VARCHAR(100),
    extraction_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    extraction_success BOOLEAN DEFAULT TRUE,
    http_status_code INTEGER,
    content_type TEXT,
    charset TEXT,
    
    -- Archival
    archive_org_url TEXT,
    archive_date TIMESTAMP WITH TIME ZONE,
    screenshot_path TEXT,
    pdf_path TEXT,
    
    -- Original/raw storage
    raw_html TEXT,
    raw_html_hash VARCHAR(64),
    headers JSONB,
    
    -- Link analysis
    outgoing_links TEXT[],
    outgoing_link_count INTEGER,
    incoming_links TEXT[],
    incoming_link_count INTEGER,
    
    -- Social metrics
    social_share_count JSONB,  -- {twitter: 123, facebook: 456, ...}
    comment_count INTEGER,
    
    -- Full-text search
    search_vector TSVECTOR,
    
    -- Status tracking
    processing_status VARCHAR(50) DEFAULT 'collected',  -- collected, extracted, analyzed, archived
    quality_score DECIMAL(3,2),  -- Overall quality 0.0 to 1.0
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    indexed_at TIMESTAMP WITH TIME ZONE,
    
    -- JSON for flexible metadata
    metadata JSONB DEFAULT '{}'
);

-- Indexes for articles
CREATE INDEX idx_articles_domain ON media_news_articles(source_domain);
CREATE INDEX idx_articles_publication_date ON media_news_articles(publication_date);
CREATE INDEX idx_articles_extraction_date ON media_news_articles(extraction_date);
CREATE INDEX idx_articles_language ON media_news_articles(language);
CREATE INDEX idx_articles_topics ON media_news_articles USING GIN (topics);
CREATE INDEX idx_articles_tags ON media_news_articles USING GIN (tags);
CREATE INDEX idx_articles_keywords ON media_news_articles USING GIN (keywords);
CREATE INDEX idx_articles_authors ON media_news_articles USING GIN (authors);
CREATE INDEX idx_articles_entities ON media_news_articles USING GIN (entities_mentioned);
CREATE INDEX idx_articles_metadata ON media_news_articles USING GIN (metadata);
CREATE INDEX idx_articles_search ON media_news_articles USING GIN (search_vector);
CREATE INDEX idx_articles_status ON media_news_articles(processing_status);

-- Trigram index for fuzzy text search
CREATE INDEX idx_articles_title_trgm ON media_news_articles USING GIN (title gin_trgm_ops);
CREATE INDEX idx_articles_content_trgm ON media_news_articles USING GIN (content gin_trgm_ops);

-- ============================================
-- VIDEOS TABLE (Rich Metadata)
-- ============================================

CREATE TABLE IF NOT EXISTS media_videos (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    queue_id INTEGER REFERENCES media_collection_queue(id) ON DELETE SET NULL,
    
    -- Core identification
    video_id TEXT NOT NULL,
    platform VARCHAR(50) NOT NULL,  -- youtube, vimeo, internet_archive, etc.
    url TEXT NOT NULL UNIQUE,
    embed_url TEXT,
    
    -- Content metadata
    title TEXT,
    description TEXT,
    duration_seconds INTEGER,
    duration_formatted TEXT,
    
    -- Creator metadata
    channel_id TEXT,
    channel_name TEXT,
    channel_url TEXT,
    uploader TEXT,
    uploader_id TEXT,
    
    -- Publication
    upload_date TIMESTAMP WITH TIME ZONE,
    publish_date TIMESTAMP WITH TIME ZONE,
    
    -- Engagement metrics
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    dislike_count BIGINT DEFAULT 0,
    comment_count BIGINT DEFAULT 0,
    share_count BIGINT DEFAULT 0,
    
    -- Content analysis
    language VARCHAR(10) DEFAULT 'en',
    transcript TEXT,
    transcript_available BOOLEAN DEFAULT FALSE,
    transcript_source VARCHAR(50),  -- youtube_api, whisper, manual
    transcript_language VARCHAR(10),
    
    -- Video quality
    resolution VARCHAR(20),  -- 1080p, 720p, etc.
    quality_score INTEGER,  -- 1-10
    file_size BIGINT,
    format VARCHAR(20),  -- mp4, webm, etc.
    
    -- Keywords and topics
    keywords_matched TEXT[],
    tags TEXT[],
    categories TEXT[],
    topics TEXT[],
    entities_mentioned TEXT[],
    
    -- Discovery metadata
    discovered_by VARCHAR(100),
    discovery_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    discovery_method VARCHAR(100),
    priority INTEGER DEFAULT 5,
    
    -- Archival
    local_path TEXT,
    thumbnail_path TEXT,
    thumbnail_url TEXT,
    archive_org_url TEXT,
    
    -- Status
    download_status VARCHAR(50) DEFAULT 'pending',  -- pending, downloading, completed, failed
    processing_status VARCHAR(50) DEFAULT 'discovered',
    
    -- Timestamps
    downloaded_at TIMESTAMP WITH TIME ZONE,
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- JSON metadata
    metadata JSONB DEFAULT '{}',
    raw_api_response JSONB  -- Original platform API response
);

CREATE INDEX idx_videos_platform ON media_videos(platform);
CREATE INDEX idx_videos_channel ON media_videos(channel_id);
CREATE INDEX idx_videos_upload_date ON media_videos(upload_date);
CREATE INDEX idx_videos_view_count ON media_videos(view_count);
CREATE INDEX idx_videos_keywords ON media_videos USING GIN (keywords_matched);
CREATE INDEX idx_videos_tags ON media_videos USING GIN (tags);
CREATE INDEX idx_videos_status ON media_videos(download_status);
CREATE INDEX idx_videos_metadata ON media_videos USING GIN (metadata);

-- ============================================
-- DOCUMENTS TABLE (Rich Metadata)
-- ============================================

CREATE TABLE IF NOT EXISTS media_documents (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    queue_id INTEGER REFERENCES media_collection_queue(id) ON DELETE SET NULL,
    
    -- Core identification
    source_url TEXT NOT NULL UNIQUE,
    canonical_url TEXT,
    title TEXT,
    description TEXT,
    
    -- Document type and format
    doc_type VARCHAR(50),  -- pdf, docx, txt, html, etc.
    mime_type TEXT,
    file_format VARCHAR(50),
    
    -- Source metadata
    source_domain TEXT,
    source_name TEXT,
    source_type VARCHAR(50),  -- government, court, academic, news, etc.
    
    -- Publication info
    publish_date TIMESTAMP WITH TIME ZONE,
    author TEXT,
    authors TEXT[],
    publisher TEXT,
    
    -- Content analysis
    content TEXT,
    content_extracted BOOLEAN DEFAULT FALSE,
    word_count INTEGER,
    page_count INTEGER,
    language VARCHAR(10) DEFAULT 'en',
    
    -- Document classification
    document_category VARCHAR(100),  -- legal_filing, court_order, indictment, etc.
    legal_case_number TEXT,
    court_name TEXT,
    jurisdiction TEXT,
    
    -- Keywords and entities
    keywords_matched TEXT[],
    tags TEXT[],
    entities_mentioned TEXT[],
    
    -- File metadata
    file_size BIGINT,
    file_hash VARCHAR(64),  -- SHA256
    file_path TEXT,
    
    -- OCR metadata
    ocr_performed BOOLEAN DEFAULT FALSE,
    ocr_engine VARCHAR(50),  -- tesseract, surya, etc.
    ocr_confidence DECIMAL(5,2),
    ocr_date TIMESTAMP WITH TIME ZONE,
    
    -- Redaction analysis
    redaction_count INTEGER,
    redaction_analysis JSONB,  -- {pages: [], total_redacted: 123, percentage: 0.5}
    
    -- Discovery metadata
    discovered_by VARCHAR(100),
    discovery_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    discovery_method VARCHAR(100),
    priority INTEGER DEFAULT 5,
    
    -- Status
    download_status VARCHAR(50) DEFAULT 'pending',
    processing_status VARCHAR(50) DEFAULT 'discovered',
    
    -- Timestamps
    downloaded_at TIMESTAMP WITH TIME ZONE,
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- JSON metadata
    metadata JSONB DEFAULT '{}',
    headers JSONB
);

CREATE INDEX idx_documents_type ON media_documents(doc_type);
CREATE INDEX idx_documents_domain ON media_documents(source_domain);
CREATE INDEX idx_documents_category ON media_documents(document_category);
CREATE INDEX idx_documents_publish_date ON media_documents(publish_date);
CREATE INDEX idx_documents_keywords ON media_documents USING GIN (keywords_matched);
CREATE INDEX idx_documents_tags ON media_documents USING GIN (tags);
CREATE INDEX idx_documents_status ON media_documents(download_status);
CREATE INDEX idx_documents_metadata ON media_documents USING GIN (metadata);

-- ============================================
-- ENTITIES TABLE (People, Organizations, Locations)
-- ============================================

CREATE TABLE IF NOT EXISTS media_entities (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    
    -- Entity identification
    entity_name TEXT NOT NULL,
    normalized_name TEXT,
    entity_type VARCHAR(50) NOT NULL,  -- person, organization, location, case_number, etc.
    
    -- Aliases and variants
    aliases TEXT[],
    name_variants TEXT[],
    
    -- Description
    description TEXT,
    wikipedia_url TEXT,
    wikidata_id TEXT,
    
    -- Classification
    category VARCHAR(100),
    subcategory VARCHAR(100),
    
    -- Metadata
    first_seen_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    mention_count INTEGER DEFAULT 0,
    sources TEXT[],
    confidence_score DECIMAL(3,2) DEFAULT 0.5,
    
    -- External IDs
    external_ids JSONB DEFAULT '{}',  -- {twitter: '@handle', linkedin: '...', etc.}
    
    -- Search
    search_vector TSVECTOR,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_entities_name ON media_entities(entity_name);
CREATE INDEX idx_entities_normalized ON media_entities(normalized_name);
CREATE INDEX idx_entities_type ON media_entities(entity_type);
CREATE INDEX idx_entities_category ON media_entities(category);
CREATE INDEX idx_entities_aliases ON media_entities USING GIN (aliases);
CREATE INDEX idx_entities_search ON media_entities USING GIN (search_vector);

-- ============================================
-- ENTITY MENTIONS (Links entities to content)
-- ============================================

CREATE TABLE IF NOT EXISTS media_entity_mentions (
    id SERIAL PRIMARY KEY,
    
    -- Link to entity
    entity_id INTEGER NOT NULL REFERENCES media_entities(id) ON DELETE CASCADE,
    
    -- Link to content
    media_type VARCHAR(50) NOT NULL,  -- news, video, document
    media_id INTEGER NOT NULL,
    
    -- Mention context
    mention_context TEXT,  -- Surrounding text
    mention_position_start INTEGER,
    mention_position_end INTEGER,
    mention_section VARCHAR(100),  -- title, body, summary, transcript
    
    -- Sentiment in context
    sentiment_score DECIMAL(4,3),
    sentiment_label VARCHAR(20),
    
    -- Confidence
    extraction_method VARCHAR(100),  -- spacy, gliner, regex, manual
    confidence_score DECIMAL(3,2) DEFAULT 0.5,
    
    -- Timestamps
    mentioned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_mentions_entity ON media_entity_mentions(entity_id);
CREATE INDEX idx_mentions_media ON media_entity_mentions(media_type, media_id);
CREATE INDEX idx_mentions_confidence ON media_entity_mentions(confidence_score);

-- ============================================
-- VIEWS FOR ANALYSIS
-- ============================================

-- View: Recent articles with full metadata
CREATE OR REPLACE VIEW vw_recent_articles AS
SELECT 
    a.id,
    a.uuid,
    a.url,
    a.title,
    a.authors,
    a.source_domain,
    a.source_name,
    a.publication_date,
    a.extraction_date,
    a.word_count,
    a.readability_score,
    a.sentiment_label,
    a.topics,
    a.tags,
    a.entities_mentioned,
    a.quality_score,
    a.metadata
FROM media_news_articles a
WHERE a.extraction_date > NOW() - INTERVAL '30 days'
ORDER BY a.extraction_date DESC;

-- View: Content statistics by domain
CREATE OR REPLACE VIEW vw_content_by_domain AS
SELECT 
    source_domain,
    COUNT(*) as article_count,
    AVG(word_count) as avg_word_count,
    AVG(quality_score) as avg_quality,
    MIN(publication_date) as earliest_article,
    MAX(publication_date) as latest_article
FROM media_news_articles
WHERE source_domain IS NOT NULL
GROUP BY source_domain
ORDER BY article_count DESC;

-- View: Entity mention statistics
CREATE OR REPLACE VIEW vw_entity_mentions AS
SELECT 
    e.entity_name,
    e.entity_type,
    COUNT(m.id) as mention_count,
    ARRAY_AGG(DISTINCT m.media_type) as mentioned_in_types,
    MIN(m.mentioned_at) as first_mentioned,
    MAX(m.mentioned_at) as last_mentioned
FROM media_entities e
LEFT JOIN media_entity_mentions m ON e.id = m.entity_id
GROUP BY e.id, e.entity_name, e.entity_type
ORDER BY mention_count DESC;

-- ============================================
-- FUNCTIONS AND TRIGGERS
-- ============================================

-- Function: Update search vector for articles
CREATE OR REPLACE FUNCTION update_article_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.subtitle, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.content_summary, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'D') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.tags, ' '), '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.keywords, ' '), '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update search vector
DROP TRIGGER IF EXISTS trigger_update_article_search ON media_news_articles;
CREATE TRIGGER trigger_update_article_search
    BEFORE INSERT OR UPDATE ON media_news_articles
    FOR EACH ROW
    EXECUTE FUNCTION update_article_search_vector();

-- Function: Update entity search vector
CREATE OR REPLACE FUNCTION update_entity_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.entity_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.normalized_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.aliases, ' '), '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update entity search
DROP TRIGGER IF EXISTS trigger_update_entity_search ON media_entities;
CREATE TRIGGER trigger_update_entity_search
    BEFORE INSERT OR UPDATE ON media_entities
    FOR EACH ROW
    EXECUTE FUNCTION update_entity_search_vector();

-- Function: Update timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply timestamp triggers
CREATE TRIGGER update_articles_timestamp BEFORE UPDATE ON media_news_articles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_videos_timestamp BEFORE UPDATE ON media_videos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_documents_timestamp BEFORE UPDATE ON media_documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_entities_timestamp BEFORE UPDATE ON media_entities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================
-- MIGRATION TRACKING
-- ============================================

CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    applied_by TEXT DEFAULT CURRENT_USER,
    checksum VARCHAR(64),
    execution_time_ms INTEGER
);

-- Record this migration
INSERT INTO schema_migrations (version, name, checksum)
VALUES ('1.0.0', 'Create media tables with rich metadata', NULL)
ON CONFLICT (version) DO NOTHING;

COMMIT;
