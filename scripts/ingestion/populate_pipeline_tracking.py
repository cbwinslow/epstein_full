#!/usr/bin/env python3
"""Scan filesystem and populate data_pipeline_tracking table with current state"""
import os
from pathlib import Path
from datetime import datetime
import config

DATA_ROOT = Path("/home/cbwinslow/workspace/epstein-data")

conn = config.get_db_connection()
cur = conn.cursor()

# Define known datasets to track
datasets = [
    {
        "source_name": "DOJ EFTA Documents",
        "source_type": "legal",
        "source_url": "https://www.justice.gov/doj/fbi/epstein-case",
        "download_path": str(DATA_ROOT / "raw-files"),
        "target_table": "documents",
        "description": "DOJ EFTA documents (1.3M PDF files)",
        "priority": "high",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 1397821,
        "download_files_count": 1313861
    },
    {
        "source_name": "Congress.gov Members",
        "source_type": "government",
        "source_url": "https://www.congress.gov",
        "download_path": str(DATA_ROOT / "raw-files/congress"),
        "target_table": "congress_members",
        "description": "Congressional member data (118th Congress)",
        "priority": "medium",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 2691
    },
    {
        "source_name": "Congress.gov Bills",
        "source_type": "government",
        "source_url": "https://www.congress.gov",
        "download_path": str(DATA_ROOT / "raw-files/congress"),
        "target_table": "congress_bills",
        "description": "Congressional bills",
        "priority": "medium",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 18415
    },
    {
        "source_name": "FEC Candidates",
        "source_type": "government",
        "source_url": "https://www.fec.gov",
        "download_path": str(DATA_ROOT / "raw-files/fec"),
        "target_table": "fec_candidates",
        "description": "FEC candidate records (2020, 2022, 2024)",
        "priority": "medium",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 11989
    },
    {
        "source_name": "FEC Committees",
        "source_type": "government",
        "source_url": "https://www.fec.gov",
        "download_path": str(DATA_ROOT / "raw-files/fec"),
        "target_table": "fec_committees",
        "description": "FEC committee records (2020, 2022, 2024)",
        "priority": "medium",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 59021
    },
    {
        "source_name": "FEC Individual Contributions",
        "source_type": "government",
        "source_url": "https://www.fec.gov/data",
        "download_path": str(DATA_ROOT / "raw-files/fec/indiv24.zip"),
        "target_table": "fec_individual_contributions",
        "description": "FEC individual contributions (90M estimated records)",
        "priority": "high",
        "download_status": "completed",
        "ingestion_status": "in_progress",
        "download_size_bytes": 4244259029,
        "notes": "Large dataset (4.2GB compressed), import running in background"
    },
    {
        "source_name": "GovInfo.gov Packages",
        "source_type": "government",
        "source_url": "https://www.govinfo.gov",
        "download_path": str(DATA_ROOT / "raw-files/govinfo"),
        "target_table": "govinfo_packages",
        "description": "GovInfo.gov packages (bills, reports, opinions)",
        "priority": "medium",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 53618
    },
    {
        "source_name": "ICIJ Offshore Leaks",
        "source_type": "financial",
        "source_url": "https://offshoreleaks-data.icij.org",
        "download_path": str(DATA_ROOT / "downloads/icij_extracted"),
        "target_table": "icij_entities",
        "description": "ICIJ Offshore Leaks database (Panama Papers, Paradise Papers, etc.)",
        "priority": "high",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 5355790
    },
    {
        "source_name": "House Financial Disclosures",
        "source_type": "government",
        "source_url": "https://disclosures-clerk.house.gov",
        "download_path": str(DATA_ROOT / "raw-files/house_fd"),
        "target_table": "house_financial_disclosures",
        "description": "House Financial Disclosures (2008-2024)",
        "priority": "high",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 37281
    },
    {
        "source_name": "Senate Financial Disclosures",
        "source_type": "government",
        "source_url": "https://efdsearch.senate.gov",
        "download_path": str(DATA_ROOT / "raw-files/senate_fd"),
        "target_table": "senate_financial_disclosures",
        "description": "Senate Financial Disclosures",
        "priority": "high",
        "download_status": "pending",
        "ingestion_status": "pending",
        "notes": "DNS resolution error for efts.senate.gov"
    },
    {
        "source_name": "Senate LDA Lobbying",
        "source_type": "government",
        "source_url": "https://lda.senate.gov",
        "download_path": str(DATA_ROOT / "raw-files/lobbying"),
        "target_table": "lobbying_registrations",
        "description": "Senate Lobbying Disclosure Act registrations and reports",
        "priority": "medium",
        "download_status": "pending",
        "ingestion_status": "pending",
        "notes": "Tables don't exist yet, not downloaded"
    },
    {
        "source_name": "FARA Registrations",
        "source_type": "government",
        "source_url": "https://www.fara.gov",
        "download_path": str(DATA_ROOT / "raw-files/fara"),
        "target_table": "fara_registrations",
        "description": "Foreign Agents Registration Act data",
        "priority": "medium",
        "download_status": "pending",
        "ingestion_status": "pending",
        "notes": "DOJ connection error during download attempt"
    },
    {
        "source_name": "White House Visitor Logs",
        "source_type": "government",
        "source_url": "https://www.whitehouse.gov",
        "download_path": str(DATA_ROOT / "raw-files/whitehouse"),
        "target_table": "whitehouse_visitors",
        "description": "White House visitor access records",
        "priority": "low",
        "download_status": "pending",
        "ingestion_status": "pending",
        "notes": "404 errors - CSV files not found on website"
    },
    {
        "source_name": "USA Spending Awards",
        "source_type": "government",
        "source_url": "https://www.usaspending.gov",
        "download_path": str(DATA_ROOT / "raw-files/usa_spending"),
        "target_table": "usa_spending_awards",
        "description": "USA Spending federal awards data",
        "priority": "medium",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 100,
        "notes": "Sample data only (2 JSON files)"
    },
    {
        "source_name": "jmail.world Emails",
        "source_type": "research",
        "source_url": "https://data.jmail.world",
        "download_path": str(DATA_ROOT / "downloads"),
        "target_table": "jmail_emails",
        "description": "jmail.world email dataset (1.78M emails)",
        "priority": "high",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 1783792
    },
    {
        "source_name": "jmail.world Documents",
        "source_type": "research",
        "source_url": "https://data.jmail.world",
        "download_path": str(DATA_ROOT / "downloads"),
        "target_table": "jmail_documents",
        "description": "jmail.world document metadata (1.41M documents)",
        "priority": "high",
        "download_status": "completed",
        "ingestion_status": "completed",
        "records_imported": 1413417
    },
    {
        "source_name": "SEC Insider Transactions",
        "source_type": "financial",
        "source_url": "https://www.sec.gov",
        "download_path": str(DATA_ROOT / "raw-files/sec"),
        "target_table": "sec_insider_transactions",
        "description": "SEC EDGAR insider trading data",
        "priority": "medium",
        "download_status": "pending",
        "ingestion_status": "pending",
        "notes": "Schema exists, data not downloaded"
    }
]

# Insert datasets into tracking table
for dataset in datasets:
    cur.execute("""
        INSERT INTO data_pipeline_tracking (
            source_name, source_type, source_url, download_status, ingestion_status,
            download_path, target_table, description, priority, records_imported,
            download_size_bytes, download_files_count, notes, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """, (
        dataset["source_name"],
        dataset["source_type"],
        dataset["source_url"],
        dataset["download_status"],
        dataset["ingestion_status"],
        dataset["download_path"],
        dataset["target_table"],
        dataset["description"],
        dataset["priority"],
        dataset.get("records_imported", 0),
        dataset.get("download_size_bytes"),
        dataset.get("download_files_count"),
        dataset.get("notes", "")
    ))

conn.commit()
print(f"Populated {len(datasets)} datasets into data_pipeline_tracking table")

# Summary query
cur.execute("""
    SELECT download_status, ingestion_status, COUNT(*) as count
    FROM data_pipeline_tracking
    GROUP BY download_status, ingestion_status
    ORDER BY download_status, ingestion_status
""")

print("\nPipeline Status Summary:")
print("=" * 60)
for row in cur.fetchall():
    print(f"{row[0]:15} / {row[1]:15}: {row[2]} datasets")

conn.close()
