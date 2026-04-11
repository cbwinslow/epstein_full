#!/usr/bin/env python3
"""
Master Historical Data Collection Orchestrator
Coordinates Wayback Machine discovery and article ingestion
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import List, Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/historical_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('master_orchestrator')

# Add paths
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.config import (
    TARGET_SOURCES, EPSTEIN_KEYWORDS, SEPT11_KEYWORDS,
    HISTORICAL_RANGES, DATABASE_URL
)


class HistoricalOrchestrator:
    """Orchestrates historical data collection."""
    
    def __init__(self):
        self.data_dir = '/home/cbwinslow/workspace/epstein-data'
        os.makedirs(f"{self.data_dir}/urls", exist_ok=True)
        os.makedirs(f"{self.data_dir}/logs", exist_ok=True)
        
    def discover_urls(self, year_start: int, year_end: int, test_mode: bool = False) -> str:
        """Run URL discovery for a date range."""
        
        output_file = f"{self.data_dir}/urls/discovered_{year_start}_{year_end}.json"
        
        # Build command
        cmd = [
            sys.executable,
            'scripts/collect_historical_data.py',
            str(year_start),
            str(year_end)
        ]
        
        if test_mode:
            # Use smaller subset for testing
            cmd.extend(['--test', '--limit', '10'])
        
        logger.info(f"Starting URL discovery: {year_start}-{year_end}")
        logger.info(f"Output: {output_file}")
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='/home/cbwinslow/workspace/epstein')
        
        if result.returncode == 0:
            logger.info("URL discovery complete")
            if os.path.exists(output_file):
                with open(output_file) as f:
                    urls = json.load(f)
                logger.info(f"Discovered {len(urls)} URLs")
                return output_file
        else:
            logger.error(f"Discovery failed: {result.stderr}")
            return None
    
    def ingest_urls(self, urls_file: str, batch_size: int = 50) -> Dict:
        """Ingest URLs from file."""
        
        logger.info(f"Starting ingestion from {urls_file}")
        
        cmd = [
            sys.executable,
            'scripts/batch_ingest_historical.py',
            urls_file,
            '--batch-size', str(batch_size)
        ]
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='/home/cbwinslow/workspace/epstein')
        
        if result.returncode == 0:
            logger.info("Ingestion batch complete")
            return {'status': 'success', 'output': result.stdout}
        else:
            logger.error(f"Ingestion failed: {result.stderr}")
            return {'status': 'error', 'error': result.stderr}
    
    def run_collection_cycle(self, year_start: int, year_end: int, test_mode: bool = False):
        """Run a full collect + ingest cycle for a date range."""
        
        logger.info("="*60)
        logger.info(f"COLLECTION CYCLE: {year_start}-{year_end}")
        logger.info("="*60)
        
        # Step 1: Discover URLs
        urls_file = self.discover_urls(year_start, year_end, test_mode)
        
        if not urls_file:
            logger.error("URL discovery failed")
            return False
        
        # Step 2: Ingest URLs
        result = self.ingest_urls(urls_file, batch_size=50 if test_mode else 100)
        
        if result['status'] == 'success':
            logger.info("Collection cycle complete!")
            return True
        else:
            logger.error("Ingestion failed")
            return False
    
    def run_full_collection(self, test_mode: bool = False):
        """Run full historical collection (2001-2026)."""
        
        periods = [
            ('9/11 Period', 2001, 2005),
            ('Mid Period', 2006, 2010),
            ('Late Period', 2011, 2015),
            ('Recent Period', 2016, 2019),
            ('Current Period', 2020, 2026)
        ]
        
        results = {}
        
        for name, start, end in periods:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {name} ({start}-{end})")
            logger.info('='*60)
            
            success = self.run_collection_cycle(start, end, test_mode)
            results[name] = 'success' if success else 'failed'
            
            # Pause between periods
            if not test_mode:
                logger.info("Pausing 30 seconds before next period...")
                import time
                time.sleep(30)
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("COLLECTION SUMMARY")
        logger.info("="*60)
        for name, status in results.items():
            logger.info(f"{name}: {status}")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Historical Data Collection for Epstein/9-11 Research'
    )
    parser.add_argument(
        '--test', action='store_true',
        help='Run in test mode (small batches)'
    )
    parser.add_argument(
        '--start-year', type=int, default=2001,
        help='Start year (default: 2001)'
    )
    parser.add_argument(
        '--end-year', type=int, default=2026,
        help='End year (default: 2026)'
    )
    parser.add_argument(
        '--period', choices=['all', '911', 'mid', 'late', 'recent', 'current'],
        default='all',
        help='Which time period to process'
    )
    
    args = parser.parse_args()
    
    orchestrator = HistoricalOrchestrator()
    
    # Define periods
    periods = {
        '911': (2001, 2005),
        'mid': (2006, 2010),
        'late': (2011, 2015),
        'recent': (2016, 2019),
        'current': (2020, 2026)
    }
    
    if args.period == 'all':
        results = orchestrator.run_full_collection(test_mode=args.test)
    else:
        start, end = periods[args.period]
        orchestrator.run_collection_cycle(start, end, test_mode=args.test)
    
    logger.info("\n✅ Orchestration complete!")


if __name__ == '__main__':
    main()
