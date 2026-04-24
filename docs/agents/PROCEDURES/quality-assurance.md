# Quality Assurance Procedures

> **Last Updated:** April 24, 2026
> **Purpose:** Procedures for ensuring data quality, deduplication, and validation

---

## 📊 Quality Checklist

### Before Import

- [ ] Verify source data exists and is readable
- [ ] Check file integrity (PDF signature, JSON validity)
- [ ] Count records in source vs. expected
- [ ] Document any discrepancies

### During Import

- [ ] Log progress at regular intervals
- [ ] Handle duplicates with `ON CONFLICT DO NOTHING`
- [ ] Verify row counts match source
- [ ] Check for data type mismatches

### After Import

- [ ] Run validation queries (see below)
- [ ] Cross-reference with other sources
- [ ] Update `docs/DATA_INVENTORY_FULL.md`
- [ ] Close relevant GitHub issue (if applicable)

---

## 🔍 Validation Queries

### Record Count Verification

```sql
-- Check all major tables
SELECT 'congress_bills' as table, COUNT(*) FROM congress_bills
UNION ALL
SELECT 'congress_members', COUNT(*) FROM congress_members
UNION ALL
SELECT 'federal_register_entries', COUNT(*) FROM federal_register_entries
UNION ALL
SELECT 'jmail_emails_full', COUNT(*) FROM jmail_emails_full
UNION ALL
SELECT 'icij_entities', COUNT(*) FROM icij_entities
UNION ALL
SELECT 'fec_individual_contributions', COUNT(*) FROM fec_individual_contributions;
```

### Data Integrity Checks

```sql
-- Check for NULL primary keys
SELECT 'congress_bills' as table, COUNT(*) FROM congress_bills WHERE bill_id IS NULL
UNION ALL
SELECT 'jmail_emails_full', COUNT(*) FROM jmail_emails_full WHERE message_id IS NULL;

-- Check for duplicate primary keys
SELECT bill_id, COUNT(*) FROM congress_bills GROUP BY bill_id HAVING COUNT(*) > 1;

-- Check date ranges
SELECT MIN(publish_date), MAX(publish_date) FROM federal_register_entries;
```

### Cross-Reference Validation

```sql
-- Check if Congress members appear in multiple congresses
SELECT bioguide_id, COUNT(DISTINCT congress_number)
FROM congress_members
GROUP BY bioguide_id
HAVING COUNT(DISTINCT congress_number) > 1;

-- Verify vote counts match
SELECT v.congress, v.house_vote_id, v.vote_count, COUNT(mv.member_id)
FROM congress_house_votes v
JOIN congress_house_member_votes mv ON v.house_vote_id = mv.house_vote_id
GROUP BY v.congress, v.house_vote_id, v.vote_count
HAVING v.vote_count != COUNT(mv.member_id);
```

---

## 📁 Deduplication Procedures

### Identify Duplicates

**Script:** `scripts/processing/deduplicate_records.py`

```bash
# Check for duplicates across all tables
python scripts/processing/deduplicate_records.py --check-only

# Output example:
# Found 187,234 duplicate records in jmail_emails_full
# Found 12,045 duplicate records in congress_bills
```

### Remove Duplicates (Safe)

```sql
-- Example: Remove duplicate emails keeping oldest
DELETE FROM jmail_emails_full a
USING b
WHERE a.ctid = b.ctid
  AND a.message_id = b.message_id
  AND a.__pheon_tid < b.__pheon_tid;
```

### Advanced Deduplication

**For embeddings and semantic duplicates:**

```bash
# Use vector similarity (pgvector)
python scripts/processing/vectorize_documents.py --dedup-threshold 0.95

# For text-based duplicates
python scripts/processing/eduplicate_records.py --method hash --tables jmail_emails_full,congress_bills
```

---

## 📈 Coverage Analysis

### Identify Gaps

**Issue #39:** 749K missing documents

```bash
# Compare expected vs. actual
python scripts/ingestion/check_inventory.py --compare

# Check specific gaps
python scripts/processing/check_coverage.py --source DOJ --expected 1.4M
```

### Fill Gaps

```bash
# Re-download missing documents
python scripts/download/download_congress_historical.py --congress 119 --only-missing

# For Senate vote details (Issue #58)
python scripts/download/download_senate_vote_details.py --retry-missing
```

---

## 🔧 Automated QA Pipeline

Create a comprehensive QA script:

```bash
# File: scripts/run_qa_checks.sh
#!/bin/bash

echo "Running QA checks..."

# 1. Count verification
echo "Checking record counts..."
psql -d epstein -f scripts/processing/verify_counts.sql > qa_counts.log

# 2. Integrity checks
echo "Checking data integrity..."
psql -d epstein -f scripts/processing/verify_integrity.sql > qa_integrity.log

# 3. Deduplication check
echo "Checking for duplicates..."
python scripts/processing/deduplicate_records.py --check-only > qa_dups.log

# 4. Coverage analysis
echo "Checking coverage..."
python scripts/ingestion/check_inventory.py --compare > qa_coverage.log

echo "QA complete! Check logs: qa_*.log"
```

---

## 📝 Notes for AI Agents

- **Run** validation queries after every import
- **Log** all QA results for future reference
- **Document** any data quality issues in GitHub issues
- **Use** `scripts/config.py` for database connections (never hardcode)
- **Cross-reference** with at least 2 other sources when possible

---

## 🚨 Known Quality Issues

### Issue #39: 749K Missing Documents
- **Status:** 🔴 Open
- **Action:** Identify specific gaps, re-download from alternate sources

### Issue #58: Senate Vote Details 403 Errors
- **Status:** 🔴 Open
- **Action:** Fix retry logic, try alternate user agents/headers

### Pre-2015 News Coverage Gap
- **GDELT limitation:** Only available from Feb 2015
- **Alternative:** Use CourtListener RECAP, Wayback Machine

---

*Last Updated: April 24, 2026*
*Status: Ready for Use*
