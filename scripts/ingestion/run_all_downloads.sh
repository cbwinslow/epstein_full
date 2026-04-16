#!/bin/bash
# Run all government dataset downloads in parallel
# April 13, 2026

set -e

BASE_DIR="/home/cbwinslow/workspace/epstein"
LOG_DIR="$BASE_DIR/logs/ingestion"
mkdir -p "$LOG_DIR"

echo "=============================================="
echo "GOVERNMENT DATA PARALLEL DOWNLOAD"
echo "Started: $(date)"
echo "=============================================="

# Function to run download with logging
run_download() {
    local name=$1
    local script=$2
    local log_file="$LOG_DIR/${name}_$(date +%Y%m%d_%H%M%S).log"
    
    echo "[$name] Starting download..."
    if "$BASE_DIR/scripts/ingestion/$script" > "$log_file" 2>&1; then
        echo "[$name] ✅ SUCCESS"
    else
        echo "[$name] ❌ FAILED (see $log_file)"
    fi
}

# Export function for parallel execution
export -f run_download
export BASE_DIR LOG_DIR

# Start all downloads in parallel
echo "Starting parallel downloads..."

# FEC 2024 (Priority 1)
run_download "fec_2024" "download_fec_2024.py" &
PID_FEC=$!

# White House Visitors (Priority 1) - Create and run
cat > "$BASE_DIR/scripts/ingestion/download_whitehouse.py" << 'PYEOF'
#!/usr/bin/env python3
"""Download White House Visitor Logs"""
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/whitehouse")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Download 2024 CSV
urls = [
    "https://www.whitehouse.gov/wp-content/uploads/2024/01/WhiteHouse-WAVES-Access-Records-2023.csv",
    "https://www.whitehouse.gov/wp-content/uploads/2025/01/WhiteHouse-WAVES-Access-Records-2024.csv",
]

for url in urls:
    filename = url.split('/')[-1]
    output = BASE_DIR / filename
    
    if output.exists():
        logger.info(f"{filename} already exists, skipping")
        continue
    
    logger.info(f"Downloading {filename}...")
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
        r.raise_for_status()
        output.write_bytes(r.content)
        logger.info(f"✅ Downloaded {filename} ({len(r.content)/1024/1024:.1f} MB)")
    except Exception as e:
        logger.error(f"❌ Failed {filename}: {e}")

logger.info("White House download complete")
PYEOF
chmod +x "$BASE_DIR/scripts/ingestion/download_whitehouse.py"
run_download "whitehouse" "download_whitehouse.py" &
PID_WHITEHOUSE=$!

# SEC EDGAR (Priority 1) - Recent filings
cat > "$BASE_DIR/scripts/ingestion/download_sec_edgar_recent.py" << 'PYEOF'
#!/usr/bin/env python3
"""Download recent SEC EDGAR Form 4 filings"""
import requests
import time
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/sec_edgar")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Research Bot contact@example.com',
    'Accept-Encoding': 'gzip, deflate',
}

# Get last 7 days of Form 4
base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
output_dir = BASE_DIR / f"form4_{datetime.now().strftime('%Y%m%d')}"
output_dir.mkdir(exist_ok=True)

for i in range(7):
    date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    logger.info(f"Fetching Form 4 for {date}...")
    
    try:
        time.sleep(0.2)  # Rate limiting
        url = f"{base_url}?action=getcurrent&type=4&date={date}&count=100&output=atom"
        r = requests.get(url, headers=HEADERS, timeout=30)
        
        if r.status_code == 200:
            output_file = output_dir / f"form4_{date}.xml"
            output_file.write_text(r.text)
            logger.info(f"✅ Saved {output_file.name}")
        else:
            logger.warning(f"⚠️ Status {r.status_code} for {date}")
            
    except Exception as e:
        logger.error(f"❌ Error for {date}: {e}")

logger.info(f"SEC EDGAR download complete. Files in: {output_dir}")
PYEOF
chmod +x "$BASE_DIR/scripts/ingestion/download_sec_edgar_recent.py"
run_download "sec_edgar" "download_sec_edgar_recent.py" &
PID_SEC=$!

# FARA (Priority 2)
cat > "$BASE_DIR/scripts/ingestion/download_fara.py" << 'PYEOF'
#!/usr/bin/env python3
"""Download FARA registration XML"""
import requests
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fara")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# FARA search/registration XML
url = "https://efile.fara.gov/pls/apex/f?p=171:1:::::"
logger.info("Checking FARA data availability...")

try:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    logger.info(f"FARA site status: {r.status_code}")
    
    # Save info file
    info_file = BASE_DIR / "fara_info.txt"
    info_file.write_text(f"FARA check: {datetime.now()}\nStatus: {r.status_code}\n")
    logger.info("✅ FARA info saved")
    
except Exception as e:
    logger.error(f"❌ FARA check failed: {e}")

logger.info("FARA download script placeholder - manual download required")
PYEOF
chmod +x "$BASE_DIR/scripts/ingestion/download_fara.py"
run_download "fara" "download_fara.py" &
PID_FARA=$!

