#!/usr/bin/env python3
"""
Letta Memory Manager — PostgreSQL Direct Access

Reads/writes to the local Letta PostgreSQL database directly.
Supports archival memories, core memory blocks, conversation logs,
and automatic hooks for AI agents.

Usage:
  python letta_memory.py save-log --text "full conversation" --tags session
  python letta_memory.py save-memory --text "fact" --tags tag1,tag2
  python letta_memory.py search --query "database"
  python letta_memory.py core-memory --label persona --value "I am..."
  python letta_memory.py list --tags session
  python letta_memory.py stats
  python letta_memory.py session-start
  python letta_memory.py session-end --summary "did X, Y, Z"
  python letta_memory.py auto-hook cline task-complete "Fixed bug"
"""

import os
import sys
import json
import uuid
import hashlib
import argparse
import psycopg2
from datetime import datetime, timezone

# =============================================================================
# Config
# =============================================================================
LETTA_DB = dict(
    host=os.environ.get("LETTA_PG_HOST", "localhost"),
    port=int(os.environ.get("LETTA_PG_PORT", "5432")),
    user=os.environ.get("LETTA_PG_USER", "letta"),
    password=os.environ.get("LETTA_PG_PASSWORD", "123qweasd"),
    dbname=os.environ.get("LETTA_PG_DB", "letta"),
)

# Agent registry
AGENT_IDS = {
    "epstein": "agent-6833e981-f29d-428b-8d2a-4b7347587e2b",
    "infra": "agent-311b8012-989e-47d5-8ccc-c19574008162",
    "test-cli": "agent-ff55cd58-504a-4356-9f78-32e7123f8dfc",
}
DEFAULT_AGENT = "epstein"
ORG_ID = "org-00000000-0000-4000-8000-000000000000"
USER_ID = "user-00000000-0000-4000-8000-000000000000"


def get_db():
    """Get Letta database connection."""
    return psycopg2.connect(**LETTA_DB)


def get_agent_archive(agent_name):
    """Get the archive_id for an agent."""
    agent_id = AGENT_IDS.get(agent_name, AGENT_IDS[DEFAULT_AGENT])
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT archive_id FROM archives_agents WHERE agent_id = %s AND is_owner = true",
        (agent_id,),
    )
    row = cur.fetchone()
    db.close()
    return row[0] if row else None


def get_all_agent_ids():
    """Get all agent IDs from the registry."""
    return AGENT_IDS


# =============================================================================
# Archival Memory (Passages)
# =============================================================================
def insert_passage(text, tags=None, agent_name=DEFAULT_AGENT):
    """Insert an archival memory passage directly into PostgreSQL."""
    archive_id = get_agent_archive(agent_name)
    if not archive_id:
        print(f"ERROR: No archive found for agent '{agent_name}'")
        return None

    passage_id = f"passage-{uuid.uuid4()}"
    now = datetime.now(timezone.utc)
    tags_json = json.dumps(tags or [])
    meta_json = json.dumps({"source": "letta_memory.py", "agent": agent_name})

    db = get_db()
    cur = db.cursor()
    cur.execute(
        """INSERT INTO archival_passages
           (id, text, metadata_, tags, created_at, updated_at, is_deleted,
            _created_by_id, _last_updated_by_id, organization_id, archive_id)
           VALUES (%s, %s, %s::json, %s::json, %s, %s, false, %s, %s, %s, %s)
           RETURNING id""",
        (passage_id, text, meta_json, tags_json, now, now, USER_ID, USER_ID, ORG_ID, archive_id),
    )
    new_id = cur.fetchone()[0]

    # Also insert tags into passage_tags table for indexing
    for tag in tags or []:
        tag_id = f"ptag-{uuid.uuid4()}"
        cur.execute(
            """INSERT INTO passage_tags (id, tag, passage_id, archive_id, created_at, updated_at, is_deleted, _created_by_id, _last_updated_by_id, organization_id)
               VALUES (%s, %s, %s, %s, %s, %s, false, %s, %s, %s)""",
            (tag_id, tag, passage_id, archive_id, now, now, USER_ID, USER_ID, ORG_ID),
        )

    db.commit()
    db.close()
    return new_id


