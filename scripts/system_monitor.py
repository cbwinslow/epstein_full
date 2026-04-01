#!/usr/bin/env python3
"""
System Monitor — Combined GPU + CPU + Disk + Processes Dashboard

Unified monitoring dashboard that combines GPU temperature, CPU temperature,
load, memory, disk usage, and running processes into a single view.

Usage:
  python system_monitor.py                    # One-shot snapshot
  python system_monitor.py --watch            # Continuous monitoring
  python system_monitor.py --watch --refresh 3 # 3s refresh
  python system_monitor.py --health           # Health check (exit code 0/1)
  python system_monitor.py --json             # JSON output
  python system_monitor.py --alert-temp 80    # Custom alert threshold

Requirements:
  - nvidia-smi (for GPU monitoring)
  - lm-sensors (for CPU temperature)
  - Python 3.10+
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

# Import our monitors
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpu_monitor import get_cpu_info
from cpu_monitor import health_check as cpu_health
from gpu_monitor import health_check as gpu_health
from gpu_monitor import query_gpus

# =============================================================================
# Configuration
# =============================================================================

DEFAULT_REFRESH = 5
DISK_WARN_PCT = 85
DISK_CRITICAL_PCT = 95


# =============================================================================
# Disk Monitoring
# =============================================================================

def get_disk_info(path: str = "/") -> dict:
    """Get disk usage for a mount point.

    Args:
        path: Mount point to check.

    Returns:
        Dict with total_gb, used_gb, free_gb, percent, path.
    """
    try:
        st = os.statvfs(path)
        total = st.f_blocks * st.f_frsize
        free = st.f_bfree * st.f_frsize
        used = total - free
        pct = (used / total * 100) if total > 0 else 0.0

        return {
            "path": path,
            "total_gb": round(total / (1024**3), 1),
            "used_gb": round(used / (1024**3), 1),
            "free_gb": round(free / (1024**3), 1),
            "percent": round(pct, 1),
            "status": "CRITICAL" if pct >= DISK_CRITICAL_PCT
                      else "WARNING" if pct >= DISK_WARN_PCT
                      else "OK",
        }
    except OSError as e:
        return {"path": path, "error": str(e)}


# =============================================================================
# Process Monitoring
# =============================================================================

def get_processes(name_pattern: str = None) -> list[dict]:
    """Get running processes matching a pattern.

    Args:
        name_pattern: Grep pattern for process name (optional).

    Returns:
        List of dicts with pid, name, cpu%, mem%.
    """
    try:
        cmd = ["ps", "aux", "--sort=-%cpu"]
        if name_pattern:
            cmd = ["ps", "aux", "--sort=-%cpu"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            lines = [l for l in result.stdout.split("\n") if name_pattern.lower() in l.lower()]
        else:
            result = subprocess.run(cmd + ["--no-headers"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")[:10]  # Top 10

        procs = []
        for line in lines:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                procs.append({
                    "user": parts[0],
                    "pid": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3],
                    "command": parts[10][:80],
                })
        return procs
    except Exception:
        return []


import subprocess

# =============================================================================
# Display
# =============================================================================

def render_bar(pct: float, width: int = 20) -> str:
    """Render a progress bar."""
    filled = int(width * min(pct, 100) / 100)
    return "█" * filled + "░" * (width - filled)


def snapshot() -> str:
    """Full system snapshot."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"\n{'═' * 70}",
        f"  SYSTEM MONITOR — {now}",
        f"{'═' * 70}",
    ]

    # GPU
    try:
        gpus = query_gpus()
        lines.append("")
        lines.append("  ┌─ GPU ─────────────────────────────────────────────┐")
        for gpu in gpus:
            icon = {"OK": "✓", "WARNING": "⚠", "CRITICAL": "🔴", "SHUTDOWN": "💀"}.get(gpu.temp_status, "?")
            bar = render_bar(gpu.gpu_utilization, 15)
            lines.append(f"  │ {icon} GPU{gpu.index} {gpu.name:<25} {gpu.temperature_gpu:>3}°C  [{bar}] {gpu.gpu_utilization:>3}%")
            lines.append(f"  │   Mem: {gpu.memory_used:>6}/{gpu.memory_total} MiB  Power: {gpu.power_draw:.0f}W")
        lines.append("  └────────────────────────────────────────────────────┘")
    except RuntimeError:
        lines.append("  GPU: not available")

    # CPU
    try:
        cpu = get_cpu_info()
        temp_str = f"{cpu.temperature:.0f}°C" if cpu.temperature else "N/A"
        icon = {"OK": "✓", "WARNING": "⚠", "CRITICAL": "🔴"}.get(cpu.temp_status, "?")
        mem_bar = render_bar(cpu.memory_percent, 15)
        load_bar = render_bar(cpu.load_percent, 15)

        lines.extend([
            "",
            "  ┌─ CPU ──────────────────────────────────────────────┐",
            f"  │ {icon} {cpu.model_name[:45]}",
            f"  │   {cpu.cores_logical} cores  Temp: {temp_str}  Uptime: {int(cpu.uptime_seconds//3600)}h",
            f"  │   Load: [{load_bar}] {cpu.load_percent:.1f}%",
            f"  │   Mem:  [{mem_bar}] {cpu.memory_used_gb:.1f}/{cpu.memory_total_gb:.1f} GB ({cpu.memory_percent:.1f}%)",
            f"  │   Swap: {cpu.swap_used_gb:.1f}/{cpu.swap_total_gb:.1f} GB",
            "  └────────────────────────────────────────────────────┘",
        ])
    except Exception as e:
        lines.append(f"  CPU: error - {e}")

    # Disk
    lines.extend([
        "",
        "  ┌─ DISK ─────────────────────────────────────────────┐",
    ])
    for path in ["/", "/mnt/data"]:
        disk = get_disk_info(path)
        if "error" not in disk:
            icon = {"OK": "✓", "WARNING": "⚠", "CRITICAL": "🔴"}.get(disk["status"], "?")
            bar = render_bar(disk["percent"], 15)
            lines.append(f"  │ {icon} {path:<20} [{bar}] {disk['percent']}%  {disk['free_gb']:.0f}GB free")
        else:
            lines.append(f"  │ {path}: {disk['error']}")
    lines.append("  └────────────────────────────────────────────────────┘")

    # Active processes
    lines.extend([
        "",
        "  ┌─ PROCESSES ─────────────────────────────────────────┐",
    ])
    procs = get_processes("download|aria2c|python")
    if procs:
        for p in procs[:8]:
            lines.append(f"  │ {p['pid']:>7} {p['cpu']:>5}% CPU  {p['mem']:>5}% MEM  {p['command'][:50]}")
    else:
        lines.append("  │ No matching processes")
    lines.append("  └────────────────────────────────────────────────────┘")

    lines.append(f"\n{'═' * 70}\n")
    return "\n".join(lines)


