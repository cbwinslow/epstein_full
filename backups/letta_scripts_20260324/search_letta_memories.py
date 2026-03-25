#!/usr/bin/env python3
"""
Search Letta Memory System

Search and retrieve memories from the Letta memory system.
Provides command-line interface for querying memories, agent context, and memory blocks.

Usage:
    # List recent memories
    python search_letta_memories.py --list

    # Search by type
    python search_letta_memories.py --type processing_status

    # Search by tags
    python search_letta_memories.py --tags ner processing

    # Search by content
    python search_letta_memories.py --search "entity extraction"

    # Show agent context
    python search_letta_memories.py --agent epstein_processor

    # Export memories to JSON
    python search_letta_memories.py --export memories.json
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any

# Add scripts directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from letta_memory import get_db_connection
except ImportError:
    print("Error: Could not import letta_memory module")
    sys.exit(1)


def search_memories_by_type(memory_type: str, limit: int = 10) -> List[Dict]:
    """Search memories by type."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, memory_type, title, LEFT(content, 100) as preview, 
                       created_at, tags
                FROM letta_memories 
                WHERE memory_type = %s
                ORDER BY created_at DESC 
                LIMIT %s
            """,
                (memory_type, limit),
            )

            results = []
            for row in cur.fetchall():
                results.append(
                    {
                        "id": row[0],
                        "memory_type": row[1],
                        "title": row[2],
                        "preview": row[3],
                        "created_at": row[4].isoformat() if row[4] else None,
                        "tags": row[5] if row[5] else [],
                    }
                )

            return results

    except Exception as e:
        print(f"Error searching memories: {e}")
        return []
    finally:
        conn.close()


def search_memories_by_content(search_term: str, limit: int = 10) -> List[Dict]:
    """Search memories by content."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            # Try trigram similarity if available
            try:
                cur.execute(
                    """
                    SELECT id, memory_type, title, 
                           similarity(content, %s) as score,
                           LEFT(content, 100) as preview,
                           created_at
                    FROM letta_memories 
                    WHERE content % %s
                    ORDER BY score DESC
                    LIMIT %s
                """,
                    (search_term, search_term, limit),
                )
            except:
                # Fallback to LIKE search
                cur.execute(
                    """
                    SELECT id, memory_type, title, 
                           0.5 as score,
                           LEFT(content, 100) as preview,
                           created_at
                    FROM letta_memories 
                    WHERE content LIKE %s OR title LIKE %s
                    ORDER BY created_at DESC
                    LIMIT %s
                """,
                    (f"%{search_term}%", f"%{search_term}%", limit),
                )

            results = []
            for row in cur.fetchall():
                results.append(
                    {
                        "id": row[0],
                        "memory_type": row[1],
                        "title": row[2],
                        "score": float(row[3]) if row[3] else 0.0,
                        "preview": row[4],
                        "created_at": row[5].isoformat() if row[5] else None,
                    }
                )

            return results

    except Exception as e:
        print(f"Error searching by content: {e}")
        return []
    finally:
        conn.close()


