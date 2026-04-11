#!/bin/bash
# Run full enrichment on all articles
# Processes 50 articles per batch, continuously

LOG_FILE="/tmp/enrichment_$(date +%Y%m%d_%H%M%S).log"
BATCH_SIZE=50
TOTAL_ARTICLES=9279
BATCHES=$((TOTAL_ARTICLES / BATCH_SIZE + 1))

echo "=========================================="
echo "FULL ENRICHMENT RUN"
echo "=========================================="
echo "Total articles to process: $TOTAL_ARTICLES"
echo "Batch size: $BATCH_SIZE"
echo "Estimated batches: $BATCHES"
echo "Log file: $LOG_FILE"
echo "=========================================="
echo ""

cd /home/cbwinslow/workspace/epstein

for i in $(seq 1 $BATCHES); do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Batch $i/$BATCHES"
    
    # Run enrichment
    python3 scripts/ingestion/enrich_with_trafilatura.py >> "$LOG_FILE" 2>&1
    
    # Check stats every 10 batches
    if [ $((i % 10)) -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stats check:"
        psql -d epstein -c "SELECT COUNT(CASE WHEN word_count > 100 THEN 1 END) as with_content, COUNT(*) as total FROM media_news_articles"
    fi
    
    # Small delay between batches
    sleep 2
done

echo ""
echo "=========================================="
echo "ENRICHMENT COMPLETE"
echo "=========================================="

# Final stats
echo "Final statistics:"
psql -d epstein -c "SELECT COUNT(CASE WHEN word_count > 100 THEN 1 END) as with_content, COUNT(*) as total FROM media_news_articles"
