#!/usr/bin/env python3
"""
Article Content Fetcher using Trafilatura

Fetches full article text from URLs stored in the database.
Uses trafilatura for robust extraction of article content.

Workflow:
1. Query URLs from database that have empty content
2. Use trafilatura to fetch and extract article text
3. Store extracted content + metadata back to database
4. Validate extraction quality
5. Report statistics

Trafilatura extracts:
- title: Article headline
- author: Article author(s)
- date: Publication date
- article_url: Source URL
- hostname: Domain
- description: Meta description
- categories: Article categories/tags
- tags: Topics/keywords
- fingerprint: Content fingerprint for deduplication
- license: License info
- image: Featured image URL
- text: Full article text (main content)
- comments: Comment count (if available)
- raw_html: Original HTML (optional)
"""

import psycopg2
import json
import time
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys
from dataclasses import dataclass

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

# Try to import trafilatura
try:
    from trafilatura import fetch_url, extract, extract_metadata
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False
    print("⚠ trafilatura not installed. Install with: pip install trafilatura")
    print("  Falling back to basic requests + BeautifulSoup")
    from bs4 import BeautifulSoup
    import requests


@dataclass
class ExtractionResult:
    """Result of article extraction."""
    article_id: str
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
    return psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')


def fetch_with_trafilatura(url: str) -> Optional[Dict]:
    """
    Fetch and extract article using trafilatura.
    
    Returns dict with all extracted metadata or None if failed.
    """
    if not TRAFILATURA_AVAILABLE:
        return None
    
    try:
        # Download the page
        downloaded = fetch_url(url, timeout=30)
        if not downloaded:
            return None
        
        # Extract main content
        result = extract(
            downloaded,
            output_format='json',
            include_comments=False,
            include_tables=True,
            include_images=True,
            article_url=article_url
        )
        
        if result:
            return json.loads(result)
        return None
        
    except Exception as e:
        print(f"  Error extracting {url}: {e}")
        return None


