#!/usr/bin/env python3
"""FEC donation downloader using open.fec.gov API.

Queries FEC for each person in exposed_persons.
Tracks progress in state file, runs via cron.

Usage:
    python scripts/fec_downloader.py          # Run once (cron calls this)
    python scripts/fec_downloader.py status   # Check progress
    python scripts/fec_downloader.py manual   # Run without rate limit check
"""

import sys
import os
import json
import time
import requests
import psycopg2
from datetime import datetime

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
API_KEY = "FpB5TzG4hjf7W9IwjBsdTKGyQImqhhidMKRLDXFm"
API_BASE = "https://api.open.fec.gov/v1/schedules/schedule_a/"
STATE_FILE = "/mnt/data/epstein-project/downloads/fec_state.json"
LOG_FILE = "/home/cbwinslow/workspace/epstein/logs/fec_downloader.log"
PER_PAGE = 100


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_person_index": 0, "total_downloaded": 0, "last_run": None}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_persons(conn):
    """Get list of persons to query, prioritized by document count."""
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM exposed_persons
        WHERE name IS NOT NULL AND name != '' AND name NOT LIKE '%(b)%'
        AND length(name) > 3
        ORDER BY source_id
    """)
    return [r[0] for r in cur.fetchall()]


def fetch_donations(name, page=1):
    """Fetch one page of FEC donations for a person."""
    resp = requests.get(API_BASE, params={
        "api_key": API_KEY,
        "contributor_name": name,
        "per_page": PER_PAGE,
        "page": page,
        "sort_hide_null": True
    }, timeout=15)
    
    if resp.status_code == 429:
        return None, 0, True  # rate limited
    
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", []), data.get("pagination", {}).get("count", 0), False


def save_donations(conn, results):
    """Save FEC results to database. Returns new count."""
    cur = conn.cursor()
    new = 0
    for r in results:
        txn_id = r.get("transaction_id", "")
        if not txn_id:
            continue
        try:
            cur.execute("""
                INSERT INTO fec_donations
                (fec_transaction_id, contributor_name, contributor_city, contributor_state,
                 contributor_employer, contributor_occupation, recipient_name, 
                 recipient_committee_id, amount, donation_date, memo_text)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (
                txn_id,
                r.get("contributor_name", ""),
                r.get("contributor_city", ""),
                r.get("contributor_state", ""),
                r.get("contributor_employer", ""),
                r.get("contributor_occupation", ""),
                r.get("recipient_name", ""),
                r.get("committee_id", ""),
                r.get("contribution_receipt_amount"),
                r.get("contribution_receipt_date"),
                r.get("memo_text", "")
            ))
            if cur.rowcount > 0:
                new += 1
        except:
            conn.rollback()
    conn.commit()
    return new


def run():
    state = load_state()
    state["last_run"] = datetime.now().isoformat()
    
    conn = psycopg2.connect(DB_URL)
    persons = get_persons(conn)
    
    start_idx = state.get("last_person_index", 0)
    total_new = 0
    requests_used = 0
    max_requests = 55  # Leave buffer under 60/hr limit
    
    for i in range(start_idx, len(persons)):
        if requests_used >= max_requests:
            log(f"Used {requests_used} requests. Stopping to stay under rate limit.")
            state["last_person_index"] = i
            save_state(state)
            conn.close()
            return total_new
        
        name = persons[i]
        
        try:
            results, total_avail, rate_limited = fetch_donations(name, page=1)
            requests_used += 1
            
            if rate_limited:
                log(f"Rate limited at person {i} ({name}). Stopping.")
                state["last_person_index"] = i
                save_state(state)
                conn.close()
                return total_new
            
            if total_avail == 0:
                continue
            
            new = save_donations(conn, results)
            total_new += new
            state["total_downloaded"] = state.get("total_downloaded", 0) + new
            
            # If more pages, fetch up to 5 more (5 more requests)
            pages_fetched = 1
            while total_avail > pages_fetched * PER_PAGE and pages_fetched < 5 and requests_used < max_requests:
                pages_fetched += 1
                results, _, rate_limited = fetch_donations(name, page=pages_fetched)
                requests_used += 1
                if rate_limited or not results:
                    break
                new = save_donations(conn, results)
                total_new += new
                state["total_downloaded"] = state.get("total_downloaded", 0) + new
            
            if new > 0:
                log(f"{name}: {total_avail} total, +{new} new (requests: {requests_used})")
            
        except Exception as e:
            log(f"{name}: error - {e}")
        
        time.sleep(0.5)
    
    state["last_person_index"] = 0  # Reset for next cycle
    save_state(state)
    conn.close()
    
    cur2 = psycopg2.connect(DB_URL).cursor()
    cur2.execute("SELECT COUNT(*) FROM fec_donations")
    total = cur2.fetchone()[0]
    log(f"Cycle complete: {total_new} new. Total in DB: {total}")
    return total_new


def show_status():
    state = load_state()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM fec_donations")
    db_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT contributor_name) FROM fec_donations")
    unique = cur.fetchone()[0]
    conn.close()
    
    print(f"\nFEC Downloader Status:")
    print(f"  In database: {db_count} donations from {unique} contributors")
    print(f"  Last person index: {state.get('last_person_index', 0)}")
    print(f"  Total downloaded: {state.get('total_downloaded', 0)}")
    print(f"  Last run: {state.get('last_run', 'never')}")


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "run"
    if action == "status":
        show_status()
    else:
        run()


if __name__ == "__main__":
    main()
