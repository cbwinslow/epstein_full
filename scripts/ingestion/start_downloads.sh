#!/bin/bash
# Start all bulk downloads with proper environment
# April 14, 2026

set -e

# Load secrets
echo "Loading API keys from .bash_secrets..."
source ~/workspace/epstein/.bash_secrets

# Verify keys are loaded
echo "Verifying API keys..."
if [ -z "$GOVINFO_API_KEY" ]; then
    echo "ERROR: GOVINFO_API_KEY not loaded"
    exit 1
fi
if [ -z "$CONGRESS_API_KEY" ]; then
    echo "WARNING: CONGRESS_API_KEY not loaded"
fi
if [ -z "$FEC_API_KEY" ]; then
    echo "WARNING: FEC_API_KEY not loaded"
fi

echo "✅ API keys loaded successfully"
echo ""

# Create directories
mkdir -p ~/workspace/epstein-data/raw-files/{govinfo,fara,lobbying,fec_committees,financial_disclosures}
mkdir -p ~/workspace/epstein/logs/ingestion

cd ~/workspace/epstein/scripts/ingestion

# Start downloads in background with proper logging
echo "Starting GovInfo bulk download (400K+ docs)..."
nohup python3 download_govinfo_bulk.py > ../../logs/ingestion/govinfo_bulk_$(date +%Y%m%d_%H%M%S).log 2>&1 &
GOVINFO_PID=$!
echo "  PID: $GOVINFO_PID"

echo "Starting FARA bulk download..."
nohup python3 download_fara_bulk.py > ../../logs/ingestion/fara_bulk_$(date +%Y%m%d_%H%M%S).log 2>&1 &
FARA_PID=$!
echo "  PID: $FARA_PID"

echo "Starting Lobbying download..."
nohup python3 download_lobbying.py > ../../logs/ingestion/lobbying_bulk_$(date +%Y%m%d_%H%M%S).log 2>&1 &
LOBBYING_PID=$!
echo "  PID: $LOBBYING_PID"

echo "Starting FEC Committees download..."
nohup python3 download_fec_committees.py > ../../logs/ingestion/fec_committees_$(date +%Y%m%d_%H%M%S).log 2>&1 &
FEC_PID=$!
echo "  PID: $FEC_PID"

echo "Starting Financial Disclosures download..."
nohup python3 download_financial_disclosures.py > ../../logs/ingestion/financial_disclosures_$(date +%Y%m%d_%H%M%S).log 2>&1 &
FD_PID=$!
echo "  PID: $FD_PID"

echo ""
echo "=========================================="
echo "All downloads started successfully!"
echo "=========================================="
echo ""
echo "Monitor progress:"
echo "  tail -f ~/workspace/epstein/logs/ingestion/*.log"
echo ""
echo "Check processes:"
echo "  ps aux | grep 'download_' | grep -v grep"
echo ""
echo "Check data growth:"
echo "  du -sh ~/workspace/epstein-data/raw-files/*/"
echo ""
echo "PIDs:"
echo "  GovInfo: $GOVINFO_PID"
echo "  FARA: $FARA_PID"
echo "  Lobbying: $LOBBYING_PID"
echo "  FEC: $FEC_PID"
echo "  Financial: $FD_PID"
