-- Add pgvector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding columns to media_news_articles
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS title_embedding vector(768),
ADD COLUMN IF NOT EXISTS summary_embedding vector(768),
ADD COLUMN IF NOT EXISTS content_embedding vector(768);

-- Add content hash for deduplication
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS content_hash VARCHAR(64),
ADD COLUMN IF NOT EXISTS title_hash VARCHAR(64);

-- Add clustering columns
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS cluster_id INTEGER,
ADD COLUMN IF NOT EXISTS canonical_article_id INTEGER REFERENCES media_news_articles(id),
ADD COLUMN IF NOT EXISTS is_duplicate BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS duplicate_reason VARCHAR(50),
ADD COLUMN IF NOT EXISTS similarity_score FLOAT;

-- Create vector indexes for semantic search
CREATE INDEX IF NOT EXISTS idx_news_title_embedding 
ON media_news_articles USING ivfflat(title_embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_news_summary_embedding 
ON media_news_articles USING ivfflat(summary_embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_news_content_embedding 
ON media_news_articles USING ivfflat(content_embedding vector_cosine_ops)
WITH (lists = 100);

-- Create hash indexes for deduplication
CREATE INDEX IF NOT EXISTS idx_news_content_hash ON media_news_articles(content_hash);
CREATE INDEX IF NOT EXISTS idx_news_title_hash ON media_news_articles(title_hash);
CREATE INDEX IF NOT EXISTS idx_news_cluster ON media_news_articles(cluster_id);

-- Create author profile table
CREATE TABLE IF NOT EXISTS media_authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    twitter_handle VARCHAR(100),
    linkedin_url TEXT,
    affiliation VARCHAR(255),
    bio TEXT,
    beat VARCHAR(100),
    location VARCHAR(100),
    total_articles INTEGER DEFAULT 0,
    epstein_articles INTEGER DEFAULT 0,
    credibility_score FLOAT,
    political_leaning VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(name, email)
);

CREATE INDEX IF NOT EXISTS idx_authors_name ON media_authors(name);
CREATE INDEX IF NOT EXISTS idx_authors_affiliation ON media_authors(affiliation);

-- Create article-author junction table
CREATE TABLE IF NOT EXISTS media_article_authors (
    article_id INTEGER REFERENCES media_news_articles(id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES media_authors(id) ON DELETE CASCADE,
    author_role VARCHAR(50),
    contribution_type VARCHAR(50),
    UNIQUE(article_id, author_id)
);

CREATE INDEX IF NOT EXISTS idx_article_authors_article ON media_article_authors(article_id);
CREATE INDEX IF NOT EXISTS idx_article_authors_author ON media_article_authors(author_id);

-- Add language detection column
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS language_code VARCHAR(10) DEFAULT 'en';

-- Add fact-checking columns
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS fact_check_status VARCHAR(50),
ADD COLUMN IF NOT EXISTS fact_check_sources JSONB,
ADD COLUMN IF NOT EXISTS correction_notes TEXT;

-- Add social signals
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS social_media_shares JSONB,
ADD COLUMN IF NOT EXISTS viral_score FLOAT,
ADD COLUMN IF NOT EXISTS engagement_metrics JSONB;

-- Add reading metrics
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS reading_time_seconds INTEGER,
ADD COLUMN IF NOT EXISTS flesch_kincaid_grade FLOAT,
ADD COLUMN IF NOT EXISTS complexity_score FLOAT;

-- Add technical metadata
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS http_status INTEGER,
ADD COLUMN IF NOT EXISTS response_time_ms INTEGER,
ADD COLUMN IF NOT EXISTS content_type VARCHAR(100),
ADD COLUMN IF NOT EXISTS charset VARCHAR(50),
ADD COLUMN IF NOT EXISTS last_modified TIMESTAMP,
ADD COLUMN IF NOT EXISTS etag VARCHAR(100);

-- Update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_media_authors_updated_at
    BEFORE UPDATE ON media_authors
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE media_authors IS 'Author profiles for news articles';
COMMENT ON TABLE media_article_authors IS 'Junction table linking articles to authors';
