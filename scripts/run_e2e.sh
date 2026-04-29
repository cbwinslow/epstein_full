#!/usr/bin/env bash

# Simple wrapper to run Playwright end‑to‑end tests.
# Usage: ./scripts/run_e2e.sh [optional args passed to `npx playwright test`]

set -euo pipefail

# Ensure Playwright is installed – if not, install it locally.
if ! command -v npx >/dev/null; then
  echo "npx not found – please install Node.js first" >&2
  exit 1
fi

# Install browsers if missing (idempotent).
npx playwright install

# Run the tests, forwarding any arguments.
exec npx playwright test "$@"
