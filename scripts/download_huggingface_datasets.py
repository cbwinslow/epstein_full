#!/usr/bin/env python3
"""
Download HuggingFace Epstein Datasets

Uses provided API key to download:
1. thelde/remo/FULL_EPSTEIN_INDEX
2. teyler/epstein-files-20k
3. kabasshouse/epstein-data
4. notesbymuneeb/epstein-emails

Usage:
    export HF_TOKEN=<your_token>
    python3 download_huggingface_datasets.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from datasets import load_dataset

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/huggingface")

# Ensure directory exists
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Get HF token from environment variable
HF_API_KEY = os.environ.get("HF_TOKEN")
if not HF_API_KEY:
    raise ValueError("HF_TOKEN environment variable not set")
os.environ["HF_TOKEN"] = HF_API_KEY

# Datasets to download
DATASETS = [
    {
        "name": "thelde/remo/FULL_EPSTEIN_INDEX",
        "folder": "full_epstein_index",
        "description": "House Oversight + DOJ combined (~20K pages)",
    },
    {
        "name": "teyler/epstein-files-20k",
        "folder": "epstein_files_20k",
        "description": "House Oversight documents (20K docs)",
    },
    {
        "name": "kabasshouse/epstein-data",
        "folder": "epstein_credit_card_data",
        "description": "Credit card transactions (CC data)",
    },
    {
        "name": "notesbymuneeb/epstein-emails",
        "folder": "epstein_emails_parsed",
        "description": "Parsed email threads (5,082 threads)",
    },
]


def download_dataset(dataset_info):
    """Download a single dataset."""
    name = dataset_info["name"]
    folder = dataset_info["folder"]
    description = dataset_info["description"]

    output_dir = BASE_DIR / folder

    print(f"\n{'=' * 70}")
    print(f"Downloading: {name}")
    print(f"Description: {description}")
    print(f"Output: {output_dir}")
    print(f"{'=' * 70}")

    if output_dir.exists() and any(output_dir.iterdir()):
        print("⚠️  Directory exists and has content. Checking...")
        # Check if already complete
        manifest_file = output_dir / "manifest.json"
        if manifest_file.exists():
            with open(manifest_file) as f:
                manifest = json.load(f)
            print(f"✅ Previously downloaded: {manifest.get('record_count', 'unknown')} records")
            return True

    try:
        print("⏳ Loading dataset from HuggingFace...")
        dataset = load_dataset(name, split="train", token=HF_API_KEY)

        record_count = len(dataset)
        print(f"✅ Loaded {record_count:,} records")

        # Save as JSONL
        output_dir.mkdir(parents=True, exist_ok=True)
        jsonl_path = output_dir / "data.jsonl"

        print("⏳ Saving to JSONL...")
        with open(jsonl_path, "w") as f:
            for i, record in enumerate(dataset):
                f.write(json.dumps(record) + "\n")
                if (i + 1) % 1000 == 0:
                    print(f"   Saved {i + 1:,} / {record_count:,} records...")

        # Create manifest
        manifest = {
            "dataset_name": name,
            "record_count": record_count,
            "download_date": str(datetime.now()),
            "output_path": str(jsonl_path),
            "features": list(dataset.features.keys()),
        }

        with open(output_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"✅ Complete! Saved to {jsonl_path}")
        print(f"   File size: {jsonl_path.stat().st_size / (1024 * 1024):.2f} MB")
        return True

    except Exception as e:
        print(f"❌ Error downloading {name}: {e}")
        return False


def main():
    print("=" * 70)
    print("HUGGINGFACE EPSTEIN DATASET DOWNLOADER")
    print("=" * 70)

    success_count = 0
    for dataset in DATASETS:
        if download_dataset(dataset):
            success_count += 1

    print(f"\n{'=' * 70}")
    print(f"SUMMARY: {success_count}/{len(DATASETS)} datasets downloaded successfully")
    print(f"Output location: {BASE_DIR}")
    print(f"{'=' * 70}")

    return 0 if success_count == len(DATASETS) else 1


if __name__ == "__main__":
    sys.exit(main())
