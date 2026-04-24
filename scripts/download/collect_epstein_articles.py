#!/usr/bin/env python3
"""
Epstein Collection Script
Recreates the ingestion that collected 9,700 articles (2000-2025).

This script uses the news_ingestion_framework to:
1. Search Google News for Epstein-related articles
2. Aggregate RSS feeds
3. Collect full article content with Trafilatura
4. Store to PostgreSQL database

Usage:
  # Full recreation (2000-2025, ~9,700 articles)
  python collect_epstein_articles.py --full
  
  # Quick test (2024 only, ~100 articles)
  python collect_epstein_articles.py --test
  
  # Custom range
  python collect_epstein_articles.py --start 2020 --end 2023 --max-stages 20

Framework: scripts/ingestion/news_ingestion_framework.py
"""

import argparse
import asyncio
import sys
from datetime import datetime

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from scripts.ingestion.news_ingestion_framework import (
    run_epstein_ingestion,
    MegaParallelOrchestrator,
    MegaParallelConfig,
    DiscoveryConfig,
    CollectionConfig,
    CollectionQueue
)
from datetime import timedelta


def run_full_collection():
    """Recreate the full 9,700 article ingestion (2000-2025)."""
    print("="*70)
    print("EPSTEIN FULL COLLECTION - 2000 to 2025")
    print("="*70)
    print("Expected: ~9,700 articles")
    print("Time: ~24 hours (with rate limiting)")
    print("="*70)
    
    results = run_epstein_ingestion(
        start_year=2000,
        end_year=2025,
        keywords=['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre'],
        max_stages=30
    )
    
    print("\n" + "="*70)
    print("COLLECTION COMPLETE")
    print("="*70)
    print(f"Articles discovered: {results['total_discovered']:,}")
    print(f"Articles collected: {results['total_collected']:,}")
    print(f"Failed: {results['total_failed']:,}")
    print(f"Success rate: {results['total_collected']/max(results['total_discovered'],1)*100:.1f}%")
    
    return results


def run_test_collection():
    """Quick test collection (2024 only)."""
    print("="*70)
    print("EPSTEIN TEST COLLECTION - 2024 Only")
    print("="*70)
    print("Expected: ~100-200 articles")
    print("Time: ~30 minutes")
    print("="*70)
    
    results = run_epstein_ingestion(
        start_year=2024,
        end_year=2024,
        keywords=['Jeffrey Epstein', 'Epstein'],
        max_stages=5
    )
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print(f"Articles discovered: {results['total_discovered']}")
    print(f"Articles collected: {results['total_collected']}")
    
    return results


def run_custom_collection(start_year: int, end_year: int, max_stages: int):
    """Custom date range collection."""
    print("="*70)
    print(f"EPSTEIN CUSTOM COLLECTION - {start_year} to {end_year}")
    print("="*70)
    
    results = run_epstein_ingestion(
        start_year=start_year,
        end_year=end_year,
        keywords=['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre'],
        max_stages=max_stages
    )
    
    print("\n" + "="*70)
    print("COLLECTION COMPLETE")
    print("="*70)
    print(f"Articles discovered: {results['total_discovered']}")
    print(f"Articles collected: {results['total_collected']}")
    
    return results


def show_stats():
    """Show current collection statistics."""
    import psycopg2
    
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()
    
    # Total articles
    cur.execute("SELECT COUNT(*) FROM media_news_articles WHERE discovery_source = 'mega_parallel_ingestion'")
    total = cur.fetchone()[0]
    
    # By year
    cur.execute("""
        SELECT EXTRACT(YEAR FROM publish_date) as year, COUNT(*)
        FROM media_news_articles
        WHERE discovery_source = 'mega_parallel_ingestion' AND publish_date IS NOT NULL
        GROUP BY EXTRACT(YEAR FROM publish_date)
        ORDER BY year
    """)
    by_year = cur.fetchall()
    
    # Queue stats
    queue = CollectionQueue()
    cur.execute("SELECT COUNT(*), COUNT(CASE WHEN status = 'pending' THEN 1 END) FROM collection_queue")
    queue_stats = cur.fetchone()
    
    cur.close()
    conn.close()
    
    print("="*70)
    print("EPSTEIN COLLECTION STATISTICS")
    print("="*70)
    print(f"Total articles collected: {total:,}")
    print(f"\nBy Year:")
    for year, count in by_year:
        print(f"  {int(year)}: {count:,}")
    print(f"\nQueue status:")
    print(f"  Total in queue: {queue_stats[0]:,}")
    print(f"  Pending: {queue_stats[1]:,}")


def main():
    parser = argparse.ArgumentParser(
        description='Epstein News Article Collection - Recreates the 9,700 article ingestion'
    )
    
    parser.add_argument('--full', action='store_true',
                       help='Run full collection (2000-2025, ~9,700 articles, ~24 hours)')
    parser.add_argument('--test', action='store_true',
                       help='Run test collection (2024 only, ~100 articles, ~30 min)')
    parser.add_argument('--stats', action='store_true',
                       help='Show current collection statistics')
    parser.add_argument('--start', type=int, default=2000,
                       help='Start year (for custom range)')
    parser.add_argument('--end', type=int, default=2025,
                       help='End year (for custom range)')
    parser.add_argument('--max-stages', type=int, default=30,
                       help='Max concurrent stages (default 30)')
    
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
    elif args.full:
        run_full_collection()
    elif args.test:
        run_test_collection()
    else:
        # Default: custom or show help
        if args.start != 2000 or args.end != 2025:
            run_custom_collection(args.start, args.end, args.max_stages)
        else:
            parser.print_help()
            print("\nExamples:")
            print("  python collect_epstein_articles.py --test")
            print("  python collect_epstein_articles.py --full")
            print("  python collect_epstein_articles.py --start 2019 --end 2021")
            print("  python collect_epstein_articles.py --stats")


if __name__ == '__main__':
    main()
