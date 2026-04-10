-- Fix missing columns in media_news_articles
ALTER TABLE media_news_articles 
ADD COLUMN IF NOT EXISTS publication_date TIMESTAMP,
ADD COLUMN IF NOT EXISTS extraction_date TIMESTAMP,
ADD COLUMN IF NOT EXISTS language TEXT,
ADD COLUMN IF NOT EXISTS topics TEXT[],
ADD COLUMN IF NOT EXISTS tags TEXT[],
ADD COLUMN IF NOT EXISTS metadata JSONB,
ADD COLUMN IF NOT EXISTS search_vector tsvector,
ADD COLUMN IF NOT EXISTS processing_status TEXT DEFAULT 'pending';

-- Fix missing columns in media_videos
ALTER TABLE media_videos
ADD COLUMN IF NOT EXISTS keywords_matched TEXT[],
ADD COLUMN IF NOT EXISTS tags TEXT[],
ADD COLUMN IF NOT EXISTS download_status TEXT DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS metadata JSONB;

-- Fix missing columns in media_documents
ALTER TABLE media_documents
ADD COLUMN IF NOT EXISTS doc_type TEXT,
ADD COLUMN IF NOT EXISTS source_domain TEXT,
ADD COLUMN IF NOT EXISTS document_category TEXT,
ADD COLUMN IF NOT EXISTS publish_date TIMESTAMP,
ADD COLUMN IF NOT EXISTS keywords_matched TEXT[],
ADD COLUMN IF NOT EXISTS tags TEXT[],
ADD COLUMN IF NOT EXISTS download_status TEXT DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS metadata JSONB;

-- Fix missing columns in media_entities
ALTER TABLE media_entities
ADD COLUMN IF NOT EXISTS category TEXT,
ADD COLUMN IF NOT EXISTS aliases TEXT[],
ADD COLUMN IF NOT EXISTS search_vector tsvector;

-- Fix missing columns in media_entity_mentions
ALTER TABLE media_entity_mentions
ADD COLUMN IF NOT EXISTS confidence_score FLOAT;
