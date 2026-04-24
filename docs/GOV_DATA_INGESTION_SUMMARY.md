# Government Data Ingestion Summary
**Finalized:** April 24, 2026
**Re-verified:** April 24, 2026

## Overview
Government historical ingestion remains active and repeatable for currently scoped sources (GovInfo, Congress, White House Visitor Logs, and FEC historical contributions), with parallel refresh runs completed on April 24, 2026 UTC.

## Final Verified State

### Core Tables
- `federal_register_entries`: 737,940 (`2000-01-03` to `2024-12-31`)
- `congress_bills`: 368,651 (105th-119th)
- `congress_members`: 10,413 (105th-119th)
- `congress_house_votes`: 2,738 (117th-119th)
- `congress_house_vote_details`: 2,738
- `congress_house_member_votes`: 1,185,626
- `congress_senate_votes`: 3,132 (106th-119th, partial)
- `congress_senate_member_votes`: 313,176 (partial)
- `congress_bill_text_versions`: 130,361
- `congress_bill_summaries`: 279,065
- `congress_bill_actions`: 875,816
- `congress_bill_cosponsors`: 2,064,763
- `govinfo_packages`: 94,741
- `court_opinions`: 31,544
- `whitehouse_visitors`: 2,544,984 (2009-2024)
- `fec_individual_contributions`: 447,189,732 (cycles 2000-2026)
- `sec_insider_transactions`: 139

### GovInfo Bulk Import Completion
- `BILLS`: 96 completed
- `BILLSTATUS`: 52 completed
- `BILLSUM`: 48 completed
- `FR`: 26 completed
- Total completed files in `govinfo_bulk_import_status`: 246

## Historical Coverage Snapshot

### Congress.gov
- Production historical backfill now covers bills/members for 105th through 119th Congress.
- House vote list + vote-detail backfill is complete through currently ingested vote rows (`pending_vote_details=0`).
- Current remaining Congress gaps:
  - Senate vote-detail pipeline exists and is ingesting, but retries/backfill are still needed due intermittent upstream HTTP 403 responses.
- Correct historical endpoints are:
  - `/bill/{congress}`
  - `/member/congress/{congress}`
  - `/house-vote/{congress}/{session}/{roll}` (vote detail)
- House vote list ingestion is wired into `congress_house_votes` where available from the official endpoint.

### GovInfo.gov
- Historical API and bulk paths are both operationalized.
- Bulk ZIP ingestion pipelines are in place for:
  - `FR`
  - `BILLS`
  - `BILLSTATUS`
  - `BILLSUM`
- Importers are hardened for malformed XML and corrupt ZIP recovery.

### White House Visitor Logs
- Integrated public archive datasets for:
  - Obama administration (2009-2017)
  - Biden administration (2021-2024)
- Pre-2009 White House logs are not publicly disclosed through the same channel.

### FEC.gov
- Historical contribution coverage is already present for 2000-2026.
- No historical re-download is required unless source-parity validation is requested.

## Script Entry Points
- `scripts/ingestion/download_congress_historical.py`
- `scripts/ingestion/import_congress.py`
- `scripts/ingestion/download_govinfo_historical.py`
- `scripts/ingestion/download_govinfo_bulk.py`
- `scripts/ingestion/import_govinfo.py`
- `scripts/ingestion/import_govinfo_billstatus_bulk.py`
- `scripts/ingestion/import_govinfo_bills_bulk.py`
- `scripts/ingestion/import_govinfo_billsum_bulk.py`
- `scripts/ingestion/import_govinfo_fr_bulk.py`
- `scripts/ingestion/download_whitehouse.py`
- `scripts/ingestion/import_whitehouse_visitors.py`

## Runtime Status (April 24, 2026)
- Active high-concurrency refresh + normalization runs were launched on April 24, 2026 UTC.
- FARA full bulk normalization run is active (see latest `import_fara_*.log`).
- Latest completion logs:
  - `/home/cbwinslow/workspace/epstein/logs/ingestion/congress_historical_20260424_153208.log`
  - `/home/cbwinslow/workspace/epstein/logs/ingestion/senate_vote_details_20260424_153208.log`
  - `/home/cbwinslow/workspace/epstein/logs/ingestion/import_govinfo_bills_bulk_20260424_153620.log`
  - `/home/cbwinslow/workspace/epstein/logs/ingestion/import_fara_20260424_153802.log`

## Remaining Gaps / Optional Expansion
1. Pre-105th Congress ingestion (requires Congress.gov API-key path and alternate handling).
2. Senate vote-detail retry/backfill completion after source 403 mitigation.
3. Pre-2009 White House visitor data (public disclosure limitation).
4. SEC EDGAR expansion for financial linkage analysis.
5. FARA full-run completion and reconciliation of final counts.
