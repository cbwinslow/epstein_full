"""Discovery Agents

Agents for discovering media content across various sources.
"""

from media_acquisition.agents.discovery.document import DocumentDiscoveryAgent
from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.agents.discovery.video import VideoDiscoveryAgent

__all__ = ["NewsDiscoveryAgent", "VideoDiscoveryAgent", "DocumentDiscoveryAgent"]
