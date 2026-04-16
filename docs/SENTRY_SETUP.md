# Sentry Error Tracking Setup

> **Purpose:** Monitor runtime errors and performance in the Epstein data pipeline

---

## What Sentry Does

Unlike the other tools (which analyze code statically), Sentry catches **runtime errors**:
- Uncaught exceptions during data processing
- Database connection failures
- Memory errors with large datasets
- Performance bottlenecks in long-running jobs

**Free tier:** 5,000 errors/month, 10M spans/month (more than enough)

---

## Setup Steps

### 1. Create Sentry Account (Free)

1. Go to https://sentry.io/signup/
2. Sign up with GitHub
3. Create a new project:
   - Platform: Python
   - Project name: `epstein-data-pipeline`

### 2. Get Your DSN

After creating the project, you'll see a DSN like:
```
https://abc123def456@o123456.ingest.sentry.io/7890123
```

**Keep this secret!** It allows sending errors to your Sentry project.

### 3. Add Secrets to GitHub

```bash
# Add the DSN
gh secret set SENTRY_DSN -b "YOUR_DSN_HERE" -R cbwinslow/epstein

# Add org slug (from Sentry URL, e.g., "my-org")
gh secret set SENTRY_ORG -b "YOUR_ORG_SLUG" -R cbwinslow/epstein

# Add project slug (e.g., "epstein-data-pipeline")
gh secret set SENTRY_PROJECT -b "epstein-data-pipeline" -R cbwinslow/epstein

# Get auth token from: https://sentry.io/settings/account/api/auth-tokens/
gh secret set SENTRY_AUTH_TOKEN -b "YOUR_AUTH_TOKEN" -R cbwinslow/epstein
```

### 4. Install SDK

```bash
# Install with monitoring dependencies
uv sync --group monitoring

# Or just sentry-sdk
pip install sentry-sdk
```

### 5. Use in Your Scripts

```python
#!/usr/bin/env python3
"""Example: Using Sentry in data processing scripts."""

import os
from config.sentry_config import init_sentry, capture_exception

# Initialize Sentry at startup
init_sentry()

# Example 1: Automatic error capture
@capture_exception
def process_large_dataset():
    """Sentry will capture any exception from this function."""
    # Your processing code here
    pass

# Example 2: Manual error capture
def manual_error_handling():
    try:
        risky_operation()
    except Exception as e:
        import sentry_sdk
        sentry_sdk.capture_exception(e)
        # Continue or re-raise

# Example 3: Capture messages for non-errors
def log_progress():
    import sentry_sdk
    sentry_sdk.capture_message(
        "Processing batch 1000/5000",
        level="info"
    )

if __name__ == "__main__":
    process_large_dataset()
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SENTRY_DSN` | ✅ Yes | Project DSN from Sentry |
| `SENTRY_ENVIRONMENT` | ❌ No | `development`, `staging`, `production` |
| `SENTRY_RELEASE` | ❌ No | Version tag (auto-set in CI) |
| `SENTRY_TRACES_SAMPLE_RATE` | ❌ No | Performance sampling (default: 0.1) |

---

## Data Scrubbing (IMPORTANT)

The Sentry config includes automatic scrubbing to **never** send:
- Database credentials
- API keys/tokens
- File paths with sensitive data
- SQL queries

This is critical for the Epstein project to avoid leaking:
- PostgreSQL connection strings
- Internal file paths
- Authentication tokens

---

## Viewing Errors

1. Go to your Sentry project: `https://sentry.io/organizations/YOUR_ORG/issues/`
2. See:
   - Stack traces with local variables
   - Frequency graphs
   - Affected users (if any)
   - Performance impact

---

## GitHub Actions Integration

The workflow `.github/workflows/sentry-release.yml` automatically:
- Creates a "release" in Sentry on each push to main
- Associates commits with errors
- Tracks which code changes introduced bugs

---

## Cost

| Plan | Price | Limits |
|------|-------|--------|
| **Developer** | **FREE** | 5,000 errors/month |
| Team | $26/mo | 50,000 errors/month |

**For a data pipeline:** The free tier is sufficient. Errors should be rare if your code is well-tested.

---

## When to Use Sentry

✅ **Good for:**
- Long-running batch jobs that might fail overnight
- Distributed processing across multiple workers
- Production data pipelines you need to monitor

❌ **Not needed for:**
- One-off scripts you run manually
- Development/testing (set `SENTRY_ENVIRONMENT=development`)

---

## Next Steps

1. [ ] Create Sentry account
2. [ ] Add the 4 secrets via `gh secret set`
3. [ ] Install SDK: `uv sync --group monitoring`
4. [ ] Test with a script that raises an exception
5. [ ] Verify error appears in Sentry dashboard
