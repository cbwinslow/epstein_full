# JMail Emails Import Guide - Reproduction Steps
=========================================

**Last Updated:** April 25, 2026
**Purpose:** Step-by-step guide to reproduce the jmail_emails table setup

---

## 🔴️ Original Problem

### Issue Identified
- **Original Schema:** `jmail_emails` table used `id INTEGER PRIMARY KEY` with a sequence
- **Source Data:** Parquet file uses **string hash IDs** (not integers)
- **Result:** Only **1,596,220 rows** were loaded (with wrong integer IDs)
- **Expected:** **1,783,792 rows** with correct string hash IDs

### Root Cause
```sql
-- WRONG schema (original)
CREATE TABLE jmail_emails (
    id INTEGER PRIMARY KEY,  -- ❌ This doesn't match parquet's string IDs!
    ...
);
```

The parquet file (`emails-slim.parquet`) uses string hash IDs like `abc123def456...`, which can't be stored in an INTEGER column properly.

---

## ✅ Solution Implemented

### Correct Schema
```sql
-- CORRECT schema (fixed)
CREATE TABLE IF NOT EXISTS jmail_emails (
    id TEXT PRIMARY KEY,  -- ✅ Matches parquet's string hash IDs
    doc_id TEXT,
    message_index TEXT,
    sender TEXT,
    subject TEXT,`
    to_recipients JSONB DEFAULT '[]',`
    cc_recipients JSONB DEFAULT '[]',`
    bcc_recipients JSONB DEFAULT '[]',`
    sent_at TIMESTAMPTZ,`
    attachments INT DEFAULT 0,`
    account_email TEXT,`
    email_drop_id TEXT,`
    folder_path TEXT,`
    is_promotional BOOLEAN DEFAULT FALSE,`
    release_batch INT,`
    epstein_is_sender BOOLEAN DEFAULT FALSE,`
    all_participants TEXT,`
    created_at TIMESTAMPTZ DEFAULT NOW()`
);
```

### Key Changes
1. **`id TEXT PRIMARY KEY`** - Changed from INTEGER to TEXT to match parquet's string hash IDs
2. **JSONB columns** - Properly defined for JSON arrays (to_recipients, cc_recipients, bcc_recipients)
3. **Timestamp handling** - TIMESTAMPTZ for proper timezone support
4. **Default values** - Proper defaults for JSONB and BOOLEAN columns

---

## 📂 Reproduction Steps

### Prerequisites
```bash
# 1. Ensure PostgreSQL is running
psql -U cbwinslow -h localhost -d epstein -c "SELECT 1"

# 2. Verify parquet file exists
ls -lh /home/cbwinslow/workspace/epstein-data/supplementary/emails-slim.parquet
# Expected: ~334 MB, 1,783,792 rows

# 3. Check Python dependencies
python3 -c "import psycopg2, pandas, pyarrow; print('Dependencies OK')"
```

### Step 1: Create Table with Correct Schema
```bash
cd /home/cbwinslow/workspace/epstein
python3 scripts/import/import_jmail_emails_final.py --create-table
```

Expected output:
```
Setting up database...
Creating jmail_emails table with correct schema...
Table created (or already exists).
Indexes created (or already exist).
```

### Step 2: Verify Table Schema
```bash
psql -U cbwinslow -d epstein -c "\d jmail_emails"
```

Expected output should show:
```
id          | text                     | not null`
...
```

### Step 3: Import All Data
```bash
cd /home/cbwinslow/workspace/epstein
python3 scripts/import/import_jmail_emails_final.py
```

Expected output:
```
Setting up database...
Creating jmail_emails table with correct schema...
Table created (or already exists).
Existing rows: 0
Loading /home/cbwinslow/workspace/epstein-data/supplementary/emails-slim.parquet...
Parquet rows: 1,783,792
New rows to insert: 1,783,792 (skipped 0 existing)

