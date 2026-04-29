#!/usr/bin/env python3
"""Compatibility wrapper for the canonical financial disclosure importer."""

import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    importer = Path(__file__).resolve().parents[1] / "ingestion" / "import_financial_disclosures.py"
    sys.path.insert(0, str(importer.parent))
    if len(sys.argv) == 1:
        sys.argv.extend(["--skip-senate"])
    runpy.run_path(
        str(importer),
        run_name="__main__",
    )
