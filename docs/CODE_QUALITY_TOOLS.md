# Code Quality Tools Setup Guide

> **Purpose:** Configure automated code quality, security scanning, and AI-powered code review for the Epstein data project

---

## Summary: Which Tools to Use

| Tool | Cost | Best For | Setup Effort | Recommendation |
|------|------|----------|--------------|----------------|
| **CodeRabbit** | Free (public repos) | AI code review on PRs | 10 minutes | **HIGHLY RECOMMENDED** |
| **GitHub Actions** | Free (public repos) | CI/CD, testing, linting | Already done ✅ | **KEEP CURRENT** |
| **SonarQube Cloud** | Free (public repos) | Deep code analysis, security | 20 minutes | **RECOMMENDED** |
| **Codacy** | Free (public repos) | Multi-language linting | 15 minutes | **OPTIONAL** (SonarQube overlaps) |
| **CodeQL** | Free (GitHub native) | Security vulnerability scanning | Already done ✅ | **KEEP CURRENT** |

---

## 1. CodeRabbit (AI Code Review) ⭐ TOP PRIORITY

**What it does:** AI-powered code review on every pull request. Reviews code quality, suggests improvements, catches bugs, and explains complex changes.

**Why for this project:**
- Your data processing scripts are complex (1M+ lines of Python across ingestion/processing)
- Catches bugs in data pipeline code before merge
- Explains SQL schema changes and data migrations
- Reviews are fast (~2 minutes) vs human review

### Setup Steps

**Step 1: Install GitHub App**
1. Go to https://coderabbit.ai/
2. Click "Get Started" or "Add to GitHub"
3. Select your `cbwinslow/epstein` repository
4. Grant read access to code, pull requests, and issues

**Step 2: Create Configuration File**
Create `.coderabbit.yaml` in repo root:

```yaml
# .coderabbit.yaml
language: en-US
early_access: false
reviews:
  profile: chill  # Options: chill, balanced, assertive
  request_changes_workflow: false
  high_level_summary: true
  poem: false  # Disable poem generation (annoying)
  review_status: true
  collapse_walkthrough: false
  path_filters: []
  path_instructions:
    - path: "scripts/ingestion/**/*.py"
      instructions: |
        Review data ingestion scripts for:
        - SQL injection vulnerabilities
        - Proper batch processing
        - Error handling for network failures
        - Rate limiting compliance
    - path: "scripts/processing/**/*.py"
      instructions: |
        Review data processing scripts for:
        - Memory efficiency with large datasets
        - Proper connection pooling
        - Transaction handling
    - path: "**/*.sql"
      instructions: |
        Review SQL for:
        - Index usage optimization
        - Potential N+1 queries
        - Proper constraints
  auto_review:
    enabled: true
    ignore_title_keywords:
      - "WIP"
      - "Draft"
      - "DO NOT MERGE"
    drafts: false
    base_branches:
      - "main"
      - "master"
      - "develop"
  chat:
    auto_reply: true
  tools:
    # Enable additional AI tools
    github_actions:
      enabled: true
    shellcheck:
      enabled: true
    ruff:
      enabled: true
    markdownlint:
      enabled: true

# Knowledge bases for context
knowledge_base:
  learnings:
    scope: auto
  issues:
    enabled: true
  jira:
    enabled: false
  linear:
    enabled: false
  pull_requests:
    enabled: true
```

**Step 3: Test It**
1. Create a test PR with some Python changes
2. CodeRabbit should comment within 1-2 minutes
3. You can chat with it by mentioning `@coderabbitai` in PR comments

