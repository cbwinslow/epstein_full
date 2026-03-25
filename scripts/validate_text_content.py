#!/usr/bin/env python3
"""
Epstein Files - Validate Text Content Population

Validates the documents_content table population from hf-parquet files.
Checks data quality, coverage, and integrity.

Usage:
    python validate_text_content.py [--full-validation]

Checks:
    1. Row counts vs expected
    2. Text quality (length, content)
    3. Foreign key integrity
    4. Coverage gaps
    5. Error detection
"""

import sys
import logging
import argparse
from datetime import datetime
import psycopg2
from psycopg2 import sql

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# PostgreSQL configuration
PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}


def get_pg_connection():
    """Get PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


def validate_counts(conn):
    """Validate row counts and coverage."""
    logger.info("=== COUNT VALIDATION ===")

    with conn.cursor() as cur:
        # Total documents
        cur.execute("SELECT COUNT(*) FROM documents")
        total_docs = cur.fetchone()[0]
        logger.info(f"Total documents: {total_docs:,}")

        # Documents with content
        cur.execute("SELECT COUNT(*) FROM documents_content")
        docs_with_content = cur.fetchone()[0]
        logger.info(f"Documents with content: {docs_with_content:,}")

        # Coverage percentage
        coverage_pct = (docs_with_content / total_docs * 100) if total_docs > 0 else 0
        logger.info(f"Content coverage: {coverage_pct:.1f}%")

        # Documents missing content
        cur.execute("""
            SELECT COUNT(*) 
            FROM documents d
            LEFT JOIN documents_content dc ON d.id = dc.document_id
            WHERE dc.document_id IS NULL
        """)
        missing_content = cur.fetchone()[0]
        logger.info(f"Documents missing content: {missing_content:,}")

        return {
            "total_docs": total_docs,
            "docs_with_content": docs_with_content,
            "coverage_pct": coverage_pct,
            "missing_content": missing_content,
        }


def validate_text_quality(conn):
    """Validate text content quality."""
    logger.info("\n=== TEXT QUALITY VALIDATION ===")

    with conn.cursor() as cur:
        # Text length statistics
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(char_count) as avg_length,
                MIN(char_count) as min_length,
                MAX(char_count) as max_length,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY char_count) as median_length
            FROM documents_content 
            WHERE char_count > 0
        """)
        result = cur.fetchone()
        total_with_text, avg_len, min_len, max_len, median_len = result

        logger.info(f"Documents with text: {total_with_text:,}")
        logger.info(f"Average text length: {avg_len:,.0f} characters")
        logger.info(f"Median text length: {median_len:,.0f} characters")
        logger.info(f"Min text length: {min_len:,} characters")
        logger.info(f"Max text length: {max_len:,} characters")

        # Empty content check
        cur.execute("SELECT COUNT(*) FROM documents_content WHERE char_count = 0")
        empty_docs = cur.fetchone()[0]
        logger.info(f"Empty documents (0 chars): {empty_docs:,}")

        # Very short documents (< 100 chars)
        cur.execute(
            "SELECT COUNT(*) FROM documents_content WHERE char_count < 100 AND char_count > 0"
        )
        short_docs = cur.fetchone()[0]
        logger.info(f"Short documents (<100 chars): {short_docs:,}")

        # Very long documents (> 100K chars)
        cur.execute("SELECT COUNT(*) FROM documents_content WHERE char_count > 100000")
        long_docs = cur.fetchone()[0]
        logger.info(f"Long documents (>100K chars): {long_docs:,}")

        return {
            "total_with_text": total_with_text,
            "avg_length": avg_len,
            "median_length": median_len,
            "empty_docs": empty_docs,
            "short_docs": short_docs,
            "long_docs": long_docs,
        }


def validate_foreign_keys(conn):
    """Validate foreign key integrity."""
    logger.info("\n=== FOREIGN KEY VALIDATION ===")

    with conn.cursor() as cur:
        # Orphaned content (document_id not in documents table)
        cur.execute("""
            SELECT COUNT(*) 
            FROM documents_content dc
            LEFT JOIN documents d ON dc.document_id = d.id
            WHERE d.id IS NULL
        """)
        orphaned = cur.fetchone()[0]
        logger.info(f"Orphaned content (no matching document): {orphaned:,}")

        # Duplicate document_ids (should be none due to unique constraint)
        cur.execute("""
            SELECT document_id, COUNT(*) 
            FROM documents_content 
            GROUP BY document_id 
            HAVING COUNT(*) > 1
        """)
        duplicates = cur.fetchall()
        logger.info(f"Duplicate document_ids: {len(duplicates):,}")

        return {"orphaned": orphaned, "duplicates": len(duplicates)}


def validate_sample_content(conn, sample_size=5):
    """Validate sample of content."""
    logger.info(f"\n=== SAMPLE CONTENT VALIDATION (first {sample_size} rows) ===")

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT dc.document_id, d.efta_number, dc.char_count, 
                   LEFT(dc.content, 100) as preview
            FROM documents_content dc
            JOIN documents d ON dc.document_id = d.id
            ORDER BY dc.id
            LIMIT %s
        """,
            (sample_size,),
        )

        samples = cur.fetchall()
        for doc_id, efta_num, char_count, preview in samples:
            logger.info(f"  Doc {doc_id} ({efta_num}): {char_count:,} chars")
            logger.info(f"    Preview: {preview}...")

        return samples


def generate_report(conn, output_file=None):
    """Generate validation report."""
    logger.info("\n=== VALIDATION REPORT ===")

    # Run all validations
    counts = validate_counts(conn)
    quality = validate_text_quality(conn)
    fks = validate_foreign_keys(conn)
    samples = validate_sample_content(conn)

    # Summary
    logger.info("\n=== SUMMARY ===")
    logger.info(f"Status: {'PASS' if counts['missing_content'] < 100000 else 'WARNING'}")
    logger.info(f"Coverage: {counts['coverage_pct']:.1f}% of documents have text")
    logger.info(f"Quality: Average {quality['avg_length']:,.0f} chars per document")
    logger.info(f"Integrity: {fks['orphaned']} orphaned, {fks['duplicates']} duplicates")

    # Recommendations
    if counts["missing_content"] > 0:
        logger.info(
            f"\n⚠️  Consider investigating {counts['missing_content']:,} documents missing content"
        )
    if quality["empty_docs"] > 1000:
        logger.info(f"\n⚠️  {quality['empty_docs']:,} documents have empty content")
    if fks["orphaned"] > 0:
        logger.info(f"\n❌ {fks['orphaned']:,} orphaned records found - data integrity issue!")

    return {
        "counts": counts,
        "quality": quality,
        "foreign_keys": fks,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Validate text content population")
    parser.add_argument(
        "--full-validation",
        action="store_true",
        help="Run full validation including sample content",
    )

    args = parser.parse_args()

    logger.info("Epstein Files - Text Content Validation")
    logger.info("=" * 60)

    # Connect to PostgreSQL
    conn = get_pg_connection()
    if not conn:
        logger.error("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)

    try:
        # Generate validation report
        report = generate_report(conn)

        # Exit with appropriate code
        if report["foreign_keys"]["orphaned"] > 0:
            sys.exit(1)  # Critical issue
        elif report["counts"]["missing_content"] > 100000:
            sys.exit(2)  # Warning
        else:
            sys.exit(0)  # Success

    except Exception as e:
        logger.error(f"Validation error: {e}")
        sys.exit(3)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
