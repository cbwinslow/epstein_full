#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    # Check government data tables
    gov_tables = [
        "congress_members",
        "congress_bills",
        "fec_candidates",
        "fec_committees",
        "fec_candidate_committee_links",
        "fec_pac_summary",
        "fec_individual_contributions",
        "govinfo_packages",
        "federal_register_entries",
        "court_opinions",
        "fara_registrations",
        "fara_foreign_principals",
        "lobbying_registrations",
        "lobbying_quarterly_reports",
        "whitehouse_visitors",
        "usa_spending_awards",
        "house_financial_disclosures",
        "senate_financial_disclosures",
    ]

    print("Government Data Ingestion Status:")
    print("=" * 60)
    for table in gov_tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"{table:40} {count:>12,}")
        except Exception as e:
            print(f"{table:40} ERROR - {str(e)[:30]}")

    print("\n" + "=" * 60)
    print("Senate LDA Status:")
    try:
        cur.execute("SELECT COUNT(*) FROM lobbying_registrations")
        lda_reg = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM lobbying_quarterly_reports")
        lda_reports = cur.fetchone()[0]
        print(f"LDA Registrations: {lda_reg:,}")
        print(f"LDA Quarterly Reports: {lda_reports:,}")
    except Exception as e:
        print(f"ERROR: {e}")

conn.close()
