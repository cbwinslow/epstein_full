#!/usr/bin/env python3
"""Epstein Exposed email downloader with retry logic.

Queries the API every hour (100 req/hr limit).
Retries every minute until successful.
Tracks progress in a state file so it can resume.

Usage:
    python scripts/epstein_exposed_emails.py          # Run once (called by cron)
    python scripts/epstein_exposed_emails.py status   # Check progress
    python scripts/epstein_exposed_emails.py manual   # Run without rate limit check
"""

import sys
import os
import json
import time
import signal
import requests
import psycopg2
from datetime import datetime, timedelta

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
API_BASE = "https://epsteinexposed.com/api/v2/emails"
STATE_FILE = "/home/cbwinslow/workspace/epstein-data/downloads/ee_emails_state.json"
LOG_FILE = "/home/cbwinslow/workspace/epstein/logs/ee_emails.log"
MAX_RETRIES = 60  # Retry every minute for up to 60 minutes
RETRY_DELAY = 60  # 1 minute between retries
BATCH_SIZE = 100   # Max per page (API limit)

shutdown = False
signal.signal(signal.SIGINT, lambda s, f: globals().__setitem__('shutdown', True))
signal.signal(signal.SIGTERM, lambda s, f: globals().__setitem__('shutdown', True))


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_page": 0, "total_downloaded": 0, "last_run": None, "last_success": None}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def fetch_page(page, per_page=BATCH_SIZE):
    """Fetch one page from the API. Returns (data, meta) or raises."""
    headers = {"User-Agent": "Mozilla/5.0 (research crawler; epstein-project)"}
    resp = requests.get(API_BASE, params={"page": page, "per_page": per_page}, headers=headers, timeout=30)
    
    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 60))
        raise Exception(f"Rate limited. Retry after {retry_after}s")
    
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", []), data.get("meta", {})


def save_emails(emails):
    """Save emails to PostgreSQL. Returns count of new inserts."""
    if not emails:
        return 0
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    inserted = 0
    for email in emails:
        try:
            # Use the email's unique slug/ID from the API
            email_id = email.get("slug", email.get("id", ""))
            if not email_id:
                continue
            
            cur.execute("""
                INSERT INTO exposed_emails (source_id, subject, from_name, from_email, email_date, to_names, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_id) DO NOTHING
            """, (
                email_id,
                email.get("subject", ""),
                email.get("from", ""),
                email.get("from_email", ""),
                email.get("date", ""),
                json.dumps(email.get("to", [])),
                f"https://epsteinexposed.com/emails/{email_id}"
            ))
            if cur.rowcount > 0:
                inserted += 1
        except Exception as e:
            conn.rollback()
            continue
    
    conn.commit()
    conn.close()
    return inserted


def run_download():
    """Main download loop with retry logic."""
    state = load_state()
    state["last_run"] = datetime.now().isoformat()
    
    # Check if we already ran recently (within 50 minutes)
    if state.get("last_success"):
        last_success = datetime.fromisoformat(state["last_success"])
        elapsed = datetime.now() - last_success
        if elapsed < timedelta(minutes=50):
            log(f"Last success was {elapsed.total_seconds()/60:.0f}min ago. Skipping (wait 50min between runs).")
            save_state(state)
            return 0
    
    page = state["last_page"] + 1
    total_new = 0
    
    for attempt in range(MAX_RETRIES):
        if shutdown:
            break
        
        try:
            emails, meta = fetch_page(page)
            
            if not emails:
                log(f"No more emails at page {page}. Download complete!")
                state["last_page"] = page - 1
                state["last_success"] = datetime.now().isoformat()
                save_state(state)
                return total_new
            
            # Save to DB
            new = save_emails(emails)
            total_new += new
            state["last_page"] = page
            state["total_downloaded"] = state.get("total_downloaded", 0) + new
            state["last_success"] = datetime.now().isoformat()
            save_state(state)
            
            total_available = meta.get("total", "?")
            log(f"Page {page}: {len(emails)} fetched, {new} new. Total: {state['total_downloaded']}/{total_available}")
            
            # If we got a full batch, there might be more pages
            if len(emails) >= BATCH_SIZE:
                page += 1
                time.sleep(1)  # Small delay between pages
                continue
            else:
                log("Last page reached.")
                break
                
        except Exception as e:
            error_msg = str(e)
            if "Rate limited" in error_msg:
                log(f"Rate limited on attempt {attempt+1}/{MAX_RETRIES}. Waiting {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
                continue
            else:
                log(f"Error on attempt {attempt+1}/{MAX_RETRIES}: {error_msg}")
                time.sleep(RETRY_DELAY)
                continue
    
    save_state(state)
    return total_new


def show_status():
    state = load_state()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM exposed_emails")
    db_count = cur.fetchone()[0]
    conn.close()
    
    print(f"\nEpstein Exposed Email Downloader Status:")
    print(f"  In database: {db_count}")
    print(f"  Last page: {state.get('last_page', 0)}")
    print(f"  Total downloaded: {state.get('total_downloaded', 0)}")
    print(f"  Last run: {state.get('last_run', 'never')}")
    print(f"  Last success: {state.get('last_success', 'never')}")


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "run"
    
    if action == "status":
        show_status()
    elif action == "manual":
        # Run without rate limit check
        state = load_state()
        state["last_success"] = None
        save_state(state)
        new = run_download()
        log(f"Manual run complete: {new} new emails")
    else:
        new = run_download()
        log(f"Run complete: {new} new emails")


if __name__ == "__main__":
    main()
