#!/usr/bin/env python3
"""
Phase 3: Content Extraction Pipeline

Purpose: Fetch full article content from URLs using Trafilatura.

Input:
  - URLs from `article_discovery_queue` table (status='pending')

Output:
  - Full articles saved to `media_news_articles` table
  - Extraction metadata (author, date, categories, etc.)
  - Updated status in queue

Usage:
  # Test mode (process 10 URLs)
  python phase3_extraction.py --test --limit 10
  
  # Bulk mode (process all pending URLs)
  python phase3_extraction.py --bulk --batch-size 100 --rate-limit 2.0

Features:
  - Robust extraction with Trafilatura
  - Fallback to BeautifulSoup if needed
  - Rate limiting to be respectful to servers
  - Progress tracking and resume capability
  - Duplicate detection via fingerprinting
"""

import argparse
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys
from dataclasses import dataclass

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'/tmp/phase3_extraction_{datetime.now():%Y%m%d_%H%M}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('extraction')

# Try to import trafilatura
try:
    from trafilatura import fetch_url, extract
    TRAFILATURA_AVAILABLE = True
    logger.info("Using Trafilatura for extraction")
except ImportError:
    TRAFILATURA_AVAILABLE = False
    logger.warning("Trafilatura not available, will use fallback")
    try:
        from bs4 import BeautifulSoup
        import requests
    except ImportError:
        logger.error("Neither trafilatura nor beautifulsoup available!")
        raise


@dataclass
class ExtractionResult:
    """Result of article extraction."""
    queue_id: int
    url: str
    success: bool
    title: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    hostname: Optional[str] = None
    fingerprint: Optional[str] = None
    image_url: Optional[str] = None
    language: Optional[str] = None
    error: Optional[str] = None
    word_count: int = 0
    extraction_time: float = 0.0


def get_db_connection():
    """Get PostgreSQL connection."""
    import psycopg2
    return psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')


def extract_with_trafilatura(url: str) -> Optional[Dict]:
    """Extract article using Trafilatura."""
    if not TRAFILATURA_AVAILABLE:
        return None
    
    try:
        downloaded = fetch_url(url, timeout=30)
        if not downloaded:
            return None
        
        result = extract(
            downloaded,
            output_format='json',
            include_comments=False,
            include_tables=True,
            include_images=True,
            url=url
        )
        
        if result:
            return json.loads(result)
        return None
        
    except Exception as e:
        logger.error(f"Trafilatura error for {url}: {e}")
        return None


