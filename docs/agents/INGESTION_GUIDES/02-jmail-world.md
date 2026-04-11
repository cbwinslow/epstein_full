# Data Source: jMail World Emails

> **Source:** https://jmail.world  
> **Type:** Email Archive  
> **License:** Public Records  
> **Status:** ✅ Complete (1.78M emails + 1.41M documents)  
> **Size:** 344 MB total  

---

## 📋 Data Overview

jMail.world provides access to the complete Epstein email archive from various sources:

- **jMail Emails:** 1,783,792 emails
- **jMail Documents:** 1,413,417 document references
- **Date Range:** 1990-2026
- **Sources:** Multiple email drops (VOL00009-00012, yahoo, etc.)

### Source Breakdown

| Source | Emails | Description |
|--------|--------|-------------|
| VOL00011 | 669,650 | Major email drop |
| VOL00009 | 639,940 | Major email drop |
| VOL00010 | 447,251 | Major email drop |
| yahoo_2 | 17,448 | Yahoo account |
| original | 8,374 | Original collection |
| ehud_ddos_dropsite_1 | 1,058 | Related emails |
| VOL00012 | 71 | Small drop |

### Top Email Senders

| Sender | Count |
|--------|-------|
| Lesley Groff | 126,338 |
| jeffrey E. (jeevacation@gmail.com) | 121,614 |
| Jeffrey Epstein | 111,421 |
| jeevacation@gmail.com | 108,377 |
| jeffrey E. | 72,160 |

---

## 🔧 Ingestion Pipeline

### Scripts Location

`/home/cbwinslow/workspace/epstein/scripts/`

### Import Scripts

1. **`import_jmail_full.py`** - Email ingestion
2. **`import_jmail_documents.py`** - Document ingestion

---

## 📥 Download Procedure

### Data Files Location

Already downloaded at:
```
/home/cbwinslow/workspace/epstein-data/downloads/
├── jmail_emails_full.parquet (319 MB)
└── jmail_documents.parquet (25 MB)
```

### If Re-download Needed

```bash
cd /home/cbwinslow/workspace/epstein-data/downloads

# Download from jmail.world API
# (Requires authentication - already done)
```

---

## 📥 Ingestion Procedure

### Step 1: Import Emails

```bash
cd /home/cbwinslow/workspace/epstein/scripts

python3 import_jmail_full.py
```

**Features:**
- Batch size: 1,000 rows
- Autocommit mode for performance
- Conflict handling: ON CONFLICT DO NOTHING
- Progress tracking with ETA

### Step 2: Import Documents

```bash
python3 import_jmail_documents.py
```

**Features:**
- Batch size: 2,000 rows
- Index creation for performance
- Zero-error tolerance

### Monitoring

```bash
# Watch email import
tail -f /tmp/jmail_import.log

# Watch document import
tail -f /tmp/jmail_docs_import.log
```

---

## 🗄️ Database Schema

### PostgreSQL Table: `jmail_emails_full`

| Column | Type | Description |
|--------|------|-------------|
| `id` | TEXT PRIMARY KEY | Unique identifier |
| `message_id` | TEXT | Email message ID |
| `sender` | TEXT | From address |
| `recipient` | TEXT | To address |
| `subject` | TEXT | Email subject |
| `body` | TEXT | Email body |
| `date` | TIMESTAMPTZ | Sent date |
| `source_file` | TEXT | Original file |
| `epstein_as_sender` | BOOLEAN | Epstein sent this |
| `email_drop` | TEXT | Which drop (VOL00009, etc.) |

### PostgreSQL Table: `jmail_documents`

| Column | Type | Description |
|--------|------|-------------|
| `id` | TEXT PRIMARY KEY | Unique identifier |
| `doc_id` | TEXT | Document ID |
| `filename` | TEXT | Original filename |
| `file_size` | BIGINT | Size in bytes |
| `mime_type` | TEXT | File type |
| `md5_hash` | TEXT | Checksum |
| `description` | TEXT | Document description |
| `path` | TEXT | File path |
| `email_drop_id` | TEXT | Associated email drop |
| `release_batch` | INT | Release batch number |
| `extracted_at` | TIMESTAMPTZ | Extraction timestamp |

### Indexes

- `idx_jmail_emails_drop` (email_drop)
- `idx_jmail_emails_sender` (sender)
- `idx_jmail_emails_date` (date)
- `idx_jmail_docs_drop` (email_drop_id)
- `idx_jmail_docs_batch` (release_batch)
- `idx_jmail_docs_md5` (md5_hash)

---

## 📊 Quality Metrics

| Metric | Value | Date |
|--------|-------|------|
| Total Emails | 1,783,792 | April 4, 2026 |
| Total Documents | 1,413,417 | April 4, 2026 |
| Errors | 0 | - |
| Import Time | ~5 hours | - |
| Epstein as Sender | 320,871 (18%) | - |

---

## 🔍 Key Statistics

### Epstein's Email Activity

| Category | Count | Percentage |
|----------|-------|------------|
| Epstein as Sender | 320,871 | 18% |
| Epstein as Recipient | 1,462,921 | 82% |

### Date Range

| Metric | Date |
|--------|------|
| Earliest | 1990-01-01 |
| Latest | 2026-10-07 |

---

## 📝 For AI Agents

### When Working with This Data:

1. **Always use batch queries** - 1.78M records is large
2. **Filter by date** when possible
3. **Use email_drop** to isolate specific sources
4. **Check epstein_as_sender** for outgoing communications
5. **Join with documents** using email_drop_id

### Sample Queries:

```sql
-- Find emails from specific sender
SELECT * FROM jmail_emails_full 
WHERE sender ILIKE '%lesley groff%'
ORDER BY date DESC
LIMIT 100;

-- Find Epstein's outgoing emails by date
SELECT * FROM jmail_emails_full 
WHERE epstein_as_sender = true 
AND date BETWEEN '2005-01-01' AND '2008-12-31'
ORDER BY date;

-- Join emails with documents
SELECT e.*, d.filename, d.file_size
FROM jmail_emails_full e
LEFT JOIN jmail_documents d ON e.email_drop = d.email_drop_id
WHERE e.sender ILIKE '%epstein%'
LIMIT 100;
```

### Performance Tips:

- Always use `email_drop` filter when possible
- Use `date` range filters
- Use indexes for sender/recipient queries
- Consider sampling for development (`LIMIT 1000`)

---

## 🔗 Related Sources

- **DOJ Library:** Overlapping document content
- **Black Book:** Contact information (cross-reference senders)
- **Flight Logs:** Travel dates (cross-reference email dates)

---

*Last Updated: April 10, 2026*
