#!/usr/bin/env python3
"""
Epstein Project - Live Progress Dashboard (rich-based)

Real-time terminal dashboard for monitoring download progress.
Uses rich Live display for smooth updates.

Usage:
  python3 dashboard.py              # Launch dashboard
  python3 dashboard.py --refresh 2  # Custom refresh rate (seconds)
  python3 dashboard.py --once       # Single snapshot (no loop)
"""

import os
import subprocess
import time
from datetime import datetime, timedelta
from glob import glob

from rich import box
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# =============================================================================
# Configuration
# =============================================================================

RAW_DIR = "/home/cbwinslow/workspace/epstein-data/raw-files"
REFRESH_INTERVAL = 3  # seconds

# Actual corpus counts
EXPECTED = {
    1: 3158, 2: 574, 3: 67, 4: 152, 5: 120,
    6: 13, 7: 17, 8: 10595, 9: 531283, 10: 498702,
    11: 336107, 12: 12080,
}

DATASET_NAMES = {
    1: "DS1 (Small)", 2: "DS2 (Small)", 3: "DS3 (Tiny)", 4: "DS4 (Tiny)",
    5: "DS5 (Tiny)", 6: "DS6 (Tiny)", 7: "DS7 (Tiny)", 8: "DS8 (Medium)",
    9: "DS9 (LARGE)", 10: "DS10 (LARGE)", 11: "DS11 (LARGE)", 12: "DS12 (Medium)",
}


# =============================================================================
# Data Collection
# =============================================================================

def get_file_counts() -> dict:
    """Count PDFs per dataset."""
    counts = {}
    for ds in range(1, 13):
        counts[ds] = len(glob(os.path.join(RAW_DIR, f"data{ds}", "*.pdf")))
    return counts


def get_disk_usage() -> tuple:
    """Get (used_bytes, total_bytes, pct_used)."""
    st = os.statvfs("/mnt/data")
    total = st.f_blocks * st.f_frsize
    free = st.f_bfree * st.f_frsize
    used = total - free
    return used, total, used / total * 100


def get_process_count() -> tuple:
    """Get (download_procs, aria2c_procs)."""
    try:
        dl = int(subprocess.run(
            ["pgrep", "-cf", "download_(cdn|doj)"],
            capture_output=True, text=True
        ).stdout.strip())
    except Exception:
        dl = 0
    try:
        aria = int(subprocess.run(
            ["pgrep", "-c", "aria2c"],
            capture_output=True, text=True
        ).stdout.strip())
    except Exception:
        aria = 0
    return dl, aria


# =============================================================================
# Formatting
# =============================================================================

def format_bytes(b) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(b) < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"


def format_eta(current: int, expected: int, rate: float) -> str:
    if rate <= 0 or expected <= 0 or current >= expected:
        return "-"
    remaining = expected - current
    secs = remaining / rate
    td = timedelta(seconds=int(secs))
    if td.days > 0:
        return f"{td.days}d{td.seconds // 3600}h"
    elif td.seconds >= 3600:
        return f"{td.seconds // 3600}h{(td.seconds % 3600) // 60}m"
    elif td.seconds >= 60:
        return f"{td.seconds // 60}m{td.seconds % 60}s"
    return f"{td.seconds}s"


def progress_bar(pct: float, width: int = 25) -> Text:
    """Render a colored progress bar."""
    filled = int(width * min(pct, 100) / 100)
    bar = Text()
    if pct >= 99.9:
        bar.append("█" * filled, style="bold green")
        bar.append("░" * (width - filled), style="dim")
    elif pct >= 50:
        bar.append("█" * filled, style="green")
        bar.append("░" * (width - filled), style="dim")
    elif pct >= 10:
        bar.append("█" * filled, style="yellow")
        bar.append("░" * (width - filled), style="dim")
    else:
        bar.append("█" * filled, style="red")
        bar.append("░" * (width - filled), style="dim")
    return bar


# =============================================================================
# Dashboard Render
# =============================================================================

prev_counts = {}
prev_time = time.time()


