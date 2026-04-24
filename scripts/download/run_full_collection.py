#!/usr/bin/env python3
"""
Master Collection and Ingestion Script
Handles everything: database setup, URL collection, and article ingestion
"""

import asyncio
import aiohttp
import json
import os
import sys
import subprocess
from datetime import datetime

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

def setup_database():
    """Ensure database tables exist."""
    print("[1] Checking database...")
    
    import psycopg2
    from media_acquisition.config import DATABASE_URL
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check if media_news_articles exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'media_news_articles'
        )
    """)
    exists = cur.fetchone()[0]
    
    if not exists:
        print("  ! Tables not found, running migrations...")
        conn.close()
        
        # Run migrations
        result = subprocess.run(
            ['python3', 'scripts/apply_migrations.py', '--apply'],
            cwd='/home/cbwinslow/workspace/epstein',
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✓ Migrations applied")
        else:
            print(f"  ✗ Migration failed: {result.stderr}")
            return False
    else:
        print("  ✓ Database tables exist")
    
    conn.close()
    return True

def collect_urls():
    """Collect URLs from news sources."""
    print("\n[2] Collecting URLs from news sources...")
    
    # Check if URLs already collected
    urls_file = '/home/cbwinslow/workspace/epstein-data/urls/epstein_2020_2024.json'
    
    if os.path.exists(urls_file) and os.path.getsize(urls_file) > 100:
        with open(urls_file, 'r') as f:
            urls = json.load(f)
        print(f"  ✓ Found existing collection: {len(urls)} URLs")
        return urls
    
    print("  ! No existing URLs found")
    print("  Use: python3 scripts/collect_news_sources.py epstein 2020 2024")
    return []

def ingest_urls(urls, batch_size=10):
    """Ingest URLs into database."""
    print(f"\n[3] Ingesting {min(batch_size, len(urls))} URLs...")
    
    from scripts.article_ingestion_pipeline import ArticleIngestionPipeline
    from media_acquisition.config import DATABASE_URL
    
    async def run_ingestion():
        async with aiohttp.ClientSession() as session:
            pipeline = ArticleIngestionPipeline(DATABASE_URL)
            
            success = 0
            failed = 0
            
            for i, item in enumerate(urls[:batch_size]):
                url = item.get('url')
                title = item.get('title', 'Unknown')[:50]
                
                print(f"  [{i+1}/{batch_size}] {title}...", end=' ')
                
                try:
                    result = await pipeline.ingest_article(
                        url=url,
                        keywords_matched=[item.get('search_query', 'jeffrey epstein')],
                        priority=5,
                        discovered_by='google_news'
                    )
                    
                    if result:
                        print(f"✓ (ID: {result})")
                        success += 1
                    else:
                        print("✗")
                        failed += 1
                        
                except Exception as e:
                    print(f"✗ ({str(e)[:40]})")
                    failed += 1
                
                await asyncio.sleep(1)  # Rate limiting
            
            return success, failed
    
    success, failed = asyncio.run(run_ingestion())
    
    print(f"\n  Results: {success} success, {failed} failed")
    return success, failed

def main():
    print("="*70)
    print("HISTORICAL DATA COLLECTION - MASTER SCRIPT")
    print("="*70)
    
    # Step 1: Setup database
    if not setup_database():
        print("\n✗ Database setup failed")
        return
    
    # Step 2: Collect URLs
    urls = collect_urls()
    
    if not urls:
        print("\n✗ No URLs to ingest")
        return
    
    # Step 3: Ingest URLs
    success, failed = ingest_urls(urls, batch_size=5)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"URLs collected: {len(urls)}")
    print(f"Successfully ingested: {success}")
    print(f"Failed: {failed}")
    
    if success > 0:
        print("\n✅ Collection and ingestion working!")
        print("\nTo continue:")
        print("  - Run full collection: python3 scripts/collect_news_sources.py epstein 2019 2024")
        print("  - Run batch ingestion: python3 scripts/batch_ingest_historical.py <urls_file>")
    else:
        print("\n⚠️  Had issues. Check logs above.")

if __name__ == '__main__':
    main()
