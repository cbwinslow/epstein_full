#!/usr/bin/env python3
"""
PARALLEL Epstein article collection using GDELT Web News NGrams 3.0
Multi-worker pipeline for maximum speed
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from multiprocessing import freeze_support
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Tuple, Dict
import threading
import queue

import psycopg2
from psycopg2.extras import execute_values

# GDELT imports
from gdeltnews.download import download
from gdeltnews.reconstruct import reconstruct
from gdeltnews.filtermerge import filtermerge

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DB_URL = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'
DATA_DIR = Path('/home/cbwinslow/workspace/epstein-data/gdelt')
GDELT_RAW = DATA_DIR / 'raw'
GDELT_RECONSTRUCTED = DATA_DIR / 'reconstructed'
GDELT_FINAL = DATA_DIR / 'final'

# Epstein search query
EPSTEIN_QUERY = '(Jeffrey Epstein OR Epstein OR "Ghislaine Maxwell" OR "Virginia Giuffre")'

# Maximum parallel workers (adjust based on CPU cores and network)
MAX_WORKERS = 8

# Progress tracking
progress_lock = threading.Lock()
total_chunks = 0
completed_chunks = 0


def setup_dirs():
    """Create data directories."""
    for d in [GDELT_RAW, GDELT_RECONSTRUCTED, GDELT_FINAL]:
        d.mkdir(parents=True, exist_ok=True)


def generate_weekly_chunks(start_date: str, end_date: str) -> List[Tuple[str, str]]:
    """Break date range into weekly chunks for parallel processing."""
    chunks = []
    current = datetime.fromisoformat(start_date.replace('Z', '+00:00').replace('+00:00', ''))
    end = datetime.fromisoformat(end_date.replace('Z', '+00:00').replace('+00:00', ''))
    
    while current < end:
        week_end = min(current + timedelta(days=7), end)
        chunks.append((
            current.strftime('%Y-%m-%dT%H:%M:%S'),
            week_end.strftime('%Y-%m-%dT%H:%M:%S')
        ))
        current = week_end
    
    return chunks


def process_chunk(chunk_id: str, start: str, end: str) -> Dict:
    """
    Process a single time chunk: download -> reconstruct -> filter
    This runs in a separate worker process.
    """
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(f"Worker-{chunk_id}")
    
    result = {
        'chunk_id': chunk_id,
        'start': start,
        'end': end,
        'downloaded': 0,
        'reconstructed': 0,
        'filtered': 0,
        'articles': [],
        'error': None
    }
    
    try:
        # Setup paths
        raw_dir = GDELT_RAW / chunk_id
        recon_dir = GDELT_RECONSTRUCTED / chunk_id
        final_csv = GDELT_FINAL / f"epstein_{chunk_id}.csv"
        
        raw_dir.mkdir(exist_ok=True)
        recon_dir.mkdir(exist_ok=True)
        
        # 1. DOWNLOAD
        logger.info(f"[{chunk_id}] Downloading {start} to {end}")
        stats = download(start, end, outdir=str(raw_dir), decompress=True, show_progress=False)
        result['downloaded'] = stats.files_downloaded if hasattr(stats, 'files_downloaded') else 0
        
        # 2. RECONSTRUCT
        logger.info(f"[{chunk_id}] Reconstructing articles")
        reconstruct(
            input_dir=str(raw_dir),
            output_dir=str(recon_dir),
            language="en",
            processes=2,  # Each worker uses 2 sub-processes
            verbose=False
        )
        
        # Count reconstructed files
        recon_files = list(recon_dir.glob("*.csv"))
        result['reconstructed'] = len(recon_files)
        
        # 3. FILTER for Epstein content
        if recon_files:
            logger.info(f"[{chunk_id}] Filtering for Epstein content")
            try:
                filtermerge(
                    input_dir=str(recon_dir),
                    output_file=str(final_csv),
                    query=EPSTEIN_QUERY,
                    verbose=False
                )
                
                # Count results
                if final_csv.exists():
                    import pandas as pd
                    df = pd.read_csv(final_csv)
                    result['filtered'] = len(df)
                    result['articles'] = df.to_dict('records')
                    logger.info(f"[{chunk_id}] Found {len(df)} Epstein articles")
            except Exception as e:
                logger.warning(f"[{chunk_id}] Filter failed (may be no matches): {e}")
        
    except Exception as e:
        logger.error(f"[{chunk_id}] Error: {e}")
        result['error'] = str(e)
    
    return result


def import_articles_to_db(articles: List[Dict]) -> int:
    """Import articles to PostgreSQL with conflict handling."""
    if not articles:
        return 0
    
    inserted = 0
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        for article in articles:
            try:
                url = article.get('url', '')
                if not url or len(url) < 10:
                    continue
                
                content = str(article.get('text', article.get('content', '')))
                word_count = len(content.split()) if content else 0
                
                cur.execute("""
                    INSERT INTO media_news_articles 
                    (article_url, title, content, publish_date, source_domain, 
                     language, word_count, all_topics, collected_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (article_url) DO UPDATE SET
                        content = EXCLUDED.content,
                        word_count = EXCLUDED.word_count,
                        all_topics = EXCLUDED.all_topics,
                        collected_at = EXCLUDED.collected_at
                    WHERE EXCLUDED.word_count > media_news_articles.word_count
                """, (
                    url[:1000],
                    str(article.get('title', ''))[:500],
                    content,
                    article.get('date', article.get('publish_date')),
                    article.get('domain', article.get('source', ''))[:200],
                    article.get('lang', 'en'),
                    word_count,
                    json.dumps({
                        'extraction_method': 'gdelt_reconstruction_parallel',
                        'fingerprint': article.get('fingerprint', '')
                    })
                ))
                inserted += 1
                
            except Exception as e:
                continue
        
        conn.commit()
        cur.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Database import failed: {e}")
    
    return inserted


def run_parallel_collection(chunks: List[Tuple[str, str]], max_workers: int = MAX_WORKERS):
    """
    Run collection in parallel using process pool.
    """
    setup_dirs()
    
    global total_chunks, completed_chunks
    total_chunks = len(chunks)
    completed_chunks = 0
    
    logger.info(f"Starting parallel collection: {total_chunks} chunks, {max_workers} workers")
    
    all_articles = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all chunks
        future_to_chunk = {
            executor.submit(process_chunk, f"chunk_{i}", start, end): (i, start, end)
            for i, (start, end) in enumerate(chunks)
        }
        
        # Process results as they complete
        for future in as_completed(future_to_chunk):
            i, start, end = future_to_chunk[future]
            
            try:
                result = future.result()
                completed_chunks += 1
                
                if result['error']:
                    logger.error(f"Chunk {i} failed: {result['error']}")
                else:
                    logger.info(
                        f"[{completed_chunks}/{total_chunks}] Chunk {i}: "
                        f"{result['downloaded']} files, "
                        f"{result['reconstructed']} recon, "
                        f"{result['filtered']} articles"
                    )
                    
                    # Collect articles for batch import
                    all_articles.extend(result['articles'])
                    
                    # Import in batches of 100
                    if len(all_articles) >= 100:
                        count = import_articles_to_db(all_articles)
                        logger.info(f"Imported {count} articles to database")
                        all_articles = []
                        
            except Exception as e:
                logger.error(f"Chunk {i} exception: {e}")
    
    # Import remaining articles
    if all_articles:
        count = import_articles_to_db(all_articles)
        logger.info(f"Imported final {count} articles")
    
    logger.info(f"\nCollection complete: {completed_chunks}/{total_chunks} chunks processed")


def get_priority_chunks() -> List[Tuple[str, str]]:
    """
    Define high-priority date ranges for Epstein coverage.
    Focus on key events rather than continuous coverage.
    """
    priority_periods = [
        # 2005-2006: Initial investigation
        ("2005-01-01T00:00:00", "2006-12-31T23:59:59"),
        # 2008-2009: First conviction
        ("2008-01-01T00:00:00", "2009-12-31T23:59:59"),
        # 2015: First major civil lawsuits
        ("2015-01-01T00:00:00", "2015-12-31T23:59:59"),
        # 2019: Arrest and death (CRITICAL)
        ("2019-01-01T00:00:00", "2019-12-31T23:59:59"),
        # 2020: Maxwell arrest
        ("2020-01-01T00:00:00", "2020-12-31T23:59:59"),
        # 2021: Maxwell trial
        ("2021-06-01T00:00:00", "2021-12-31T23:59:59"),
        # 2022: Document releases
        ("2022-01-01T00:00:00", "2022-12-31T23:59:59"),
        # 2024-2025: Recent developments
        ("2024-01-01T00:00:00", "2025-03-31T23:59:59"),
    ]
    
    # Break into weekly chunks
    all_chunks = []
    for start, end in priority_periods:
        chunks = generate_weekly_chunks(start, end)
        all_chunks.extend(chunks)
    
    return all_chunks


def main():
    freeze_support()
    
    # Get high-priority chunks
    chunks = get_priority_chunks()
    logger.info(f"Total chunks to process: {len(chunks)}")
    
    # Run parallel collection
    workers = min(MAX_WORKERS, len(chunks))
    run_parallel_collection(chunks, max_workers=workers)


if __name__ == '__main__':
    main()
