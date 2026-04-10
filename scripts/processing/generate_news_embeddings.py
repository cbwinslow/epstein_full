#!/usr/bin/env python3
"""
Generate embeddings for news articles using sentence-transformers.
Supports GPU acceleration with Tesla K80/K40m.
"""

import hashlib
import logging
import sys
from datetime import datetime

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

import psycopg2
from sentence_transformers import SentenceTransformer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_content_hash(title: str, content: str) -> str:
    """Generate SHA-256 hash for deduplication."""
    text = f"{title}|||{content}"
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def get_articles_without_embeddings(conn, limit=1000):
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


def generate_embeddings(text, model):
    """Generate embedding for text."""
    if not text or len(text.strip()) < 10:
        return None
    return model.encode(text, show_progress_bar=False)


def update_article_embeddings(conn, article_id, title_emb, summary_emb, content_emb, 
                             content_hash, title_hash):
    """Update article with embeddings and hashes."""
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


def main():
    logger.info("=" * 60)
    logger.info("NEWS ARTICLE EMBEDDING GENERATION")
    logger.info("=" * 60)
    
    # Database connection
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    
    # Load model (use nomic-embed-text-v2-moe for 768-dim embeddings)
    logger.info("Loading sentence-transformers model on CPU...")
    model = SentenceTransformer('nomic-ai/nomic-embed-text-v2-moe', trust_remote_code=True, device='cpu')
    logger.info("Model loaded successfully")
    
    # Get articles without embeddings
    logger.info("Fetching articles without embeddings...")
    articles = get_articles_without_embeddings(conn, limit=1000)
    logger.info(f"Found {len(articles)} articles to process")
    
    # Process articles
    processed = 0
    skipped = 0
    errors = 0
    
    for i, (article_id, title, summary, content) in enumerate(articles, 1):
        try:
            # Generate hashes
            title_hash = hashlib.sha256(title.encode('utf-8')).hexdigest()
            content_hash = generate_content_hash(title, content) if content else None
            
            # Generate embeddings
            title_emb = generate_embeddings(title, model)
            summary_emb = generate_embeddings(summary, model) if summary else None
            content_emb = generate_embeddings(content, model) if content and len(content) > 100 else None
            
            if title_emb is None:
                logger.warning(f"Skipping article {article_id}: no valid title")
                skipped += 1
                continue
            
            # Update database
            update_article_embeddings(
                conn, article_id, 
                title_emb.tolist() if title_emb is not None else None,
                summary_emb.tolist() if summary_emb is not None else None,
                content_emb.tolist() if content_emb is not None else None,
                content_hash, title_hash
            )
            
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
