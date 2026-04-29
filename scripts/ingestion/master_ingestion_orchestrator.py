#!/usr/bin/env python3
"""
MASTER INGESTION ORCHESTRATOR - ALL DATA SOURCES

This script orchestrates parallel ingestion of ALL missing financial disclosure data
using available workers to maximize throughput and minimize completion time.

Strategy:
- Worker 1: FEC Campaign Finance (2000-2023) - 400M records
- Worker 2: LDA Lobbying Filings (2000-2026) - 250K records
- Worker 3: House CapitolGains (1995-2007) - 25K disclosures + 10K trades
- Worker 4: Senate CapitolGains (2000-2011) - 1.5K disclosures + 500 trades
- Worker 5: SEC EDGAR Insider Transactions (2000-2026) - 50K records
- Worker 6: White House Logs (2000-2008) - 500K records

All workers run in parallel with rate limiting and error handling.
"""

import logging
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import psycopg2

# Configuration
RAW_FILES_DIR = Path("/home/cbwinslow/workspace/epstein/epstein-data/raw-files")
LOG_DIR = RAW_FILES_DIR / "ingestion_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
log_file = LOG_DIR / f"master_ingestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Worker configurations
WORKERS = {
    "worker_1_fec": {
        "name": "FEC Campaign Finance (2000-2023)",
        "script": "scripts/ingestion/fec_complete_ingestion.py",
        "command": ["python3", "scripts/ingestion/fec_complete_ingestion.py", "--all-cycles"],
        "description": "Ingest all FEC individual contributions for 2000-2023 cycles (~400M records)",
        "priority": 1,
        "estimated_time": 7200,  # 2 hours
        "enabled": True,
    },
    "worker_2_lda": {
        "name": "LDA Lobbying Filings (2000-2026)",
        "script": "scripts/ingestion/lda_ingestion.py",
        "command": ["python3", "scripts/ingestion/lda_ingestion.py", "--all-years"],
        "description": "Ingest all LDA lobbying filings for 2000-2026 (~250K records)",
        "priority": 1,
        "estimated_time": 1800,  # 30 min
        "enabled": True,
    },
    "worker_3_house_capitolgains": {
        "name": "House CapitolGains (1995-2007)",
        "script": "scripts/ingestion/senate_bulk_ingest.py",
        "command": [
            "python3",
            "scripts/ingestion/senate_bulk_ingest.py",
            "--chamber",
            "HOUSE",
            "--years",
            "1995:2007",
        ],
        "description": "Ingest House disclosures and trades for 1995-2007 (~25K disclosures + 10K trades)",
        "priority": 2,
        "estimated_time": 3600,  # 1 hour
        "enabled": True,
    },
    "worker_4_senate_capitolgains": {
        "name": "Senate CapitolGains (2000-2011)",
        "script": "scripts/ingestion/senate_bulk_ingest.py",
        "command": [
            "python3",
            "scripts/ingestion/senate_bulk_ingest.py",
            "--chamber",
            "SENATE",
            "--years",
            "2000:2011",
        ],
        "description": "Ingest Senate disclosures and trades for 2000-2011 (~1.5K disclosures + 500 trades)",
        "priority": 2,
        "estimated_time": 1800,  # 30 min
        "enabled": True,
    },
    "worker_5_sec_edgar": {
        "name": "SEC EDGAR Insider Transactions (2000-2026)",
        "script": "scripts/ingestion/sec_insider_ingestion.py",
        "command": ["python3", "scripts/ingestion/sec_insider_ingestion.py", "--all-years"],
        "description": "Ingest all SEC insider transactions for 2000-2026 (~50K records)",
        "priority": 3,
        "estimated_time": 3600,  # 1 hour
        "enabled": True,
    },
    "worker_6_whitehouse": {
        "name": "White House Visitor Logs (2000-2008)",
        "script": "scripts/ingestion/whitehouse_logs_ingestion.py",
        "command": [
            "python3",
            "scripts/ingestion/whitehouse_logs_ingestion.py",
            "--start-year",
            "2000",
            "--end-year",
            "2008",
        ],
        "description": "Ingest White House visitor logs for 2000-2008 (~500K records)",
        "priority": 3,
        "estimated_time": 3600,  # 1 hour
        "enabled": True,
    },
}


def check_database_connection():
    """Verify database connectivity."""
    try:
        conn = psycopg2.connect(dbname="epstein", user="postgres", host="localhost")
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("✅ Database connection verified")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def check_script_exists(script_path):
    """Check if script exists and is executable."""
    path = Path(script_path)
    if path.exists():
        logger.info(f"✅ Script exists: {script_path}")
        return True
    else:
        logger.warning(f"⚠️  Script not found: {script_path}")
        return False


