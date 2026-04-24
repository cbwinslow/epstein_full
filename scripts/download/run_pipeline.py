#!/usr/bin/env python3
"""
News Ingestion Pipeline Orchestrator

Runs the complete 3-phase workflow:
  Phase 1: Discovery - Find article URLs from RSS feeds
  Phase 2: (Storage handled automatically)
  Phase 3: Extraction - Fetch full content with Trafilatura

Usage:
  # Full pipeline test (small sample)
  python run_pipeline.py --mode test --keywords "Jeffrey Epstein"
  
  # Production run (all phases)
  python run_pipeline.py --mode production --start-date 2024-01-01 --end-date 2025-12-31
  
  # Run specific phase
  python run_pipeline.py --phase discovery --keywords "Epstein"
  python run_pipeline.py --phase extraction --limit 50

Workflow:
  ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
  │  Phase 1        │────▶│  Phase 2         │────▶│  Phase 3        │
  │  Discovery      │     │  Storage         │     │  Extraction     │
  │  (RSS/News)     │     │  (Queue)         │     │  (Trafilatura)  │
  └─────────────────┘     └──────────────────┘     └─────────────────┘
       ↓                                                    ↓
  article_discovery_queue                           media_news_articles
"""

import argparse
import asyncio
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')


def run_phase1_discovery(keywords, start_date, end_date):
    """Run Phase 1: URL Discovery."""
    print("="*80)
    print("PHASE 1: URL DISCOVERY")
    print("="*80)
    
    from scripts.ingestion.phase1_discovery import RSSDiscoveryAgent, save_to_discovery_queue
    
    agent = RSSDiscoveryAgent(keywords, start_date, end_date)
    
    # Run async discovery
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    discovered = loop.run_until_complete(agent.discover_all())
    loop.close()
    
    if discovered:
        saved = save_to_discovery_queue(discovered)
        print(f"\n✓ Phase 1 complete: {saved} URLs queued for extraction")
        return saved
    else:
        print("\n⚠ No URLs discovered")
        return 0


def run_phase3_extraction(test_mode=False, limit=10, batch_size=100, rate_limit=2.0):
    """Run Phase 3: Content Extraction."""
    print("\n" + "="*80)
    print("PHASE 3: CONTENT EXTRACTION")
    print("="*80)
    
    from scripts.ingestion.phase3_extraction import run_test_sample, run_bulk_extraction
    
    if test_mode:
        run_test_sample(limit)
    else:
        run_bulk_extraction(batch_size, rate_limit)


def run_full_pipeline(args):
    """Run complete pipeline."""
    print("\n" + "="*80)
    print("NEWS INGESTION PIPELINE - FULL WORKFLOW")
    print("="*80)
    print(f"Keywords: {args.keywords}")
    print(f"Date range: {args.start_date} to {args.end_date}")
    print(f"Mode: {'TEST' if args.test else 'PRODUCTION'}")
    print("="*80)
    
    # Phase 1: Discovery
    discovered_count = run_phase1_discovery(
        args.keywords,
        args.start_date,
        args.end_date
    )
    
    if discovered_count == 0:
        print("\n✗ Pipeline stopped: No URLs to process")
        return
    
    # Phase 3: Extraction
    print("\n" + "-"*80)
    print("Moving to Phase 3...")
    print("-"*80)
    
    run_phase3_extraction(
        test_mode=args.test,
        limit=args.limit if args.test else 10,
        batch_size=args.batch_size,
        rate_limit=args.rate_limit
    )
    
    print("\n" + "="*80)
    print("PIPELINE COMPLETE")
    print("="*80)


def check_prerequisites():
    """Check that required tools are installed."""
    import subprocess
    
    print("Checking prerequisites...")
    
    # Check trafilatura
    try:
        import trafilatura
        print("  ✓ trafilatura installed")
    except ImportError:
        print("  ✗ trafilatura not installed")
        print("  Install with: pip install trafilatura")
        return False
    
    # Check database connection
    try:
        import psycopg2
        conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
        conn.close()
        print("  ✓ Database connection OK")
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        return False
    
    print("  ✓ All prerequisites met\n")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='News Ingestion Pipeline - 3-Phase Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test run (small sample, recommended first)
  python run_pipeline.py --mode test --keywords "Jeffrey Epstein"
  
  # Production run
  python run_pipeline.py --mode production \\
    --start-date 2024-01-01 --end-date 2025-12-31 \\
    --keywords "Epstein" "Ghislaine Maxwell"
  
  # Run just discovery
  python run_pipeline.py --phase discovery --keywords "Epstein case"
  
  # Run just extraction (on pending URLs)
  python run_pipeline.py --phase extraction --test --limit 20
        """
    )
    
    parser.add_argument('--mode', choices=['test', 'production'], default='test',
                       help='Test mode (small sample) or production (full run)')
    parser.add_argument('--phase', choices=['discovery', 'extraction', 'all'], default='all',
                       help='Which phase to run')
    parser.add_argument('--keywords', nargs='+', 
                       default=['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell'],
                       help='Keywords to search for')
    parser.add_argument('--start-date', type=lambda s: __import__('datetime').datetime.strptime(s, '%Y-%m-%d').date(),
                       default=date(2024, 1, 1), help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=lambda s: __import__('datetime').datetime.strptime(s, '%Y-%m-%d').date(),
                       default=date(2025, 12, 31), help='End date (YYYY-MM-DD)')
    parser.add_argument('--limit', type=int, default=10,
                       help='Number of URLs to test (test mode)')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='Batch size for bulk extraction')
    parser.add_argument('--rate-limit', type=float, default=2.0,
                       help='Seconds between requests (be nice to servers)')
    parser.add_argument('--test', action='store_true',
                       help='Shortcut for --mode test')
    
    args = parser.parse_args()
    
    if args.test:
        args.mode = 'test'
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n✗ Prerequisites not met. Please install required packages.")
        sys.exit(1)
    
    # Run requested phases
    if args.phase == 'discovery' or args.phase == 'all':
        discovered = run_phase1_discovery(args.keywords, args.start_date, args.end_date)
        
        if args.phase == 'discovery':
            return  # Stop after discovery
        
        if discovered == 0:
            print("\n✗ No URLs discovered. Stopping pipeline.")
            return
    
    if args.phase == 'extraction' or args.phase == 'all':
        run_phase3_extraction(
            test_mode=(args.mode == 'test'),
            limit=args.limit,
            batch_size=args.batch_size,
            rate_limit=args.rate_limit
        )
    
    print("\n" + "="*80)
    print("WORKFLOW COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("  1. Review extracted articles in database")
    print("  2. Run: python scripts/processing/review_dataset.py")
    print("  3. Prepare for Hugging Face: python scripts/processing/prepare_huggingface_dataset.py")


if __name__ == '__main__':
    main()
