# Data Source: GDELT News Articles

> **Source:** http://data.gdeltproject.org/gdeltv2/  
> **Type:** Global Knowledge Graph (GKG) 2.0  
> **License:** Research Use  
> **Status:** ✅ Active (23,413+ articles)  
> **Coverage:** February 2015 - Present  

---

## 📋 Data Overview

GDELT (Global Database of Events, Language, and Tone) provides entity-extracted news data. The GKG 2.0 includes:

- **15-minute slices:** ~3,000-5,000 articles per slice
- **Entity extraction:** Persons, organizations, locations
- **Theme classification:** 200+ CAMEO event codes
- **Tone analysis:** Sentiment scores per article
- **Source metadata:** URL, publication date, language

### Epstein Coverage

| Date | Articles | Event |
|------|----------|-------|
| 2019-07-06 | 2,874 | Arrest day (peak) |
| 2019-07-10 | 2,768 | Breaking news |
| 2019-08-10 | 2,147 | Death reported |
| 2024-01-04 | 2,601 | Document releases |
| 2024-2025 | ~2,000 | Recent civil suits |

**⚠️ Limitation:** GDELT started February 2015. Pre-2015 era (9/11, Wexner money) NOT covered.

---

## 🔧 Ingestion Pipeline

### Scripts Location

`/home/cbwinslow/workspace/epstein-pipeline/`

### Core Scripts

1. **`gdelt_ingestion_pipeline.py`** - Single date range
2. **`gdelt_parallel_swarm.py`** - Parallel processing

---

## 📥 Download & Ingest Procedure

### Option 1: Single Date Range (Testing)

```bash
cd /home/cbwinslow/workspace/epstein-pipeline

# Download and ingest specific period
python3 gdelt_ingestion_pipeline.py \
    --start-date 2019-07-06 \
    --end-date 2019-08-31
```

### Option 2: Parallel Swarm (Production)

```bash
# Run swarm for large date range
python3 gdelt_parallel_swarm.py \
    --start-date 2019-07-01 \
    --end-date 2025-04-10 \
    --max-workers 5

# Resume interrupted swarm
python3 gdelt_parallel_swarm.py \
    --start-date 2019-07-01 \
    --end-date 2025-04-10 \
    --max-workers 5 \
    --resume
```

### Monitoring

```bash
# Watch swarm status
tail -f /tmp/gdelt_swarm.log

# Check progress
tail -f /tmp/swarm_run2.log

# Verify database count
psql "postgresql://cbwinslow:123qweasd@localhost:5432/epstein" -c \
    "SELECT COUNT(*) FROM media_news_articles WHERE discovery_source = 'gdelt';"
```

---

## 🗄️ Database Schema

### PostgreSQL Table: `media_news_articles`

| Column | Type | Description |
|--------|------|-------------|
| `article_url` | TEXT | Original URL (unique) |
| `source_domain` | TEXT | News outlet domain |
| `publish_date` | DATE | Publication date |
| `title` | TEXT | Article title |
| `all_topics` | JSONB | Entity metadata |
| `discovery_source` | TEXT | 'gdelt' |
| `collected_at` | TIMESTAMP | Ingestion time |

### JSON Topics Structure

```json
{
    "gkg_persons": ["Jeffrey Epstein", "Ghislaine Maxwell"],
    "gkg_organizations": ["Palm Beach Police", "FBI"],
    "gkg_locations": ["New York", "Paris", "London"],
    "gkg_themes": ["CRIME", "LEGAL", "JUSTICE"],
    "gkg_tone": -2.5,
    "gkg_record_id": "20190707000000-1234"
}
```

---

## 🔍 Search Terms

The pipeline filters for these entities:

```python
EPSTEIN_TERMS = [
    'epstein',
    'maxwell',
    'ghislaine',
    'giuffre',
    'virginia roberts',
    'les wexner',
    'alan dershowitz',
    'prince andrew',
    'little st. james',
    'zorro ranch',
    'lolita express',
    'jeffrey e.',
    'j. epstein',
    'epstein island'
]
```

---

## 📊 Quality Metrics

| Metric | Value |
|--------|-------|
| Total Articles | 23,413 |
| Earliest Date | 2015-02-15 |
| Latest Date | 2024-01-09 |
| Peak Day | 2019-07-10 (2,874 articles) |
| NULL Titles | 0 (100% complete) |
| NULL Topics | 0 (100% complete) |

---

## 🏢 Top News Sources

| Source | Articles |
|--------|----------|
| iheart.com | 636 |
| yahoo.com | 218 |
| dailymail.co.uk | 190 |
| reuters.com | 115 |
| msn.com | 108 |

---

## 📝 For AI Agents

### When Adding Coverage:

1. **Check existing dates** - Don't duplicate
2. **Use parallel swarm** for ranges > 30 days
3. **Monitor logs** for errors
4. **Verify ingestion** with database queries
5. **Document gaps** (pre-2015 not available)

### Key Commands:

```bash
# Check current coverage by year
psql "postgresql://cbwinslow:123qweasd@localhost:5432/epstein" -c \
    "SELECT EXTRACT(YEAR FROM publish_date)::int, COUNT(*) 
     FROM media_news_articles WHERE discovery_source = 'gdelt' 
     GROUP BY 1 ORDER BY 1;"

# Find gap periods
psql "postgresql://cbwinslow:123qweasd@localhost:5432/epstein" -c \
    "SELECT publish_date, COUNT(*) 
     FROM media_news_articles WHERE discovery_source = 'gdelt' 
     AND publish_date BETWEEN '2020-01-01' AND '2020-12-31'
     GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
```

### ⚠️ Important Notes:

- **No pre-2015 data** available from GDELT
- **GKG 2.0 started** February 2015
- **For 9/11 era coverage**, need alternative sources
- **Swarm chunks** date ranges into 30-day segments

---

## 🔗 Related Documentation

- **Pipeline Docs:** `../../docs/GDELT_PIPELINE.md`
- **Data Inventory:** `../../DATA_INVENTORY_FULL.md`
- **Main Script:** `../../epstein-pipeline/gdelt_ingestion_pipeline.py`

---

*Last Updated: April 10, 2026*
