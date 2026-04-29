#!/usr/bin/env python3
"""
Download bulk SEC EDGAR Form 4 (Insider Transaction) filings
Historical data from 2000 to present
"""

import json
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import requests

# Configuration
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/sec_edgar")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Logging
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"sec_bulk_download_{datetime.now():%Y%m%d_%H%M%S}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# SEC EDGAR requires proper User-Agent
HEADERS = {
    "User-Agent": "Research Bot contact@epsteinresearch.org",
    "Accept-Encoding": "gzip, deflate",
    "Host": "www.sec.gov",
}

# Rate limiting: 10 requests per second max
REQUEST_DELAY = 0.15


class SECBulkDownloader:
    def __init__(self, data_dir: Path = BASE_DIR):
        self.data_dir = data_dir
        self.base_url = "https://www.sec.gov/Archives/edgar"
        self.daily_index_url = f"{self.base_url}/daily-index"

    def get_daily_index(self, date_str: str, form_type: str = "4") -> List[Dict]:
        """
        Fetch daily index for a specific date
        Returns list of filings matching form_type
        """
        # Format: master.YYYYMMDD.idx
        index_url = f"{self.daily_index_url}/master.{date_str}.idx"

        try:
            time.sleep(REQUEST_DELAY)
            response = requests.get(index_url, headers=HEADERS, timeout=30)

            if response.status_code == 200:
                filings = []
                lines = response.text.split("\n")

                # Skip header lines (until we find the separator)
                data_started = False
                for line in lines:
                    if "----" in line:
                        data_started = True
                        continue
                    if not data_started:
                        continue

                    # Parse line: CIK|Company Name|Form Type|Date Filed|Filing Filename
                    parts = line.strip().split("|")
                    if len(parts) >= 5 and parts[2].strip() == f"{form_type}":
                        filings.append(
                            {
                                "cik": parts[0].strip(),
                                "company_name": parts[1].strip(),
                                "form_type": parts[2].strip(),
                                "date_filed": parts[3].strip(),
                                "filename": parts[4].strip(),
                            }
                        )

                return filings
            else:
                logger.warning(f"Status {response.status_code} for {date_str}")
                return []

        except Exception as e:
            logger.error(f"Error fetching {date_str}: {e}")
            return []

    def download_filing(self, filename: str, output_dir: Path) -> bool:
        """
        Download a specific filing file
        """
        url = f"{self.base_url}/{filename}"
        # Replace / with _ in filename for local storage
        safe_filename = filename.replace("/", "_")
        output_file = output_dir / safe_filename

        if output_file.exists():
            return True

        try:
            time.sleep(REQUEST_DELAY)
            response = requests.get(url, headers=HEADERS, timeout=30)

            if response.status_code == 200:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_bytes(response.content)
                return True
            else:
                logger.warning(f"Status {response.status_code} for {filename}")
                return False

        except Exception as e:
            logger.error(f"Error downloading {filename}: {e}")
            return False

    def download_form4_range(self, start_date: str, end_date: str, max_per_day: int = 500):
        """
        Download Form 4 filings for a date range

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            max_per_day: Maximum filings to download per day
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        current = start
        total_filings = 0
        total_downloaded = 0

        logger.info(f"Starting bulk download: {start_date} to {end_date}")
        logger.info(f"Max {max_per_day} filings per day")

        while current <= end:
            date_str = current.strftime("%Y%m%d")
            display_date = current.strftime("%Y-%m-%d")

            logger.info(f"\n{'=' * 60}")
            logger.info(f"Processing {display_date}")
            logger.info(f"{'=' * 60}")

            # Get filings for this date
            filings = self.get_daily_index(date_str, form_type="4")

            if filings:
                logger.info(f"Found {len(filings)} Form 4 filings")

                # Limit to max_per_day
                filings = filings[:max_per_day]

                # Create output directory for this date
                output_dir = self.data_dir / "form4_bulk" / date_str
                output_dir.mkdir(parents=True, exist_ok=True)

                # Save index
                index_file = output_dir / "filings_index.json"
                with open(index_file, "w") as f:
                    json.dump(filings, f, indent=2)

                # Download filings
                downloaded = 0
                for i, filing in enumerate(filings):
                    if self.download_filing(filing["filename"], output_dir):
                        downloaded += 1
                        total_downloaded += 1

                    if (i + 1) % 100 == 0:
                        logger.info(f"  Progress: {i + 1}/{len(filings)} downloaded")

                total_filings += len(filings)
                logger.info(f"  Completed: {downloaded}/{len(filings)} downloaded to {output_dir}")
            else:
                logger.info(f"No Form 4 filings found for {display_date}")

            current += timedelta(days=1)

        logger.info(f"\n{'=' * 60}")
        logger.info("BULK DOWNLOAD COMPLETE")
        logger.info(f"{'=' * 60}")
        logger.info(f"Date range: {start_date} to {end_date}")
        logger.info(f"Total filings found: {total_filings}")
        logger.info(f"Total downloaded: {total_downloaded}")
        logger.info(f"Output directory: {self.data_dir / 'form4_bulk'}")

        return total_downloaded

    def download_form4_recent(self, days: int = 30, max_filings: int = 1000):
        """
        Download recent Form 4 filings (last N days)
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        return self.download_form4_range(
            start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), max_per_day=max_filings
        )


def main():
    """Main function"""
    downloader = SECBulkDownloader()

    # Download last 30 days (for testing)
    logger.info("Downloading recent Form 4 filings (last 30 days)...")
    downloader.download_form4_recent(days=30, max_filings=500)

    # For bulk historical download, uncomment:
    # logger.info("Downloading bulk historical Form 4 filings (2000-2026)...")
    # downloader.download_form4_range("2000-01-01", "2026-12-31", max_per_day=500)


if __name__ == "__main__":
    main()
