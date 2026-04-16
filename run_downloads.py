#!/usr/bin/env python3
"""
Unified download runner for Epstein data ingestion pipeline.
Industry standard: Single entry point with proper path resolution.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Project paths (resolved absolutely)
PROJECT_ROOT = Path(__file__).parent.resolve()
SCRIPTS_DIR = PROJECT_ROOT / 'scripts' / 'ingestion'
LOGS_DIR = PROJECT_ROOT / 'logs' / 'ingestion'
DATA_DIR = PROJECT_ROOT / 'epstein-data' / 'raw-files'
SECRETS_FILE = PROJECT_ROOT / '.bash_secrets'

# Download configurations
DOWNLOADS = [
    {
        'name': 'FEC Committees',
        'script': 'download_fec_committees.py',
        'data_dir': 'fec_committees',
        'priority': 1,
        'est_time': '15 min'
    },
    {
        'name': 'FARA Bulk',
        'script': 'download_fara_bulk.py',
        'data_dir': 'fara',
        'priority': 2,
        'est_time': '10 min'
    },
    {
        'name': 'Financial Disclosures',
        'script': 'download_financial_disclosures.py',
        'data_dir': 'financial_disclosures',
        'priority': 3,
        'est_time': '20 min'
    },
    {
        'name': 'Lobbying',
        'script': 'download_lobbying.py',
        'data_dir': 'lobbying',
        'priority': 4,
        'est_time': '2 hours'
    },
    {
        'name': 'GovInfo Bulk',
        'script': 'download_govinfo_bulk.py',
        'data_dir': 'govinfo',
        'priority': 5,
        'est_time': '3 hours'
    }
]


def load_secrets():
    """Load API keys from .bash_secrets file."""
    if not SECRETS_FILE.exists():
        logger.warning(f"Secrets file not found: {SECRETS_FILE}")
        return
    
    with open(SECRETS_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith('export ') and '=' in line:
                key_val = line[7:].split('=', 1)
                if len(key_val) == 2:
                    key, val = key_val
                    val = val.strip('"\'')
                    os.environ[key] = val
                    logger.debug(f"Loaded: {key}")
    
    # Verify critical keys
    required = ['GOVINFO_API_KEY', 'CONGRESS_API_KEY']
    for key in required:
        if os.environ.get(key):
            logger.info(f"✅ {key} loaded")
        else:
            logger.warning(f"⚠️  {key} NOT SET")


def ensure_directories():
    """Create required directories."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    for dl in DOWNLOADS:
        (DATA_DIR / dl['data_dir']).mkdir(parents=True, exist_ok=True)
    logger.info("✅ Directories created")


def run_download(config: dict) -> dict:
    """Run a single download script."""
    name = config['name']
    script = config['script']
    script_path = SCRIPTS_DIR / script
    
    if not script_path.exists():
        return {'name': name, 'status': 'FAILED', 'error': f'Script not found: {script_path}'}
    
    log_file = LOGS_DIR / f"{config['data_dir']}_{datetime.now():%Y%m%d_%H%M%S}.log"
    
    logger.info(f"🚀 Starting: {name}")
    logger.info(f"   Script: {script_path}")
    logger.info(f"   Log: {log_file}")
    logger.info(f"   Est. time: {config['est_time']}")
    
    try:
        # Run with timeout (4 hours max)
        with open(log_file, 'w') as log_f:
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=log_f,
                stderr=subprocess.STDOUT,
                cwd=str(SCRIPTS_DIR),
                env=os.environ.copy()
            )
            
            try:
                exit_code = process.wait(timeout=14400)  # 4 hours
                if exit_code == 0:
                    return {'name': name, 'status': 'SUCCESS', 'log': str(log_file)}
                else:
                    return {'name': name, 'status': 'FAILED', 'exit_code': exit_code, 'log': str(log_file)}
            except subprocess.TimeoutExpired:
                process.kill()
                return {'name': name, 'status': 'TIMEOUT', 'log': str(log_file)}
                
    except Exception as e:
        return {'name': name, 'status': 'ERROR', 'error': str(e)}


def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("EPSTEIN DATA DOWNLOAD ORCHESTRATOR")
    logger.info("=" * 60)
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Scripts: {SCRIPTS_DIR}")
    logger.info(f"Data: {DATA_DIR}")
    logger.info(f"Logs: {LOGS_DIR}")
    logger.info("")
    
    # Load environment
    load_secrets()
    ensure_directories()
    
    logger.info(f"\n📋 Downloads to run: {len(DOWNLOADS)}")
    for i, dl in enumerate(DOWNLOADS, 1):
        logger.info(f"  {i}. {dl['name']} (est. {dl['est_time']})")
    
    logger.info("\n" + "=" * 60)
    logger.info("Starting parallel downloads...")
    logger.info("=" * 60 + "\n")
    
    # Run downloads in parallel (max 3 concurrent to avoid overwhelming APIs)
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(run_download, dl): dl for dl in DOWNLOADS}
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['status'] == 'SUCCESS':
                logger.info(f"✅ {result['name']}: COMPLETE")
            else:
                logger.error(f"❌ {result['name']}: {result['status']}")
                if 'error' in result:
                    logger.error(f"   Error: {result['error']}")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("=" * 60)
    
    success = sum(1 for r in results if r['status'] == 'SUCCESS')
    failed = len(results) - success
    
    logger.info(f"Total: {len(results)}")
    logger.info(f"Success: {success}")
    logger.info(f"Failed: {failed}")
    logger.info("")
    
    for r in results:
        icon = "✅" if r['status'] == 'SUCCESS' else "❌"
        logger.info(f"{icon} {r['name']}: {r['status']}")
        if 'log' in r:
            logger.info(f"   Log: {r['log']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Run complete!")
    logger.info("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
