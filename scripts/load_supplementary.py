#!/usr/bin/env python3
"""Load supplementary datasets into PostgreSQL."""

import json
import os

import psycopg2

PG = dict(
    host="localhost",
    port=5432,
    user="cbwinslow",
    password=os.environ.get("PG_PASSWORD", ""),
    dbname="epstein",
)
DATA = "/home/cbwinslow/workspace/epstein-data/supplementary"


def get_pg():
    return psycopg2.connect(**PG)


def load_exposed_persons(pg):
    """Load Epstein Exposed persons into external_references."""
    data = json.load(open(f"{DATA}/epstein_exposed_persons.json"))
    persons = data.get("data", [])
    print(f"  persons: {len(persons)} records")

    cur = pg.cursor()
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

    for p in persons:
        cur.execute(
            """
            INSERT INTO exposed_persons (source_id, name, slug, category, aliases, short_bio, image_url, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING
        """,
            (
                str(p.get("id")),
                p.get("name", ""),
                p.get("slug", ""),
                p.get("category", ""),
                json.dumps(p.get("aliases", [])),
                p.get("short_bio", ""),
                p.get("image_url", ""),
                p.get("status", ""),
            ),
        )
    pg.commit()
    cur.execute("SELECT COUNT(*) FROM exposed_persons")
    print(f"    loaded: {cur.fetchone()[0]} rows")


def load_exposed_flights(pg):
    """Load Epstein Exposed flights."""
    data = json.load(open(f"{DATA}/epstein_exposed_flights.json"))
    flights = data.get("data", [])
    print(f"  flights: {len(flights)} records")

    cur = pg.cursor()
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

    for f in flights:
        cur.execute(
            """
            INSERT INTO exposed_flights (source_id, flight_date, origin, destination, aircraft, pilot, passenger_count, passenger_ids)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING
        """,
            (
                str(f.get("id")),
                f.get("date", ""),
                f.get("origin", ""),
                f.get("destination", ""),
                f.get("aircraft", ""),
                f.get("pilot", ""),
                f.get("passenger_count"),
                json.dumps(f.get("passenger_ids", [])),
            ),
        )
    pg.commit()
    cur.execute("SELECT COUNT(*) FROM exposed_flights")
    print(f"    loaded: {cur.fetchone()[0]} rows")


def load_exposed_emails(pg):
    """Load Epstein Exposed emails."""
    data = json.load(open(f"{DATA}/epstein_exposed_emails.json"))
    emails = data.get("data", [])
    print(f"  emails: {len(emails)} records")

    cur = pg.cursor()
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

    for e in emails:
        cur.execute(
            """
            INSERT INTO exposed_emails (source_id, subject, from_name, from_email, email_date, to_names, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING
        """,
            (
                str(e.get("id")),
                e.get("subject", ""),
                e.get("from_name", ""),
                e.get("from_email", ""),
                e.get("date", ""),
                json.dumps(e.get("to_names", [])),
                e.get("url", ""),
            ),
        )
    pg.commit()
    cur.execute("SELECT COUNT(*) FROM exposed_emails")
    print(f"    loaded: {cur.fetchone()[0]} rows")


def load_exposed_locations(pg):
    """Load Epstein Exposed locations."""
    data = json.load(open(f"{DATA}/epstein_exposed_locations.json"))
    locations = data.get("data", [])
    print(f"  locations: {len(locations)} records")

    cur = pg.cursor()
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

    for loc in locations:
        cur.execute(
            """
            INSERT INTO exposed_locations (source_id, name, location_type, address, city, state, country, coordinates)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING
        """,
            (
                str(loc.get("id")),
                loc.get("name", ""),
                loc.get("type", ""),
                loc.get("address", ""),
                loc.get("city", ""),
                loc.get("state", ""),
                loc.get("country", ""),
                json.dumps(loc.get("coordinates", {})),
            ),
        )
    pg.commit()
    cur.execute("SELECT COUNT(*) FROM exposed_locations")
    print(f"    loaded: {cur.fetchone()[0]} rows")


def load_fec_donations(pg):
    """Load FEC political donation records."""
    path = f"{DATA}/fec_donations.json"
    if not os.path.exists(path):
        print("  fec_donations: file not found")
        return

    donations = json.load(open(path))
    print(f"  fec_donations: {len(donations)} records")

    cur = pg.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fec_donations (
            id SERIAL PRIMARY KEY,
            fec_transaction_id TEXT UNIQUE,
            contributor_name TEXT,
            contributor_city TEXT,
            contributor_state TEXT,
            contributor_zip TEXT,
            contributor_employer TEXT,
            contributor_occupation TEXT,
            recipient_name TEXT,
            recipient_committee_id TEXT,
            amount NUMERIC,
            donation_date TEXT,
            memo_text TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("TRUNCATE fec_donations")

    for d in donations:
        cur.execute(
            """
            INSERT INTO fec_donations (fec_transaction_id, contributor_name, contributor_city,
                contributor_state, contributor_zip, contributor_employer, contributor_occupation,
                recipient_name, recipient_committee_id, amount, donation_date, memo_text)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (fec_transaction_id) DO NOTHING
        """,
            (
                d.get("transaction_id", ""),
                d.get("contributor_name", ""),
                d.get("contributor_city", ""),
                d.get("contributor_state", ""),
                d.get("contributor_zip", ""),
                d.get("contributor_employer", ""),
                d.get("contributor_occupation", ""),
                d.get("recipient_name", ""),
                d.get("committee_id", ""),
                d.get("contribution_receipt_amount"),
                d.get("contribution_receipt_date", ""),
                d.get("memo_text", ""),
            ),
        )
    pg.commit()
    cur.execute("SELECT COUNT(*) FROM fec_donations")
    print(f"    loaded: {cur.fetchone()[0]} rows")


print("Loading supplementary data into PostgreSQL...")
pg = get_pg()
load_exposed_persons(pg)
load_exposed_flights(pg)
load_exposed_emails(pg)
load_exposed_locations(pg)
load_fec_donations(pg)
pg.close()
print("\nDone!")
