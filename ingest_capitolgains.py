"""Entry point for the Capitol Gains ingestion pipeline.

This script orchestrates the download, extraction, transformation, and loading
of congressional disclosure data (House and Senate). It provides a simple CLI
that can be extended with sub‑commands for each stage of the pipeline.

Usage example::

    python ingest_capitolgains.py download --source house --date 2024-01-01
    python ingest_capitolgains.py run_all

The actual implementation of the downloaders, ETL components and DB loader are
provided in separate modules under the ``epstein`` package (to be created).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)


def _ensure_env_loaded() -> None:
    """Load environment variables from the project's .env files if present."""
    from dotenv import load_dotenv

    env_path = Path(__file__).parent / ".env"
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)
        log.debug("Loaded environment from %s", env_path)
    letta_env = Path(__file__).parent / "letta.env"
    if letta_env.is_file():
        load_dotenv(dotenv_path=letta_env, override=True)
        log.debug("Loaded environment from %s", letta_env)


def download_house(date: str, out_dir: Path) -> Path:
    """Placeholder for House disclosure bulk download.

    Args:
        date: Date string (YYYY-MM-DD) identifying the batch to download.
        out_dir: Directory where the raw JSON will be stored.

    Returns:
        Path to the downloaded JSON file.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    placeholder = out_dir / f"house_{date}.json"
    placeholder.touch()
    log.info("Created placeholder House file %s", placeholder)
    return placeholder


def download_senate(date: str, out_dir: Path) -> Path:
    """Placeholder for Senate disclosure bulk download.

    Mirrors :func:`download_house` but for Senate data.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    placeholder = out_dir / f"senate_{date}.json"
    placeholder.touch()
    log.info("Created placeholder Senate file %s", placeholder)
    return placeholder


def run_all(date: str | None = None) -> None:
    """Run the full pipeline for a given date or the latest available.

    This is a high‑level orchestration stub. Real implementation would invoke the
    ETL extractor, transformer, and loader modules.
    """
    from datetime import datetime

    if date is None:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    raw_dir = Path("raw")
    log.info("Starting full pipeline for %s", date)
    download_house(date, raw_dir)
    download_senate(date, raw_dir)
    # TODO: call extractor, transformer, loader
    log.info("Pipeline stub completed for %s", date)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capitol Gains ingestion pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    dl = sub.add_parser("download", help="Download raw disclosure files")
    dl.add_argument("--source", choices=["house", "senate"], required=True)
    dl.add_argument("--date", required=True, help="YYYY-MM-DD batch date")
    dl.add_argument("--out-dir", default="raw", help="Directory for raw files")

    sub.add_parser("run_all", help="Run the full pipeline for a date")
    parser.add_argument("--date", help="Optional date for run_all (YYYY-MM-DD)")
    return parser


def main() -> None:
    _ensure_env_loaded()
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "download":
        out_dir = Path(args.out_dir)
        if args.source == "house":
            download_house(args.date, out_dir)
        else:
            download_senate(args.date, out_dir)
    elif args.command == "run_all":
        run_all(getattr(args, "date", None))
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
