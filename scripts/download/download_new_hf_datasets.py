#!/usr/bin/env python3
"""
Download additional Epstein datasets from HuggingFace using direct CDN URLs.

Datasets to download:
1. nynxz/epstein-images (1,800 page images, ~5GB)
2. nynxz/epstein-images-cropped (1,600 cropped images, ~5GB)
3. AUSEagle/epstein-data-text (4.12M rows of OCR text, 2.3GB)
4. notesbymuneeb/epstein-emails (5,082 structured email threads)
5. qarnold/epstein-emails-embeddings (5,082 email embeddings)
6. to-be/epstein-emails (4,272 emails from Vision LLM extraction)
"""

import json
import os
import sys
import time
from pathlib import Path

# Load HF token
TOKEN_FILE = Path.home() / ".huggingface" / "token"
HF_TOKEN = ""
if TOKEN_FILE.exists():
    try:
        HF_TOKEN = json.loads(TOKEN_FILE.read_text())["token"]
    except Exception:
        pass

if not HF_TOKEN:
    HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Base output directory
OUTPUT_DIR = Path("/home/cbwinslow/workspace/epstein-data/hf-new-datasets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# CDN base URL for parquet conversions
CDN_BASE = "https://huggingface.co/datasets/{repo}/resolve/main"
PARQUET_CDN = "https://datasets-server.huggingface.co/parquet?dataset={repo}"

DATASETS = [
    {
        "name": "nynxz/epstein-images",
        "description": "Page images from EFTA documents (1,800 images)",
        "output": OUTPUT_DIR / "epstein-images",
        "type": "imagefolder",
    },
    {
        "name": "nynxz/epstein-images-cropped",
        "description": "Cropped page images (1,600 images)",
        "output": OUTPUT_DIR / "epstein-images-cropped",
        "type": "imagefolder",
    },
    {
        "name": "AUSEagle/epstein-data-text",
        "description": "Raw OCR text from all EFTA files (4.12M rows)",
        "output": OUTPUT_DIR / "epstein-data-text",
        "type": "parquet",
    },
    {
        "name": "notesbymuneeb/epstein-emails",
        "description": "Structured email threads from House Oversight docs",
        "output": OUTPUT_DIR / "epstein-emails-structured",
        "type": "parquet",
    },
    {
        "name": "qarnold/epstein-emails-embeddings",
        "description": "Email thread embeddings (768-dim)",
        "output": OUTPUT_DIR / "epstein-emails-embeddings",
        "type": "parquet",
    },
    {
        "name": "to-be/epstein-emails",
        "description": "Emails extracted from screenshots via Vision LLM",
        "output": OUTPUT_DIR / "epstein-emails-vision",
        "type": "parquet",
    },
]


def download_with_retry(url, output_path, max_retries=5):
    """Download a file with retries and exponential backoff."""
    import urllib.request

    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=300) as response:
                content = response.read()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(content)
                return True
        except Exception as e:
            wait_time = min(2**attempt * 2, 60)
            print(f"    Attempt {attempt + 1} failed: {e}")
            print(f"    Retrying in {wait_time}s...")
            time.sleep(wait_time)
    return False