def extract_with_fallback(url: str) -> Optional[Dict]:
    """Fallback extraction using requests + BeautifulSoup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        content = '\n\n'.join(lines)
        
        # Get title
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else None
        
        # Get meta description
        desc_meta = soup.find('meta', attrs={'name': 'description'})
        description = desc_meta.get('content') if desc_meta else None
        
        return {
            'title': title,
            'text': content,
            'description': description,
            'url': url
        }
        
    except Exception as e:
        logger.error(f"Fallback extraction error for {url}: {e}")
        return None


def extract_article(url: str) -> Optional[Dict]:
    """Extract article content using best available method."""
    # Try trafilatura first
    if TRAFILATURA_AVAILABLE:
        result = extract_with_trafilatura(url)
        if result:
            result['_extraction_method'] = 'trafilatura'
            return result
    
    # Fallback to BeautifulSoup
    result = extract_with_fallback(url)
    if result:
        result['_extraction_method'] = 'fallback'
        return result
    
    return None


def process_single_article(queue_id: int, url: str) -> ExtractionResult:
    """Process a single article."""
    start_time = time.time()
    
    data = extract_article(url)
    extraction_time = time.time() - start_time
    
    if not data:
        return ExtractionResult(
            queue_id=queue_id,
            url=url,
            success=False,
            error="Failed to extract content",
            extraction_time=extraction_time
        )
    
    text = data.get('text', '') or data.get('raw_text', '')
    word_count = len(text.split()) if text else 0
    
    return ExtractionResult(
        queue_id=queue_id,
        url=url,
        success=True,
        title=data.get('title'),
        author=data.get('author'),
        publish_date=data.get('date'),
        content=text,
        description=data.get('description'),
        categories=data.get('categories', []),
        tags=data.get('tags', []),
        hostname=data.get('hostname'),
        fingerprint=data.get('fingerprint'),
        image_url=data.get('image'),
        language=data.get('language'),
        word_count=word_count,
        extraction_time=extraction_time
    )


def get_pending_urls(limit: Optional[int] = None) -> List[Tuple[int, str, str]]:
    """Get pending URLs from discovery queue."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
        SELECT id, url, title
        FROM article_discovery_queue
        WHERE status = 'pending'
        ORDER BY discovered_at
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    cur.execute(query)
    urls = [(row[0], row[1], row[2]) for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return urls


def save_article_to_database(result: ExtractionResult, queue_data: Dict) -> bool:
    """Save extracted article to media_news_articles table."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO media_news_articles (
                source_domain,
                source_name,
                article_url,
                title,
                authors,
                publish_date,
                publish_timestamp,
                content,
                summary,
                keywords,
                word_count,
                primary_topic,
                discovery_source,
                collection_method,
                extraction_method,
                extraction_confidence,
                collected_at,
                entities_mentioned,
                all_topics
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s
            )
            ON CONFLICT (article_url) DO NOTHING
            RETURNING id
        """, (
            result.hostname or 'unknown',
            queue_data.get('source', 'Unknown'),
            result.url,
            result.title or queue_data.get('title', 'Untitled'),
            [result.author] if result.author else None,
            result.publish_date,
            result.publish_date,
            result.content,
            result.description,
            result.tags,
            result.word_count,
            'news',
            queue_data.get('discovery_method', 'rss'),
            result.fingerprint or 'direct',
            result.extraction_time,
            json.dumps({
                'categories': result.categories,
                'tags': result.tags,
                'hostname': result.hostname,
                'fingerprint': result.fingerprint,
                'image_url': result.image_url,
                'language': result.language,
                'extraction_method': 'trafilatura' if TRAFILATURA_AVAILABLE else 'fallback'
            }),
            json.dumps({}) if not result.categories else json.dumps({'categories': result.categories})
        ))
        
        inserted = cur.fetchone()
        
        # Update queue status
        if inserted:
            cur.execute("""
                UPDATE article_discovery_queue
                SET status = 'completed', processed_at = NOW()
                WHERE id = %s
            """, (result.queue_id,))
        else:
            # Duplicate URL
            cur.execute("""
                UPDATE article_discovery_queue
                SET status = 'duplicate', processed_at = NOW()
                WHERE id = %s
            """, (result.queue_id,))
        
        conn.commit()
        return True
        
    except Exception as e:
        logger.error(f"Database error: {e}")
        conn.rollback()
        
        # Mark as failed
        cur.execute("""
            UPDATE article_discovery_queue
            SET status = 'failed', processed_at = NOW()
            WHERE id = %s
        """, (result.queue_id,))
        conn.commit()
        
        return False
    finally:
        cur.close()
        conn.close()


def run_test_sample(limit: int = 10):
    """Test extraction on small sample."""
    logger.info(f"Testing extraction on {limit} articles")
    
    pending = get_pending_urls(limit)
    logger.info(f"Found {len(pending)} pending URLs")
    
    if not pending:
        logger.warning("No pending URLs found. Run phase1_discovery.py first.")
        return
    
    results = []
    success_count = 0
    
    for i, (queue_id, url, title) in enumerate(pending, 1):
        logger.info(f"[{i}/{len(pending)}] Processing: {url[:80]}...")
        
        result = process_single_article(queue_id, url)
        results.append(result)
        
        if result.success:
            success_count += 1
            logger.info(f"  ✓ Success: {result.word_count} words")
            
            # Save to database
            queue_data = {'source': 'RSS', 'title': title, 'discovery_method': 'rss'}
            if save_article_to_database(result, queue_data):
                logger.info(f"  ✓ Saved to database")
            else:
                logger.error(f"  ✗ Failed to save")
        else:
            logger.error(f"  ✗ Failed: {result.error}")
        
        # Rate limiting
        if i < len(pending):
            time.sleep(2)
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("TEST SAMPLE RESULTS")
    logger.info("="*60)
    logger.info(f"Total: {len(results)}")
    logger.info(f"Successful: {success_count} ({success_count/len(results)*100:.1f}%)")
    logger.info(f"Failed: {len(results) - success_count}")
    
    if success_count > 0:
        avg_words = sum(r.word_count for r in results if r.success) / success_count
        logger.info(f"Average words per article: {avg_words:.0f}")
    
    # Show sample content
    logger.info("\n--- Sample Extracted Content ---")
    for result in results[:3]:
        if result.success and result.content:
            logger.info(f"\n[{result.title or 'No Title'}]")
            preview = result.content[:300].replace('\n', ' ')
            logger.info(f"Preview: {preview}...")


