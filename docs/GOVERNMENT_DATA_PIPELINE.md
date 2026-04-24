# Government Data Pipeline
**Last Updated:** April 24, 2026

## Purpose
Operational runbook for repeatable ingestion of Congress.gov and GovInfo.gov data, with validation and resumable execution.

## Current Baseline (Revalidated 2026-04-24 UTC)
- `congress_bills`: 368,651 (105th-119th)
- `congress_members`: 10,413 (105th-119th)
- `congress_house_votes`: 2,738 (117th-119th)
- `congress_house_vote_details`: 2,738
- `congress_house_member_votes`: 1,185,626
- `congress_senate_votes`: 3,132 (106th-119th, partial)
- `congress_senate_member_votes`: 313,176
- `congress_bill_text_versions`: 130,361
- `congress_bill_vote_references`: 11,546
- `congress_bill_summaries`: 279,065
- `congress_bill_actions`: 875,816
- `congress_bill_cosponsors`: 2,064,763
- `federal_register_entries`: 737,940 (2000-01-03..2024-12-31)
- `court_opinions`: 31,544
- `govinfo_packages`: 94,741
- `govinfo_bulk_import_status`: 246 completed
- `fara_registrations`: 7,045
- `fara_foreign_principals`: 17,358
- `fara_short_forms`: 44,413
- `fara_registrant_docs`: 124,224
- `sec_insider_transactions`: 139

## Pipelines

### Congress.gov Historical
- Downloader: `scripts/ingestion/download_congress_historical.py`
- Importer: `scripts/ingestion/import_congress.py`
- Supported components:
  - `bills`
  - `members`
  - `votes` (house vote list)
- Key endpoints:
  - `/bill/{congress}`
  - `/member/congress/{congress}`
  - `/house-vote/{congress}` (list-level)
  - `/house-vote/{congress}/{session}/{roll}` (detail-level)

### Congress House Vote Detail Backfill
- Downloader/importer: `scripts/ingestion/download_house_vote_details.py`
- Idempotency key:
  - `congress_house_vote_details`: `(congress, session, roll_call_number)`
  - `congress_house_member_votes`: `(congress, session, roll_call_number, bioguide_id)`
- Notes:
  - Fetches detail JSON from Congress API and member roll calls from Clerk XML (`sourceDataURL`).
  - Script handles schema migration for legacy pre-session uniqueness constraints.

### GovInfo Bulk
- Downloader: `scripts/ingestion/download_govinfo_bulk.py`
- Importers:
  - `scripts/ingestion/import_govinfo_fr_bulk.py`
  - `scripts/ingestion/import_govinfo_bills_bulk.py`
  - `scripts/ingestion/import_govinfo_billsum_bulk.py`
  - `scripts/ingestion/import_govinfo_billstatus_bulk.py`
- Bulk datasets:
  - `FR`
  - `BILLS`
  - `BILLSUM`
  - `BILLSTATUS`

### Senate Vote Details
- Downloader/importer: `scripts/ingestion/download_senate_vote_details.py`
- Source:
  - `https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_{congress}_{session}.xml`
  - `https://www.senate.gov/legislative/LIS/roll_call_votes/vote{congress}{session}/vote_{congress}_{session}_{vote:05d}.xml`
- Normalized tables:
  - `congress_senate_votes` (unique `(congress, session, vote_number)`)
  - `congress_senate_member_votes` (unique `(congress, session, vote_number, member_key)`)
- Operational note:
  - Endpoint currently has intermittent/host-specific HTTP 403 responses; rerun/backfill loop is required.

### FARA Bulk
- Downloader: `scripts/ingestion/download_fara_bulk.py`
- Importer: `scripts/ingestion/import_fara.py`
- Normalized tables:
  - `fara_registrations`
  - `fara_foreign_principals`
  - `fara_short_forms`
  - `fara_registrant_docs`

## Repeatable Execution Pattern

### 1. Download
```bash
python scripts/ingestion/download_congress_historical.py --congresses 106-119 --components bills,members,votes --workers 16 --import-after-download
python scripts/ingestion/download_govinfo_bulk.py --dataset all --years 2000-2024 --congresses 108-119 --workers 6
python scripts/ingestion/download_fara_bulk.py
```

### 2. Import
```bash
python scripts/ingestion/import_congress.py
python scripts/ingestion/download_house_vote_details.py --limit 1000000 --concurrency 40
python scripts/ingestion/download_senate_vote_details.py --congresses 106-119 --sessions 1,2 --concurrency 30 --rate-delay 0.08 --max-retries 6
python scripts/ingestion/import_govinfo_fr_bulk.py --workers 6
python scripts/ingestion/import_govinfo_bills_bulk.py --workers 6
python scripts/ingestion/import_govinfo_billsum_bulk.py --workers 6
python scripts/ingestion/import_govinfo_billstatus_bulk.py --workers 6
python scripts/ingestion/import_fara.py --batch-size 5000
```

### 3. Validate
```bash
PGPASSWORD=123qweasd psql -h localhost -U cbwinslow -d epstein -At -c "
SELECT 'congress_bills|'||count(*)||'|'||min(congress)||'|'||max(congress) FROM congress_bills
UNION ALL SELECT 'congress_members|'||count(*)||'|'||min(congress_number)||'|'||max(congress_number) FROM congress_members
UNION ALL SELECT 'congress_house_votes|'||count(*)||'|'||min(congress)||'|'||max(congress) FROM congress_house_votes
UNION ALL SELECT 'congress_house_vote_details|'||count(*)||'|'||min(congress)||'|'||max(congress) FROM congress_house_vote_details
UNION ALL SELECT 'congress_house_member_votes|'||count(*)||'|'||min(congress)||'|'||max(congress) FROM congress_house_member_votes
UNION ALL SELECT 'pending_vote_details|'||count(*)
  FROM congress_house_votes v
  LEFT JOIN congress_house_vote_details d
    ON d.congress=v.congress AND d.session=v.session_number AND d.roll_call_number=v.roll_call_number
  WHERE d.id IS NULL
UNION ALL SELECT 'congress_bill_text_versions|'||count(*)||'|'||min(congress)||'|'||max(congress) FROM congress_bill_text_versions
UNION ALL SELECT 'federal_register_entries|'||count(*)||'|'||min(date_published)||'|'||max(date_published) FROM federal_register_entries;
"
```

## Gap Matrix (Next Work)

### Required for “2000+ complete congressional legislative pipeline”
1. Resolve Senate source 403 blocks and complete backfill reruns for failed vote detail rows.
2. Expand SEC EDGAR beyond recent feed to historical Form 4 / 13F archives.
3. Optional pre-105th congressional expansion (API-key path + alternate handling).

## Tracking Protocol
- Update these after every meaningful run:
  - `TASKS.md`
  - `CONTEXT.md`
  - `AGENTS.md`
  - `docs/GOV_DATA_INGESTION_SUMMARY.md`
- Add/update GitHub comments on:
  - `#51` Congress completion (106th/119th/vote details)
  - `#52` GovInfo expansion beyond current baseline
  - `#55` SEC EDGAR
  - `#57` FARA

## Related Docs
- `docs/GOV_DATA_INGESTION_SUMMARY.md`
- `docs/DATA_INVENTORY_FULL.md`
- `docs/SESSION_LOGS/government_data_ingestion_20260423.md`
- `docs/SESSION_LOGS/government_data_ingestion_20260424.md`
- `/home/cbwinslow/workspace/epstein/logs/ingestion/congress_historical_20260424_131710.log`
- `/home/cbwinslow/workspace/epstein/logs/ingestion/house_vote_details_20260424_131136.log`
