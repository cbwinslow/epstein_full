#!/usr/bin/env python3
"""
Staged news ingestion orchestrator for large-scale historical collection.
Runs year-by-year from 2000 to present, managing batches and tracking progress.
"""

import asyncio
import argparse
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json
import sys

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from run_news_ingestion import (
    create_ingestion_run,
    update_run_results,
    complete_ingestion_run
)
from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.agents.discovery.google_news import GoogleNewsScraper
from media_acquisition.agents.discovery.rss_aggregator import RSSAggregatorAgent
from media_acquisition.base import AgentConfig, StorageManager, NewsArticleURL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StagedIngestionOrchestrator:
    """
    Orchestrate large-scale historical news ingestion.
    Breaks down 2000-2024 into manageable year-by-year runs.
    """

    def __init__(self,
                 keywords: List[str],
                 start_year: int = 2000,
                 end_year: int = 2024,
                 articles_per_year: int = 500,
                 batch_months: int = 3):
        """
        Initialize orchestrator.

        Args:
            keywords: Search keywords
            start_year: Earliest year to collect (default 2000)
            end_year: Latest year to collect (default 2024)
            articles_per_year: Target articles per year
            batch_months: Process in X-month batches for granularity
        """
        self.keywords = keywords
        self.start_year = start_year
        self.end_year = end_year
        self.articles_per_year = articles_per_year
        self.batch_months = batch_months

        self.storage = StorageManager(
            connection_string='postgresql://cbwinslow:123qweasd@localhost:5432/epstein',
            base_path='/home/cbwinslow/workspace/epstein-data/media'
        )

        # Track overall progress
        self.total_discovered = 0
        self.total_queued = 0
        self.total_collected = 0
        self.total_failed = 0

        # Stage tracking
        self.stage_runs: List[Dict] = []

    def generate_stages(self) -> List[Tuple[str, str, int]]:
        """
        Generate ingestion stages as (start_date, end_date, max_results) tuples.
        Breaks years into batches for better granularity.
        """
        stages = []

        for year in range(self.start_year, self.end_year + 1):
            # Divide year into batches
            if self.batch_months == 12:
                # One batch per year
                start = f"{year}-01-01"
                end = f"{year}-12-31"
                max_results = self.articles_per_year
                stages.append((start, end, max_results))
            else:
                # Multiple batches per year
                for month in range(1, 13, self.batch_months):
                    start_month = month
                    end_month = min(month + self.batch_months - 1, 12)

                    start = f"{year}-{start_month:02d}-01"
                    # Approximate end date
                    if end_month == 12:
                        end = f"{year}-12-31"
                    else:
                        end = f"{year}-{end_month + 1:02d}-01"

                    # Divide max results across batches
                    max_results = max(50, self.articles_per_year // (12 // self.batch_months))
                    stages.append((start, end, max_results))

        return stages

    async def run_discovery(self,
                           stage_run_id: str,
                           start_date: str,
                           end_date: str,
                           max_results: int) -> List[NewsArticleURL]:
        """Run multi-source discovery for a stage."""
        logger.info(f"[STAGE {stage_run_id[:8]}] Discovery: {start_date} to {end_date}")

        all_articles = []
        source_breakdown = {}

        # 1. Google News (primary source)
        try:
            scraper = GoogleNewsScraper(delay=1.5)
            result = scraper.search(
                keywords=self.keywords,
                date_range=(start_date, end_date),
                max_results=max_results // 2  # Split quota
            )
            if result.output:
                all_articles.extend(result.output)
                source_breakdown['google_news'] = len(result.output)
                logger.info(f"  Google News: {len(result.output)} articles")
        except Exception as e:
            logger.warning(f"  Google News failed: {e}")

        # 2. RSS Aggregator (multiple sources)
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
                max_results=max_results // 2,
                max_sources=30
            )
            await rss_agent.close()

            if result.output:
                # Filter out duplicates
                existing_urls = {a.url for a in all_articles}
                new_articles = [a for a in result.output if a.url not in existing_urls]
                all_articles.extend(new_articles)
                source_breakdown['rss_aggregator'] = len(new_articles)
                logger.info(f"  RSS Aggregator: {len(new_articles)} new articles")
        except Exception as e:
            logger.warning(f"  RSS aggregator failed: {e}")

        # 3. GDELT (if available)
        # Note: Rate limited, use sparingly
        if len(all_articles) < max_results * 0.5:
            try:
                from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
                config = AgentConfig(agent_id='gdelt-backup')
                agent = NewsDiscoveryAgent(config)
                result = await agent.execute({
                    'keywords': self.keywords,
                    'date_range': (start_date, end_date),
                    'max_results': max_results - len(all_articles)
                })
                if result.output:
                    existing_urls = {a.url for a in all_articles}
                    new_articles = [a for a in result.output if a.url not in existing_urls]
                    all_articles.extend(new_articles)
                    source_breakdown['gdelt'] = len(new_articles)
                    logger.info(f"  GDELT: {len(new_articles)} articles")
            except Exception as e:
                logger.warning(f"  GDELT failed: {e}")

        # Update stage with source breakdown
        await update_run_results(
            stage_run_id,
            len(all_articles),
            0, 0, 0,
            source_breakdown
        )

        logger.info(f"[STAGE {stage_run_id[:8]}] Total discovered: {len(all_articles)}")
        return all_articles

    async def run_stage(self,
                       start_date: str,
                       end_date: str,
                       max_results: int) -> Dict:
        """Run a single ingestion stage."""
        stage_run_id = await create_ingestion_run(
            keywords=self.keywords,
            start_date=start_date,
            end_date=end_date,
            max_results=max_results,
            run_name=f"Staged Ingestion {start_date} to {end_date}"
        )

        logger.info(f"\n{'='*60}")
        logger.info(f"STAGE: {start_date} to {end_date}")
        logger.info(f"Run ID: {stage_run_id}")
        logger.info(f"{'='*60}")

        try:
            # Discovery
            articles = await self.run_discovery(
                stage_run_id, start_date, end_date, max_results
            )

            if not articles:
                logger.warning(f"[STAGE {stage_run_id[:8]}] No articles discovered")
                await complete_ingestion_run(stage_run_id, 'completed', 'No articles found')
                return {'run_id': stage_run_id, 'status': 'empty', 'collected': 0}

            # Queue articles
            queued = 0
            for article in articles:
                try:
                    item_id = self.storage.queue_item(
                        media_type='news',
                        source_url=article.url,
                        priority=article.priority,
                        keywords_matched=article.keywords_matched,
                        discovered_by=f'staged-orchestrator-{stage_run_id[:8]}',
                        ingestion_run_id=stage_run_id
                    )
                    if item_id:
                        queued += 1
                    else:
                        # Link existing
                        self.storage.link_queue_item_to_run(article.url, 'news', stage_run_id)
                        queued += 1
                except Exception as e:
                    logger.warning(f"Failed to queue {article.url}: {e}")

            self.total_queued += queued

            result = {
                'run_id': stage_run_id,
                'status': 'completed',
                'start_date': start_date,
                'end_date': end_date,
                'discovered': len(articles),
                'queued': queued,
                'collected': collected,
                'failed': failed
            }
            self.stage_runs.append(result)
            return result

        except Exception as e:
            logger.error(f"[STAGE {stage_run_id[:8]}] Failed: {e}")
            await complete_ingestion_run(stage_run_id, 'failed', str(e)[:500])
            return {'run_id': stage_run_id, 'status': 'failed', 'error': str(e)}

    async def run_all_stages(self, skip_existing: bool = True):
        """Run all stages sequentially."""
        stages = self.generate_stages()
        logger.info(f"Generated {len(stages)} stages from {self.start_year} to {self.end_year}")

        completed = 0
        failed = 0

        for idx, (start_date, end_date, max_results) in enumerate(stages, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"PROGRESS: Stage {idx}/{len(stages)} ({idx/len(stages)*100:.1f}%)")
            logger.info(f"{'='*60}")

            result = await self.run_stage(start_date, end_date, max_results)

            if result['status'] == 'completed':
                completed += 1
            elif result['status'] == 'failed':
                failed += 1

            # Brief pause between stages
            await asyncio.sleep(2)

        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info("STAGED INGESTION COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Stages completed: {completed}/{len(stages)}")
        logger.info(f"Stages failed: {failed}")
        logger.info(f"Total discovered: {self.total_discovered}")
        logger.info(f"Total queued: {self.total_queued}")
        logger.info(f"Total collected: {self.total_collected}")
        logger.info(f"Total failed: {self.total_failed}")

        return {
            'stages_total': len(stages),
            'stages_completed': completed,
            'stages_failed': failed,
            'total_discovered': self.total_discovered,
            'total_collected': self.total_collected,
            'stage_details': self.stage_runs
        }


def main():
    parser = argparse.ArgumentParser(description='Staged Historical News Ingestion')
    parser.add_argument('--start-year', type=int, default=2000,
                       help='Start year (default: 2000)')
    parser.add_argument('--end-year', type=int, default=2024,
                       help='End year (default: 2024)')
    parser.add_argument('--articles-per-year', type=int, default=500,
                       help='Target articles per year (default: 500)')
    parser.add_argument('--batch-months', type=int, default=3,
                       help='Process in X-month batches (default: 3)')
    parser.add_argument('--keywords', nargs='+',
                       default=['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre'],
                       help='Search keywords')

    args = parser.parse_args()

    orchestrator = StagedIngestionOrchestrator(
        keywords=args.keywords,
        start_year=args.start_year,
        end_year=args.end_year,
        articles_per_year=args.articles_per_year,
        batch_months=args.batch_months
    )

    try:
        results = asyncio.run(orchestrator.run_all_stages())

        # Save results
        output_file = f"/tmp/staged_ingestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"\nResults saved to: {output_file}")

    except KeyboardInterrupt:
        logger.info("\nOrchestrator interrupted by user")
    except Exception as e:
        logger.error(f"Orchestrator failed: {e}")
        raise


if __name__ == '__main__':
    main()