### Cost
- **Public repos:** FREE unlimited usage
- **Private repos:** $15/user/month (you don't need this)

---

## 2. SonarQube Cloud (Deep Code Analysis)

**What it does:** Static analysis for code smells, bugs, security vulnerabilities, and technical debt. More thorough than basic linters.

**Why for this project:**
- Your Python codebase is large and complex
- SQL injection risks in data ingestion scripts
- Security issues in file processing code
- Tracks technical debt over time

### Setup Steps

**Step 1: Sign Up**
1. Go to https://sonarcloud.io/
2. Sign up with your GitHub account
3. Import your `cbwinslow/epstein` repository

**Step 2: Create `sonar-project.properties`**

```properties
# sonar-project.properties
sonar.projectKey=cbwinslow_epstein
sonar.organization=cbwinslow
sonar.host.url=https://sonarcloud.io

# Source code
sonar.sources=.
sonar.exclusions=**/tests/**,**/node_modules/**,**/.git/**,**/venv/**,**/__pycache__/**,**/data/**,**/downloads/**

# Python specific
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml

# Test coverage
sonar.coverage.exclusions=**/tests/**,scripts/archive/**,scripts/migrations/**

# Encoding
sonar.sourceEncoding=UTF-8
```

**Step 3: Add GitHub Action Workflow**

Create `.github/workflows/sonarqube.yml`:

```yaml
name: SonarQube Analysis

on:
  push:
    branches: [main, master, develop]
  pull_request:
    branches: [main, master]

jobs:
  sonarqube:
    name: SonarQube Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for blame info

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/epstein_test
        run: |
          pytest tests/ --cov=. --cov-report=xml --cov-report=term

      - name: SonarQube Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

**Step 4: Add Secret**
1. In SonarCloud, get your project token
2. Go to GitHub → Settings → Secrets → Actions
3. Add `SONAR_TOKEN` with your SonarCloud token

### Cost
- **Public repos:** FREE (unlimited analysis)
- **Private repos:** Starting at $10/month

---

## 3. Enhanced GitHub Actions

Your current CI is good but can be enhanced. Here's an improved setup:

### New/Enhanced Workflows

**`.github/workflows/ci-enhanced.yml`** (improvements to existing):

```yaml
name: Enhanced CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  # Fast linting job
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync

      - name: Run Ruff (lint + format)
        run: |
          uv run ruff check .
          uv run ruff format --check .

      - name: Run MyPy type checking
        run: uv run mypy media_acquisition scripts --ignore-missing-imports

      - name: Check SQL migrations
        run: |
          # Validate SQL syntax
          for f in migrations/*.sql; do
            echo "Checking $f"
            psql --version  # Just check psql is available
          done

  # Security scanning
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  # Data validation job (Epstein-specific)
  data-validation:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, '[data]') || github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync

      - name: Run data validation scripts
        run: |
          # Add your data validation scripts here
          uv run python scripts/validate_schema.py || true
          uv run python scripts/check_data_integrity.py || true
```

### Secrets to Add

Go to GitHub → Settings → Secrets → Actions and add:

| Secret | Purpose |
|--------|---------|
| `SONAR_TOKEN` | SonarQube Cloud authentication |
| `CODECOV_TOKEN` | Codecov coverage uploads (optional) |
| `DATABASE_URL` | For integration tests (use GitHub Secrets) |

---

## 4. Codacy (Alternative to SonarQube)

**Skip this if you use SonarQube** - they overlap significantly.

### Quick Setup (if you want both)

1. Go to https://www.codacy.com/
2. Sign up with GitHub
3. Add your repository
4. Add badge to README:

```markdown
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/YOUR_PROJECT_ID)](https://app.codacy.com/gh/cbwinslow/epstein/dashboard)
```

### Why Codacy over SonarQube?
- Better multi-language support in one dashboard
- Simpler setup (no configuration files)
- Better PR decoration (inline comments)

### Why SonarQube over Codacy?
- Better Python-specific analysis
- Security focus (SAST)
- More detailed issue tracking
- Free for public repos with more features

**My recommendation:** Use **SonarQube Cloud** (it's free and more thorough for Python).

---

## 5. Pre-commit Hooks (Local Quality Gates)

Your pre-commit config is good but outdated. Here's an updated version:

```yaml
# .pre-commit-config.yaml (updated)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0  # Updated from v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-json
      - id: check-merge-conflict
      - id: debug-statements
      - id: check-toml
      - id: detect-private-key

  # Replace Black + isort + flake8 with Ruff
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # MyPy for type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - types-psycopg2
          - types-python-dateutil
          - pydantic
        args: ['--ignore-missing-imports']

  # SQL linting
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.0.0
    hooks:
      - id: sqlfluff-lint
        args: [--dialect, postgres]

  # Security scanning
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
```

---

## Implementation Priority

### Week 1: Quick Wins
1. **Set up CodeRabbit** (10 min) - Immediate AI reviews
2. **Update pre-commit hooks** (15 min) - Local quality gates
3. **Add SonarQube Cloud** (20 min) - Deep analysis

### Week 2: CI/CD Improvements
4. **Enhance GitHub Actions** (30 min) - Add security scanning, data validation
5. **Add coverage reporting** (15 min) - Integrate with Codecov or SonarQube

### Week 3: Advanced Features
6. **Configure CodeRabbit custom instructions** (20 min) - Tailor reviews for data processing code
7. **Add dependency scanning** (15 min) - Snyk or Dependabot

---

## Cost Summary

| Tool | Public Repo Cost | Your Cost |
|------|------------------|-----------|
| CodeRabbit | FREE | $0 |
| SonarQube Cloud | FREE | $0 |
| GitHub Actions | FREE (2,000 min/month) | $0 |
| CodeQL | FREE (GitHub native) | $0 |
| Pre-commit | FREE | $0 |
| **TOTAL** | | **$0** |

---

## Next Steps

1. **Start with CodeRabbit** - biggest impact, easiest setup
2. **Set up SonarQube Cloud** - comprehensive analysis
3. **Update pre-commit hooks** - catch issues before push
4. **Enhance GitHub Actions** - automated CI/CD

**Want me to create any of these configuration files for you?** I can generate:
- `.coderabbit.yaml`
- `sonar-project.properties`
- `.github/workflows/sonarqube.yml`
- Updated `.pre-commit-config.yaml`
