#!/usr/bin/env python3
"""Scan filesystem and compare with SQL records"""

import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data")

def scan_directory(dir_path, name):
    """Scan a directory and extract file metadata."""
    full_path = BASE_DIR / dir_path
    
    if not full_path.exists():
        return None
    
    files = [f for f in full_path.rglob("*") if f.is_file()]
    
    data = {
        "name": name,
        "path": str(full_path),
        "file_count": len(files),
        "total_size_mb": sum(f.stat().st_size for f in files) / (1024*1024),
        "by_extension": defaultdict(list),
        "sample_filenames": []
    }
    
    for f in files:
        ext = f.suffix.lower()
        data["by_extension"][ext].append(f.name)
    
    # Get sample filenames for pattern analysis
    for f in files[:20]:
        data["sample_filenames"].append({
            "name": f.name,
            "size_mb": f.stat().st_size / (1024*1024)
        })
    
    return data

def main():
    datasets = [
        ("huggingface/epstein_files_20k", "epstein_files_20k"),
        ("hf-house-oversight", "house_oversight_txt"),
        ("hf-emails-threads", "email_threads"),
        ("hf-ocr-complete/data", "ocr_complete"),
        ("hf-embeddings/data", "embeddings"),
        ("hf-new-datasets/epstein-data-text", "epstein_data_text"),
        ("hf-new-datasets/epstein-images", "epstein_images"),
        ("hf-new-datasets/epstein-images-cropped", "epstein_images_cropped"),
        ("hf-datasets/fbi-files", "fbi_files"),
        ("hf-datasets/full-index", "full_index"),
    ]
    
    results = {}
    for dir_path, name in datasets:
        data = scan_directory(dir_path, name)
        if data:
            results[name] = data
            print(f"✅ {name}: {data['file_count']} files, {data['total_size_mb']:.1f} MB")
    
    # Save detailed results
    with open("/tmp/filesystem_scan.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed scan saved: /tmp/filesystem_scan.json")
    
    # Print summary
    print("\n" + "="*60)
    print("FILESYSTEM SUMMARY")
    print("="*60)
    
    total_files = sum(d['file_count'] for d in results.values())
    total_size = sum(d['total_size_mb'] for d in results.values())
    
    print(f"Total datasets: {len(results)}")
    print(f"Total files: {total_files:,}")
    print(f"Total size: {total_size:.1f} MB ({total_size/1024:.2f} GB)")
    
    # Show by extension
    all_exts = defaultdict(int)
    for d in results.values():
        for ext, files in d['by_extension'].items():
            all_exts[ext] += len(files)
    
    print("\nFiles by extension:")
    for ext, count in sorted(all_exts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {ext or '(no ext)'}: {count:,} files")

if __name__ == "__main__":
    main()
