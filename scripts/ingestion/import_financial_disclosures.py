#!/usr/bin/env python3
"""Import congressional financial disclosure metadata and House PTR transactions.

The original downloader used the House ``public_disc/privatelaw`` URL family,
which is not the financial disclosure bulk feed. The canonical House bulk
indexes are ``public_disc/financial-pdfs/{year}FD.zip`` and House PTR PDFs are
served from ``public_disc/ptr-pdfs/{year}/{filing_id}.pdf``.
"""

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

import fitz
import requests

from config import RAW_FILES_DIR, get_db_connection, setup_file_logger

logger, log_file = setup_file_logger("import_financial_disclosures")

BASE_DIR = RAW_FILES_DIR / "financial_disclosures"
HOUSE_BULK_URLS = (
    "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip",
    "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.ZIP",
)
HOUSE_FINANCIAL_PDF_URL = (
    "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id}.pdf"
)
HOUSE_PTR_PDF_URL = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf"

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

HOUSE_PTR_OCR_DDL = """
CREATE TABLE IF NOT EXISTS house_ptr_ocr_pages (
    filing_id       TEXT NOT NULL,
    year            INT,
    page_number     INT NOT NULL,
    image_width     INT,
    image_height    INT,
    rotation        INT,
    ocr_text        TEXT,
    words           JSONB,
    avg_confidence  NUMERIC,
    ocr_engine      TEXT DEFAULT 'tesseract',
    ocr_config      TEXT,
    source_pdf      TEXT,
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (filing_id, page_number)
);

CREATE TABLE IF NOT EXISTS house_ptr_ocr_status (
    filing_id       TEXT PRIMARY KEY,
    year            INT,
    pdf_path        TEXT,
    page_count      INT,
    pages_ocr       INT,
    status          TEXT,
    error           TEXT,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_house_ptr_ocr_pages_year ON house_ptr_ocr_pages(year);
CREATE INDEX IF NOT EXISTS idx_house_ptr_ocr_status_status ON house_ptr_ocr_status(status);
"""

CONGRESS_TRADING_EXTENSIONS_DDL = """
ALTER TABLE congress_trading
    ADD COLUMN IF NOT EXISTS source_filing_id TEXT,
    ADD COLUMN IF NOT EXISTS source_page_number INT,
    ADD COLUMN IF NOT EXISTS source_row_hash TEXT,
    ADD COLUMN IF NOT EXISTS source_raw_text TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS idx_congress_trading_source_row_hash
    ON congress_trading(source_row_hash)
    WHERE source_row_hash IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_congress_trading_source_filing
    ON congress_trading(source_filing_id);
"""

AMOUNT_NUMBER_PATTERN = r"\d[\d,]*(?:\.\d{1,2})?"
AMOUNT_PATTERN = rf"\$?{AMOUNT_NUMBER_PATTERN}"

MODERN_PTR_ROW_RE = re.compile(
    r"^(?:(?P<owner>SP|JT|DC|DC/SP|SP/DC)\s+)?"
    r"(?P<asset>.+?)\s+"
    r"[_—–-]*\s*"
    r"(?P<txn_type>P|S|SS|E)\$?(?:\s+\(partial\))?\s+"
    r"(?P<txn_date>\d{1,2}/\d{1,2}/\d{4})\.?\s+"
    r"(?P<notice_date>\d{1,2}/\d{1,2}/\d{4})\.?\s+"
    r"[_—–-]*\s*"
    rf"(?P<amount>{AMOUNT_PATTERN}(?:\s*[-—–]\s*{AMOUNT_PATTERN}|\+?)?)"
    r"(?:\s+[\w|~]{1,6})?\s*$",
    re.IGNORECASE,
)

TICKER_ONLY_RE = re.compile(r"^\(([A-Z][A-Z0-9.\-]{0,9})\)(?:\s+\[[A-Z]{1,4}\])?$")
TICKER_PREFIX_RE = re.compile(r"^\(([A-Z][A-Z0-9.\-]{0,9})\)")
ASSET_TAG_RE = re.compile(r"\s+\[[A-Z]{1,4}[|\]]?\s*$")
ASSET_TYPE_RE = re.compile(r"\[([A-Z]{1,4})[|\]]")
DATE_PAIR_RE = re.compile(r"\d{1,2}/\d{1,2}/\d{4}\.?\s+\d{1,2}/\d{1,2}/\d{4}\.?")
DANGLING_AMOUNT_RE = re.compile(rf"({AMOUNT_PATTERN}\s*[-—–])(?:\s*[\w|~\[\]]+)*\s*$")
AMOUNT_VALUE_RE = re.compile(AMOUNT_PATTERN)
DOLLAR_AMOUNT_RE = re.compile(rf"\${AMOUNT_NUMBER_PATTERN}")


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