def run_worker(worker_id, config):
    """Execute a single worker task."""
    logger.info(f"{'=' * 80}")
    logger.info(f"🚀 STARTING {worker_id.upper()}: {config['name']}")
    logger.info(f"{'=' * 80}")
    logger.info(f"Command: {' '.join(config['command'])}")
    logger.info(f"Description: {config['description']}")

    start_time = time.time()

    try:
        # Create worker-specific log file
        worker_log = LOG_DIR / f"{worker_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Execute the command
        result = subprocess.run(
            config["command"],
            capture_output=True,
            text=True,
            timeout=config["estimated_time"] + 300,  # Add 5 min buffer
            cwd="/home/cbwinslow/workspace/epstein",
        )

        elapsed = time.time() - start_time

        # Save worker log
        with open(worker_log, "w") as f:
            f.write(f"Worker: {worker_id}\n")
            f.write(f"Command: {' '.join(config['command'])}\n")
            f.write(f"Start Time: {datetime.now().isoformat()}\n")
            f.write(f"Elapsed: {elapsed:.2f}s\n")
            f.write(f"Return Code: {result.returncode}\n")
            f.write(f"\nSTDOUT:\n{result.stdout}\n")
            f.write(f"\nSTDERR:\n{result.stderr}\n")

        if result.returncode == 0:
            logger.info(f"✅ {worker_id.upper()} COMPLETED SUCCESSFULLY in {elapsed:.2f}s")
            logger.info(f"   Log: {worker_log}")
            return {
                "worker_id": worker_id,
                "status": "success",
                "elapsed": elapsed,
                "log_file": str(worker_log),
            }
        else:
            logger.error(f"❌ {worker_id.upper()} FAILED with code {result.returncode}")
            logger.error(f"   Error: {result.stderr[:500]}")
            logger.error(f"   Log: {worker_log}")
            return {
                "worker_id": worker_id,
                "status": "failed",
                "elapsed": elapsed,
                "error": result.stderr[:500],
                "log_file": str(worker_log),
            }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        logger.error(f"❌ {worker_id.upper()} TIMED OUT after {elapsed:.2f}s")
        return {
            "worker_id": worker_id,
            "status": "timeout",
            "elapsed": elapsed,
            "error": "Worker timed out",
            "log_file": str(worker_log),
        }
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ {worker_id.upper()} ERROR: {e}")
        return {
            "worker_id": worker_id,
            "status": "error",
            "elapsed": elapsed,
            "error": str(e),
            "log_file": None,
        }


def print_summary(results):
    """Print execution summary."""
    logger.info(f"\n{'=' * 80}")
    logger.info("📊 INGESTION SUMMARY")
    logger.info(f"{'=' * 80}")

    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]

    logger.info(f"\nTotal Workers: {len(results)}")
    logger.info(f"✅ Successful: {len(successful)}")
    logger.info(f"❌ Failed: {len(failed)}")

    if successful:
        logger.info("\n✅ Successful Workers:")
        for r in successful:
            logger.info(f"   - {r['worker_id']}: {r['elapsed']:.2f}s")

    if failed:
        logger.info("\n❌ Failed Workers:")
        for r in failed:
            logger.info(f"   - {r['worker_id']}: {r.get('error', 'Unknown error')}")

    total_time = sum(r["elapsed"] for r in results)
    logger.info(f"\n⏱ Total Execution Time: {total_time:.2f}s ({total_time / 60:.2f} minutes)")
    logger.info(f"{'=' * 80}\n")


def main():
    """Main orchestration function."""
    logger.info("🚀 MASTER INGESTION ORCHESTRATOR STARTING")
    logger.info(f"Start Time: {datetime.now().isoformat()}")
    logger.info(f"Workers Configured: {len(WORKERS)}")

    # Verify prerequisites
    logger.info("\n🔍 Verifying prerequisites...")
    if not check_database_connection():
        logger.error("❌ Cannot proceed without database connection")
        sys.exit(1)

    # Check scripts
    missing_scripts = []
    for worker_id, config in WORKERS.items():
        if config["enabled"] and not check_script_exists(config["script"]):
            missing_scripts.append(worker_id)

    if missing_scripts:
        logger.warning(f"⚠️  Missing scripts for: {missing_scripts}")
        logger.warning("   These workers will be skipped")
        for worker_id in missing_scripts:
            WORKERS[worker_id]["enabled"] = False

    # Group workers by priority
    priorities = sorted(set(w["priority"] for w in WORKERS.values() if w["enabled"]))

    all_results = []

    # Execute workers by priority level
    for priority in priorities:
        priority_workers = {
            k: v for k, v in WORKERS.items() if v["enabled"] and v["priority"] == priority
        }

        if not priority_workers:
            continue

        logger.info(f"\n{'=' * 80}")
        logger.info(f"📦 EXECUTING PRIORITY {priority} WORKERS")
        logger.info(f"Workers: {list(priority_workers.keys())}")
        logger.info(f"{'=' * 80}")

        # Execute priority group in parallel
        with ThreadPoolExecutor(max_workers=len(priority_workers)) as executor:
            futures = {
                executor.submit(run_worker, worker_id, config): worker_id
                for worker_id, config in priority_workers.items()
            }

            for future in as_completed(futures):
                result = future.result()
                all_results.append(result)

    # Print summary
    print_summary(all_results)

    # Final database check
    logger.info("\n🔍 Verifying final database state...")
    try:
        conn = psycopg2.connect(dbname="epstein", user="postgres", host="localhost")
        cursor = conn.cursor()

        tables = [
            ("house_financial_disclosures", "House Disclosures"),
            ("senate_financial_disclosures", "Senate Disclosures"),
            ("congress_trading", "Trading Records"),
            ("fec_individual_contributions", "FEC Contributions"),
            ("lda_filings", "LDA Filings"),
        ]

        for table, name in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                logger.info(f"   {name}: {count:,} records")
            except Exception as e:
                logger.warning(f"   {name}: Error - {e}")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"   Database check failed: {e}")

    logger.info(f"\n✅ Master Ingestion Complete at {datetime.now().isoformat()}")
    logger.info(f"   Log File: {log_file}")


if __name__ == "__main__":
    main()
