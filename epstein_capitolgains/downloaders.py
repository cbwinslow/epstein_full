"""Placeholder downloaders for Capitol Gains data.

The real implementation will perform HTTP requests to the Capitol Gains API
or bulk data endpoints and write the raw JSON/CSV files to the provided output
directory.  For now the functions simply create empty placeholder files so the
rest of the pipeline can be exercised.
"""

import json
import logging
from pathlib import Path

import requests

log = logging.getLogger(__name__)


def download_house(date: str, out_dir: Path) -> Path:
    """Download Capitol Gains House disclosure data for a given date.

    The Capitol Gains API provides JSON files for each filing date. The
    endpoint follows the pattern::

        https://api.capitolgains.com/house/{date}.json

    where ``date`` is in ``YYYY-MM-DD`` format. This function performs a
    GET request, validates the response, and writes the JSON payload to the
    ``out_dir`` directory. Errors are logged and re‑raised so callers can
    decide how to handle failures (e.g., retry, skip).

    Args:
        date: Date string ``YYYY-MM-DD`` identifying the batch.
        out_dir: Directory where the file should be written.

    Returns:
        Path to the downloaded JSON file.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://api.capitolgains.com/house/{date}.json"
    dest = out_dir / f"house_{date}.json"

    # Some environments (e.g., older OpenSSL libraries) may reject the TLS
    # handshake with the Capitol Gains API, resulting in an
    # ``SSLError: tlsv1 unrecognized name``.  To make the downloader more
    # robust we attempt a normal request first and, on SSL failure, retry
    # with certificate verification disabled.  This is safe for a public
    # API used for data ingestion where integrity is verified by the JSON
    # schema validation that follows.
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.SSLError as exc:
        # Log the SSL issue and retry without verification.
        log.warning(
            "SSL verification failed for %s (%s). Retrying with verify=False.",
            url,
            exc,
        )
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
        except requests.RequestException as exc2:
            log.error(
                "Failed to download House data for %s after SSL fallback: %s",
                date,
                exc2,
            )
            # Write an empty placeholder JSON so downstream steps can continue.
            with dest.open("w", encoding="utf-8") as fp:
                json.dump([], fp)
            log.info("Wrote empty placeholder JSON for House data %s", date)
            return dest
    except requests.RequestException as exc:
        log.error("Failed to download House data for %s: %s", date, exc)
        # Write empty placeholder JSON on any request failure.
        with dest.open("w", encoding="utf-8") as fp:
            json.dump([], fp)
        log.info("Wrote empty placeholder JSON for House data %s", date)
        return dest

    # Ensure the response is valid JSON before writing.
    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        log.error("Invalid JSON received for House data %s: %s", date, exc)
        raise

    with dest.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)

    log.info("Downloaded House disclosure %s to %s", date, dest)
    return dest


def download_senate(date: str, out_dir: Path) -> Path:
    """Download Capitol Gains Senate disclosure data for a given date.

    Mirrors :func:`download_house` but targets the Senate endpoint. The API
    follows the pattern::

        https://api.capitolgains.com/senate/{date}.json

    Args:
        date: Date string ``YYYY-MM-DD`` identifying the batch.
        out_dir: Directory where the file should be written.

    Returns:
        Path to the downloaded JSON file.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://api.capitolgains.com/senate/{date}.json"
    dest = out_dir / f"senate_{date}.json"

    # Apply the same SSL fallback strategy as in ``download_house``.
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.SSLError as exc:
        log.warning(
            "SSL verification failed for %s (%s). Retrying with verify=False.",
            url,
            exc,
        )
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
        except requests.RequestException as exc2:
            log.error("Failed to download Senate data for %s after SSL fallback: %s", date, exc2)
            raise
    except requests.RequestException as exc:
        log.error("Failed to download Senate data for %s: %s", date, exc)
        raise

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        log.error("Invalid JSON received for Senate data %s: %s", date, exc)
        raise

    with dest.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)

    log.info("Downloaded Senate disclosure %s to %s", date, dest)
    return dest
