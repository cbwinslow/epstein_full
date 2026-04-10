#!/usr/bin/env python3
"""
Cross-Reference Validation Script
Validates our data against EpsteinExposed database structure and identifies discrepancies
"""

import os
import sys
import json
import sqlite3
import psycopg2
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv('/home/cbwinslow/workspace/epstein/.env')

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data"
RESEARCH_DATA = "/home/cbwinslow/workspace/epstein/Epstein-research-data"

# Expected EpsteinExposed data structure
EPSTEIN_EXPOSED_EXPECTED = {
    "total_documents": 1400000,  # ~1.4 million PDFs
    "datasets": {
        "data0": {"files": 3159, "description": "Initial release subset"},
        "data1": {"files": 3159, "description": "Initial release"},
        "data2": {"files": 50000, "description": "Supplement 1"},
        "data3": {"files": 50000, "description": "Supplement 2"},
        "data4": {"files": 50000, "description": "Supplement 3"},
        "data5": {"files": 50000, "description": "Supplement 4"},
        "data6": {"files": 50000, "description": "Supplement 5"},
        "data7": {"files": 50000, "description": "Supplement 6"},
        "data8": {"files": 50000, "description": "Supplement 7"},
        "data9": {"files": 50000, "description": "Supplement 8"},
        "data10": {"files": 497679, "description": "Supplement 9 (Largest)"},
        "data11": {"files": 260041, "description": "Supplement 10"},
        "data12": {"files": 100000, "description": "Supplement 11"},
    },
    "database_tables": {
        "documents": 1397821,
        "pages": 2892730,
        "entities": 10000,  # Estimated
        "communications": 41924,
        "redactions": 2587102,
        "images": 38955,
        "transcripts": 1628,
    }
}

