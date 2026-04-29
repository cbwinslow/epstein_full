"""Placeholder loader for Capitol Gains data.

In a full implementation this module would take the transformed parquet files
and load them into the project's database (PostgreSQL, SQLite, etc.).  The
placeholder simply logs the action and returns the path that would have been
loaded.
"""

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def load_to_db(parquet_path: Path, db_uri: str | None = None) -> Path:
    """Placeholder loader.

    Args:
        parquet_path: Path to the parquet file produced by the ETL step.
        db_uri: Optional database connection string.  If omitted a default
            local SQLite file ``capitolgains.db`` in the current working
            directory is assumed.

    Returns:
        The path that would have been loaded (for downstream steps).
    """
    if db_uri is None:
        db_uri = "sqlite:///capitolgains.db"
    log.info("Pretending to load %s into %s", parquet_path, db_uri)
    return parquet_path
