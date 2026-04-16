#!/usr/bin/env python3
"""
Government Data Download Orchestrator
Parallel download manager for all government datasets
"""

import os
import sys
import json
import logging
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Optional

# Configuration
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")
LOCK_DIR = Path("/home/cbwinslow/workspace/epstein/logs/locks")
MAX_WORKERS = 5  # Parallel downloads

# Ensure directories exist
BASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOCK_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"orchestrator_{datetime.now():%Y%m%d_%H%M%S}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Dataset configurations
DATASETS = {
    "fec_2024": {
        "name": "FEC 2024 Individual Contributions",
        "script": "download_fec_2024.py",
        "priority": 1,
        "est_size_gb": 3,
        "est_records": 20000000,
    },
    "whitehouse_visitors": {
        "name": "White House Visitor Logs",
        "script": "download_whitehouse_visitors.py",
        "priority": 1,
        "est_size_gb": 1,
        "est_records": 5000000,
    },
    "sec_edgar_recent": {
        "name": "SEC EDGAR Recent Filings (30 days)",
        "script": "download_sec_edgar_recent.py",
        "priority": 1,
        "est_size_gb": 0.5,
        "est_records": 10000,
    },
    "fara_registrations": {
        "name": "FARA Foreign Agent Registrations",
        "script": "download_fara.py",
        "priority": 2,
        "est_size_gb": 0.2,
        "est_records": 50000,
    },
    "lobbying_disclosure": {
        "name": "Lobbying Disclosure Database",
        "script": "download_lobbying.py",
        "priority": 2,
        "est_size_gb": 0.5,
        "est_records": 200000,
    },
    "usa_spending_recent": {
        "name": "USA Spending Recent Awards",
        "script": "download_usa_spending.py",
        "priority": 2,
        "est_size_gb": 5,
        "est_records": 1000000,
    },
    "congress_members": {
        "name": "Congress.gov Members & Votes",
        "script": "download_congress.py",
        "priority": 3,
        "est_size_gb": 0.1,
        "est_records": 10000,
        "api_key": "CONGRESS_API_KEY",
    },
    "govinfo_register": {
        "name": "GovInfo Federal Register",
        "script": "download_govinfo.py",
        "priority": 3,
        "est_size_gb": 0.5,
        "est_records": 50000,
        "api_key": "GOVINFO_API_KEY",
    },
}


def is_locked(dataset_id: str) -> bool:
    """Check if a dataset download is in progress"""
    lock_file = LOCK_DIR / f"{dataset_id}.lock"
    if lock_file.exists():
        # Check if lock is stale (>4 hours)
        lock_age = datetime.now().timestamp() - lock_file.stat().st_mtime
        if lock_age > 4 * 3600:  # 4 hours
            logger.warning(f"Removing stale lock for {dataset_id}")
            lock_file.unlink()
            return False
        return True
    return False


def acquire_lock(dataset_id: str) -> bool:
    """Acquire a lock for downloading a dataset"""
    lock_file = LOCK_DIR / f"{dataset_id}.lock"
    if is_locked(dataset_id):
        return False
    lock_file.write_text(str(datetime.now()))
    return True


def release_lock(dataset_id: str):
    """Release the lock for a dataset"""
    lock_file = LOCK_DIR / f"{dataset_id}.lock"
    if lock_file.exists():
        lock_file.unlink()