Importing 1,783,792 emails (batch_size=5000)...
  Progress: 100,000/1,783,792 (5.6%) inserted=100,000 skipped=0 errors=0 (410 rows/s)
  ...
  Progress: 1,783,792/1,783,792 (100.0%) inserted=1,783,792 skipped=0 errors=0 (...)
Done! Inserted: 1,783,792, Skipped: 0, Errors: 0

=== Import Summary ===
Total emails: 1,783,792
Expected: 1,783,792
Completeness: 100.0%
...
```

### Step 4: Verify Import
```bash
psql -U cbwinslow -d epstein -c "SELECT COUNT(*) FROM jmail_emails;"
# Expected: 1,783,792

# Check sample IDs (should be string hashes, not integers)
psql -U cbwinslow -d epstein -c "SELECT id FROM jmail_emails LIMIT 5;"
# Expected: String hashes like "a1b2c3d4...", not integers like "1", "2", etc.
```

---

## 🔧 Fixes Applied to Import Script

### Bug #1: psycopg2.extras.executemany (Fixed)
**Original (broken):**
```python
psycopg2.extras.executemany(cur, INSERT_SQL, batch_data)  # ❌ Module not available
```

**Fixed:**
```python
cur.executemany(INSERT_SQL, batch_data)  # ✅ Correct method
```

### Bug #2: ON CONFLICT Typo (Fixed)
**Original (broken):**
```sql
ON CONFLICT (id) DO NOTHING  -- ❌ Typo in keyword
```

**Fixed:**
```sql
ON CONFLICT (id) DO NOTHING  -- ✅ Correct PostgreSQL syntax
```

### Bug #3: INSERT Statement Placeholder Count (Fixed)
**Original (broken):**
```python
INSERT_SQL = """
INSERT INTO jmail_emails (...) VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  # ❌ Only 15 placeholders
)
"""
# But we have 17 columns!
```

**Fixed:**
```python
INSERT_SQL = """
INSERT INTO jmail_emails (...) VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s,
    %s, %s  # ✅ Now 17 placeholders for 17 columns
)
"""
```

---

## 📊 Data Cleaning Rules

### Invalid JSON Handling
```python
def safe_json(val):
    """Convert value to valid JSON string safely."""
    if pd.isna(val) or val is None:
        return '[]'  # Default to empty array

    if isinstance(val, list):
        return json.dumps(val)

    if isinstance(val, str):
        try:
            json.loads(val)  # Validate it's valid JSON
            return val
        except (json.JSONDecodeError, ValueError):
            return '[]'  # Invalid JSON → empty array
    return '[]'
```

**Examples of invalid data fixed:**
- `[Redacted], Jeffrey Epstein <jeevacation@gmail.com>` → `[]` (not valid JSON)
- `NaN` → `[]` (missing value)
- Valid JSON array → kept as-is

### Timestamp Validation
```python
def parse_timestamp(val):
    """Parse timestamp, filtering out obviously wrong dates."""
    if pd.isna(val):
        return None

    try:
        if isinstance(val, str):
            # Quick sanity check on year
            if len(val) >= 4:
                year_str = val[:4]
                if year_str.isdigit():
                    year = int(year_str)
                    if year < 1990 or year > 2030:
                        return None  # Filter out invalid years
            dt = pd.to_datetime(val, utc=True, errors='coerce')
            if pd.isna(dt):
                return None
            return dt.to_pydatetime()
        return None
    except Exception:
        return None
