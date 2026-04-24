#!/usr/bin/env python3
"""
Parallel FEC data ingestion - processes all downloaded FEC files in parallel
Uses multiprocessing for maximum speed
"""

import subprocess
import sys
from pathlib import Path
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATA_DIR = Path('/home/cbwinslow/workspace/epstein-data/raw-files/fec')
SCRIPT_DIR = Path('/home/cbwinslow/workspace/epstein/scripts')

# Number of parallel workers (use CPU count, but max 4 to not overwhelm DB)
MAX_WORKERS = min(4, multiprocessing.cpu_count())

def get_cycle_from_filename(filename):
    """Extract election cycle from filename (e.g., indiv24.zip -> 2024)"""
    base = filename.stem
    year_suffix = base[-2:]
    year = int(year_suffix)
    if year >= 80:
        return 1900 + year
    else:
        return 2000 + year

def process_single_file(zip_file):
    """Process a single FEC file - runs in separate process"""
    cycle = get_cycle_from_filename(zip_file)
    logger.info(f"[Worker] Starting {zip_file.name} (cycle {cycle})")
    
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / 'fec_fast_ingest.py'),
        '--file', str(zip_file),
        '--cycle', str(cycle)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"[Worker] Failed {zip_file.name}: {result.stderr[:500]}")
        return (zip_file.name, False, 0)
    else:
        # Parse rows imported from output
        output = result.stdout
        rows = 0
        for line in output.split('\n'):
            if 'Total rows imported' in line:
                try:
                    rows = int(line.split(':')[1].strip().replace(',', ''))
                except:
                    pass
        logger.info(f"[Worker] Completed {zip_file.name}: {rows:,} rows")
        return (zip_file.name, True, rows)

def main():
    # Get all individual contribution files
    indiv_files = sorted(DATA_DIR.glob('indiv*.zip'))
    logger.info(f"Found {len(indiv_files)} files to process")
    logger.info(f"Using {MAX_WORKERS} parallel workers")
    logger.info(f"Using COPY protocol for maximum speed")
    
    total_rows = 0
    success_count = 0
    fail_count = 0
    
    # Process files in parallel
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_single_file, zip_file): zip_file 
            for zip_file in indiv_files
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_file):
            zip_file = future_to_file[future]
            try:
                name, success, rows = future.result()
                if success:
                    success_count += 1
                    total_rows += rows
                    logger.info(f"✓ {name}: {rows:,} rows (Total: {total_rows:,})")
                else:
                    fail_count += 1
                    logger.error(f"✗ {name}: FAILED")
            except Exception as e:
                fail_count += 1
                logger.error(f"✗ {zip_file.name}: Exception - {e}")
    
    logger.info("=" * 60)
    logger.info(f"Ingestion Complete!")
    logger.info(f"Successful: {success_count}/{len(indiv_files)}")
    logger.info(f"Failed: {fail_count}/{len(indiv_files)}")
    logger.info(f"Total rows imported: {total_rows:,}")
    logger.info("=" * 60)

if __name__ == '__main__':
    main()
