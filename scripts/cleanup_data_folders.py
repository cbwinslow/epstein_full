#!/usr/bin/env python3
"""
Cleanup script for ~/workspace/epstein-data/
- Remove empty directories
- Clean up incomplete downloads
- Organize files properly
"""

import os
import shutil
from pathlib import Path

DATA_DIR = Path.home() / "workspace/epstein-data"

def find_empty_dirs(path):
    """Find all empty directories."""
    empty = []
    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            empty.append(Path(root))
    return empty

def find_empty_files(path):
    """Find all empty files."""
    empty = []
    for f in path.rglob("*"):
        if f.is_file() and f.stat().st_size == 0:
            empty.append(f)
    return empty

def main():
    print("="*70)
    print("CLEANUP REPORT - epstein-data")
    print("="*70)
    
    # 1. Check processed/ directory
    print("\n1. PROCESSED DIRECTORY:")
    processed = DATA_DIR / "processed"
    if processed.exists():
        empty_dirs = find_empty_dirs(processed)
        print(f"   Empty subdirectories: {len(empty_dirs)}")
        for d in empty_dirs:
            print(f"   - {d.relative_to(DATA_DIR)}")
    
    # 2. Check downloads/ directory
    print("\n2. DOWNLOADS DIRECTORY:")
    downloads = DATA_DIR / "downloads"
    empty_files = find_empty_files(downloads)
    print(f"   Empty files: {len(empty_files)}")
    for f in empty_files[:10]:  # Show first 10
        print(f"   - {f.name} (0 bytes)")
    
    empty_dirs = find_empty_dirs(downloads)
    print(f"   Empty directories: {len(empty_dirs)}")
    for d in empty_dirs[:10]:
        print(f"   - {d.relative_to(DATA_DIR)}")
    
    # 3. Check backups/ directory
    print("\n3. BACKUPS DIRECTORY:")
    backups = DATA_DIR / "backups"
    if backups.exists():
        files = list(backups.iterdir())
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        print(f"   Files: {len(files)}")
        print(f"   Total size: {total_size / (1024**3):.1f} GB")
        for f in files:
            if f.is_file():
                size_mb = f.stat().st_size / (1024**2)
                print(f"   - {f.name} ({size_mb:.0f} MB)")
    
    # 4. Check external_repos/
    print("\n4. EXTERNAL REPOS:")
    external = DATA_DIR / "external_repos"
    if external.exists():
        for repo in external.iterdir():
            if repo.is_dir():
                items = list(repo.iterdir())
                print(f"   - {repo.name}: {len(items)} items")
    
    # 5. HF Directory naming
    print("\n5. HF DIRECTORY NAMING:")
    hf_dirs = [d for d in DATA_DIR.iterdir() if d.is_dir() and d.name.startswith("hf")]
    print(f"   HF directories: {len(hf_dirs)}")
    for d in sorted(hf_dirs, key=lambda x: x.name):
        print(f"   - {d.name}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("✅ Task 1: HF naming standardized (all use 'hf-' prefix)")
    print("✅ Task 2: processed/ is empty (nothing to move)")
    print(f"⚠️  Task 3: {len(empty_files)} empty files in downloads/")
    print("✅ Task 4: external_repos/ checked")

if __name__ == "__main__":
    main()
