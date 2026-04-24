#!/usr/bin/env python3
"""
Collect Epstein-related news articles using GDELT Web News NGrams 3.0
Reconstructs full-text articles from n-grams - FREE and open for research
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from multiprocessing import freeze_support
import psycopg2
from psycopg2.extras import execute_values

# GDELT imports
from gdeltnews.download import download
from gdeltnews.reconstruct import reconstruct
from gdeltnews.filtermerge import filtermerge

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
DB_URL = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'
DATA_DIR = Path('/home/cbwinslow/workspace/epstein-data/gdelt')
GDELT_RAW = DATA_DIR / 'raw'
GDELT_RECONSTRUCTED = DATA_DIR / 'reconstructed'
GDELT_FINAL = DATA_DIR / 'final'

# Epstein search query (GDELT boolean syntax)
EPSTEIN_QUERY = '(Jeffrey Epstein OR Epstein OR "Ghislaine Maxwell" OR "Virginia Giuffre" OR "Jean-Luc Brunel" OR "Les Wexner" OR "Prince Andrew" OR "Bill Clinton" AND Epstein)'

# Date ranges for collection (ISO 8601 with time)
DATE_RANGES = [
    # Pre-arrest (background)
    ("2000-01-01T00:00:00", "2005-12-31T23:59:59"),
    # First case (2006-2008)
    ("2006-01-01T00:00:00", "2008-12-31T23:59:59"),
    # Between cases (2009-2018)
    ("2009-01-01T00:00:00", "2018-12-31T23:59:59"),
    # 2019 arrest and death
    ("2019-01-01T00:00:00", "2019-12-31T23:59:59"),
    # 2020-2021 (Maxwell trial)
    ("2020-01-01T00:00:00", "2021-12-31T23:59:59"),
    # 2022-2023 (Document releases)
    ("2022-01-01T00:00:00", "2023-12-31T23:59:59"),
    # 2024-2025 (Recent)
    ("2024-01-01T00:00:00", "2025-12-31T23:59:59"),
]

def setup_dirs():
    """Create data directories."""
    for d in [GDELT_RAW, GDELT_RECONSTRUCTED, GDELT_FINAL]:
        d.mkdir(parents=True, exist_ok=True)
    logger.info(f"Data directories ready: {DATA_DIR}")

def download_gdelt_range(start_date: str, end_date: str) -> bool:
    """Download GDELT n-grams for date range."""
    outdir = GDELT_RAW / f"{start_date}_{end_date}"
    outdir.mkdir(exist_ok=True)
    
    try:
        logger.info(f"Downloading GDELT: {start_date} to {end_date}")
        download(
            start_date,
            end_date,
            outdir=str(outdir),
            decompress=True,
            show_progress=True
        )
        logger.info(f"Download complete: {outdir}")
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False

def reconstruct_articles(input_dir: str, output_dir: str) -> bool:
    """Reconstruct full articles from n-grams."""
    try:
        logger.info(f"Reconstructing articles from {input_dir}")
        reconstruct(
            input_dir=input_dir,
            output_dir=output_dir,
            language="en",
            processes=8,  # Use 8 cores
            verbose=True
        )
        logger.info(f"Reconstruction complete: {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Reconstruction failed: {e}")
        return False

def filter_epstein_articles(input_dir: str, output_file: str) -> bool:
    """Filter for Epstein-related content."""
    try:
        logger.info(f"Filtering for Epstein content")
        filtermerge(
            input_dir=input_dir,
            output_file=output_file,
            query=EPSTEIN_QUERY,
            verbose=True
        )
        logger.info(f"Filtering complete: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Filtering failed: {e}")
        return False

def import_to_postgresql(csv_file: str) -> int:
    """Import articles to PostgreSQL."""
    import pandas as pd
    
    try:
        logger.info(f"Importing {csv_file} to PostgreSQL")
        df = pd.read_csv(csv_file)
        
        if len(df) == 0:
            logger.warning("No articles to import")
            return 0
        
        # Connect to database
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Prepare data for insertion
        articles = []
        for _, row in df.iterrows():
            articles.append({
                'url': row.get('url', ''),
                'title': row.get('title', '')[:500],
                'content': row.get('text', row.get('content', '')),
                'publish_date': row.get('date', row.get('publish_date', None)),
                'source_domain': row.get('domain', row.get('source', '')),
                'language': row.get('lang', 'en'),
                'word_count': len(str(row.get('text', '')).split()) if row.get('text') else 0,
                'all_topics': json.dumps({
                    'extraction_method': 'gdelt_reconstruction',
                    'gdelt_date_range': f"{row.get('start_date', '')} to {row.get('end_date', '')}",
                    'fingerprint': row.get('fingerprint', '')
                }),
                'collected_at': datetime.now()
            })
        
        # Insert with conflict handling
        inserted = 0
        for article in articles:
            try:
                cur.execute("""
                    INSERT INTO media_news_articles 
                    (article_url, title, content, publish_date, source_domain, 
                     language, word_count, all_topics, collected_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (article_url) DO UPDATE SET
                        content = EXCLUDED.content,
                        word_count = EXCLUDED.word_count,
                        all_topics = EXCLUDED.all_topics,
                        collected_at = EXCLUDED.collected_at
                    WHERE EXCLUDED.word_count > media_news_articles.word_count
                """, (
                    article['url'], article['title'], article['content'],
                    article['publish_date'], article['source_domain'],
                    article['language'], article['word_count'], 
                    article['all_topics'], article['collected_at']
                ))
                inserted += 1
            except Exception as e:
                logger.warning(f"Insert failed for {article['url']}: {e}")
                continue
        
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"Imported {inserted}/{len(articles)} articles")
        return inserted
        
    except Exception as e:
        logger.error(f"Import failed: {e}")
        return 0

def process_date_range(start_date: str, end_date: str) -> int:
    """Process a single date range: download -> reconstruct -> filter -> import."""
    range_name = f"{start_date}_{end_date}"
    
    # 1. Download
    raw_dir = GDELT_RAW / range_name
    if not download_gdelt_range(start_date, end_date):
        return 0
    
    # 2. Reconstruct
    recon_dir = GDELT_RECONSTRUCTED / range_name
    if not reconstruct_articles(str(raw_dir), str(recon_dir)):
        return 0
    
    # 3. Filter for Epstein content
    final_csv = GDELT_FINAL / f"epstein_{range_name}.csv"
    if not filter_epstein_articles(str(recon_dir), str(final_csv)):
        return 0
    
    # 4. Import to PostgreSQL
    return import_to_postgresql(str(final_csv))

def run_full_collection():
    """Run collection for all date ranges."""
    setup_dirs()
    
    total_articles = 0
    for start, end in DATE_RANGES:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {start} to {end}")
        logger.info(f"{'='*60}")
        
        count = process_date_range(start, end)
        total_articles += count
        
        logger.info(f"Range complete: {count} articles")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"COLLECTION COMPLETE: {total_articles} total articles")
    logger.info(f"{'='*60}")

def run_test_collection():
    """Test with a small 1-month range."""
    setup_dirs()
    
    # Test: July 2019 (arrest month) - ISO 8601 timestamps
    logger.info("\n" + "="*60)
    logger.info("TEST COLLECTION: July 2019 (arrest month)")
    logger.info("="*60)
    
    count = process_date_range("2019-07-01T00:00:00", "2019-07-31T23:59:59")
    logger.info(f"Test complete: {count} articles")
    
    return count

def main():
    """Main entry point."""
    freeze_support()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_test_collection()
    else:
        run_full_collection()

if __name__ == '__main__':
    main()
