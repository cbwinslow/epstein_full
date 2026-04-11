#!/usr/bin/env python3
"""
Mega-parallel news ingestion orchestrator.
Leverages 128GB RAM to run 20-30 concurrent stages.
Uses process pools + async for maximum throughput.
"""

import asyncio
import argparse
import logging
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
import json
import sys
import time
import os

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from run_news_ingestion import (
    create_ingestion_run,
    update_run_results,
    complete_ingestion_run,
    collect_articles
)
from media_acquisition.agents.discovery.google_news import GoogleNewsScraper
from media_acquisition.agents.discovery.rss_aggregator import RSSAggregatorAgent
from media_acquisition.base import AgentConfig, StorageManager, NewsArticleURL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mega_parallel_ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global configuration for mega-parallel processing
MAX_CONCURRENT_STAGES = 30  # Number of parallel stage workers
MAX_CONCURRENT_COLLECTION = 20  # Number of parallel article collectors per stage
BATCH_SIZE = 200  # Articles per batch
CHUNK_SIZE = 4  # Months per chunk for finer parallelism


class MegaParallelOrchestrator:
    """
    Mega-parallel orchestrator using 128GB RAM.
    Runs 20-30 stages concurrently with process pools.
    """

    def __init__(self,
                 keywords: List[str],
                 start_year: int = 2000,
                 end_year: int = 2024,
                 articles_per_year: int = 1000,
                 max_workers: int = 30):
        """
        Initialize mega-parallel orchestrator.

        Args:
            keywords: Search keywords
            start_year: Earliest year
            end_year: Latest year
            articles_per_year: Target articles per year
            max_workers: Max parallel stages (default 30)
        """
        self.keywords = keywords
        self.start_year = start_year
        self.end_year = end_year
        self.articles_per_year = articles_per_year
        self.max_workers = max_workers

        # Connection pool for database
        self.connection_string = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'
        self.base_path = '/home/cbwinslow/workspace/epstein-data/media'

        # Stats tracking
        self.stats_lock = asyncio.Lock()
        self.total_discovered = 0
        self.total_queued = 0
        self.total_collected = 0
        self.total_failed = 0
        self.completed_stages = 0
        self.failed_stages = 0

        # Stage tracking
        self.stage_results: List[Dict] = []

    def generate_stage_chunks(self) -> List[Tuple[str, str, int]]:
        """
        Generate small chunks for maximum parallelism.
        Creates 4-month chunks for ~300 total stages.
        """
        chunks = []

        for year in range(self.start_year, self.end_year + 1):
            for month in range(1, 13, CHUNK_SIZE):
                start_month = month
                end_month = min(month + CHUNK_SIZE - 1, 12)

                start = f"{year}-{start_month:02d}-01"
                if end_month == 12:
                    end = f"{year}-12-31"
                else:
                    end = f"{year}-{end_month + 1:02d}-01"

                # Articles per chunk
                max_results = max(100, self.articles_per_year // (12 // CHUNK_SIZE))
                chunks.append((start, end, max_results))

        return chunks

    async def discover_for_stage(self,
                                 stage_id: str,
                                 start_date: str,
                                 end_date: str,
                                 max_results: int) -> List[NewsArticleURL]:
        """Run multi-source discovery for a single stage."""
        all_articles = []
        source_breakdown = {}

        # Create storage for this stage
        storage = StorageManager(
            connection_string=self.connection_string,
            base_path=self.base_path
        )

        # 1. Google News (fastest, most results)
        try:
            scraper = GoogleNewsScraper(delay=0.8)  # Reduced delay
            result = scraper.search(
                keywords=self.keywords,
                date_range=(start_date, end_date),
                max_results=max_results
            )
            if result.output:
                all_articles.extend(result.output)
                source_breakdown['google_news'] = len(result.output)
        except Exception as e:
            logger.warning(f"[Stage {stage_id[:8]}] Google News failed: {e}")

        # 2. RSS Aggregator (parallel sources)
        if len(all_articles) < max_results:
            try:
                rss_agent = RSSAggregatorAgent()
                from datetime import datetime as dt
                date_range_dt = (
                    dt.strptime(start_date, '%Y-%m-%d'),
                    dt.strptime(end_date, '%Y-%m-%d')
                )
                result = await rss_agent.discover(
                    keywords=self.keywords,
                    date_range=date_range_dt,
                    max_results=max_results - len(all_articles),
                    max_sources=20  # Reduced for speed
                )
                await rss_agent.close()

                if result.output:
                    existing_urls = {a.url for a in all_articles}
                    new_articles = [a for a in result.output if a.url not in existing_urls]
                    all_articles.extend(new_articles)
                    source_breakdown['rss'] = len(new_articles)
            except Exception as e:
                logger.warning(f"[Stage {stage_id[:8]}] RSS failed: {e}")

        # Update run with discovery results
        await update_run_results(
            stage_id, len(all_articles), 0, 0, 0, source_breakdown
        )

        return all_articles

    async def process_stage(self,
                           start_date: str,
                           end_date: str,
                           max_results: int,
                           worker_id: int) -> Dict:
        """Process a single stage with full pipeline."""
        stage_start_time = time.time()

        # Create run
        run_id = await create_ingestion_run(
            keywords=self.keywords,
            start_date=start_date,
            end_date=end_date,
            max_results=max_results,
            run_name=f"MegaParallel Stage {start_date} to {end_date}"
        )

        logger.info(f"[Worker {worker_id}] Stage {run_id[:8]}: {start_date} to {end_date}")

        try:
            # Create storage for this worker
            storage = StorageManager(
                connection_string=self.connection_string,
                base_path=self.base_path
            )

            # Discovery
            articles = await self.discover_for_stage(
                run_id, start_date, end_date, max_results
            )

            if not articles:
                await complete_ingestion_run(run_id, 'completed', 'No articles')
                async with self.stats_lock:
                    self.completed_stages += 1
                return {'run_id': run_id, 'status': 'empty', 'discovered': 0}

            # Queue articles
            queued = 0
            for article in articles:
                try:
                    item_id = storage.queue_item(
                        media_type='news',
                        source_url=article.url,
                        priority=article.priority,
                        keywords_matched=article.keywords_matched,
                        discovered_by=f'mega-{worker_id}-{run_id[:8]}',
                        ingestion_run_id=run_id
                    )
                    if item_id:
                        queued += 1
                    else:
                        storage.link_queue_item_to_run(article.url, 'news', run_id)
                        queued += 1
                except Exception as e:
                    logger.warning(f"[Worker {worker_id}] Queue failed: {e}")

            # Collection with high concurrency
            collected, failed = await collect_articles(
                storage, run_id,
                batch_size=BATCH_SIZE,
                max_concurrent=MAX_CONCURRENT_COLLECTION
            )

            # Complete run
            await complete_ingestion_run(run_id, 'completed')

            duration = time.time() - stage_start_time

            # Update global stats
            async with self.stats_lock:
                self.total_discovered += len(articles)
                self.total_queued += queued
                self.total_collected += collected
                self.total_failed += failed
                self.completed_stages += 1

            result = {
                'run_id': run_id,
                'status': 'completed',
                'worker_id': worker_id,
                'start_date': start_date,
                'end_date': end_date,
                'discovered': len(articles),
                'queued': queued,
                'collected': collected,
                'failed': failed,
                'duration_seconds': duration
            }

            logger.info(f"[Worker {worker_id}] ✓ Stage {run_id[:8]} complete: "
                       f"{collected} collected in {duration:.1f}s")

            return result

        except Exception as e:
            logger.error(f"[Worker {worker_id}] ✗ Stage {run_id[:8]} failed: {e}")
            await complete_ingestion_run(run_id, 'failed', str(e)[:500])

            async with self.stats_lock:
                self.failed_stages += 1

            return {'run_id': run_id, 'status': 'failed', 'error': str(e)}

    async def run_mega_parallel(self):
        """Run all stages with mega-parallel processing."""
        chunks = self.generate_stage_chunks()
        total_stages = len(chunks)

        logger.info(f"{'='*60}")
        logger.info(f"MEGA-PARALLEL INGESTION")
        logger.info(f"{'='*60}")
        logger.info(f"Total stages: {total_stages}")
        logger.info(f"Max parallel workers: {self.max_workers}")
        logger.info(f"Collection concurrency: {MAX_CONCURRENT_COLLECTION}")
        logger.info(f"RAM available: ~128GB")
        logger.info(f"{'='*60}")

        # Create semaphore to limit concurrent stages
        semaphore = asyncio.Semaphore(self.max_workers)

        async def process_with_limit(args):
            idx, (start, end, max_r) = args
            async with semaphore:
                return await self.process_stage(start, end, max_r, idx % self.max_workers)

        # Create all tasks
        tasks = [
            process_with_limit((i, chunk))
            for i, chunk in enumerate(chunks)
        ]

        # Progress reporting task
        async def report_progress():
            while True:
                await asyncio.sleep(30)  # Report every 30 seconds
                async with self.stats_lock:
                    completed = self.completed_stages
                    failed = self.failed_stages
                    collected = self.total_collected

                remaining = total_stages - completed - failed
                pct = (completed / total_stages) * 100 if total_stages > 0 else 0

                logger.info(f"\n{'='*60}")
                logger.info(f"PROGRESS: {completed}/{total_stages} ({pct:.1f}%)")
                logger.info(f"Collected: {collected} articles")
                logger.info(f"Failed stages: {failed}")
                logger.info(f"Remaining: {remaining}")
                logger.info(f"{'='*60}\n")

        # Run all tasks with progress reporting
        progress_task = asyncio.create_task(report_progress())

        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_duration = time.time() - start_time

        # Cancel progress reporter
        progress_task.cancel()
        try:
            await progress_task
        except asyncio.CancelledError:
            pass

        # Process results
        for result in results:
            if isinstance(result, dict):
                self.stage_results.append(result)
            else:
                logger.error(f"Stage failed with exception: {result}")

        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info(f"MEGA-PARALLEL INGESTION COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Total duration: {total_duration/3600:.1f} hours")
        logger.info(f"Stages completed: {self.completed_stages}/{total_stages}")
        logger.info(f"Stages failed: {self.failed_stages}")
        logger.info(f"Total discovered: {self.total_discovered}")
        logger.info(f"Total queued: {self.total_queued}")
        logger.info(f"Total collected: {self.total_collected}")
        logger.info(f"Total failed: {self.total_failed}")
        logger.info(f"Throughput: {self.total_collected/(total_duration/3600):.0f} articles/hour")

        return {
            'total_stages': total_stages,
            'completed': self.completed_stages,
            'failed': self.failed_stages,
            'total_discovered': self.total_discovered,
            'total_collected': self.total_collected,
            'duration_hours': total_duration / 3600,
            'throughput_per_hour': self.total_collected / (total_duration / 3600) if total_duration > 0 else 0,
            'stage_details': self.stage_results
        }


def main():
    parser = argparse.ArgumentParser(description='Mega-Parallel News Ingestion')
    parser.add_argument('--start-year', type=int, default=2000)
    parser.add_argument('--end-year', type=int, default=2024)
    parser.add_argument('--articles-per-year', type=int, default=1000)
    parser.add_argument('--max-workers', type=int, default=30,
                       help='Number of parallel stage workers (default: 30)')
    parser.add_argument('--collection-workers', type=int, default=20,
                       help='Parallel collectors per stage (default: 20)')
    parser.add_argument('--keywords', nargs='+',
                       default=['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre'])

    args = parser.parse_args()

    # Set global vars from args
    global MAX_CONCURRENT_STAGES, MAX_CONCURRENT_COLLECTION
    MAX_CONCURRENT_STAGES = args.max_workers
    MAX_CONCURRENT_COLLECTION = args.collection_workers

    orchestrator = MegaParallelOrchestrator(
        keywords=args.keywords,
        start_year=args.start_year,
        end_year=args.end_year,
        articles_per_year=args.articles_per_year,
        max_workers=args.max_workers
    )

    try:
        results = asyncio.run(orchestrator.run_mega_parallel())

        # Save results
        output_file = f"/tmp/mega_parallel_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"\nResults saved to: {output_file}")

    except KeyboardInterrupt:
        logger.info("\nOrchestrator interrupted")
    except Exception as e:
        logger.error(f"Orchestrator failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


if __name__ == '__main__':
    # Set higher process limit for Linux
    import resource
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
    except Exception:
        pass

    main()
