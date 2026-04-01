#!/usr/bin/env python3
"""
Background file-size watcher that feeds the progress tracker.
Runs in a loop, scanning watched paths, updating the shared state.

Usage:
  python3 file_watcher.py &
  
  # Or add watches manually:
  python3 file_watcher.py --once
"""

import os
import subprocess
import sys
import time
from pathlib import Path

# Import shared configuration
from epstein_config import DATABASES_DIR, RAW_FILES_DIR

TRACKER = "/home/cbwinslow/workspace/epstein/scripts/tracker.py"
PYTHON = "/home/cbwinslow/workspace/epstein/venv/bin/python3"
POLL_INTERVAL = 5  # seconds

# Watches: (task_id, directory_or_file, pattern)
WATCHES = [
    # Databases
    ("db-fulltext", str(DATABASES_DIR), "full_text_corpus.db"),
    ("db-redaction", str(DATABASES_DIR), "redaction_analysis_v2.db"),
    ("db-image", str(DATABASES_DIR), "image_analysis.db"),
    ("db-ocr", str(DATABASES_DIR), "ocr_database.db"),
    ("db-comms", str(DATABASES_DIR), "communications.db"),
    ("db-transcripts", str(DATABASES_DIR), "transcripts.db"),
    ("db-kg", str(DATABASES_DIR), "knowledge_graph.db"),
    # DOJ raw files (PDFs)
    ("doj-ds1", str(RAW_FILES_DIR / "data1"), "*.pdf"),
    ("doj-ds2", str(RAW_FILES_DIR / "data2"), "*.pdf"),
    ("doj-ds3", str(RAW_FILES_DIR / "data3"), "*.pdf"),
    ("doj-ds4", str(RAW_FILES_DIR / "data4"), "*.pdf"),
    ("doj-ds5", str(RAW_FILES_DIR / "data5"), "*.pdf"),
    ("doj-ds6", str(RAW_FILES_DIR / "data6"), "*.pdf"),
    ("doj-ds7", str(RAW_FILES_DIR / "data7"), "*.pdf"),
    ("doj-ds8", str(RAW_FILES_DIR / "data8"), "*.pdf"),
    ("doj-ds9", str(RAW_FILES_DIR / "data9"), "*.pdf"),
    ("doj-ds10", str(RAW_FILES_DIR / "data10"), "*.pdf"),
    ("doj-ds11", str(RAW_FILES_DIR / "data11"), "*.pdf"),
    ("doj-ds12", str(RAW_FILES_DIR / "data12"), "*.pdf"),
]

def count_files(directory: str, pattern: str) -> tuple:
    """Count files and total size matching a glob pattern."""
    from glob import glob
    matches = glob(os.path.join(directory, pattern))
    total_size = sum(os.path.getsize(f) for f in matches if os.path.exists(f))
    return len(matches), total_size

def run_tracker(*args):
    subprocess.run([PYTHON, TRACKER] + list(args), capture_output=True)

def update_all():
    for task_id, directory, pattern in WATCHES:
        count, size = count_files(directory, pattern)
        run_tracker("update", "--id", task_id, "--current", str(size))

def main():
    once = "--once" in sys.argv

    print(f"File watcher started (poll every {POLL_INTERVAL}s)")
    print(f"Watches: {WATCHES}")

    while True:
        try:
            update_all()
            if once:
                break
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\nWatcher stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
