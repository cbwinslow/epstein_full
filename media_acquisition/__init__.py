"""Epstein Media Acquisition System

A comprehensive media acquisition and analysis system for collecting
Epstein-related news articles, videos, documents, and other media.

Components:
- Discovery Agents: Find media across GDELT, Wayback Machine, APIs
- Collection Agents: Download and store media content
- Processing Agents: NLP analysis, entity extraction, transcription
- Storage Manager: PostgreSQL and filesystem storage
- Master Controller: Orchestrates all operations

Usage:
    from media_acquisition import MediaAcquisitionSystem
    
    system = MediaAcquisitionSystem()
    system.run_historical_collection(
        start_date='2024-01-01',
        end_date='2024-12-31',
        media_types=['news', 'video']
    )
"""

__version__ = '1.0.0'
__author__ = 'Epstein Files Analysis Project'

from media_acquisition.base import (
    AgentConfig,
    StorageManager,
    DiscoveryAgent,
    CollectionAgent,
    ProcessingAgent,
    BaseAgent,
    TaskResult,
    MediaURL,
    NewsArticleURL,
    VideoMetadata,
    DocumentMetadata,
    AgentState,
)

from media_acquisition.master import MediaAcquisitionSystem

__all__ = [
    'AgentConfig',
    'StorageManager',
    'DiscoveryAgent',
    'CollectionAgent',
    'ProcessingAgent',
    'BaseAgent',
    'TaskResult',
    'MediaURL',
    'NewsArticleURL',
    'VideoMetadata',
    'DocumentMetadata',
    'AgentState',
    'MediaAcquisitionSystem',
]
