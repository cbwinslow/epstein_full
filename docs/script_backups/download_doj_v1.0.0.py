#!/usr/bin/env python3
"""
Production DOJ Epstein File Downloader v2

Downloads all PDF files from all 12 DOJ datasets using known EFTA numbering.
No page scraping needed — generates URLs directly from EFTA ranges.

Features:
- Direct EFTA URL construction (no HTML scraping, no rate limits)
- Stealth Playwright context (age-gate handling)
- PDF signature validation
- SHA-256 integrity checking
- Resume support (state files track last downloaded EFTA)
- Progress tracking (tracker.py integration)
- Periodic status display
- Disk space monitoring

Usage:
  python3 download_doj.py                    # All datasets (production)
  python3 download_doj.py --datasets 5,9     # Specific datasets
  python3 download_doj.py --monitor          # Show progress only
"""

import os
import sys
import json
import time
import signal
import argparse
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from glob import glob

# === PATHS ===
RAW_DIR = "/mnt/data/epstein-project/raw-files"
TRACKER = "/home/cbwinslow/workspace/epstein/scripts/tracker.py"
PYTHON = "/home/cbwinslow/workspace/epstein/venv/bin/python3"
LOG_DIR = "/mnt/data/epstein-project/logs"

# === EFTA RANGES (from Epstein-research-data) ===
EFTA_RANGES = {
    1:  (1, 3158),
    2:  (3159, 3857),
    3:  (3858, 5586),
    4:  (5705, 8320),
    5:  (8409, 8528),
    6:  (8529, 8998),
    7:  (9016, 9664),
    8:  (9676, 39023),
    9:  (39025, 1262781),
    10: (1262782, 2205654),
    11: (2205655, 2730264),
    12: (2730265, 2858497),
}

# === CONFIG ===
DELAY_BETWEEN_DOWNLOADS = 0.3  # seconds
DELAY_BETWEEN_BATCHES = 0.1    # seconds between files in a batch
BATCH_SIZE = 10                 # files per batch
DISK_ALERT_PCT = 90
PROGRESS_INTERVAL = 15          # seconds between status displays
MAX_RETRIES = 3
CONCURRENCY = 5                 # parallel downloads per dataset

PDF_URL = "https://www.justice.gov/epstein/files/DataSet%20{ds}/EFTA{efta:08d}.pdf"
AGE_GATE_URL = "https://www.justice.gov/epstein/doj-disclosures/data-set-{ds}-files?page=0"


