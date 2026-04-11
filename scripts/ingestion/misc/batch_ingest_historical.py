#!/usr/bin/env python3
"""
Batch Ingestion Pipeline for Historical Articles
Processes URLs discovered by the historical collector
"""

import asyncio
import aiohttp
import json
import logging
import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('batch_ingestion')

# Add parent directory to path
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.config import get_storage_manager, DATABASE_URL, BATCH_CONFIG
from scripts.article_ingestion_pipeline import ArticleIngestionPipeline


class BatchIngestionManager:
    """Manages batch ingestion with resume capability."""
    
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.storage = get_storage_manager()
        self.pipeline: Optional[ArticleIngestionPipeline] = None
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self.pipeline = ArticleIngestionPipeline(self.session)
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def process_url(self, url_data: Dict) -> Optional[Dict]:
        """Process a single URL."""
        try:
            # Use the article ingestion pipeline
            metadata = await self.pipeline.ingest_article(
                url=url_data['url'],
                priority=5,
                keywords_matched=url_data.get('keywords_matched', []),
                discovered_by=url_data.get('source', 'news_collection')
            )
            
            if metadata:
                logger.info(f"✓ Ingested: {url_data['url'][:80]}...")
                return metadata
            else:
                logger.warning(f"✗ Failed: {url_data['url'][:80]}...")
                return None
                
        except Exception as e:
            logger.error(f"✗ Error processing {url_data.get('url', 'unknown')}: {e}")
            return None
    
    async def process_batch(self, urls: List[Dict]) -> Dict:
        """Process a batch of URLs."""
        results = {
            'processed': 0,
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for url_data in urls:
            result = await self.process_url(url_data)
            results['processed'] += 1
            
            if result:
                results['success'] += 1
            else:
                results['failed'] += 1
            
            # Rate limiting
            await asyncio.sleep(0.25)
        
        return results
    
    def load_urls_from_file(self, filepath: str) -> List[Dict]:
        """Load URLs from JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    async def run_ingestion(self, urls_file: str, resume: bool = True):
        """Run full ingestion from URL file."""
        
        # Load URLs
        logger.info(f"Loading URLs from {urls_file}")
        all_urls = self.load_urls_from_file(urls_file)
        logger.info(f"Loaded {len(all_urls)} URLs")
        
        # Check for already processed URLs
        if resume:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("SELECT source_url FROM media_collection_queue WHERE status = 'completed'")
            processed = {row[0] for row in cur.fetchall()}
            conn.close()
            
            # Filter out already processed
            all_urls = [u for u in all_urls if u.get('url') not in processed]
            logger.info(f"Filtered to {len(all_urls)} unprocessed URLs")
        
        # Process in batches
        total_results = {
            'processed': 0,
            'success': 0,
            'failed': 0
        }
        
        for i in range(0, len(all_urls), self.batch_size):
            batch = all_urls[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            total_batches = (len(all_urls) + self.batch_size - 1) // self.batch_size
            
            logger.info(f"\n--- Batch {batch_num}/{total_batches} ({len(batch)} URLs) ---")
            
            results = await self.process_batch(batch)
            
            total_results['processed'] += results['processed']
            total_results['success'] += results['success']
            total_results['failed'] += results['failed']
            
            # Save progress
            progress = {
                'timestamp': datetime.now().isoformat(),
                'batch': batch_num,
                'total_batches': total_batches,
                'batch_results': results,
                'cumulative': total_results
            }
            
            progress_file = urls_file.replace('.json', '_progress.json')
            with open(progress_file, 'w') as f:
                json.dump(progress, f, indent=2)
            
            logger.info(f"Batch complete: {results['success']}/{results['processed']} succeeded")
            logger.info(f"Cumulative: {total_results['success']}/{total_results['processed']}")
        
        return total_results


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch ingest historical articles')
    parser.add_argument('urls_file', help='JSON file containing URLs to ingest')
    parser.add_argument('--batch-size', type=int, default=100, help='Batch size')
    parser.add_argument('--no-resume', action='store_true', help='Skip resume check')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.urls_file):
        print(f"Error: File not found: {args.urls_file}")
        sys.exit(1)
    
    async with BatchIngestionManager(batch_size=args.batch_size) as manager:
        results = await manager.run_ingestion(
            urls_file=args.urls_file,
            resume=not args.no_resume
        )
    
    print("\n" + "="*60)
    print("INGESTION COMPLETE")
    print("="*60)
    print(f"Total processed: {results['processed']}")
    print(f"Successful: {results['success']}")
    print(f"Failed: {results['failed']}")
    print(f"Success rate: {results['success']/results['processed']*100:.1f}%" if results['processed'] > 0 else "N/A")


if __name__ == '__main__':
    asyncio.run(main())
