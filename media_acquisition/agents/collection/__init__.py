"""Collection Agents

Agents for collecting and downloading media content.
"""

from media_acquisition.agents.collection.video import VideoTranscriber
from media_acquisition.agents.collection.news import NewsCollector

__all__ = ['VideoTranscriber', 'NewsCollector']
