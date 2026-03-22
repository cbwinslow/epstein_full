#!/usr/bin/env python3
"""
CPU Temperature, Load, and Memory Monitor

Monitors CPU temperature (via lm-sensors), load average, per-core usage,
and memory utilization. Supports continuous monitoring with alerts.

Usage:
  python cpu_monitor.py                    # One-shot snapshot
  python cpu_monitor.py --watch            # Continuous monitoring
  python cpu_monitor.py --watch --refresh 3 # 3s refresh
  python cpu_monitor.py --alert 80         # Alert if temp > 80°C
  python cpu_monitor.py --json             # JSON output

Requirements:
  - lm-sensors (sudo apt install lm-sensors)
  - Python 3.10+
"""

import subprocess
import json
import os
import sys
import time
import argparse
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional


# =============================================================================
# Configuration
# =============================================================================

TEMP_WARN = 75
TEMP_CRITICAL = 85
LOAD_WARN_PCT = 80    # % of cores
MEM_WARN_PCT = 85
MEM_CRITICAL_PCT = 95
DEFAULT_REFRESH = 5


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class CPUInfo:
    """CPU state snapshot."""
    cores_physical: int
    cores_logical: int
    model_name: str
    temperature: Optional[float]       # °C (from sensors)
    load_1min: float
    load_5min: float
    load_15min: float
    load_percent: float                # % of total cores
    memory_total_gb: float
    memory_used_gb: float
    memory_available_gb: float
    memory_percent: float
    swap_total_gb: float
    swap_used_gb: float
    swap_percent: float
    uptime_seconds: float
    timestamp: str

    @property
    def temp_status(self) -> str:
        if self.temperature is None:
            return "N/A"
        if self.temperature >= TEMP_CRITICAL:
            return "CRITICAL"
        elif self.temperature >= TEMP_WARN:
            return "WARNING"
        return "OK"

    @property
    def load_status(self) -> str:
        if self.load_percent >= LOAD_WARN_PCT:
            return "HIGH"
        return "OK"

    @property
    def mem_status(self) -> str:
        if self.memory_percent >= MEM_CRITICAL_PCT:
            return "CRITICAL"
        elif self.memory_percent >= MEM_WARN_PCT:
            return "WARNING"
        return "OK"


# =============================================================================
# Data Collection
# =============================================================================

def get_cpu_info() -> CPUInfo:
    """Collect CPU information from /proc and sensors.

    Returns:
        CPUInfo object with current state.

    Raises:
        RuntimeError: If critical system files are unreadable.
    """
    now = datetime.now().isoformat()

    # CPU cores
    cores_logical = os.cpu_count() or 1
    cores_physical = _get_physical_cores()

    # Model name
    model_name = _get_cpu_model()

    # Temperature (from lm-sensors)
    temperature = _get_cpu_temperature()

    # Load average
    try:
        with open("/proc/loadavg", "r") as f:
            parts = f.read().split()
            load_1 = float(parts[0])
            load_5 = float(parts[1])
            load_15 = float(parts[2])
    except (IOError, IndexError, ValueError):
        load_1 = load_5 = load_15 = 0.0

    load_pct = (load_1 / cores_logical * 100) if cores_logical > 0 else 0.0

    # Memory
    mem = _get_memory_info()

    # Uptime
    uptime = _get_uptime()

    return CPUInfo(
        cores_physical=cores_physical,
        cores_logical=cores_logical,
        model_name=model_name,
        temperature=temperature,
        load_1min=load_1,
        load_5min=load_5,
        load_15min=load_15,
        load_percent=round(load_pct, 1),
        memory_total_gb=mem["total_gb"],
        memory_used_gb=mem["used_gb"],
        memory_available_gb=mem["available_gb"],
        memory_percent=mem["percent"],
        swap_total_gb=mem["swap_total_gb"],
        swap_used_gb=mem["swap_used_gb"],
        swap_percent=mem["swap_percent"],
        uptime_seconds=uptime,
        timestamp=now,
    )


