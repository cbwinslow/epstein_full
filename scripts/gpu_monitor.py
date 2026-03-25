#!/usr/bin/env python3
"""
GPU Temperature and Utilization Monitor

Monitors NVIDIA GPU temperature, power, memory, and utilization.
Supports continuous monitoring with configurable thresholds and alerts.

Usage:
  python gpu_monitor.py                    # One-shot snapshot
  python gpu_monitor.py --watch            # Continuous monitoring (5s refresh)
  python gpu_monitor.py --watch --refresh 2 # 2s refresh
  python gpu_monitor.py --alert 80         # Alert if temp > 80°C
  python gpu_monitor.py --json             # JSON output for scripting

Requirements:
  - nvidia-smi (installed with NVIDIA drivers)
  - Python 3.10+
"""

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

# =============================================================================
# Configuration
# =============================================================================

# Temperature thresholds (Celsius)
TEMP_WARN = 75       # Warning threshold
TEMP_CRITICAL = 85   # Critical threshold
TEMP_SHUTDOWN = 90   # Shutdown threshold

# Default refresh interval (seconds)
DEFAULT_REFRESH = 5


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class GPUInfo:
    """Snapshot of GPU state."""
    index: int
    name: str
    temperature_gpu: int           # °C
    temperature_memory: Optional[int]  # °C (may be N/A)
    power_draw: float              # Watts
    power_limit: float             # Watts
    fan_speed: Optional[int]       # % (may be N/A on Tesla)
    memory_used: int               # MiB
    memory_total: int              # MiB
    memory_percent: float          # %
    gpu_utilization: int           # %
    timestamp: str

    @property
    def temp_status(self) -> str:
        if self.temperature_gpu >= TEMP_SHUTDOWN:
            return "SHUTDOWN"
        elif self.temperature_gpu >= TEMP_CRITICAL:
            return "CRITICAL"
        elif self.temperature_gpu >= TEMP_WARN:
            return "WARNING"
        else:
            return "OK"


# =============================================================================
# GPU Query
# =============================================================================