def parse_year_range(value: str) -> range:
    if ":" in value:
        start_text, end_text = value.split(":", 1)
        start_year = int(start_text)
        end_year = int(end_text)
    else:
        start_year = end_year = int(value)
    if start_year > end_year:
        raise argparse.ArgumentTypeError("start year must be <= end year")
    return range(start_year, end_year + 1)


def house_pdf_url(year: int, doc_id: str, filing_type: str) -> str:
    if filing_type == "P":
        return HOUSE_PTR_PDF_URL.format(year=year, doc_id=doc_id)
    return HOUSE_FINANCIAL_PDF_URL.format(year=year, doc_id=doc_id)


def fetch_house_zip(session: requests.Session, year: int) -> tuple[bytes | None, str | None, str]:
    for url in HOUSE_BULK_URLS:
        try:
            response = session.get(url.format(year=year), timeout=60)
        except requests.RequestException as exc:
            logger.warning("House FD %s request failed for %s: %s", year, url, exc)
            continue
        if response.status_code == 200 and zipfile.is_zipfile(io.BytesIO(response.content)):
            return response.content, response.url, "available"
        if response.status_code == 404:
            continue
        logger.warning(
            "House FD %s unexpected response from %s: status=%s bytes=%s zip=%s",
            year,
            url,
            response.status_code,
            len(response.content),
            zipfile.is_zipfile(io.BytesIO(response.content)),
        )
    return None, None, "unavailable"


def write_availability_audit(rows):
    audit_dir = BASE_DIR / "availability"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_path = audit_dir / f"house_fd_availability_{datetime.now(UTC):%Y%m%dT%H%M%SZ}.json"
    audit_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    logger.info("Wrote House FD availability audit: %s", audit_path)


def ingest_house_fd(conn, years=range(2000, 2027)):
    """
    The correct FD index URL. Each ZIP contains a CSV index + PDFs are linked separately.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (research/epstein_full)"})
    audit_rows = []
    for year in years:
        logger.info(f"House FD {year}")
        try:
            content, source_url, status = fetch_house_zip(session, year)
            if content is None:
                logger.warning("House FD %s unavailable from Clerk bulk ZIP endpoints", year)
                audit_rows.append(
                    {
                        "year": year,
                        "status": status,
                        "source_url": None,
                        "bytes": 0,
                        "rows_imported": 0,
                    }
                )
                continue

            raw_dir = BASE_DIR / "house" / str(year)
            raw_dir.mkdir(parents=True, exist_ok=True)
            raw_zip = raw_dir / f"{year}FD.zip"
            raw_zip.write_bytes(content)

            imported = 0
            with zipfile.ZipFile(io.BytesIO(content)) as z:
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
                                        house_pdf_url(
                                            year, doc_id, row.get("FilingType", "").strip()
                                        )
                                    ),
                                }
                            )
                            if len(rows) >= 500:
                                batch_insert(conn, "house_financial_disclosures", rows, "filing_id")
                                imported += len(rows)
                                rows = []
                        if rows:
                            batch_insert(conn, "house_financial_disclosures", rows, "filing_id")
                            imported += len(rows)
                        logger.info(f"House FD {year} done from {txt_name}")
            audit_rows.append(
                {
                    "year": year,
                    "status": "available",
                    "source_url": source_url,
                    "bytes": len(content),
                    "raw_zip": str(raw_zip),
                    "rows_imported": imported,
                }
            )
        except Exception as e:
            logger.error(f"Failed House FD {year}: {e}")
            audit_rows.append(
                {
                    "year": year,
                    "status": "error",
                    "source_url": source_url if "source_url" in locals() else None,
                    "bytes": len(content) if "content" in locals() and content else 0,
                    "rows_imported": 0,
                    "error": str(e),
                }
            )
    write_availability_audit(audit_rows)


def fix_house_pdf_urls(conn) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE house_financial_disclosures
            SET pdf_url = CASE
                WHEN filing_type = 'P'
                    THEN 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/'
                        || year || '/' || filing_id || '.pdf'
                ELSE 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/'
                        || year || '/' || filing_id || '.pdf'
            END,
            updated_at = NOW()
            WHERE pdf_url IS NULL
               OR (filing_type = 'P' AND pdf_url NOT LIKE '%/ptr-pdfs/%')
               OR (filing_type <> 'P' AND pdf_url NOT LIKE '%/financial-pdfs/%')
            """
        )
        updated = cur.rowcount
    conn.commit()
    logger.info("Corrected %s House disclosure PDF URLs", updated)
    return updated