def health_check() -> dict:
    """Combined health check for all components."""
    gpu_ok = True
    cpu_ok = True
    disk_ok = True
    warnings = []
    critical = []

    # GPU
    try:
        gpus = query_gpus()
        gh = gpu_health(gpus)
        warnings.extend(gh["warnings"])
        critical.extend(gh["critical"])
        gpu_ok = gh["healthy"]
    except RuntimeError:
        warnings.append("GPU monitoring unavailable")

    # CPU
    try:
        cpu = get_cpu_info()
        ch = cpu_health(cpu)
        warnings.extend(ch["warnings"])
        critical.extend(ch["critical"])
        cpu_ok = ch["healthy"]
    except Exception:
        warnings.append("CPU monitoring unavailable")

    # Disk
    for path in ["/", "/mnt/data"]:
        disk = get_disk_info(path)
        if "error" not in disk:
            if disk["status"] == "CRITICAL":
                critical.append(f"Disk {path}: {disk['percent']}% used")
                disk_ok = False
            elif disk["status"] == "WARNING":
                warnings.append(f"Disk {path}: {disk['percent']}% used")

    return {
        "healthy": gpu_ok and cpu_ok and disk_ok,
        "warnings": warnings,
        "critical": critical,
        "timestamp": datetime.now().isoformat(),
    }


def watch(refresh: int = DEFAULT_REFRESH):
    """Continuous monitoring loop."""
    try:
        while True:
            os.system("clear")
            print(snapshot())
            print(f"  Refreshing every {refresh}s. Ctrl+C to stop.")
            time.sleep(refresh)
    except KeyboardInterrupt:
        print("\nMonitor stopped.")


def main():
    parser = argparse.ArgumentParser(description="Combined system monitor")
    parser.add_argument("--watch", action="store_true", help="Continuous mode")
    parser.add_argument("--refresh", type=int, default=DEFAULT_REFRESH)
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--health", action="store_true", help="Health check")

    args = parser.parse_args()

    if args.health:
        health = health_check()
        print(json.dumps(health, indent=2))
        sys.exit(0 if health["healthy"] else 1)
    elif args.json:
        data = {
            "gpu": [g.__dict__ for g in query_gpus()],
            "cpu": get_cpu_info().__dict__,
            "disk": {p: get_disk_info(p) for p in ["/", "/mnt/data"]},
        }
        print(json.dumps(data, indent=2, default=str))
    elif args.watch:
        watch(refresh=args.refresh)
    else:
        print(snapshot())


if __name__ == "__main__":
    main()
