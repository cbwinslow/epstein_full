#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    # Check House FD
    try:
        cur.execute('SELECT COUNT(*) FROM house_financial_disclosures')
        house_count = cur.fetchone()[0]
        print(f'House FD: {house_count:,} records')
        
        # Check year range
        cur.execute('SELECT MIN(year), MAX(year) FROM house_financial_disclosures')
        min_year, max_year = cur.fetchone()
        print(f'Year range: {min_year}-{max_year}')
    except Exception as e:
        print(f'House FD: ERROR - {e}')
    
    # Check Senate FD
    try:
        cur.execute('SELECT COUNT(*) FROM senate_financial_disclosures')
        senate_count = cur.fetchone()[0]
        print(f'Senate FD: {senate_count:,} records')
    except Exception as e:
        print(f'Senate FD: ERROR - {e}')
    
    # Check Senate LDA
    try:
        cur.execute('SELECT COUNT(*) FROM lobbying_registrations')
        lda_reg = cur.fetchone()[0]
        print(f'Senate LDA Registrations: {lda_reg:,} records')
    except Exception as e:
        print(f'Senate LDA Registrations: ERROR - {e}')
    
    try:
        cur.execute('SELECT COUNT(*) FROM lobbying_quarterly_reports')
        lda_reports = cur.fetchone()[0]
        print(f'Senate LDA Reports: {lda_reports:,} records')
    except Exception as e:
        print(f'Senate LDA Reports: ERROR - {e}')

conn.close()
