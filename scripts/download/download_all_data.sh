#!/bin/bash
#=============================================================================
# COMPREHENSIVE DATA DOWNLOADER FOR EPSTEIN ANALYSIS PROJECT
# Downloads all missing financial, lobbying, and insider trading data
#=============================================================================

set -e  # Exit on error

# Configuration
BASE_DIR="/home/cbwinslow/workspace/epstein"
RAW_DIR="$BASE_DIR/epstein-data/raw-files"
LOG_DIR="$RAW_DIR/download_logs"
FEC_DIR="$RAW_DIR/fec"
LDA_DIR="$RAW_DIR/lda"
SEC_DIR="$RAW_DIR/sec_edgar"
HOUSE_DIR="$RAW_DIR/financial_disclosures"

# Create directories
mkdir -p "$LOG_DIR" "$FEC_DIR" "$LDA_DIR" "$SEC_DIR" "$HOUSE_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/download_master.log"
}

log "========================================"
log "STARTING COMPREHENSIVE DATA DOWNLOAD"
log "========================================"

#=============================================================================
# 1. DOWNLOAD FEC BULK DATA (2000-2024)
#=============================================================================
log ""
log "=== DOWNLOADING FEC BULK DATA ==="

FEC_BASE_URL="https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads"

# Download all available FEC cycles
for year in 2000 2002 2004 2006 2008 2010 2012 2014 2016 2018 2020 2022 2024; do
    log "Downloading FEC data for $year cycle..."

    # Individual contributions
    if [ ! -f "$FEC_DIR/itcont_${year}.zip" ]; then
        wget -q --tries=3 --timeout=30 \
            "$FEC_BASE_URL/$year/itcont_${year}.zip" \
            -O "$FEC_DIR/itcont_${year}.zip" \
            2>&1 | tee -a "$LOG_DIR/fec_${year}.log" || \
        wget -q --tries=3 --timeout=30 \
            "https://www.fec.gov/files/bulk-downloads/$year/itcont_${year}.zip" \
            -O "$FEC_DIR/itcont_${year}.zip" \
            2>&1 | tee -a "$LOG_DIR/fec_${year}.log" || \
        log "WARNING: Could not download itcont_${year}.zip"
    else
        log "SKIP: itcont_${year}.zip already exists"
    fi

    # Committee master
    if [ ! -f "$FEC_DIR/cm_${year}.zip" ]; then
        wget -q --tries=3 --timeout=30 \
            "$FEC_BASE_URL/$year/cm_${year}.zip" \
            -O "$FEC_DIR/cm_${year}.zip" \
            2>&1 | tee -a "$LOG_DIR/fec_${year}.log" || \
        log "WARNING: Could not download cm_${year}.zip"
    else
        log "SKIP: cm_${year}.zip already exists"
    fi

    # Candidate master
    if [ ! -f "$FEC_DIR/cn_${year}.zip" ]; then
        wget -q --tries=3 --timeout=30 \
            "$FEC_BASE_URL/$year/cn_${year}.zip" \
            -O "$FEC_DIR/cn_${year}.zip" \
            2>&1 | tee -a "$LOG_DIR/fec_${year}.log" || \
        log "WARNING: Could not download cn_${year}.zip"
    else
        log "SKIP: cn_${year}.zip already exists"
    fi
done

#=============================================================================
# 2. DOWNLOAD LDA LOBBYING DATA (1999-2024)
#=============================================================================
log ""
log "=== DOWNLOADING LDA LOBBYING DATA ==="

LDA_BASE_URL="https://lda.senate.gov/api/v1"

# Download LDA filings for all years
for year in $(seq 1999 2024); do
    log "Downloading LDA data for $year..."

    # Try to download quarterly filings
    for quarter in Q1 Q2 Q3 Q4; do
        output_file="$LDA_DIR/lda_${year}_${quarter}.xml"

        if [ ! -f "$output_file" ]; then
            # Use the Senate LDA API
            curl -s --max-time 60 \
                -H "Accept: application/xml" \
                "${LDA_BASE_URL}/filings/?filing_year=${year}&filing_period=${quarter}" \
                -o "$output_file" 2>&1 | tee -a "$LOG_DIR/lda_${year}.log" || \
            log "WARNING: Could not download LDA ${year} ${quarter}"

            # Check if file is valid XML
            if [ -f "$output_file" ] && [ ! -s "$output_file" ]; then
                rm -f "$output_file"
            fi
        else
            log "SKIP: ${year} ${quarter} already exists"
        fi
    done
done

