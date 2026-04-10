"""
Setup script for test database.
Creates necessary tables and indexes for testing.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration
TEST_DB_NAME = 'epstein_test'
DEFAULT_DB_URL = 'postgresql://cbwinslow:123qweasd@localhost:5432/postgres'


def create_test_database():
    """Create test database if it doesn't exist."""
    conn = psycopg2.connect(DEFAULT_DB_URL)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    with conn.cursor() as cur:
        # Check if database exists
        cur.execute(
            "SELECT EXISTS (SELECT FROM pg_database WHERE datname = %s)",
            (TEST_DB_NAME,)
        )
        exists = cur.fetchone()[0]
        
        if not exists:
            print(f"Creating test database: {TEST_DB_NAME}")
            cur.execute(f"CREATE DATABASE {TEST_DB_NAME}")
            print(f"✓ Database {TEST_DB_NAME} created")
        else:
            print(f"✓ Database {TEST_DB_NAME} already exists")
    
    conn.close()


def create_tables():
    """Create test tables."""
    test_db_url = f"postgresql://cbwinslow:123qweasd@localhost:5432/{TEST_DB_NAME}"
    conn = psycopg2.connect(test_db_url)
    
    with conn.cursor() as cur:
        # Create media_collection_queue table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_collection_queue (
                id SERIAL PRIMARY KEY,
                media_type TEXT NOT NULL,
                source_url TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                status TEXT DEFAULT 'pending',
                keywords_matched TEXT[],
                discovered_by TEXT,
                discovery_date TIMESTAMP DEFAULT NOW(),
                metadata JSONB DEFAULT '{}',
                UNIQUE(source_url, media_type)
            )
        """)
        
        # Create media_news_articles table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_news_articles (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT,
                content_cleaned TEXT,
                source_domain TEXT,
                publish_date TIMESTAMP,
                priority INTEGER DEFAULT 5,
                keywords_matched TEXT[],
                extraction_method TEXT,
                word_count INTEGER,
                readability_score FLOAT,
                metadata JSONB DEFAULT '{}',
                collected_at TIMESTAMP DEFAULT NOW(),
                stored_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create media_videos table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_videos (
                id SERIAL PRIMARY KEY,
                video_id TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                title TEXT,
                description TEXT,
                platform TEXT,
                duration_seconds INTEGER,
                upload_date TIMESTAMP,
                view_count INTEGER DEFAULT 0,
                transcript_available BOOLEAN DEFAULT FALSE,
                transcript_source TEXT,
                keywords_matched TEXT[],
                discovery_method TEXT,
                priority INTEGER DEFAULT 5,
                metadata JSONB DEFAULT '{}',
                stored_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create media_documents table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_documents (
                id SERIAL PRIMARY KEY,
                source_url TEXT UNIQUE NOT NULL,
                title TEXT,
                doc_type TEXT,
                content TEXT,
                source_domain TEXT,
                publish_date TIMESTAMP,
                file_size BIGINT,
                checksum TEXT,
                keywords_matched TEXT[],
                discovery_method TEXT,
                priority INTEGER DEFAULT 5,
                metadata JSONB DEFAULT '{}',
                stored_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create media_entities table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_entities (
                id SERIAL PRIMARY KEY,
                entity_name TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                normalized_name TEXT,
                normalized_name_tsvector TSVECTOR,
                description TEXT,
                metadata JSONB DEFAULT '{}',
                first_seen_date TIMESTAMP DEFAULT NOW(),
                last_seen_date TIMESTAMP DEFAULT NOW(),
                mention_count INTEGER DEFAULT 0,
                sources TEXT[],
                confidence_score DECIMAL(3,2) DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create media_entity_mentions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_entity_mentions (
                id SERIAL PRIMARY KEY,
                entity_id INTEGER REFERENCES media_entities(id),
                media_type TEXT NOT NULL,
                media_id INTEGER NOT NULL,
                mention_context TEXT,
                confidence_score DECIMAL(3,2) DEFAULT 0.5,
                mentioned_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_queue_status ON media_collection_queue(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_queue_media_type ON media_collection_queue(media_type)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_articles_domain ON media_news_articles(source_domain)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_videos_platform ON media_videos(platform)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_entities_name ON media_entities(entity_name)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_entities_type ON media_entities(entity_type)")
        
        conn.commit()
        print("✓ All tables and indexes created")
    
    conn.close()


def main():
    """Main setup function."""
    print("=" * 60)
    print("SETTING UP TEST DATABASE")
    print("=" * 60)
    
    try:
        create_test_database()
        create_tables()
        print("=" * 60)
        print("SETUP COMPLETE")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"✗ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
