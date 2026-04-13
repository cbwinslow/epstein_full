#!/usr/bin/env python3
"""Generate comprehensive data import summary report"""
import psycopg2
from datetime import datetime

def generate_report():
    conn = psycopg2.connect(
        host='localhost', dbname='epstein', user='cbwinslow', password='123qweasd',
        connect_timeout=10
    )
    cur = conn.cursor()
    
    print("="*70)
    print("EPSTEIN DATA IMPORT SUMMARY REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Overall Summary
    print("\n📊 OVERALL SUMMARY")
    print("-"*70)
    cur.execute("SELECT * FROM v_overall_data_summary")
    row = cur.fetchone()
    print(f"Complete Sources:     {row[0]}")
    print(f"In Progress Sources:  {row[1]}")
    print(f"Pending Sources:      {row[2]}")
    print(f"Duplicate Sources:    {row[3]}")
    print(f"Total Records:        {row[4]:,} / {row[5]:,}")
    if row[5] > 0:
        pct = 100.0 * row[4] / row[5]
        print(f"Overall Completion:   {pct:.1f}%")
    
    # By Source Type
    print("\n📁 BY SOURCE TYPE")
    print("-"*70)
    cur.execute("SELECT * FROM v_data_inventory_summary ORDER BY source_type, status")
    for row in cur.fetchall():
        print(f"{row[0]:<15} {row[1]:<12} {row[2]:>3} sources  {row[4]:>12,} / {row[3]:>12,} ({row[5]:>5.1f}%)")
    
    # ICIJ Import Progress
    print("\n🔄 ICIJ IMPORT PROGRESS (Running in Background)")
    print("-"*70)
    cur.execute("SELECT filename, status, rows_imported, total_rows FROM icij_import_progress ORDER BY status, filename")
    for row in cur.fetchall():
        filename, status, imported, total = row
        icon = {'complete': '✅', 'running': '🔄', 'pending': '⏳', 'failed': '❌'}.get(status, '❓')
        if total and total > 0:
            pct = 100.0 * (imported or 0) / total
            print(f"{icon} {filename:<25} {status:<10} {imported:>10,} / {total:>10,} ({pct:>5.1f}%)")
        else:
            print(f"{icon} {filename:<25} {status:<10} {imported:>10,}")
    
    # HF Datasets Detail
    print("\n✅ HF DATASETS (COMPLETE)")
    print("-"*70)
    cur.execute("SELECT source_name, target_table, actual_records, status FROM data_inventory WHERE source_type = 'huggingface' AND status = 'complete' ORDER BY actual_records DESC")
    for row in cur.fetchall():
        print(f"  {row[0]:<30} {row[1]:<25} {row[2]:>10,} records")
    
    # Validation Views Available
    print("\n🔍 VALIDATION VIEWS AVAILABLE")
    print("-"*70)
    views = [
        'v_table_record_counts - Table sizes and existence',
        'v_icij_import_summary - Real-time ICIJ import progress',
        'v_icij_relationship_validation - Relationship integrity checks',
        'v_icij_data_quality - Data quality issues',
        'v_hf_dataset_summary - HF dataset summary',
        'v_data_inventory_summary - Overall inventory status',
        'v_overall_data_summary - High-level summary'
    ]
    for view in views:
        print(f"  • {view}")
    
    # Functions Available
    print("\n⚙️  FUNCTIONS AVAILABLE")
    print("-"*70)
    functions = [
        'get_import_status() - Get import status for all sources',
        'check_duplicate_node_ids() - Check for duplicate node IDs',
        'run_full_validation() - Run full validation report',
        'refresh_inventory_counts() - Refresh actual record counts'
    ]
    for func in functions:
        print(f"  • {func}")
    
    print("\n" + "="*70)
    print("ICIJ import is running in background with 6 parallel workers.")
    print("ETA: 2-3 hours for full completion.")
    print("="*70)
    
    conn.close()

if __name__ == "__main__":
    generate_report()
