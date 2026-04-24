#!/usr/bin/env python3
"""
Download epstein-files-20k from HuggingFace
Dataset: teyler/epstein-files-20k (2,136,420 records)
Output: /home/cbwinslow/workspace/epstein-data/huggingface/epstein_files_20k/
"""

import os
import sys
import json
import time
from pathlib import Path

# Get HF token from environment
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    print("❌ Error: HF_TOKEN environment variable not set")
    print("Usage: HF_TOKEN=xxx python3 download_hf_epstein_files_20k.py")
    sys.exit(1)

# Output directory
OUTPUT_DIR = Path("/home/cbwinslow/workspace/epstein-data/huggingface/epstein_files_20k")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Dataset info
DATASET_NAME = "teyler/epstein-files-20k"
REPO_ID = "teyler/epstein-files-20k"

def download_with_huggingface_hub():
    """Download using huggingface_hub library."""
    try:
        from huggingface_hub import hf_hub_download, login
        
        print(f"🔑 Logging in to HuggingFace...")
        login(token=HF_TOKEN)
        
        print(f"📥 Downloading {DATASET_NAME}...")
        print(f"📁 Output: {OUTPUT_DIR}")
        
        # Download the dataset
        # The dataset should have a data.jsonl file
        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename="data.jsonl",
            repo_type="dataset",
            local_dir=OUTPUT_DIR,
            resume_download=True
        )
        
        print(f"✅ Downloaded: {downloaded_path}")
        return True
        
    except ImportError:
        print("❌ huggingface_hub not installed. Installing...")
        return False
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        return False

def download_with_wget():
    """Download using wget with CDN URL."""
    import subprocess
    
    # CDN URL for the dataset
    url = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main/data.jsonl"
    output_file = OUTPUT_DIR / "data.jsonl"
    
    print(f"📥 Downloading from CDN...")
    print(f"🔗 URL: {url}")
    print(f"📁 Output: {output_file}")
    
    # Use wget with resume support
    cmd = [
        "wget",
        "--continue",  # Resume partial downloads
        "--show-progress",
        "--timeout=60",
        "--tries=5",
        "--header", f"Authorization: Bearer {HF_TOKEN}",
        "-O", str(output_file),
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Download complete: {output_file}")
            # Get file size
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"📊 Size: {size_mb:.2f} MB")
            return True
        else:
            print(f"❌ wget failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def download_with_curl():
    """Download using curl as fallback."""
    import subprocess
    
    url = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main/data.jsonl"
    output_file = OUTPUT_DIR / "data.jsonl"
    
    print(f"📥 Downloading with curl...")
    
    cmd = [
        "curl",
        "-L",  # Follow redirects
        "-C", "-",  # Resume
        "--progress-bar",
        "--retry", "5",
        "--header", f"Authorization: Bearer {HF_TOKEN}",
        "-o", str(output_file),
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Download complete")
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"📊 Size: {size_mb:.2f} MB")
            return True
        else:
            print(f"❌ curl failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("HuggingFace Dataset Download: epstein-files-20k")
    print("=" * 60)
    print(f"Dataset: {DATASET_NAME}")
    print(f"Records: ~2,136,420")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)
    
    # Check if already downloaded
    output_file = OUTPUT_DIR / "data.jsonl"
    if output_file.exists():
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"⚠️  File already exists: {output_file}")
        print(f"📊 Size: {size_mb:.2f} MB")
        if size_mb > 100:  # Assume complete if >100MB
            print("✅ File appears complete ( >100MB). Skipping download.")
            return
        else:
            print("📥 Resuming download...")
    
    # Try huggingface_hub first
    if download_with_huggingface_hub():
        return
    
    # Fall back to wget
    print("\n📥 Trying wget...")
    if download_with_wget():
        return
    
    # Fall back to curl
    print("\n📥 Trying curl...")
    if download_with_curl():
        return
    
    print("\n❌ All download methods failed")
    sys.exit(1)

if __name__ == "__main__":
    main()
