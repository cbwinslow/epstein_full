#!/usr/bin/env python3
"""
Enrich existing articles with Trafilatura content extraction.
Uses the 9,283 URLs already in your database.
"""

import json
import logging
import psycopg2
from trafilatura import fetch_url, extract
from typing import Optional, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URL = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'


def get_articles_without_content(limit: int = 100) -> list:
    """Get articles that need content extraction."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, article_url, title 
        FROM media_news_articles 
        WHERE (content IS NULL OR LENGTH(content) < 100)
        AND article_url NOT LIKE '%%news.google.com%%'
        LIMIT %s
    """, (limit,))
    
    articles = cur.fetchall()
    cur.close()
    conn.close()
    
    return articles


def extract_with_trafilatura(url: str) -> Optional[Dict]:
    """Extract ALL content and metadata using Trafilatura."""
    try:
        downloaded = fetch_url(url)
        if not downloaded:
            return None
        
        # Extract with maximum metadata
        result = extract(
            downloaded,
            output_format='json',
            include_comments=False,
            include_tables=True,
            include_images=True,
            include_links=True,
            url=url,
            with_metadata=True
        )
        
        if result:
            data = json.loads(result)
            content = data.get('text', '') or data.get('raw_text', '')
            
            return {
                # Core content
                'content': content,
                'title': data.get('title'),
                'author': data.get('author'),
                'publish_date': data.get('date'),
                'word_count': len(content.split()) if content else 0,
                
                # Full metadata
                'description': data.get('description'),
                'categories': data.get('categories', []),
                'tags': data.get('tags', []),
                'language': data.get('language', 'en'),
                'fingerprint': data.get('fingerprint'),
                'hostname': data.get('hostname'),
                'source': data.get('source'),
                'url': data.get('url', url),
                'license': data.get('license'),
                'image_url': data.get('image'),
                'image_urls': data.get('images', []),
                'link_urls': data.get('links', []),
                
                # Additional metadata
                'sitename': data.get('sitename'),
                'raw_html': data.get('raw_html', '')[:50000],  # First 50KB of raw HTML
                'extraction_success': True
            }
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
    
    return None


def update_article(article_id: int, data: Dict) -> bool:
    """Update article with extracted content."""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE media_news_articles 
            SET content = %s,
                authors = %s,
                publish_date = COALESCE(%s, publish_date),
                word_count = %s,
                summary = %s,
                language = %s,
                all_topics = %s,
                collected_at = NOW()
            WHERE id = %s
        """, (
            data['content'],
            [data['author']] if data.get('author') else None,
            data.get('publish_date'),
            data['word_count'],
            data.get('description', '')[:1000] if data.get('description') else None,
            data.get('language', 'en'),
            json.dumps({
                'categories': data.get('categories', []),
                'tags': data.get('tags', []),
                'fingerprint': data.get('fingerprint'),
                'hostname': data.get('hostname'),
                'source': data.get('source'),
                'image_url': data.get('image_url'),
                'image_urls': data.get('image_urls', []),
                'link_urls': data.get('link_urls', []),
                'sitename': data.get('sitename'),
                'license': data.get('license'),
                'extraction_success': data.get('extraction_success', True),
                'extraction_method': 'trafilatura_v2_full'
            }),
            article_id
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Update failed: {e}")
        return False


def main():
    logger.info("="*60)
    logger.info("Enriching articles with Trafilatura")
    logger.info("="*60)
    
    # Get articles needing content
    articles = get_articles_without_content(limit=50)
    logger.info(f"Found {len(articles)} articles to process")
    
    if not articles:
        logger.info("No articles need enrichment!")
        return
    
    success = 0
    failed = 0
    
    for i, (article_id, url, title) in enumerate(articles):
        logger.info(f"[{i+1}/{len(articles)}] {title[:60]}...")
        
        data = extract_with_trafilatura(url)
        
        if data and data.get('content'):
            if update_article(article_id, data):
                success += 1
                logger.info(f"  ✓ Updated ({data['word_count']} words)")
            else:
                failed += 1
                logger.info("  ✗ Update failed")
        else:
            failed += 1
            logger.info("  ✗ No content extracted")
    
    logger.info("\n" + "="*60)
    logger.info(f"Complete: {success} success, {failed} failed")
    logger.info("="*60)


if __name__ == '__main__':
    main()
