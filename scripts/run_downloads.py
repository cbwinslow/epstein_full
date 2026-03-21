#!/usr/bin/env python3
"""
Production DOJ File Download Runner

Runs epstein-ripper for all 12 datasets with:
- Progress tracking via tracker.py
- Disk space monitoring (alerts at 90%)
- Periodic status display
- Graceful shutdown on Ctrl+C (resume-safe)
- Log capture

Usage:
  python3 run_downloads.py              # Run all datasets
  python3 run_downloads.py --datasets 1,5,9  # Specific datasets
  python3 run_downloads.py --resume     # Resume from state files
  python3 run_downloads.py --monitor    # Just show progress (no download)
"""

import os
import sys
import time
import signal
import subprocess
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from glob import glob

# === CONFIG ===
RIPPER_DIR = "/home/cbwinslow/workspace/epstein/epstein-ripper"
RAW_DIR = "/mnt/data/epstein-project/raw-files"
TRACKER = "/home/cbwinslow/workspace/epstein/scripts/tracker.py"
PYTHON = "/home/cbwinslow/workspace/epstein/venv/bin/python3"
LOG_DIR = "/mnt/data/epstein-project/logs"
DISK_ALERT_PCT = 90
PROGRESS_INTERVAL = 30  # seconds between status updates
CHECK_INTERVAL = 10     # seconds between file count checks

# Expected files per dataset (from DOJ page counts × 50 files/page + last page)
EXPECTED = {
    1: 3158, 2: 699, 3: 1729, 4: 2616, 5: 120,
    6: 470, 7: 649, 8: 29348, 9: 103608, 10: 94287,
    11: 52459, 12: 12820
}

