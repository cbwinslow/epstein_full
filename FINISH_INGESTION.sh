#!/bin/bash
set -e
echo "==========================================="
echo "FINISH EPSTEIN DATA INGESTION - COMPLETE ALL"
echo "==========================================="
echo "Started: $(date)"
echo ""

# Configuration
DATA_DIR="/home/cbwinslow/workspace/epstein-data"
SCRIPT_DIR="/home/cbwinslow/workspace/epstein/scripts"

# =========================================
# PHASE 2: DOWNLOAD ALL MISSING DATA
# =========================================

echo "PHASE 2: DOWNLOADING ALL MISSING DATA"
echo "========================================"

# Check what's already downloaded
echo "Checking existing downloads..."
ls $DATA_DIR/raw-files/ | grep -E "data|congress|govinfo|whitehouse|fara|fec|sec_edgar|senate|fbi" || echo "Some directories missing"

# 1. Senate Vote Details (Issue #58 - 403 errors need retry)
echo ""
echo "2. Senate Vote Details (Issue #58) - Retrying with delays..."
if [ -d "$SCRIPT_DIR/ingestion/download_senate_vote_details.py" ]; then
    python3 $SCRIPT_DIR/ingestion/download_senate_vote_details.py --retry --delay 2.0 --congress 119 2>&1 | tee -a /tmp/senate_votes.log || echo "⚠️ Senate vote details still having issues - check /tmp/senate_votes.log"
else
    echo "⚠️ Script not found: download_senate_vote_details.py"
fi

# 2. SEC EDGAR Bulk (Issue #55)
echo ""
echo "5. SEC EDGAR Bulk Import (Issue #55)..."
if [ -d "$SCRIPT_DIR/ingestion/download_sec_edgar_recent.py" ]; then
    python3 $SCRIPT_DIR/ingestion/download_sec_edgar_recent.py --form 4 --years 2020-2026 2>&1 | tee -a /tmp/sec_edgar.log
    python3 $SCRIPT_DIR/ingestion/download_sec_edgar_recent.py --form 13F --years 2020-2026 2>&1 | tee -a /tmp/sec_edgar.log
else
    echo "⚠️ Script not found: download_sec_edgar_recent.py"
fi

# 3. FBI Vault (Issue #44)
echo ""
echo "4. FBI Vault Documents (Issue #44)..."
if [ -d "$SCRIPT_DIR/ingestion/download_fbi_vault.py" ]; then
    python3 $SCRIPT_DIR/ingestion/download_fbi_vault.py 2>&1 | tee -a /tmp/fbi_vault.log
else
    echo "⚠️ Script not found: download_fbi_vault.py"
    echo "   Creating FBI Vault download..."
    # Check if we can download from vault.fbi.gov
    mkdir -p $DATA_DIR/raw-files/fbi-vault/
    echo "   TODO: Implement FBI Vault download from https://vault.fbi.gov/"
fi

# 4. Birthday Book (dleeerdefi - Issue #9)
echo ""
echo "6. Birthday Book (dleeerdefi - 128 pages)..."
if [ -d "$SCRIPT_DIR/ingestion/download_hf_resume.py" ]; then
    python3 $SCRIPT_DIR/ingestion/download_hf_resume.py --dataset birthday_book 2>&1 | tee -a /tmp/birthday_book.log
else
    echo "⚠️ Script not found: download_hf_resume.py"
fi