def query_gpus() -> list[GPUInfo]:
    """Query all NVIDIA GPUs using nvidia-smi.

    Returns:
        List of GPUInfo objects, one per GPU.

    Raises:
        RuntimeError: If nvidia-smi is not available or fails.
    """
    # Check nvidia-smi exists
    try:
        subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                       capture_output=True, check=True)
    except FileNotFoundError:
        raise RuntimeError(
            "nvidia-smi not found. Install NVIDIA drivers or check PATH."
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"nvidia-smi failed: {e.stderr.decode().strip()}")

    # Query GPU state
    query_fields = (
        "name,"
        "temperature.gpu,"
        "temperature.memory,"
        "power.draw,"
        "power.limit,"
        "fan.speed,"
        "memory.used,"
        "memory.total,"
        "utilization.gpu"
    )

    try:
        result = subprocess.run(
            ["nvidia-smi",
             f"--query-gpu={query_fields}",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"nvidia-smi query failed: {e.stderr.strip()}")

    gpus = []
    now = datetime.now().isoformat()

    for idx, line in enumerate(result.stdout.strip().split("\n")):
        parts = [p.strip() for p in line.split(",")]

        if len(parts) < 9:
            continue

        # Parse fields (handle "N/A" values)
        def safe_int(val, default=0):
            try:
                return int(val)
            except (ValueError, TypeError):
                return default

        def safe_float(val, default=0.0):
            try:
                return float(val)
            except (ValueError, TypeError):
                return default

        mem_used = safe_int(parts[6])
        mem_total = safe_int(parts[7])
        mem_pct = (mem_used / mem_total * 100) if mem_total > 0 else 0.0

        gpu = GPUInfo(
            index=idx,
            name=parts[0],
            temperature_gpu=safe_int(parts[1]),
            temperature_memory=safe_int(parts[2]) if parts[2] != "[N/A]" else None,
            power_draw=safe_float(parts[3]),
            power_limit=safe_float(parts[4]),
            fan_speed=safe_int(parts[5]) if parts[5] != "[N/A]" else None,
            memory_used=mem_used,
            memory_total=mem_total,
            memory_percent=round(mem_pct, 1),
            gpu_utilization=safe_int(parts[8]),
            timestamp=now,
        )
        gpus.append(gpu)

    return gpus


# =============================================================================
# Display
# =============================================================================

def format_gpu_card(gpu: GPUInfo) -> str:
    """Format a single GPU as a readable card."""
    status_icon = {
        "OK": "✓",
        "WARNING": "⚠",
        "CRITICAL": "🔴",
        "SHUTDOWN": "💀",
    }.get(gpu.temp_status, "?")

    lines = [
        f"  {status_icon} GPU {gpu.index}: {gpu.name}",
        f"    Temp:    {gpu.temperature_gpu}°C  [{gpu.temp_status}]",
    ]

    if gpu.temperature_memory is not None:
        lines.append(f"    Mem Temp: {gpu.temperature_memory}°C")

    lines.extend([
        f"    Power:   {gpu.power_draw:.0f}W / {gpu.power_limit:.0f}W ({gpu.power_draw/gpu.power_limit*100:.0f}%)",
        f"    Memory:  {gpu.memory_used:,} / {gpu.memory_total:,} MiB ({gpu.memory_percent:.1f}%)",
        f"    GPU Util:{gpu.gpu_utilization}%",
    ])

    if gpu.fan_speed is not None:
        lines.append(f"    Fan:     {gpu.fan_speed}%")

    return "\n".join(lines)


def snapshot(gpus: list[GPUInfo]) -> str:
    """Format a full snapshot of all GPUs."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"\n{'=' * 60}",
        f"  GPU MONITOR — {now}",
        f"{'=' * 60}",
    ]

    for gpu in gpus:
        lines.append("")
        lines.append(format_gpu_card(gpu))

    lines.append(f"\n{'=' * 60}\n")
    return "\n".join(lines)


def watch(refresh: int = DEFAULT_REFRESH, alert_temp: Optional[int] = None):
    """Continuous monitoring loop.

    Args:
        refresh: Seconds between updates.
        alert_temp: Alert threshold temperature (None to use defaults).
    """
    try:
        while True:
            os.system("clear")
            gpus = query_gpus()
            print(snapshot(gpus))

            # Temperature alerts
            for gpu in gpus:
                threshold = alert_temp or TEMP_WARN
                if gpu.temperature_gpu >= threshold:
                    print(f"  ⚠️  ALERT: GPU {gpu.index} at {gpu.temperature_gpu}°C!")

            print(f"  Refreshing every {refresh}s. Ctrl+C to stop.")
            time.sleep(refresh)

    except KeyboardInterrupt:
        print("\nMonitor stopped.")


def get_json(gpus: list[GPUInfo]) -> str:
    """Return GPU state as JSON string."""
    return json.dumps([asdict(g) for g in gpus], indent=2)


# =============================================================================
# Health Check
# =============================================================================

def health_check(gpus: list[GPUInfo]) -> dict:
    """Run a health check and return status.

    Returns:
        Dict with 'healthy' (bool), 'warnings' (list), 'critical' (list).
    """
    warnings = []
    critical = []

    for gpu in gpus:
        if gpu.temperature_gpu >= TEMP_CRITICAL:
            critical.append(f"GPU {gpu.index} ({gpu.name}): {gpu.temperature_gpu}°C")
        elif gpu.temperature_gpu >= TEMP_WARN:
            warnings.append(f"GPU {gpu.index} ({gpu.name}): {gpu.temperature_gpu}°C")

        if gpu.memory_percent > 95:
            critical.append(f"GPU {gpu.index}: memory at {gpu.memory_percent}%")
        elif gpu.memory_percent > 85:
            warnings.append(f"GPU {gpu.index}: memory at {gpu.memory_percent}%")

    return {
        "healthy": len(critical) == 0,
        "warnings": warnings,
        "critical": critical,
        "gpus": len(gpus),
        "timestamp": datetime.now().isoformat(),
    }


# =============================================================================
# Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="NVIDIA GPU temperature and utilization monitor"
    )
    parser.add_argument(
        "--watch", action="store_true",
        help="Continuous monitoring mode"
    )
    parser.add_argument(
        "--refresh", type=int, default=DEFAULT_REFRESH,
        help=f"Refresh interval in seconds (default: {DEFAULT_REFRESH})"
    )
    parser.add_argument(
        "--alert", type=int, default=None,
        help=f"Alert threshold temperature (default: {TEMP_WARN}°C)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--health", action="store_true",
        help="Run health check and exit with code"
    )

    args = parser.parse_args()

    try:
        gpus = query_gpus()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not gpus:
        print("No NVIDIA GPUs detected.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(get_json(gpus))
    elif args.health:
        health = health_check(gpus)
        print(json.dumps(health, indent=2))
        sys.exit(0 if health["healthy"] else 1)
    elif args.watch:
        watch(refresh=args.refresh, alert_temp=args.alert)
    else:
        print(snapshot(gpus))


# Import os for watch()
import os

if __name__ == "__main__":
    main()