# Also try bulk download URLs
log "Attempting bulk LDA downloads..."
for year in $(seq 2000 2020); do
    # Senate.gov bulk downloads (discontinued but archived)
    wget -q --tries=2 --timeout=30 \
        "https://www.senate.gov/legislative/Public_Disclosure/lda_${year}.zip" \
        -O "$LDA_DIR/lda_${year}_bulk.zip" \
        2>&1 | tee -a "$LOG_DIR/lda_bulk.log" || \
    log "WARNING: Could not download bulk LDA for $year"
done

#=============================================================================
# 3. DOWNLOAD SEC EDGAR INSIDER TRADING DATA (2000-2026)
#=============================================================================
log ""
log "=== DOWNLOADING SEC EDGAR DATA ==="

# SEC bulk data is available via FTP
SEC_FTP="ftp://ftp.sec.gov/edgar/daily-index"

# Download daily index files for each year
for year in $(seq 2000 2026); do
    log "Downloading SEC index for $year..."

    # Try to get the yearly index
    wget -q --tries=3 --timeout=30 \
        "https://www.sec.gov/Archives/edgar/daily-index/$year/QTR1/form.zip" \
        -O "$SEC_DIR/form_${year}_q1.zip" \
        2>&1 | tee -a "$LOG_DIR/sec_${year}.log" || \
    log "WARNING: Could not download SEC Q1 $year"

    wget -q --tries=3 --timeout=30 \
        "https://www.sec.gov/Archives/edgar/daily-index/$year/QTR2/form.zip" \
        -O "$SEC_DIR/form_${year}_q2.zip" \
        2>&1 | tee -a "$LOG_DIR/sec_${year}.log" || \
    log "WARNING: Could not download SEC Q2 $year"

    wget -q --tries=3 --timeout=30 \
        "https://www.sec.gov/Archives/edgar/daily-index/$year/QTR3/form.zip" \
        -O "$SEC_DIR/form_${year}_q3.zip" \
        2>&1 | tee -a "$LOG_DIR/sec_${year}.log" || \
    log "WARNING: Could not download SEC Q3 $year"

    wget -q --tries=3 --timeout=30 \
        "https://www.sec.gov/Archives/edgar/daily-index/$year/QTR4/form.zip" \
        -O "$SEC_DIR/form_${year}_q4.zip" \
        2>&1 | tee -a "$LOG_DIR/sec_${year}.log" || \
    log "WARNING: Could not download SEC Q4 $year"
done

# Also try to download bulk company insider transaction data
log "Downloading SEC bulk insider transaction data..."
wget -q --tries=3 --timeout=30 \
    "https://www.sec.gov/files/dera/data/financial-statement-and-notes-data-sets/2023q3_notes.zip" \
    -O "$SEC_DIR/sec_bulk_sample.zip" \
    2>&1 | tee -a "$LOG_DIR/sec_bulk.log" || \
log "WARNING: Could not download SEC bulk data"

#=============================================================================
# 4. DOWNLOAD HOUSE FINANCIAL DISCLOSURES (1995-2007)
#=============================================================================
log ""
log "=== DOWNLOADING HOUSE FINANCIAL DISCLOSURES ==="

HOUSE_BASE="https://disclosures-clerk.house.gov/FinancialDisclosure"

# The House site doesn't have easy bulk downloads, but we can try
# to access archived annual reports
for year in $(seq 1995 2007); do
    log "Checking House disclosures for $year..."

    # Try to access the annual report archive
    wget -q --tries=2 --timeout=30 \
        "${HOUSE_BASE}/archives/${year}AnnualReports.zip" \
        -O "$HOUSE_DIR/house_${year}_annual.zip" \
        2>&1 | tee -a "$LOG_DIR/house_${year}.log" || \
    log "WARNING: Could not download House $year annual reports"
done

#=============================================================================
# 5. SUMMARY
#=============================================================================
log ""
log "========================================"
log "DOWNLOAD SUMMARY"
log "========================================"

FEC_FILES=$(ls -1 "$FEC_DIR"/*.zip 2>/dev/null | wc -l)
LDA_FILES=$(ls -1 "$LDA_DIR"/*.xml 2>/dev/null | wc -l)
SEC_FILES=$(ls -1 "$SEC_DIR"/*.zip 2>/dev/null | wc -l)
HOUSE_FILES=$(ls -1 "$HOUSE_DIR"/*.zip 2>/dev/null | wc -l)

log "FEC files downloaded: $FEC_FILES"
log "LDA files downloaded: $LDA_FILES"
log "SEC files downloaded: $SEC_FILES"
log "House files downloaded: $HOUSE_FILES"

log ""
log "Download complete. Check individual logs for details."
log "========================================"