def is_pdf_bytes(content: bytes) -> bool:
    return content.startswith(b"%PDF-")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def download_one_pdf(record: dict, output_root: Path) -> dict:
    year = int(record["year"])
    filing_id = record["filing_id"]
    out_dir = output_root / str(year)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{filing_id}.pdf"

    if out_path.exists() and out_path.stat().st_size > 0:
        content = out_path.read_bytes()
        return {
            **record,
            "status": "exists_valid" if is_pdf_bytes(content) else "exists_invalid",
            "path": str(out_path),
            "bytes": len(content),
            "sha256": sha256_bytes(content) if is_pdf_bytes(content) else None,
        }

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (research/epstein_full)"})
    try:
        response = session.get(record["pdf_url"], timeout=60)
    except requests.RequestException as exc:
        return {**record, "status": "request_error", "error": str(exc)}

    if response.status_code != 200:
        return {
            **record,
            "status": "http_error",
            "http_status": response.status_code,
            "bytes": len(response.content),
        }

    if not is_pdf_bytes(response.content):
        return {
            **record,
            "status": "invalid_pdf",
            "http_status": response.status_code,
            "bytes": len(response.content),
        }

    out_path.write_bytes(response.content)
    return {
        **record,
        "status": "downloaded",
        "path": str(out_path),
        "bytes": len(response.content),
        "sha256": sha256_bytes(response.content),
    }


def iter_house_ptr_records(conn, years: range, limit: int | None = None):
    with conn.cursor() as cur:
        sql = """
            SELECT filing_id, year, first_name, last_name, state_dst, pdf_url
            FROM house_financial_disclosures
            WHERE filing_type = 'P'
              AND year BETWEEN %s AND %s
            ORDER BY year, filing_id
        """
        params = [years.start, years.stop - 1]
        if limit:
            sql += " LIMIT %s"
            params.append(limit)
        cur.execute(sql, params)
        cols = [desc[0] for desc in cur.description]
        for row in cur.fetchall():
            yield dict(zip(cols, row))


def download_house_ptr_pdfs(conn, years: range, limit: int | None = None, workers: int = 8):
    fix_house_pdf_urls(conn)
    records = list(iter_house_ptr_records(conn, years, limit))
    output_root = BASE_DIR / "house_ptr"
    manifest_dir = BASE_DIR / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"house_ptr_download_{datetime.now(UTC):%Y%m%dT%H%M%SZ}.jsonl"

    logger.info(
        "Downloading %s House PTR PDFs for years %s-%s with %s workers",
        len(records),
        years.start,
        years.stop - 1,
        workers,
    )
    counts = {}
    with manifest_path.open("w", encoding="utf-8") as manifest:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(download_one_pdf, record, output_root) for record in records]
            for index, future in enumerate(as_completed(futures), start=1):
                result = future.result()
                counts[result["status"]] = counts.get(result["status"], 0) + 1
                manifest.write(json.dumps(result, sort_keys=True) + "\n")
                if index % 250 == 0 or index == len(records):
                    logger.info("House PTR PDF progress: %s/%s %s", index, len(records), counts)

    logger.info("House PTR PDF manifest: %s", manifest_path)
    logger.info("House PTR PDF summary: %s", counts)
    return counts


def ensure_house_ptr_ocr_tables(conn):
    with conn.cursor() as cur:
        cur.execute(HOUSE_PTR_OCR_DDL)
    conn.commit()