def list_passages(agent_name=DEFAULT_AGENT, tags_filter=None, limit=50):
    """List archival passages for an agent."""
    archive_id = get_agent_archive(agent_name)
    if not archive_id:
        print(f"ERROR: No archive found for agent '{agent_name}'")
        return []

    db = get_db()
    cur = db.cursor()

    if tags_filter:
        # Filter by tags using JSON containment
        tag_list = [t.strip() for t in tags_filter.split(",")]
        # Build a query that checks if any of the filter tags are in the passage's tags
        tag_conditions = " OR ".join(["tags::text LIKE %s" for _ in tag_list])
        params = [archive_id] + [f"%{t}%" for t in tag_list] + [limit]
        cur.execute(
            f"""SELECT id, text, tags, created_at FROM archival_passages
                WHERE archive_id = %s AND is_deleted = false
                AND ({tag_conditions})
                ORDER BY created_at DESC LIMIT %s""",
            params,
        )
    else:
        cur.execute(
            """SELECT id, text, tags, created_at FROM archival_passages
               WHERE archive_id = %s AND is_deleted = false
               ORDER BY created_at DESC LIMIT %s""",
            (archive_id, limit),
        )

    rows = cur.fetchall()
    db.close()

    results = []
    for row in rows:
        results.append(
            {
                "id": row[0],
                "text": row[1],
                "tags": row[2] if isinstance(row[2], list) else json.loads(row[2] or "[]"),
                "created_at": str(row[3]),
            }
        )
    return results


def search_passages(query, agent_name=DEFAULT_AGENT, limit=10):
    """Search archival passages using text matching (LIKE) since embeddings may not be set up."""
    archive_id = get_agent_archive(agent_name)
    if not archive_id:
        return []

    db = get_db()
    cur = db.cursor()
    cur.execute(
        """SELECT id, text, tags, created_at FROM archival_passages
           WHERE archive_id = %s AND is_deleted = false
           AND text ILIKE %s
           ORDER BY created_at DESC LIMIT %s""",
        (archive_id, f"%{query}%", limit),
    )
    rows = cur.fetchall()
    db.close()

    results = []
    for row in rows:
        results.append(
            {
                "id": row[0],
                "text": row[1],
                "tags": row[2] if isinstance(row[2], list) else json.loads(row[2] or "[]"),
                "created_at": str(row[3]),
            }
        )
    return results


def count_passages(agent_name=DEFAULT_AGENT):
    """Count archival passages for an agent."""
    archive_id = get_agent_archive(agent_name)
    if not archive_id:
        return 0
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM archival_passages WHERE archive_id = %s AND is_deleted = false",
        (archive_id,),
    )
    count = cur.fetchone()[0]
    db.close()
    return count


# =============================================================================
# Core Memory (Blocks)
# =============================================================================
def get_blocks(agent_name=DEFAULT_AGENT):
    """Get all core memory blocks for an agent."""
    agent_id = AGENT_IDS.get(agent_name, AGENT_IDS[DEFAULT_AGENT])
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """SELECT b.id, b.label, b.value, b.description, b.limit
           FROM block b
           JOIN blocks_agents ba ON b.id = ba.block_id
           WHERE ba.agent_id = %s AND b.is_deleted = false""",
        (agent_id,),
    )
    rows = cur.fetchall()
    db.close()
    return [
        {"id": r[0], "label": r[1], "value": r[2], "description": r[3], "limit": r[4]} for r in rows
    ]


def set_block(label, value, description="", agent_name=DEFAULT_AGENT):
    """Create or update a core memory block for an agent."""
    agent_id = AGENT_IDS.get(agent_name, AGENT_IDS[DEFAULT_AGENT])
    block_id = f"block-{uuid.uuid4()}"
    now = datetime.now(timezone.utc)
    char_limit = 5000

    db = get_db()
    cur = db.cursor()

    # Check if block already exists for this agent
    cur.execute(
        """SELECT b.id FROM block b
           JOIN blocks_agents ba ON b.id = ba.block_id
           WHERE ba.agent_id = %s AND b.label = %s AND b.is_deleted = false""",
        (agent_id, label),
    )
    existing = cur.fetchone()

    if existing:
        # Update existing block
        cur.execute(
            """UPDATE block SET value = %s, description = %s, updated_at = %s
               WHERE id = %s""",
            (value, description, now, existing[0]),
        )
        block_id = existing[0]
    else:
        # Create new block
        cur.execute(
            """INSERT INTO block (id, value, "limit", label, description, is_template, organization_id,
               created_at, updated_at, is_deleted, _created_by_id, _last_updated_by_id, read_only, hidden)
               VALUES (%s, %s, %s, %s, %s, false, %s, %s, %s, false, %s, %s, false, false)
               RETURNING id""",
            (block_id, value, char_limit, label, description, ORG_ID, now, now, USER_ID, USER_ID),
        )
        new_block_id = cur.fetchone()[0]

        # Link block to agent
        cur.execute(
            """INSERT INTO blocks_agents (agent_id, block_id, block_label)
               VALUES (%s, %s, %s)""",
            (agent_id, new_block_id, label),
        )

    db.commit()
    db.close()
    return block_id


