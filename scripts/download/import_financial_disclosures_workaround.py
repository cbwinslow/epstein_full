#!/usr/bin/env python3
"""
House Financial Disclosures: correct URL pattern uses FD/ not privatelaw/
Senate Financial Disclosures: requires scraping the eFD search portal

House correct URL pattern:
  https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{filing_id}.pdf
  Index: https://disclosures-clerk.house.gov/public_disc/fd-data/FD{year}.zip
"""

import csv
import io
import zipfile

import requests

from config import RAW_FILES_DIR, get_db_connection, setup_file_logger

logger, log_file = setup_file_logger("import_financial_disclosures_workaround")

BASE_DIR = RAW_FILES_DIR / "financial_disclosures"

DDL = """
CREATE TABLE IF NOT EXISTS house_financial_disclosures (
    filing_id       TEXT PRIMARY KEY,
    year            INT,
    last_name       TEXT,
    first_name      TEXT,
    suffix          TEXT,
    filing_type     TEXT,
    state_dst       TEXT,
    pdf_url         TEXT,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
"""

SENATE_DDL = """
CREATE TABLE IF NOT EXISTS senate_financial_disclosures (
    report_id       TEXT PRIMARY KEY,
    first_name      TEXT,
    last_name      TEXT,
    office_name     TEXT,
    filing_type     TEXT,
    report_year     INT,
    date_received   DATE,
    pdf_url         TEXT,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
"""

SENATE_SEARCH = "https://efts.senate.gov/LATEST/search-index"


def batch_insert(conn, table, rows, conflict_col):
    if not rows:
        return
    # Deduplicate rows by conflict_col to prevent "affect row a second time" error
    seen = {}
    deduped = []
    for row in rows:
        key = row[conflict_col]
        if key not in seen:
            seen[key] = True
            deduped.append(row)
    rows = deduped

    cols = list(rows[0].keys())
    values = [[r[c] for c in cols] for r in rows]
    col_str = ", ".join(cols)
    update_str = ", ".join(f"{c}=EXCLUDED.{c}" for c in cols if c != conflict_col)
    sql = f"""
        INSERT INTO {table} ({col_str})
        VALUES %s
        ON CONFLICT ({conflict_col}) DO UPDATE SET {update_str}
    """
    try:
        with conn.cursor() as cur:
            from psycopg2.extras import execute_values

            execute_values(cur, sql, values)
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def ingest_house_fd(conn, years=range(2000, 2025)):
    """
    The correct FD index URL. Each ZIP contains a CSV index + PDFs are linked separately.
    """
    for year in years:
        # CORRECT URL pattern from disclosures-clerk.house.gov
        url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip"
        logger.info(f"House FD {year}: {url}")
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            if len(r.content) < 5000:
                logger.warning(
                    f"Suspiciously small response for {year}: {len(r.content)} bytes — skipping"
                )
                continue
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                txt_files = [n for n in z.namelist() if n.lower().endswith(".txt")]
                for txt_name in txt_files:
                    with z.open(txt_name) as f:
                        reader = csv.DictReader(
                            io.TextIOWrapper(f, encoding="utf-8"), delimiter="\t"
                        )
                        rows = []
                        for row in reader:
                            doc_id = row.get("DocID", "").strip()
                            if not doc_id:
                                continue
                            rows.append(
                                {
                                    "filing_id": doc_id,
                                    "year": year,
                                    "last_name": row.get("Last", "").strip(),
                                    "first_name": row.get("First", "").strip(),
                                    "suffix": row.get("Suffix", "").strip(),
                                    "filing_type": row.get("FilingType", "").strip(),
                                    "state_dst": row.get("StateDst", "").strip(),
                                    "pdf_url": (
                                        f"https://disclosures-clerk.house.gov/"
                                        f"public_disc/financial-pdfs/{year}/{doc_id}.pdf"
                                    ),
                                }
                            )
                            if len(rows) >= 500:
                                batch_insert(conn, "house_financial_disclosures", rows, "filing_id")
                                rows = []
                        if rows:
                            batch_insert(conn, "house_financial_disclosures", rows, "filing_id")
                        logger.info(f"House FD {year} done from {txt_name}")
        except Exception as e:
            logger.error(f"Failed House FD {year}: {e}")


