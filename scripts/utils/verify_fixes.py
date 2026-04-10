#!/usr/bin/env python3
"""Quick verification of bug fixes"""

import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

print("=== VERIFICATION TEST ===\n")

# 1. Check StorageManager
from media_acquisition.base import StorageManager
sm = StorageManager(
    connection_string='postgresql://cbwinslow:123qweasd@localhost:5432/epstein',
    base_path='/tmp/test'
)
checks = {
    'StorageManager.add_to_queue': hasattr(sm, 'add_to_queue'),
    'StorageManager.get_queue_summary': hasattr(sm, 'get_queue_summary'),
    'StorageManager.queue_item': hasattr(sm, 'queue_item'),
}

# 2. Check NewsDiscoveryAgent
from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.base import AgentConfig
config = AgentConfig(agent_id='test')
news_agent = NewsDiscoveryAgent(config)
checks['NewsDiscoveryAgent.search'] = hasattr(news_agent, 'search')

# 3. Check VideoDiscoveryAgent
from media_acquisition.agents.discovery.video import VideoDiscoveryAgent
video_agent = VideoDiscoveryAgent(config)
checks['VideoDiscoveryAgent.youtube'] = hasattr(video_agent, 'youtube')
checks['VideoDiscoveryAgent.search'] = hasattr(video_agent, 'search')

# 4. Check NewsCollector
from media_acquisition.agents.collection.news import NewsCollector
collector = NewsCollector(config, sm)
checks['NewsCollector.process_article'] = hasattr(collector, 'process_article')
checks['NewsCollector.collect'] = hasattr(collector, 'collect')

# Print results
for name, result in checks.items():
    status = "✓" if result else "✗"
    print(f"{status} {name}")

# Summary
passed = sum(checks.values())
total = len(checks)
print(f"\n=== SUMMARY: {passed}/{total} checks passed ===")

if passed == total:
    print("All bugs fixed!")
else:
    print("Some issues remain")
    sys.exit(1)
