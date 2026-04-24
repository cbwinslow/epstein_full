#!/usr/bin/env python3
"""
Download White House Visitor Logs (WAVES records)
Source: bidenwhitehouse.archives.gov/disclosures/visitor-logs/

Covers Biden administration: 2021-2024
Total: 1,786,410 records available
"""

import concurrent.futures
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

import requests

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/whitehouse")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"whitehouse_visitors_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

BASE_DIR.mkdir(parents=True, exist_ok=True)

VISITOR_LOGS = {
    # Biden administration (2021-2024)
    "2021": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/04/2021_WAVES-ACCESS-RECORDS.csv",
    "2022_01": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/05/2022.01_WAVES-ACCESS-RECORDS.csv",
    "2022_02": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/05/2022.02_WAVES-ACCESS-RECORDS.csv",
    "2022_03": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/07/2022.03_WAVES-ACCESS-.csv",
    "2022_04": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/08/2022.04_WAVES-ACCESS-RECORDS.csv",
    "2022_05": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/08/2022.05-WAVES-ACCESS-RECORDS.csv",
    "2022_06": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/10/2022.06_WAVES-ACCESS-RECORDS.csv",
    "2022_07": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/10/2022.07_WAVES-ACCESS-RECORDS.csv",
    "2022_08": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/11/2022.08_WAVES-ACCESS-RECORDS.csv",
    "2022_09": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/12/2022.09_WAVES-ACCESS-RECORDS.csv",
    "2022_10": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/01/2022.10_WAVES-ACCESS-RECORDS.csv",
    "2022_11": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/02/2022.11_WAVES-ACCESS-RECORDS.csv",
    "2022_12": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/03/2022.12_WAVES-ACCESS-RECORDS.csv",
    "2023_01": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/04/2023.01_WAVES-ACCESS-RECORDS.csv",
    "2023_02": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/05/2023.02_WAVES-ACCESS-RECORDS.csv",
    "2023_03": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/06/2023.03_WAVES-ACCESS-RECORDS.csv",
    "2023_04": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/07/2023.04_WAVES-ACCESS-RECORDS.csv",
    "2023_05": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/08/2023.05_WAVES-ACCESS-RECORDS.csv",
    "2023_06": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/09/2023.06_WAVES-ACCESS-RECORDS.csv",
    "2023_07": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/10/2023.07_WAVES-ACCESS-RECORDS.csv",
    "2023_08": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/11/2023.08_WAVES-ACCESS-RECORDS.csv",
    "2023_09": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/12/2023.09_WAVES-ACCESS-RECORDS.csv",
    "2023_10": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/01/2023.10_WAVES-ACCESS-RECORDS.csv",
    "2023_11": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/2023.11_WAVES-ACCESS-RECORDS.csv",
    "2023_12": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/03/2023.12_WAVES-ACCESS-RECORDS.csv",
    "2024_01": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/04/2024.01_WAVES-ACCESS-RECORDS.csv",
    "2024_02": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/06/2024.02_WAVES-Access-Records.csv",
    "2024_03": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/07/2024.03_WAVES-Access-Records.csv",
    "2024_04": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/08/2024.04_WAVES-Access-Records.csv",
    "2024_05": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/09/2024.05_WAVES-Access-Records.csv",
    "2024_06": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/10/2024.06_WAVES-Access-Records.csv",
    "2024_07": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/11/2024.07_WAVES-Access-Records.csv",
    "2024_08": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2025/01/2024.08_WAVES-Access-Records.csv",
}

