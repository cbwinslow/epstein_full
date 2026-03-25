# Letta Memory System Integration

## Overview

The Epstein Files project uses a custom Letta-inspired memory system for persistent knowledge storage, progress tracking, and state management across processing sessions.

## Architecture

### PostgreSQL Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `letta_memories` | Long-term knowledge storage | memory_type, title, content, metadata, tags |
| `letta_memory_blocks` | Reusable context blocks | label, content, description |
| `letta_agent_context` | Agent-specific state | agent_name, context_key, context_value |

### Memory Types

| Type | Use Case | Example |
|------|----------|---------|
| `processing_status` | Track progress of processing tasks | "NER extraction: 11K documents, 171K entities" |
| `technical_architecture` | System design and infrastructure | "PostgreSQL migration complete" |
| `conversation_log` | Opencode session logs | "Planning session: RAG database discussion" |
| `data_quality` | Data validation findings | "OCR redundant: 2.89M pages exist" |
| `verification_status` | Validation results | "File registry: 1.3M files hashed" |
| `project_overview` | High-level project context | "Epstein files analysis project" |

## Configuration

### Environment Variables (`.env`)

```bash
# PostgreSQL connection
PG_HOST=localhost
PG_PORT=5432
PG_USER=cbwinslow
PG_PASSWORD=123qweasd
PG_DBNAME=epstein
```

### Import Pattern

```python
import sys
import os
sys.path.append('scripts')  # Add scripts directory to path
from letta_memory import store_memory, store_agent_context, store_memory_block
```

## Integration Guide

### 1. Basic Memory Storage

```python
# Store processing progress
memory_id = store_memory(
    memory_type="processing_status",
    title="Entity Extraction Progress",
    content="Processed 11,100 documents, extracted 171,387 entities",
    metadata={
        "documents_processed": 11100,
        "entities_extracted": 171387,
        "script": "extract_entities.py",
        "timestamp": datetime.now().isoformat()
    },
    tags=["ner", "entities", "processing", "progress"]
)
```

### 2. Agent Context Updates

```python
# Update current focus
store_agent_context(
    agent_name="epstein_processor",
    context_key="current_focus",
    context_value="entity_extraction"
)

# Update processing counters
store_agent_context(
    agent_name="epstein_processor",
    context_key="entities_extracted",
    context_value=json.dumps({
        "count": 171387,
        "last_update": datetime.now().isoformat()
    })
)
```

### 3. Memory Blocks for Reusable Context

```python
# Store reusable processing pattern
store_memory_block(
    label="entity_extraction_workflow",
    content="""
    Entity Extraction Workflow:
    1. Load spaCy model (en_core_web_sm)
    2. Process documents in batches of 100
    3. Extract PERSON, ORG, GPE, DATE entities
    4. Store in document_entities table
    5. Update agent context with progress
    """,
    description="Standard entity extraction workflow"
)
```

### 4. Conversation Logging

```bash
# Save conversation logs from opencode
python scripts/save_conversation_to_letta.py --file session-ses_2f34.md --agent-name "data_analyst"

# Batch save all conversations
python scripts/save_conversation_to_letta.py --directory . --pattern "session-*.md"
```

### 5. Querying Memories

```python
# Get recent processing status
conn = get_db_connection()
with conn.cursor() as cur:
    cur.execute("""
        SELECT title, content, created_at 
        FROM letta_memories 
        WHERE memory_type = 'processing_status' 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    recent_status = cur.fetchall()
```

## Integration with Existing Scripts

### populate_file_registry.py

```python
# After scanning files
store_memory(
    memory_type="processing_status",
    title="File Registry Complete",
    content=f"Scanned {len(files)} files, inserted {inserted} records",
    metadata={"files_scanned": len(files), "records_inserted": inserted},
    tags=["file_registry", "processing", "complete"]
)
```

### extract_entities.py

```python
# After entity extraction batch
store_agent_context(
    agent_name="ner_processor",
    context_key="extraction_progress",
    context_value=json.dumps({
        "documents_processed": documents_processed,
        "entities_extracted": entities_extracted,
        "batch_time": time.time() - start_time
    })
)
```

### validate_text_content.py

```python
# Store validation results
store_memory(
    memory_type="verification_status",
    title="Text Content Validation",
    content=f"Coverage: {coverage:.1f}%, Missing: {missing:,} documents",
    metadata=validation_results,
    tags=["validation", "text_content", "quality_check"]
)
```

## Memory Search and Retrieval

### By Type

```sql
SELECT * FROM letta_memories 
WHERE memory_type = 'processing_status'
ORDER BY created_at DESC;
```

### By Tags

```sql
SELECT * FROM letta_memories 
WHERE tags @> ARRAY['ner', 'processing']
ORDER BY created_at DESC;
```

### By Content (Full-Text Search)

```sql
-- Enable pg_trgm extension if not already
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SELECT *, similarity(content, 'entity extraction') as score
FROM letta_memories 
WHERE content % 'entity extraction'
ORDER BY score DESC;
```

### Agent Context History

```sql
SELECT agent_name, context_key, context_value, created_at
FROM letta_agent_context 
WHERE agent_name = 'epstein_processor'
ORDER BY created_at DESC;
```

## Best Practices

### 1. Consistent Memory Types
- Use predefined memory types for consistency
- Follow naming conventions (snake_case)
- Include timestamps in metadata

### 2. Tag Strategy
- Always include `project: epstein_files`
- Add processing stage tags (e.g., `ner`, `ocr`, `file_registry`)
- Include status tags (e.g., `complete`, `in_progress`, `failed`)

### 3. Metadata Structure
- Include script name for traceability
- Add timestamps for timeline tracking
- Store quantitative metrics for analysis

### 4. Agent Context Updates
- Update context frequently during processing
- Use JSON for complex state data
- Include last update timestamp

### 5. Memory Block Usage
- Store reusable workflows as memory blocks
- Label blocks clearly for easy reference
- Update blocks when workflows change

## Monitoring

### Check Memory Count

```sql
SELECT memory_type, COUNT(*) as count
FROM letta_memories 
GROUP BY memory_type
ORDER BY count DESC;
```

### Recent Activity

```sql
SELECT DATE(created_at) as day, COUNT(*) as memories
FROM letta_memories 
GROUP BY DATE(created_at)
ORDER BY day DESC
LIMIT 7;
```

### Agent Context Status

```sql
SELECT agent_name, COUNT(*) as context_entries
FROM letta_agent_context 
GROUP BY agent_name;
```

## Troubleshooting

### Connection Issues
1. Check PostgreSQL is running: `systemctl status postgresql`
2. Verify password in `.env` file
3. Test connection: `psql -h localhost -U cbwinslow -d epstein`

### Missing Tables
```sql
-- Check if tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE 'letta_%';
```

### Large Memory Content
- Consider truncating very long content (> 100KB)
- Store references to files instead of full content
- Use memory blocks for large reusable content

## Integration Checklist

- [ ] Import `letta_memory` module
- [ ] Add progress logging at key milestones
- [ ] Update agent context during processing
- [ ] Store validation results as memories
- [ ] Save conversation logs from sessions
- [ ] Tag memories appropriately
- [ ] Include quantitative metrics in metadata

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-24  
**Author:** Epstein Files Analysis Project  
**Status:** Active Integration Guide