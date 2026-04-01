#!/usr/bin/env python3
"""
Epstein Files - Extract Named Entities using spaCy NER

Processes the documents_content table and extracts named entities
using spaCy NER (en_core_web_sm model). Stores results in document_entities table.

Usage:
    python extract_entities.py [--batch-size 100] [--model en_core_web_sm] [--limit 1000]

Features:
    - GPU-accelerated NER with spaCy
    - Batch processing for efficiency
    - Progress tracking with ETA
    - Entity types: PERSON, ORG, GPE, DATE, MONEY, CARDINAL, etc.
    - Resume capability (skip already processed documents)
    - Validation and reporting

Author: Epstein Files Analysis Project
Date: 2026-03-24
"""

import os
import sys
import logging
import argparse
import time
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
import spacy
from spacy.tokens import Doc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/cbwinslow/workspace/epstein/processed/entity_extraction.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_BATCH_SIZE = 100
DEFAULT_MODEL = "en_core_web_sm"
ENTITY_TYPES = [
    "PERSON",
    "ORG",
    "GPE",
    "DATE",
    "MONEY",
    "CARDINAL",
    "NORP",
    "FAC",
    "PRODUCT",
    "EVENT",
    "WORK_OF_ART",
    "LAW",
    "LANGUAGE",
    "LOC",
    "QUANTITY",
    "PERCENT",
    "TIME",
]

# PostgreSQL configuration
PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}


class EntityExtractor:
    """Extract named entities from text using spaCy."""

    def __init__(self, model_name: str = DEFAULT_MODEL, use_gpu: bool = True):
        """Initialize spaCy model."""
        try:
            # Try to use GPU
            if use_gpu:
                spacy.prefer_gpu()
                logger.info("Using GPU for NER processing")

            self.nlp = spacy.load(model_name)
            logger.info(f"Loaded spaCy model: {model_name}")

            # Increase max length for long documents
            self.nlp.max_length = 2000000  # 2MB text limit

        except Exception as e:
            logger.error(f"Failed to load spaCy model {model_name}: {e}")
            # Fallback to CPU
            self.nlp = spacy.load(model_name, disable=["parser", "ner"])
            self.nlp.enable_pipe("ner")
            logger.info("Falling back to CPU for NER processing")

    def extract_entities(self, text: str, document_id: int) -> List[Dict]:
        """Extract entities from text.

        Args:
            text: Input text
            document_id: Document ID for reference

        Returns:
            List of entity dictionaries
        """
        if not text or len(text.strip()) == 0:
            return []

        try:
            # Process text with spaCy
            doc = self.nlp(text[:1000000])  # Limit to 1M chars to avoid memory issues

            entities = []
            for ent in doc.ents:
                # Only include entity types we care about
                if ent.label_ in ENTITY_TYPES:
                    entity_dict = {
                        "document_id": document_id,
                        "entity_text": ent.text.strip(),
                        "entity_type": ent.label_,
                        "start_char": ent.start_char,
                        "end_char": ent.end_char,
                        "confidence": 0.9,  # spaCy doesn't provide confidence by default
                        "extraction_method": "spacy_ner",
                    }
                    entities.append(entity_dict)

            return entities

        except Exception as e:
            logger.error(f"Error extracting entities from document {document_id}: {e}")
            return []


def get_pg_connection():
    """Get PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


def get_processed_document_ids(conn) -> set:
    """Get set of document IDs already processed.

    Args:
        conn: PostgreSQL connection

    Returns:
        Set of document IDs
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT document_id FROM document_entities")
            return set(row[0] for row in cur.fetchall())
    except Exception as e:
        logger.error(f"Error fetching processed document IDs: {e}")
        return set()


def insert_entities_batch(entities: List[Dict], conn) -> int:
    """Insert batch of entities into document_entities table.

    Args:
        entities: List of entity dictionaries
        conn: PostgreSQL connection

    Returns:
        Number of entities inserted
    """
    if not entities:
        return 0

    try:
        with conn.cursor() as cur:
            # Prepare data for insertion
            data = []
            for entity in entities:
                data.append(
                    (
                        entity["document_id"],
                        entity["entity_text"],
                        entity["entity_type"],
                        entity["start_char"],
                        entity["end_char"],
                        entity["confidence"],
                        entity["extraction_method"],
                    )
                )

            # Insert with ON CONFLICT DO NOTHING (skip duplicates)
            query = """
                INSERT INTO document_entities 
                (document_id, entity_text, entity_type, start_char, end_char, 
                 confidence, extraction_method)
                VALUES %s
                ON CONFLICT (document_id, entity_text, entity_type, start_char) DO NOTHING
            """

            execute_values(cur, query, data)
            inserted = cur.rowcount
            conn.commit()

            return inserted

    except Exception as e:
        logger.error(f"Error inserting entities batch: {e}")
        conn.rollback()
        return 0


