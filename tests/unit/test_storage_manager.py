"""
Unit tests for StorageManager.
"""

import pytest
from datetime import datetime
from media_acquisition.base import StorageManager


class TestStorageManager:
    """Test suite for StorageManager class."""
    
    def test_init(self, storage_manager: StorageManager):
        """Test StorageManager initialization."""
        assert storage_manager is not None
        assert hasattr(storage_manager, 'connection_string')
        assert hasattr(storage_manager, 'base_path')
        assert storage_manager.connection_string is not None
    
    def test_add_to_queue(self, storage_manager: StorageManager):
        """Test adding item to queue."""
        queue_id = storage_manager.add_to_queue(
            media_type='news',
            source_url='https://example.com/test-article',
            priority=5,
            keywords_matched=['Epstein'],
            discovered_by='test-suite',
            metadata={'title': 'Test Article', 'source_domain': 'example.com'}
        )
        
        assert queue_id is not None
        assert isinstance(queue_id, int)
        assert queue_id > 0
    
    def test_get_queue_summary(self, storage_manager: StorageManager):
        """Test getting queue summary."""
        # Add some items first
        for i in range(3):
            storage_manager.add_to_queue(
                media_type='news',
                source_url=f'https://example.com/article{i}',
                priority=5,
                keywords_matched=['Epstein'],
                discovered_by='test'
            )
        
        summary = storage_manager.get_queue_summary()
        
        assert isinstance(summary, dict)
        assert 'news' in summary
        assert summary['news']['pending'] == 3
    
    def test_duplicate_url_handling(self, storage_manager: StorageManager):
        """Test that duplicate URLs are handled correctly."""
        url = 'https://example.com/duplicate-article'
        
        # First add
        id1 = storage_manager.add_to_queue(
            media_type='news',
            source_url=url,
            priority=5,
            keywords_matched=['Epstein']
        )
        
        # Second add (should return None due to ON CONFLICT DO NOTHING)
        id2 = storage_manager.add_to_queue(
            media_type='news',
            source_url=url,
            priority=5,
            keywords_matched=['Epstein']
        )
        
        assert id1 is not None
        assert id2 is None  # Duplicate should not be added
    
    def test_add_to_queue_different_media_types(self, storage_manager: StorageManager):
        """Test adding same URL with different media types."""
        url = 'https://example.com/media-item'
        
        id1 = storage_manager.add_to_queue(
            media_type='news',
            source_url=url,
            priority=5
        )
        
        id2 = storage_manager.add_to_queue(
            media_type='video',
            source_url=url,
            priority=5
        )
        
        # Should allow same URL with different media types
        assert id1 is not None
        assert id2 is not None
        assert id1 != id2
    
    def test_queue_item_priority_ordering(self, storage_manager: StorageManager):
        """Test that items are returned in priority order."""
        # Add items with different priorities
        id1 = storage_manager.add_to_queue(
            media_type='news',
            source_url='https://example.com/low-priority',
            priority=9
        )
        
        id2 = storage_manager.add_to_queue(
            media_type='news',
            source_url='https://example.com/high-priority',
            priority=1
        )
        
        items = storage_manager.get_queued_items(media_type='news', limit=10)
        
        # Should be ordered by priority (lower number = higher priority)
        assert len(items) == 2
        assert items[0]['priority'] == 1
        assert items[1]['priority'] == 9
    
    @pytest.mark.integration
    def test_database_connection(self, storage_manager: StorageManager):
        """Test database connection is working."""
        try:
            summary = storage_manager.get_queue_summary()
            assert isinstance(summary, dict)
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")
