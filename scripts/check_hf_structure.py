#!/usr/bin/env python3
"""Check structure of HuggingFace dataset directories"""

from pathlib import Path
import json

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data")

def check_structure(path, name, sample_count=3):
    """Check directory structure and sample files"""
    full_path = BASE_DIR / path
    print(f"\n{'='*70}")
    print(f"📁 {name}: {full_path}")
    print('='*70)
    
    if not full_path.exists():
        print("  ❌ Directory does NOT exist")
        return None
    
    files = list(full_path.rglob('*'))
    files = [f for f in files if f.is_file()]
    
    if not files:
        print("  ⚠️  No files found")
        return None
    
    # Count by extension
    ext_counts = {}
    for f in files:
        ext = f.suffix.lower()
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
    
    print(f"  📊 Total files: {len(files)}")
    print(f"  📊 By extension: {dict(sorted(ext_counts.items(), key=lambda x: -x[1])[:5])}")
    
    # Sample files
    print(f"  \n  📄 Sample files ({min(sample_count, len(files))}):")
    for f in sorted(files)[:sample_count]:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"    - {f.name} ({size_mb:.2f} MB)")
    
    return files

# Check each directory
dirs_to_check = [
    ("hf-datasets/full-index", "Full Index"),
    ("hf-datasets/fbi-files", "FBI Files"),
    ("hf-new-datasets/epstein-data-text", "Epstein Data Text"),
    ("hf-new-datasets/epstein-images", "Epstein Images"),
    ("hf-new-datasets/epstein-images-cropped", "Epstein Images Cropped"),
    ("hf-ocr-complete/data", "OCR Complete"),
    ("hf-embeddings/data", "Embeddings"),
    ("hf-emails-threads", "Email Threads"),
    ("hf-house-oversight", "House Oversight TXT"),
]

print("="*70)
print("HUGGINGFACE DATASET STRUCTURE ANALYSIS")
print("="*70)

results = {}
for path, name in dirs_to_check:
    files = check_structure(path, name)
    results[name] = files

# Summary
print("\n" + "="*70)
print("SUMMARY - What needs importing")
print("="*70)

# Compare with SQL tables
sql_tables = {
    "full_epstein_index": 8531,
    "house_oversight_emails": 5082,
    "house_oversight_embeddings": 69290,
    "fbi_vault_pages": 1426,
    "hf_epstein_files_20k": 2136420,
}

print("\n✅ Already in SQL:")
for table, count in sql_tables.items():
    print(f"  - {table}: {count:,} records")

print("\n📁 On disk (need to check for duplicates):")
for name, files in results.items():
    if files:
        print(f"  - {name}: {len(files)} files")
