#!/usr/bin/env python3
"""
Epstein Project — HuggingFace Dataset Downloader

Downloads the AfricanKillshot/Epstein-Files parquet dataset using aria2c.
Supports parallel downloads with authentication.

Usage:
  python download_hf.py                    # Download all parquet files
  python download_hf.py --verify           # Verify existing downloads
  python download_hf.py --resume           # Resume incomplete downloads
  python download_hf.py --test 5           # Download 5 files for testing
"""

import argparse
import os
import subprocess
from pathlib import Path

# =============================================================================
# Configuration
# =============================================================================

REPO_ID = "AfricanKillshot/Epstein-Files"
HF_DIR = os.environ.get("HF_DIR", "/home/cbwinslow/workspace/epstein-data/hf-parquet")
LOG_DIR = os.environ.get("LOG_DIR", "/home/cbwinslow/workspace/epstein-data/logs")
URL_FILE = os.path.join(LOG_DIR, "hf_urls.txt")
ARIA2_LOG = os.path.join(LOG_DIR, "hf_aria2c.log")

# aria2c settings
ARIA2_CONCURRENT = 8       # Parallel file downloads
ARIA2_CONNECTIONS = 4      # Connections per file
ARIA2_RETRIES = 5
ARIA2_TIMEOUT = 60


def get_hf_token() -> str:
    """Get HuggingFace token from .env or environment."""
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.startswith("HF_TOKEN="):
                        token = line.split("=", 1)[1].strip()
                        break
    return token


def list_parquet_files() -> list:
    """List all parquet files in the HF repo."""
    try:
        from huggingface_hub import list_repo_files
        files = list_repo_files(REPO_ID, repo_type="dataset")
        return sorted([f for f in files if f.endswith(".parquet")])
    except Exception as e:
        print(f"Error listing repo files: {e}")
        return []


def generate_url_list(parquet_files: list, token: str) -> str:
    """Generate aria2c input file with HF URLs.

    Args:
        parquet_files: List of parquet filenames.
        token: HuggingFace auth token.

    Returns:
        Path to the generated URL file.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(HF_DIR, exist_ok=True)

    with open(URL_FILE, "w") as f:
        for pfile in parquet_files:
            url = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main/{pfile}"
            f.write(url + "\n")
            f.write(f"  dir={HF_DIR}\n")
            f.write(f"  out={pfile}\n")
            if token:
                f.write(f"  header=Authorization: Bearer {token}\n")

    return URL_FILE


def run_aria2c(url_file: str) -> int:
    """Run aria2c with the URL file.

    Args:
        url_file: Path to aria2c input file.

    Returns:
        Exit code from aria2c.
    """
    cmd = [
        "aria2c",
        "--input-file", url_file,
        "--max-concurrent-downloads", str(ARIA2_CONCURRENT),
        "--max-connection-per-server", str(ARIA2_CONNECTIONS),
        "--retry-wait", "3",
        "--max-tries", str(ARIA2_RETRIES),
        "--timeout", str(ARIA2_TIMEOUT),
        "--continue=true",
        "--auto-file-renaming=false",
        "--allow-overwrite=false",
        "--summary-interval=10",
        "--log", ARIA2_LOG,
        "--log-level=notice",
        "--console-log-level=notice",
    ]

    print(f"Running aria2c with {ARIA2_CONCURRENT} concurrent downloads...")
    try:
        return subprocess.run(cmd).returncode
    except FileNotFoundError:
        print("Error: aria2c not found. Install: sudo apt-get install aria2")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130


def verify_downloads() -> dict:
    """Verify downloaded parquet files.

    Returns:
        Dict with verification results.
    """
    results = {"total": 0, "present": 0, "missing": 0, "zero_size": 0, "total_size": 0}

    parquet_files = list_parquet_files()
    if not parquet_files:
        print("Could not list repo files. Checking local directory only.")
        local_files = sorted(Path(HF_DIR).glob("*.parquet"))
        for f in local_files:
            results["total"] += 1
            results["present"] += 1
            results["total_size"] += f.stat().st_size
        return results

    results["total"] = len(parquet_files)

    for pfile in parquet_files:
        local_path = os.path.join(HF_DIR, pfile)
        if os.path.exists(local_path):
            size = os.path.getsize(local_path)
            if size == 0:
                results["zero_size"] += 1
            else:
                results["present"] += 1
                results["total_size"] += size
        else:
            results["missing"] += 1

    return results


def print_status():
    """Print current download status."""
    results = verify_downloads()
    total = results["total"]
    present = results["present"]
    size_gb = results["total_size"] / (1024**3)

    print(f"\n{'='*50}")
    print("  HF Parquet Download Status")
    print(f"{'='*50}")
    print(f"  Files:  {present}/{total} ({present/max(total,1)*100:.1f}%)")
    print(f"  Size:   {size_gb:.1f} GB")
    print(f"  Missing: {results['missing']}")
    print(f"  Zero:   {results['zero_size']}")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description="HuggingFace dataset downloader")
    parser.add_argument("--verify", action="store_true", help="Verify downloads only")
    parser.add_argument("--resume", action="store_true", help="Resume incomplete downloads")
    parser.add_argument("--test", type=int, default=0, help="Download only N files for testing")

    args = parser.parse_args()

    if args.verify:
        print_status()
        return

    token = get_hf_token()
    if not token:
        print("Warning: No HF_TOKEN found. Set in .env or environment variable.")
        print("Downloads may be rate-limited without authentication.\n")

    print(f"Listing parquet files from {REPO_ID}...")
    parquet_files = list_parquet_files()
    print(f"Found {len(parquet_files)} parquet files")

    if args.test > 0:
        parquet_files = parquet_files[:args.test]
        print(f"Test mode: downloading {len(parquet_files)} files")

    print("Generating URL list...")
    url_file = generate_url_list(parquet_files, token)
    print(f"URL list: {url_file} ({len(parquet_files)} files)")

    rc = run_aria2c(url_file)
    print_status()

    if rc == 0:
        print("Download complete!")
    else:
        print(f"aria2c exited with code {rc}")


if __name__ == "__main__":
    main()