# =============================================================================
# High-level functions
# =============================================================================
def chunk_text(text, max_chars=7500):
    """Split text into chunks that fit in archival passages."""
    chunks = []
    while len(text) > max_chars:
        split_at = text.rfind("\n", 0, max_chars)
        if split_at < max_chars // 2:
            split_at = text.rfind(". ", 0, max_chars)
        if split_at < max_chars // 2:
            split_at = max_chars
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        chunks.append(text)
    return chunks


def save_conversation_log(text, tags="", agent_name=DEFAULT_AGENT):
    """Save a full conversation log as archival memories + file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    date = datetime.now().strftime("%Y-%m-%d")

    # Save to file
    log_dir = os.path.expanduser("~/workspace/epstein/memories/conversation-logs")
    os.makedirs(log_dir, exist_ok=True)
    filepath = os.path.join(log_dir, f"conversation-{timestamp}.md")
    with open(filepath, "w") as f:
        f.write(f"# Conversation Log: {timestamp}\n\n")
        f.write(text)

    # Chunk and insert
    chunks = chunk_text(text)
    all_tags = [t.strip() for t in f"conversation-log,{date},{tags}".split(",") if t.strip()]

    ids = []
    for i, chunk in enumerate(chunks):
        label = f"CONVERSATION LOG {date} (part {i + 1}/{len(chunks)})"
        memory_text = f"{label}\n\n{chunk}"
        pid = insert_passage(memory_text, all_tags, agent_name)
        ids.append(pid)

    print(f"Saved: {filepath}")
    print(f"  {len(chunks)} chunks → Letta archival memory")
    print(f"  Tags: {all_tags}")
    return filepath, ids


def save_memory(text, tags="", agent_name=DEFAULT_AGENT):
    """Save a single memory."""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    content_hash = hashlib.md5(text.encode()).hexdigest()[:12]
    tag_list.append(f"hash:{content_hash}")

    pid = insert_passage(text, tag_list, agent_name)
    print(f"Memory saved: {text[:80]}...")
    print(f"  Tags: {tag_list}")
    return pid


def session_start(agent_name=DEFAULT_AGENT):
    """Start a session."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.now().strftime("%Y-%m-%d")

    text = f"SESSION START {timestamp}: Agent {agent_name} activated."
    insert_passage(text, ["session-start", date], agent_name)

    set_block(
        "current_session",
        f"Session {date} started at {timestamp}. Agent: {agent_name}.",
        "Tracks the current active session",
        agent_name,
    )
    print(f"Session started: {agent_name} at {timestamp}")