def fetch_with_fallback(url: str) -> Optional[Dict]:
    """
    Fallback extraction using requests + BeautifulSoup.
    Used when trafilatura is not available.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        content = '\n'.join(lines)
        
        # Get title
        title = soup.find('title')
        title = title.get_text() if title else None
        
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
        print(f"  Fallback error for {url}: {e}")
        return None


def process_article(article_id: str, url: str) -> ExtractionResult:
    """
    Process a single article - fetch and extract content.
    
    Args:
        article_id: Database ID of the article
        article_url: URL to fetch
        
    Returns:
        ExtractionResult with all extracted data
    """
    start_time = time.time()
    
    # Try trafilatura first
    if TRAFILATURA_AVAILABLE:
        data = fetch_with_trafilatura(url)
    else:
        data = fetch_with_fallback(url)
    
    extraction_time = time.time() - start_time
    
    if not data:
        return ExtractionResult(
            article_id=article_id,
            url=url,
            success=False,
            error="Failed to extract content",
            extraction_time=extraction_time
        )
    
    # Calculate word count
    text = data.get('text', '') or data.get('raw_text', '')
    word_count = len(text.split()) if text else 0
    
    return ExtractionResult(
        article_id=article_id,
        article_url=article_url,
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


def update_database(result: ExtractionResult) -> bool:
    """
    Update database with extracted content.
    
    Args:
        result: ExtractionResult with extracted data
        
    Returns:
        True if update successful
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Update the article with extracted content
        # Store all metadata in a JSONB column if available, or separate columns
        cur.execute("""
            UPDATE media_news_articles
            SET 
                content = %s,
                word_count = %s,
                title = COALESCE(%s, title),
                publish_date = COALESCE(%s, publish_date),
                author = %s,
                description = %s,
                language_code = %s,
                updated_at = NOW(),
                extraction_metadata = %s
            WHERE id = %s
        """, (
            result.content,
            result.word_count,
            result.title,
            result.publish_date,
            result.author,
            result.description,
            result.language,
            json.dumps({
                'categories': result.categories,
                'tags': result.tags,
                'hostname': result.hostname,
                'fingerprint': result.fingerprint,
                'image_url': result.image_url,
                'extraction_time': result.extraction_time,
                'extraction_method': 'trafilatura' if TRAFILATURA_AVAILABLE else 'fallback',
                'extracted_at': datetime.now().isoformat()
            }),
            result.article_id
        ))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"  Database error for {result.article_id}: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def get_articles_without_content(limit: Optional[int] = None) -> List[Tuple[str, str]]:
    """
    Get articles that need content fetched.
    
    Args:
        limit: Optional limit for testing
        
    Returns:
        List of (article_id, url) tuples
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
        SELECT id, url
        FROM media_news_articles
        WHERE updated_at > '2026-04-09'
          AND (content IS NULL OR TRIM(content) = '')
        ORDER BY RANDOM()
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    cur.execute(query)
    articles = [(row[0], row[1]) for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return articles


def run_test_sample(sample_size: int = 10):
    """
    Run on small sample to validate approach.
    
    Args:
        sample_size: Number of articles to test (default 10)
    """
    print("=" * 80)
    print(f"TESTING ON SAMPLE OF {sample_size} ARTICLES")
    print("=" * 80)
    
    articles = get_articles_without_content(limit=sample_size)
    print(f"\nFound {len(articles)} articles to process")
    
    results = []
    success_count = 0
    
    for i, (article_id, url) in enumerate(articles, 1):
        if not url:
            print(f"\n[{i}/{len(articles)}] Skipping: No URL for article {article_id}")
            continue
        print(f"\n[{i}/{len(articles)}] Processing: {url[:80]}...")
        
        result = process_article(article_id, url)
        results.append(result)
        
        if result.success:
            success_count += 1
            print(f"  ✓ Success: {result.word_count} words")
            print(f"    Title: {result.title[:60] if result.title else 'N/A'}...")
            print(f"    Author: {result.author or 'N/A'}")
            print(f"    Date: {result.publish_date or 'N/A'}")
            
            # Update database
            if update_database(result):
                print(f"  ✓ Database updated")
            else:
                print(f"  ✗ Database update failed")
        else:
            print(f"  ✗ Failed: {result.error}")
        
        # Rate limiting
        if i < len(articles):
            time.sleep(2)  # Be nice to servers
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SAMPLE RESULTS")
    print("=" * 80)
    print(f"Total processed: {len(results)}")
    print(f"Successful: {success_count} ({success_count/len(results)*100:.1f}%)")
    print(f"Failed: {len(results) - success_count}")
    
    if success_count > 0:
        avg_words = sum(r.word_count for r in results if r.success) / success_count
        avg_time = sum(r.extraction_time for r in results if r.success) / success_count
        print(f"\nAverage words per article: {avg_words:.0f}")
        print(f"Average extraction time: {avg_time:.2f}s")
    
    # Show sample content
    print("\n--- Sample Extracted Content ---")
    for result in results[:3]:
        if result.success and result.content:
            print(f"\n[{result.title or 'No Title'}]")
            print(f"Preview: {result.content[:300]}...")
            print("-" * 40)
    
    return results


def run_bulk_processing(batch_size: int = 100, rate_limit: float = 1.0):
    """
    Run bulk processing on all articles.
    
    Args:
        batch_size: Process in batches of N
        rate_limit: Seconds between requests
    """
    print("=" * 80)
    print("BULK ARTICLE FETCHING")
    print("=" * 80)
    
    articles = get_articles_without_content()
    total = len(articles)
    
    print(f"\nTotal articles to process: {total:,}")
    print(f"Batch size: {batch_size}")
    print(f"Rate limit: {rate_limit}s between requests")
    print(f"Estimated time: {(total * (rate_limit + 2)) / 3600:.1f} hours")
    
    success_count = 0
    fail_count = 0
    total_words = 0
    
    for batch_num, i in enumerate(range(0, total, batch_size), 1):
        batch = articles[i:i + batch_size]
        print(f"\n--- Batch {batch_num}/{(total // batch_size) + 1} ({len(batch)} articles) ---")
        
        batch_success = 0
        batch_fail = 0
        
        for article_id, url in batch:
            result = process_article(article_id, url)
            
            if result.success:
                batch_success += 1
                total_words += result.word_count
                update_database(result)
                print(f"  ✓ {result.word_count} words")
            else:
                batch_fail += 1
                print(f"  ✗ Failed")
            
            time.sleep(rate_limit)
        
        success_count += batch_success
        fail_count += batch_fail
        
        # Progress report
        progress = (i + len(batch)) / total * 100
        print(f"\nProgress: {progress:.1f}% | Success: {success_count} | Failed: {fail_count}")
        
        # Save checkpoint every 10 batches
        if batch_num % 10 == 0:
            with open(f'/tmp/fetch_checkpoint_{batch_num}.json', 'w') as f:
                json.dump({
                    'batch': batch_num,
                    'processed': success_count + fail_count,
                    'success': success_count,
                    'failed': fail_count,
                    'total_words': total_words
                }, f)
    
    # Final summary
    print("\n" + "=" * 80)
    print("BULK PROCESSING COMPLETE")
    print("=" * 80)
    print(f"Total processed: {success_count + fail_count}")
    print(f"Successful: {success_count} ({success_count/(success_count+fail_count)*100:.1f}%)")
    print(f"Failed: {fail_count}")
    print(f"Total words extracted: {total_words:,}")
    if success_count > 0:
        print(f"Average words per article: {total_words/success_count:.0f}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch article content using trafilatura')
    parser.add_argument('--test', action='store_true', help='Run test on small sample')
    parser.add_argument('--sample-size', type=int, default=10, help='Sample size for testing')
    parser.add_argument('--bulk', action='store_true', help='Run bulk processing')
    parser.add_argument('--batch-size', type=int, default=100, help='Batch size for bulk')
    parser.add_argument('--rate-limit', type=float, default=1.0, help='Seconds between requests')
    
    args = parser.parse_args()
    
    if args.test:
        run_test_sample(args.sample_size)
    elif args.bulk:
        run_bulk_processing(args.batch_size, args.rate_limit)
    else:
        print("Usage:")
        print("  python fetch_article_content.py --test --sample-size 20")
        print("  python fetch_article_content.py --bulk --batch-size 100")
        print("\nRecommended workflow:")
        print("  1. Test first: --test --sample-size 10")
        print("  2. If successful: --bulk --batch-size 100")