def ensure_congress_trading_extensions(conn):
    with conn.cursor() as cur:
        cur.execute(CONGRESS_TRADING_EXTENSIONS_DDL)
    conn.commit()


def run_tesseract(image_path: Path, *args: str) -> str:
    cmd = ["tesseract", str(image_path), "stdout", *args]
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    output = completed.stdout if completed.stdout else completed.stderr
    if completed.returncode != 0 and "--psm 0" not in " ".join(args):
        raise RuntimeError(output.strip())
    return output


def detect_tesseract_rotation(image_path: Path) -> int:
    output = run_tesseract(image_path, "--psm", "0")
    rotate = 0
    confidence = 0.0
    for line in output.splitlines():
        if line.startswith("Rotate:"):
            rotate = int(line.split(":", 1)[1].strip())
        elif line.startswith("Orientation confidence:"):
            try:
                confidence = float(line.split(":", 1)[1].strip())
            except ValueError:
                confidence = 0.0
    if confidence < 1.0:
        return 0
    return (360 - rotate) % 360


def parse_tesseract_tsv(tsv_text: str) -> tuple[str, list[dict], float | None]:
    lines = [line for line in tsv_text.splitlines() if line.strip()]
    if not lines:
        return "", [], None
    header = lines[0].split("\t")
    words = []
    text_lines = {}
    confidences = []
    for line in lines[1:]:
        values = line.split("\t")
        if len(values) < len(header):
            values.extend([""] * (len(header) - len(values)))
        row = dict(zip(header, values))
        text = row.get("text", "").strip()
        if not text:
            continue
        try:
            conf = float(row.get("conf", "-1"))
        except ValueError:
            conf = -1.0
        word = {
            "text": text,
            "conf": conf,
            "left": int(float(row.get("left") or 0)),
            "top": int(float(row.get("top") or 0)),
            "width": int(float(row.get("width") or 0)),
            "height": int(float(row.get("height") or 0)),
            "block_num": int(float(row.get("block_num") or 0)),
            "par_num": int(float(row.get("par_num") or 0)),
            "line_num": int(float(row.get("line_num") or 0)),
            "word_num": int(float(row.get("word_num") or 0)),
        }
        words.append(word)
        if conf >= 0:
            confidences.append(conf)
        key = (word["block_num"], word["par_num"], word["line_num"])
        text_lines.setdefault(key, []).append(word)

    rendered_lines = []
    for key in sorted(text_lines):
        line_words = sorted(text_lines[key], key=lambda item: item["left"])
        rendered_lines.append(" ".join(item["text"] for item in line_words))
    avg_confidence = sum(confidences) / len(confidences) if confidences else None
    return "\n".join(rendered_lines), words, avg_confidence