# Lobbying (Priority 2)
cat > "$BASE_DIR/scripts/ingestion/download_lobbying.py" << 'PYEOF'
#!/usr/bin/env python3
"""Download Lobbying Disclosure data"""
import requests
import logging
import sys
from pathlib import Path

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/lobbying")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Lobbying data URLs (quarterly files)
base_url = "https://www.senate.gov/legislative/lobbying.htm"
logger.info("Checking lobbying data sources...")

try:
    r = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    logger.info(f"Lobbying site status: {r.status_code}")
    
    info_file = BASE_DIR / "lobbying_sources.txt"
    info_file.write_text(f"Lobbying Disclosure Database\nSource: {base_url}\nStatus: {r.status_code}\n")
    logger.info("✅ Lobbying info saved")
    
except Exception as e:
    logger.error(f"❌ Lobbying check failed: {e}")

logger.info("Lobbying download requires manual bulk download from senate.gov")
PYEOF
chmod +x "$BASE_DIR/scripts/ingestion/download_lobbying.py"
run_download "lobbying" "download_lobbying.py" &
PID_LOBBYING=$!

# USA Spending (Priority 2)
cat > "$BASE_DIR/scripts/ingestion/download_usa_spending.py" << 'PYEOF'
#!/usr/bin/env python3
"""Download USA Spending data via API"""
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/usa_spending")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# USA Spending API - search for recent awards
url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
headers = {'Content-Type': 'application/json'}

# Search for recent awards (last 90 days)
payload = {
    "filters": {
        "time_period": [{"start_date": "2024-01-01", "end_date": "2024-12-31"}],
        "award_type_codes": ["A", "B", "C", "D"]  # Contracts, Grants, Loans
    },
    "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency"],
    "sort": "Award Amount",
    "order": "desc",
    "limit": 100
}

logger.info("Fetching USA Spending data...")

try:
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    
    output_file = BASE_DIR / f"usa_spending_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    results_count = len(data.get('results', []))
    logger.info(f"✅ Downloaded {results_count} awards to {output_file}")
    
except Exception as e:
    logger.error(f"❌ USA Spending download failed: {e}")

logger.info("USA Spending download complete")
PYEOF
chmod +x "$BASE_DIR/scripts/ingestion/download_usa_spending.py"
run_download "usa_spending" "download_usa_spending.py" &
PID_USA=$!

# Congress.gov (Priority 3) - Requires API key
cat > "$BASE_DIR/scripts/ingestion/download_congress.py" << 'PYEOF'
#!/usr/bin/env python3
"""Download Congress.gov data via API"""
import os
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/congress")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get('CONGRESS_API_KEY')
if not API_KEY:
    logger.error("CONGRESS_API_KEY not set in environment")
    sys.exit(1)

base_url = "https://api.congress.gov/v3"
headers = {'X-API-Key': API_KEY}

# Get recent bills (118th Congress)
logger.info("Fetching Congress bills...")

try:
    url = f"{base_url}/bill?congress=118&limit=100&format=json"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    
    output_file = BASE_DIR / f"congress_bills_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    bills_count = len(data.get('bills', []))
    logger.info(f"✅ Downloaded {bills_count} bills to {output_file}")
    
except Exception as e:
    logger.error(f"❌ Congress download failed: {e}")

logger.info("Congress.gov download complete")
PYEOF
chmod +x "$BASE_DIR/scripts/ingestion/download_congress.py"
run_download "congress" "download_congress.py" &
PID_CONGRESS=$!

# GovInfo.gov (Priority 3) - Requires API key
cat > "$BASE_DIR/scripts/ingestion/download_govinfo.py" << 'PYEOF'
#!/usr/bin/env python3
"""Download GovInfo.gov data via API"""
import os
import requests
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo")
BASE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get('GOVINFO_API_KEY')
if not API_KEY:
    logger.error("GOVINFO_API_KEY not set in environment")
    sys.exit(1)

base_url = "https://api.govinfo.gov"
headers = {'X-Api-Key': API_KEY}

# Get recent Federal Register collections
logger.info("Fetching GovInfo collections...")

try:
    url = f"{base_url}/collections/FR/2024"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    
    output_file = BASE_DIR / f"govinfo_collections_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    packages_count = len(data.get('packages', []))
    logger.info(f"✅ Downloaded {packages_count} packages to {output_file}")
    
except Exception as e:
    logger.error(f"❌ GovInfo download failed: {e}")

logger.info("GovInfo.gov download complete")
PYEOF
chmod +x "$BASE_DIR/scripts/ingestion/download_govinfo.py"
run_download "govinfo" "download_govinfo.py" &
PID_GOVINFO=$!

echo ""
echo "=============================================="
echo "All downloads started in parallel!"
echo "=============================================="
echo "PIDs: FEC=$PID_FEC WhiteHouse=$PID_WHITEHOUSE SEC=$PID_SEC FARA=$PID_FARA"
echo "      Lobbying=$PID_LOBBYING USA=$PID_USA Congress=$PID_CONGRESS GovInfo=$PID_GOVINFO"
echo ""
echo "Waiting for all downloads to complete..."
echo ""

# Wait for all background jobs
wait

echo ""
echo "=============================================="
echo "All downloads completed!"
echo "Finished: $(date)"
echo "=============================================="
echo ""
echo "Check logs in: $LOG_DIR"
echo "Downloaded data in: /home/cbwinslow/workspace/epstein-data/raw-files/"
