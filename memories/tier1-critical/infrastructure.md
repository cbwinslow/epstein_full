# Tier 1: Critical (Must Know for Every Session)

> These are the facts you MUST know before doing any work.
> Read this first, always. Rank: 1 (highest priority).

## Database

- **PostgreSQL 16** is the primary database
- **User:** `cbwinslow`
- **Database:** `epstein`
- **Connect:** `psql -h localhost -U cbwinslow -d epstein`
- **Auth:** `~/.pgpass` + env vars (`PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASSWORD`, `PG_DBNAME`)
- **Extensions:** pgvector 0.6.0, pg_trgm, unaccent, pg_stat_statements
- **Tables:** 42 tables, ~10.9M rows, 12GB total
- **FTS:** 2,892,730 pages indexed (100% complete)

## Python Environment

- **Venv:** `/home/cbwinslow/workspace/epstein/.venv`
- **Python:** 3.12 (uv-managed)
- **Activate:** `source .venv/bin/activate`
- **Epstein-Pipeline CLI:** `epstein-pipeline` (30+ commands, 151 tests pass)
- **Install:** `source .venv/bin/activate && pip install <package>`

## Data Storage

- **Mount:** `/mnt/data/epstein-project/` (2.3TB free on RAID5+LVM)
- **Raw PDFs:** `raw-files/` (106GB, 583K files)
- **HF Parquet:** `hf-parquet/` (318GB, 634 files)
- **Databases:** `databases/` (8.4GB pre-built SQLite, migrated to PG)
- **Supplementary:** `supplementary/` (Epstein Exposed API + FEC data, 5,464 new rows)

## Security

- **NEVER hardcode credentials** — use `os.environ.get()` always
- **Password rotation needed** — `123qweasd` in git history from prior commits
- `.env` was never committed (only `.env.example`)

## Letta Memory System

- **Letta server:** port 8283, v0.16.6, URL: https://letta.cloudcurio.cc
- **CLI:** `~/bin/letta` (create, send, memory, archival-insert, archival-search)
- **Epstein agent:** `agent-6833e981-f29d-428b-8d2a-4b7347587e2b`
- **Memory tiers:** `memories/` directory (4 tiers + sessions)
- **Archival memories** stored in Letta for semantic search

## Git

- **Repo:** https://github.com/cbwinslow/epstein_full
- **Branch:** main
- **CONTEXT.md** is living memory — update EVERY session
- **TASKS.md** is append-only — never overwrite history

## Rules

1. NEVER modify upstream repos (call via CLI or import only)
2. NEVER hardcode credentials — use env vars
3. ALWAYS update CONTEXT.md after significant changes
4. ALWAYS validate code before marking tasks done
5. ALWAYS use parameterized SQL (never string interpolation)
