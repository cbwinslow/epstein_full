#!/usr/bin/env python3
"""
Epstein Project - CDN Downloader (RollCall Mirror)

Fast parallel download using the RollCall CDN mirror.
No age gate, no Playwright needed — pure HTTP with aria2c.

Downloads files using aria2c with 10 parallel connections.
Skips already-downloaded files and confirmed-removed EFTAs.

Usage:
  python3 download_cdn.py                    # Download all remaining files
  python3 download_cdn.py --datasets 9,10    # Specific datasets only
  python3 download_cdn.py --test 50          # Test with 50 files
  python3 download_cdn.py --monitor          # Show progress only
"""

import argparse
import csv
import json
import os
import sqlite3
import subprocess
import time
from datetime import datetime
from glob import glob

# Import shared configuration
from epstein_config import RAW_FILES_DIR, LOGS_DIR, FULL_TEXT_CORPUS_DB

# =============================================================================
# Configuration Constants
# =============================================================================

CDN_URL = "https://media-cdn.rollcall.com/epstein-files/EFTA{efta:08d}.pdf"
RAW_DIR = str(RAW_FILES_DIR)
LOG_DIR = str(LOGS_DIR)
TRACKER = "/home/cbwinslow/workspace/epstein/scripts/tracker.py"
PYTHON = "/home/cbwinslow/workspace/epstein/venv/bin/python3"
EFTA_LIST_FILE = os.path.join(LOG_DIR, "efta_to_download.json")
REMOVED_CSV = "/home/cbwinslow/workspace/epstein/Epstein-research-data/doj_audit/CONFIRMED_REMOVED.csv"
URL_LIST_FILE = os.path.join(LOG_DIR, "cdn_urls.txt")
ARIA2_LOG = os.path.join(LOG_DIR, "aria2c.log")

# aria2c settings
ARIA2_CONNECTIONS = 10       # Parallel downloads
ARIA2_MAX_CONCURRENT = 16    # Max active downloads
ARIA2_RETRIES = 3            # Retry count per file
ARIA2_TIMEOUT = 30           # Connection timeout (seconds)
ARIA2_SPLIT = 1              # Single connection per file (many small files)


# =============================================================================
# Utility Functions
# =============================================================================

