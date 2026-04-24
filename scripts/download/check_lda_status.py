#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    # Check if Senate LDA tables exist
    try:
        cur.execute("SELECT COUNT(*) FROM lobbying_registrations")
        reg_count = cur.fetchone()[0]
        print(f"Lobbying Registrations: {reg_count:,} records")
    except Exception as e:
        print(f"Lobbying Registrations: ERROR - {e}")

    try:
        cur.execute("SELECT COUNT(*) FROM lobbying_quarterly_reports")
        report_count = cur.fetchone()[0]
        print(f"Lobbying Quarterly Reports: {report_count:,} records")
    except Exception as e:
        print(f"Lobbying Quarterly Reports: ERROR - {e}")

conn.close()
