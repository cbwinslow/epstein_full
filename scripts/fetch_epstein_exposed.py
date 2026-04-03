#!/usr/bin/env python3
"""
Epstein Exposed API — Comprehensive Bulk Downloader

Downloads all available data from https://epsteinexposed.com/api/v2
and loads it into PostgreSQL.

Endpoints (27 total):
  Bulk exports: persons, flights, locations, organizations
  Paginated:    emails, nonprofits, doj-audit, network, search
  Singles:      stats, network/graph

Usage:
  python fetch_epstein_exposed.py              # Download all (skip rate-limited)
  python fetch_epstein_exposed.py --force      # Re-download everything
  python fetch_epstein_exposed.py --check      # Check what's available vs downloaded
  python fetch_epstein_exposed.py --load-only  # Skip downloads, just load JSON to PG

Environment:
  PG_HOST, PG_PORT, PG_USER, PG_PASSWORD, PG_DBNAME — PostgreSQL connection
"""

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path

import requests

# =============================================================================
# Config
# =============================================================================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Accept": "application/json",
}
BASE = "https://epsteinexposed.com/api/v2"
OUTDIR = "/home/cbwinslow/workspace/epstein-data/supplementary"

PG_HOST = os.environ.get("PG_HOST", "localhost")
PG_PORT = int(os.environ.get("PG_PORT", "5432"))
PG_USER = os.environ.get("PG_USER", "cbwinslow")
PG_PASS = os.environ.get("PG_PASSWORD", "")
PG_DB = os.environ.get("PG_DBNAME", "epstein")

# Bulk export endpoints — full dataset in one request
BULK_EXPORTS = {
    "persons": {
        "endpoint": "export/persons",
        "format": "json",
        "file": "export_persons.json",
        "pg_table": "exposed_persons",
        "description": "1,578+ persons with bios, categories, aliases, stats",
    },
    "flights": {
        "endpoint": "export/flights",
        "format": "json",
        "file": "export_flights.json",
        "pg_table": "exposed_flights",
        "description": "3,615+ individual flight records with origin/destination/aircraft",
    },
    "locations": {
        "endpoint": "export/locations",
        "format": "json",
        "file": "export_locations.json",
        "pg_table": "exposed_locations",
        "description": "83+ geocoded properties, airports, institutions",
    },
    "organizations": {
        "endpoint": "export/organizations",
        "format": "json",
        "file": "export_organizations.json",
        "pg_table": "exposed_organizations",
        "description": "Companies, foundations, entities connected to the case",
    },
}

# Paginated endpoints — need multiple requests
PAGINATED = {
    "emails": {
        "endpoint": "emails",
        "file": "epstein_exposed_emails.json",
        "pg_table": "exposed_emails",
        "per_page": 200,
        "description": "11,280+ email records (news, correspondence, newsletters)",
    },
    "nonprofits": {
        "endpoint": "nonprofits",
        "file": "epstein_exposed_nonprofits.json",
        "pg_table": "exposed_nonprofits",
        "per_page": 200,
        "description": "Epstein-linked nonprofits with IRS Form 990 data",
    },
}

# Single-call endpoints
SINGLES = {
    "stats": {
        "endpoint": "stats",
        "file": "epstein_exposed_stats.json",
        "description": "Database statistics: entity counts, integrity metrics",
    },
    "network_graph": {
        "endpoint": "network/graph",
        "file": "epstein_exposed_network_graph.json",
        "description": "Full connection graph (nodes + edges)",
        "params": {"min_shared_docs": 5},
    },
    "doj_audit_stats": {
        "endpoint": "doj-audit",
        "file": "epstein_exposed_doj_audit_stats.json",
        "description": "DOJ document audit: removed, verified, size mismatches",
        "params": {"view": "stats"},
    },
    "doj_audit_analysis": {
        "endpoint": "doj-audit",
        "file": "epstein_exposed_doj_audit_analysis.json",
        "description": "Removal analysis: dataset removal rates, impacted persons",
        "params": {"view": "analysis"},
    },
}


