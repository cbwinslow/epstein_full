#!/usr/bin/env python3
"""
Resumable HuggingFace Dataset Downloader

Resumes from where it left off using JSONL append mode.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from datasets import load_dataset

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/huggingface")

# Get HF token from environment variable
HF_API_KEY = os.environ.get("HF_TOKEN")
if not HF_API_KEY:
    raise ValueError("HF_TOKEN environment variable not set")


def download_with_resume(dataset_name, folder_name, batch_size=10000):
    """Download with resume capability."""
    output_dir = BASE_DIR / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / "data.jsonl"
    manifest_path = output_dir / "manifest.json"

    # Check existing progress
    start_idx = 0
    if jsonl_path.exists():
        with open(jsonl_path, "r") as f:
            start_idx = sum(1 for _ in f)
        print(f"📂 Resuming from record {start_idx:,}")

    print(f"⏳ Loading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name, split="train", token=HF_API_KEY)
    total = len(dataset)

    print(f"📊 Total records: {total:,} | Starting from: {start_idx:,}")

    # Append mode
    with open(jsonl_path, "a") as f:
        for i in range(start_idx, total):
            f.write(json.dumps(dataset[i]) + "\n")

            if (i + 1) % batch_size == 0:
                print(f"   Saved {i + 1:,} / {total:,} ({(i + 1) / total * 100:.1f}%)")
                # Flush periodically
                f.flush()

    # Save manifest
    manifest = {
        "dataset_name": dataset_name,
        "record_count": total,
        "download_date": str(datetime.now()),
        "output_path": str(jsonl_path),
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Complete! Total saved: {total:,} records")
    print(f"   File size: {jsonl_path.stat().st_size / (1024 * 1024):.2f} MB")
    return True


if __name__ == "__main__":
    # Resume teyler/epstein-files-20k
    print("=" * 70)
    print("RESUMING DOWNLOAD: teyler/epstein-files-20k")
    print("=" * 70)

    try:
        download_with_resume("teyler/epstein-files-20k", "epstein_files_20k", batch_size=10000)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
