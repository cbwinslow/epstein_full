"""Shared configuration for Epstein project paths.

This module provides centralized path configuration to avoid hardcoding
paths across multiple scripts. All scripts should import from here.
"""

from pathlib import Path

# Base data directory (migrated from /home/cbwinslow/workspace/epstein-data/)
DATA_ROOT = Path("/home/cbwinslow/workspace/epstein-data")

# Subdirectories
RAW_FILES_DIR = DATA_ROOT / "raw-files"
DATABASES_DIR = DATA_ROOT / "databases"
PROCESSED_DIR = DATA_ROOT / "processed"
KNOWLEDGE_GRAPH_DIR = DATA_ROOT / "knowledge-graph"
LOGS_DIR = DATA_ROOT / "logs"
MODELS_DIR = DATA_ROOT / "models"
DOWNLOADS_DIR = DATA_ROOT / "downloads"
BACKUPS_DIR = DATA_ROOT / "backups"

# Pre-built databases (from Epstein-research-data)
FULL_TEXT_CORPUS_DB = DATABASES_DIR / "full_text_corpus.db"
REDACTION_ANALYSIS_DB = DATABASES_DIR / "redaction_analysis_v2.db"
IMAGE_ANALYSIS_DB = DATABASES_DIR / "image_analysis.db"
OCR_DATABASE_DB = DATABASES_DIR / "ocr_database.db"
COMMUNICATIONS_DB = DATABASES_DIR / "communications.db"
TRANSCRIPTS_DB = DATABASES_DIR / "transcripts.db"
KNOWLEDGE_GRAPH_DB = DATABASES_DIR / "knowledge_graph.db"
PROSECUTORIAL_QUERY_DB = DATABASES_DIR / "prosecutorial_query_graph.db"

# Project directories (code, not data)
PROJECT_ROOT = Path("/home/cbwinslow/workspace/epstein")
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
WORKERS_DIR = PROJECT_ROOT / "workers"
DOCS_DIR = PROJECT_ROOT / "docs"
VENV_DIR = PROJECT_ROOT / "venv"

# Legacy path for backward compatibility (can be removed later)
LEGACY_DATA_ROOT = Path("/home/cbwinslow/workspace/epstein-data")


def ensure_dirs():
    """Ensure all data directories exist."""
    for dir_path in [
        DATA_ROOT, RAW_FILES_DIR, DATABASES_DIR, PROCESSED_DIR,
        KNOWLEDGE_GRAPH_DIR, LOGS_DIR, MODELS_DIR, DOWNLOADS_DIR, BACKUPS_DIR
    ]:
        dir_path.mkdir(parents=True, exist_ok=True)


def get_dataset_path(dataset_num: int) -> Path:
    """Get path to a specific DOJ dataset directory.
    
    Args:
        dataset_num: Dataset number (1-12)
        
    Returns:
        Path to dataset directory
    """
    return RAW_FILES_DIR / f"data{dataset_num}"


def get_all_dataset_paths() -> list[Path]:
    """Get paths to all DOJ dataset directories.
    
    Returns:
        List of paths to data1 through data12
    """
    return [get_dataset_path(i) for i in range(1, 13)]


def resolve_path(path_str: str) -> Path:
    """Resolve a path string, handling both old and new paths.
    
    This function converts legacy /mnt/data paths to new workspace paths.
    
    Args:
        path_str: Path string that may contain old or new path
        
    Returns:
        Resolved Path object pointing to correct location
    """
    path_str = str(path_str)
    
    # Convert legacy paths to new paths
    if "/home/cbwinslow/workspace/epstein-data" in path_str:
        relative = path_str.split("/home/cbwinslow/workspace/epstein-data")[1]
        return DATA_ROOT / relative.lstrip("/")
    
    return Path(path_str)