# =============================================================================
# Helpers
# =============================================================================
def pg_conn():
    import psycopg2

    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASS, dbname=PG_DB
    )


def fetch(url, params=None, timeout=30):
    """Make a GET request, handle rate limiting and timeouts."""
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        return None, f"TIMEOUT (>{timeout}s)"
    except requests.exceptions.ConnectionError as e:
        return None, f"CONNECTION ERROR: {e}"
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 60))
        remaining = r.headers.get("X-RateLimit-Remaining", "?")
        reset = r.headers.get("X-RateLimit-Reset", "?")
        return None, f"RATE LIMITED — wait {wait}s (remaining: {remaining}, reset: {reset})"
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}: {r.text[:100]}"
    return r, None


def save_json(data, filepath):
    """Save data as JSON."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    return os.path.getsize(filepath)


def load_json(filepath):
    """Load JSON file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath) as f:
        return json.load(f)


# =============================================================================
# Download functions
# =============================================================================
def download_bulk_export(name, config):
    """Download a bulk export dataset (single request)."""
    filepath = os.path.join(OUTDIR, config["file"])
    print(f"  {name}: ", end="", flush=True)

    url = f"{BASE}/{config['endpoint']}"
    params = {"format": config.get("format", "json")}
    r, err = fetch(url, params=params, timeout=120)

    if err:
        print(err)
        return False

    try:
        data = r.json()
        if isinstance(data, list):
            count = len(data)
        elif isinstance(data, dict):
            count = len(data.get("data", data))
        else:
            count = "?"
        size = save_json(data, filepath)
        print(f"OK — {count} records, {size:,} bytes")
        return True
    except Exception as e:
        print(f"PARSE ERROR: {e}")
        return False


def download_paginated(name, config):
    """Download all pages from a paginated endpoint."""
    filepath = os.path.join(OUTDIR, config["file"])
    print(f"  {name}: ", end="", flush=True)

    all_records = []
    page = 1
    per_page = config.get("per_page", 200)

    while True:
        url = f"{BASE}/{config['endpoint']}"
        params = {"per_page": per_page, "page": page}
        r, err = fetch(url, params=params, timeout=30)

        if err:
            print(f"Page {page}: {err}")
            if all_records:
                save_json({"data": all_records, "meta": {"total": len(all_records)}}, filepath)
                print(f"  Saved partial: {len(all_records)} records")
            return False

        data = r.json()
        records = data.get("data", [])
        meta = data.get("meta", {})
        total = meta.get("total", 0)
        has_more = meta.get("has_more", False)
        all_records.extend(records)

        if not has_more or not records:
            break
        page += 1
        time.sleep(0.3)

    save_json({"data": all_records, "meta": {"total": len(all_records)}}, filepath)
    print(f"OK — {len(all_records)} records across {page} pages")
    return True


def download_singles():
    """Download single-call endpoints."""
    print("\nSingle endpoints:")
    results = []
    for name, config in SINGLES.items():
        filepath = os.path.join(OUTDIR, config["file"])
        print(f"  {name}: ", end="", flush=True)

        url = f"{BASE}/{config['endpoint']}"
        params = config.get("params", {})
        r, err = fetch(url, params=params, timeout=60)

        if err:
            print(err)
            results.append((name, False))
            continue

        try:
            data = r.json()
            size = save_json(data, filepath)
            print(f"OK — {size:,} bytes")
            results.append((name, True))
        except Exception as e:
            print(f"PARSE ERROR: {e}")
            results.append((name, False))
    return results


