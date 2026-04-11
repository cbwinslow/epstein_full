# Ingestion Scripts - Organized

## Directory Structure

| Directory | Count | Purpose |
|-----------|-------|---------|
| `archive/` | 28 | Broken/deprecated scripts |
| `download/` | 9 | Data download scripts |
| `enrichment/` | 5 | Article content enrichment |
| `fec/` | 4 | FEC campaign finance data |
| `import/` | 9 | Database import scripts |
| `jmail/` | 7 | JMail email/document processing |
| `misc/` | 5 | Other utilities |

## Key Scripts

### Working Enrichment
- `enrichment/enrich_with_trafilatura.py` - Main article enrichment
- `enrichment/monitor_enrichment.py` - Progress monitoring

### Downloads
- `download/download_manager.py` - General download manager
- `download/download_fec_bulk.py` - FEC bulk data
- `download/download_icij.py` - ICIJ offshore leaks

### Database Imports
- `import/import_fbi_files.py` - FBI vault import
- `import/import_icij.py` - ICIJ data import

## Archive Contents
Scripts moved to `archive/` are broken/deprecated:
- Failed framework attempts (news_ingestion_framework.py, phase1_discovery.py, etc.)
- Duplicate download scripts
- Old collection scripts

## Usage

```bash
# Enrich articles
cd enrichment && python3 enrich_with_trafilatura.py

# Monitor progress
cd enrichment && python3 monitor_enrichment.py

# Quality control
psql -d epstein -f ../quality_control_queries.sql
```
