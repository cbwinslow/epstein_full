#!/bin/bash
# Quick start script for historical data collection

echo "=========================================="
echo "HISTORICAL DATA COLLECTION - QUICK START"
echo "=========================================="
echo ""

# Check Python
echo "[1] Checking Python environment..."
cd /home/cbwinslow/workspace/epstein
python3 --version

# Check database
echo ""
echo "[2] Checking database connection..."
python3 -c "
from media_acquisition.config import DATABASE_URL
import psycopg2
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM media_collection_queue')
print(f'Queue items: {cur.fetchone()[0]}')
cur.execute('SELECT COUNT(*) FROM media_news_articles')
print(f'Articles: {cur.fetchone()[0]}')
conn.close()
print('✓ Database connected')
"

# Show options
echo ""
echo "[3] Collection Options:"
echo ""
echo "A) Collect Epstein articles (2020-2024):"
echo "   python3 scripts/collect_news_sources.py epstein 2020 2024"
echo ""
echo "B) Collect 9/11 articles (2001-2005):"
echo "   python3 scripts/collect_news_sources.py sept11 2001 2005"
echo ""
echo "C) Run full orchestration (all periods):"
echo "   python3 scripts/orchestrate_historical_collection.py"
echo ""
echo "D) Test with single URL:"
echo "   python3 scripts/article_ingestion_pipeline.py"
echo ""

# Check if URLs were already collected
echo "[4] Checking for existing URL collections..."
ls -lh /home/cbwinslow/workspace/epstein-data/urls/*.json 2>/dev/null || echo "No URL files found yet"

echo ""
echo "Ready to start collection!"
echo "=========================================="