def run_download_script(script_name: str, dataset_id: str, dataset_name: str) -> Dict:
    """Execute a download script and return results"""
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        logger.error(f"Script not found: {script_path}")
        return {
            "dataset": dataset_name,
            "status": "failed",
            "error": f"Script not found: {script_name}",
            "timestamp": datetime.now().isoformat(),
        }
    
    logger.info(f"Starting download: {dataset_name}")
    start_time = datetime.now()
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(Path(__file__).parent),
            capture_output=True,
            text=True,
            timeout=7200,  # 2 hour timeout
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if result.returncode == 0:
            logger.info(f"✅ {dataset_name} completed in {duration:.1f}s")
            return {
                "dataset": dataset_name,
                "status": "success",
                "duration": duration,
                "stdout": result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout,
                "timestamp": end_time.isoformat(),
            }
        else:
            logger.error(f"❌ {dataset_name} failed: {result.stderr}")
            return {
                "dataset": dataset_name,
                "status": "failed",
                "error": result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr,
                "duration": duration,
                "timestamp": end_time.isoformat(),
            }
            
    except subprocess.TimeoutExpired:
        logger.error(f"⏱️ {dataset_name} timed out (>2 hours)")
        return {
            "dataset": dataset_name,
            "status": "timeout",
            "error": "Download exceeded 2 hour timeout",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.exception(f"💥 {dataset_name} exception: {e}")
        return {
            "dataset": dataset_name,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def download_worker(dataset_id: str, config: Dict) -> Dict:
    """Worker function for parallel downloads"""
    dataset_name = config["name"]
    script_name = config["script"]
    
    # Check for API key requirement
    if "api_key" in config:
        api_key = os.environ.get(config["api_key"])
        if not api_key:
            return {
                "dataset": dataset_name,
                "status": "skipped",
                "reason": f"API key {config['api_key']} not set",
                "timestamp": datetime.now().isoformat(),
            }
    
    # Acquire lock
    if not acquire_lock(dataset_id):
        return {
            "dataset": dataset_name,
            "status": "skipped",
            "reason": "Download already in progress",
            "timestamp": datetime.now().isoformat(),
        }
    
    try:
        result = run_download_script(script_name, dataset_id, dataset_name)
        return result
    finally:
        release_lock(dataset_id)


def run_parallel_downloads(max_workers: int = MAX_WORKERS, priority_filter: Optional[int] = None):
    """Run downloads in parallel with priority filtering"""
    
    # Filter datasets by priority if specified
    datasets_to_download = []
    for dataset_id, config in DATASETS.items():
        if priority_filter is None or config["priority"] <= priority_filter:
            if not is_locked(dataset_id):
                datasets_to_download.append((dataset_id, config))
    
    # Sort by priority
    datasets_to_download.sort(key=lambda x: x[1]["priority"])
    
    if not datasets_to_download:
        logger.info("No datasets to download (all locked or filtered)")
        return []
    
    logger.info(f"Starting parallel download of {len(datasets_to_download)} datasets with {max_workers} workers")
    
    results = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_dataset = {
            executor.submit(download_worker, dataset_id, config): (dataset_id, config)
            for dataset_id, config in datasets_to_download
        }
        
        # Process completed downloads
        for future in as_completed(future_to_dataset):
            dataset_id, config = future_to_dataset[future]
            try:
                result = future.result()
                results.append(result)
                
                # Log progress
                success_count = sum(1 for r in results if r["status"] == "success")
                fail_count = sum(1 for r in results if r["status"] in ["failed", "error", "timeout"])
                logger.info(f"Progress: {len(results)}/{len(datasets_to_download)} complete | ✅ {success_count} | ❌ {fail_count}")
                
            except Exception as e:
                logger.exception(f"Future failed for {config['name']}: {e}")
                results.append({
                    "dataset": config["name"],
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                })
    
    return results


def save_results(results: List[Dict]):
    """Save download results to JSON file"""
    results_file = LOG_DIR / f"download_results_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "summary": {
                "total": len(results),
                "success": sum(1 for r in results if r["status"] == "success"),
                "failed": sum(1 for r in results if r["status"] in ["failed", "error"]),
                "skipped": sum(1 for r in results if r["status"] == "skipped"),
                "timeout": sum(1 for r in results if r["status"] == "timeout"),
            }
        }, f, indent=2)
    logger.info(f"Results saved to {results_file}")


def update_database_inventory(results: List[Dict]):
    """Update PostgreSQL inventory with download status"""
    import psycopg2
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='epstein',
            user='cbwinslow',
            password='123qweasd'
        )
        cur = conn.cursor()
        
        for result in results:
            status = result["status"]
            dataset_name = result["dataset"]
            
            # Map status to inventory status
            if status == "success":
                db_status = "downloaded"
            elif status == "failed":
                db_status = "failed"
            elif status == "skipped":
                db_status = "pending"
            else:
                db_status = "error"
            
            # Update inventory
            cur.execute("""
                UPDATE data_inventory 
                SET status = %s,
                    last_updated = NOW(),
                    metadata = jsonb_set(
                        COALESCE(metadata, '{}'::jsonb),
                        '{download_result}',
                        %s::jsonb
                    )
                WHERE source_name = %s
            """, (db_status, json.dumps(result), dataset_name))
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database inventory updated")
        
    except Exception as e:
        logger.error(f"Failed to update database inventory: {e}")


def main():
    """Main orchestration function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Government Data Download Orchestrator")
    parser.add_argument("--priority", type=int, help="Only download datasets with priority <= N")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS, help="Number of parallel workers")
    parser.add_argument("--dataset", type=str, help="Download specific dataset only")
    parser.add_argument("--update-db", action="store_true", help="Update PostgreSQL inventory after downloads")
    
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("GOVERNMENT DATA DOWNLOAD ORCHESTRATOR")
    logger.info("=" * 80)
    logger.info(f"Max workers: {args.workers}")
    logger.info(f"Priority filter: {args.priority if args.priority else 'None (all)'}")
    logger.info(f"Target datasets: {args.dataset if args.dataset else 'All available'}")
    logger.info("=" * 80)
    
    # Single dataset mode
    if args.dataset:
        if args.dataset in DATASETS:
            config = DATASETS[args.dataset]
            logger.info(f"Single dataset mode: {config['name']}")
            result = download_worker(args.dataset, config)
            results = [result]
        else:
            logger.error(f"Unknown dataset: {args.dataset}")
            sys.exit(1)
    else:
        # Parallel download mode
        results = run_parallel_downloads(
            max_workers=args.workers,
            priority_filter=args.priority
        )
    
    # Save results
    save_results(results)
    
    # Update database if requested
    if args.update_db:
        update_database_inventory(results)
    
    # Print summary
    logger.info("=" * 80)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("=" * 80)
    
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] in ["failed", "error"])
    skipped = sum(1 for r in results if r["status"] == "skipped")
    timeout = sum(1 for r in results if r["status"] == "timeout")
    
    logger.info(f"Total datasets: {len(results)}")
    logger.info(f"✅ Success: {success}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"⏭️ Skipped: {skipped}")
    logger.info(f"⏱️ Timeout: {timeout}")
    logger.info("=" * 80)
    
    # Exit with error code if any failures
    if failed > 0 or timeout > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
