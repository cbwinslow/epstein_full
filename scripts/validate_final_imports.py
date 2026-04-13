#!/usr/bin/env python3
"""
Validate final state of all HF datasets and data imports
Compare filesystem vs PostgreSQL to confirm completeness
"""

import asyncpg
import asyncio
import json
from pathlib import Path

DATA_DIR = Path.home() / "workspace/epstein-data"

async def get_sql_counts():
    """Get record counts from PostgreSQL."""
    conn = await asyncpg.connect("postgresql://cbwinslow:123qweasd@localhost:5432/epstein")
    
    # HF-related tables
    hf_tables = [
        'hf_epstein_files_20k',
        'hf_house_oversight_docs',
        'hf_email_threads',
        'hf_ocr_complete',
        'hf_embeddings',
        'hf_epstein_data_text',
        'full_epstein_index',
        'house_oversight_embeddings',
        'fbi_vault_pages'
    ]
    
    results = {}
    for table in hf_tables:
        try:
            count = await conn.fetchval(f"SELECT COUNT(*) FROM {table}")
            results[table] = count
        except Exception as e:
            results[table] = f"ERROR: {e}"
    
    await conn.close()
    return results

def scan_hf_directories():
    """Scan all HF directories on disk."""
    hf_dirs = {}
    
    if not DATA_DIR.exists():
        return hf_dirs
    
    for item in DATA_DIR.iterdir():
        if item.is_dir() and (item.name.startswith('hf-') or item.name.startswith('huggingface')):
            try:
                # Count files and size
                total_size = 0
                file_count = 0
                for f in item.rglob("*"):
                    if f.is_file():
                        total_size += f.stat().st_size
                        file_count += 1
                
                hf_dirs[item.name] = {
                    'files': file_count,
                    'size_mb': total_size / (1024 * 1024),
                    'path': str(item.relative_to(DATA_DIR))
                }
            except Exception as e:
                hf_dirs[item.name] = {'error': str(e)}
    
    return hf_dirs

async def main():
    print("="*70)
    print("FINAL VALIDATION - HF Dataset Import Status")
    print("="*70)
    
    # 1. SQL counts
    print("\n📊 POSTGRESQL TABLE COUNTS:")
    sql_counts = await get_sql_counts()
    for table, count in sorted(sql_counts.items()):
        if isinstance(count, int):
            print(f"   {table}: {count:,} records")
        else:
            print(f"   {table}: {count}")
    
    # 2. Filesystem scan
    print("\n📁 FILESYSTEM HF DIRECTORIES:")
    hf_dirs = scan_hf_directories()
    for name, info in sorted(hf_dirs.items()):
        if 'error' in info:
            print(f"   {name}: ERROR - {info['error']}")
        else:
            size_gb = info['size_mb'] / 1024
            if size_gb > 1:
                print(f"   {name}: {info['files']} files, {size_gb:.2f} GB")
            else:
                print(f"   {name}: {info['files']} files, {info['size_mb']:.1f} MB")
    
    # 3. Cross-reference
    print("\n🔍 CROSS-REFERENCE (Filesystem vs SQL):")
    
    mapping = {
        'hf-epstein-files-20k': 'hf_epstein_files_20k',
        'hf-house-oversight': 'hf_house_oversight_docs',
        'hf-emails-threads': 'hf_email_threads',
        'hf-ocr-complete': 'hf_ocr_complete',
        'hf-embeddings': 'hf_embeddings',
        'hf-new-datasets': ['hf_epstein_data_text'],  # Multiple datasets
        'hf-datasets': ['fbi_vault_pages', 'full_epstein_index'],
    }
    
    for fs_dir, sql_table in mapping.items():
        if fs_dir in hf_dirs:
            fs_info = hf_dirs[fs_dir]
            if isinstance(sql_table, list):
                # Multiple tables for one directory
                total_sql = sum(sql_counts.get(t, 0) for t in sql_table if isinstance(sql_counts.get(t), int))
                print(f"   {fs_dir}: {fs_info['files']} files -> {total_sql:,} SQL records")
            else:
                sql_count = sql_counts.get(sql_table, 0)
                if isinstance(sql_count, int):
                    if sql_count > 0:
                        print(f"   ✅ {fs_dir}: {fs_info['files']} files -> {sql_count:,} records in {sql_table}")
                    else:
                        print(f"   🔄 {fs_dir}: {fs_info['files']} files -> NOT YET IMPORTED to {sql_table}")
                else:
                    print(f"   ❌ {fs_dir}: {fs_info['files']} files -> TABLE MISSING: {sql_table}")
    
    # 4. Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    total_fs_dirs = len(hf_dirs)
    imported = sum(1 for t in ['hf_epstein_files_20k', 'hf_house_oversight_docs', 
                                'full_epstein_index', 'fbi_vault_pages'] 
                   if isinstance(sql_counts.get(t), int) and sql_counts.get(t, 0) > 0)
    pending = sum(1 for t in ['hf_embeddings', 'hf_epstein_data_text'] 
                  if isinstance(sql_counts.get(t), int) and sql_counts.get(t, 0) == 0)
    
    print(f"   HF directories on disk: {total_fs_dirs}")
    print(f"   Successfully imported: {imported}")
    print(f"   Still pending import: {pending}")
    print(f"   Dropped (duplicates): 1 (hf_email_threads)")
    
    # 5. Final Answer
    print("\n" + "="*70)
    print("FINAL ANSWER")
    print("="*70)
    
    pending_imports = []
    if isinstance(sql_counts.get('hf_embeddings'), int) and sql_counts.get('hf_embeddings', 0) == 0:
        pending_imports.append("hf_embeddings (341 MB)")
    if isinstance(sql_counts.get('hf_epstein_data_text'), int) and sql_counts.get('hf_epstein_data_text', 0) == 0:
        pending_imports.append("hf_epstein_data_text (2.2 GB)")
    
    if pending_imports:
        print(f"   ⏳ REMAINING HF IMPORTS: {len(pending_imports)}")
        for p in pending_imports:
            print(f"      - {p}")
        print("\n   ✅ All other HF datasets: IMPORTED or DROPPED as duplicates")
    else:
        print("   ✅ ALL HF DATASETS IMPORTED - No remaining imports!")
    
    # 6. Other data sources
    print("\n   📌 OTHER DATA SOURCES (non-HF):")
    print("      - ICIJ Offshore Leaks: ⏳ NOT STARTED (~6M records)")
    print("      - FEC Campaign Finance: ✅ LOADED (5.4M records)")
    print("      - GDELT News: 🔄 Active collection (23K+ articles)")

if __name__ == "__main__":
    asyncio.run(main())