def _get_physical_cores() -> int:
    """Get physical CPU core count."""
    try:
        result = subprocess.run(
            ["lscpu"], capture_output=True, text=True, check=True
        )
        for line in result.stdout.split("\n"):
            if "Core(s) per socket" in line:
                cores = int(line.split(":")[1].strip())
                sockets = 1
                for l in result.stdout.split("\n"):
                    if "Socket(s)" in l:
                        sockets = int(l.split(":")[1].strip())
                return cores * sockets
    except (subprocess.CalledProcessError, ValueError):
        pass
    return os.cpu_count() or 1


def _get_cpu_model() -> str:
    """Get CPU model name."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":")[1].strip()
    except IOError:
        pass
    return "Unknown"


def _get_cpu_temperature() -> Optional[float]:
    """Get CPU temperature from lm-sensors or sysfs.

    Returns:
        Temperature in Celsius, or None if unavailable.
    """
    # Try lm-sensors first
    try:
        result = subprocess.run(
            ["sensors", "-j"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # Look for coretemp or similar
            for chip_name, chip_data in data.items():
                if "core" in chip_name.lower() or "temp" in chip_name.lower():
                    for key, val in chip_data.items():
                        if isinstance(val, dict):
                            for k, v in val.items():
                                if "input" in k and isinstance(v, (int, float)):
                                    return float(v)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass

    # Try sysfs thermal zones
    for i in range(10):
        path = f"/sys/class/thermal/thermal_zone{i}/temp"
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    raw = int(f.read().strip())
                    return raw / 1000.0  # millidegrees to degrees
            except (IOError, ValueError):
                continue

    return None


def _get_memory_info() -> dict:
    """Parse /proc/meminfo for memory statistics."""
    result = {
        "total_gb": 0.0, "used_gb": 0.0, "available_gb": 0.0,
        "percent": 0.0, "swap_total_gb": 0.0, "swap_used_gb": 0.0,
        "swap_percent": 0.0,
    }

    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()

        mem = {}
        for line in lines:
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip().split()[0]
                mem[key] = int(val) * 1024  # kB to bytes

        total = mem.get("MemTotal", 0)
        available = mem.get("MemAvailable", 0)
        used = total - available
        swap_total = mem.get("SwapTotal", 0)
        swap_free = mem.get("SwapFree", 0)
        swap_used = swap_total - swap_free

        result = {
            "total_gb": round(total / (1024**3), 1),
            "used_gb": round(used / (1024**3), 1),
            "available_gb": round(available / (1024**3), 1),
            "percent": round(used / total * 100, 1) if total > 0 else 0.0,
            "swap_total_gb": round(swap_total / (1024**3), 1),
            "swap_used_gb": round(swap_used / (1024**3), 1),
            "swap_percent": round(swap_used / swap_total * 100, 1) if swap_total > 0 else 0.0,
        }
    except (IOError, ValueError):
        pass

    return result


def _get_uptime() -> float:
    """Get system uptime in seconds."""
    try:
        with open("/proc/uptime", "r") as f:
            return float(f.read().split()[0])
    except (IOError, IndexError, ValueError):
        return 0.0


# =============================================================================
# Display
# =============================================================================

def format_uptime(seconds: float) -> str:
    """Format uptime as human-readable string."""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    mins = int((seconds % 3600) // 60)
    if days > 0:
        return f"{days}d {hours}h {mins}m"
    elif hours > 0:
        return f"{hours}h {mins}m"
    else:
        return f"{mins}m"


def render_bar(pct: float, width: int = 20, warn: float = 80, critical: float = 90) -> str:
    """Render a colored progress bar."""
    filled = int(width * min(pct, 100) / 100)
    if pct >= critical:
        char = "█"
    elif pct >= warn:
        char = "▓"
    else:
        char = "█"
    return char * filled + "░" * (width - filled)


def snapshot(cpu: CPUInfo) -> str:
    """Format a CPU snapshot."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"\n{'=' * 60}",
        f"  CPU MONITOR — {now}",
        f"{'=' * 60}",
        f"  {cpu.model_name}",
        f"  {cpu.cores_physical} physical / {cpu.cores_logical} logical cores",
        f"  Uptime: {format_uptime(cpu.uptime_seconds)}",
        "",
    ]

    # Temperature
    if cpu.temperature is not None:
        icon = {"OK": "✓", "WARNING": "⚠", "CRITICAL": "🔴"}.get(cpu.temp_status, "?")
        temp_bar = render_bar(cpu.temperature, 20, TEMP_WARN, TEMP_CRITICAL)
        lines.append(f"  {icon} Temperature: {cpu.temperature:.0f}°C  [{temp_bar}]")
    else:
        lines.append("  Temperature: N/A (install lm-sensors)")

    # Load
    load_icon = "⚠" if cpu.load_status == "HIGH" else "✓"
    load_bar = render_bar(cpu.load_percent, 20, LOAD_WARN_PCT, 95)
    lines.extend([
        "",
        f"  {load_icon} CPU Load: {cpu.load_percent:.1f}%  [{load_bar}]",
        f"    1min: {cpu.load_1min:.2f}  5min: {cpu.load_5min:.2f}  15min: {cpu.load_15min:.2f}",
    ])

    # Memory
    mem_icon = {"OK": "✓", "WARNING": "⚠", "CRITICAL": "🔴"}.get(cpu.mem_status, "?")
    mem_bar = render_bar(cpu.memory_percent, 20, MEM_WARN_PCT, MEM_CRITICAL_PCT)
    lines.extend([
        "",
        f"  {icon} Memory: {cpu.memory_used_gb:.1f} / {cpu.memory_total_gb:.1f} GB ({cpu.memory_percent:.1f}%)",
        f"    [{mem_bar}]",
        f"    Available: {cpu.memory_available_gb:.1f} GB  Swap: {cpu.swap_used_gb:.1f} / {cpu.swap_total_gb:.1f} GB",
    ])

    lines.append(f"\n{'=' * 60}\n")
    return "\n".join(lines)