```

**Examples of timestamps filtered:**
- Years < 1990 → NULL (before Epstein's activity)
- Years > 2030 → NULL (future dates)
- Valid timestamps → kept as-is

---

## 📈 Indexes Created

```sql
CREATE INDEX IF NOT EXISTS idx_jmail_emails_sent ON jmail_emails(sent_at);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_sender ON jmail_emails(sender);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_account ON jmail_emails(account_email);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_promo ON jmail_emails(is_promotional);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_doc ON jmail_emails(doc_id);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_drop ON jmail_emails(email_drop_id);
CREATE INDEX IF NOT EXISTS idx_jmail_emails_epstein ON jmail_emails(epstein_is_sender);
```

---

## 📋 Backup Information

### Original Broken Table
```sql
-- Backup of original (wrong schema, integer IDs)
CREATE TABLE jmail_emails_backup AS SELECT * FROM jmail_emails;
-- Row count: 1,596,220 (with wrong integer IDs)
```

To restore from backup (if needed):
```sql
DROP TABLE IF EXISTS jmail_emails;
ALTER TABLE jmail_emails_backup RENAME TO jmail_emails;
```

**Note:** The backup has wrong schema (INTEGER id), don't use it for the correct import!

---

## 📌 Verification Queries

### Check Final Count
```sql
SELECT COUNT(*) FROM jmail_emails;
-- Expected: 1,783,792
```

### Check ID Format (Should be String Hashes)
```sql
SELECT id, LENGTH(id) FROM jmail_emails LIMIT 10;
-- Expected: String IDs with length > 10 characters
```

### Check Data Sources
```sql
SELECT email_drop_id, COUNT(*) as cnt
FROM jmail_emails
GROUP BY email_drop_id
ORDER BY cnt DESC;
```

Expected sources:
- VOL00009-12: DOJ EFTA document emails (~1.75M)
- yahoo_2: Epstein's personal Yahoo inbox (~17K)
- House Oversight: Congressional releases (~8K)
- Ehud Barak: Former Israeli PM emails (~1K)

### Check Epstein as Sender
```sql
SELECT epstein_is_sender, COUNT(*) as cnt
FROM jmail_emails
GROUP BY epstein_is_sender;
-- Expected: Mix of TRUE and FALSE
```

### Check Date Range
```sql
SELECT
    MIN(sent_at) as earliest,
    MAX(sent_at) as latest
FROM jmail_emails
WHERE sent_at IS NOT NULL;
-- Expected: ~1990s to ~2020s
```

---

## 📎 Script Location

**Primary Script:** `/home/cbwinslow/workspace/epstein/scripts/import/import_jmail_emails_final.py`

**Features:**
- ✅ Correct schema creation (TEXT id)
- ✅ Data cleaning (invalid JSON, timestamp validation)
- ✅ Batch insert with conflict handling
- ✅ Progress tracking with row/s rate
- ✅ Summary statistics after import
- ✅ Resume capability (skips existing IDs)

**Usage:**
```bash
# Create table
python3 scripts/import/import_jmail_emails_final.py --create-table

# Import all data
python3 scripts/import/import_jmail_emails_final.py

# Verify only
python3 scripts/import/import_jmail_emails_final.py --verify

# Dry run (check what would be imported)
python3 scripts/import/import_jmail_emails_final.py --dry-run
```

---

## 📍 Related Files

### Data
- **Source Parquet:** `/home/cbwinslow/workspace/epstein-data/supplementary/emails-slim.parquet` (334 MB)
- **Backup Table:** `jmail_emails_backup` (original broken table, 1,596,220 rows)

### Scripts
- **Main Import:** `/home/cbwinslow/workspace/epstein/scripts/import/import_jmail_emails_final.py`
- **Old Broken Import:** `/home/cbwinslow/workspace/epstein/scripts/import/import_jmail_emails.py` (don't use)

### Documentation
- **This Guide:** `/home/cbwinslow/workspace/epstein/docs/JMAIL_IMPORT_GUIDE.md`
- **Data Inventory:** `/home/cbwinslow/workspace/epstein/docs/DATA_INVENTORY_FULL.md`

---

## 📏 Next Steps After Import

1. ✅ **Verify row count:** 1,783,792 rows
2. ✅ **Verify ID format:** String hashes (not integers)
3. ✅ **Verify data integrity:** JSON columns valid, timestamps in range
4. 🔴 **Import related tables:**
   - `jmail_documents` (51,728 records from `jmail_documents.parquet`)
   - `jmail_photos` (pending - 403 errors from source)
   - `jmail_imessages` (pending - 403 errors from source)

---

*Created: April 25, 2026  *
*Author: cbwinslow*
*Status: ✅ Import script fixed and running*
