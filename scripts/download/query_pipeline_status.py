#!/usr/bin/env python3
import config

conn = config.get_db_connection()
cur = conn.cursor()

print("=" * 80)
print("DATA PIPELINE TRACKING STATUS")
print("=" * 80)

# Query all datasets
cur.execute("""
    SELECT
        source_name,
        source_type,
        download_status,
        ingestion_status,
        target_table,
        records_imported,
        priority,
        notes
    FROM data_pipeline_tracking
    ORDER BY
        CASE priority
            WHEN 'high' THEN 1
            WHEN 'medium' THEN 2
            WHEN 'low' THEN 3
        END,
        download_status,
        ingestion_status
""")

print(
    f"\n{'Source Name':<35} {'Type':<12} {'Download':<12} {'Ingest':<12} {'Records':>12} {'Priority':<8}"
)
print("-" * 100)

for row in cur.fetchall():
    (
        source_name,
        source_type,
        download_status,
        ingestion_status,
        target_table,
        records_imported,
        priority,
        notes,
    ) = row
    print(
        f"{source_name:<35} {source_type:<12} {download_status:<12} {ingestion_status:<12} {records_imported:>12,} {priority:<8}"
    )
    if notes:
        print(f"  └─ {notes}")

# Summary
cur.execute("""
    SELECT download_status, ingestion_status, COUNT(*) as count
    FROM data_pipeline_tracking
    GROUP BY download_status, ingestion_status
    ORDER BY download_status, ingestion_status
""")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
for row in cur.fetchall():
    print(f"{row[0]:15} / {row[1]:15}: {row[2]} datasets")

# Total records
cur.execute("""
    SELECT SUM(records_imported) as total
    FROM data_pipeline_tracking
    WHERE ingestion_status = 'completed'
""")
total_records = cur.fetchone()[0]
print(f"\nTotal records imported: {total_records:,}")

conn.close()
