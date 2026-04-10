#!/usr/bin/env python3
"""
Epstein Project - Download & Processing Progress Tracker (SQLite-backed)

Multi-process-safe progress tracker using SQLite WAL mode.
Multiple workers can register, update, and query tasks concurrently
without corruption.

Usage:
  # Monitor (reads state, refreshes every 2s)
  python3 tracker.py watch

  # Register a download task
  python3 tracker.py register --id raw-ds1 --label "Dataset 1" --expected 15000

  # Update progress
  python3 tracker.py update --id raw-ds1 --current 3200

  # Mark done
  python3 tracker.py done --id raw-ds1

  # Snapshot (one-shot print)
  python3 tracker.py snapshot
"""

import argparse
import os
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# =============================================================================
# Configuration Constants
# =============================================================================

DB_PATH = "/home/cbwinslow/workspace/epstein-data/logs/progress.db"
DB_TIMEOUT = 10          # SQLite lock wait timeout (seconds)
HISTORY_LIMIT = 10       # Max history samples kept per task for rate calculation
REFRESH_INTERVAL = 2.0   # Watch mode refresh interval (seconds)


# =============================================================================
# Database Layer
# =============================================================================

def get_conn() -> sqlite3.Connection:
    """Open SQLite connection with WAL mode and create tables if needed.

    Returns:
        sqlite3.Connection: Open connection with WAL journal mode enabled.
    """
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")

    # Create tasks table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            type TEXT DEFAULT 'download',
            expected INTEGER DEFAULT 0,
            current INTEGER DEFAULT 0,
            rate_bps REAL DEFAULT 0,
            status TEXT DEFAULT 'running',
            started_at TEXT,
            last_update TEXT,
            finished_at TEXT
        )
    """)

    # Create history table for rate calculation
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            ts TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_history_task_ts
        ON task_history (task_id, ts DESC)
    """)

    conn.commit()
    return conn


# =============================================================================
# Task Operations
# =============================================================================

