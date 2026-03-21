# Tier 1: Critical (Must Know for Every Session)

> These are the facts you MUST know before doing any work.
> Read this first, always. Rank: 1 (highest priority).

## Database

- **PostgreSQL 16** is the primary database
- **User:** `cbwinslow`
- **Password:** `123qweasd`
- **Database:** `epstein`
- **Connect:** `psql -h localhost -U cbwinslow -d epstein`
- **Auth:** `~/.pgpass` (non-interactive)
- **Extensions:** pgvector 0.6.0, pg_trgm, unaccent, pg_stat_statements
- **Tables:** 27 tables, 10.9M rows total
- **FTS:** 2,892,730 pages indexed (100% complete)

## Python Environment

- **Venv:** `/home/cbwinslow/workspace/epstein/.venv`
- **Python:** 3.12 (uv-managed)
- **Activate:** `source .venv/bin/activate`
- **Install:** `export PATH=$HOME/.local/bin:$PATH && uv pip install <package>`
- **Never use pip directly** — always `uv pip`

## Data Storage

- **Mount:** `/mnt/data/epstein-project/` (2.3TB free on RAID5+LVM)
- **Raw PDFs:** `raw-files/` (~58GB, growing)
- **Databases:** `databases/` (8.4GB pre-built SQLite)
- **HF Parquet:** `hf-parquet/` (318GB, 634 files)
- **Processed:** `processed/` (empty, ready)
- **Logs:** `logs/` (tracker DB, download logs)

## Git

- **Repo:** https://github.com/cbwinslow/epstein_full
- **Branch:** main
- **Submodules:** 4 upstream repos (DO NOT MODIFY)
- **CONTEXT.md** is living memory — included in every prompt
- **TASKS.md** is append-only — never overwrite history

## Rules

1. NEVER modify upstream repos (call via CLI or import only)
2. ALWAYS use `uv pip` (never bare `pip`)
3. ALWAYS update CONTEXT.md after significant changes
4. ALWAYS validate code before marking tasks done
5. ALWAYS use parameterized SQL (never string interpolation)