def log(msg: str) -> None:
    """Print timestamped log message and append to log file."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, "cdn_download.log"), "a") as f:
        f.write(line + "\n")


def load_removed_eftas() -> set:
    """Load the set of confirmed-removed EFTA numbers from audit CSV.

    Returns:
        set: Set of EFTA integers that return 404 on DOJ.
    """
    removed = set()
    if not os.path.exists(REMOVED_CSV):
        log(f"Warning: Removed CSV not found at {REMOVED_CSV}")
        return removed

    try:
        with open(REMOVED_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                efta_str = row.get("efta", "")
                if efta_str.startswith("EFTA"):
                    try:
                        removed.add(int(efta_str[4:]))
                    except ValueError:
                        pass
        log(f"Loaded {len(removed):,} confirmed-removed EFTAs")
    except Exception as e:
        log(f"Error loading removed CSV: {e}")

    return removed


def get_efta_to_dataset_map() -> dict:
    """Build mapping of EFTA number -> dataset number from full_text_corpus.

    Returns:
        dict: Maps EFTA integer -> dataset integer.
    """
    db_path = "/home/cbwinslow/workspace/epstein-data/databases/full_text_corpus.db"
    if not os.path.exists(db_path):
        log("Warning: full_text_corpus.db not found, using fallback ranges")
        return _fallback_efta_map()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute(
            "SELECT DISTINCT efta_number, dataset FROM pages "
            "WHERE efta_number LIKE 'EFTA%' AND dataset BETWEEN 1 AND 12"
        )
        mapping = {}
        for row in cursor.fetchall():
            try:
                efta_num = int(row[0][4:])
                mapping[efta_num] = row[1]
            except (ValueError, IndexError):
                pass
        conn.close()
        log(f"Loaded EFTA-to-dataset mapping: {len(mapping):,} entries")
        return mapping
    except sqlite3.Error as e:
        log(f"Error reading full_text_corpus: {e}")
        return _fallback_efta_map()


def _fallback_efta_map() -> dict:
    """Build EFTA mapping from hardcoded ranges if DB unavailable."""
    ranges = {
        1: (1, 3158), 2: (3159, 3857), 3: (3858, 5586), 4: (5705, 8320),
        5: (8409, 8528), 6: (8529, 8998), 7: (9016, 9664), 8: (9676, 39023),
        9: (39025, 1262781), 10: (1262782, 2205654), 11: (2205655, 2730264),
        12: (2730265, 2858497),
    }
    mapping = {}
    for ds, (start, end) in ranges.items():
        for efta in range(start, end + 1):
            mapping[efta] = ds
    return mapping


def is_valid_pdf(filepath: str) -> bool:
    """Check if file exists and has valid PDF header."""
    try:
        if not os.path.exists(filepath) or os.path.getsize(filepath) < 100:
            return False
        with open(filepath, "rb") as f:
            return f.read(5) == b"%PDF-"
    except OSError:
        return False


# =============================================================================
# URL List Generation
# =============================================================================

def build_url_list(datasets: list[int] = None, test_limit: int = 0) -> tuple:
    """Build aria2c input file with URLs, output dirs, and filenames.

    Args:
        datasets: List of dataset numbers to include (None = all).
        test_limit: If > 0, only include this many URLs (for testing).

    Returns:
        tuple: (url_count, url_list_path)
    """
    # Load EFTA list (already filtered to exclude downloaded files)
    if not os.path.exists(EFTA_LIST_FILE):
        log(f"Error: EFTA list not found at {EFTA_LIST_FILE}")
        log("Run the Playwright downloader first to generate the list, or")
        log("rebuild from full_text_corpus.db")
        return 0, None

    with open(EFTA_LIST_FILE) as f:
        efta_lists = json.load(f)

    # Load removed EFTAs
    removed = load_removed_eftas()

    # Load EFTA->dataset mapping
    efta_to_ds = get_efta_to_dataset_map()

    # Filter datasets
    if datasets:
        efta_lists = {k: v for k, v in efta_lists.items() if int(k) in datasets}

    # Build URL list
    url_lines = []
    skipped_removed = 0
    skipped_exists = 0

    for ds_str, eftas in efta_lists.items():
        ds = int(ds_str)
        out_dir = os.path.join(RAW_DIR, f"data{ds}")

        for efta in eftas:
            # Skip confirmed-removed
            if efta in removed:
                skipped_removed += 1
                continue

            # Skip already downloaded (double-check)
            out_path = os.path.join(out_dir, f"EFTA{efta:08d}.pdf")
            if is_valid_pdf(out_path):
                skipped_exists += 1
                continue

            url = CDN_URL.format(efta=efta)

            # aria2c input format: url\n  dir=output_dir\n  out=filename
            url_lines.append(url)
            url_lines.append(f"  dir={out_dir}")
            url_lines.append(f"  out=EFTA{efta:08d}.pdf")

            if test_limit > 0 and len(url_lines) // 3 >= test_limit:
                break

        if test_limit > 0 and len(url_lines) // 3 >= test_limit:
            break

    url_count = len(url_lines) // 3

    log(f"URL list: {url_count:,} files to download")
    log(f"  Skipped (removed): {skipped_removed:,}")
    log(f"  Skipped (exists): {skipped_exists:,}")

    # Write URL list file
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(URL_LIST_FILE, "w") as f:
        f.write("\n".join(url_lines) + "\n")

    return url_count, URL_LIST_FILE


# =============================================================================
# Download Execution
# =============================================================================

def run_aria2c(url_file: str) -> int:
    """Run aria2c with the given URL list file.

    Args:
        url_file: Path to aria2c input file.

    Returns:
        int: Exit code from aria2c.
    """
    cmd = [
        "aria2c",
        "--input-file", url_file,
        "--max-concurrent-downloads", str(ARIA2_MAX_CONCURRENT),
        "--max-connection-per-server", str(ARIA2_CONNECTIONS),
        "--retry-wait", "2",
        "--max-tries", str(ARIA2_RETRIES),
        "--timeout", str(ARIA2_TIMEOUT),
        "--continue=true",
        "--auto-file-renaming=false",
        "--allow-overwrite=false",
        "--summary-interval=10",
        "--download-result=full",
        "--log", ARIA2_LOG,
        "--log-level=notice",
        # Don't overwhelm the CDN
        "--max-overall-download-limit=0",
        "--max-download-limit=0",
        # Validation
        "--check-integrity=false",
        # Quiet but show progress
        "--console-log-level=notice",
    ]

    log(f"Running aria2c: {len(open(url_file).readlines()) // 3} URLs")
    log(f"Command: {' '.join(cmd[:6])}...")

    try:
        proc = subprocess.run(cmd, timeout=None)
        return proc.returncode
    except FileNotFoundError:
        log("Error: aria2c not found. Install with: sudo apt-get install aria2")
        return 1
    except KeyboardInterrupt:
        log("Interrupted by user")
        return 130


# =============================================================================
# Progress Monitoring
# =============================================================================

def count_downloaded() -> dict:
    """Count downloaded PDFs per dataset.

    Returns:
        dict: Maps dataset number -> file count.
    """
    counts = {}
    for ds in range(1, 13):
        pattern = os.path.join(RAW_DIR, f"data{ds}", "*.pdf")
        counts[ds] = len(glob(pattern))
    return counts


def update_tracker() -> None:
    """Update the SQLite tracker with current file counts."""
    counts = count_downloaded()
    for ds, count in counts.items():
        subprocess.run(
            [PYTHON, TRACKER, "update", "--id", f"doj-ds{ds}", "--current", str(count)],
            capture_output=True
        )


def print_status() -> None:
    """Print current download status."""
    os.system("clear")
    counts = count_downloaded()
    total = sum(counts.values())

    print("=" * 60)
    print("  EPSTEIN CDN DOWNLOADER (RollCall Mirror)")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    expected = {
        1: 3158, 2: 699, 3: 1729, 4: 2616, 5: 120,
        6: 470, 7: 649, 8: 29348, 9: 103608, 10: 94287,
        11: 52459, 12: 12820,
    }

    for ds in range(1, 13):
        count = counts[ds]
        exp = expected[ds]
        pct = (count / exp * 100) if exp > 0 else 0
        bar = "█" * int(20 * pct / 100) + "░" * (20 - int(20 * pct / 100))
        icon = "✓" if pct >= 99 else "●"
        print(f"  {icon} DS {ds:>2} [{bar}] {pct:5.1f}%  {count:>7,} / {exp:>7,}")

    print(f"\n  TOTAL: {total:,} files")
    print("=" * 60)


def monitor_loop(refresh: int = 15) -> None:
    """Continuously display progress.

    Args:
        refresh: Seconds between updates.
    """
    try:
        while True:
            update_tracker()
            print_status()
            print(f"\n  Refreshing every {refresh}s. Ctrl+C to stop.")
            time.sleep(refresh)
    except KeyboardInterrupt:
        print("\nStopped.")


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    """Parse arguments and run the CDN downloader."""
    parser = argparse.ArgumentParser(
        description="CDN Downloader - Fast parallel download via RollCall mirror"
    )
    parser.add_argument(
        "--datasets", type=str, default=None,
        help="Comma-separated dataset numbers (e.g., '9,10'). Default: all."
    )
    parser.add_argument(
        "--test", type=int, default=0,
        help="Test mode: download only N files (e.g., --test 50)"
    )
    parser.add_argument(
        "--monitor", action="store_true",
        help="Monitor only (no download)"
    )

    args = parser.parse_args()

    if args.monitor:
        monitor_loop()
        return

    # Parse datasets
    datasets = None
    if args.datasets:
        datasets = [int(d) for d in args.datasets.split(",")]

    log("=" * 50)
    log("CDN Downloader starting")
    log(f"Datasets: {datasets or 'all'}")
    if args.test:
        log(f"Test mode: {args.test} files only")
    log("=" * 50)

    # Build URL list
    url_count, url_file = build_url_list(datasets=datasets, test_limit=args.test)
    if url_count == 0:
        log("No files to download (all done or list empty)")
        return

    # Run aria2c
    log(f"Starting download of {url_count:,} files via RollCall CDN...")
    start_time = time.time()
    rc = run_aria2c(url_file)
    elapsed = time.time() - start_time

    # Final status
    update_tracker()
    print_status()

    final_counts = count_downloaded()
    total = sum(final_counts.values())
    rate = url_count / elapsed if elapsed > 0 else 0

    log(f"aria2c exit code: {rc}")
    log(f"Downloaded: {total:,} total files")
    log(f"Session: {url_count} files in {elapsed:.0f}s ({rate:.1f} files/sec)")
    log(f"Log: {ARIA2_LOG}")


if __name__ == "__main__":
    main()