class CrossReferenceValidator:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "dataset_comparison": {},
            "database_comparison": {},
            "discrepancies": [],
            "missing_data": [],
            "recommendations": []
        }
        
    def scan_raw_files(self):
        """Scan raw files and compare with expected counts"""
        print("Scanning raw files...")
        
        raw_dir = f"{DATA_ROOT}/raw-files"
        
        for dataset_name, expected in EPSTEIN_EXPOSED_EXPECTED["datasets"].items():
            dataset_path = os.path.join(raw_dir, dataset_name)
            
            if not os.path.exists(dataset_path):
                actual_count = 0
            else:
                actual_count = sum(1 for _ in Path(dataset_path).rglob("*") if _.is_file())
            
            expected_count = expected["files"]
            difference = actual_count - expected_count
            percent_complete = (actual_count / expected_count * 100) if expected_count > 0 else 0
            
            status = "✓" if percent_complete >= 95 else "⚠" if percent_complete >= 50 else "✗"
            
            self.results["dataset_comparison"][dataset_name] = {
                "expected": expected_count,
                "actual": actual_count,
                "difference": difference,
                "percent_complete": round(percent_complete, 2),
                "status": status,
                "description": expected["description"]
            }
            
            if percent_complete < 95:
                self.results["missing_data"].append({
                    "type": "dataset_incomplete",
                    "dataset": dataset_name,
                    "missing": expected_count - actual_count,
                    "severity": "high" if percent_complete < 50 else "medium"
                })
    
    def check_sqlite_databases(self):
        """Check SQLite database counts"""
        print("Checking SQLite databases...")
        
        db_checks = {
            "full_text_corpus.db": {
                "documents": "SELECT COUNT(*) FROM documents",
                "pages": "SELECT COUNT(*) FROM pages"
            },
            "redaction_analysis_v2.db": {
                "redactions": "SELECT COUNT(*) FROM redactions"
            },
            "communications.db": {
                "emails": "SELECT COUNT(*) FROM emails"
            },
            "transcripts.db": {
                "transcripts": "SELECT COUNT(*) FROM transcripts"
            },
            "image_analysis.db": {
                "images": "SELECT COUNT(*) FROM images"
            },
            "knowledge_graph.db": {
                "entities": "SELECT COUNT(*) FROM entities"
            }
        }
        
        for db_name, queries in db_checks.items():
            db_path = f"{DATA_ROOT}/databases/{db_name}"
            
            if not os.path.exists(db_path):
                self.results["database_comparison"][db_name] = {
                    "status": "missing",
                    "error": "Database file not found"
                }
                continue
            
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                db_results = {"status": "ok", "tables": {}}
                
                for table, query in queries.items():
                    try:
                        cursor.execute(query)
                        count = cursor.fetchone()[0]
                        db_results["tables"][table] = count
                        
                        # Compare with expected
                        expected = EPSTEIN_EXPOSED_EXPECTED["database_tables"].get(table)
                        if expected:
                            percent = (count / expected * 100) if expected > 0 else 0
                            db_results["tables"][f"{table}_expected"] = expected
                            db_results["tables"][f"{table}_percent"] = round(percent, 2)
                            
                    except Exception as e:
                        db_results["tables"][table] = f"Error: {e}"
                
                conn.close()
                self.results["database_comparison"][db_name] = db_results
                
            except Exception as e:
                self.results["database_comparison"][db_name] = {
                    "status": "error",
                    "error": str(e)
                }
    
    def check_postgresql(self):
        """Check PostgreSQL database"""
        print("Checking PostgreSQL database...")
        
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "epstein"),
                user=os.getenv("POSTGRES_USER", "cbwinslow"),
                password=os.getenv("POSTGRES_PASSWORD", "123qweasd"),
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=os.getenv("POSTGRES_PORT", "5432")
            )
            cursor = conn.cursor()
            
            # Check if tables exist and get counts
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            pg_results = {
                "status": "connected",
                "tables": {}
            }
            
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    pg_results["tables"][table] = count
                except Exception as e:
                    pg_results["tables"][table] = f"Error: {e}"
            
            conn.close()
            self.results["database_comparison"]["postgresql"] = pg_results
            
        except Exception as e:
            self.results["database_comparison"]["postgresql"] = {
                "status": "error",
                "error": str(e)
            }
    
    def validate_document_integrity(self):
        """Validate document integrity across databases"""
        print("Validating document integrity...")
        
        # Check document counts match between raw files and databases
        total_raw = sum(
            ds["actual"] 
            for ds in self.results["dataset_comparison"].values()
        )
        
        # Get count from full_text_corpus
        db_path = f"{DATA_ROOT}/databases/full_text_corpus.db"
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM documents")
                db_count = cursor.fetchone()[0]
                conn.close()
                
                difference = total_raw - db_count
                
                self.results["document_integrity"] = {
                    "raw_file_count": total_raw,
                    "database_count": db_count,
                    "difference": difference,
                    "status": "ok" if abs(difference) < 1000 else "mismatch"
                }
                
                if abs(difference) > 1000:
                    self.results["discrepancies"].append({
                        "type": "document_count_mismatch",
                        "description": f"Raw files ({total_raw}) != Database ({db_count})",
                        "severity": "high"
                    })
                    
            except Exception as e:
                self.results["document_integrity"] = {
                    "error": str(e)
                }
    
    def generate_recommendations(self):
        """Generate recommendations based on findings"""
        recommendations = []
        
        # Dataset recommendations
        incomplete_datasets = [
            name for name, data in self.results["dataset_comparison"].items()
            if data.get("percent_complete", 0) < 95
        ]
        
        if incomplete_datasets:
            recommendations.append({
                "priority": 1,
                "action": "Download missing datasets",
                "datasets": incomplete_datasets,
                "description": f"Download {len(incomplete_datasets)} incomplete datasets from DOJ"
            })
        
        # PostgreSQL recommendations
        pg_status = self.results["database_comparison"].get("postgresql", {}).get("status")
        if pg_status == "error":
            recommendations.append({
                "priority": 1,
                "action": "Initialize PostgreSQL",
                "description": "Run init_postgres_db.py to create and populate database"
            })
        
        # Missing databases
        missing_dbs = [
            name for name, data in self.results["database_comparison"].items()
            if data.get("status") == "missing"
        ]
        
        if missing_dbs:
            recommendations.append({
                "priority": 2,
                "action": "Rebuild missing databases",
                "databases": missing_dbs,
                "description": f"Rebuild {len(missing_dbs)} SQLite databases from raw data"
            })
        
        self.results["recommendations"] = recommendations
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("CROSS-REFERENCE VALIDATION REPORT")
        print("="*80)
        print(f"Generated: {self.results['timestamp']}")
        print()
        
        # Summary
        total_datasets = len(self.results["dataset_comparison"])
        complete_datasets = sum(
            1 for ds in self.results["dataset_comparison"].values()
            if ds.get("percent_complete", 0) >= 95
        )
        
        total_raw = sum(
            ds["actual"] 
            for ds in self.results["dataset_comparison"].values()
        )
        
        print("SUMMARY")
        print("-"*80)
        print(f"Total Datasets: {total_datasets}")
        print(f"Complete (≥95%): {complete_datasets}")
        print(f"Incomplete: {total_datasets - complete_datasets}")
        print(f"Total Raw Files: {total_raw:,}")
        print(f"Expected Total: {EPSTEIN_EXPOSED_EXPECTED['total_documents']:,}")
        print(f"Coverage: {total_raw / EPSTEIN_EXPOSED_EXPECTED['total_documents'] * 100:.1f}%")
        print()
        
        # Dataset Comparison
        print("DATASET COMPARISON")
        print("-"*80)
        for name, data in sorted(self.results["dataset_comparison"].items()):
            status = data.get("status", "?")
            actual = data.get("actual", 0)
            expected = data.get("expected", 0)
            percent = data.get("percent_complete", 0)
            
            print(f"{status} {name:12} : {actual:>8,} / {expected:>8,} ({percent:>5.1f}%) - {data.get('description', '')}")
        
        print()
        print("DATABASE COMPARISON")
        print("-"*80)
        
        for db_name, data in self.results["database_comparison"].items():
            print(f"\n{db_name}:")
            if data.get("status") == "error":
                print(f"  ERROR: {data.get('error')}")
            elif data.get("status") == "missing":
                print(f"  MISSING: {data.get('error')}")
            else:
                for table, count in data.get("tables", {}).items():
                    if not table.endswith("_expected") and not table.endswith("_percent"):
                        expected_key = f"{table}_expected"
                        percent_key = f"{table}_percent"
                        expected = data["tables"].get(expected_key)
                        percent = data["tables"].get(percent_key)
                        
                        if expected:
                            print(f"  - {table}: {count:,} (expected: {expected:,}, {percent}%)")
                        else:
                            print(f"  - {table}: {count:,}")
        
        # Document Integrity
        if "document_integrity" in self.results:
            print()
            print("DOCUMENT INTEGRITY")
            print("-"*80)
            integrity = self.results["document_integrity"]
            if "error" in integrity:
                print(f"  Error: {integrity['error']}")
            else:
                print(f"  Raw files: {integrity['raw_file_count']:,}")
                print(f"  Database:  {integrity['database_count']:,}")
                print(f"  Status:    {integrity['status']}")
        
        # Missing Data
        if self.results["missing_data"]:
            print()
            print("MISSING DATA")
            print("-"*80)
            for item in sorted(self.results["missing_data"], key=lambda x: x["severity"], reverse=True):
                symbol = "🔴" if item["severity"] == "high" else "🟡"
                print(f"{symbol} {item['dataset']}: {item['missing']:,} files missing ({item['type']})")
        
        # Discrepancies
        if self.results["discrepancies"]:
            print()
            print("DISCREPANCIES FOUND")
            print("-"*80)
            for disc in self.results["discrepancies"]:
                print(f"⚠ {disc['type']}: {disc['description']}")
        
        # Recommendations
        print()
        print("RECOMMENDATIONS")
        print("-"*80)
        
        if not self.results["recommendations"]:
            print("✓ All validations passed - no action needed")
        else:
            for i, rec in enumerate(sorted(self.results["recommendations"], key=lambda x: x["priority"]), 1):
                print(f"{i}. [Priority {rec['priority']}] {rec['action']}")
                print(f"   {rec['description']}")
                if "datasets" in rec:
                    print(f"   Datasets: {', '.join(rec['datasets'])}")
                print()
        
        print("="*80)
    
    def save_results(self):
        """Save results to JSON file"""
        output_file = f"{DATA_ROOT}/validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed report saved to: {output_file}")
    
    def run(self):
        """Run all validations"""
        print("Starting cross-reference validation...\n")
        
        self.scan_raw_files()
        self.check_sqlite_databases()
        self.check_postgresql()
        self.validate_document_integrity()
        self.generate_recommendations()
        self.generate_report()
        self.save_results()
        
        return self.results

if __name__ == "__main__":
    validator = CrossReferenceValidator()
    results = validator.run()
    
    # Exit with error code if critical issues found
    critical_issues = [
        m for m in results.get("missing_data", [])
        if m["severity"] == "high"
    ]
    
    sys.exit(0 if len(critical_issues) == 0 else 1)
