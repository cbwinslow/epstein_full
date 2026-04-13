#!/usr/bin/env python3
"""Duplicate Detection Analysis for Epstein Datasets"""

import asyncio
import asyncpg
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data")

async def analyze_all_tables(conn):
    """Get all tables with record counts."""
    tables = await conn.fetch("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    
    results = []
    for t in tables:
        name = t['table_name']
        try:
            count = await conn.fetchval(f'SELECT COUNT(*) FROM "{name}"')
            results.append({"table": name, "records": count})
        except:
            pass
    return results

async def find_cross_duplicates(conn):
    """Find duplicates across tables."""
    duplicates = []
    
    # Check email thread overlap
    try:
        overlap = await conn.fetchval("""
            SELECT COUNT(*) FROM hf_email_threads h
            INNER JOIN house_oversight_emails ho
            ON h.thread_id = ho.thread_id
        """)
        if overlap > 0:
            duplicates.append({
                "type": "email_threads",
                "tables": ["hf_email_threads", "house_oversight_emails"],
                "overlap": overlap,
                "note": "Exact duplicates"
            })
    except:
        pass
    
    # Check doc_id patterns
    try:
        sql_files = await conn.fetch("""
            SELECT DISTINCT file_path FROM hf_house_oversight_docs
            WHERE file_path IS NOT NULL LIMIT 100
        """)
        patterns = defaultdict(int)
        for row in sql_files:
            val = str(row['file_path'])
            if 'EFT' in val:
                patterns['EFT_docs'] += 1
            if 'email' in val.lower():
                patterns['email_refs'] += 1
        
        duplicates.append({
            "type": "filename_patterns",
            "patterns": dict(patterns)
        })
    except:
        pass
    
    return duplicates

async def analyze_filesystem():
    """Analyze filesystem datasets."""
    fs_data = {}
    
    dirs = [
        ("huggingface/epstein_files_20k", "epstein-files-20k"),
        ("hf-datasets/fbi-files", "fbi-files"),
        ("hf-new-datasets/epstein-data-text", "epstein-data-text"),
        ("hf-ocr-complete/data", "ocr-complete"),
    ]
    
    for dir_path, name in dirs:
        full_path = BASE_DIR / dir_path
        if full_path.exists():
            files = [f for f in full_path.rglob("*") if f.is_file()]
            fs_data[name] = {
                "file_count": len(files),
                "total_size_mb": sum(f.stat().st_size for f in files) / (1024*1024)
            }
    
    return fs_data

async def main():
    print("="*70)
    print("DUPLICATE DETECTION ANALYSIS")
    print("="*70)
    
    conn = await asyncpg.connect(DB_URL)
    try:
        # Analyze SQL tables
        print("\n📊 SQL Tables:")
        tables = await analyze_all_tables(conn)
        for t in tables:
            print(f"  - {t['table']}: {t['records']:,} records")
        
        # Find duplicates
        print("\n🔍 Cross-Table Duplicates:")
        dups = await find_cross_duplicates(conn)
        for d in dups:
            if 'overlap' in d:
                print(f"  ⚠️  {d['tables'][0]} vs {d['tables'][1]}: {d['overlap']:,} duplicates")
            else:
                print(f"  📁 Patterns: {d['patterns']}")
        
        # Analyze filesystem
        print("\n📁 Filesystem Datasets:")
        fs = await analyze_filesystem()
        for name, data in fs.items():
            print(f"  - {name}: {data['file_count']} files, {data['total_size_mb']:.1f} MB")
        
        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "sql_tables": tables,
            "duplicates": dups,
            "filesystem": fs
        }
        
        with open("/tmp/duplicate_analysis.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved: /tmp/duplicate_analysis.json")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
