# Agents Documentation

This file documents the custom agents and scripts used in the Epstein project.

## ingest_capitolgains

**Purpose**: Wrapper script for ingesting Capitol Gains data (House and Senate disclosures).
**Location**: `ingest_capitolgains.py`
**Description**: Provides a CLI entry point that loads environment variables, downloads raw data for the House and Senate, and orchestrates further processing steps. Currently contains placeholder download functions that can be expanded with actual scraper logic.
**Usage**:
```bash
python ingest_capitolgains.py download --source house --date 2024-01-01 --out-dir data/raw
python ingest_capitolgains.py download --source senate --date 2024-01-01 --out-dir data/raw
python ingest_capitolgains.py run_all --date 2024-01-01
```

---

## epstein_capitolgains.loader

**Purpose**: Placeholder loader for Capitol Gains data.
**Location**: `epstein_capitolgains/loader.py`
**Description**: In a full implementation this module would take the transformed parquet files and load them into the project's database (PostgreSQL, SQLite, etc.). The placeholder simply logs the action and returns the path that would have been loaded.
**Usage**:
```python
from epstein_capitolgains.loader import load_to_db
load_to_db(Path("data/processed/house_2024-01-01.parquet"))
```

---

*Other agents can be documented here following the same format.*
