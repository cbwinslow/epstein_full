#!/usr/bin/env python3
"""
Epstein Files - Letta Memory Management

Manages memories and context for the Epstein files analysis project.
Stores project knowledge, processing status, and analysis results in PostgreSQL.
"""

import json
import logging
import os
from typing import Dict, List, Optional

import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/home/cbwinslow/workspace/epstein/.env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/cbwinslow/workspace/epstein/processed/letta_memory.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Get PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=int(os.getenv("PG_PORT", 5432)),
            database=os.getenv("PG_DBNAME", "epstein"),
            user=os.getenv("PG_USER", "cbwinslow"),
            password=os.getenv("PG_PASSWORD", "123qweasd"),
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


def create_memory_tables():
    """Create tables for memory management."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            # Create memories table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS letta_memories (
                    id SERIAL PRIMARY KEY,
                    memory_type VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tags TEXT[]
                )
            """)

            # Create memory blocks table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS letta_memory_blocks (
                    id SERIAL PRIMARY KEY,
                    label VARCHAR(100) UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create agent context table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS letta_agent_context (
                    id SERIAL PRIMARY KEY,
                    agent_name VARCHAR(100) NOT NULL,
                    context_key VARCHAR(100) NOT NULL,
                    context_value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(agent_name, context_key)
                )
            """)

            # Create indexes
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_type ON letta_memories(memory_type)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_tags ON letta_memories USING GIN(tags)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_memory_blocks_label ON letta_memory_blocks(label)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_agent_context_name ON letta_agent_context(agent_name)"
            )

            conn.commit()
            logger.info("✓ Memory tables created successfully")
            return True

    except Exception as e:
        logger.error(f"Error creating memory tables: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def store_memory(
    memory_type: str, title: str, content: str, metadata: Dict = None, tags: List[str] = None
):
    """Store a memory in the database."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO letta_memories (memory_type, title, content, metadata, tags)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """,
                (memory_type, title, content, json.dumps(metadata or {}), tags or []),
            )

            memory_id = cur.fetchone()[0]
            conn.commit()

            logger.info(f"✓ Stored memory '{title}' (ID: {memory_id})")
            return memory_id

    except Exception as e:
        logger.error(f"Error storing memory: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_memory_by_title(title: str) -> Optional[Dict]:
    """Retrieve a memory by title."""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, memory_type, title, content, metadata, created_at, tags
                FROM letta_memories
                WHERE title = %s
                ORDER BY updated_at DESC
                LIMIT 1
            """,
                (title,),
            )

            result = cur.fetchone()
            if result:
                return {
                    "id": result[0],
                    "memory_type": result[1],
                    "title": result[2],
                    "content": result[3],
                    "metadata": json.loads(result[4]),
                    "created_at": result[5],
                    "tags": result[6],
                }
            return None

    except Exception as e:
        logger.error(f"Error retrieving memory: {e}")
        return None
    finally:
        conn.close()


def search_memories(query: str, memory_type: str = None, tags: List[str] = None) -> List[Dict]:
    """Search memories by content."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            # Build query
            sql = """
                SELECT id, memory_type, title, content, metadata, created_at, tags
                FROM letta_memories
                WHERE content ILIKE %s
            """
            params = [f"%{query}%"]

            if memory_type:
                sql += " AND memory_type = %s"
                params.append(memory_type)

            if tags:
                sql += " AND tags && %s"
                params.append(tags)

            sql += " ORDER BY updated_at DESC"

            cur.execute(sql, params)
            results = cur.fetchall()

            memories = []
            for row in results:
                memories.append(
                    {
                        "id": row[0],
                        "memory_type": row[1],
                        "title": row[2],
                        "content": row[3],
                        "metadata": json.loads(row[4]),
                        "created_at": row[5],
                        "tags": row[6],
                    }
                )

            return memories

    except Exception as e:
        logger.error(f"Error searching memories: {e}")
        return []
    finally:
        conn.close()


def store_memory_block(label: str, content: str, description: str = None):
    """Store a reusable memory block."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO letta_memory_blocks (label, content, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (label) DO UPDATE SET
                    content = EXCLUDED.content,
                    description = EXCLUDED.description,
                    updated_at = NOW()
                RETURNING id
            """,
                (label, content, description),
            )

            block_id = cur.fetchone()[0]
            conn.commit()

            logger.info(f"✓ Stored memory block '{label}' (ID: {block_id})")
            return block_id

    except Exception as e:
        logger.error(f"Error storing memory block: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_memory_block(label: str) -> Optional[Dict]:
    """Retrieve a memory block by label."""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, label, content, description, created_at, updated_at
                FROM letta_memory_blocks
                WHERE label = %s
                ORDER BY updated_at DESC
                LIMIT 1
            """,
                (label,),
            )

            result = cur.fetchone()
            if result:
                return {
                    "id": result[0],
                    "label": result[1],
                    "content": result[2],
                    "description": result[3],
                    "created_at": result[4],
                    "updated_at": result[5],
                }
            return None

    except Exception as e:
        logger.error(f"Error retrieving memory block: {e}")
        return None
    finally:
        conn.close()


def store_agent_context(agent_name: str, context_key: str, context_value: str):
    """Store agent-specific context."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO letta_agent_context (agent_name, context_key, context_value)
                VALUES (%s, %s, %s)
                ON CONFLICT (agent_name, context_key) DO UPDATE SET
                    context_value = EXCLUDED.context_value,
                    updated_at = NOW()
                RETURNING id
            """,
                (agent_name, context_key, context_value),
            )

            context_id = cur.fetchone()[0]
            conn.commit()

            logger.info(f"✓ Stored agent context '{agent_name}.{context_key}' (ID: {context_id})")
            return context_id

    except Exception as e:
        logger.error(f"Error storing agent context: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_agent_context(agent_name: str, context_key: str = None) -> Dict:
    """Retrieve agent-specific context."""
    conn = get_db_connection()
    if not conn:
        return {}

    try:
        with conn.cursor() as cur:
            if context_key:
                cur.execute(
                    """
                    SELECT context_key, context_value, updated_at
                    FROM letta_agent_context
                    WHERE agent_name = %s AND context_key = %s
                    ORDER BY updated_at DESC
                """,
                    (agent_name, context_key),
                )
            else:
                cur.execute(
                    """
                    SELECT context_key, context_value, updated_at
                    FROM letta_agent_context
                    WHERE agent_name = %s
                    ORDER BY updated_at DESC
                """,
                    (agent_name,),
                )

            results = cur.fetchall()

            context = {}
            for row in results:
                context[row[0]] = {"value": row[1], "updated_at": row[2]}

            return context

    except Exception as e:
        logger.error(f"Error retrieving agent context: {e}")
        return {}
    finally:
        conn.close()


def initialize_epstein_memories():
    """Initialize core memories for the Epstein files project."""

    # Project overview memory
    store_memory(
        memory_type="project_overview",
        title="Epstein Files Project Overview",
        content="""
        The Epstein Files Analysis Project is a comprehensive investigation into the Jeffrey Epstein case documents.
        
        Key Components:
        - 268,000+ PDF documents from DOJ datasets
        - PostgreSQL database with 1.39M+ documents
        - OCR processing pipeline using PyMuPDF and spaCy
        - Entity extraction for people, organizations, locations, dates, financial data
        - Knowledge graph with 606+ entities and 2,300+ relationships
        - Multiple pre-built databases with specialized analysis
        
        Processing Pipeline:
        1. Download datasets from DOJ website
        2. OCR extraction using PyMuPDF (text layer) and Surya (scanned pages)
        3. Entity extraction using spaCy NER and GLiNER
        4. Storage in PostgreSQL with FTS5 full-text search
        5. Knowledge graph building and relationship analysis
        6. Cross-referencing with pre-built databases
        
        Current Status:
        - Dataset 8: 1000 files processed (2.4M pages, 3.1M characters, 47,901 entities)
        - PostgreSQL database: 1.39M documents
        - Processing pipeline: Operational with all-pages support
        - Memory system: Active with project context tracking
        """,
        tags=["project", "overview", "epstein", "investigation"],
    )

    # Processing status memory
    store_memory(
        memory_type="processing_status",
        title="Current Processing Status",
        content="""
        Processing Pipeline Status:
        
        ✅ Completed:
        - Dataset 8: 1000/1000 files processed (100%)
        - OCR extraction: All pages processed
        - Entity extraction: 47,901 entities identified
        - PostgreSQL integration: Documents_content table created
        - Memory system: Letta memory management active
        
        🔄 In Progress:
        - Remaining datasets: 1-7, 9-10 (267K+ files remaining)
        - Full-scale processing: Ready to scale infrastructure
        - Cross-database integration: Linking with pre-built databases
        
        📊 Statistics:
        - Total pages processed: 2,477
        - Total characters extracted: 3,142,201
        - Entity breakdown:
          - PERSON: 8,335
          - ORG: 12,076
          - GPE: 6,167
          - DATE: 8,345
          - CARDINAL: 12,339
          - MONEY: 639
        
        🎯 Next Steps:
        1. Scale processing to remaining datasets
        2. Integrate with pre-built knowledge graphs
        3. Perform cross-dataset analysis
        4. Generate comprehensive reports
        """,
        tags=["status", "processing", "progress", "statistics"],
    )

    # Technical architecture memory
    store_memory(
        memory_type="technical_architecture",
        title="Technical Architecture",
        content="""
        System Architecture:
        
        Infrastructure:
        - Ubuntu 24.04 LTS server
        - Python 3.12 with uv package manager
        - PostgreSQL 16 database (epstein)
        - 3 GPUs: 2x Tesla K80, 1x Tesla K40m
        - 128GB RAM, 1TB NVMe storage
        
        Processing Pipeline:
        - OCR Backend: PyMuPDF (instant), Surya (GPU-accelerated), Docling (fallback)
        - NER: spaCy en_core_web_sm, GLiNER zero-shot, regex patterns
        - Storage: PostgreSQL with FTS5, pgvector for embeddings
        - Processing: Multi-threaded with 8 workers, chunked memory management
        
        Database Schema:
        - documents: Core document metadata (1.39M records)
        - entities: Named entities with source references
        - documents_content: OCR text content and processing metadata
        - relationships: Entity relationships and co-occurrence data
        - letta_memories: Project knowledge and context
        
        Integration Points:
        - Epstein-Pipeline: CLI tools for processing
        - Epstein-research-data: Pre-built analysis databases
        - epstein-ripper: DOJ download automation
        - Letta: Memory management and agent context
        
        Performance:
        - Processing speed: ~0.97 seconds per file
        - Memory management: 50-page chunks for large documents
        - GPU utilization: K80 for OCR, K40m for embeddings
        - Storage efficiency: Compressed text with metadata indexing
        """,
        tags=["architecture", "technical", "infrastructure", "database"],
    )

    # Memory blocks
    store_memory_block(
        label="project_context",
        content="""
        Epstein Files Analysis Project - Comprehensive investigation of Jeffrey Epstein case documents.
        Processing 268K+ PDFs with OCR and NER for entity extraction and knowledge graph building.
        PostgreSQL database with 1.39M documents, specialized analysis databases, and cross-referencing.
        """,
        description="Core project context for all agents",
    )

    store_memory_block(
        label="processing_pipeline",
        content="""
        1. Download datasets from DOJ website using epstein-ripper
        2. OCR extraction: PyMuPDF (text layer) + Surya (scanned pages) + Docling (fallback)
        3. Entity extraction: spaCy NER + GLiNER + regex patterns
        4. Storage: PostgreSQL with FTS5 search and pgvector embeddings
        5. Knowledge graph: Entity relationships and co-occurrence analysis
        6. Cross-referencing: Integration with pre-built databases
        """,
        description="Standard processing workflow",
    )

    store_memory_block(
        label="database_schema",
        content="""
        Core Tables:
        - documents: Document metadata (efta_number, dataset, file_path, etc.)
        - entities: Named entities with source references
        - documents_content: OCR text and processing metadata
        - relationships: Entity relationships
        - letta_memories: Project knowledge and context
        
        Pre-built Databases:
        - full_text_corpus.db: 1.4M docs with FTS5 search
        - redaction_analysis_v2.db: 2.59M redactions
        - image_analysis.db: 38K image descriptions
        - communications.db: 41K emails and communication pairs
        - transcripts.db: 1.6K media transcriptions
        - knowledge_graph.db: 606 entities, 2.3K relationships
        """,
        description="Database structure and schema",
    )

    logger.info("✓ Epstein project memories initialized")


def main():
    """Main function to set up memory system."""
    logger.info("Initializing Epstein Files Memory System...")

    # Create tables
    if not create_memory_tables():
        logger.error("Failed to create memory tables")
        return

    # Initialize core memories
    initialize_epstein_memories()

    # Store current processing status
    store_agent_context("epstein_processor", "last_dataset", "dataset_8")
    store_agent_context("epstein_processor", "files_processed", "1000")
    store_agent_context("epstein_processor", "total_pages", "2477")
    store_agent_context("epstein_processor", "entities_extracted", "47901")

    logger.info("✓ Memory system initialized successfully")


if __name__ == "__main__":
    main()
