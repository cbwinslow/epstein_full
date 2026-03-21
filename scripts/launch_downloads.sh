#!/bin/bash
# Production DOJ Download Launcher
# Runs multiple downloader processes for maximum throughput
# Each process handles specific datasets in parallel

set -e

SCRIPTS="/home/cbwinslow/workspace/epstein/scripts"
PYTHON="/home/cbwinslow/workspace/epstein/venv/bin/python3"
RAW_DIR="/mnt/data/epstein-project/raw-files"
LOG_DIR="/mnt/data/epstein-project/logs"
MONITOR="$PYTHON $SCRIPTS/download_doj.py --monitor"

mkdir -p "$LOG_DIR"

echo "=================================================="
echo "  EPSTEIN DOJ FILE DOWNLOADER — Production Launch"
echo "  $(date)"
echo "=================================================="
echo ""
echo "Starting parallel downloaders..."
echo ""

# Kill any existing downloaders
pkill -f "download_doj" 2>/dev/null || true
sleep 1

# Group datasets by size for balanced load
# Group A: Small datasets (1-7) — ~9.5K files total
# Group B: Dataset 8 — ~29K files
# Group C: Dataset 9 — ~104K files (largest)
# Group D: Dataset 10 — ~94K files
# Group E: Datasets 11-12 — ~65K files

cd "$RAW_DIR"

echo "Group A: Datasets 1-7 (small)"
PYTHONUNBUFFERED=1 $PYTHON "$SCRIPTS/download_doj.py" --datasets 1-7 >> "$LOG_DIR/group_a.log" 2>&1 &
echo "  PID: $!"

sleep 2

echo "Group B: Dataset 8"
PYTHONUNBUFFERED=1 $PYTHON "$SCRIPTS/download_doj.py" --datasets 8 >> "$LOG_DIR/group_b.log" 2>&1 &
echo "  PID: $!"

sleep 2

echo "Group C: Dataset 9 (largest)"
PYTHONUNBUFFERED=1 $PYTHON "$SCRIPTS/download_doj.py" --datasets 9 >> "$LOG_DIR/group_c.log" 2>&1 &
echo "  PID: $!"

sleep 2

echo "Group D: Dataset 10"
PYTHONUNBUFFERED=1 $PYTHON "$SCRIPTS/download_doj.py" --datasets 10 >> "$LOG_DIR/group_d.log" 2>&1 &
echo "  PID: $!"

sleep 2

echo "Group E: Datasets 11-12"
PYTHONUNBUFFERED=1 $PYTHON "$SCRIPTS/download_doj.py" --datasets 11-12 >> "$LOG_DIR/group_e.log" 2>&1 &
echo "  PID: $!"

echo ""
echo "All downloaders started."
echo ""
echo "Monitor progress:"
echo "  python3 $SCRIPTS/download_doj.py --monitor"
echo "  python3 $SCRIPTS/tracker.py watch"
echo "  tail -f $LOG_DIR/group_*.log"
echo ""
echo "Logs: $LOG_DIR/group_{a,b,c,d,e}.log"
echo "State: $LOG_DIR/ds{1-12}_state.json"
echo ""
echo "To stop: pkill -f download_doj"
echo ""