def ocr_pdf_pages(pdf_path: Path, dpi: int = 200, psm: int = 6) -> list[dict]:
    pages = []
    with tempfile.TemporaryDirectory(prefix="house_ptr_ocr_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        doc = fitz.open(pdf_path)
        for page_index, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
            image_path = tmp_path / f"page_{page_index}.png"
            pix.save(image_path)

            rotation = detect_tesseract_rotation(image_path)
            if rotation:
                from PIL import Image

                image = Image.open(image_path)
                image = image.rotate(rotation, expand=True)
                image.save(image_path)

            tsv = run_tesseract(image_path, "--psm", str(psm), "tsv")
            text, words, avg_confidence = parse_tesseract_tsv(tsv)
            pages.append(
                {
                    "page_number": page_index,
                    "image_width": pix.width,
                    "image_height": pix.height,
                    "rotation": rotation,
                    "ocr_text": text,
                    "words": words,
                    "avg_confidence": avg_confidence,
                    "ocr_config": f"dpi={dpi};psm={psm}",
                }
            )
    return pages


def iter_house_ptr_pdf_files(conn, years: range, limit: int | None = None, redo: bool = False):
    sql = """
        SELECT h.filing_id, h.year,
               %s || '/' || h.year || '/' || h.filing_id || '.pdf' AS pdf_path
        FROM house_financial_disclosures h
        LEFT JOIN house_ptr_ocr_status s ON s.filing_id = h.filing_id
        WHERE h.filing_type = 'P'
          AND h.year BETWEEN %s AND %s
          AND (%s OR s.status IS DISTINCT FROM 'complete')
        ORDER BY h.year, h.filing_id
    """
    params = [str(BASE_DIR / "house_ptr"), years.start, years.stop - 1, redo]
    if limit:
        sql += " LIMIT %s"
        params.append(limit)
    with conn.cursor() as cur:
        cur.execute(sql, params)
        cols = [desc[0] for desc in cur.description]
        for row in cur.fetchall():
            yield dict(zip(cols, row))


def insert_house_ptr_ocr_result(
    conn, record: dict, pages: list[dict], status: str, error: str | None = None
):
    from psycopg2.extras import Json, execute_values

    if pages:
        rows = [
            (
                record["filing_id"],
                record["year"],
                page["page_number"],
                page["image_width"],
                page["image_height"],
                page["rotation"],
                page["ocr_text"],
                Json(page["words"]),
                page["avg_confidence"],
                "tesseract",
                page["ocr_config"],
                record["pdf_path"],
            )
            for page in pages
        ]
        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO house_ptr_ocr_pages
                (filing_id, year, page_number, image_width, image_height, rotation,
                 ocr_text, words, avg_confidence, ocr_engine, ocr_config, source_pdf)
                VALUES %s
                ON CONFLICT (filing_id, page_number) DO UPDATE SET
                    year = EXCLUDED.year,
                    image_width = EXCLUDED.image_width,
                    image_height = EXCLUDED.image_height,
                    rotation = EXCLUDED.rotation,
                    ocr_text = EXCLUDED.ocr_text,
                    words = EXCLUDED.words,
                    avg_confidence = EXCLUDED.avg_confidence,
                    ocr_engine = EXCLUDED.ocr_engine,
                    ocr_config = EXCLUDED.ocr_config,
                    source_pdf = EXCLUDED.source_pdf,
                    updated_at = NOW()
                """,
                rows,
            )

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO house_ptr_ocr_status
            (filing_id, year, pdf_path, page_count, pages_ocr, status, error)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (filing_id) DO UPDATE SET
                year = EXCLUDED.year,
                pdf_path = EXCLUDED.pdf_path,
                page_count = EXCLUDED.page_count,
                pages_ocr = EXCLUDED.pages_ocr,
                status = EXCLUDED.status,
                error = EXCLUDED.error,
                updated_at = NOW()
            """,
            (
                record["filing_id"],
                record["year"],
                record["pdf_path"],
                len(pages),
                len(pages),
                status,
                error,
            ),
        )
    conn.commit()


def ocr_one_house_ptr_pdf(
    record: dict, dpi: int, psm: int
) -> tuple[dict, list[dict], str, str | None]:
    pdf_path = Path(record["pdf_path"])
    try:
        if not pdf_path.exists():
            raise FileNotFoundError(str(pdf_path))
        pages = ocr_pdf_pages(pdf_path, dpi=dpi, psm=psm)
        return record, pages, "complete", None
    except Exception as exc:
        return record, [], "error", str(exc)


def ocr_house_ptr_pdfs(
    conn,
    years: range,
    limit: int | None = None,
    dpi: int = 200,
    psm: int = 6,
    redo: bool = False,
    workers: int = 4,
):
    ensure_house_ptr_ocr_tables(conn)
    records = list(iter_house_ptr_pdf_files(conn, years, limit, redo))
    logger.info(
        "OCRing %s House PTR PDFs for years %s-%s with %s workers",
        len(records),
        years.start,
        years.stop - 1,
        workers,
    )
    counts = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(ocr_one_house_ptr_pdf, record, dpi, psm) for record in records]
        for index, future in enumerate(as_completed(futures), start=1):
            record, pages, status, error = future.result()
            insert_house_ptr_ocr_result(conn, record, pages, status, error)
            counts[status] = counts.get(status, 0) + 1
            if status == "error":
                logger.error("House PTR OCR failed for %s: %s", record["filing_id"], error)
            if index % 25 == 0 or index == len(records):
                logger.info("House PTR OCR progress: %s/%s %s", index, len(records), counts)
    return counts


