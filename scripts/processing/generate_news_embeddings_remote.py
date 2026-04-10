#!/usr/bin/env python3
"""
Generate embeddings for news articles using remote Windows GPU endpoint
Usage: python3 scripts/generate_news_embeddings_remote.py
"""

import requests
import psycopg2
import logging
import hashlib
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
EMBEDDINGS_URL = "http://192.168.1.100:8000"  # Update with Windows IP
AUTH_TOKEN = "epstein-embeddings-2024"
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"


def generate_content_hash(title: str, content: str) -> str:
    """Generate SHA-256 hash for deduplication."""
    text = f"{title}|||{content}"
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def check_endpoint_health() -> bool:
    """Check if embeddings endpoint is healthy."""
    try:
        response = requests.get(f"{EMBEDDINGS_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            logger.info(f"Endpoint healthy: {health}")
            return True
    except Exception as e:
        logger.error(f"Cannot connect to embeddings endpoint: {e}")
    return False


def get_articles_without_embeddings(conn, limit: int = 1000) -> list:
    """Get articles that don't have embeddings yet."""
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, summary, content
        FROM media_news_articles
        WHERE title_embedding IS NULL
        AND title IS NOT NULL
        ORDER BY collected_at DESC
        LIMIT %s
    """, (limit,))
    return cur.fetchall()


def generate_embedding_remote(text: str) -> Optional[list]:
    """Generate embedding via remote Windows GPU endpoint."""
    try:
        response = requests.post(
            f"{EMBEDDINGS_URL}/embed",
            json={"texts": [text], "batch_size": 1},
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["embeddings"][0]
        else:
            logger.error(f"Embedding request failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None


def update_article_embeddings(conn, article_id: int, title_emb: list, 
                             summary_emb: Optional[list], content_emb: Optional[list],
                             content_hash: Optional[str], title_hash: str) -> bool:
    """Update article with embeddings and hashes."""
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE media_news_articles
            SET title_embedding = %s,
                summary_embedding = %s,
                content_embedding = %s,
                content_hash = %s,
                title_hash = %s
            WHERE id = %s
        """, (title_emb, summary_emb, content_emb, content_hash, title_hash, article_id))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error updating article {article_id}: {e}")
        conn.rollback()
        return False


def main():
    logger.info("=" * 60)
    logger.info("NEWS ARTICLE EMBEDDING GENERATION (REMOTE GPU)")
    logger.info("=" * 60)
    
    # Check endpoint health
    if not check_endpoint_health():
        logger.error("Embeddings endpoint is not available. Exiting.")
        return
    
    # Database connection
    try:
        conn = psycopg2.connect(DB_URL)
        logger.info("Connected to database")
    except Exception as e:
        logger.error(f"Cannot connect to database: {e}")
        return
    
    # Get articles without embeddings
    logger.info("Fetching articles without embeddings...")
    articles = get_articles_without_embeddings(conn, limit=1000)
    logger.info(f"Found {len(articles)} articles to process")
    
    if len(articles) == 0:
        logger.info("No articles to process. Exiting.")
        conn.close()
        return
    
    # Process articles
    processed = 0
    skipped = 0
    errors = 0
    
    for i, (article_id, title, summary, content) in enumerate(articles, 1):
        try:
            # Generate hashes
            title_hash = hashlib.sha256(title.encode('utf-8')).hexdigest()
            content_hash = generate_content_hash(title, content) if content else None
            
            # Generate title embedding
            title_emb = generate_embedding_remote(title)
            if title_emb is None:
                logger.warning(f"Skipping article {article_id}: failed to generate title embedding")
                skipped += 1
                continue
            
            # Generate summary embedding
            summary_emb = None
            if summary and len(summary.strip()) > 10:
                summary_emb = generate_embedding_remote(summary)
            
            # Generate content embedding
            content_emb = None
            if content and len(content.strip()) > 100:
                content_emb = generate_embedding_remote(content)
            
            # Update database
            if update_article_embeddings(
                conn, article_id, 
                title_emb, summary_emb, content_emb,
                content_hash, title_hash
            ):
                processed += 1
            
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{len(articles)} processed ({processed} successful, {skipped} skipped, {errors} errors)")
                
        except Exception as e:
            logger.error(f"Error processing article {article_id}: {e}")
            errors += 1
    
    conn.close()
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("EMBEDDING GENERATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Processed: {processed}")
    logger.info(f"Skipped: {skipped}")
    logger.info(f"Errors: {errors}")
    logger.info(f"Total: {len(articles)}")


if __name__ == '__main__':
    main()
