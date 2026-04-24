# Data Collection Procedures

> **Last Updated:** April 24, 2026
> **Purpose:** Step-by-step procedures for collecting data from all sources

---

## 📋 Standard Data Collection Workflow

### Before Starting Any Collection

1. **Read** `docs/DATA_INVENTORY_FULL.md` - Check what's already collected
2. **Verify** the source is not already ingested (check PostgreSQL tables)
3. **Check** `docs/agents/INGESTION_GUIDES/` for source-specific procedures
4. **Review** `scripts/config.py` - Understand path configuration

### Standard Collection Steps

```bash
# 1. Check current inventory
python scripts/ingestion/check_inventory.py

# 2. Verify source availability
python scripts/ingestion/check_gov_data_status.py

# 3. Run collection (example: Congress data)
python scripts/download/download_congress_historical.py --congress 105

# 4. Verify downloaded files
ls -la /home/cbwinslow/workspace/epstein-data/raw-files/

# 5. Update inventory
vim docs/DATA_INVENTORY_FULL.md
# Add record count, date, status
```

---

## 📁 Source-Specific Procedures

### 1. DOJ Epstein Library

**Script:** `epstein-ripper/auto_ep_rip.py`
**Output:** `/home/cbwinslow/workspace/epstein-data/raw-files/data{1-12}/`
**Status:** ✅ Complete (1.4M docs)

```bash
cd epstein-ripper
python auto_ep_rip.py --dataset 1  # Downloads dataset 1
python auto_ep_rip.py --dataset 2  # Downloads dataset 2
# ... up to dataset 12
```

**Verification:**
```bash
ls /home/cbwinslow/workspace/epstein-data/raw-files/data1/ | wc -l
# Should show ~260,000 PDFs
```

---

### 2. jMail World Emails

**Scripts:** `scripts/import/import_jmail_*.py`
**Output:** PostgreSQL `jmail_emails_full`, `jmail_documents`
**Status:** ✅ Complete (1.78M emails)

```bash
# Download (if needed)
python scripts/download/download_hf_resume.py --dataset jmail_emails

# Import to PostgreSQL
python scripts/import/import_jmail_full.py
python scripts/import/import_jmail_documents.py
```

**Verification:**
```sql
SELECT COUNT(*) FROM jmail_emails_full;
-- Should return: 1,783,792
```

---

### 3. GovInfo Bulk Data

**Scripts:** `scripts/download/download_govinfo_bulk.py`
**Output:** `/home/cbwinslow/workspace/epstein-data/raw-files/govinfo_bulk/`
**Status:** ✅ Complete (246 files)

```bash
# Download Federal Register bulk (yearly ZIPs)
python scripts/download/download_govinfo_bulk.py --type FR --year 2024

# Download Bill Status bulk (by congress, bill type)
python scripts/download/download_govinfo_bulk.py --type BILLSTATUS --congress 119 --type HR

# Import to PostgreSQL
python scripts/import/import_govinfo_bulk.py --type FR
```

**Verification:**
```sql
SELECT COUNT(*) FROM federal_register_entries;
-- Should return: 737,940
```

---

### 4. Congress.gov Historical

**Script:** `scripts/download/download_congress_historical.py`
**Output:** `/home/cbwinslow/workspace/epstein-data/raw-files/congress_historical/`
**Status:** ✅ Complete (105th-119th)

```bash
# Download by congress number
python scripts/download/download_congress_historical.py --congress 105
python scripts/download/download_congress_historical.py --congress 106
# ... up to 119

# Import to PostgreSQL
python scripts/import/import_congress.py --congress 119
```

**Verification:**
```sql
SELECT COUNT(*) FROM congress_bills;
-- Should return: 368,651 (105th-119th)
```

---

### 5. Senate Vote Details (🚨 OPEN Issue #58)

**Script:** `scripts/download/download_senate_vote_details.py`
**Status:** 🔴 403 errors from senate.gov

```bash
# Try with retry logic
python scripts/download/download_senate_vote_details.py --retry --delay 2.0

# Alternative: Check if files already exist
ls /home/cbwinslow/workspace/epstein-data/raw-files/senate_votes/ 2>/dev/null || echo "Need to download"

# If 403 persists, document in issue and move to alternate source
```

**Next Action:** Fix 403 errors, try alternate user agents or headers

---

### 6. SEC EDGAR Bulk (🚨 OPEN Issue #55)

**Script:** `scripts/download/download_sec_edgar_recent.py`
**Status:** 🔴 Needs bulk run

```bash
# Download Form 4, 13F data
python scripts/download/download_sec_edgar_recent.py --form 4 --years 2020-2026
python scripts/download/download_sec_edgar_recent.py --form 13F --years 2020-2026
```

**Next Action:** Run bulk import, verify financial linkage data

---

## 🔧 Repeatable Collection Script

Create a wrapper script for full collection:

```bash
# File: scripts/run_all_downloads.sh
#!/bin/bash
# Run all downloads in sequence

echo "Starting full data collection..."

# 1. DOJ (already complete, skip)
echo "✅ DOJ Epstein Library - Complete"

# 2. Congress historical
for congress in {105..119}; do
    echo "Downloading Congress $congress..."
    python scripts/download/download_congress_historical.py --congress $congress
done

# 3. GovInfo bulk
for year in {2000..2024}; do
    echo "Downloading Federal Register $year..."
    python scripts/download/download_govinfo_bulk.py --type FR --year $year
done

echo "Collection complete!"
```

---

## 📝 Notes for AI Agents

- **Always** check `docs/DATA_INVENTORY_FULL.md` before starting
- **Verify** data isn't already ingested (check PostgreSQL)
- **Use** `scripts/config.py` for all paths (never hardcode)
- **Document** any new sources in `docs/agents/INGESTION_GUIDES/`
- **Update** inventory after each collection

---

*Last Updated: April 24, 2026*
*Status: Ready for Use*
