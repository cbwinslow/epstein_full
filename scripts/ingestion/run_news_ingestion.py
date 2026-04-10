#!/usr/bin/env python3
"""
News Ingestion Pipeline for Jeffrey Epstein Articles
Discovers, downloads, and stores news articles in PostgreSQL
Tracks each run with unique UUID for audit trail
"""

import asyncio
import logging
import socket
import sys
import uuid
from datetime import datetime
from typing import Dict, List, Optional

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.agents.collection.news import NewsCollector
from media_acquisition.base import AgentConfig, StorageManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Current run tracking
CURRENT_RUN: Dict = {}


async def check_schema():
    """Check if media schema exists."""
    import psycopg2
    try:
        conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
        cur = conn.cursor()
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'media_news_articles'
            )
        """)
        exists = cur.fetchone()[0]
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        logger.error("Database check failed: %s", e)
        return False


async def create_schema():
    """Create media schema if it doesn't exist."""
    import subprocess
    schema_file = '/home/cbwinslow/workspace/epstein/scripts/create_media_schema.sql'

    logger.info("Creating media schema from %s", schema_file)
    try:
        result = subprocess.run(
            ['psql', '-h', 'localhost', '-U', 'cbwinslow', '-d', 'epstein', '-f', schema_file],
            env={'PGPASSWORD': '123qweasd'},
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Media schema created successfully")
            return True
        else:
            logger.error("Schema creation failed: %s", result.stderr)
            return False
    except Exception as e:
        logger.error("Schema creation error: %s", e)
        return False


async def create_ingestion_run(keywords: List[str], start_date: str, end_date: str,
                                 max_results: int, run_name: Optional[str] = None) -> str:
    """Create a new ingestion run record and return the run_id."""
    import psycopg2
    import json
    import os

    run_id = str(uuid.uuid4())
    logs_path = f"/tmp/news_ingestion_{run_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()

    config_json = json.dumps({'script_version': '2.0', 'keywords': keywords, 'date_range': [start_date, end_date]})

    cur.execute("""
        INSERT INTO media_ingestion_runs (
            id, run_name, run_type, keywords, date_range_start, date_range_end,
            max_results_requested, sources_used, status, started_at,
            logs_path, hostname, pid, config
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s)
    """, (
        run_id,
        run_name,
        'news',
        keywords,
        start_date,
        end_date,
        max_results,
        ['google_news', 'gdelt', 'rss'],
        'running',
        logs_path,
        socket.gethostname(),
        os.getpid(),
        config_json
    ))

    conn.commit()
    cur.close()
    conn.close()

    # Store globally for current run
    CURRENT_RUN['id'] = run_id
    CURRENT_RUN['logs_path'] = logs_path
    CURRENT_RUN['start_time'] = datetime.now()

    logger.info(f"[RUN {run_id[:8]}] Created ingestion run")
    logger.info(f"[RUN {run_id[:8]}] Log file: {logs_path}")

    return run_id


async def update_run_results(run_id: str, discovered: int, queued: int, collected: int,
                             failed: int, sources_breakdown: dict):
    """Update run with discovery/collection results."""
    import psycopg2

    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()

    cur.execute("""
        UPDATE media_ingestion_runs
        SET total_discovered = %s,
            total_queued = %s,
            total_collected = %s,
            total_failed = %s,
            google_news_count = %s,
            gdelt_count = %s,
            wayback_count = %s,
            rss_count = %s
        WHERE id = %s
    """, (
        discovered, queued, collected, failed,
        sources_breakdown.get('google_news', 0),
        sources_breakdown.get('gdelt', 0),
        sources_breakdown.get('wayback', 0),
        sources_breakdown.get('rss', 0),
        run_id
    ))

    conn.commit()
    cur.close()
    conn.close()

    logger.info(f"[RUN {run_id[:8]}] Updated results: {discovered} discovered, {queued} queued, {collected} collected")


async def complete_ingestion_run(run_id: str, status: str = 'completed', error_message: Optional[str] = None):
    """Mark ingestion run as completed or failed."""
    import psycopg2

    start_time = CURRENT_RUN.get('start_time', datetime.now())
    duration = int((datetime.now() - start_time).total_seconds())

    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()

    cur.execute("""
        UPDATE media_ingestion_runs
        SET status = %s,
            completed_at = NOW(),
            duration_seconds = %s,
            error_message = %s
        WHERE id = %s
    """, (status, duration, error_message, run_id))

    conn.commit()
    cur.close()
    conn.close()

    logger.info(f"[RUN {run_id[:8]}] Run {status} in {duration}s")


async def discover_articles(keywords, start_date, end_date, max_results, run_id: str):
    """Discover articles using NewsDiscoveryAgent."""
    logger.info(f"[RUN {run_id[:8]}] === DISCOVERY PHASE ===")
    logger.info(f"[RUN {run_id[:8]}] Keywords: {keywords}")
    logger.info(f"[RUN {run_id[:8]}] Date range: {start_date} to {end_date}")
    logger.info(f"[RUN {run_id[:8]}] Max results: {max_results}")

    config = AgentConfig(agent_id='news-discovery')
    agent = NewsDiscoveryAgent(config)
    
    results = await agent.search(
        keywords=keywords,
        date_range=(start_date, end_date),
        max_results=max_results
    )
    
    logger.info(f"[RUN {run_id[:8]}] Discovered {len(results)} articles")

    # Breakdown by source
    sources = {}
    for article in results:
        source = article.discovery_method
        sources[source] = sources.get(source, 0) + 1

    logger.info(f"[RUN {run_id[:8]}] Source breakdown: {sources}")

    # Update run with discovery results
    await update_run_results(run_id, len(results), 0, 0, 0, sources)

    return results


async def queue_articles(storage, articles, run_id: str):
    """Queue articles for collection, linked to ingestion run."""
    logger.info(f"[RUN {run_id[:8]}] === QUEUEING PHASE ===")

    queued = 0
    skipped = 0
    linked = 0

    for article in articles:
        try:
            item_id = storage.queue_item(
                media_type='news',
                source_url=article.url,
                priority=article.priority,
                keywords_matched=article.keywords_matched,
                discovered_by=f'news-discovery-v2-{run_id[:8]}',
                ingestion_run_id=run_id
            )
            if item_id:
                queued += 1
            else:
                # Item already exists - update it to link to this run
                storage.link_queue_item_to_run(article.url, 'news', run_id)
                linked += 1
        except Exception as e:
            logger.warning(f"[RUN {run_id[:8]}] Failed to queue {article.url}: {e}")

    total_queued = queued + linked
    logger.info(f"[RUN {run_id[:8]}] Queued {queued} new, linked {linked} existing (total: {total_queued})")

    # Update run with queued count
    await update_run_results(run_id, len(articles), total_queued, 0, 0, {})

    return total_queued


async def collect_single_article(storage, collector, item, run_id, idx, total):
    """Collect a single article with proper error handling."""
    try:
        # Mark as processing
        storage.update_queue_status(item['id'], 'processing')

        # Create article URL object
        from media_acquisition.base import NewsArticleURL
        article_url = NewsArticleURL(
            url=item['source_url'],
            title=item.get('metadata', {}).get('title') if item.get('metadata') else None,
            priority=item['priority'],
            keywords_matched=item.get('keywords_matched', []),
            discovery_method=item.get('discovered_by', 'unknown')
        )

        # Collect
        result = await collector.collect(article_url)

        if result and result.get('stored_id'):
            storage.update_queue_status(
                item['id'],
                'completed',
                result_id=result['stored_id']
            )
            logger.info(f"  [{idx}/{total}] ✓ Stored: {result.get('title', 'N/A')[:50]}")
            return 'success'
        else:
            storage.update_queue_status(
                item['id'],
                'failed',
                error_message='Collection returned None'
            )
            logger.warning(f"  [{idx}/{total}] ✗ Failed: {item['source_url'][:50]}")
            return 'failed'

    except Exception as e:
        logger.error(f"  [{idx}/{total}] ✗ Error: {item['source_url'][:50]} - {e}")
        storage.update_queue_status(
            item['id'],
            'failed',
            error_message=str(e)[:500]
        )
        return 'error'


async def collect_articles(storage, run_id: str, batch_size=100, max_concurrent=5):
    """Collect queued articles linked to this run with parallel processing."""
    logger.info(f"[RUN {run_id[:8]}] === COLLECTION PHASE (Parallel: {max_concurrent}) ===")

    config = AgentConfig(agent_id='news-collector')
    collector = NewsCollector(config, storage)

    collected = 0
    failed = 0
    total_processed = 0

    # Get total pending count for this run
    import psycopg2
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM media_collection_queue
        WHERE media_type='news' AND status='pending' AND ingestion_run_id = %s
    """, (run_id,))
    total_pending = cur.fetchone()[0]
    cur.close()
    conn.close()

    logger.info(f"[RUN {run_id[:8]}] Total pending articles for this run: {total_pending}")

    # Process in batches with parallel workers
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_with_limit(args):
        async with semaphore:
            result = await collect_single_article(*args)
            await asyncio.sleep(0.3)  # Rate limiting between articles
            return result

    while True:
        # Get pending items for this run
        items = storage.get_queued_items(
            media_type='news',
            status='pending',
            limit=batch_size,
            ingestion_run_id=run_id
        )

        if not items:
            logger.info("No more pending articles")
            break

        logger.info(f"[Progress] Processed: {total_processed}/{total_pending} | Collected: {collected} | Failed: {failed}")
        logger.info(f"Processing batch of {len(items)} articles with {max_concurrent} concurrent workers...")

        # Create tasks for parallel processing
        tasks = []
        for idx, item in enumerate(items, total_processed + 1):
            task = process_with_limit((storage, collector, item, run_id, idx, total_pending))
            tasks.append(task)

        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Count results
        for result in results:
            total_processed += 1
            if result == 'success':
                collected += 1
            elif result in ('failed', 'error'):
                failed += 1

        logger.info(f"[Batch Complete] Processed: {total_processed}/{total_pending} | Collected: {collected} | Failed: {failed}")
    
    logger.info(f"Collection complete: {collected} collected, {failed} failed")
    return collected, failed


async def show_stats(storage):
    """Show collection statistics."""
    logger.info(f"=== STATISTICS ===")
    
    # Queue summary
    summary = storage.get_queue_summary()
    logger.info(f"Queue summary: {summary}")
    
    # Database counts
    import psycopg2
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT COUNT(*) FROM media_news_articles")
        article_count = cur.fetchone()[0]
        logger.info(f"Total articles in database: {article_count}")
        
        cur.execute("""
            SELECT source_domain, COUNT(*) 
            FROM media_news_articles 
            GROUP BY source_domain 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """)
        top_sources = cur.fetchall()
        logger.info("Top 10 sources:")
        for source, count in top_sources:
            logger.info(f"  {source}: {count}")
        
        cur.execute("""
            SELECT MIN(publish_date), MAX(publish_date) 
            FROM media_news_articles 
            WHERE publish_date IS NOT NULL
        """)
        date_range = cur.fetchone()
        if date_range[0]:
            logger.info(f"Date range: {date_range[0]} to {date_range[1]}")
        
    except Exception as e:
        logger.warning(f"Could not fetch stats: {e}")
    finally:
        cur.close()
        conn.close()


async def main():
    """Main pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description='News Ingestion Pipeline')
    parser.add_argument('--keywords', nargs='+', 
                       default=['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre'],
                       help='Search keywords')
    parser.add_argument('--start-date', default='2019-01-01',
                       help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default='2025-12-31',
                       help='End date (YYYY-MM-DD)')
    parser.add_argument('--max-results', type=int, default=5000,
                       help='Maximum articles to discover')
    parser.add_argument('--batch-size', type=int, default=50,
                       help='Collection batch size')
    parser.add_argument('--skip-discovery', action='store_true',
                       help='Skip discovery, only collect queued items')
    parser.add_argument('--skip-collection', action='store_true',
                       help='Skip collection, only discover and queue')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("NEWS INGESTION PIPELINE - JEFFREY EPSTEIN")
    logger.info("=" * 60)
    logger.info(f"Keywords: {args.keywords}")
    logger.info(f"Date range: {args.start_date} to {args.end_date}")
    logger.info(f"Max results: {args.max_results}")
    logger.info(f"Batch size: {args.batch_size}")
    logger.info("")
    
    # Check schema
    logger.info("Checking database schema...")
    schema_exists = await check_schema()
    if not schema_exists:
        logger.info("Schema does not exist, creating...")
        if not await create_schema():
            logger.error("Failed to create schema, exiting")
            return
    else:
        logger.info("✓ Schema exists")

    run_id = None
    articles = []
    queued = 0
    collected = 0
    failed = 0

    try:
        # Create ingestion run with unique ID
        run_id = await create_ingestion_run(
            keywords=args.keywords,
            start_date=args.start_date,
            end_date=args.end_date,
            max_results=args.max_results,
            run_name=f"News Ingestion {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

        # Initialize storage
        storage = StorageManager(
            connection_string='postgresql://cbwinslow:123qweasd@localhost:5432/epstein',
            base_path='/home/cbwinslow/workspace/epstein-data/media'
        )

        # Discovery phase
        if not args.skip_discovery:
            articles = await discover_articles(
                keywords=args.keywords,
                start_date=args.start_date,
                end_date=args.end_date,
                max_results=args.max_results,
                run_id=run_id
            )

            if articles:
                queued = await queue_articles(storage, articles, run_id)
                logger.info(f"[RUN {run_id[:8]}] Queued {queued} articles for collection")
            else:
                logger.warning(f"[RUN {run_id[:8]}] No articles discovered")
                await complete_ingestion_run(run_id, 'completed', 'No articles discovered')
                return
        else:
            logger.info(f"[RUN {run_id[:8]}] Skipping discovery phase")

        # Collection phase
        if not args.skip_collection:
            collected, failed = await collect_articles(storage, run_id, batch_size=args.batch_size)

            # Update final results
            sources_breakdown = agent.metrics.get('sources_breakdown', {}) if 'agent' in locals() else {}
            await update_run_results(run_id, len(articles), queued, collected, failed, sources_breakdown)

            # Mark run as completed
            await complete_ingestion_run(run_id, 'completed')
        else:
            logger.info(f"[RUN {run_id[:8]}] Skipping collection phase")
            # Mark run as completed (discovery only)
            await complete_ingestion_run(run_id, 'completed')

        # Show statistics
        await show_stats(storage)

        logger.info("")
        logger.info("=" * 60)
        logger.info(f"[RUN {run_id[:8]}] PIPELINE COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Run ID: {run_id}")
        logger.info(f"Collected: {collected}")
        logger.info(f"Failed: {failed}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        if run_id:
            await complete_ingestion_run(run_id, 'failed', str(e)[:500])
        raise


if __name__ == '__main__':
    asyncio.run(main())
