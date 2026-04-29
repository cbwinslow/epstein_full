"""Placeholder ETL (Extract‑Transform‑Load) utilities for Capitol Gains.

The real pipeline will read the raw JSON files produced by the downloaders,
extract the relevant fields, transform them into a normalized schema and
write the results to a database or parquet file.  For now the functions simply
log their actions and return the path to a dummy ``.parquet`` file.
"""

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def extract_transform(raw_path: Path, out_dir: Path) -> Path:
    """Placeholder ETL step.

    Args:
        raw_path: Path to the raw JSON file.
        out_dir: Directory where the transformed output should be written.

    Returns:
        Path to a dummy ``.parquet`` file representing the transformed data.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / (raw_path.stem + ".parquet")
    # Create an empty file to act as a placeholder.
    out_file.touch()
    log.info("ETL placeholder created %s from %s", out_file, raw_path)
    return out_file
