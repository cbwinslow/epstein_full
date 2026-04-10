#!/bin/bash
# Media Acquisition System - Quick Start Script
# Usage: ./scripts/start_media_acquisition.sh

set -e

echo "=========================================="
echo "Epstein Media Acquisition System"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check Python
echo "Checking environment..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi
print_status "Python 3 found"

# Check PostgreSQL
echo ""
echo "Checking database connection..."
if ! python3 -c "import psycopg2" 2>/dev/null; then
    print_warning "psycopg2 not installed, installing..."
    pip install psycopg2-binary
fi

# Test database connection
if python3 -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    conn.close()
    print('Database connection OK')
except Exception as e:
    print(f'Database error: {e}')
    exit(1)
" 2>/dev/null; then
    print_status "Database connection OK"
else
    print_error "Cannot connect to database"
    exit 1
fi

# Run migrations
echo ""
echo "Checking database schema..."
cd /home/cbwinslow/workspace/epstein
if python3 scripts/apply_migrations.py --verify 2>/dev/null | grep -q "All.*tables present"; then
    print_status "Database schema OK"
else
    print_warning "Schema needs update, running migrations..."
    python3 scripts/apply_migrations.py
fi

# Create media directories
echo ""
echo "Setting up media directories..."
mkdir -p /home/cbwinslow/workspace/epstein-data/media/{news,videos,documents,archive}
print_status "Media directories ready"

# Check for API keys
echo ""
echo "Checking API configuration..."
if [ -f .env ]; then
    source .env
fi

if [ -z "$YOUTUBE_API_KEY" ]; then
    print_warning "YOUTUBE_API_KEY not set - video discovery will be limited"
fi

if [ -z "$NEWSAPI_KEY" ]; then
    print_warning "NEWSAPI_KEY not set - using GDELT for news discovery"
fi

# Display options
echo ""
echo "=========================================="
echo "Ready! Choose an option:"
echo "=========================================="
echo ""
echo "1. Run full media acquisition (discovery + collection)"
echo "2. Run news discovery only"
echo "3. Run article collection from queue"
echo "4. Run video discovery"
echo "5. Run document discovery"
echo "6. Ingest specific URL with rich metadata"
echo "7. Check system status"
echo "8. Run tests"
echo "9. Exit"
echo ""
read -p "Enter choice [1-9]: " choice

case $choice in
    1)
        echo ""
        echo "Starting full media acquisition..."
        python3 scripts/run_media_acquisition.py
        ;;
    2)
        echo ""
        echo "Starting news discovery..."
        python3 -c "
import asyncio
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from scripts.run_media_acquisition import MediaAcquisitionRunner
runner = MediaAcquisitionRunner()
async def main():
    await runner.initialize()
    await runner.discover_news(max_results=50)
asyncio.run(main())
"
        ;;
    3)
        echo ""
        echo "Collecting articles from queue..."
        python3 -c "
import asyncio
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from scripts.run_media_acquisition import MediaAcquisitionRunner
runner = MediaAcquisitionRunner()
async def main():
    await runner.initialize()
    await runner.collect_news(batch_size=20)
asyncio.run(main())
"
        ;;
    4)
        echo ""
        echo "Starting video discovery..."
        python3 -c "
import asyncio
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from scripts.run_media_acquisition import MediaAcquisitionRunner
runner = MediaAcquisitionRunner()
async def main():
    await runner.initialize()
    await runner.discover_videos(max_results=20)
asyncio.run(main())
"
        ;;
    5)
        echo ""
        echo "Starting document discovery..."
        python3 -c "
import asyncio
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from scripts.run_media_acquisition import MediaAcquisitionRunner
runner = MediaAcquisitionRunner()
async def main():
    await runner.initialize()
    await runner.discover_documents(max_results=20)
asyncio.run(main())
"
        ;;
    6)
        echo ""
        read -p "Enter URL to ingest: " url
        read -p "Enter keywords (comma-separated): " keywords
        echo "Ingesting with rich metadata extraction..."
        python3 -c "
import asyncio
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from scripts.article_ingestion_pipeline import ArticleIngestionPipeline

async def main():
    pipeline = ArticleIngestionPipeline('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    keywords = [k.strip() for k in '$keywords'.split(',')]
    article_id = await pipeline.ingest_article('$url', keywords)
    if article_id:
        print(f'✓ Article ingested: ID {article_id}')
    else:
        print('✗ Failed to ingest article')

asyncio.run(main())
"
        ;;
    7)
        echo ""
        echo "Checking system status..."
        python3 scripts/check_status.py
        ;;
    8)
        echo ""
        echo "Running tests..."
        python3 scripts/run_tests.py unit
        ;;
    9)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Done!"
echo "=========================================="
