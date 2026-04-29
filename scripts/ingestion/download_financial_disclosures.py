#!/usr/bin/env python3
"""Compatibility entry point for financial disclosure acquisition.

The old implementation used House ``public_disc/privatelaw`` URLs, which are
not the financial disclosure bulk feed. This wrapper delegates to the canonical
importer so existing orchestration scripts keep working.
"""

import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Preserve the old downloader behavior of not attempting the blocked
        # Senate ingest while using the corrected House bulk-feed path.
        sys.argv.extend(["--skip-senate"])
    runpy.run_path(
        str(Path(__file__).with_name("import_financial_disclosures.py")),
        run_name="__main__",
    )
