#!/usr/bin/env python3
"""
Comprehensive Data Inventory and Cross-Validation Script
for Epstein Document Analysis Project
"""

import os
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import subprocess

# Configuration
PROJECT_ROOT = "/home/cbwinslow/workspace/epstein"
DATA_ROOT = "/home/cbwinslow/workspace/epstein-data"
EXTERNAL_STORAGE = "/mnt/archives"
RESEARCH_DATA = f"{PROJECT_ROOT}/Epstein-research-data"

class DataInventory:
    def __init__(self):
        self.inventory = {
            "timestamp": datetime.now().isoformat(),
            "raw_files": {},
            "processed_data": {},
            "databases": {},
            "repositories": {},
            "validation": {},
            "gaps": []
        }
        
    def scan_raw_files(self):
        """Scan all raw file datasets"""
        print("Scanning raw files...")
        raw_dir = f"{DATA_ROOT}/raw-files"
        
        if not os.path.exists(raw_dir):
            print(f"Warning: {raw_dir} does not exist")
            return
            
        for dataset in os.listdir(raw_dir):
            dataset_path = os.path.join(raw_dir, dataset)
            if not os.path.isdir(dataset_path):
                continue
                
            # Count files by extension
            file_counts = defaultdict(int)
            file_sizes = defaultdict(int)
            total_size = 0
            
            for root, dirs, files in os.walk(dataset_path):
                for file in files:
                    ext = Path(file).suffix.lower() or 'no_extension'
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        file_counts[ext] += 1
                        file_sizes[ext] += size
                        total_size += size
                    except OSError:
                        pass
            
            self.inventory["raw_files"][dataset] = {
                "path": dataset_path,
                "total_files": sum(file_counts.values()),
                "total_size_bytes": total_size,
                "total_size_human": self._human_readable_size(total_size),
                "file_types": dict(file_counts),
                "size_by_type": {k: self._human_readable_size(v) for k, v in file_sizes.items()}
            }
            
    def scan_processed_data(self):
        """Scan processed data directories"""
        print("Scanning processed data...")
        
        processed_dirs = [
            f"{DATA_ROOT}/processed",
            f"{PROJECT_ROOT}/processed",
            f"{PROJECT_ROOT}/output",
            f"{PROJECT_ROOT}/out",
            f"{PROJECT_ROOT}/data"
        ]
        
        for proc_dir in processed_dirs:
            if os.path.exists(proc_dir):
                files = list(Path(proc_dir).rglob("*"))
                file_list = [str(f) for f in files if f.is_file()]
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                
                self.inventory["processed_data"][proc_dir] = {
                    "file_count": len(file_list),
                    "total_size": self._human_readable_size(total_size),
                    "sample_files": file_list[:10]
                }
                
    def scan_databases(self):
        """Scan all databases (SQLite and PostgreSQL)"""
        print("Scanning databases...")
        
        # SQLite databases
        db_paths = [
            f"{RESEARCH_DATA}",
            f"{DATA_ROOT}/databases",
            f"{PROJECT_ROOT}/databases"
        ]
        
        for db_path in db_paths:
            if not os.path.exists(db_path):
                continue
                
            for db_file in Path(db_path).rglob("*.db"):
                try:
                    conn = sqlite3.connect(str(db_file))
                    cursor = conn.cursor()
                    
                    # Get table list
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [row[0] for row in cursor.fetchall()]
                    
                    # Get row counts
                    table_info = {}
                    for table in tables[:20]:  # Limit to first 20 tables
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {table}")
                            count = cursor.fetchone()[0]
                            table_info[table] = count
                        except:
                            pass
                    
                    self.inventory["databases"][str(db_file)] = {
                        "type": "sqlite",
                        "tables": table_info,
                        "total_tables": len(tables),
                        "size": self._human_readable_size(db_file.stat().st_size)
                    }
                    
                    conn.close()
                except Exception as e:
                    self.inventory["databases"][str(db_file)] = {
                        "error": str(e)
                    }
                    
        # PostgreSQL databases
        try:
            result = subprocess.run(
                ["sudo", "-u", "postgres", "psql", "-d", "epstein", "-c", 
                 "SELECT schemaname, tablename FROM pg_tables WHERE schemaname='public';"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.inventory["databases"]["postgresql_epstein"] = {
                    "type": "postgresql",
                    "tables": result.stdout,
                    "location": "/mnt/sql/main"
                }
        except Exception as e:
            self.inventory["databases"]["postgresql_epstein"] = {
                "error": str(e)
            }
            
    def scan_repositories(self):
        """Scan all project repositories"""
        print("Scanning repositories...")
        
        repos = [
            ("epstein", PROJECT_ROOT),
            ("Epstein-Pipeline", f"{PROJECT_ROOT}/Epstein-Pipeline"),
            ("Epstein-research-data", f"{PROJECT_ROOT}/Epstein-research-data"),
            ("EpsteinLibraryMediaScraper", f"{PROJECT_ROOT}/EpsteinLibraryMediaScraper"),
            ("epstein-ripper", f"{PROJECT_ROOT}/epstein-ripper"),
            ("epstein-data", "/home/cbwinslow/workspace/epstein-data")
        ]
        
        for name, path in repos:
            if os.path.exists(path):
                # Count files
                total_files = 0
                file_types = defaultdict(int)
                
                for root, dirs, files in os.walk(path):
                    # Skip .git directories
                    dirs[:] = [d for d in dirs if d != '.git']
                    total_files += len(files)
                    for f in files:
                        ext = Path(f).suffix.lower() or 'no_ext'
                        file_types[ext] += 1
                
                # Check for git
                git_info = None
                git_dir = os.path.join(path, '.git')
                if os.path.exists(git_dir):
                    try:
                        result = subprocess.run(
                            ["git", "-C", path, "log", "--oneline", "-1"],
                            capture_output=True, text=True, timeout=5
                        )
                        if result.returncode == 0:
                            git_info = result.stdout.strip()
                    except:
                        pass
                
                self.inventory["repositories"][name] = {
                    "path": path,
                    "exists": True,
                    "total_files": total_files,
                    "file_types": dict(file_types),
                    "last_commit": git_info
                }
            else:
                self.inventory["repositories"][name] = {
                    "path": path,
                    "exists": False
                }
                
    def validate_data(self):
        """Cross-validate data integrity"""
        print("Validating data...")
        
        validation_results = {
            "checksums": {},
            "missing_files": [],
            "corrupted_files": [],
            "consistency_checks": {}
        }
        
        # Check for known required files/directories
        required_paths = [
            f"{DATA_ROOT}/raw-files/data1",
            f"{DATA_ROOT}/raw-files/data10",
            f"{DATA_ROOT}/raw-files/data11",
            f"{RESEARCH_DATA}/tools"
        ]
        
        for path in required_paths:
            if not os.path.exists(path):
                validation_results["missing_files"].append(path)
                
        # Check dataset consistency
        for dataset, info in self.inventory["raw_files"].items():
            if info["total_files"] == 0:
                validation_results["consistency_checks"][dataset] = "Empty dataset"
            elif info["total_size_bytes"] == 0:
                validation_results["consistency_checks"][dataset] = "Zero bytes total size"
            else:
                validation_results["consistency_checks"][dataset] = "OK"
                
        self.inventory["validation"] = validation_results
        
    def identify_gaps(self):
        """Identify data gaps and supplement opportunities"""
        print("Identifying gaps...")
        
        gaps = []
        
        # Check for missing datasets (data2-data9 should exist if we're following pattern)
        raw_datasets = set(self.inventory["raw_files"].keys())
        expected_datasets = set([f"data{i}" for i in range(1, 13)])
        missing_datasets = expected_datasets - raw_datasets
        
        if missing_datasets:
            gaps.append({
                "type": "missing_datasets",
                "description": f"Expected datasets not found: {missing_datasets}",
                "severity": "medium"
            })
            
        # Check for empty datasets
        for dataset, info in self.inventory["raw_files"].items():
            if info["total_files"] == 0:
                gaps.append({
                    "type": "empty_dataset",
                    "dataset": dataset,
                    "description": f"Dataset {dataset} has no files",
                    "severity": "high"
                })
                
        # Check for missing databases
        if "postgresql_epstein" not in self.inventory["databases"]:
            gaps.append({
                "type": "missing_database",
                "description": "PostgreSQL epstein database not accessible",
                "severity": "high"
            })
            
        # Check for missing processed data
        if not self.inventory["processed_data"]:
            gaps.append({
                "type": "missing_processed_data",
                "description": "No processed data found",
                "severity": "low"
            })
            
        self.inventory["gaps"] = gaps
        
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE DATA INVENTORY REPORT")
        print("="*80)
        print(f"Generated: {self.inventory['timestamp']}")
        print()
        
        # Raw Files Summary
        print("RAW FILES SUMMARY")
        print("-"*80)
        for dataset, info in sorted(self.inventory["raw_files"].items()):
            print(f"\n{dataset}:")
            print(f"  Files: {info['total_files']:,}")
            print(f"  Size: {info['total_size_human']}")
            print(f"  Types: {dict(info['file_types'])}")
            
        # Databases Summary
        print("\n" + "="*80)
        print("DATABASES SUMMARY")
        print("-"*80)
        for db, info in self.inventory["databases"].items():
            print(f"\n{db}:")
            if "error" in info:
                print(f"  ERROR: {info['error']}")
            else:
                print(f"  Type: {info.get('type', 'unknown')}")
                print(f"  Size: {info.get('size', 'N/A')}")
                if "tables" in info and isinstance(info["tables"], dict):
                    print(f"  Tables: {len(info['tables'])}")
                    for table, count in list(info["tables"].items())[:5]:
                        print(f"    - {table}: {count:,} rows")
                        
        # Repositories Summary
        print("\n" + "="*80)
        print("REPOSITORIES SUMMARY")
        print("-"*80)
        for repo, info in self.inventory["repositories"].items():
            status = "✓" if info.get("exists") else "✗"
            print(f"\n{status} {repo}:")
            if info.get("exists"):
                print(f"  Path: {info['path']}")
                print(f"  Files: {info.get('total_files', 0):,}")
                if info.get("last_commit"):
                    print(f"  Last commit: {info['last_commit']}")
                    
        # Validation Results
        print("\n" + "="*80)
        print("VALIDATION RESULTS")
        print("-"*80)
        val = self.inventory["validation"]
        
        if val.get("missing_files"):
            print("\nMissing Required Files:")
            for f in val["missing_files"]:
                print(f"  ✗ {f}")
        else:
            print("\n✓ All required files present")
            
        if val.get("consistency_checks"):
            print("\nConsistency Checks:")
            for dataset, status in val["consistency_checks"].items():
                symbol = "✓" if status == "OK" else "⚠"
                print(f"  {symbol} {dataset}: {status}")
                
        # Data Gaps
        print("\n" + "="*80)
        print("DATA GAPS & SUPPLEMENT OPPORTUNITIES")
        print("-"*80)
        if self.inventory["gaps"]:
            for gap in self.inventory["gaps"]:
                severity_symbol = "🔴" if gap["severity"] == "high" else "🟡" if gap["severity"] == "medium" else "🟢"
                print(f"\n{severity_symbol} {gap['type']}")
                print(f"   {gap['description']}")
        else:
            print("\n✓ No significant data gaps identified")
            
        print("\n" + "="*80)
        print("END OF REPORT")
        print("="*80)
        
    def save_inventory(self, output_file="data_inventory.json"):
        """Save inventory to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.inventory, f, indent=2, default=str)
        print(f"\nInventory saved to: {output_file}")
        
    def _human_readable_size(self, size_bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
        
    def run(self):
        """Run complete inventory"""
        print("Starting comprehensive data inventory...\n")
        
        self.scan_raw_files()
        self.scan_processed_data()
        self.scan_databases()
        self.scan_repositories()
        self.validate_data()
        self.identify_gaps()
        self.generate_report()
        
        # Save to file
        output_path = f"{PROJECT_ROOT}/data_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_inventory(output_path)
        
        return self.inventory


if __name__ == "__main__":
    inventory = DataInventory()
    results = inventory.run()
    sys.exit(0 if not results["gaps"] else 1)
