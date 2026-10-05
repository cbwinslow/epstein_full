"""Collection Agents

Agents for collecting and downloading media content.
"""

from media_acquisition.agents.collection.news import NewsCollector
from media_acquisition.agents.collection.video import VideoTranscriber

__all__ = ["VideoTranscriber", "NewsCollector"]