def watch(refresh: int = DEFAULT_REFRESH, alert_temp: Optional[int] = None):
    """Continuous monitoring loop."""
    try:
        while True:
            os.system("clear")
            cpu = get_cpu_info()
            print(snapshot(cpu))

            threshold = alert_temp or TEMP_WARN
            if cpu.temperature and cpu.temperature >= threshold:
                print(f"  ⚠️  ALERT: CPU at {cpu.temperature:.0f}°C!")

            print(f"  Refreshing every {refresh}s. Ctrl+C to stop.")
            time.sleep(refresh)

    except KeyboardInterrupt:
        print("\nMonitor stopped.")


# =============================================================================
# Health Check
# =============================================================================

def health_check(cpu: CPUInfo) -> dict:
    """Run a health check and return status."""
    warnings = []
    critical = []

    if cpu.temperature is not None:
        if cpu.temperature >= TEMP_CRITICAL:
            critical.append(f"CPU temperature: {cpu.temperature:.0f}°C")
        elif cpu.temperature >= TEMP_WARN:
            warnings.append(f"CPU temperature: {cpu.temperature:.0f}°C")

    if cpu.load_percent >= LOAD_WARN_PCT:
        warnings.append(f"CPU load: {cpu.load_percent:.1f}%")

    if cpu.memory_percent >= MEM_CRITICAL_PCT:
        critical.append(f"Memory: {cpu.memory_percent:.1f}%")
    elif cpu.memory_percent >= MEM_WARN_PCT:
        warnings.append(f"Memory: {cpu.memory_percent:.1f}%")

    return {
        "healthy": len(critical) == 0,
        "warnings": warnings,
        "critical": critical,
        "cpu": {
            "model": cpu.model_name,
            "cores": cpu.cores_logical,
            "temperature": cpu.temperature,
            "load_percent": cpu.load_percent,
            "memory_percent": cpu.memory_percent,
        },
        "timestamp": datetime.now().isoformat(),
    }


# =============================================================================
# Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CPU temperature, load, and memory monitor"
    )
    parser.add_argument("--watch", action="store_true", help="Continuous mode")
    parser.add_argument("--refresh", type=int, default=DEFAULT_REFRESH)
    parser.add_argument("--alert", type=int, default=None, help="Alert threshold °C")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--health", action="store_true", help="Health check")

    args = parser.parse_args()

    try:
        cpu = get_cpu_info()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(asdict(cpu), indent=2))
    elif args.health:
        health = health_check(cpu)
        print(json.dumps(health, indent=2))
        sys.exit(0 if health["healthy"] else 1)
    elif args.watch:
        watch(refresh=args.refresh, alert_temp=args.alert)
    else:
        print(snapshot(cpu))


if __name__ == "__main__":
    main()
