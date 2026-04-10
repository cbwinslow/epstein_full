#!/bin/bash
# Background Data Unification Runner
# Usage: ./run_unification.sh [download|import|all]

set -e

EPSTEIN_ROOT="/home/cbwinslow/workspace/epstein"
DATA_ROOT="/home/cbwinslow/workspace/epstein-data"
LOG_DIR="$DATA_ROOT/logs"
PID_DIR="$DATA_ROOT/pids"

mkdir -p "$LOG_DIR" "$PID_DIR"

# Generate timestamp
TS=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/unify_$TS.log"
PID_FILE="$PID_DIR/unify_$TS.pid"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

check_postgres() {
    log "Checking PostgreSQL connection..."
    if PGPASSWORD=123qweasd psql -h localhost -U cbwinslow -d epstein -c "SELECT 1" > /dev/null 2>&1; then
        log "✓ PostgreSQL is accessible"
        return 0
    else
        error "✗ Cannot connect to PostgreSQL"
        return 1
    fi
}

start_downloads() {
    log "Starting background downloads..."
    
    # jmail emails download
    if [ ! -f "$DATA_ROOT/supplementary/emails-slim.parquet" ]; then
        log "Downloading jmail emails (38.8MB)..."
        (
            cd "$DATA_ROOT/supplementary"
            aria2c -x 4 -s 4 --continue=true \
                "https://data.jmail.world/v1/emails-slim.parquet" \
                2>&1 | tee -a "$LOG_FILE"
        ) &
        DOWNLOAD_PIDS+=("$!")
    else
        log "jmail emails already downloaded"
    fi
    
    # jmail iMessages
    if [ ! -f "$DATA_ROOT/supplementary/imessage_conversations.parquet" ]; then
        log "Downloading jmail iMessage conversations..."
        (
            cd "$DATA_ROOT/supplementary"
            aria2c -x 4 -s 4 --continue=true \
                "https://data.jmail.world/v1/imessage_conversations.parquet" \
                2>&1 | tee -a "$LOG_FILE"
        ) &
        DOWNLOAD_PIDS+=("$!")
    fi
    
    # jmail photos
    if [ ! -f "$DATA_ROOT/supplementary/photos.parquet" ]; then
        log "Downloading jmail photos metadata..."
        (
            cd "$DATA_ROOT/supplementary"
            aria2c -x 4 -s 4 --continue=true \
                "https://data.jmail.world/v1/photos.parquet" \
                2>&1 | tee -a "$LOG_FILE"
        ) &
        DOWNLOAD_PIDS+=("$!")
    fi
    
    log "Downloads started in background (PIDs: ${DOWNLOAD_PIDS[*]})"
}

start_ingestion() {
    log "Starting data ingestion..."
    
    # Run Python unification script
    cd "$EPSTEIN_ROOT"
    
    # Check if we have pandas for parquet processing
    if ! python3 -c "import pandas" 2>/dev/null; then
        warn "pandas not installed, installing..."
        pip install pandas pyarrow -q
    fi
    
    # Start the unification process
    python3 scripts/master_unify.py --import-only 2>&1 | tee -a "$LOG_FILE" &
    INGESTION_PID=$!
    
    echo $INGESTION_PID > "$PID_FILE"
    log "Ingestion started (PID: $INGESTION_PID)"
    log "Log file: $LOG_FILE"
}

show_status() {
    log "Checking process status..."
    
    # Check downloads
    for pid in "${DOWNLOAD_PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            log "Download PID $pid: RUNNING"
        else
            log "Download PID $pid: COMPLETED"
        fi
    done
    
    # Check ingestion
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log "Ingestion PID $pid: RUNNING"
        else
            log "Ingestion PID $pid: COMPLETED"
        fi
    fi
    
    # Show recent log entries
    log "Recent progress:"
    tail -20 "$LOG_FILE" 2>/dev/null || log "No log entries yet"
}

monitor_progress() {
    log "Starting progress monitor (Ctrl+C to stop)..."
    
    while true; do
        clear
        echo "=========================================="
        echo "Data Unification Progress Monitor"
        echo "=========================================="
        echo "Started: $TS"
        echo "Log: $LOG_FILE"
        echo ""
        
        # Show process status
        echo "Active Processes:"
        ps aux | grep -E "(aria2c|master_unify)" | grep -v grep | while read line; do
            echo "  $line"
        done
        
        echo ""
        echo "Recent Progress (last 30 lines):"
        tail -30 "$LOG_FILE" 2>/dev/null | tail -r | head -30 | tail -r
        
        echo ""
        echo "Database Status:"
        PGPASSWORD=123qweasd psql -h localhost -U cbwinslow -d epstein -c "
            SELECT 'documents: ' || COUNT(*) FROM documents
            UNION ALL
            SELECT 'pages: ' || COUNT(*) FROM pages
            UNION ALL
            SELECT 'entities: ' || COUNT(*) FROM entities
            UNION ALL
            SELECT 'emails: ' || COUNT(*) FROM emails
            UNION ALL
            SELECT 'jmail_emails: ' || COUNT(*) FROM jmail_emails
        " 2>/dev/null || echo "  (DB connection unavailable)"
        
        echo ""
        echo "Press Ctrl+C to exit monitor. Processes continue in background."
        
        sleep 5
    done
}

# Main execution
MODE=${1:-all}
DOWNLOAD_PIDS=()

case "$MODE" in
    download)
        check_postgres || exit 1
        start_downloads
        log "Downloads running in background"
        log "Monitor with: tail -f $LOG_FILE"
        ;;
    import)
        check_postgres || exit 1
        start_ingestion
        log "Ingestion running in background"
        log "Monitor with: tail -f $LOG_FILE"
        ;;
    all)
        check_postgres || exit 1
        start_downloads
        start_ingestion
        log "All processes started!"
        log "Monitor with: $0 monitor"
        log "Or: tail -f $LOG_FILE"
        ;;
    status)
        show_status
        ;;
    monitor)
        monitor_progress
        ;;
    *)
        echo "Usage: $0 [download|import|all|status|monitor]"
        echo ""
        echo "Commands:"
        echo "  download  - Start only downloads in background"
        echo "  import    - Start only data ingestion"
        echo "  all       - Start both downloads and ingestion"
        echo "  status    - Show current status"
        echo "  monitor   - Interactive progress monitor"
        exit 1
        ;;
esac

exit 0