def parse_house_amount(amount_text: str) -> tuple[float | None, float | None, str]:
    normalized = re.sub(r"\s+", " ", amount_text.replace("$", "")).strip()
    normalized = normalized.replace("—", "-").replace("–", "-")
    decimal_hyphen_match = re.fullmatch(r"(\d{1,3})-(\d{2})", normalized)
    if decimal_hyphen_match:
        value = float(f"{decimal_hyphen_match.group(1)}.{decimal_hyphen_match.group(2)}")
        return value, value, amount_text.strip()
    numbers = [
        float(value.replace(",", "")) for value in re.findall(r"\d[\d,]*(?:\.\d{1,2})?", normalized)
    ]
    if not numbers:
        return None, None, amount_text.strip()
    if len(numbers) == 1:
        if normalized.endswith("+"):
            return float(numbers[0]), None, amount_text.strip()
        return float(numbers[0]), float(numbers[0]), amount_text.strip()
    return float(numbers[0]), float(numbers[1]), amount_text.strip()


def parse_house_date(value: str):
    from datetime import datetime as dt

    return dt.strptime(value, "%m/%d/%Y").date()


def normalize_house_notice_date(transaction_date, notice_date):
    if notice_date >= transaction_date and (notice_date - transaction_date).days <= 90:
        return notice_date
    if (transaction_date - notice_date).days <= 90:
        return notice_date

    for year in (transaction_date.year, transaction_date.year + 1):
        try:
            candidate = notice_date.replace(year=year)
        except ValueError:
            continue
        if transaction_date <= candidate and (candidate - transaction_date).days <= 90:
            return candidate
    return notice_date


def extract_ticker(asset_name: str) -> str | None:
    matches = re.findall(r"\(([A-Z][A-Z0-9.\-]{0,9})\)", asset_name)
    return matches[-1] if matches else None


def strip_house_asset_tags(asset_name: str) -> str:
    return ASSET_TAG_RE.sub("", asset_name).strip()


def extract_house_asset_type(value: str) -> str | None:
    matches = ASSET_TYPE_RE.findall(value)
    return matches[-1] if matches else None


def normalize_transaction_type(value: str) -> str:
    value = value.upper()
    if value.startswith("P"):
        return "Purchase"
    if value.startswith("S"):
        return "Sale"
    if value.startswith("E"):
        return "Exchange"
    return value