# =============================================================================
# Load into PostgreSQL
# =============================================================================
def load_exposed_persons(cur, filepath):
    """Load persons from bulk export into PostgreSQL."""
    data = load_json(filepath)
    if not data:
        return 0

    records = data if isinstance(data, list) else data.get("data", [])
    if not records:
        return 0

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exposed_persons (
            id SERIAL PRIMARY KEY,
            source_id TEXT UNIQUE,
            name TEXT,
            slug TEXT,
            category TEXT,
            aliases TEXT,
            short_bio TEXT,
            image_url TEXT,
            status TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("TRUNCATE exposed_persons")

    for r in records:
        cur.execute(
            """INSERT INTO exposed_persons (source_id, name, slug, category, aliases, short_bio, image_url, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING""",
            (
                str(r.get("id", "")),
                r.get("name", ""),
                r.get("slug", ""),
                r.get("category", ""),
                json.dumps(r.get("aliases", [])),
                r.get("short_bio", ""),
                r.get("image_url", ""),
                r.get("status", ""),
            ),
        )
    return len(records)


def load_exposed_flights(cur, filepath):
    """Load flights from bulk export into PostgreSQL."""
    data = load_json(filepath)
    if not data:
        return 0

    records = data if isinstance(data, list) else data.get("data", [])
    if not records:
        return 0

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exposed_flights (
            id SERIAL PRIMARY KEY,
            source_id TEXT UNIQUE,
            flight_date TEXT,
            origin TEXT,
            destination TEXT,
            aircraft TEXT,
            pilot TEXT,
            passenger_count INTEGER,
            passenger_ids JSONB,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("TRUNCATE exposed_flights")

    for r in records:
        cur.execute(
            """INSERT INTO exposed_flights (source_id, flight_date, origin, destination, aircraft, pilot, passenger_count, passenger_ids)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING""",
            (
                str(r.get("id", "")),
                r.get("date", ""),
                r.get("origin", ""),
                r.get("destination", ""),
                r.get("aircraft", ""),
                r.get("pilot", ""),
                r.get("passenger_count"),
                json.dumps(r.get("passenger_ids", [])),
            ),
        )
    return len(records)


def load_exposed_locations(cur, filepath):
    """Load locations from bulk export into PostgreSQL."""
    data = load_json(filepath)
    if not data:
        return 0

    records = data if isinstance(data, list) else data.get("data", [])
    if not records:
        return 0

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exposed_locations (
            id SERIAL PRIMARY KEY,
            source_id TEXT UNIQUE,
            name TEXT,
            location_type TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            coordinates JSONB,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("TRUNCATE exposed_locations")

    for r in records:
        cur.execute(
            """INSERT INTO exposed_locations (source_id, name, location_type, address, city, state, country, coordinates)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING""",
            (
                str(r.get("id", "")),
                r.get("name", ""),
                r.get("type", ""),
                r.get("address", ""),
                r.get("city", ""),
                r.get("state", ""),
                r.get("country", ""),
                json.dumps(r.get("coordinates", {})),
            ),
        )
    return len(records)


def load_exposed_organizations(cur, filepath):
    """Load organizations from bulk export into PostgreSQL."""
    data = load_json(filepath)
    if not data:
        return 0

    records = data if isinstance(data, list) else data.get("data", [])
    if not records:
        return 0

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exposed_organizations (
            id SERIAL PRIMARY KEY,
            source_id TEXT UNIQUE,
            name TEXT,
            slug TEXT,
            org_type TEXT,
            description TEXT,
            connected_persons INTEGER,
            connected_documents INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("TRUNCATE exposed_organizations")

    for r in records:
        cur.execute(
            """INSERT INTO exposed_organizations (source_id, name, slug, org_type, description, connected_persons, connected_documents)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING""",
            (
                str(r.get("id", "")),
                r.get("name", ""),
                r.get("slug", ""),
                r.get("category", r.get("type", "")),
                r.get("description", r.get("short_bio", "")),
                r.get("stats", {}).get("persons", 0) if isinstance(r.get("stats"), dict) else 0,
                r.get("stats", {}).get("documents", 0) if isinstance(r.get("stats"), dict) else 0,
            ),
        )
    return len(records)


def load_exposed_emails(cur, filepath):
    """Load emails from paginated data into PostgreSQL."""
    raw = load_json(filepath)
    if not raw:
        return 0

    records = raw.get("data", raw) if isinstance(raw, dict) else raw
    if not records:
        return 0

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exposed_emails (
            id SERIAL PRIMARY KEY,
            source_id TEXT UNIQUE,
            subject TEXT,
            from_name TEXT,
            from_email TEXT,
            email_date TEXT,
            to_names JSONB,
            url TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("TRUNCATE exposed_emails")

    for r in records:
        cur.execute(
            """INSERT INTO exposed_emails (source_id, subject, from_name, from_email, email_date, to_names, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING""",
            (
                str(r.get("id", "")),
                r.get("subject", ""),
                r.get("from_name", ""),
                r.get("from_email", ""),
                r.get("date", ""),
                json.dumps(r.get("to_names", [])),
                r.get("url", ""),
            ),
        )
    return len(records)


def load_exposed_nonprofits(cur, filepath):
    """Load nonprofits into PostgreSQL."""
    raw = load_json(filepath)
    if not raw:
        return 0

    records = raw.get("data", raw) if isinstance(raw, dict) else raw
    if not records:
        return 0

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exposed_nonprofits (
            id SERIAL PRIMARY KEY,
            source_id TEXT UNIQUE,
            name TEXT,
            slug TEXT,
            category TEXT,
            ein TEXT,
            officers JSONB,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("TRUNCATE exposed_nonprofits")

    for r in records:
        cur.execute(
            """INSERT INTO exposed_nonprofits (source_id, name, slug, category, ein, officers, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING""",
            (
                str(r.get("id", "")),
                r.get("name", ""),
                r.get("slug", ""),
                r.get("category", ""),
                r.get("ein", ""),
                json.dumps(r.get("officers", [])),
                r.get("description", r.get("short_bio", "")),
            ),
        )
    return len(records)


LOADERS = {
    "export_persons.json": load_exposed_persons,
    "export_flights.json": load_exposed_flights,
    "export_locations.json": load_exposed_locations,
    "export_organizations.json": load_exposed_organizations,
    "epstein_exposed_emails.json": load_exposed_emails,
    "epstein_exposed_nonprofits.json": load_exposed_nonprofits,
}


def load_all():
    """Load all JSON files into PostgreSQL."""
    print("\nLoading into PostgreSQL...")
    conn = pg_conn()
    cur = conn.cursor()
    total = 0

    for filename, loader in LOADERS.items():
        filepath = os.path.join(OUTDIR, filename)
        if os.path.exists(filepath):
            try:
                count = loader(cur, filepath)
                conn.commit()
                cur.execute(
                    f"SELECT COUNT(*) FROM {loader.__name__.replace('load_', 'exposed_').replace('exposed_exposed_', 'exposed_')}"
                )
                # Use the table name from the loader docstring or just count
                table = (
                    filename.replace("export_", "exposed_")
                    .replace("epstein_exposed_", "exposed_")
                    .replace(".json", "")
                )
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                db_count = cur.fetchone()[0]
                print(f"  {table}: {db_count} rows")
                total += db_count
            except Exception as e:
                print(f"  {filename}: ERROR — {e}")
        else:
            print(f"  {filename}: not found (skipped)")

    conn.close()
    print(f"\nTotal loaded: {total} rows")
    return total


# =============================================================================
# Check mode — what's available vs what's downloaded
# =============================================================================
def check_status():
    """Check what's downloaded vs what's available."""
    print("=" * 70)
    print("EPSTEIN EXPOSED API — Data Status")
    print("=" * 70)

    print("\nBULK EXPORTS:")
    print(f"{'Dataset':<20} {'File':<35} {'Status':<15} {'Size':>10}")
    print("-" * 80)
    for name, config in BULK_EXPORTS.items():
        filepath = os.path.join(OUTDIR, config["file"])
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            data = load_json(filepath)
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                count = len(data.get("data", []))
            else:
                count = "?"
            print(f"{name:<20} {config['file']:<35} {'DOWNLOADED':<15} {size:>10,}")
            print(f"{'':>20} {count} records — {config['description']}")
        else:
            print(f"{name:<20} {config['file']:<35} {'NOT FOUND':<15} {'':>10}")
            print(f"{'':>20} {config['description']}")

    print("\nPAGINATED ENDPOINTS:")
    print(f"{'Dataset':<20} {'File':<35} {'Status':<15} {'Size':>10}")
    print("-" * 80)
    for name, config in PAGINATED.items():
        filepath = os.path.join(OUTDIR, config["file"])
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            raw = load_json(filepath)
            records = raw.get("data", raw) if isinstance(raw, dict) else raw
            print(f"{name:<20} {config['file']:<35} {'DOWNLOADED':<15} {size:>10,}")
            print(f"{'':>20} {len(records)} records — {config['description']}")
        else:
            print(f"{name:<20} {config['file']:<35} {'NOT FOUND':<15} {'':>10}")
            print(f"{'':>20} {config['description']}")

    print("\nSINGLE ENDPOINTS:")
    print(f"{'Dataset':<20} {'File':<35} {'Status':<15} {'Size':>10}")
    print("-" * 80)
    for name, config in SINGLES.items():
        filepath = os.path.join(OUTDIR, config["file"])
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"{name:<20} {config['file']:<35} {'DOWNLOADED':<15} {size:>10,}")
        else:
            print(f"{name:<20} {config['file']:<35} {'NOT FOUND':<15} {'':>10}")
        print(f"{'':>20} {config['description']}")

    # Check PostgreSQL
    print("\nPOSTGRESQL TABLES:")
    print(f"{'Table':<30} {'Rows':>10}")
    print("-" * 42)
    try:
        conn = pg_conn()
        cur = conn.cursor()
        for table in [
            "exposed_persons",
            "exposed_flights",
            "exposed_emails",
            "exposed_locations",
            "exposed_organizations",
            "exposed_nonprofits",
        ]:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"{table:<30} {count:>10,}")
            except Exception:
                print(f"{table:<30} {'N/A':>10}")
        conn.close()
    except Exception as e:
        print(f"  Connection error: {e}")


# =============================================================================
# Main
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Epstein Exposed API downloader")
    parser.add_argument("--force", action="store_true", help="Re-download everything")
    parser.add_argument("--check", action="store_true", help="Check status only")
    parser.add_argument("--load-only", action="store_true", help="Load existing JSON to PG")
    args = parser.parse_args()

    if args.check:
        check_status()
        return

    if args.load_only:
        load_all()
        return

    os.makedirs(OUTDIR, exist_ok=True)
    start = datetime.now()

    print("=" * 70)
    print("EPSTEIN EXPOSED API — Bulk Downloader")
    print(f"Started: {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1. Bulk exports
    print("\nBulk exports (1 request each):")
    for name, config in BULK_EXPORTS.items():
        filepath = os.path.join(OUTDIR, config["file"])
        if os.path.exists(filepath) and not args.force:
            data = load_json(filepath)
            count = len(data) if isinstance(data, list) else len(data.get("data", []))
            print(f"  {name}: SKIPPED — {count} records already on disk")
            continue
        download_bulk_export(name, config)

    # 2. Paginated endpoints
    print("\nPaginated endpoints:")
    for name, config in PAGINATED.items():
        filepath = os.path.join(OUTDIR, config["file"])
        if os.path.exists(filepath) and not args.force:
            raw = load_json(filepath)
            records = raw.get("data", raw) if isinstance(raw, dict) else raw
            print(f"  {name}: SKIPPED — {len(records)} records already on disk")
            continue
        download_paginated(name, config)

    # 3. Single endpoints
    download_singles()

    # 4. Load into PostgreSQL
    load_all()

    elapsed = datetime.now() - start
    print(f"\nFinished in {elapsed}")
    print("Run with --check to see status, --load-only to re-load without downloading")


if __name__ == "__main__":
    main()