def download_parquet_dataset(ds_config):
    """Download a dataset using the datasets-server parquet endpoint."""
    name = ds_config["name"]
    desc = ds_config["description"]
    output = ds_config["output"]

    print(f"\n{'=' * 60}")
    print(f"Downloading: {name}")
    print(f"Description: {desc}")
    print(f"Output: {output}")
    print(f"{'=' * 60}")

    if output.exists() and any(output.iterdir()):
        print(f"  Skipping - already exists at {output}")
        return

    output.mkdir(parents=True, exist_ok=True)

    # Use datasets-server to get parquet URLs
    parquet_url = PARQUET_CDN.format(repo=name)
    print(f"  Fetching parquet info from: {parquet_url}")

    import urllib.request

    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    try:
        req = urllib.request.Request(parquet_url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            parquet_info = json.loads(response.read())
    except Exception as e:
        print(f"  ERROR fetching parquet info: {e}")
        return

    # Find the train split parquet files
    parquet_files = []
    if "parquet_files" in parquet_info:
        for pf in parquet_info["parquet_files"]:
            if pf.get("split") == "train":
                parquet_files.append(pf["url"])

    if not parquet_files:
        print(f"  No train split parquet files found")
        print(
            f"  Available splits: {[pf.get('split') for pf in parquet_info.get('parquet_files', [])]}"
        )
        return

    print(f"  Found {len(parquet_files)} parquet file(s)")

    # Download each parquet file
    for i, pf_url in enumerate(parquet_files):
        filename = pf_url.split("/")[-1]
        local_path = output / filename
        print(f"  Downloading {filename}...")

        success = download_with_retry(pf_url, local_path)
        if success:
            size_mb = local_path.stat().st_size / (1024 * 1024)
            print(f"    Downloaded: {size_mb:.1f} MB")
        else:
            print(f"    FAILED to download {filename}")

    # Save metadata
    meta_path = output / "metadata.json"
    meta_path.write_text(
        json.dumps(
            {
                "name": name,
                "description": desc,
                "parquet_files": [pf.split("/")[-1] for pf in parquet_files],
                "num_parquet_files": len(parquet_files),
            },
            indent=2,
        )
    )

    print(f"  Metadata saved to {meta_path}")


def download_imagefolder_dataset(ds_config):
    """Download an imagefolder dataset (images as parquet or individual files)."""
    name = ds_config["name"]
    desc = ds_config["description"]
    output = ds_config["output"]

    print(f"\n{'=' * 60}")
    print(f"Downloading: {name}")
    print(f"Description: {desc}")
    print(f"Output: {output}")
    print(f"{'=' * 60}")

    if output.exists() and any(output.iterdir()):
        print(f"  Skipping - already exists at {output}")
        return

    output.mkdir(parents=True, exist_ok=True)

    # For imagefolder datasets, try the parquet conversion first
    parquet_url = PARQUET_CDN.format(repo=name)
    print(f"  Fetching parquet info from: {parquet_url}")

    import urllib.request

    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    try:
        req = urllib.request.Request(parquet_url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            parquet_info = json.loads(response.read())
    except Exception as e:
        print(f"  ERROR fetching parquet info: {e}")
        return

    parquet_files = []
    if "parquet_files" in parquet_info:
        for pf in parquet_info["parquet_files"]:
            if pf.get("split") == "train":
                parquet_files.append(pf["url"])

    if parquet_files:
        print(f"  Found {len(parquet_files)} parquet file(s) for image data")
        for i, pf_url in enumerate(parquet_files):
            filename = pf_url.split("/")[-1]
            local_path = output / filename
            print(f"  Downloading {filename}...")
            success = download_with_retry(pf_url, local_path)
            if success:
                size_mb = local_path.stat().st_size / (1024 * 1024)
                print(f"    Downloaded: {size_mb:.1f} MB")
            else:
                print(f"    FAILED to download {filename}")
    else:
        print(f"  No parquet conversion available for this imagefolder dataset")
        print(f"  Would need to download individual image files (8,404 files)")

    # Save metadata
    meta_path = output / "metadata.json"
    meta_path.write_text(
        json.dumps(
            {
                "name": name,
                "description": desc,
                "parquet_files": [pf.split("/")[-1] for pf in parquet_files],
                "num_parquet_files": len(parquet_files),
            },
            indent=2,
        )
    )


def main():
    print("Epstein HuggingFace Dataset Downloader (Direct CDN)")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"HF Token: {'SET' if HF_TOKEN else 'NOT SET'}")

    # Show what will be downloaded
    print(f"\nDatasets to download:")
    for i, ds in enumerate(DATASETS, 1):
        print(f"  {i}. {ds['name']} - {ds['description']}")

    # Download all
    for ds in DATASETS:
        if ds["type"] == "imagefolder":
            download_imagefolder_dataset(ds)
        else:
            download_parquet_dataset(ds)

    print(f"\n{'=' * 60}")
    print("Download complete!")
    print(f"All datasets saved to: {OUTPUT_DIR}")

    # List results
    print(f"\nDownloaded datasets:")
    for d in sorted(OUTPUT_DIR.iterdir()):
        if d.is_dir():
            total_size = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
            print(f"  {d.name}: {total_size / (1024 * 1024):.1f} MB")


if __name__ == "__main__":
    main()
