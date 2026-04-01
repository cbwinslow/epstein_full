#!/usr/bin/env python3
"""
Batch FEC data ingestion - processes all downloaded FEC files
"""

import subprocess
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path('/mnt/data/epstein-project/raw-files/fec')
SCRIPT_DIR = Path('/home/cbwinslow/workspace/epstein/scripts')

def get_cycle_from_filename(filename):
    """Extract election cycle from filename (e.g., indiv24.zip -> 2024)"""
    # Extract 2-digit year suffix
    base = filename.stem  # e.g., 'indiv24'
    year_suffix = base[-2:]  # e.g., '24'
    
    # Convert to 4-digit year
    year = int(year_suffix)
    if year >= 80:  # 1980-1999
        return 1900 + year
    else:  # 2000-2099
        return 2000 + year

def main():
    # Process individual contributions
    indiv_files = sorted(DATA_DIR.glob('indiv*.zip'))
    logger.info(f"Found {len(indiv_files)} individual contribution files")
    
    for zip_file in indiv_files:
        cycle = get_cycle_from_filename(zip_file)
        logger.info(f"Processing {zip_file.name} (cycle {cycle})")
        
        cmd = [
            sys.executable,
            str(SCRIPT_DIR / 'fec_fast_ingest.py'),
            '--file', str(zip_file),
            '--cycle', str(cycle)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Failed to process {zip_file.name}: {result.stderr}")
        else:
            logger.info(f"Successfully processed {zip_file.name}")
            logger.info(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)

if __name__ == '__main__':
    main()
