#!/usr/bin/env python3
"""
Epstein Project — Comprehensive Data Quality Validation System

This script combines SQL views, database checks, cross-validation,
and AI agent integration for automated data quality monitoring.

Usage:
  python data_quality_validator.py              # Full validation
  python data_quality_validator.py --quick      # Quick check
  python data_quality_validator.py --sql-only   # SQL validation only
  python data_quality_validator.py --ai-report # Generate AI analysis
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration
PG_HOST = os.environ.get("PG_HOST", "localhost")
PG_PORT = int(os.environ.get("PG_PORT", "5432"))
PG_USER = os.environ.get("PG_USER", "cbwinslow")
PG_PASS = os.environ.get("PG_PASSWORD", "")
PG_DB = os.environ.get("PG_DB", "epstein")
PROJECT_ROOT = os.environ.get("EPSTEIN_PROJECT_ROOT", "/home/cbwinslow/workspace/epstein")
REPORT_DIR = f"{PROJECT_ROOT}/data_quality_reports"


class DataQualityValidator:
    """Comprehensive data quality validation system."""
    
    def __init__(self):
        self.conn = None
        self.issues = []
        self.warnings = []
        self.info = []
        self.stats = {}
        
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(
                host=PG_HOST, port=PG_PORT,
                user=PG_USER, password=PG_PASS,
                dbname=PG_DB
            )
            return True
        except Exception as e:
            print(f"✗ Failed to connect to PostgreSQL: {e}")
            return False
    
    def run_sql_validation(self) -> Dict:
        """Run SQL-based data quality checks."""
        print("\n" + "="*80)
        print("SQL DATA QUALITY VALIDATION")
        print("="*80)
        
        results = {
            "orphaned_records": [],
            "duplicates": [],
            "completeness": [],
            "table_stats": {}
        }
        
        # Check for orphaned records
        print("\n[1/4] Checking for orphaned foreign key records...")
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM orphaned_records")
                rows = cur.fetchall()
                for row in rows:
                    if row['orphan_count'] > 0:
                        self.issues.append({
                            'type': 'orphaned_record',
                            'severity': 'HIGH',
                            'table': row['reference_column'],
                            'details': f"{row['orphan_count']} orphans in {row['reference_column']} -> {row['parent_column']}"
                        })
                        print(f"  ✗ {row['reference_column']}: {row['orphan_count']} orphans")
                    else:
                        print(f"  ✓ {row['reference_column']}: OK")
                results['orphaned_records'] = [dict(r) for r in rows]
        except Exception as e:
            print(f"  ⚠ orphaned_records view not available: {e}")
        
        # Check for duplicates
        print("\n[2/4] Checking for duplicate records...")
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM duplicate_detection")
                rows = cur.fetchall()
                for row in rows:
                    self.warnings.append({
                        'type': 'duplicate',
                        'severity': 'MEDIUM',
                        'table': row['table_name'],
                        'details': f"{row['duplicate_count']} duplicates of {row['duplicate_value']}"
                    })
                    print(f"  ⚠ {row['table_name']}: {row['duplicate_count']} duplicates")
                if not rows:
                    print("  ✓ No duplicates found")
                results['duplicates'] = [dict(r) for r in rows]
        except Exception as e:
            print(f"  ⚠ duplicate_detection view not available: {e}")
        
        # Check data completeness
        print("\n[3/4] Checking data completeness...")
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM data_completeness")
                rows = cur.fetchall()
                for row in rows:
                    pct = row.get('title_completeness_pct', 0)
                    if pct < 80:
                        self.issues.append({
                            'type': 'low_completeness',
                            'severity': 'HIGH',
                            'table': row['table_name'],
                            'details': f"Only {pct}% complete"
                        })
                        print(f"  ✗ {row['table_name']}: {pct}% (LOW)")
                    elif pct < 95:
                        self.warnings.append({
                            'type': 'medium_completeness',
                            'severity': 'MEDIUM',
                            'table': row['table_name'],
                            'details': f"{pct}% complete"
                        })
                        print(f"  ⚠ {row['table_name']}: {pct}% (WARNING)")
                    else:
                        print(f"  ✓ {row['table_name']}: {pct}% (OK)")
                results['completeness'] = [dict(r) for r in rows]
        except Exception as e:
            print(f"  ⚠ data_completeness view not available: {e}")
        
        # Run the comprehensive data quality check function
        print("\n[4/4] Running comprehensive quality check...")
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM run_data_quality_check()")
                rows = cur.fetchall()
                for row in rows:
                    print(f"  [{row['severity']}] {row['check_type']}: {row['status']} - {row['details']}")
                results['full_check'] = [dict(r) for r in rows]
        except Exception as e:
            print(f"  ⚠ run_data_quality_check() not available: {e}")
        
        return results
    
    def validate_foreign_keys(self) -> bool:
        """Cross-validate foreign key relationships."""
        print("\n" + "="*80)
        print("FOREIGN KEY VALIDATION")
        print("="*80)
        
        checks = [
            ("relationships.source_entity_id", "entities.id",
             "SELECT COUNT(*) FROM relationships r WHERE NOT EXISTS (SELECT 1 FROM entities e WHERE e.id = r.source_entity_id)"),
            ("relationships.target_entity_id", "entities.id",
             "SELECT COUNT(*) FROM relationships r WHERE NOT EXISTS (SELECT 1 FROM entities e WHERE e.id = r.target_entity_id)"),
            ("rider_clauses.subpoena_id", "subpoenas.id",
             "SELECT COUNT(*) FROM rider_clauses rc WHERE NOT EXISTS (SELECT 1 FROM subpoenas s WHERE s.id = rc.subpoena_id)"),
            ("email_participants.email_id", "emails.id",
             "SELECT COUNT(*) FROM email_participants ep WHERE NOT EXISTS (SELECT 1 FROM emails e WHERE e.id = ep.email_id)"),
        ]
        
        all_passed = True
        for ref_col, parent_col, query in checks:
            try:
                with self.conn.cursor() as cur:
                    cur.execute(query)
                    orphans = cur.fetchone()[0]
                    if orphans == 0:
                        print(f"  ✓ {ref_col} → {parent_col}")
                    else:
                        print(f"  ✗ {ref_col} → {parent_col}: {orphans:,} orphans")
                        all_passed = False
                        self.issues.append({
                            'type': 'fk_violation',
                            'severity': 'HIGH',
                            'table': ref_col,
                            'details': f"{orphans} orphaned records"
                        })
            except Exception as e:
                print(f"  ⚠ {ref_col}: {e}")
        
        return all_passed
    
    def check_document_consistency(self) -> Dict:
        """Validate document processing consistency."""
        print("\n" + "="*80)
        print("DOCUMENT PROCESSING CONSISTENCY")
        print("="*80)
        
        stats = {
            'total_documents': 0,
            'with_ocr': 0,
            'with_classification': 0,
            'with_entities': 0,
            'with_redactions': 0
        }
        
        try:
            with self.conn.cursor() as cur:
                # Total documents
                cur.execute("SELECT COUNT(*) FROM documents")
                stats['total_documents'] = cur.fetchone()[0]
                
                # With OCR
                cur.execute("SELECT COUNT(DISTINCT efta_number) FROM ocr_results")
                stats['with_ocr'] = cur.fetchone()[0]
                
                # With classification
                cur.execute("SELECT COUNT(*) FROM document_classification")
                stats['with_classification'] = cur.fetchone()[0]
                
                # With entities
                cur.execute("SELECT COUNT(DISTINCT efta_number) FROM document_entities")
                stats['with_entities'] = cur.fetchone()[0]
                
                # With redactions
                cur.execute("SELECT COUNT(DISTINCT efta_number) FROM redactions")
                stats['with_redactions'] = cur.fetchone()[0]
                
                print(f"  Total documents: {stats['total_documents']:,}")
                if stats['total_documents'] > 0:
                    print(f"  With OCR: {stats['with_ocr']:,} ({stats['with_ocr']*100/stats['total_documents']:.1f}%)")
                    print(f"  With classification: {stats['with_classification']:,} ({stats['with_classification']*100/stats['total_documents']:.1f}%)")
                    print(f"  With entities: {stats['with_entities']:,} ({stats['with_entities']*100/stats['total_documents']:.1f}%)")
                    print(f"  With redactions: {stats['with_redactions']:,} ({stats['with_redactions']*100/stats['total_documents']:.1f}%)")
                else:
                    print("  With OCR: 0 (0.0%)")
                    print("  With classification: 0 (0.0%)")
                    print("  With entities: 0 (0.0%)")
                    print("  With redactions: 0 (0.0%)")
                
                # Check for documents without any processing
                cur.execute("""
                    SELECT COUNT(*) FROM documents d
                    LEFT JOIN ocr_results o ON d.efta_number = o.efta_number
                    LEFT JOIN document_classification dc ON d.efta_number = dc.efta_number
                    LEFT JOIN document_entities de ON d.efta_number = de.efta_number
                    WHERE o.efta_number IS NULL AND dc.efta_number IS NULL AND de.efta_number IS NULL
                """)
                unprocessed = cur.fetchone()[0]
                if unprocessed > 0:
                    print(f"  ⚠ Unprocessed documents: {unprocessed:,}")
                    self.warnings.append({
                        'type': 'unprocessed_documents',
                        'severity': 'MEDIUM',
                        'table': 'documents',
                        'details': f"{unprocessed} documents have no processing data"
                    })
                else:
                    print(f"  ✓ All documents have some processing data")
                
        except Exception as e:
            print(f"  ⚠ Error checking document consistency: {e}")
        
        return stats
    
    def validate_sqlite_databases(self) -> List[Dict]:
        """Validate SQLite database files."""
        print("\n" + "="*80)
        print("SQLITE DATABASE VALIDATION")
        print("="*80)
        
        import sqlite3
        
        sqlite_dbs = [
            f"{PROJECT_ROOT}/prosecutorial_query_graph.db",
        ]
        
        # Check for compressed databases
        gz_dbs = [
            f"{PROJECT_ROOT}/image_analysis.db.gz",
            f"{PROJECT_ROOT}/ocr_database.db.gz",
            f"{PROJECT_ROOT}/redaction_analysis_v2.db.gz",
            f"{PROJECT_ROOT}/transcripts.db.gz",
        ]
        
        results = []
        
        # Check uncompressed databases
        for db_path in sqlite_dbs:
            if os.path.exists(db_path):
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [r[0] for r in cursor.fetchall()]
                    conn.close()
                    print(f"  ✓ {os.path.basename(db_path)}: {len(tables)} tables")
                    results.append({
                        'file': db_path,
                        'status': 'valid',
                        'tables': len(tables)
                    })
                except Exception as e:
                    print(f"  ✗ {os.path.basename(db_path)}: {e}")
                    results.append({
                        'file': db_path,
                        'status': 'error',
                        'error': str(e)
                    })
                    self.issues.append({
                        'type': 'sqlite_error',
                        'severity': 'HIGH',
                        'table': os.path.basename(db_path),
                        'details': str(e)
                    })
        
        # Check compressed databases
        for gz_path in gz_dbs:
            if os.path.exists(gz_path):
                size = os.path.getsize(gz_path)
                print(f"  ℹ {os.path.basename(gz_path)}: {size/1024/1024:.1f} MB (compressed)")
                results.append({
                    'file': gz_path,
                    'status': 'compressed',
                    'size_mb': size/1024/1024
                })
        
        return results
    
    def generate_report(self) -> Dict:
        """Generate comprehensive data quality report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_issues': len(self.issues),
                'total_warnings': len(self.warnings),
                'total_info': len(self.info),
                'critical_count': len([i for i in self.issues if i.get('severity') == 'HIGH']),
                'status': 'PASS' if not self.issues else 'FAIL'
            },
            'issues': self.issues,
            'warnings': self.warnings,
            'info': self.info,
            'stats': self.stats
        }
        return report
    
    def save_report(self, report: Dict, filename: str = None):
        """Save report to file."""
        os.makedirs(REPORT_DIR, exist_ok=True)
        
        if filename is None:
            filename = f"data_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(REPORT_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n✓ Report saved to: {filepath}")
        return filepath
    
    def generate_ai_analysis_prompt(self, report: Dict) -> str:
        """Generate prompt for AI agent analysis."""
        prompt = f"""# Data Quality Analysis Request

## Summary
- Timestamp: {report['timestamp']}
- Status: {report['summary']['status']}
- Critical Issues: {report['summary']['critical_count']}
- Total Issues: {report['summary']['total_issues']}
- Total Warnings: {report['summary']['total_warnings']}

## Issues Found
"""
        
        for issue in report['issues'][:10]:  # Top 10 issues
            prompt += f"- [{issue['severity']}] {issue['type']} in {issue['table']}: {issue['details']}\n"
        
        if len(report['issues']) > 10:
            prompt += f"- ... and {len(report['issues']) - 10} more issues\n"
        
        prompt += """
## Warnings Found
"""
        for warning in report['warnings'][:5]:  # Top 5 warnings
            prompt += f"- [{warning['severity']}] {warning['type']} in {warning['table']}: {warning['details']}\n"
        
        prompt += """
## Request
Please analyze this data quality report and provide:
1. Root cause analysis for critical issues
2. Recommended fixes prioritized by severity
3. SQL queries or scripts to resolve issues
4. Preventive measures to avoid future data quality problems
5. Suggestions for improving the data validation process

Focus on the highest severity issues first.
"""
        
        return prompt
    
    def run_full_validation(self, ai_analysis: bool = False) -> Dict:
        """Run complete data quality validation."""
        print("\n" + "="*80)
        print("EPSTEIN PROJECT - DATA QUALITY VALIDATION")
        print("="*80)
        print(f"Started: {datetime.now().isoformat()}")
        
        if not self.connect():
            return {'error': 'Failed to connect to database'}
        
        # Run all validation checks
        sql_results = self.run_sql_validation()
        fk_valid = self.validate_foreign_keys()
        doc_stats = self.check_document_consistency()
        sqlite_results = self.validate_sqlite_databases()
        
        self.stats = {
            'sql_validation': sql_results,
            'document_stats': doc_stats,
            'sqlite_databases': sqlite_results,
            'foreign_keys_valid': fk_valid
        }
        
        # Generate and save report
        report = self.generate_report()
        report_path = self.save_report(report)
        
        # Print summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"  Status: {report['summary']['status']}")
        print(f"  Critical Issues: {report['summary']['critical_count']}")
        print(f"  Total Issues: {report['summary']['total_issues']}")
        print(f"  Total Warnings: {report['summary']['total_warnings']}")
        print(f"  Report: {report_path}")
        
        # Generate AI analysis if requested
        if ai_analysis:
            ai_prompt = self.generate_ai_analysis_prompt(report)
            ai_prompt_path = os.path.join(REPORT_DIR, f"ai_analysis_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            with open(ai_prompt_path, 'w') as f:
                f.write(ai_prompt)
            print(f"  AI Prompt: {ai_prompt_path}")
        
        print(f"\nCompleted: {datetime.now().isoformat()}")
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Epstein Project Data Quality Validator"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Run quick validation only"
    )
    parser.add_argument(
        "--sql-only", action="store_true",
        help="Run SQL validation only"
    )
    parser.add_argument(
        "--ai-report", action="store_true",
        help="Generate AI analysis prompt"
    )
    parser.add_argument(
        "--apply-views", action="store_true",
        help="Apply data quality SQL views first"
    )
    
    args = parser.parse_args()
    
    validator = DataQualityValidator()
    
    # Apply SQL views if requested
    if args.apply_views:
        print("Applying data quality SQL views...")
        views_file = f"{PROJECT_ROOT}/migrations/004_data_quality_views.sql"
        if os.path.exists(views_file):
            try:
                subprocess.run(
                    ["psql", "-h", PG_HOST, "-U", PG_USER, "-d", PG_DB, "-f", views_file],
                    check=True, capture_output=True
                )
                print("✓ SQL views applied successfully")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to apply SQL views: {e}")
                return 1
        else:
            print(f"✗ SQL views file not found: {views_file}")
            return 1
    
    # Run validation
    if args.quick:
        if not validator.connect():
            return 1
        validator.run_sql_validation()
    elif args.sql_only:
        if not validator.connect():
            return 1
        validator.run_sql_validation()
        validator.validate_foreign_keys()
    else:
        report = validator.run_full_validation(ai_analysis=args.ai_report)
        if report.get('summary', {}).get('status') == 'FAIL':
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
