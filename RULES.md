# Epstein Files Analysis - Rules & Conventions

## Data Integrity Rules
1. **Never modify raw downloaded files** - they are immutable archival copies
2. **Validate PDF signatures** before saving - reject HTML age-gate pages
3. **SHA-256 hash everything** - detect corruption and duplicates
4. **Log all operations** - every download, processing step, and error
5. **Resume-safe** - all operations must be idempotent and resumable

## Processing Rules
1. **OCR confidence threshold**: 0.7 minimum for text extraction
2. **NER minimum mention count**: 2+ documents for entity inclusion
3. **Deduplication**: 3-pass (hash → MinHash → semantic similarity)
4. **Redaction handling**: Flag proper vs improper redactions, attempt text recovery
5. **GPU scheduling**: Batch operations, respect CUDA memory limits (12GB per K80)

## Rate Limiting Rules
1. **DOJ website**: 0.75s between downloads, 0.5s between page scrapes
2. **Archive.org**: 1.0s between API requests
3. **GitHub API**: Respect 60/hour (unauthenticated) or 5000/hour (authenticated)
4. **Concurrent downloads**: Max 5 per dataset, 10 total

## Storage Rules
1. **Raw files**: `/mnt/data/epstein-project/raw-files/data{N}/`
2. **Databases**: `/mnt/data/epstein-project/databases/`
3. **Processed output**: `/mnt/data/epstein-project/processed/`
4. **Logs**: `/mnt/data/epstein-project/logs/`
5. **Alert at 90% disk usage** - pause downloads, notify

## Security Rules
1. **No credentials in code** - use environment variables only
2. **No personally identifiable information in logs** - redact victim names
3. **Age verification** - always pass the DOJ age gate
4. **Session management** - rebuild Playwright context on poison detection

## Naming Conventions
- EFTA numbers: `EFTA{8-digit-zero-padded}` (e.g., `EFTA00000001`)
- Dataset directories: `data{N}` (e.g., `data1`, `data12`)
- State files: `resume_data{N}.txt`
- Index files: `index_data{N}.json`
- Log files: `download.log`, `processing.log`

## Code Style
- Python 3.10+ with type hints
- Black formatting, ruff linting
- Docstrings for all public functions
- Async for I/O operations (aiohttp, playwright)
- Rich console output for progress tracking

## Code Quality Standards
1. **File header** — every script starts with a docstring: purpose, usage examples, author
2. **Configuration constants** — all magic values at top of file as named constants, never inline
3. **Parameterized SQL** — always use `?` placeholders, never f-strings or string concatenation in queries
4. **Error handling** — every DB/network/file operation in try/except with specific error types
5. **Resource cleanup** — always use `finally` to close connections, files, handles
6. **Docstrings** — every public function: one-line summary, Args/Returns/Raises
7. **Comments** — explain WHY, not WHAT. Section headers for logical groups
8. **Type hints** — function signatures must have types for args and return
9. **Logging to stderr** — errors go to `stderr`, progress to `stdout`
10. **Idempotent** — operations must be safe to re-run (INSERT OR REPLACE, check before create)
11. **No global mutable state** — pass config via constants or function args
12. **Separate concerns** — I/O, logic, and display in different functions

## Testing Rules
1. Validate PDF signature on every download
2. Check file sizes match expected
3. Verify OCR output contains expected content
4. Test entity extraction against known entities
5. Validate knowledge graph relationships

## Codebase Separation Rules
1. **NEVER modify cloned/forked repos directly** — treat them as upstream dependencies
2. **Build on top, not inside** — our code lives in `scripts/`, `workers/`, or our own modules
3. **Extend via composition** — wrap upstream classes/methods, don't patch them
4. **Use interfaces** — call upstream CLI commands or import their public APIs as-is
5. **Track our additions separately** — everything we write should be clearly ours
6. **Upstream-ready** — write clean code that could be submitted as PRs to original repos
7. **Document integration points** — clearly note which upstream version/commit we tested against

### Allowed interactions with upstream repos:
- `import` their public modules and call their functions
- Shell out to their CLI commands (`epstein-pipeline ocr ...`, `python3 auto_ep_rip.py ...`)
- Read their config files and output formats
- Subclass their base classes in our own code

### Forbidden:
- Editing files inside `Epstein-Pipeline/`, `epstein-ripper/`, `Epstein-research-data/`, etc.
- Forking their code into our scripts without attribution
- Monkey-patching their modules at runtime

## Validation Loop Rule
1. **Every piece of code must be validated** — create a test or execute it to prove it works
2. **Validation methods** (use best judgment per situation):
   - **Execute and verify**: Run the code, check output matches expectations
   - **Unit test**: Write a test function that exercises the code path
   - **Integration test**: Test that components work together (e.g., tracker + watcher)
   - **Data verification**: Query databases, check file sizes, confirm structure
   - **Smoke test**: Minimal invocation to prove no crashes
3. **Document validation results** — what was tested, how, what passed/failed
4. **If uncertain, ask the user** — don't assume, don't skip
5. **Fix before proceeding** — broken code blocks downstream work
6. **Re-validate after changes** — any edit to validated code requires re-validation

## Living Documentation Rule
1. **CONTEXT.md is our memory** — update it EVERY session with:
   - What we did
   - What we learned
   - What changed
   - Current state of everything
2. **Include CONTEXT.md in every prompt** — it's the persistent context between sessions
3. **Keep it concise** — facts, paths, numbers, status. No prose.
4. **Timestamp entries** — date every change so we can track evolution
5. **Mark TODOs clearly** — `[ ]` pending, `[~]` in progress, `[x]` done

## Documentation Rules
1. Update CONTEXT.md with new findings
2. Log all data quality issues
3. Document API changes and URL pattern discoveries
4. Track dataset version changes (DOJ removes/alters files)

## Environment & Tooling Rules
1. **Python version**: 3.12 pinned in `.python-version` and `pyproject.toml`
2. **Package manager**: `uv` only — never `pip install` directly
   - Add deps: `uv add <package>`
   - Run scripts: `uv run python scripts/foo.py`
   - Sync all: `uv sync`
3. **Node**: Use `npx` for one-off tools, never global installs
4. **Config files**: All in project root — `pyproject.toml`, `.python-version`, `.env`
5. **Secrets**: In `.env` (git-ignored), template in `.env.example`
6. **Setup**: `./setup.sh` creates entire environment from scratch
7. **Verification**: Run `uv run python scripts/setup_dev.py` after setup

## Deployment Checklist
Before pushing any code:
1. [ ] Code runs without errors (`uv run python scripts/foo.py`)
2. [ ] No hardcoded paths — use constants from config
3. [ ] No secrets in code — use `.env` variables
4. [ ] Docstrings on all public functions
5. [ ] Updated TASKS.md if task status changed
6. [ ] Updated CONTEXT.md if state changed
7. [ ] Git commit with descriptive message
8. [ ] Push to GitHub

## Anti-Drift Rules
1. **Check TASKS.md** before starting — don't duplicate work
2. **Check CONTEXT.md** for current state — don't assume old paths/configs
3. **Check existing scripts/** — don't reinvent tools
4. **Use same patterns** — match existing code style and conventions
5. **Ask if uncertain** — better to clarify than to waste time
6. **Update memory files** — CONTEXT.md + TASKS.md after every session
7. **Single source of truth** — pyproject.toml for deps, .python-version for Python, .env for secrets
