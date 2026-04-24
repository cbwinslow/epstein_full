#!/usr/bin/env python3
"""
Monitor enrichment progress and alert when complete.
Runs continuously and logs stats every 5 minutes.
"""

import time
import psycopg2
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URL = 'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'

def get_stats():
    """Get current enrichment stats."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN word_count > 100 THEN 1 END) as enriched,
            COUNT(CASE WHEN word_count IS NULL OR word_count < 100 THEN 1 END) as pending,
            AVG(word_count) as avg_words,
            MAX(word_count) as max_words
        FROM media_news_articles
    """)
    
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    return {
        'total': row[0],
        'enriched': row[1],
        'pending': row[2],
        'avg_words': round(row[3] or 0, 1),
        'max_words': row[4] or 0
    }

def main():
    logger.info("="*60)
    logger.info("ENRICHMENT MONITOR STARTED")
    logger.info("="*60)
    
    last_enriched = 0
    stall_count = 0
    
    while True:
        stats = get_stats()
        
        # Calculate progress
        progress = (stats['enriched'] / stats['total']) * 100 if stats['total'] > 0 else 0
        
        logger.info(f"Progress: {stats['enriched']}/{stats['total']} ({progress:.1f}%) | "
                   f"Pending: {stats['pending']} | Avg words: {stats['avg_words']}")
        
        # Check if stalled (no progress for 3 cycles = 15 min)
        if stats['enriched'] == last_enriched:
            stall_count += 1
            if stall_count >= 3:
                logger.warning(f"ENRICHMENT STALLED - No progress for {stall_count * 5} minutes")
                if stall_count >= 6:
                    logger.info("ENRICHMENT APPEARS COMPLETE (no progress for 30 min)")
                    break
        else:
            stall_count = 0
            last_enriched = stats['enriched']
        
        # Check if complete
        if stats['pending'] == 0:
            logger.info("="*60)
            logger.info("ENRICHMENT COMPLETE!")
            logger.info(f"Total articles: {stats['total']}")
            logger.info(f"Successfully enriched: {stats['enriched']}")
            logger.info(f"Average word count: {stats['avg_words']}")
            logger.info("="*60)
            break
        
        time.sleep(300)  # 5 minutes

if __name__ == '__main__':
    main()
