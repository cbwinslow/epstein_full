#!/usr/bin/env python3
"""Configuration for media acquisition system."""

import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'epstein',
    'user': 'cbwinslow',
    'password': '123qweasd'
}

# Build connection string
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Storage paths
BASE_PATH = '/home/cbwinslow/workspace/epstein-data/media'
DOWNLOAD_PATH = '/home/cbwinslow/workspace/epstein-data/downloads'

# Keywords for Epstein-related content
EPSTEIN_KEYWORDS = [
    'jeffrey epstein',
    'ghislaine maxwell',
    'les wexner',
    'virginia giuffre',
    'alan dershowitz',
    'prince andrew',
    'bill clinton epstein',
    'lollita express',
    'epstein island',
    'little saint james',
    'epstein black book',
    'epstein flight logs',
    'jane doe epstein',
    'epstein victims',
    'epstein palm beach',
    'epstein new york mansion',
    'epstein sex trafficking',
    'epstein minor',
    'maxwell epstein',
    'epstein network'
]

# Keywords for 9/11 related content
SEPT11_KEYWORDS = [
    '9/11',
    'september 11',
    'world trade center',
    'twin towers',
    'pentagon attack',
    'flight 93',
    'osama bin laden',
    'al qaeda',
    'terrorist attack 2001',
    'ground zero',
    '9/11 commission',
    '9/11 memorial',
    '9/11 truth',
    '9/11 conspiracy',
    'bush 9/11',
    'cheney 9/11',
    'cia 9/11',
    'fbi 9/11',
    '9/11 intelligence',
    '9/11 warnings'
]

# Date ranges for historical collection
HISTORICAL_RANGES = {
    'early_period': (2001, 2005),      # 9/11 aftermath, early Epstein
    'mid_period': (2006, 2010),        # Middle period
    'late_period': (2011, 2015),       # Late middle
    'recent_period': (2016, 2019),     # Pre-arrest
    'current_period': (2020, 2026)     # Post-arrest to present
}

# News sources to target
TARGET_SOURCES = [
    'nytimes.com',
    'washingtonpost.com',
    'cnn.com',
    'bbc.com',
    'foxnews.com',
    'reuters.com',
    'apnews.com',
    'nbcnews.com',
    'abcnews.go.com',
    'cbsnews.com',
    'usatoday.com',
    'wsj.com',
    'theguardian.com',
    'miamiherald.com',     # Key for Epstein coverage
    'palmbeachpost.com',
    'vanityfair.com',
    'newyorker.com',
    'politico.com',
    'theatlantic.com',
    'vox.com',
    'slate.com',
    'dailybeast.com',
    'huffpost.com'
]

# Wayback Machine configuration
WAYBACK_CONFIG = {
    'base_url': 'https://web.archive.org/web',
    'cdx_url': 'https://web.archive.org/cdx/search/cdx',
    'rate_limit': 0.5,  # seconds between requests
    'timeout': 30
}

# Collection batch settings
BATCH_CONFIG = {
    'batch_size': 100,
    'max_retries': 3,
    'retry_delay': 5,
    'save_interval': 10,  # Save progress every N items
    'resume_file': '/home/cbwinslow/workspace/epstein-data/.collection_state.json'
}

# Rate limiting
RATE_LIMITS = {
    'wayback': 0.5,
    'news_api': 1.0,
    'general_web': 0.25
}

def get_storage_manager():
    """Get configured StorageManager instance."""
    from media_acquisition.base import StorageManager
    return StorageManager(DATABASE_URL, BASE_PATH)

def get_connection_string():
    """Get database connection string."""
    return DATABASE_URL

def ensure_directories():
    """Ensure all required directories exist."""
    os.makedirs(BASE_PATH, exist_ok=True)
    os.makedirs(f"{BASE_PATH}/news-html", exist_ok=True)
    os.makedirs(f"{BASE_PATH}/videos", exist_ok=True)
    os.makedirs(f"{BASE_PATH}/documents", exist_ok=True)
    os.makedirs(f"{BASE_PATH}/transcripts", exist_ok=True)
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