def session_end(agent_name=DEFAULT_AGENT, summary=""):
    """End a session."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.now().strftime("%Y-%m-%d")

    text = f"SESSION END {timestamp}: {summary}" if summary else f"SESSION END {timestamp}."
    insert_passage(text, ["session-end", date, "summary"], agent_name)

    # Save to session log file
    session_dir = os.path.expanduser("~/workspace/epstein/memories/sessions")
    os.makedirs(session_dir, exist_ok=True)
    filepath = os.path.join(session_dir, f"{date}.md")
    with open(filepath, "a") as f:
        f.write(f"\n## Session End: {timestamp}\n\n{summary}\n")

    set_block(
        "current_session",
        f"No active session. Last ended {timestamp}.",
        "Tracks the current active session",
        agent_name,
    )
    print(f"Session ended: {agent_name} at {timestamp}")


def auto_hook(agent_name_str, event, context=""):
    """Hook for AI agents to call automatically."""
    agent_name = DEFAULT_AGENT  # All hooks go to the default agent
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.now().strftime("%Y-%m-%d")

    text = f"[{agent_name_str}] {event} at {timestamp}"
    if context:
        text += f": {context}"

    tags = ["auto-hook", agent_name_str, event, date]
    insert_passage(text, tags, agent_name)
    print(f"Hook logged: {text}")


def show_stats(agent_name=DEFAULT_AGENT):
    """Show memory statistics."""
    archive_id = get_agent_archive(agent_name)
    agent_id = AGENT_IDS.get(agent_name)

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM archival_passages WHERE archive_id = %s AND is_deleted = false",
        (archive_id,),
    )
    total = cur.fetchone()[0]

    cur.execute(
        """SELECT tags::text, COUNT(*) FROM archival_passages
           WHERE archive_id = %s AND is_deleted = false
           GROUP BY tags::text ORDER BY COUNT(*) DESC LIMIT 10""",
        (archive_id,),
    )
    tag_counts = cur.fetchall()

    cur.execute(
        """SELECT COUNT(*) FROM block b
           JOIN blocks_agents ba ON b.id = ba.block_id
           WHERE ba.agent_id = %s AND b.is_deleted = false""",
        (agent_id,),
    )
    block_count = cur.fetchone()[0]

    db.close()

    print(f"Agent: {agent_name} ({agent_id})")
    print(f"Archive: {archive_id}")
    print(f"Archival passages: {total}")
    print(f"Core memory blocks: {block_count}")
    print(f"\nTop tag groups:")
    for tags_json, count in tag_counts[:5]:
        tags = tags_json if isinstance(tags_json, list) else json.loads(tags_json or "[]")
        print(f"  {tags}: {count}")


# =============================================================================
# CLI
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Letta Memory Manager (PostgreSQL)")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("save-log", help="Save conversation log")
    p.add_argument("--text", help="Conversation text")
    p.add_argument("--file", help="File to read from")
    p.add_argument("--tags", default="", help="Comma-separated tags")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")

    p = sub.add_parser("save-memory", help="Save a single memory")
    p.add_argument("--text", required=True, help="Memory text")
    p.add_argument("--tags", default="", help="Comma-separated tags")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")

    p = sub.add_parser("search", help="Search memories")
    p.add_argument("--query", required=True, help="Search query")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")

    p = sub.add_parser("core-memory", help="Set core memory block")
    p.add_argument("--label", required=True, help="Block label")
    p.add_argument("--value", required=True, help="Block value")
    p.add_argument("--description", default="", help="Block description")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")

    p = sub.add_parser("list", help="List memories")
    p.add_argument("--tags", default=None, help="Filter by tags")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")
    p.add_argument("--limit", type=int, default=20, help="Max results")

    p = sub.add_parser("stats", help="Show memory stats")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")

    p = sub.add_parser("session-start", help="Start session")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")

    p = sub.add_parser("session-end", help="End session")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")
    p.add_argument("--summary", default="", help="Session summary")

    p = sub.add_parser("auto-hook", help="Agent auto-hook")
    p.add_argument("agent_name", help="Agent name (cline, kilo, opencode)")
    p.add_argument("event", help="Event type")
    p.add_argument("context", nargs="?", default="", help="Context")

    p = sub.add_parser("blocks", help="Show core memory blocks")
    p.add_argument("--agent", default=DEFAULT_AGENT, help="Agent name")

    args = parser.parse_args()

    if args.command == "save-log":
        if args.file:
            with open(args.file) as f:
                text = f.read()
        elif args.text:
            text = args.text
        else:
            print("Provide --file or --text")
            sys.exit(1)
        save_conversation_log(text, args.tags, args.agent)

    elif args.command == "save-memory":
        save_memory(args.text, args.tags, args.agent)

    elif args.command == "search":
        results = search_passages(args.query, args.agent)
        if results:
            print(f"Found {len(results)} results:\n")
            for i, r in enumerate(results, 1):
                print(f"  [{i}] {r['text'][:200]}")
                print(f"      Tags: {r['tags']}")
                print()
        else:
            print("No results found.")

    elif args.command == "core-memory":
        bid = set_block(args.label, args.value, args.description, args.agent)
        print(f"Core memory set: {args.label}")

    elif args.command == "list":
        passages = list_passages(args.agent, args.tags, args.limit)
        print(f"Archival memories: {len(passages)}")
        for p in passages:
            print(f"  [{p['created_at'][:19]}] {p['text'][:100]}")
            print(f"    Tags: {p['tags']}")

    elif args.command == "stats":
        show_stats(args.agent)

    elif args.command == "session-start":
        session_start(args.agent)

    elif args.command == "session-end":
        session_end(args.agent, args.summary)

    elif args.command == "auto-hook":
        auto_hook(args.agent_name, args.event, args.context)

    elif args.command == "blocks":
        blocks = get_blocks(args.agent)
        for b in blocks:
            print(f"  {b['label']}: {b['value'][:200]}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
