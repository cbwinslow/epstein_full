# Tier 4: Data Quality Validation

> Validation results and known data issues.
> Rank: 4 (reference — read when validating or debugging).

## PostgreSQL Migration Validation

- **35/35 checks PASSED** (27 table counts + 5 random hashes + FTS + extensions + graph integrity)
- All 27 tables: exact row count match between SQLite and PostgreSQL
- 5 random page MD5 hashes: all match
- FTS: 865,400 pages contain 'Epstein' (working)
- Extensions: vector, pg_trgm, unaccent, pg_stat_statements
- Graph integrity: 0 orphaned relationships

## Known Data Issues

- **67,784 documents confirmed removed** from DOJ (HTTP 404)
- **23,989 documents with size mismatches** (post-release modification)
- **DS9-11 redaction "recovery" is false positive** — garbled OCR of black bars, not hidden content
- **Some EFTA numbers span multiple pages** — a single document consumes consecutive EFTA numbers
- **HOUSE_OVERSIGHT_* and DOJ-OGR-* identifiers** exist in transcripts/communications (not standard EFTA format)

## Known Bug Fixes

- **Akamai WAF blocks Playwright:** Fixed with stealth user-agent
- **JSON tracker corruption:** Fixed by rewriting with SQLite WAL mode
- **Curses doesn't work in non-TTY:** Fixed by switching to Rich library
- **epstein-ripper hangs at auth:** Fixed by building custom download_doj.py
- **PyTorch 2.10 CUDA not available:** Fixed by downgrading to 2.3.1+cu118
- **tracker.py format_bytes on file counts:** Minor cosmetic issue (shows "B" instead of "files")