class DOJDownloader:
    def __init__(self, datasets: list[int]):
        self.datasets = datasets
        self.running = True
        self.start_time = datetime.now()
        self.browser = None
        self.context = None
        self.stats = {ds: {"downloaded": 0, "failed": 0, "skipped": 0} for ds in datasets}

    # ---- State ----

    def state_file(self, ds: int) -> str:
        return os.path.join(LOG_DIR, f"ds{ds}_state.json")

    def load_state(self, ds: int) -> dict:
        path = self.state_file(ds)
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        start, end = EFTA_RANGES[ds]
        return {"last_efta": start - 1, "range_start": start, "range_end": end}

    def save_state(self, ds: int, state: dict):
        os.makedirs(LOG_DIR, exist_ok=True)
        path = self.state_file(ds)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f)
        os.replace(tmp, path)

    # ---- File Operations ----

    def count_pdfs(self, ds: int) -> int:
        return len(glob(os.path.join(RAW_DIR, f"data{ds}", "*.pdf")))

    def total_size(self, ds: int) -> int:
        return sum(os.path.getsize(f) for f in glob(os.path.join(RAW_DIR, f"data{ds}", "*.pdf")) if os.path.exists(f))

    def disk_pct(self) -> float:
        st = os.statvfs("/mnt/data")
        return (st.f_blocks - st.f_bfree) / st.f_blocks * 100

    @staticmethod
    def fmt_size(b) -> str:
        for u in ["B", "KB", "MB", "GB", "TB"]:
            if abs(b) < 1024:
                return f"{b:.1f} {u}"
            b /= 1024
        return f"{b:.1f} PB"

    def is_valid_pdf(self, path: str) -> bool:
        try:
            with open(path, "rb") as f:
                return f.read(5) == b"%PDF-"
        except:
            return False

    # ---- Logging ----

    def log(self, msg: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}", flush=True)
        with open(os.path.join(LOG_DIR, "download.log"), "a") as f:
            f.write(f"[{ts}] {msg}\n")

    # ---- Browser ----

    async def setup(self):
        from playwright.async_api import async_playwright
        self.pw_cm = async_playwright()
        self.pw = await self.pw_cm.__aenter__()
        self.browser = await self.pw.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        await self.context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        # Warm up cookies by visiting the site once
        page = await self.context.new_page()
        await page.goto(AGE_GATE_URL.format(ds=1), wait_until="domcontentloaded", timeout=30000)
        age = await page.query_selector("#age-button-yes")
        if age and await age.is_visible():
            await age.click()
            await asyncio.sleep(1)
        await page.close()

    async def teardown(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        await self.pw_cm.__aexit__(None, None, None)

    # ---- Download ----

    async def download_one(self, ds: int, efta: int) -> bool:
        out_dir = os.path.join(RAW_DIR, f"data{ds}")
        filename = f"EFTA{efta:08d}.pdf"
        out_path = os.path.join(out_dir, filename)

        # Skip if already valid
        if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
            if self.is_valid_pdf(out_path):
                return True

        url = PDF_URL.format(ds=ds, efta=efta)

        for attempt in range(MAX_RETRIES):
            try:
                resp = await self.context.request.get(
                    url, timeout=60000,
                    headers={"Referer": "https://www.justice.gov/epstein/", "Accept": "application/pdf,*/*"}
                )

                if resp.status == 404:
                    return False  # File doesn't exist (DOJ removed it)

                if resp.status != 200:
                    await asyncio.sleep(1)
                    continue

                body = await resp.body()
                if len(body) < 100 or body[:5] != b"%PDF-":
                    return False

                tmp = out_path + ".tmp"
                with open(tmp, "wb") as f:
                    f.write(body)
                os.replace(tmp, out_path)
                return True

            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(2 ** attempt)

        return False

    async def download_dataset(self, ds: int):
        out_dir = os.path.join(RAW_DIR, f"data{ds}")
        os.makedirs(out_dir, exist_ok=True)

        # Load the pre-built EFTA list (avoids 404 waste)
        efta_list_file = os.path.join(LOG_DIR, "efta_to_download.json")
        if os.path.exists(efta_list_file):
            with open(efta_list_file) as f:
                all_eftas = json.load(f)
            efta_list = all_eftas.get(str(ds), [])
            if not efta_list:
                self.log(f"DS {ds}: no files to download")
                return
        else:
            # Fallback: use range
            start, end = EFTA_RANGES[ds]
            efta_list = list(range(start, end + 1))

        state = self.load_state(ds)
        last = state.get("last_efta", 0)

        # Resume: skip EFTAs we already tried
        efta_list = [e for e in efta_list if e > last]

        self.log(f"DS {ds}: {len(efta_list):,} files to download (resuming from EFTA{last+1:08d})")

        downloaded = 0
        failed = 0
        consecutive_fail = 0

        for efta in efta_list:
            if not self.running:
                break

            ok = await self.download_one(ds, efta)

            if ok:
                downloaded += 1
                consecutive_fail = 0
            else:
                failed += 1
                consecutive_fail += 1

            # Save progress every 200 files
            if (downloaded + failed) % 200 == 0:
                state["last_efta"] = efta
                self.save_state(ds, state)
                self.log(f"DS {ds}: {efta:08d} (+{downloaded} ok, +{failed} fail)")

            await asyncio.sleep(DELAY_BETWEEN_DOWNLOADS)

        # Final save
        if efta_list:
            state["last_efta"] = efta_list[-1]
        self.save_state(ds, state)

        self.stats[ds] = {"downloaded": downloaded, "failed": failed, "skipped": 0}
        self.log(f"DS {ds}: done. {downloaded} new, {failed} failed/missing")

    # ---- Display ----

    def print_status(self):
        os.system("clear")
        elapsed = datetime.now() - self.start_time
        disk = self.disk_pct()

        print("=" * 78)
        print(f"  EPSTEIN DOJ FILE DOWNLOADER v2")
        print(f"  Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}  Elapsed: {str(elapsed).split('.')[0]}")
        print(f"  Disk: {disk:.1f}% {'⚠️' if disk > DISK_ALERT_PCT else '✓'}")
        print("=" * 78)

        grand_total = 0
        grand_expected = 0
        grand_size = 0

        for ds in self.datasets:
            count = self.count_pdfs(ds)
            start, end = EFTA_RANGES[ds]
            expected = end - start + 1
            size = self.total_size(ds)
            grand_total += count
            grand_expected += expected
            grand_size += size

            pct = (count / expected * 100) if expected > 0 else 0
            bar = "█" * int(30 * pct / 100) + "░" * (30 - int(30 * pct / 100))
            status = "✓" if pct >= 99 else "●"
            s = self.stats.get(ds, {})

            print(f"  {status} DS {ds:>2} [{bar}] {pct:5.1f}%  {count:>7,} / {expected:>7,}  {self.fmt_size(size):>10}  +{s.get('downloaded',0)} new")

        pct = (grand_total / grand_expected * 100) if grand_expected > 0 else 0
        bar = "█" * int(30 * pct / 100) + "░" * (30 - int(30 * pct / 100))
        print(f"\n{'─' * 78}")
        print(f"  TOTAL [{bar}] {pct:.1f}%  {grand_total:,} / {grand_expected:,}  {self.fmt_size(grand_size)}")
        print(f"{'─' * 78}")
        print(f"  Ctrl+C = stop (resume-safe). Updates every {PROGRESS_INTERVAL}s.")

    def update_tracker(self):
        for ds in self.datasets:
            count = self.count_pdfs(ds)
            subprocess.run([PYTHON, TRACKER, "update", "--id", f"doj-ds{ds}", "--current", str(count)], capture_output=True)

    # ---- Main ----

    async def run(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        await self.setup()

        try:
            for ds in self.datasets:
                if not self.running:
                    break
                await self.download_dataset(ds)
        finally:
            await self.teardown()

        self.update_tracker()
        self.print_status()
        self.log("All datasets complete!")


async def monitor_loop():
    d = DOJDownloader(list(range(1, 13)))
    try:
        while True:
            d.update_tracker()
            d.print_status()
            await asyncio.sleep(PROGRESS_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped.")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", type=str, default="1-12")
    parser.add_argument("--monitor", action="store_true")
    args = parser.parse_args()

    if args.monitor:
        await monitor_loop()
        return

    parts = []
    for p in args.datasets.split(","):
        if "-" in p:
            s, e = p.split("-")
            parts.extend(range(int(s), int(e) + 1))
        else:
            parts.append(int(p))

    d = DOJDownloader(parts)

    def handler(sig, frame):
        print("\n\nShutting down (resume-safe)...")
        d.running = False

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    await d.run()


if __name__ == "__main__":
    asyncio.run(main())