class DownloadMonitor:
    """Monitors download progress and reports via tracker."""

    def __init__(self, datasets: list[int]):
        self.datasets = datasets
        self.running = True
        self.start_time = datetime.now()
        self.last_progress = datetime.now()
        self.prev_counts = {}  # dataset_id -> (count, timestamp)
        self.process = None

    def count_pdfs(self, dataset_id: int) -> int:
        pattern = os.path.join(RAW_DIR, f"data{dataset_id}", "*.pdf")
        return len(glob(pattern))

    def total_size(self, dataset_id: int) -> int:
        pattern = os.path.join(RAW_DIR, f"data{dataset_id}", "*.pdf")
        return sum(os.path.getsize(f) for f in glob(pattern) if os.path.exists(f))

    def disk_usage_pct(self) -> float:
        st = os.statvfs("/mnt/data")
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        total = st.f_blocks * st.f_frsize
        return used / total * 100

    def format_bytes(self, b: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if abs(b) < 1024:
                return f"{b:.1f} {unit}"
            b /= 1024
        return f"{b:.1f} PB"

    def calc_rate(self, dataset_id: int) -> float:
        """Calculate files/second for a dataset."""
        count = self.count_pdfs(dataset_id)
        now = datetime.now()
        if dataset_id in self.prev_counts:
            prev_count, prev_time = self.prev_counts[dataset_id]
            dt = (now - prev_time).total_seconds()
            if dt > 0 and count > prev_count:
                rate = (count - prev_count) / dt
                self.prev_counts[dataset_id] = (count, now)
                return rate
        self.prev_counts[dataset_id] = (count, now)
        return 0.0

    def update_tracker(self):
        """Update tracker with current counts for all datasets."""
        for ds in self.datasets:
            count = self.count_pdfs(ds)
            subprocess.run([
                PYTHON, TRACKER, "update",
                "--id", f"doj-ds{ds}",
                "--current", str(count)
            ], capture_output=True)

    def register_datasets(self):
        """Register all datasets in tracker."""
        for ds in self.datasets:
            subprocess.run([
                PYTHON, TRACKER, "register",
                "--id", f"doj-ds{ds}",
                "--label", f"DOJ Dataset {ds} ({EXPECTED.get(ds, '?')} files)",
                "--expected", str(EXPECTED.get(ds, 0)),
                "--type", "download"
            ], capture_output=True)

    def print_status(self):
        """Print formatted status to console."""
        os.system("clear")
        elapsed = datetime.now() - self.start_time
        disk_pct = self.disk_usage_pct()

        print("=" * 78)
        print(f"  EPSTEIN DOJ FILE DOWNLOADER — Production Run")
        print(f"  Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Elapsed: {str(elapsed).split('.')[0]}")
        print(f"  Disk: {disk_pct:.1f}% used {'⚠️  WARNING' if disk_pct > DISK_ALERT_PCT else '✓'}")
        print("=" * 78)

        grand_total = 0
        grand_expected = 0

        for ds in self.datasets:
            count = self.count_pdfs(ds)
            expected = EXPECTED.get(ds, 0)
            size = self.total_size(ds)
            rate = self.calc_rate(ds)
            grand_total += count
            grand_expected += expected

            pct = (count / expected * 100) if expected > 0 else 0
            filled = int(30 * pct / 100)
            bar = "█" * filled + "░" * (30 - filled)

            # ETA
            if rate > 0 and expected > count:
                remaining = expected - count
                eta_secs = remaining / rate
                eta_str = str(timedelta(seconds=int(eta_secs)))
            else:
                eta_str = "---"

            status = "✓" if pct >= 99 else "●"
            rate_str = f"{rate:.1f} f/s" if rate > 0 else "---"

            print(f"\n  {status} Dataset {ds:>2}  [{bar}] {pct:5.1f}%")
            print(f"    {count:>6,} / {expected:>6,} files  {self.format_bytes(size):>10}  {rate_str:>10}  ETA: {eta_str}")

        overall_pct = (grand_total / grand_expected * 100) if grand_expected > 0 else 0
        print(f"\n{'─' * 78}")
        overall_bar = "█" * int(30 * overall_pct / 100) + "░" * (30 - int(30 * overall_pct / 100))
        print(f"  OVERALL: [{overall_bar}] {overall_pct:.1f}%  ({grand_total:,} / {grand_expected:,} files)")
        print(f"{'─' * 78}")
        print(f"\n  Ctrl+C to stop (resume-safe). Updates every {PROGRESS_INTERVAL}s.")

    def monitor_loop(self):
        """Background monitor that updates tracker and shows status."""
        while self.running:
            self.update_tracker()
            self.print_status()

            # Disk space alert
            if self.disk_usage_pct() > DISK_ALERT_PCT:
                print(f"\n  ⚠️  DISK SPACE ALERT: {self.disk_usage_pct():.1f}% used!")
                print(f"  Consider pausing downloads and freeing space.")

            time.sleep(PROGRESS_INTERVAL)

    def signal_handler(self, sig, frame):
        print("\n\nShutting down... (progress saved, safe to resume)")
        self.running = False
        if self.process:
            self.process.terminate()
        sys.exit(0)


def run_download(datasets: str, headless: bool = True):
    """Run the epstein-ripper with monitoring."""
    monitor = DownloadMonitor([int(d) for d in datasets.split(",")])
    monitor.register_datasets()

    # Set up signal handler
    signal.signal(signal.SIGINT, monitor.signal_handler)
    signal.signal(signal.SIGTERM, monitor.signal_handler)

    # Start monitor in background thread
    import threading
    monitor_thread = threading.Thread(target=monitor.monitor_loop, daemon=True)
    monitor_thread.start()

    # Run the ripper from the raw-files directory
    cmd = [
        PYTHON,
        os.path.join(RIPPER_DIR, "auto_ep_rip.py"),
        "--datasets", datasets,
        "--mode", "sync",
    ]
    if headless:
        cmd.append("--headless")

    print(f"\nStarting ripper: {' '.join(cmd)}")
    print(f"Working directory: {RAW_DIR}\n")

    log_file = os.path.join(LOG_DIR, f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    os.makedirs(LOG_DIR, exist_ok=True)

    with open(log_file, "w") as log:
        monitor.process = subprocess.Popen(
            cmd,
            cwd=RAW_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in monitor.process.stdout:
            sys.stdout.write(line)
            log.write(line)
            log.flush()

        monitor.process.wait()

    # Final status
    monitor.update_tracker()
    monitor.print_status()
    print(f"\nLog saved to: {log_file}")
    print("Download complete!" if monitor.process.returncode == 0 else f"Exited with code {monitor.process.returncode}")


def monitor_only():
    """Just show current progress without downloading."""
    datasets = list(range(1, 13))
    monitor = DownloadMonitor(datasets)

    try:
        while True:
            monitor.update_tracker()
            monitor.print_status()
            time.sleep(PROGRESS_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitor stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DOJ File Download Runner")
    parser.add_argument("--datasets", type=str, default="1-12",
                        help="Datasets to download (e.g. '1-12' or '1,5,9')")
    parser.add_argument("--monitor", action="store_true",
                        help="Monitor only (no download)")
    parser.add_argument("--no-headless", action="store_true",
                        help="Run browser with GUI (slower, more reliable)")

    args = parser.parse_args()

    if args.monitor:
        monitor_only()
    else:
        # Expand ranges like "1-12"
        ds_parts = []
        for part in args.datasets.split(","):
            if "-" in part:
                start, end = part.split("-")
                ds_parts.extend(str(i) for i in range(int(start), int(end) + 1))
            else:
                ds_parts.append(part)
        datasets_str = ",".join(ds_parts)
        run_download(datasets_str, headless=not args.no_headless)
