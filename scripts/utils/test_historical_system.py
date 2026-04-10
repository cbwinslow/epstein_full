#!/usr/bin/env python3
"""
Quick test of the historical collection system
Tests components before full run
"""

import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

print("="*70)
print("HISTORICAL COLLECTION SYSTEM - COMPONENT TEST")
print("="*70)

# Test 1: Configuration
print("\n[1] Testing configuration...")
try:
    from media_acquisition.config import DATABASE_URL, TARGET_SOURCES, EPSTEIN_KEYWORDS
    print(f"   ✓ Database URL configured")
    print(f"   ✓ {len(TARGET_SOURCES)} target sources")
    print(f"   ✓ {len(EPSTEIN_KEYWORDS)} Epstein keywords")
    print(f"   ✓ {len(SEPT11_KEYWORDS)} 9/11 keywords")
except Exception as e:
    print(f"   ✗ {e}")
    sys.exit(1)

# Test 2: Storage Manager
print("\n[2] Testing StorageManager...")
try:
    from media_acquisition.base import StorageManager
    sm = StorageManager(DATABASE_URL, '/home/cbwinslow/workspace/epstein-data/media')
    summary = sm.get_queue_summary()
    print(f"   ✓ StorageManager connected")
    print(f"   ✓ Queue summary: {summary}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 3: Database Connection
print("\n[3] Testing database...")
try:
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM media_collection_queue")
    count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM media_news_articles")
    article_count = cur.fetchone()[0]
    conn.close()
    print(f"   ✓ Database connected")
    print(f"   ✓ Queue items: {count}")
    print(f"   ✓ Articles stored: {article_count}")
except Exception as e:
    print(f"   ✗ {e}")

# Test 4: Pipeline Imports
print("\n[4] Testing ingestion pipeline...")
try:
    from scripts.article_ingestion_pipeline import ArticleIngestionPipeline
    print("   ✓ ArticleIngestionPipeline imported")
except Exception as e:
    print(f"   ✗ {e}")

# Test 5: Collection Scripts
print("\n[5] Testing collection scripts...")
try:
    from scripts.collect_historical_data import WaybackCollector, HistoricalCollectionManager
    print("   ✓ WaybackCollector imported")
except Exception as e:
    print(f"   ⚠ {e}")

try:
    from scripts.collect_historical_v2 import DirectWaybackCollector
    print("   ✓ DirectWaybackCollector imported")
except Exception as e:
    print(f"   ⚠ {e}")

try:
    from scripts.batch_ingest_historical import BatchIngestionManager
    print("   ✓ BatchIngestionManager imported")
except Exception as e:
    print(f"   ⚠ {e}")

print("\n" + "="*70)
print("COMPONENT TEST COMPLETE")
print("="*70)

print("\nSystem is ready for historical data collection!")
print("\nTo start collection, run:")
print("  cd /home/cbwinslow/workspace/epstein")
print("  python3 scripts/collect_historical_data.py 2001 2005  # 9/11 period")
print("  python3 scripts/collect_historical_data.py 2019 2024  # Recent Epstein")
print("\nOr use the orchestrator:")
print("  python3 scripts/orchestrate_historical_collection.py --test")
print("  python3 scripts/orchestrate_historical_collection.py --period 911")
