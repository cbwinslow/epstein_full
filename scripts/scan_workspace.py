#!/usr/bin/env python3
"""
Scan ~/workspace for all epstein-related folders and files
"""

import os
import json
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path.home() / "workspace"
EPSTEIN_DATA = WORKSPACE / "epstein-data"

def scan_directory(path, name):
    """Scan a directory and return summary."""
    if not path.exists():
        return None
    
    try:
        items = list(path.iterdir())
        files = [f for f in items if f.is_file()]
        dirs = [d for d in items if d.is_dir()]
        
        total_size = sum(f.stat().st_size for f in files) if files else 0
        
        return {
            "path": str(path),
            "files": len(files),
            "directories": len(dirs),
            "total_size_mb": total_size / (1024 * 1024),
            "subdirs": [d.name for d in dirs[:20]]  # First 20
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    print("="*70)
    print("WORKSPACE SCAN - Epstein Related Folders")
    print("="*70)
    
    # 1. Scan ~/workspace for epstein folders
    print("\n📁 ~/workspace/ - Epstein folders:")
    epstein_folders = []
    
    try:
        for item in WORKSPACE.iterdir():
            if item.is_dir() and "epstein" in item.name.lower():
                info = scan_directory(item, item.name)
                epstein_folders.append(info)
                size_str = f"{info['total_size_mb']:.1f} MB" if info else "N/A"
                print(f"  📂 {item.name}/")
                print(f"     Files: {info['files']}, Dirs: {info['directories']}, Size: {size_str}")
    except Exception as e:
        print(f"  Error scanning workspace: {e}")
    
    # 2. Scan epstein-data in detail
    print("\n📁 ~/workspace/epstein-data/ - Data directories:")
    data_dirs = []
    
    if EPSTEIN_DATA.exists():
        for item in sorted(EPSTEIN_DATA.iterdir()):
            if item.is_dir():
                try:
                    # Calculate size recursively
                    total_size = 0
                    file_count = 0
                    for f in item.rglob("*"):
                        if f.is_file():
                            total_size += f.stat().st_size
                            file_count += 1
                    
                    size_mb = total_size / (1024 * 1024)
                    size_gb = size_mb / 1024
                    
                    data_dirs.append({
                        "name": item.name,
                        "path": str(item),
                        "files": file_count,
                        "size_mb": size_mb,
                        "size_gb": size_gb
                    })
                    
                    if size_gb > 1:
                        print(f"  📂 {item.name}/ - {file_count:,} files, {size_gb:.1f} GB")
                    else:
                        print(f"  📂 {item.name}/ - {file_count:,} files, {size_mb:.1f} MB")
                        
                except Exception as e:
                    print(f"  ⚠️  {item.name}/ - Error: {e}")
    
    # 3. Save detailed report
    report = {
        "workspace_folders": epstein_folders,
        "data_directories": data_dirs,
        "timestamp": "April 13, 2026"
    }
    
    with open("/tmp/workspace_scan_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved: /tmp/workspace_scan_report.json")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Epstein folders in workspace: {len(epstein_folders)}")
    print(f"Data directories in epstein-data: {len(data_dirs)}")
    
    total_gb = sum(d['size_gb'] for d in data_dirs)
    print(f"Total data size: {total_gb:.1f} GB")

if __name__ == "__main__":
    main()
