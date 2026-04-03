#!/usr/bin/env python3
"""
Chunked DOJ Downloader — splits large datasets into parallel chunks.

Each chunk gets its own Playwright context and downloads independently.
State is tracked per-chunk for resume support.
"""

import argparse
import asyncio
import json
import os
import signal
from datetime import datetime

RAW_DIR = "/home/cbwinslow/workspace/epstein-data/raw-files"
TRACKER = "/home/cbwinslow/workspace/epstein/scripts/tracker.py"
PYTHON = "/home/cbwinslow/workspace/epstein/venv/bin/python3"
LOG_DIR = "/home/cbwinslow/workspace/epstein-data/logs"
EFTA_LIST_FILE = os.path.join(LOG_DIR, "efta_to_download.json")

DELAY = 0.25
MAX_RETRIES = 3
DISK_ALERT = 90


class ChunkDownloader:
    def __init__(self, chunk_id: str, ds: int, efta_list: list[int]):
        self.chunk_id = chunk_id
        self.ds = ds
        self.efta_list = efta_list
        self.running = True
        self.downloaded = 0
        self.failed = 0

    def state_file(self) -> str:
        return os.path.join(LOG_DIR, f"chunk_{self.chunk_id}.json")

    def load_state(self) -> int:
        if os.path.exists(self.state_file()):
            with open(self.state_file()) as f:
                return json.load(f).get("last_index", 0)
        return 0

    def save_state(self, idx: int):
        with open(self.state_file() + ".tmp", "w") as f:
            json.dump({"last_index": idx, "chunk_id": self.chunk_id, "ds": self.ds}, f)
        os.replace(self.state_file() + ".tmp", self.state_file())

    def log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{self.chunk_id}] {msg}"
        print(line, flush=True)
        with open(os.path.join(LOG_DIR, f"chunk_{self.chunk_id}.log"), "a") as f:
            f.write(line + "\n")

    def is_valid_pdf(self, path: str) -> bool:
        try:
            with open(path, "rb") as f:
                return f.read(5) == b"%PDF-"
        except:
            return False

    async def download_one(self, ctx, efta: int) -> bool:
        out_dir = os.path.join(RAW_DIR, f"data{self.ds}")
        filename = f"EFTA{efta:08d}.pdf"
        out_path = os.path.join(out_dir, filename)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 100 and self.is_valid_pdf(out_path):
            return True

        url = f"https://www.justice.gov/epstein/files/DataSet%20{self.ds}/EFTA{efta:08d}.pdf"

        for attempt in range(MAX_RETRIES):
            try:
                resp = await ctx.request.get(url, timeout=60000, headers={
                    "Referer": "https://www.justice.gov/epstein/",
                    "Accept": "application/pdf,*/*"
                })
                if resp.status == 404:
                    return False
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
            except:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(2 ** attempt)
        return False

    async def run(self, ctx):
        os.makedirs(os.path.join(RAW_DIR, f"data{self.ds}"), exist_ok=True)
        start_idx = self.load_state()
        remaining = self.efta_list[start_idx:]
        self.log(f"Starting: {len(remaining):,} files (DS {self.ds})")

        for i, efta in enumerate(remaining):
            if not self.running:
                break
            ok = await self.download_one(ctx, efta)
            if ok:
                self.downloaded += 1
            else:
                self.failed += 1

            if (self.downloaded + self.failed) % 500 == 0:
                self.save_state(start_idx + i + 1)
                self.log(f"Progress: {start_idx + i + 1:,}/{len(self.efta_list):,} (+{self.downloaded} ok, +{self.failed} fail)")

            await asyncio.sleep(DELAY)

        self.save_state(start_idx + len(remaining))
        self.log(f"Done: {self.downloaded:,} downloaded, {self.failed:,} failed")


def split_list(lst: list, n: int) -> list[list]:
    """Split a list into n roughly equal chunks."""
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


async def run_chunks(chunk_configs: list[dict]):
    """Run multiple chunks in parallel."""
    from playwright.async_api import async_playwright

    pw_cm = async_playwright()
    pw = await pw_cm.__aenter__()
    browser = await pw.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
    )

    # Create one context per chunk
    contexts = []
    for cfg in chunk_configs:
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        await ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        contexts.append(ctx)

    # Warm up: visit site once per context
    for ctx in contexts:
        page = await ctx.new_page()
        await page.goto("https://www.justice.gov/epstein/doj-disclosures/data-set-1-files?page=0",
                        wait_until="domcontentloaded", timeout=30000)
        age = await page.query_selector("#age-button-yes")
        if age and await age.is_visible():
            await age.click()
            await asyncio.sleep(0.5)
        await page.close()

    # Create chunk downloaders
    downloaders = []
    for cfg in chunk_configs:
        d = ChunkDownloader(cfg["id"], cfg["ds"], cfg["eftas"])
        downloaders.append(d)

    # Run all chunks concurrently
    tasks = []
    for d, ctx in zip(downloaders, contexts):
        tasks.append(asyncio.create_task(d.run(ctx)))

    # Wait for all to complete
    await asyncio.gather(*tasks, return_exceptions=True)

    # Cleanup
    for ctx in contexts:
        await ctx.close()
    await browser.close()
    await pw_cm.__aexit__(None, None, None)

    # Summary
    total_dl = sum(d.downloaded for d in downloaders)
    total_fail = sum(d.failed for d in downloaders)
    print(f"\nAll chunks done: {total_dl:,} downloaded, {total_fail:,} failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", type=int, default=15, help="Total parallel chunks")
    args = parser.parse_args()

    with open(EFTA_LIST_FILE) as f:
        efta_lists = json.load(f)

    # Build chunk configs
    chunk_configs = []
    chunk_num = 0

    for ds_str, eftas in efta_lists.items():
        ds = int(ds_str)
        if not eftas:
            continue

        # Split large datasets, keep small ones as single chunks
        if len(eftas) > 10000:
            # Determine number of chunks for this dataset
            # Distribute chunks proportionally
            n_chunks = max(1, min(5, len(eftas) // 50000 + 1))
            sub_lists = split_list(eftas, n_chunks)
        else:
            sub_lists = [eftas]

        for sub in sub_lists:
            chunk_num += 1
            chunk_configs.append({
                "id": f"c{chunk_num:02d}",
                "ds": ds,
                "eftas": sub
            })

    print(f"Created {len(chunk_configs)} chunks across {len(efta_lists)} datasets")
    for c in chunk_configs:
        print(f"  {c['id']}: DS {c['ds']}, {len(c['eftas']):,} files")

    # Signal handling
    loop = asyncio.get_event_loop()

    def handler():
        print("\nShutting down (resume-safe)...")
        for cfg in chunk_configs:
            cfg["_stop"] = True

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, handler)

    asyncio.run(run_chunks(chunk_configs))


if __name__ == "__main__":
    main()
