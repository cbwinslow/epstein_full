#!/usr/bin/env python3
"""
Epstein Project — Database Integrity Check

Validates data integrity: foreign keys, orphaned records, duplicate detection,
and cross-table consistency.

Usage:
  python db_integrity.py              # Full integrity check
  python db_integrity.py --fk         # Foreign key checks only
  python db_integrity.py --duplicates  # Duplicate detection only
"""

import sys
import os
import argparse
import os
import psycopg2
import os

# =============================================================================
# Configuration
# =============================================================================

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = os.environ.get("PG_PASSWORD", "")
PG_DB = "epstein"


def get_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASS,
        dbname=PG_DB
    )


def check_foreign_keys(conn):
    """Check for orphaned foreign key references."""
    print("\n=== Foreign Key Integrity ===")

    checks = [
        ("relationships.source_entity_id", "entities.id",
         "SELECT COUNT(*) FROM relationships r WHERE NOT EXISTS (SELECT 1 FROM entities e WHERE e.id = r.source_entity_id)"),
        ("relationships.target_entity_id", "entities.id",
         "SELECT COUNT(*) FROM relationships r WHERE NOT EXISTS (SELECT 1 FROM entities e WHERE e.id = r.target_entity_id)"),
        ("edge_sources.relationship_id", "relationships.id",
         "SELECT COUNT(*) FROM edge_sources es WHERE NOT EXISTS (SELECT 1 FROM relationships r WHERE r.id = es.relationship_id)"),
        ("email_participants.email_id", "emails.id",
         "SELECT COUNT(*) FROM email_participants ep WHERE NOT EXISTS (SELECT 1 FROM emails e WHERE e.id = ep.email_id)"),
        ("rider_clauses.subpoena_id", "subpoenas.id",
         "SELECT COUNT(*) FROM rider_clauses rc WHERE NOT EXISTS (SELECT 1 FROM subpoenas s WHERE s.id = rc.subpoena_id)"),
        ("clause_fulfillment.clause_id", "rider_clauses.id",
         "SELECT COUNT(*) FROM clause_fulfillment cf WHERE NOT EXISTS (SELECT 1 FROM rider_clauses rc WHERE rc.id = cf.clause_id)"),
        ("clause_fulfillment.return_id", "returns.id",
         "SELECT COUNT(*) FROM clause_fulfillment cf WHERE cf.return_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM returns r WHERE r.id = cf.return_id)"),
    ]

    passed = 0
    for ref_col, parent_col, query in checks:
        cur = conn.cursor()
        cur.execute(query)
        orphans = cur.fetchone()[0]
        if orphans == 0:
            print(f"  ✓ {ref_col} → {parent_col}")
            passed += 1
        else:
            print(f"  ✗ {ref_col} → {parent_col}: {orphans:,} orphans")

    print(f"\n  Result: {passed}/{len(checks)} FK checks passed")
    return passed == len(checks)


def check_duplicates(conn):
    """Check for duplicate records."""
    print("\n=== Duplicate Detection ===")

    checks = [
        ("documents", "efta_number"),
        ("pages", "efta_number, page_number"),
        ("entities", "name, entity_type"),
        ("emails", "efta_number, from_name, subject"),
        ("transcripts", "efta_number"),
    ]

    passed = 0
    for table, cols in checks:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT {cols}, COUNT(*) AS cnt
            FROM {table}
            GROUP BY {cols}
            HAVING COUNT(*) > 1
            LIMIT 5
        """)
        dups = cur.fetchall()
        if not dups:
            print(f"  ✓ {table} ({cols}): no duplicates")
            passed += 1
        else:
            print(f"  ⚠ {table} ({cols}): {len(dups)} duplicate groups found")
            for row in dups:
                print(f"    {row}")

    print(f"\n  Result: {passed}/{len(checks)} duplicate checks clean")
    return passed == len(checks)


def check_nulls(conn):
    """Check for unexpected NULL values in critical columns."""
    print("\n=== NULL Value Checks ===")

    checks = [
        ("entities", "name"),
        ("relationships", "relationship_type"),
        ("pages", "efta_number"),
        ("emails", "efta_number"),
        ("redactions", "efta_number"),
    ]

    passed = 0
    for table, col in checks:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
        nulls = cur.fetchone()[0]
        if nulls == 0:
            print(f"  ✓ {table}.{col}: no NULLs")
            passed += 1
        else:
            print(f"  ⚠ {table}.{col}: {nulls:,} NULLs")

    print(f"\n  Result: {passed}/{len(checks)} NULL checks clean")
    return passed == len(checks)


def check_cross_references(conn):
    """Check cross-table consistency (only for standard EFTA identifiers)."""
    print("\n=== Cross-Reference Checks ===")

    # Check if all EFTA-format efta_numbers in redactions exist in documents
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(DISTINCT r.efta_number)
        FROM redactions r
        WHERE r.efta_number LIKE 'EFTA%'
          AND NOT EXISTS (SELECT 1 FROM documents d WHERE d.efta_number = r.efta_number)
    """)
    missing = cur.fetchone()[0]
    print(f"  {'✓' if missing == 0 else '⚠'} Redaction EFTAs not in documents: {missing:,}")

    # Check if all EFTA-format efta_numbers in emails exist in documents
    # (Skip HOUSE_OVERSIGHT_* and DOJ-OGR_* — valid external sources)
    cur.execute("""
        SELECT COUNT(DISTINCT e.efta_number)
        FROM emails e
        WHERE e.efta_number LIKE 'EFTA%'
          AND NOT EXISTS (SELECT 1 FROM documents d WHERE d.efta_number = e.efta_number)
    """)
    missing_efta = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(DISTINCT e.efta_number)
        FROM emails e
        WHERE e.efta_number NOT LIKE 'EFTA%'
          AND NOT EXISTS (SELECT 1 FROM documents d WHERE d.efta_number = e.efta_number)
    """)
    missing_external = cur.fetchone()[0]

    print(f"  {'✓' if missing_efta == 0 else '⚠'} Email EFTAs not in documents: {missing_efta:,}")
    print(f"  ✓ Email external IDs (non-EFTA): {missing_external:,} (House Oversight, DOJ-OGR — expected)")

    return missing_efta == 0


def main():
    parser = argparse.ArgumentParser(description="Database integrity check")
    parser.add_argument("--fk", action="store_true", help="Foreign key checks only")
    parser.add_argument("--duplicates", action="store_true", help="Duplicate detection only")
    args = parser.parse_args()

    conn = get_conn()

    print("=" * 60)
    print("  DATABASE INTEGRITY CHECK")
    print("=" * 60)

    results = []

    if args.fk:
        results.append(("FK", check_foreign_keys(conn)))
    elif args.duplicates:
        results.append(("Duplicates", check_duplicates(conn)))
    else:
        results.append(("FK", check_foreign_keys(conn)))
        results.append(("Duplicates", check_duplicates(conn)))
        results.append(("NULLs", check_nulls(conn)))
        results.append(("Cross-ref", check_cross_references(conn)))

    conn.close()

    all_pass = all(r[1] for r in results)
    print(f"\n{'=' * 60}")
    print(f"  {'✓ ALL CHECKS PASSED' if all_pass else '✗ SOME CHECKS FAILED'}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