def search_memories_by_tags(tags: List[str], limit: int = 10) -> List[Dict]:
    """Search memories by tags."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            # Build tag array for query
            tag_array = "{" + ",".join(tags) + "}"

            cur.execute(
                """
                SELECT id, memory_type, title, 
                       LEFT(content, 100) as preview,
                       tags, created_at
                FROM letta_memories 
                WHERE tags @> %s::text[]
                ORDER BY created_at DESC 
                LIMIT %s
            """,
                (tag_array, limit),
            )

            results = []
            for row in cur.fetchall():
                results.append(
                    {
                        "id": row[0],
                        "memory_type": row[1],
                        "title": row[2],
                        "preview": row[3],
                        "tags": row[4] if row[4] else [],
                        "created_at": row[5].isoformat() if row[5] else None,
                    }
                )

            return results

    except Exception as e:
        print(f"Error searching by tags: {e}")
        return []
    finally:
        conn.close()


def get_agent_context(agent_name: str) -> List[Dict]:
    """Get agent context for specific agent."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT context_key, context_value, created_at, updated_at
                FROM letta_agent_context 
                WHERE agent_name = %s
                ORDER BY updated_at DESC
            """,
                (agent_name,),
            )

            results = []
            for row in cur.fetchall():
                try:
                    context_value = json.loads(row[1]) if row[1] else {}
                except:
                    context_value = {"raw": row[1]}

                results.append(
                    {
                        "context_key": row[0],
                        "context_value": context_value,
                        "created_at": row[2].isoformat() if row[2] else None,
                        "updated_at": row[3].isoformat() if row[3] else None,
                    }
                )

            return results

    except Exception as e:
        print(f"Error getting agent context: {e}")
        return []
    finally:
        conn.close()


def list_memory_types() -> List[Dict]:
    """List all memory types with counts."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT memory_type, COUNT(*) as count,
                       MAX(created_at) as latest
                FROM letta_memories 
                GROUP BY memory_type
                ORDER BY count DESC
            """)

            results = []
            for row in cur.fetchall():
                results.append(
                    {
                        "memory_type": row[0],
                        "count": row[1],
                        "latest": row[2].isoformat() if row[2] else None,
                    }
                )

            return results

    except Exception as e:
        print(f"Error listing memory types: {e}")
        return []
    finally:
        conn.close()


def export_memories(output_file: str) -> bool:
    """Export all memories to JSON file."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, memory_type, title, content, metadata, 
                       tags, created_at, updated_at
                FROM letta_memories 
                ORDER BY created_at DESC
            """)

            memories = []
            for row in cur.fetchall():
                try:
                    metadata = json.loads(row[4]) if row[4] else {}
                except:
                    metadata = {"raw": row[4]}

                memories.append(
                    {
                        "id": row[0],
                        "memory_type": row[1],
                        "title": row[2],
                        "content": row[3],
                        "metadata": metadata,
                        "tags": row[5] if row[5] else [],
                        "created_at": row[6].isoformat() if row[6] else None,
                        "updated_at": row[7].isoformat() if row[7] else None,
                    }
                )

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "export_date": datetime.now().isoformat(),
                        "total_memories": len(memories),
                        "memories": memories,
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )

            print(f"✅ Exported {len(memories)} memories to {output_file}")
            return True

    except Exception as e:
        print(f"Error exporting memories: {e}")
        return False
    finally:
        conn.close()


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Search Letta Memory System")
    parser.add_argument("--list", action="store_true", help="List recent memories")
    parser.add_argument("--type", help="Search by memory type")
    parser.add_argument("--tags", nargs="+", help="Search by tags")
    parser.add_argument("--search", help="Search by content")
    parser.add_argument("--agent", help="Show agent context")
    parser.add_argument("--export", help="Export memories to JSON file")
    parser.add_argument("--limit", type=int, default=10, help="Limit results")

    args = parser.parse_args()

    print("🧠 Letta Memory System Search")
    print("=" * 50)

    if args.export:
        export_memories(args.export)
        return

    if args.agent:
        print(f"🤖 Agent Context: {args.agent}")
        print("-" * 40)
        contexts = get_agent_context(args.agent)
        for ctx in contexts:
            print(f"  {ctx['context_key']}:")
            if isinstance(ctx["context_value"], dict):
                for k, v in ctx["context_value"].items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {ctx['context_value']}")
            print(f"    Updated: {ctx['updated_at']}")
        return

    if args.type:
        print(f"🔍 Memories of type: {args.type}")
        print("-" * 40)
        results = search_memories_by_type(args.type, args.limit)
        for mem in results:
            print(f"  [{mem['id']}] {mem['title']}")
            print(f"    {mem['preview']}...")
            print(f"    Created: {mem['created_at']}")
        return

    if args.tags:
        print(f"🏷️  Memories with tags: {', '.join(args.tags)}")
        print("-" * 40)
        results = search_memories_by_tags(args.tags, args.limit)
        for mem in results:
            print(f"  [{mem['id']}] {mem['title']}")
            print(f"    Tags: {', '.join(mem['tags'])}")
            print(f"    {mem['preview']}...")
        return

    if args.search:
        print(f"🔎 Search: '{args.search}'")
        print("-" * 40)
        results = search_memories_by_content(args.search, args.limit)
        for mem in results:
            print(f"  [{mem['id']}] {mem['title']} (score: {mem['score']:.2f})")
            print(f"    {mem['preview']}...")
        return

    # Default: show memory types
    print("📊 Memory Types:")
    print("-" * 40)
    types = list_memory_types()
    for t in types:
        print(f"  {t['memory_type']}: {t['count']} memories")
        if t["latest"]:
            print(f"    Latest: {t['latest']}")


if __name__ == "__main__":
    main()
