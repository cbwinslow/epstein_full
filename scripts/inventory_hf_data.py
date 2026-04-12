#!/usr/bin/env python3
"""Inventory HuggingFace datasets in epstein-data"""

import os
from pathlib import Path

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data")

def check_dir(path, name):
    """Check if directory exists and list contents"""
    full_path = BASE_DIR / path
    print(f"\n{'='*60}")
    print(f"📁 {name}: {full_path}")
    print('='*60)
    
    if not full_path.exists():
        print("  ❌ Directory does NOT exist")
        return
    
    try:
        items = list(full_path.iterdir())
        if not items:
            print("  ⚠️  Directory is EMPTY")
            return
        
        # Sort by type (dirs first) then by name
        dirs = [p for p in items if p.is_dir()]
        files = [p for p in items if p.is_file()]
        
        for d in sorted(dirs):
            size = sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            print(f"  📂 {d.name}/ ({size_mb:.1f} MB)")
            
        for f in sorted(files)[:20]:  # Limit to 20 files
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  📄 {f.name} ({size_mb:.2f} MB)")
            
        if len(files) > 20:
            print(f"  ... and {len(files) - 20} more files")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

# Main inventory
print("="*60)
print("HUGGINGFACE DATASET INVENTORY")
print(f"Base: {BASE_DIR}")
print("="*60)

# Check all HF-related directories
dirs_to_check = [
    ("huggingface", "Standard HuggingFace"),
    ("hf-datasets", "HF Datasets"),
    ("hf-new-datasets", "HF New Datasets"),
    ("hf-house-oversight", "HF House Oversight"),
    ("hf-emails-threads", "HF Emails Threads"),
    ("hf-ocr-complete", "HF OCR Complete"),
    ("hf-embeddings", "HF Embeddings"),
    ("hf-emails-alt", "HF Emails Alt"),
]

for path, name in dirs_to_check:
    check_dir(path, name)

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

datasets_found = []
for path, name in dirs_to_check:
    full_path = BASE_DIR / path
    if full_path.exists() and any(full_path.iterdir()):
        datasets_found.append(name)

if datasets_found:
    print(f"✅ Found data in: {', '.join(datasets_found)}")
else:
    print("⚠️  No HuggingFace data found")

print("\n🔍 Check for FULL_EPSTEIN_INDEX dataset:")
full_epstein = BASE_DIR / "huggingface" / "full_epstein_index"
if full_epstein.exists():
    print(f"  ✅ Found: {full_epstein}")
else:
    print(f"  ❌ Not found: {full_epstein}")
    print(f"  📥 Needs download from: thelde/remo/FULL_EPSTEIN_INDEX")

print("\n🔍 Check for epstein-files-20k dataset:")
ep20k = BASE_DIR / "huggingface" / "epstein_files_20k"
if ep20k.exists():
    files = list(ep20k.glob("*"))
    if files:
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        print(f"  ✅ Found: {ep20k}")
        print(f"  📊 Size: {total_size/(1024*1024):.2f} MB")
        print(f"  📄 Files: {len(files)}")
    else:
        print(f"  ⚠️  Directory exists but EMPTY")
else:
    print(f"  ❌ Not found")
