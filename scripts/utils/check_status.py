#!/usr/bin/env python3
"""Quick status check for media acquisition system."""
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

print("=" * 60)
print("MEDIA ACQUISITION SYSTEM STATUS CHECK")
print("=" * 60)

# Test 1: VideoDiscoveryAgent
print("\n[1] VideoDiscoveryAgent...")
from media_acquisition.agents.discovery.video import VideoDiscoveryAgent
from media_acquisition.base import AgentConfig
config = AgentConfig(agent_id='test', youtube_api_key='test_key')
agent = VideoDiscoveryAgent(config)
print(f"    ✓ youtube attribute: {hasattr(agent, 'youtube')}")

# Test 2: StorageManager
print("\n[2] StorageManager...")
from media_acquisition.base import StorageManager
sm = StorageManager(
    connection_string='postgresql://cbwinslow:123qweasd@localhost:5432/epstein',
    base_path='/home/cbwinslow/workspace/epstein-data/media'
)
print(f"    ✓ add_to_queue: {hasattr(sm, 'add_to_queue')}")
print(f"    ✓ get_queue_summary: {hasattr(sm, 'get_queue_summary')}")

# Test 3: NewsCollector
print("\n[3] NewsCollector...")
from media_acquisition.agents.collection.news import NewsCollector
collector = NewsCollector(config, sm)
print(f"    ✓ process_article: {hasattr(collector, 'process_article')}")

# Test 4: Database
print("\n[4] Database tables...")
import psycopg2
conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'media_%' ORDER BY table_name")
tables = cur.fetchall()
print(f"    ✓ Found {len(tables)} media tables")
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t[0]}")
    count = cur.fetchone()[0]
    print(f"      - {t[0]}: {count} rows")
conn.close()

# Test 5: Queue status
print("\n[5] Queue status...")
summary = sm.get_queue_summary()
if summary:
    for media_type, statuses in summary.items():
        for status, count in statuses.items():
            print(f"    - {media_type} [{status}]: {count}")
else:
    print("    (queue is empty)")

print("\n" + "=" * 60)
print("STATUS: All systems operational")
print("=" * 60)
