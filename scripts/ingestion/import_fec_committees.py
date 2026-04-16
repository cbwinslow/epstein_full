#!/usr/bin/env python3
"""
Import FEC Candidates & Committees data to PostgreSQL
Source: FEC bulk data files
Tables: fec_candidates, fec_committees, fec_candidate_committee_links, fec_pac_summary
"""

import csv
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import psycopg2

BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files/fec_committees")
LOG_DIR = Path("/home/cbwinslow/workspace/epstein/logs/ingestion")

log_file = LOG_DIR / f"import_fec_committees_{datetime.now():%Y%m%d_%H%M%S}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Get PostgreSQL connection with hardcoded credentials"""
    return psycopg2.connect(
        host='localhost', database='epstein',
        user='cbwinslow', password='123qweasd'
    )


def create_tables():
    """Create FEC tables if they don't exist"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # FEC Candidates table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fec_candidates (
            id SERIAL PRIMARY KEY,
            candidate_id TEXT,
            candidate_name TEXT,
            party TEXT,
            election_year INT,
            state TEXT,
            district TEXT,
            office TEXT,
            incumbent TEXT,
            status TEXT,
            pcc TEXT,
            total_receipts NUMERIC,
            total_disbursements NUMERIC,
            cash_on_hand NUMERIC,
            debt NUMERIC,
            coverage_from DATE,
            coverage_through DATE,
            raw_data TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # FEC Committees table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fec_committees (
            id SERIAL PRIMARY KEY,
            committee_id TEXT,
            committee_name TEXT,
            committee_type TEXT,
            committee_designation TEXT,
            party TEXT,
            interest_group_category TEXT,
            connected_organization TEXT,
            candidate_id TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            treasurer_name TEXT,
            raw_data TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # FEC Candidate-Committee Links table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fec_candidate_committee_links (
            id SERIAL PRIMARY KEY,
            candidate_id TEXT,
            committee_id TEXT,
            election_year INT,
            committee_type TEXT,
            committee_designation TEXT,
            linkage_id TEXT,
            raw_data TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # FEC PAC Summary table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fec_pac_summary (
            id SERIAL PRIMARY KEY,
            committee_id TEXT,
            committee_name TEXT,
            committee_type TEXT,
            committee_designation TEXT,
            filing_frequency TEXT,
            total_receipts NUMERIC,
            total_disbursements NUMERIC,
            cash_on_hand NUMERIC,
            debt NUMERIC,
            coverage_from DATE,
            coverage_through DATE,
            raw_data TEXT,
            source_file TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fec_cand_id ON fec_candidates (candidate_id);
        CREATE INDEX IF NOT EXISTS idx_fec_cand_name ON fec_candidates (candidate_name);
        CREATE INDEX IF NOT EXISTS idx_fec_cand_state ON fec_candidates (state);
        CREATE INDEX IF NOT EXISTS idx_fec_cand_year ON fec_candidates (election_year);
        
        CREATE INDEX IF NOT EXISTS idx_fec_comm_id ON fec_committees (committee_id);
        CREATE INDEX IF NOT EXISTS idx_fec_comm_name ON fec_committees (committee_name);
        CREATE INDEX IF NOT EXISTS idx_fec_comm_type ON fec_committees (committee_type);
        CREATE INDEX IF NOT EXISTS idx_fec_comm_cand ON fec_committees (candidate_id);
        
        CREATE INDEX IF NOT EXISTS idx_fec_ccl_cand ON fec_candidate_committee_links (candidate_id);
        CREATE INDEX IF NOT EXISTS idx_fec_ccl_comm ON fec_candidate_committee_links (committee_id);
        
        CREATE INDEX IF NOT EXISTS idx_fec_pac_id ON fec_pac_summary (committee_id);
        CREATE INDEX IF NOT EXISTS idx_fec_pac_name ON fec_pac_summary (committee_name);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tables created/verified")


def parse_delimited_file(filepath: Path) -> List[Dict]:
    """Parse FEC pipe-delimited file"""
    records = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # FEC uses pipe delimiter
                fields = line.split('|')
                records.append(fields)
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
    
    return records


def import_candidates(filepath: Path, year: int) -> int:
    """Import candidate data from weball{YY}.txt file"""
    records = parse_delimited_file(filepath)
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0
    
    # FEC weball format: CAND_ID|CAND_NAME|CAND_ICI|PTY_CD|...|COV_END_DT|...
    for fields in records:
        try:
            if len(fields) < 10:
                continue
            
            cur.execute("""
                INSERT INTO fec_candidates (
                    candidate_id, candidate_name, party, election_year, state, district,
                    office, incumbent, status, pcc, total_receipts, total_disbursements,
                    cash_on_hand, debt, coverage_through, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                fields[0] if len(fields) > 0 else None,  # CAND_ID
                fields[1] if len(fields) > 1 else None,  # CAND_NAME
                fields[3] if len(fields) > 3 else None,  # PTY_CD
                year,
                fields[18] if len(fields) > 18 else None,  # CAND_ST
                fields[19] if len(fields) > 19 else None,  # CAND_DISTRICT
                fields[5] if len(fields) > 5 else None,   # CAND_OFFICE
                fields[4] if len(fields) > 4 else None,   # CAND_ICI
                fields[7] if len(fields) > 7 else None,   # CAND_STATUS
                fields[8] if len(fields) > 8 else None,   # PCC
                parse_amount(fields[10]) if len(fields) > 10 else 0,  # TTL_RECEIPTS
                parse_amount(fields[12]) if len(fields) > 12 else 0,  # TTL_DISB
                parse_amount(fields[14]) if len(fields) > 14 else 0,  # COH_COP
                parse_amount(fields[16]) if len(fields) > 16 else 0,  # DEBTS_OWED
                parse_date(fields[25]) if len(fields) > 25 else None,  # COV_END_DT
                '|'.join(fields),  # raw_data
                filepath.name
            ))
            inserted += 1
            
        except Exception as e:
            logger.debug(f"Insert failed for {fields[0] if fields else 'unknown'}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_committees(filepath: Path, year: int) -> int:
    """Import committee data from cm{YY}.txt file"""
    records = parse_delimited_file(filepath)
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0
    
    # FEC cm format: CMTE_ID|CMTE_NM|TRES_NM|CMTE_ST1|CMTE_ST2|...|CMTE_TP|...
    for fields in records:
        try:
            if len(fields) < 5:
                continue
            
            cur.execute("""
                INSERT INTO fec_committees (
                    committee_id, committee_name, treasurer_name, city, state, zip,
                    committee_type, committee_designation, party, interest_group_category,
                    connected_organization, candidate_id, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                fields[0] if len(fields) > 0 else None,  # CMTE_ID
                fields[1] if len(fields) > 1 else None,  # CMTE_NM
                fields[2] if len(fields) > 2 else None,  # TRES_NM
                fields[3] if len(fields) > 3 else None,  # CMTE_ST1
                fields[5] if len(fields) > 5 else None,  # CMTE_CITY
                fields[6] if len(fields) > 6 else None,  # CMTE_ST
                fields[10] if len(fields) > 10 else None,  # CMTE_TP
                fields[11] if len(fields) > 11 else None,  # CMTE_DSGN
                fields[12] if len(fields) > 12 else None,  # CMTE_PTY_AFFILIATION
                fields[13] if len(fields) > 13 else None,  # ORG_TP
                fields[14] if len(fields) > 14 else None,  # CONNECTED_ORG_NM
                fields[15] if len(fields) > 15 else None,  # CAND_ID
                '|'.join(fields),
                filepath.name
            ))
            inserted += 1
            
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_candidate_committee_links(filepath: Path, year: int) -> int:
    """Import candidate-committee linkage data from ccl{YY}.txt file"""
    records = parse_delimited_file(filepath)
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0
    
    # FEC ccl format: CAND_ID|CAND_ELECTION_YR|FEC_ELECTION_YR|CMTE_ID|CMTE_TP|...|LINKAGE_ID
    for fields in records:
        try:
            if len(fields) < 4:
                continue
            
            cur.execute("""
                INSERT INTO fec_candidate_committee_links (
                    candidate_id, election_year, committee_id, committee_type,
                    committee_designation, linkage_id, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                fields[0] if len(fields) > 0 else None,  # CAND_ID
                int(fields[1]) if len(fields) > 1 and fields[1].isdigit() else year,  # CAND_ELECTION_YR
                fields[3] if len(fields) > 3 else None,  # CMTE_ID
                fields[4] if len(fields) > 4 else None,  # CMTE_TP
                fields[5] if len(fields) > 5 else None,  # CMTE_DSGN
                fields[6] if len(fields) > 6 else None,  # LINKAGE_ID
                '|'.join(fields),
                filepath.name
            ))
            inserted += 1
            
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def import_pac_summary(filepath: Path, year: int) -> int:
    """Import PAC summary data from webk{YY}.txt file"""
    records = parse_delimited_file(filepath)
    if not records:
        return 0
    
    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0
    
    # FEC webk format: CMTE_ID|CMTE_NM|...|TTL_RECEIPTS|TTL_DISB|...|COH_COP|...
    for fields in records:
        try:
            if len(fields) < 10:
                continue
            
            cur.execute("""
                INSERT INTO fec_pac_summary (
                    committee_id, committee_name, committee_type, committee_designation,
                    filing_frequency, total_receipts, total_disbursements, cash_on_hand,
                    debt, coverage_through, raw_data, source_file
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                fields[0] if len(fields) > 0 else None,  # CMTE_ID
                fields[1] if len(fields) > 1 else None,  # CMTE_NM
                fields[9] if len(fields) > 9 else None,  # CMTE_TP
                fields[10] if len(fields) > 10 else None,  # CMTE_DSGN
                fields[11] if len(fields) > 11 else None,  # FILING_FREQ
                parse_amount(fields[14]) if len(fields) > 14 else 0,  # TTL_RECEIPTS
                parse_amount(fields[16]) if len(fields) > 16 else 0,  # TTL_DISB
                parse_amount(fields[18]) if len(fields) > 18 else 0,  # COH_COP
                parse_amount(fields[20]) if len(fields) > 20 else 0,  # DEBTS_OWED
                parse_date(fields[24]) if len(fields) > 24 else None,  # COV_END_DT
                '|'.join(fields),
                filepath.name
            ))
            inserted += 1
            
        except Exception as e:
            logger.debug(f"Insert failed: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    return inserted


def parse_amount(value: str) -> Optional[float]:
    """Parse amount string to float"""
    if not value:
        return 0
    try:
        # Remove commas and convert
        return float(value.replace(',', '').replace('$', ''))
    except:
        return 0


def parse_date(value: str) -> Optional[str]:
    """Parse date string to ISO format"""
    if not value:
        return None
    try:
        # FEC dates are MM/DD/YYYY
        parts = value.split('/')
        if len(parts) == 3:
            return f"{parts[2]}-{parts[0]}-{parts[1]}"
        return None
    except:
        return None


def update_inventory(counts: Dict[str, int]):
    """Update data inventory table"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    for source, count in counts.items():
        cur.execute("""
            INSERT INTO data_inventory (source_name, status, actual_records, last_updated)
            VALUES (%s, 'imported', %s, NOW())
            ON CONFLICT (source_name) DO UPDATE SET
                status = 'imported',
                actual_records = %s,
                last_updated = NOW()
        """, (source, count, count))
    
    conn.commit()
    cur.close()
    conn.close()


def main():
    logger.info("=" * 80)
    logger.info("FEC CANDIDATES & COMMITTEES IMPORT")
    logger.info("=" * 80)
    
    create_tables()
    
    if not BASE_DIR.exists():
        logger.error(f"Data directory not found: {BASE_DIR}")
        return
    
    txt_files = list(BASE_DIR.glob("*.txt"))
    if not txt_files:
        logger.warning("No .txt files found")
        return
    
    logger.info(f"Found {len(txt_files)} data files")
    
    counts = {
        'FEC Candidates': 0,
        'FEC Committees': 0,
        'FEC Candidate-Committee Links': 0,
        'FEC PAC Summary': 0
    }
    
    for txt_file in sorted(txt_files):
        logger.info(f"\nProcessing {txt_file.name}...")
        
        # Extract year from filename
        year = 2024
        if '20' in txt_file.name:
            try:
                year = int(txt_file.name.split('weball')[1].split('.')[0])
                if year < 100:
                    year = 2000 + year
            except:
                pass
        
        imported = 0
        
        if 'weball' in txt_file.name:
            imported = import_candidates(txt_file, year)
            counts['FEC Candidates'] += imported
            logger.info(f"  Imported {imported} candidates")
            
        elif 'cm' in txt_file.name and 'ccl' not in txt_file.name:
            imported = import_committees(txt_file, year)
            counts['FEC Committees'] += imported
            logger.info(f"  Imported {imported} committees")
            
        elif 'ccl' in txt_file.name:
            imported = import_candidate_committee_links(txt_file, year)
            counts['FEC Candidate-Committee Links'] += imported
            logger.info(f"  Imported {imported} linkages")
            
        elif 'webk' in txt_file.name:
            imported = import_pac_summary(txt_file, year)
            counts['FEC PAC Summary'] += imported
            logger.info(f"  Imported {imported} PAC records")
    
    update_inventory(counts)
    
    logger.info("\n" + "=" * 80)
    logger.info("IMPORT SUMMARY")
    logger.info("=" * 80)
    for source, count in counts.items():
        logger.info(f"  {source}: {count} records")
    total = sum(counts.values())
    logger.info(f"  TOTAL: {total} records")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
