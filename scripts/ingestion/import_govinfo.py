#!/usr/bin/env python3
"""
Import GovInfo.gov data to PostgreSQL
Source: api.govinfo.gov
Tables: govinfo_packages, federal_register_entries, court_opinions
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import psycopg2

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/govinfo")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_govinfo_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg2.connect(
        host='localhost', database='epstein',
        user='cbwinslow', password='123qweasd'
    )


def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # GovInfo packages table (main)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS govinfo_packages (
            id SERIAL PRIMARY KEY,
            package_id TEXT UNIQUE,
            title TEXT,
            collection_code TEXT,
            collection_name TEXT,
            date_issued DATE,
            congress INT,
            session INT,
            chamber TEXT,
            bill_number TEXT,
            bill_type TEXT,
            su_doc_class_number TEXT,
            publisher TEXT,
            is_appropriation BOOLEAN DEFAULT FALSE,
            is_private BOOLEAN DEFAULT FALSE,
            download_pdf_url TEXT,
            download_txt_url TEXT,
            download_xml_url TEXT,
            detail_view_txt_url TEXT,
            date_inreceived DATE,
            pages INT,
            current_chamber TEXT,
            current_congress INT,
            bill_version TEXT,
            effective_date DATE,
            entry_type TEXT,
            office_code TEXT,
            office_name TEXT,
            is_law BOOLEAN DEFAULT FALSE,
            law_number TEXT,
            migrated_doc_id TEXT,
            primary_located_doc_id TEXT,
            last_modified DATE,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Federal Register specific table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS federal_register_entries (
            id SERIAL PRIMARY KEY,
            package_id TEXT UNIQUE,
            fr_doc_number TEXT,
            citation TEXT,
            title TEXT,
            abstract TEXT,
            dates TEXT,
            agencies TEXT,
            action TEXT,
            significant BOOLEAN DEFAULT FALSE,
            rindicators TEXT,
            pdf_url TEXT,
            html_url TEXT,
            mods_url TEXT,
            premis_url TEXT,
            date_published DATE,
            volume INT,
            page_start INT,
            page_end INT,
            number_of_pages INT,
            docket_ids TEXT,
            regulations_dot_gov_ids TEXT,
            correction_of_fr_doc_number TEXT,
            is_correction BOOLEAN DEFAULT FALSE,
            su_doc_class_number TEXT,
            original_content_type TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Court opinions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS court_opinions (
            id SERIAL PRIMARY KEY,
            package_id TEXT UNIQUE,
            court_name TEXT,
            court_type TEXT,
            case_name TEXT,
            case_number TEXT,
            date_decided DATE,
            date_filed DATE,
            judges TEXT,
            attorneys TEXT,
            parties TEXT,
            nature_of_suit TEXT,
            cause TEXT,
            jurisdiction TEXT,
            jurisdiction_basis TEXT,
            case_source TEXT,
            case_source_area TEXT,
            case_source_state TEXT,
            case_source_subdivisions TEXT,
            pdf_url TEXT,
            html_url TEXT,
            summary TEXT,
            outcome TEXT,
            disposition TEXT,
            raw_data JSONB,
            imported_at TIMESTAMPTZ DEFAULT NOW(),
            source_file TEXT
        )
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_gi_collection ON govinfo_packages (collection_code);
        CREATE INDEX IF NOT EXISTS idx_gi_date ON govinfo_packages (date_issued);
        CREATE INDEX IF NOT EXISTS idx_gi_congress ON govinfo_packages (congress);
        CREATE INDEX IF NOT EXISTS idx_gi_bill ON govinfo_packages (bill_number);
        
        CREATE INDEX IF NOT EXISTS idx_fr_date ON federal_register_entries (date_published);
        CREATE INDEX IF NOT EXISTS idx_fr_agencies ON federal_register_entries (agencies);
        CREATE INDEX IF NOT EXISTS idx_fr_doc ON federal_register_entries (fr_doc_number);
        
        CREATE INDEX IF NOT EXISTS idx_co_court ON court_opinions (court_name);
        CREATE INDEX IF NOT EXISTS idx_co_date ON court_opinions (date_decided);
        CREATE INDEX IF NOT EXISTS idx_co_case ON court_opinions (case_number);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables and indexes created/verified")


def payload_packages(data) -> List[Dict]:
    """Return packages from either a wrapped API payload or a raw list file."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get('packages', [])
    return []