def build_dashboard() -> Panel:
    """Build the dashboard layout."""
    global prev_counts, prev_time

    now = time.time()
    counts = get_file_counts()
    total = sum(counts.values())
    total_expected = sum(EXPECTED.values())
    overall_pct = (total / total_expected * 100) if total_expected > 0 else 0

    # Rate calculation
    dt = now - prev_time
    rate = 0
    if dt > 0 and prev_counts:
        rate = (total - sum(prev_counts.values())) / dt

    prev_counts = counts
    prev_time = now

    # Disk and processes
    used, disk_total, disk_pct = get_disk_usage()
    dl_procs, aria_procs = get_process_count()

    # === Build table ===
    table = Table(
        box=box.SIMPLE_HEAVY,
        show_header=True,
        header_style="bold cyan",
        pad_edge=False,
        expand=True,
    )

    table.add_column("DS", width=4, justify="center")
    table.add_column("Progress", min_width=25)
    table.add_column("Pct", width=7, justify="right")
    table.add_column("Files", width=16, justify="right")

    for ds in range(1, 13):
        count = counts.get(ds, 0)
        exp = EXPECTED.get(ds, 0)
        pct = (count / exp * 100) if exp > 0 else 0

        # Per-dataset rate
        ds_rate = 0
        if prev_counts and ds in prev_counts and dt > 0:
            # Use previous counts for rate (current already updated)
            pass  # Rate per-dataset is noisy, skip for now

        is_done = pct >= 99.9
        icon = "✓" if is_done else "●"
        ds_label = f"{icon} {ds}"

        table.add_row(
            ds_label,
            progress_bar(pct),
            f"{pct:.1f}%",
            f"{count:,}/{exp:,}",
        )

    # === Summary ===
    disk_color = "red" if disk_pct > 90 else "magenta"

    summary = Text()
    summary.append("  Files: ", style="bold")
    summary.append(f"{total:,}", style="green bold")
    summary.append(f" / {total_expected:,}  ({overall_pct:.1f}%)", style="dim")
    summary.append("  │  Rate: ", style="bold")
    summary.append(f"{rate:.1f}/s", style="cyan bold")
    summary.append("  │  ETA: ", style="bold")
    summary.append(f"{format_eta(total, total_expected, rate)}", style="yellow")
    summary.append("\n  Disk: ", style="bold")
    summary.append(f"{format_bytes(used)} / {format_bytes(disk_total)}", style=disk_color)
    summary.append(f"  ({disk_pct:.1f}%)", style="dim")
    summary.append("  │  Processes: ", style="bold")
    summary.append(f"{dl_procs} download + {aria_procs} aria2c", style="cyan")
    summary.append("  │  Time: ", style="bold")
    summary.append(f"{datetime.now().strftime('%H:%M:%S')}", style="dim")

    # Overall progress bar
    overall_bar = progress_bar(overall_pct, width=40)

    # === Combine into panel ===
    content = Table.grid(expand=True)
    content.add_row(summary)
    content.add_row(Text())
    content.add_row(table)
    content.add_row(Text())
    content.add_row(Text("  Overall: ", style="bold"), overall_bar,
                    Text(f"  {overall_pct:.1f}%", style="bold green"))
    content.add_row(Text())
    content.add_row(Text("  Ctrl+C to quit  │  Refreshes every 3s", style="dim"))

    return Panel(
        content,
        title="[bold cyan] EPSTEIN PROJECT — DOWNLOAD DASHBOARD [/bold cyan]",
        border_style="cyan",
        expand=True,
    )


def run_live(refresh: int = REFRESH_INTERVAL):
    """Run the live dashboard."""
    console = Console()
    with Live(build_dashboard(), console=console, refresh_per_second=1 / refresh) as live:
        try:
            while True:
                live.update(build_dashboard())
                time.sleep(refresh)
        except KeyboardInterrupt:
            pass


def run_once():
    """Print a single snapshot."""
    console = Console()
    console.print(build_dashboard())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Live download dashboard")
    parser.add_argument("--refresh", type=int, default=REFRESH_INTERVAL,
                        help="Refresh interval in seconds")
    parser.add_argument("--once", action="store_true",
                        help="Single snapshot (no loop)")
    args = parser.parse_args()

    if args.once:
        run_once()
    else:
        run_live(args.refresh)
