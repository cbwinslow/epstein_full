"""Media Acquisition Agents Package

Contains all agent implementations organized by type:
- discovery: Find media content
- collection: Download media content  
- processing: Analyze media content
"""

from media_acquisition.agents.discovery import (
    NewsDiscoveryAgent,
    VideoDiscoveryAgent,
    DocumentDiscoveryAgent
)
from media_acquisition.agents.collection import VideoTranscriber, NewsCollector
from media_acquisition.agents.processing import EntityExtractor

__all__ = [
    'NewsDiscoveryAgent',
    'VideoDiscoveryAgent',
    'DocumentDiscoveryAgent',
    'VideoTranscriber',
    'NewsCollector',
    'EntityExtractor'
]
