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
import sys
import time
import subprocess
from pathlib import Path

TRACKER = "/home/cbwinslow/workspace/epstein/scripts/tracker.py"
PYTHON = "/home/cbwinslow/workspace/epstein/venv/bin/python3"
POLL_INTERVAL = 5  # seconds

# Watches: (task_id, directory_or_file, pattern)
WATCHES = [
    # Databases
    ("db-fulltext", "/mnt/data/epstein-project/databases", "full_text_corpus.db"),
    ("db-redaction", "/mnt/data/epstein-project/databases", "redaction_analysis_v2.db"),
    ("db-image", "/mnt/data/epstein-project/databases", "image_analysis.db"),
    ("db-ocr", "/mnt/data/epstein-project/databases", "ocr_database.db"),
    ("db-comms", "/mnt/data/epstein-project/databases", "communications.db"),
    ("db-transcripts", "/mnt/data/epstein-project/databases", "transcripts.db"),
    ("db-kg", "/mnt/data/epstein-project/databases", "knowledge_graph.db"),
    # DOJ raw files (PDFs)
    ("doj-ds1", "/mnt/data/epstein-project/raw-files/data1", "*.pdf"),
    ("doj-ds2", "/mnt/data/epstein-project/raw-files/data2", "*.pdf"),
    ("doj-ds3", "/mnt/data/epstein-project/raw-files/data3", "*.pdf"),
    ("doj-ds4", "/mnt/data/epstein-project/raw-files/data4", "*.pdf"),
    ("doj-ds5", "/mnt/data/epstein-project/raw-files/data5", "*.pdf"),
    ("doj-ds6", "/mnt/data/epstein-project/raw-files/data6", "*.pdf"),
    ("doj-ds7", "/mnt/data/epstein-project/raw-files/data7", "*.pdf"),
    ("doj-ds8", "/mnt/data/epstein-project/raw-files/data8", "*.pdf"),
    ("doj-ds9", "/mnt/data/epstein-project/raw-files/data9", "*.pdf"),
    ("doj-ds10", "/mnt/data/epstein-project/raw-files/data10", "*.pdf"),
    ("doj-ds11", "/mnt/data/epstein-project/raw-files/data11", "*.pdf"),
    ("doj-ds12", "/mnt/data/epstein-project/raw-files/data12", "*.pdf"),
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