def register_task(task_id: str, label: str, expected: int = 0,
                  task_type: str = "download") -> None:
    """Register a new task or update an existing one.

    Args:
        task_id: Unique identifier for the task (e.g., 'doj-ds1').
        label: Human-readable label (e.g., 'DOJ Dataset 1').
        expected: Expected total count (e.g., file count).
        task_type: Task category (e.g., 'download', 'ocr', 'kg').
    """
    conn = None
    try:
        conn = get_conn()
        now = datetime.now().isoformat()
        conn.execute(
            "INSERT OR REPLACE INTO tasks "
            "(id, label, type, expected, current, rate_bps, status, started_at, last_update) "
            "VALUES (?, ?, ?, ?, 0, 0.0, 'running', ?, ?)",
            (task_id, label, task_type, expected, now, now)
        )
        conn.commit()
        print(f"Registered: {task_id} ({label})")
    except sqlite3.Error as e:
        print(f"Error registering task {task_id}: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()


def update_task(task_id: str, current: int) -> None:
    """Update task progress count and recalculate rate.

    Args:
        task_id: Task identifier to update.
        current: Current progress value (e.g., files downloaded so far).
    """
    conn = None
    try:
        conn = get_conn()
        now = datetime.now().isoformat()

        # Update the task's current count
        conn.execute(
            "UPDATE tasks SET current = ?, last_update = ? WHERE id = ?",
            (current, now, task_id)
        )

        # Append to history for rate calculation
        conn.execute(
            "INSERT INTO task_history (task_id, ts, value) VALUES (?, ?, ?)",
            (task_id, now, current)
        )

        # Prune old history (keep only last N samples)
        conn.execute(
            "DELETE FROM task_history WHERE task_id = ? AND id NOT IN ("
            "  SELECT id FROM task_history WHERE task_id = ? ORDER BY ts DESC LIMIT ?"
            ")",
            (task_id, task_id, HISTORY_LIMIT)
        )

        conn.commit()

        # Calculate rate from history
        _recalculate_rate(conn, task_id)

    except sqlite3.Error as e:
        print(f"Error updating task {task_id}: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()


def _recalculate_rate(conn: sqlite3.Connection, task_id: str) -> None:
    """Calculate rate from history samples and update the task row.

    Args:
        conn: Open database connection.
        task_id: Task identifier.
    """
    try:
        rows = conn.execute(
            "SELECT ts, value FROM task_history "
            "WHERE task_id = ? ORDER BY ts ASC LIMIT ?",
            (task_id, HISTORY_LIMIT)
        ).fetchall()

        if len(rows) < 2:
            return

        t0 = datetime.fromisoformat(rows[0][0])
        t1 = datetime.fromisoformat(rows[-1][0])
        v0 = rows[0][1]
        v1 = rows[-1][1]
        dt = (t1 - t0).total_seconds()

        if dt > 0:
            rate = round((v1 - v0) / dt, 2)
            conn.execute(
                "UPDATE tasks SET rate_bps = ? WHERE id = ?",
                (rate, task_id)
            )
            conn.commit()
    except (sqlite3.Error, ValueError) as e:
        print(f"Error calculating rate for {task_id}: {e}", file=sys.stderr)


def done_task(task_id: str, status: str = "completed") -> None:
    """Mark a task as completed or failed.

    Args:
        task_id: Task identifier.
        status: Final status ('completed', 'failed', 'cancelled').
    """
    conn = None
    try:
        conn = get_conn()
        now = datetime.now().isoformat()
        conn.execute(
            "UPDATE tasks SET status = ?, finished_at = ? WHERE id = ?",
            (status, now, task_id)
        )
        conn.commit()
        print(f"Marked {task_id} as {status}")
    except sqlite3.Error as e:
        print(f"Error marking task {task_id} done: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()


def get_tasks() -> dict:
    """Retrieve all tasks as a dictionary keyed by task ID.

    Returns:
        dict: Task data keyed by task_id, matching original JSON structure.
    """
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute(
            "SELECT id, label, type, expected, current, rate_bps, "
            "status, started_at, last_update, finished_at "
            "FROM tasks ORDER BY id"
        ).fetchall()

        tasks = {}
        for row in rows:
            tasks[row[0]] = {
                "label": row[1],
                "type": row[2],
                "expected": row[3],
                "current": row[4],
                "rate_bps": row[5],
                "status": row[6],
                "started_at": row[7],
                "last_update": row[8],
                "finished_at": row[9],
            }
        return tasks
    except sqlite3.Error as e:
        print(f"Error reading tasks: {e}", file=sys.stderr)
        return {}
    finally:
        if conn:
            conn.close()


# =============================================================================
# Display / Formatting
# =============================================================================

def format_bytes(b) -> str:
    """Format byte count to human-readable string.

    Args:
        b: Byte count (int or float).

    Returns:
        Formatted string (e.g., '1.5 GB').
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(b) < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"


def format_rate(bps: float) -> str:
    """Format rate in items/sec.

    Args:
        bps: Items per second.

    Returns:
        Formatted string (e.g., '3.2 /s') or '---' if zero.
    """
    if bps <= 0:
        return "---"
    return f"{bps:.1f} /s"


def format_eta(current: int, expected: int, bps: float) -> str:
    """Estimate time remaining.

    Args:
        current: Current progress value.
        expected: Target value.
        bps: Current rate (items per second).

    Returns:
        Human-readable ETA string or '---'.
    """
    if bps <= 0 or expected <= 0 or current >= expected:
        return "---"
    remaining = expected - current
    secs = remaining / bps
    td = timedelta(seconds=int(secs))
    if td.days > 0:
        return f"{td.days}d {td.seconds // 3600}h"
    elif td.seconds >= 3600:
        return f"{td.seconds // 3600}h {(td.seconds % 3600) // 60}m"
    elif td.seconds >= 60:
        return f"{td.seconds // 60}m {td.seconds % 60}s"
    else:
        return f"{td.seconds}s"


def render_bar(pct: float, width: int = 30) -> str:
    """Render a text-based progress bar.

    Args:
        pct: Percentage (0-100).
        width: Bar width in characters.

    Returns:
        String like '[████████░░░░░░░░]'.
    """
    filled = int(width * min(pct, 100) / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"


def snapshot() -> None:
    """Print a formatted progress snapshot for all tasks."""
    tasks = get_tasks()

    if not tasks:
        print("No tasks registered.")
        return

    now = datetime.now()
    print(f"\n{'=' * 78}")
    print("  EPSTEIN PROJECT PROGRESS")
    print(f"  Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 78}")

    total_expected = 0
    total_current = 0

    for tid, t in tasks.items():
        label = t["label"]
        status = t["status"]
        current = t["current"]
        expected = t["expected"]
        bps = t.get("rate_bps", 0)

        total_expected += expected
        total_current += current

        pct = (current / expected * 100) if expected > 0 else 0
        icon = "✓" if status == "completed" else "✗" if status == "failed" else "●"
        bar = render_bar(pct)
        rate_str = format_rate(bps)
        eta_str = format_eta(current, expected, bps)

        # Staleness check
        last_update = t.get("last_update")
        stale = ""
        if last_update and status == "running":
            try:
                last = datetime.fromisoformat(last_update)
                stale_secs = (now - last).total_seconds()
                if stale_secs > 60:
                    stale = " STALE"
            except ValueError:
                pass

        print(f"\n  {icon} {label:<30} [{status}]{stale}")
        print(f"    {bar} {pct:5.1f}%")
        print(f"    {current:>10,} / {expected:<10,}  {rate_str:>12}  ETA: {eta_str}")

    # Overall progress
    if total_expected > 0:
        overall_pct = total_current / total_expected * 100
        print(f"\n{'─' * 78}")
        print(f"  OVERALL: {render_bar(overall_pct)} {overall_pct:.1f}%")
        print(f"  {total_current:,} / {total_expected:,}")

    print(f"{'=' * 78}\n")


def watch(refresh: float = REFRESH_INTERVAL) -> None:
    """Continuously display progress, refreshing at the given interval.

    Args:
        refresh: Seconds between display refreshes.
    """
    try:
        while True:
            os.system("clear")
            snapshot()
            print(f"  Refreshing every {refresh}s. Ctrl+C to stop.")
            time.sleep(refresh)
    except KeyboardInterrupt:
        print("\nStopped.")


def scan_directory(task_id: str, label: str, directory: str,
                   pattern: str = "*.pdf") -> None:
    """Scan a directory and register/update a task with file counts.

    Args:
        task_id: Task identifier.
        label: Human-readable label.
        directory: Directory path to scan.
        pattern: Glob pattern for file matching.
    """
    try:
        files = list(Path(directory).rglob(pattern))
        total_size = sum(f.stat().st_size for f in files if f.exists())
        register_task(task_id, label, expected=len(files))
        update_task(task_id, len(files))
        print(f"  Found {len(files)} files, {format_bytes(total_size)}")
    except OSError as e:
        print(f"Error scanning {directory}: {e}", file=sys.stderr)


# =============================================================================
# CLI Entry Point
# =============================================================================

def main() -> None:
    """Parse CLI arguments and dispatch to the appropriate handler."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "watch":
        watch()
    elif cmd == "snapshot":
        snapshot()
    elif cmd == "register":
        p = argparse.ArgumentParser(description="Register a new task")
        p.add_argument("--id", required=True, help="Task identifier")
        p.add_argument("--label", required=True, help="Human-readable label")
        p.add_argument("--expected", type=int, default=0, help="Expected total")
        p.add_argument("--type", default="download", help="Task type")
        args = p.parse_args(sys.argv[2:])
        register_task(args.id, args.label, args.expected, args.type)
    elif cmd == "update":
        p = argparse.ArgumentParser(description="Update task progress")
        p.add_argument("--id", required=True, help="Task identifier")
        p.add_argument("--current", type=int, required=True, help="Current value")
        args = p.parse_args(sys.argv[2:])
        update_task(args.id, args.current)
    elif cmd == "done":
        p = argparse.ArgumentParser(description="Mark task as done")
        p.add_argument("--id", required=True, help="Task identifier")
        p.add_argument("--status", default="completed",
                       choices=["completed", "failed", "cancelled"],
                       help="Final status")
        args = p.parse_args(sys.argv[2:])
        done_task(args.id, args.status)
    elif cmd == "scan":
        p = argparse.ArgumentParser(description="Scan directory and register task")
        p.add_argument("--id", required=True, help="Task identifier")
        p.add_argument("--label", required=True, help="Human-readable label")
        p.add_argument("--dir", required=True, help="Directory to scan")
        p.add_argument("--pattern", default="*.pdf", help="File glob pattern")
        args = p.parse_args(sys.argv[2:])
        scan_directory(args.id, args.label, args.dir, args.pattern)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
