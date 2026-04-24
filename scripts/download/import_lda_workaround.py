#!/usr/bin/env python3
"""
Senate LDA workaround: use search API instead of broken bulk download endpoints.
No auth required for read. Docs: https://lda.senate.gov/api/redoc/v1/
"""

import json
import time

import requests

from config import get_db_connection, setup_file_logger

logger, log_file = setup_file_logger("import_lda_workaround")

BASE = "https://lda.senate.gov/api/v1"

DDL = """
CREATE TABLE IF NOT EXISTS lda_filings (
    filing_uuid         TEXT PRIMARY KEY,
    filing_type         TEXT,
    filing_year         INT,
    filing_period       TEXT,
    registrant_name     TEXT,
    registrant_id       TEXT,
    client_name         TEXT,
    client_id           TEXT,
    lobbyist_names      JSONB,
    lobbying_activities JSONB,
    income              NUMERIC,
    expenses            NUMERIC,
    signed_date         DATE,
    url                 TEXT,
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_lda_registrant ON lda_filings(registrant_name);
CREATE INDEX IF NOT EXISTS idx_lda_client ON lda_filings(client_name);
CREATE INDEX IF NOT EXISTS idx_lda_year ON lda_filings(filing_year);
"""


def paginate_lda(endpoint, params=None):
    params = params or {}
    params["page_size"] = 25  # LDA API is slow; keep small
    params["page"] = 1
    retry_count = 0
    max_retries = 5
    while True:
        try:
            r = requests.get(f"{BASE}/{endpoint}/", params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])
            if not results:
                break
            yield from results
            if not data.get("next"):
                break
            params["page"] += 1
            retry_count = 0  # Reset retry count on success
            time.sleep(1.0)  # Increased from 0.5 to avoid rate limiting
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error(
                        f"Max retries ({max_retries}) exceeded for {endpoint} page {params['page']}"
                    )
                    raise
                backoff = min(2**retry_count, 60)  # Exponential backoff, max 60s
                logger.warning(
                    f"Rate limited (429). Waiting {backoff}s before retry {retry_count}/{max_retries}"
                )
                time.sleep(backoff)
            else:
                raise


def parse_filing(f):
    lobbyists = [
        f"{l.get('lobbyist', {}).get('first_name', '')} {l.get('lobbyist', {}).get('last_name', '')}".strip()
        for l in f.get("lobbyists", [])
    ]
    activities = [
        {
            "general_issue_code": a.get("general_issue_code"),
            "description": a.get("description", "")[:500],
        }
        for a in f.get("lobbying_activities", [])
    ]
    income = None
    expenses = None
    if f.get("income"):
        try:
            income = float(str(f["income"]).replace(",", ""))
        except (ValueError, TypeError):
            pass
    if f.get("expenses"):
        try:
            expenses = float(str(f["expenses"]).replace(",", ""))
        except (ValueError, TypeError):
            pass

    return {
        "filing_uuid": f.get("filing_uuid"),
        "filing_type": f.get("filing_type"),
        "filing_year": f.get("filing_year"),
        "filing_period": f.get("filing_period"),
        "registrant_name": f.get("registrant", {}).get("name"),
        "registrant_id": str(f.get("registrant", {}).get("id", "")),
        "client_name": f.get("client", {}).get("name"),
        "client_id": str(f.get("client", {}).get("id", "")),
        "lobbyist_names": json.dumps(lobbyists),
        "lobbying_activities": json.dumps(activities),
        "income": income,
        "expenses": expenses,
        "signed_date": f.get("dt_posted"),
        "url": f"https://lda.senate.gov/filings/{f.get('filing_uuid')}/",
    }


def batch_insert(conn, table, rows):
    if not rows:
        return
    cols = list(rows[0].keys())
    values = [[r[c] for c in cols] for r in rows]
    col_str = ", ".join(cols)
    update_str = ", ".join(f"{c}=EXCLUDED.{c}" for c in cols if c != "filing_uuid")
    sql = f"""
        INSERT INTO {table} ({col_str})
        VALUES %s
        ON CONFLICT (filing_uuid) DO UPDATE SET {update_str}
    """
    with conn.cursor() as cur:
        from psycopg2.extras import execute_values

        execute_values(cur, sql, values)
    conn.commit()


def ingest_lda(conn, years=range(2015, 2026)):
    for year in years:
        logger.info(f"LDA year {year}")
        rows = []
        for filing in paginate_lda("filings", {"filing_year": year}):
            row = parse_filing(filing)
            if row["filing_uuid"]:
                rows.append(row)
            if len(rows) >= 200:
                batch_insert(conn, "lda_filings", rows)
                rows = []
        if rows:
            batch_insert(conn, "lda_filings", rows)
        logger.info(f"LDA year {year} done")


def update_inventory(conn, total_records):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO data_inventory (source_name, source_type, table_name, status, expected_records, actual_records, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (source_name) DO UPDATE SET
                    status = EXCLUDED.status,
                    actual_records = EXCLUDED.actual_records,
                    last_updated = NOW()
            """,
                (
                    "Senate LDA Lobbying",
                    "government",
                    "lda_filings",
                    "imported",
                    None,
                    total_records,
                ),
            )
        conn.commit()
        logger.info(f"Inventory updated: {total_records} records")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("SENATE LDA WORKAROUND INGESTION")
    logger.info("=" * 80)

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(DDL)
    conn.commit()

    ingest_lda(conn)

    # Get total count
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM lda_filings")
        total = cur.fetchone()[0]

    update_inventory(conn, total)

    conn.close()
    logger.info("=" * 80)
    logger.info(f"LDA INGESTION COMPLETE: {total} records")
    logger.info("=" * 80)