OBAMA_VISITOR_LOGS = {
    # Obama administration (2009-2017) - from obamawhitehouse.archives.gov
    "2009_2010": "https://obamawhitehouse.archives.gov/files/disclosures/visitors/WhiteHouse-WAVES-Released-1210.zip",
    "2011_part1": "https://obamawhitehouse.archives.gov/files/disclosures/visitors/WhiteHouse-WAVES-Released-0711b.zip",
    "2011_part2": "https://obamawhitehouse.archives.gov/files/disclosures/visitors/WhiteHouse-WAVES-Released-through-December-2011.zip",
    "2012": "https://obamawhitehouse.archives.gov/sites/default/files/disclosures/whitehouse-waves-2012.csv_.zip",
    "2013": "https://obamawhitehouse.archives.gov/sites/default/files/disclosures/whitehouse-waves-2013.csv__0.zip",
    "2014": "https://obamawhitehouse.archives.gov/sites/default/files/disclosures/whitehouse-waves-2014_03.csv_.zip",
}


def download_file(key: str, url: str) -> Dict:
    """Download a single visitor log file"""
    output_dir = BASE_DIR / key
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{key}.csv"

    if output_file.exists():
        size = output_file.stat().st_size
        logger.info(f"⏭ Already exists: {key} ({size / 1024 / 1024:.2f} MB)")
        return {"key": key, "status": "skipped", "size": size}

    logger.info(f"⬇ Downloading: {key}")
    logger.info(f"   URL: {url}")

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=300)

        if response.status_code == 200 and len(response.content) > 100:
            output_file.write_bytes(response.content)
            size = len(response.content)
            logger.info(f"✅ Downloaded: {key} ({size / 1024 / 1024:.2f} MB)")
            return {"key": key, "status": "success", "size": size}
        else:
            logger.warning(
                f"⚠️ Failed: {key} (status={response.status_code}, size={len(response.content)})"
            )
            return {"key": key, "status": "failed", "error": f"status={response.status_code}"}

    except Exception as e:
        logger.error(f"❌ Error: {key} - {e}")
        return {"key": key, "status": "error", "error": str(e)}


def download_zip_file(key: str, url: str) -> Dict:
    """Download and extract ZIP file"""
    output_dir = BASE_DIR / f"obama_{key}"
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / f"{key}.zip"

    if zip_path.exists():
        logger.info(f"⏭ ZIP exists: {key}")
    else:
        logger.info(f"⬇ Downloading: {key}")
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=600)
            if response.status_code == 200:
                zip_path.write_bytes(response.content)
                logger.info(f"✅ Downloaded: {key} ({len(response.content) / 1024 / 1024:.2f} MB)")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"key": key, "status": "error"}

    # Extract if needed
    if zip_path.exists():
        import zipfile

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(output_dir)
                logger.info(f"Extracted: {key}")
        except Exception as e:
            logger.error(f"Extract error: {e}")

    return {"key": key, "status": "success"}


def download_obama():
    """Download Obama administration visitor logs"""
    logger.info("\n--- OBAMA ADMINISTRATION ---")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(download_zip_file, key, url): key
            for key, url in OBAMA_VISITOR_LOGS.items()
        }

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    return results


def main():
    logger.info("=" * 80)
    logger.info("WHITE HOUSE VISITOR LOGS DOWNLOAD")
    logger.info("=" * 80)
    logger.info(f"Output: {BASE_DIR}")
    logger.info(f"Log: {log_file}")
    logger.info("=" * 80)

    # Download Biden
    logger.info("\n--- BIDEN ADMINISTRATION ---")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(download_file, key, url): key for key, url in VISITOR_LOGS.items()
        }

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    # Download Obama
    obama_results = download_obama()
    results.extend(obama_results)

    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] in ("failed", "error"))

    total_size = sum(r.get("size", 0) for r in results)

    logger.info("=" * 80)
    logger.info("DOWNLOAD COMPLETE")
    logger.info(f"Success: {success}, Skipped: {skipped}, Failed: {failed}")
    logger.info(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    logger.info("=" * 80)

    return {
        "success": success,
        "skipped": skipped,
        "failed": failed,
        "total_size_mb": total_size / 1024 / 1024,
    }


if __name__ == "__main__":
    main()
