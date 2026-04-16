# Data Acquisition Rule

## Purpose
Maintain organized, validated, reproducible data acquisition code and records for the Epstein investigation.

## Requirements

### 1. Code Organization
- All data acquisition scripts in `scripts/ingestion/` or `scripts/download/`
- Clear naming: `download_{source}_{dataset}.py`
- Modular design: separate download, parse, validate, load functions
- Configuration via environment variables or config files (no hardcoded secrets)

### 2. Documentation Standards
- Every script must have:
  - Docstring explaining data source, format, update frequency
  - Expected record count and size
  - API documentation links
  - Rate limit information
  - Known issues or limitations

### 3. Validation Requirements
- Download validation (checksums, file size)
- Data format validation (schema checks)
- Record count validation (expected vs actual)
- Cross-reference validation (against other datasets)
- Log all validation results

### 4. Logging & Journaling
- All downloads logged to `logs/ingestion/`
- Log format: timestamp, source, records, file size, status, errors
- Maintain ingestion journal in `docs/INGESTION_JOURNAL.md`
- GitHub issues for tracking each dataset acquisition

### 5. Reproducibility
- All code must be version controlled (GitHub)
- Dependencies listed in requirements.txt
- Docker/container support where applicable
- README with setup and run instructions
- Example .env file showing required variables

### 6. Data Lineage
- Track source → download → transform → load
- Maintain `data_inventory` table in PostgreSQL
- Record: source, download date, record count, checksum, location
- Cross-reference tables for entity linking

### 7. Error Handling
- Graceful failures with retry logic
- Exponential backoff for API rate limits
- Quarantine corrupted/partial files
- Alert on repeated failures

### 8. Multi-Agent Coordination
- Use `ingestion/` directory structure for parallel workers
- Queue-based work distribution where applicable
- Lock files to prevent duplicate downloads
- State tracking for resume capability

## Directory Structure

```
scripts/
├── ingestion/
│   ├── download_{source}.py      # Download scripts
│   ├── parse_{format}.py         # Parser utilities
│   └── validate_{dataset}.py     # Validation scripts
├── database/
│   └── update_inventory.sql      # Inventory updates
└── utils/
    └── data_quality.py           # Shared validation functions

logs/
├── ingestion/
│   └── YYYY-MM-DD/               # Daily log directories
└── validation/
    └── YYYY-MM-DD/

data/
├── raw/
│   └── {source}/                 # Raw downloads
├── processed/
│   └── {source}/                 # Cleaned/transformed
└── inventory.json                # Data manifest

docs/
├── INGESTION_JOURNAL.md          # Acquisition timeline
├── DATA_SOURCES.md               # Source documentation
└── VALIDATION_REPORTS/           # Validation outputs
```

## Checklist Before Merging

- [ ] Script tested and working
- [ ] Documentation complete
- [ ] Validation checks pass
- [ ] Logs generated successfully
- [ ] Inventory updated
- [ ] GitHub issue created/updated
- [ ] No secrets in code
- [ ] Rate limits respected
- [ ] Error handling tested

## Cross-Validation Requirements

Every dataset must be cross-validated with:
1. Other government datasets (FEC vs SEC vs Congress)
2. News articles (GDELT mentions)
3. ICIJ offshore data (entity matching)
4. Flight logs (person presence)

## SQL Tracking Tables

```sql
-- Required tables for data acquisition tracking
data_inventory      -- Master inventory of all datasets
ingestion_log       -- Detailed download logs
validation_results  -- Quality check results
cross_references    -- Entity links across datasets
```
