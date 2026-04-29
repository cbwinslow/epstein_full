#!/usr/bin/env python3
"""Compatibility wrapper for the renamed financial disclosure importer.

Use ``import_financial_disclosures.py`` directly for new work.
"""

import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).with_name("import_financial_disclosures.py")),
        run_name="__main__",
    )