def process_documents(
    conn,
    extractor: EntityExtractor,
    batch_size: int = DEFAULT_BATCH_SIZE,
    limit: Optional[int] = None,
) -> Tuple[int, int, int]:
    """Process documents and extract entities.

    Args:
        conn: PostgreSQL connection
        extractor: EntityExtractor instance
        batch_size: Batch size for processing
        limit: Maximum number of documents to process

    Returns:
        Tuple of (documents_processed, entities_extracted, errors)
    """
    # Get already processed document IDs
    processed_ids = get_processed_document_ids(conn)
    logger.info(f"Found {len(processed_ids):,} already processed documents")

    # Build query for unprocessed documents with content
    query = """
        SELECT dc.document_id, dc.content, d.efta_number
        FROM documents_content dc
        JOIN documents d ON dc.document_id = d.id
        WHERE dc.document_id NOT IN %s
        AND dc.content IS NOT NULL 
        AND dc.char_count > 0
        ORDER BY dc.document_id
    """

    if limit:
        query += f" LIMIT {limit}"

    try:
        with conn.cursor() as cur:  # Regular cursor
            # Handle empty processed_ids set
            if processed_ids:
                params = (tuple(processed_ids),)
            else:
                params = ((0,),)  # Use dummy value that won't match any ID

            cur.execute(query, params)

            documents_processed = 0
            entities_extracted = 0
            errors = 0

            batch_entities = []

            while True:
                rows = cur.fetchmany(batch_size)
                if not rows:
                    break

                for document_id, content, efta_number in rows:
                    try:
                        # Extract entities
                        entities = extractor.extract_entities(content, document_id)

                        if entities:
                            batch_entities.extend(entities)
                            entities_extracted += len(entities)

                        documents_processed += 1

                        # Log progress every 100 documents
                        if documents_processed % 100 == 0:
                            logger.info(
                                f"Processed {documents_processed:,} documents, "
                                f"extracted {entities_extracted:,} entities"
                            )

                    except Exception as e:
                        logger.error(
                            f"Error processing document {document_id} ({efta_number}): {e}"
                        )
                        errors += 1
                        continue

                # Insert batch when it reaches batch_size
                if len(batch_entities) >= batch_size * 10:  # Insert every 10 batches
                    inserted = insert_entities_batch(batch_entities, conn)
                    logger.debug(f"Inserted {inserted:,} entities")
                    batch_entities = []

            # Insert remaining entities
            if batch_entities:
                inserted = insert_entities_batch(batch_entities, conn)
                logger.debug(f"Inserted final {inserted:,} entities")

            return documents_processed, entities_extracted, errors

    except Exception as e:
        logger.error(f"Error in document processing: {e}")
        return 0, 0, 1


def validate_results(conn):
    """Validate entity extraction results."""
    logger.info("=== VALIDATION RESULTS ===")

    with conn.cursor() as cur:
        # Count entities by type
        cur.execute("""
            SELECT entity_type, COUNT(*) as count
            FROM document_entities
            GROUP BY entity_type
            ORDER BY count DESC
        """)
        entity_counts = cur.fetchall()

        logger.info("Entity counts by type:")
        for entity_type, count in entity_counts:
            logger.info(f"  {entity_type}: {count:,}")

        # Documents with entities
        cur.execute("SELECT COUNT(DISTINCT document_id) FROM document_entities")
        docs_with_entities = cur.fetchone()[0]
        logger.info(f"Documents with entities: {docs_with_entities:,}")

        # Total entities
        cur.execute("SELECT COUNT(*) FROM document_entities")
        total_entities = cur.fetchone()[0]
        logger.info(f"Total entity mentions: {total_entities:,}")

        # Average entities per document
        cur.execute(
            "SELECT AVG(entity_count) FROM (SELECT COUNT(*) as entity_count FROM document_entities GROUP BY document_id) t"
        )
        avg_entities = cur.fetchone()[0]
        if avg_entities:
            logger.info(f"Average entities per document: {avg_entities:.1f}")

        # Sample entities
        cur.execute("""
            SELECT d.efta_number, de.entity_text, de.entity_type
            FROM document_entities de
            JOIN documents d ON de.document_id = d.id
            ORDER BY RANDOM()
            LIMIT 10
        """)
        samples = cur.fetchall()
        logger.info("\nSample entities:")
        for efta_num, entity_text, entity_type in samples:
            logger.info(f"  {efta_num}: {entity_text} ({entity_type})")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Extract named entities from documents")
    parser.add_argument(
        "--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="Batch size for processing"
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="spaCy model name")
    parser.add_argument("--limit", type=int, help="Limit number of documents to process")
    parser.add_argument(
        "--validate-only", action="store_true", help="Only validate existing results"
    )
    parser.add_argument("--no-gpu", action="store_true", help="Disable GPU processing")

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Epstein Files - Entity Extraction")
    logger.info("=" * 60)

    start_time = time.time()

    # Connect to PostgreSQL
    conn = get_pg_connection()
    if not conn:
        logger.error("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)

    try:
        if args.validate_only:
            # Only validate existing results
            validate_results(conn)
            return

        # Initialize entity extractor
        logger.info(f"Initializing spaCy model: {args.model}")
        extractor = EntityExtractor(model_name=args.model, use_gpu=not args.no_gpu)

        # Process documents
        logger.info("Starting entity extraction...")
        docs_processed, entities_extracted, errors = process_documents(
            conn, extractor, args.batch_size, args.limit
        )

        # Log results
        logger.info("=" * 60)
        logger.info("EXTRACTION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Documents processed: {docs_processed:,}")
        logger.info(f"Entities extracted: {entities_extracted:,}")
        logger.info(f"Errors: {errors:,}")

        if docs_processed > 0:
            avg_entities = entities_extracted / docs_processed
            logger.info(f"Average entities per document: {avg_entities:.1f}")

        elapsed_time = time.time() - start_time
        logger.info(f"\nTotal execution time: {elapsed_time / 60:.1f} minutes")

        # Validate results
        logger.info("\nValidating results...")
        validate_results(conn)

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