def run_bulk_extraction(batch_size: int = 100, rate_limit: float = 2.0):
    """Run bulk extraction on all pending URLs."""
    logger.info("Starting bulk extraction")
    
    pending = get_pending_urls()
    total = len(pending)
    
    if not pending:
        logger.warning("No pending URLs found. Run phase1_discovery.py first.")
        return
    
    logger.info(f"Total pending URLs: {total}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Rate limit: {rate_limit}s")
    logger.info(f"Estimated time: {(total * (rate_limit + 3)) / 3600:.1f} hours")
    
    success_count = 0
    fail_count = 0
    total_words = 0
    
    for batch_num, i in enumerate(range(0, total, batch_size), 1):
        batch = pending[i:i + batch_size]
        logger.info(f"\n--- Batch {batch_num}/{(total // batch_size) + 1} ---")
        
        batch_success = 0
        batch_fail = 0
        
        for queue_id, url, title in batch:
            result = process_single_article(queue_id, url)
            
            if result.success:
                batch_success += 1
                total_words += result.word_count
                
                queue_data = {'source': 'RSS', 'title': title, 'discovery_method': 'rss'}
                save_article_to_database(result, queue_data)
                
                logger.info(f"  ✓ {result.word_count} words - {result.title[:50] if result.title else 'No title'}...")
            else:
                batch_fail += 1
                logger.error(f"  ✗ Failed - {result.error}")
            
            time.sleep(rate_limit)
        
        success_count += batch_success
        fail_count += batch_fail
        
        progress = (i + len(batch)) / total * 100
        logger.info(f"Progress: {progress:.1f}% | Success: {success_count} | Failed: {fail_count}")
        
        # Checkpoint every 10 batches
        if batch_num % 10 == 0:
            with open(f'/tmp/extraction_checkpoint_{batch_num}.json', 'w') as f:
                json.dump({
                    'batch': batch_num,
                    'processed': success_count + fail_count,
                    'success': success_count,
                    'failed': fail_count,
                    'total_words': total_words
                }, f)
    
    # Final summary
    logger.info("\n" + "="*60)
    logger.info("BULK EXTRACTION COMPLETE")
    logger.info("="*60)
    logger.info(f"Total: {success_count + fail_count}")
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {fail_count}")
    logger.info(f"Total words: {total_words:,}")
    if success_count > 0:
        logger.info(f"Avg words/article: {total_words/success_count:.0f}")


def main():
    parser = argparse.ArgumentParser(description='Phase 3: Extract article content from URLs')
    parser.add_argument('--test', action='store_true', help='Test mode - process small sample')
    parser.add_argument('--limit', type=int, default=10, help='Number of URLs to test')
    parser.add_argument('--bulk', action='store_true', help='Bulk mode - process all pending')
    parser.add_argument('--batch-size', type=int, default=100, help='Batch size for bulk mode')
    parser.add_argument('--rate-limit', type=float, default=2.0, help='Seconds between requests')
    
    args = parser.parse_args()
    
    if args.test:
        run_test_sample(args.limit)
    elif args.bulk:
        run_bulk_extraction(args.batch_size, args.rate_limit)
    else:
        print("Usage:")
        print("  python phase3_extraction.py --test --limit 10")
        print("  python phase3_extraction.py --bulk --batch-size 100")
        print("\nRecommended workflow:")
        print("  1. Test first: --test --limit 10")
        print("  2. If successful: --bulk --batch-size 100")


if __name__ == '__main__':
    main()