def infer_collection(filepath: Path, data: Dict, pkg: Dict) -> tuple[str, str]:
    """Infer collection code/name from package, wrapper, or directory name."""
    collection_code = (
        pkg.get('collectionCode')
        or pkg.get('docClass')
        or data.get('collection')
        or filepath.parent.parent.name.upper()
    )
    collection_names = {
        'FR': 'Federal Register',
        'BILLS': 'Bills',
        'USCOURTS': 'Court Opinions',
        'CRPT': 'Committee Reports',
        'USCODE': 'United States Code',
    }
    collection_name = pkg.get('collectionName') or collection_names.get(collection_code, collection_code)
    return collection_code, collection_name


def parse_packages_file(filepath: Path) -> List[Dict]:
    records = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for pkg in payload_packages(data):
            # Parse lastModified date
            last_mod = pkg.get('lastModified', '')
            if last_mod:
                last_mod = last_mod[:10]  # Get just the date part
            collection_code, collection_name = infer_collection(filepath, data if isinstance(data, dict) else {}, pkg)
            
            record = {
                'package_id': pkg.get('packageId', ''),
                'title': pkg.get('title', ''),
                'collection_code': collection_code,
                'collection_name': collection_name,
                'date_issued': pkg.get('dateIssued') or None,
                'congress': pkg.get('congress', 0) or 0,
                'session': pkg.get('session', 0) or 0,
                'chamber': pkg.get('chamber', ''),
                'bill_number': pkg.get('billNumber', ''),
                'bill_type': pkg.get('billType', ''),
                'su_doc_class_number': pkg.get('suDocClassNumber', ''),
                'publisher': pkg.get('publisher', ''),
                'is_appropriation': pkg.get('isAppropriation', False) or False,
                'is_private': pkg.get('isPrivate', False) or False,
                'download_pdf_url': pkg.get('download', {}).get('pdfLink', '') if pkg.get('download') else '',
                'download_txt_url': pkg.get('download', {}).get('txtLink', '') if pkg.get('download') else '',
                'download_xml_url': pkg.get('download', {}).get('xmlLink', '') if pkg.get('download') else '',
                'detail_view_txt_url': pkg.get('detailView', ''),
                'date_inreceived': pkg.get('dateInReceived') or None,
                'pages': pkg.get('pages', 0) or 0,
                'current_chamber': pkg.get('currentChamber', ''),
                'current_congress': pkg.get('currentCongress', 0) or 0,
                'bill_version': pkg.get('billVersion', ''),
                'effective_date': pkg.get('effectiveDate') or None,
                'entry_type': pkg.get('entryType', ''),
                'office_code': pkg.get('officeCode', ''),
                'office_name': pkg.get('officeName', ''),
                'is_law': pkg.get('isLaw', False) or False,
                'law_number': pkg.get('lawNumber', ''),
                'migrated_doc_id': pkg.get('migratedDocId', ''),
                'primary_located_doc_id': pkg.get('primaryLocatedDocId', ''),
                'last_modified': last_mod or None,
                'raw_data': json.dumps(pkg),
                'source_file': str(filepath)
            }
            records.append(record)
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def import_packages(records: List[Dict]) -> int:
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    inserted = 0
    for r in records:
        try:
            cur.execute("""
                INSERT INTO govinfo_packages (
                    package_id, title, collection_code, collection_name, date_issued,
                    congress, session, chamber, bill_number, bill_type, su_doc_class_number,
                    publisher, is_appropriation, is_private, download_pdf_url,
                    download_txt_url, download_xml_url, detail_view_txt_url, date_inreceived,
                    pages, current_chamber, current_congress, bill_version, effective_date,
                    entry_type, office_code, office_name, is_law, law_number,
                    migrated_doc_id, primary_located_doc_id, last_modified, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (package_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    collection_code = EXCLUDED.collection_code,
                    collection_name = EXCLUDED.collection_name,
                    date_issued = EXCLUDED.date_issued,
                    congress = EXCLUDED.congress,
                    raw_data = EXCLUDED.raw_data,
                    imported_at = NOW()
            """, (
                r['package_id'], r['title'], r['collection_code'], r['collection_name'],
                r['date_issued'], r['congress'], r['session'], r['chamber'], r['bill_number'],
                r['bill_type'], r['su_doc_class_number'], r['publisher'], r['is_appropriation'],
                r['is_private'], r['download_pdf_url'], r['download_txt_url'],
                r['download_xml_url'], r['detail_view_txt_url'], r['date_inreceived'],
                r['pages'], r['current_chamber'], r['current_congress'], r['bill_version'],
                r['effective_date'], r['entry_type'], r['office_code'], r['office_name'],
                r['is_law'], r['law_number'], r['migrated_doc_id'], r['primary_located_doc_id'],
                r['last_modified'], r['raw_data'], r['source_file']
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_federal_register_entries(records: List[Dict]) -> int:
    """Populate federal_register_entries from GovInfo package summaries."""
    fr_records = [r for r in records if r.get('collection_code') == 'FR']
    if not fr_records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0

    for r in fr_records:
        try:
            raw = json.loads(r['raw_data'])
            cur.execute("""
                INSERT INTO federal_register_entries (
                    package_id, fr_doc_number, citation, title, abstract, dates,
                    agencies, action, significant, rindicators, pdf_url, html_url,
                    mods_url, premis_url, date_published, volume, page_start, page_end,
                    number_of_pages, docket_ids, regulations_dot_gov_ids,
                    correction_of_fr_doc_number, is_correction, su_doc_class_number,
                    original_content_type, raw_data, source_file
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (package_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    date_published = EXCLUDED.date_published,
                    html_url = EXCLUDED.html_url,
                    raw_data = EXCLUDED.raw_data,
                    imported_at = NOW()
            """, (
                r['package_id'],
                raw.get('frDocNumber') or raw.get('packageId'),
                raw.get('citation') or '',
                r['title'],
                raw.get('abstract') or '',
                raw.get('dates') or '',
                ', '.join(raw.get('agencies', [])) if isinstance(raw.get('agencies'), list) else (raw.get('agencies') or ''),
                raw.get('action') or '',
                bool(raw.get('significant', False)),
                ', '.join(raw.get('rindicators', [])) if isinstance(raw.get('rindicators'), list) else (raw.get('rindicators') or ''),
                r['download_pdf_url'],
                raw.get('packageLink') or r['detail_view_txt_url'],
                raw.get('modsLink') or '',
                raw.get('premisLink') or '',
                r['date_issued'],
                raw.get('volume'),
                raw.get('pageStart'),
                raw.get('pageEnd'),
                raw.get('pages'),
                ', '.join(raw.get('docketIds', [])) if isinstance(raw.get('docketIds'), list) else (raw.get('docketIds') or ''),
                ', '.join(raw.get('regulationsDotGovIds', [])) if isinstance(raw.get('regulationsDotGovIds'), list) else (raw.get('regulationsDotGovIds') or ''),
                raw.get('correctionOfFrDocNumber') or '',
                bool(raw.get('isCorrection', False)),
                r['su_doc_class_number'],
                raw.get('originalContentType') or '',
                r['raw_data'],
                r['source_file'],
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Federal Register insert failed: {e}")

    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_court_opinions(records: List[Dict]) -> int:
    """Populate court_opinions from GovInfo package summaries."""
    court_records = [r for r in records if r.get('collection_code') == 'USCOURTS']
    if not court_records:
        return 0

    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0

    for r in court_records:
        try:
            raw = json.loads(r['raw_data'])
            package_id = r['package_id']
            package_tail = package_id.replace('USCOURTS-', '', 1) if package_id.startswith('USCOURTS-') else package_id
            case_number = raw.get('caseNumber') or package_tail
            court_name = raw.get('courtName') or package_tail.split('-', 1)[0]

            cur.execute("""
                INSERT INTO court_opinions (
                    package_id, court_name, court_type, case_name, case_number,
                    date_decided, date_filed, judges, attorneys, parties, nature_of_suit,
                    cause, jurisdiction, jurisdiction_basis, case_source, case_source_area,
                    case_source_state, case_source_subdivisions, pdf_url, html_url,
                    summary, outcome, disposition, raw_data, source_file
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (package_id) DO UPDATE SET
                    case_name = EXCLUDED.case_name,
                    date_filed = EXCLUDED.date_filed,
                    html_url = EXCLUDED.html_url,
                    raw_data = EXCLUDED.raw_data,
                    imported_at = NOW()
            """, (
                package_id,
                court_name,
                raw.get('courtType') or '',
                r['title'],
                case_number,
                raw.get('dateDecided') or r['date_issued'],
                raw.get('dateFiled') or r['date_issued'],
                ', '.join(raw.get('judges', [])) if isinstance(raw.get('judges'), list) else (raw.get('judges') or ''),
                ', '.join(raw.get('attorneys', [])) if isinstance(raw.get('attorneys'), list) else (raw.get('attorneys') or ''),
                ', '.join(raw.get('parties', [])) if isinstance(raw.get('parties'), list) else (raw.get('parties') or ''),
                raw.get('natureOfSuit') or '',
                raw.get('cause') or '',
                raw.get('jurisdiction') or '',
                raw.get('jurisdictionBasis') or '',
                raw.get('caseSource') or '',
                raw.get('caseSourceArea') or '',
                raw.get('caseSourceState') or '',
                ', '.join(raw.get('caseSourceSubdivisions', [])) if isinstance(raw.get('caseSourceSubdivisions'), list) else (raw.get('caseSourceSubdivisions') or ''),
                r['download_pdf_url'],
                raw.get('packageLink') or r['detail_view_txt_url'],
                raw.get('summary') or '',
                raw.get('outcome') or '',
                raw.get('disposition') or '',
                r['raw_data'],
                r['source_file'],
            ))
            inserted += 1
        except Exception as e:
            logger.debug(f"Court opinion insert failed: {e}")

    conn.commit()
    cur.close()
    conn.close()
    return inserted


def update_inventory(count: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE data_inventory 
        SET status = 'imported', actual_records = %s, last_updated = NOW()
        WHERE source_name = 'GovInfo Federal Register'
    """, (count,))
    conn.commit()
    cur.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-dir', type=Path, default=BASE_DIR, help='Directory containing GovInfo JSON files')
    parser.add_argument('--recursive', action='store_true', help='Scan JSON files recursively')
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("GOVINFO.GOV IMPORT")
    logger.info("=" * 80)
    
    create_tables()
    
    if args.recursive:
        json_files = sorted(
            path for path in args.base_dir.glob("**/*.json")
            if "_partial" not in path.name
        )
    else:
        json_files = []
        for subdir in ['bills', 'crpt', 'fr', 'uscode', 'uscourts']:
            json_files.extend(
                sorted(
                    path for path in (args.base_dir / subdir).glob("*.json")
                    if "_partial" not in path.name
                )
            )
    
    if not json_files:
        logger.warning("No JSON files found")
        return
    
    logger.info(f"Found {len(json_files)} JSON files")
    
    total_packages = 0
    
    for json_file in json_files:
        logger.info(f"Processing {json_file.name}...")
        records = parse_packages_file(json_file)
        if records:
            imported = import_packages(records)
            total_packages += imported
            logger.info(f"  Imported {imported} packages")
            fr_imported = import_federal_register_entries(records)
            if fr_imported:
                logger.info(f"  Imported {fr_imported} federal register entries")
            court_imported = import_court_opinions(records)
            if court_imported:
                logger.info(f"  Imported {court_imported} court opinions")
    
    update_inventory(total_packages)
    
    logger.info("=" * 80)
    logger.info(f"IMPORT COMPLETE: {total_packages} packages")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