def iter_modern_house_ptr_transactions(conn, years: range, limit: int | None = None):
    sql = """
        SELECT p.filing_id, p.year, p.page_number, p.ocr_text,
               h.first_name, h.last_name, h.state_dst, h.pdf_url
        FROM house_ptr_ocr_pages p
        JOIN house_financial_disclosures h ON h.filing_id = p.filing_id
        WHERE p.year BETWEEN %s AND %s
          AND p.ocr_text ILIKE '%%TRANSACTIONS%%'
        ORDER BY p.year, p.filing_id, p.page_number
    """
    params = [years.start, years.stop - 1]
    if limit:
        sql += " LIMIT %s"
        params.append(limit)
    with conn.cursor() as cur:
        cur.execute(sql, params)
        cols = [desc[0] for desc in cur.description]
        for page in (dict(zip(cols, row)) for row in cur.fetchall()):
            clean_lines = [
                re.sub(r"\s+", " ", line).strip() for line in page["ocr_text"].splitlines()
            ]
            for index, clean_line in enumerate(clean_lines):
                if not clean_line or "FILING STATUS" in clean_line.upper():
                    continue
                candidate_line = clean_line
                asset_continuation = ""
                if (
                    index + 1 < len(clean_lines)
                    and DATE_PAIR_RE.search(clean_line)
                    and DANGLING_AMOUNT_RE.search(clean_line)
                    and AMOUNT_VALUE_RE.search(clean_lines[index + 1])
                ):
                    continuation_amount_match = DOLLAR_AMOUNT_RE.search(
                        clean_lines[index + 1]
                    ) or AMOUNT_VALUE_RE.search(clean_lines[index + 1])
                    continuation_amount = continuation_amount_match.group(0)
                    asset_continuation = clean_lines[index + 1][
                        : continuation_amount_match.start()
                    ].strip()
                    candidate_line = (
                        f"{DANGLING_AMOUNT_RE.sub(r'\1', clean_line)} {continuation_amount}"
                    )
                candidate_line = re.sub(r"=\s*(?=\$?\d)", "", candidate_line)
                match = MODERN_PTR_ROW_RE.match(candidate_line)
                if not match:
                    continue
                groups = match.groupdict()
                raw_asset_name = groups["asset"].strip()
                if asset_continuation and "FILING STATUS" not in asset_continuation.upper():
                    raw_asset_name = f"{raw_asset_name} {asset_continuation}"
                asset_type = extract_house_asset_type(raw_asset_name)
                asset_name = strip_house_asset_tags(raw_asset_name)
                # Avoid parsing header or OCR noise as an asset row.
                if len(asset_name) < 3 or asset_name.upper().startswith(
                    ("ID OWNER", "OWNER ASSET", "SUBHOLDING")
                ):
                    continue
                if index + 1 < len(clean_lines) and TICKER_ONLY_RE.match(clean_lines[index + 1]):
                    asset_name = f"{asset_name} {clean_lines[index + 1]}"
                    asset_type = asset_type or extract_house_asset_type(clean_lines[index + 1])
                elif index + 1 < len(clean_lines) and TICKER_PREFIX_RE.match(
                    clean_lines[index + 1]
                ):
                    asset_name = (
                        f"{asset_name} ({TICKER_PREFIX_RE.match(clean_lines[index + 1]).group(1)})"
                    )
                    asset_type = asset_type or extract_house_asset_type(clean_lines[index + 1])
                asset_name = strip_house_asset_tags(asset_name)
                amount_low, amount_high, normalized_amount = parse_house_amount(groups["amount"])
                if amount_low is None:
                    continue
                transaction_date = parse_house_date(groups["txn_date"])
                notice_date = normalize_house_notice_date(
                    transaction_date, parse_house_date(groups["notice_date"])
                )
                row_hash_input = "|".join(
                    [
                        page["filing_id"],
                        str(page["page_number"]),
                        asset_name,
                        groups["txn_type"].upper(),
                        groups["txn_date"],
                        groups["notice_date"],
                        normalized_amount,
                    ]
                )
                yield {
                    "politician_name": f"{page['first_name']} {page['last_name']}".strip(),
                    "politician_state": (page["state_dst"] or "")[:2] or None,
                    "politician_district": (page["state_dst"] or "")[2:] or None,
                    "transaction_date": transaction_date,
                    "ticker": extract_ticker(asset_name),
                    "asset_name": asset_name,
                    "asset_type": asset_type,
                    "transaction_type": normalize_transaction_type(groups["txn_type"]),
                    "amount_low": amount_low,
                    "amount_high": amount_high,
                    "amount_text": normalized_amount,
                    "description": f"Owner: {groups.get('owner')}" if groups.get("owner") else None,
                    "data_source": "House PTR OCR",
                    "filing_date": notice_date,
                    "disclosure_url": page["pdf_url"],
                    "source_filing_id": page["filing_id"],
                    "source_page_number": page["page_number"],
                    "source_row_hash": hashlib.sha256(row_hash_input.encode("utf-8")).hexdigest(),
                    "source_raw_text": candidate_line,
                }


