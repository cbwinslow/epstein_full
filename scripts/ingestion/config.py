#!/usr/bin/env python3
"""
Centralized configuration for all ingestion scripts
Provides configurable paths, database settings, and common utilities
"""

import os
import logging
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime
import psycopg2

# Base paths
BASE_DATA_DIR = Path(os.getenv('EPSTEIN_DATA_DIR', '/home/cbwinslow/workspace/epstein-data'))
RAW_FILES_DIR = BASE_DATA_DIR / 'raw-files'
DOWNLOADS_DIR = BASE_DATA_DIR / 'downloads'
LOGS_DIR = BASE_DATA_DIR / 'logs' / 'ingestion'

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'epstein'),
    'user': os.getenv('DB_USER', 'cbwinslow'),
    'password': os.getenv('DB_PASSWORD', '123qweasd')
}

# Source-specific paths
CONGRESS_DIR = RAW_FILES_DIR / 'congress'
GOVINFO_DIR = RAW_FILES_DIR / 'govinfo'
FEC_DIR = RAW_FILES_DIR / 'fec'
FEC_COMMITTEES_DIR = RAW_FILES_DIR / 'fec_committees'


def get_db_connection():
    """Get PostgreSQL connection with centralized configuration"""
    return psycopg2.connect(**DB_CONFIG)


def get_source_path(source: str) -> Path:
    """Get path for a specific data source"""
    paths = {
        'congress': CONGRESS_DIR,
        'govinfo': GOVINFO_DIR,
        'fec': FEC_DIR,
        'fec_committees': FEC_COMMITTEES_DIR
    }
    return paths.get(source, RAW_FILES_DIR / source)


def get_log_file(source: str) -> Path:
    """Get log file path for a specific source"""
    from datetime import datetime
    return LOGS_DIR / f"import_{source}_{datetime.now():%Y%m%d_%H%M%S}.log"


def setup_file_logger(name: str) -> tuple[logging.Logger, Path]:
    """
    Setup a file logger with timestamped log file in centralized logs directory.
    Returns tuple of (logger, log_file_path).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{name}_{timestamp}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.propagate = False
    
    return logger, log_file