def ingest_senate_fd(conn, years=range(2012, 2026)):
    """
    Senate eFD uses an undocumented ES endpoint that accepts JSON search.
    Works without auth — just needs correct headers.
    """
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json",
            "Referer": "https://efts.senate.gov/",
            "User-Agent": "Mozilla/5.0 (research/epstein_full)",
        }
    )
    for year in years:
        logger.info(f"Senate FD {year}")
        params = {
            "q": "",
            "dateRange": "custom",
            "fromDate": f"{year}-01-01",
            "toDate": f"{year}-12-31",
            "resultsPerPage": 100,
            "start": 0,
        }
        rows = []
        while True:
            try:
                r = session.get(SENATE_SEARCH, params=params, timeout=30)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                logger.error(f"Senate FD request failed {year}: {e}")
                break
            hits = data.get("hits", {}).get("hits", [])
            if not hits:
                break
            for hit in hits:
                src = hit.get("_source", {})
                report_id = hit.get("_id") or src.get("id")
                if not report_id:
                    continue
                rows.append(
                    {
                        "report_id": str(report_id),
                        "first_name": src.get("first_name"),
                        "last_name": src.get("last_name"),
                        "office_name": src.get("office_name"),
                        "filing_type": src.get("filing_type"),
                        "report_year": year,
                        "date_received": src.get("date_received"),
                        "pdf_url": src.get("pdf_url")
                        or (f"https://efts.senate.gov/LATEST/search-index/documents/{report_id}"),
                    }
                )
            if len(rows) >= 500:
                batch_insert(conn, "senate_financial_disclosures", rows, "report_id")
                rows = []
            total = data.get("hits", {}).get("total", {}).get("value", 0)
            params["start"] += len(hits)
            if params["start"] >= total:
                break
        if rows:
            batch_insert(conn, "senate_financial_disclosures", rows, "report_id")
        logger.info(f"Senate FD {year} done")


def update_inventory(conn, house_count, senate_count):
    try:
        with conn.cursor() as cur:
            # House Financial Disclosures
            cur.execute(
                """
                INSERT INTO data_inventory (source_name, source_type, target_table, actual_records, status, imported_at, last_updated)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (source_name) DO UPDATE SET
                    actual_records = EXCLUDED.actual_records,
                    status = EXCLUDED.status,
                    last_updated = NOW()
            """,
                (
                    "House Financial Disclosures",
                    "government",
                    "house_financial_disclosures",
                    house_count,
                    "complete" if house_count > 0 else "failed",
                ),
            )

            # Senate Financial Disclosures
            cur.execute(
                """
                INSERT INTO data_inventory (source_name, source_type, target_table, actual_records, status, imported_at, last_updated)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (source_name) DO UPDATE SET
                    actual_records = EXCLUDED.actual_records,
                    status = EXCLUDED.status,
                    last_updated = NOW()
            """,
                (
                    "Senate Financial Disclosures",
                    "government",
                    "senate_financial_disclosures",
                    senate_count,
                    "complete" if senate_count > 0 else "failed",
                ),
            )
        conn.commit()
        logger.info(f"Inventory updated: House={house_count}, Senate={senate_count}")
    except Exception as e:
        logger.error(f"Failed to update inventory: {e}")


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("HOUSE/SENATE FINANCIAL DISCLOSURES WORKAROUND INGESTION")
    logger.info("=" * 80)

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(DDL)
        cur.execute(SENATE_DDL)
    conn.commit()

    try:
        ingest_house_fd(conn)
    except Exception as e:
        logger.error(f"House FD ingestion failed: {e}")
        conn.rollback()

    try:
        ingest_senate_fd(conn)
    except Exception as e:
        logger.error(f"Senate FD ingestion failed: {e}")
        conn.rollback()

    # Get total counts
    house_total = 0
    senate_total = 0
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM house_financial_disclosures")
            house_total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM senate_financial_disclosures")
            senate_total = cur.fetchone()[0]

        update_inventory(conn, house_total, senate_total)
    except Exception as e:
        logger.error(f"Failed to get counts or update inventory: {e}")
        conn.rollback()

    conn.close()
    logger.info("=" * 80)
    logger.info(
        f"FINANCIAL DISCLOSURES INGESTION COMPLETE: House={house_total}, Senate={senate_total}"
    )
    logger.info("=" * 80)