def load_house_ptr_transactions(conn, years: range, limit: int | None = None) -> dict:
    from psycopg2.extras import execute_values

    ensure_congress_trading_extensions(conn)
    rows_by_hash = {}
    for row in iter_modern_house_ptr_transactions(conn, years, limit):
        rows_by_hash.setdefault(row["source_row_hash"], row)
    rows = list(rows_by_hash.values())
    if not rows:
        logger.info(
            "No modern House PTR transaction rows matched for %s-%s", years.start, years.stop - 1
        )
        return {"matched": 0, "inserted_or_updated": 0}

    cols = list(rows[0].keys())
    values = [[row[col] for col in cols] for row in rows]
    insert_cols = ", ".join(cols)
    update_cols = ", ".join(
        f"{col}=EXCLUDED.{col}" for col in cols if col not in {"source_row_hash"}
    )
    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM congress_trading t
            USING house_financial_disclosures h
            WHERE t.source_filing_id = h.filing_id
              AND t.data_source = 'House PTR OCR'
              AND h.year BETWEEN %s AND %s
            """,
            (years.start, years.stop - 1),
        )
        execute_values(
            cur,
            f"""
            INSERT INTO congress_trading ({insert_cols})
            VALUES %s
            ON CONFLICT (source_row_hash) WHERE source_row_hash IS NOT NULL
            DO UPDATE SET {update_cols}
            """,
            values,
        )
        affected = cur.rowcount
    conn.commit()
    logger.info("Loaded %s matched House PTR transaction rows into congress_trading", len(rows))
    return {"matched": len(rows), "inserted_or_updated": affected}


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


def build_parser():
    parser = argparse.ArgumentParser(
        description="Import House/Senate financial disclosure metadata"
    )
    parser.add_argument(
        "--house-years",
        type=parse_year_range,
        default=parse_year_range("2000:2026"),
        help="House year or inclusive range, e.g. 2000:2026",
    )
    parser.add_argument(
        "--senate-years",
        type=parse_year_range,
        default=parse_year_range("2012:2026"),
        help="Senate year or inclusive range, e.g. 2012:2026",
    )
    parser.add_argument("--skip-house", action="store_true", help="Skip House import")
    parser.add_argument("--skip-senate", action="store_true", help="Skip Senate import")
    parser.add_argument(
        "--fix-house-pdf-urls", action="store_true", help="Correct House PDF URL paths"
    )
    parser.add_argument(
        "--download-house-ptrs", action="store_true", help="Download House PTR PDFs"
    )
    parser.add_argument(
        "--ptr-years",
        type=parse_year_range,
        default=parse_year_range("2013:2026"),
        help="House PTR year or inclusive range, e.g. 2013:2026",
    )
    parser.add_argument("--ptr-limit", type=int, help="Limit House PTR downloads for smoke tests")
    parser.add_argument(
        "--ptr-workers", type=int, default=8, help="Concurrent House PTR download workers"
    )
    parser.add_argument(
        "--ocr-house-ptrs", action="store_true", help="OCR downloaded House PTR PDFs"
    )
    parser.add_argument(
        "--ocr-years",
        type=parse_year_range,
        default=parse_year_range("2013:2026"),
        help="House PTR OCR year or inclusive range, e.g. 2013:2026",
    )
    parser.add_argument("--ocr-limit", type=int, help="Limit House PTR OCR for smoke tests")
    parser.add_argument("--ocr-dpi", type=int, default=200, help="Render DPI for House PTR OCR")
    parser.add_argument("--ocr-psm", type=int, default=6, help="Tesseract page segmentation mode")
    parser.add_argument("--ocr-redo", action="store_true", help="Redo complete House PTR OCR rows")
    parser.add_argument(
        "--ocr-workers", type=int, default=4, help="Concurrent House PTR OCR workers"
    )
    parser.add_argument(
        "--load-house-ptr-transactions",
        action="store_true",
        help="Parse OCRed modern House PTR rows into congress_trading",
    )
    parser.add_argument(
        "--transaction-years",
        type=parse_year_range,
        default=parse_year_range("2013:2026"),
        help="House PTR transaction parse year or inclusive range",
    )
    parser.add_argument("--transaction-page-limit", type=int, help="Limit OCR pages parsed")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()

    logger.info("=" * 80)
    logger.info("HOUSE/SENATE FINANCIAL DISCLOSURES INGESTION")
    logger.info("=" * 80)

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(DDL)
        cur.execute(SENATE_DDL)
    conn.commit()

    if args.fix_house_pdf_urls:
        fix_house_pdf_urls(conn)

    if not args.skip_house:
        try:
            ingest_house_fd(conn, args.house_years)
        except Exception as e:
            logger.error(f"House FD ingestion failed: {e}")
            conn.rollback()

    if not args.skip_senate:
        try:
            ingest_senate_fd(conn, args.senate_years)
        except Exception as e:
            logger.error(f"Senate FD ingestion failed: {e}")
            conn.rollback()

    if args.download_house_ptrs:
        download_house_ptr_pdfs(conn, args.ptr_years, args.ptr_limit, args.ptr_workers)

    if args.ocr_house_ptrs:
        ocr_house_ptr_pdfs(
            conn,
            args.ocr_years,
            args.ocr_limit,
            dpi=args.ocr_dpi,
            psm=args.ocr_psm,
            redo=args.ocr_redo,
            workers=args.ocr_workers,
        )

    if args.load_house_ptr_transactions:
        load_house_ptr_transactions(conn, args.transaction_years, args.transaction_page_limit)

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