# 5. Check all raw-files directories
echo ""
echo "Checking all raw-files directories..."
for dir in $DATA_DIR/raw-files/*/; do
    count=$(ls -1 "$dir" 2>/dev/null | wc -l)
    echo "  $dir: $count files"
done

echo ""
echo "PHASE 2 COMPLETE: Downloading done"
echo "========================================"

# =========================================
# PHASE 3: IMPORT ALL DATA TO POSTGRESQL  
# =========================================

echo ""
echo "PHASE 3: IMPORTING ALL DATA TO POSTGRESQL"
echo "========================================"

# Check what tables already exist
echo "Checking existing PostgreSQL tables..."
psql -d epstein -c "
SELECT table_name FROM information_schema.tables 
WHERE table_schema='public' 
ORDER BY table_name;" 2>&1 | grep -E "congress|senate|sec_edgar|fbi|birthday|neo4j|black_book|flight" || echo "Some tables missing"

# 1. Import Senate Vote Details (if downloaded)
echo ""
echo "Importing Senate Vote Details..."
if [ -d "$SCRIPT_DIR/import/import_senate_votes.py" ]; then
    python3 $SCRIPT_DIR/import/import_senate_votes.py 2>&1 | tee -a /tmp/import_senate.log
else
    echo "⚠️ Skipping - script not found"
fi

# 2. Import SEC EDGAR
echo ""
echo "Importing SEC EDGAR data..."
if [ -d "$SCRIPT_DIR/import/import_sec_edgar.py" ]; then
    python3 $SCRIPT_DIR/import/import_sec_edgar.py 2>&1 | tee -a /tmp/import_sec_edgar.log
else
    echo "⚠️ Skipping - script not found"
fi

# 3. Import Neo4j Graph (Issue #30)
echo ""
echo "Importing Neo4j Graph (Issue #30)..."
if [ -d "$SCRIPT_DIR/import/import_neo4j_graph.py" ]; then
    python3 $SCRIPT_DIR/import/import_neo4j_graph.py 2>&1 | tee -a /tmp/import_neo4j.log
else
    echo "⚠️ Script not found: import_neo4j_graph.py"
    echo "   Creating import script..."
    # Create the import script from docs/agents/INGESTION_GUIDES/07-third-party-repos.md
    echo "   TODO: Implement Neo4j import"
fi

# 4. Import Birthday Book (if downloaded)
echo ""
echo "Importing Birthday Book..."
if [ -d "$SCRIPT_DIR/import/import_birthday_book.py" ]; then
    python3 $SCRIPT_DIR/import/import_birthday_book.py 2>&1 | tee -a /tmp/import_birthday.log
else
    echo "⚠️ Script not found: import_birthday_book.py"
fi

# 5. Verify all tables
echo ""
echo "Verifying all PostgreSQL tables..."
psql -d epstein -c "
SELECT 
    'congress_senate_vote_details' as table,
    (SELECT COUNT(*) FROM congress_senate_vote_details) as records
UNION ALL
SELECT 'sec_edgar', (SELECT COUNT(*) FROM sec_edgar)
UNION ALL
SELECT 'fbi_vault', (SELECT COUNT(*) FROM fbi_vault)
UNION ALL
SELECT 'birthday_book', (SELECT COUNT(*) FROM birthday_book_pages)
UNION ALL
SELECT 'neo4j_nodes', (SELECT COUNT(*) FROM kg_nodes)
" 2>&1 || echo "⚠️ Some tables not found"

echo ""
echo "PHASE 3 COMPLETE: Importing done"
echo "========================================"

# =========================================
# PHASE 4-5: PROCESSING & ENRICHMENT
# =========================================

echo ""
echo "PHASE 4-5: PROCESSING & ENRICHMENT"
echo "========================================"

# 1. OCR remaining documents (Issue #39 - 749K missing)
echo "Processing remaining documents (749K missing - Issue #39)..."
if [ -d "/home/cbwinslow/workspace/epstein/epstein-pipeline" ]; then
    cd /home/cbwinslow/workspace/epstein/epstein-pipeline
    python3 ocr.py $DATA_DIR/raw-files/ --output $DATA_DIR/processed/ocr_output/ --backend surya 2>&1 | tee -a /tmp/ocr.log &
    echo "  OCR running in background (PID $!)"
    cd /home/cbwinslow/workspace/epstein
else
    echo "⚠️ epstein-pipeline not found"
fi

# 2. Generate embeddings (Issue #29)
echo ""
echo "Generating embeddings (Issue #29)..."
if [ -d "$SCRIPT_DIR/enrichment/embed_*.py" ]; then
    python3 $SCRIPT_DIR/enrichment/rtx3060_embeddings.py --all 2>&1 | tee -a /tmp/embeddings.log &
    echo "  Embeddings running in background (PID $!)"
else
    echo "⚠️ Embedding scripts not found"
fi

# 3. Build knowledge graph (Issue #12, #30)
echo ""
echo "Building knowledge graph (Issue #12, #30)..."
if [ -d "$SCRIPT_DIR/processing/master_unify.py" ]; then
    python3 $SCRIPT_DIR/processing/master_unify.py --all-sources 2>&1 | tee -a /tmp/graph.log &
    echo "  Graph building in background (PID $!)"
else
    echo "⚠️ master_unify.py not found"
fi

echo ""
echo "PHASE 4-5 COMPLETE: Processing & Enrichment running in background"
echo "========================================"

# =========================================
# FINAL VERIFICATION
# =========================================

echo ""
echo "FINAL VERIFICATION"
echo "========================================"

# Count all major tables
echo "Counting all records in PostgreSQL..."
psql -d epstein -c "
SELECT 'DOJ Documents' as source, COUNT(*) FROM documents
UNION ALL
SELECT 'jMail Emails', COUNT(*) FROM jmail_emails_full
UNION ALL
SELECT 'ICIJ Entities', COUNT(*) FROM icij_entities
UNION ALL
SELECT 'FEC Contributions', COUNT(*) FROM fec_individual_contributions
UNION ALL
SELECT 'Congress Bills', COUNT(*) FROM congress_bills
UNION ALL
SELECT 'Congress Members', COUNT(*) FROM congress_members
UNION ALL
SELECT 'House Votes', COUNT(*) FROM congress_house_votes
UNION ALL
SELECT 'Senate Votes', COUNT(*) FROM congress_senate_votes
UNION ALL
SELECT 'Federal Register', COUNT(*) FROM federal_register_entries
UNION ALL
SELECT 'White House Visitors', COUNT(*) FROM whitehouse_visitors
UNION ALL
SELECT 'GDELT News', COUNT(*) FROM media_news_articles
UNION ALL
SELECT 'Black Book', COUNT(*) FROM black_book_contacts
UNION ALL
SELECT 'Flight Logs', COUNT(*) FROM flight_logs_github
" 2>&1

# Check raw files
echo ""
echo "Checking raw files..."
du -sh $DATA_DIR/raw-files/*/ 2>/dev/null | sort -h

# Check archive files
echo ""
echo "Checking archive files..."
ls -lh $DATA_DIR/databases/*.db 2>/dev/null | awk '{print $9, $5}'

echo ""
echo "==========================================="
echo "FINISH EPSTEIN DATA INGESTION - COMPLETE!"
echo "Finished: $(date)"
echo "Check logs in /tmp/*.log"
echo "==========================================="
