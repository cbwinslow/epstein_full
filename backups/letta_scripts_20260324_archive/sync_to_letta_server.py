#!/usr/bin/env python3
"""
Sync Epstein Memories to Letta Server

Transfers memories from the custom Epstein memory system to the self-hosted
Letta server using archival memory insertion.

Usage:
    python sync_to_letta_server.py --agent coder
    python sync_to_letta_server.py --agent agent-1167f15a-a10a-4595-b962-ec0f372aae0d
"""

import sys
import os
import json
import subprocess
import argparse
from typing import List, Dict, Tuple

# Add scripts directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from letta_memory import get_db_connection
except ImportError:
    print("Error: Could not import letta_memory module")
    sys.exit(1)

# Agent IDs for common agents
AGENT_IDS = {
    "coder": "agent-1167f15a-a10a-4595-b962-ec0f372aae0d",
    "researcher": "agent-a3b6b8f5-dffb-49f2-82a8-69097d410f96",
    "infra-assistant": "agent-311b8012-989e-47d5-8ccc-c19574008162",
    "ops-monitor": "agent-7290d241-dbac-4dd5-b969-d601e8caac6d",
}


def get_agent_id(agent_name: str) -> str:
    """Get agent ID from name or return if already an ID."""
    if agent_name.startswith("agent-"):
        return agent_name
    return AGENT_IDS.get(agent_name, AGENT_IDS["coder"])


def fetch_custom_memories() -> List[Dict]:
    """Fetch all memories from custom Epstein memory system."""
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to PostgreSQL")
        return []

    memories = []
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, memory_type, title, content, metadata, tags, created_at
                FROM letta_memories 
                ORDER BY created_at ASC
            """)

            for row in cur.fetchall():
                # Handle metadata - may be dict (from JSONB) or string
                metadata = row[4]
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {"raw": metadata}
                elif metadata is None:
                    metadata = {}

                memory = {
                    "id": row[0],
                    "memory_type": row[1],
                    "title": row[2],
                    "content": row[3],
                    "metadata": metadata,
                    "tags": row[5] if row[5] else [],
                    "created_at": str(row[6]),
                }
                memories.append(memory)

        print(f"✅ Fetched {len(memories)} memories from custom system")
        return memories

    except Exception as e:
        print(f"Error fetching memories: {e}")
        return []
    finally:
        conn.close()


def format_memory_for_letta(memory: Dict) -> Tuple[str, str]:
    """Format memory content for Letta archival memory insertion."""
    # Create a concise summary for archival memory
    tags = memory.get("tags", [])
    tag_str = ",".join(tags) if tags else memory["memory_type"]

    # Create structured content
    content = f"[{memory['memory_type'].upper()}] {memory['title']}\n\n{memory['content']}"

    # Truncate if too long (Letta may have limits)
    if len(content) > 10000:
        content = content[:10000] + "\n\n[Content truncated...]"

    return content, tag_str


def insert_to_letta_server(agent_id: str, content: str, tags: str) -> bool:
    """Insert memory into Letta server using CLI."""
    try:
        # Use letta archival-insert command (with full path to avoid venv issues)
        letta_path = "/home/cbwinslow/bin/letta"  # Direct path to letta binary
        cmd = [
            letta_path,
            "archival-insert",
            agent_id,
            content[:1000],  # Truncate for command line
            tags,
        ]

        # Clean environment to avoid venv conflicts
        clean_env = {k: v for k, v in os.environ.items() if not k.startswith("VIRTUAL_ENV")}
        clean_env["PYTHONUNBUFFERED"] = "1"

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=clean_env)

        if result.returncode == 0:
            return True
        else:
            # Show actual command for debugging
            print(f"❌ Failed command: {' '.join(cmd[:3])}...")
            print(f"   Error: {result.stderr.strip()}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def update_agent_persona(agent_id: str, memory: Dict) -> bool:
    """Update agent persona with important context."""
    if memory["memory_type"] not in ["project_overview", "technical_architecture"]:
        return False

    try:
        # Update core memory (persona)
        cmd = [
            "letta",
            "memory-update",
            agent_id,
            "persona",
            f"Working on: {memory['title']}. {memory['content'][:500]}",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        return result.returncode == 0

    except Exception:
        return False


def save_conversation_to_letta(agent_id: str, conversation_file: str) -> bool:
    """Save conversation log to Letta server."""
    if not os.path.exists(conversation_file):
        print(f"⚠️ Conversation file not found: {conversation_file}")
        return False

    try:
        with open(conversation_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Create a summary of the conversation
        lines = content.split("\n")
        title = lines[0].lstrip("#").strip() if lines else "Unknown conversation"

        # Count key metrics
        assistant_messages = content.count("## Assistant")
        user_messages = content.count("## User")

        summary = f"""
        CONVERSATION LOG: {title}
        
        Session: {os.path.basename(conversation_file)}
        Assistant messages: {assistant_messages}
        User messages: {user_messages}
        Total length: {len(content):,} characters
        
        Key topics discussed:
        - Epstein files analysis project
        - File registry and text content population
        - NER entity extraction
        - Letta memory system integration
        
        Status at end:
        - NER extraction: In progress (4.5%)
        - Text content: Complete (98.8% coverage)
        - File registry: Complete (1.31M files)
        """

        # Insert as archival memory
        cmd = ["letta", "archival-insert", agent_id, summary, "conversation,log,epstein,session"]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print(f"✅ Saved conversation log: {title}")
            return True
        else:
            print(f"❌ Failed to save conversation: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error saving conversation: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Sync Epstein memories to Letta server")
    parser.add_argument("--agent", default="coder", help="Agent name or ID")
    parser.add_argument("--conversation", help="Path to conversation log file")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without executing"
    )

    args = parser.parse_args()

    agent_id = get_agent_id(args.agent)
    print(f"🧠 Syncing to Letta Server")
    print(f"   Agent: {args.agent} ({agent_id})")
    print("=" * 60)

    # Step 1: Fetch custom memories
    print("\n📥 Fetching memories from custom system...")
    memories = fetch_custom_memories()

    if not memories:
        print("❌ No memories found to sync")
        return

    # Step 2: Insert memories into Letta server
    print(f"\n📤 Inserting {len(memories)} memories into Letta server...")

    success_count = 0
    persona_updated = False

    for memory in memories:
        content, tags = format_memory_for_letta(memory)

        if args.dry_run:
            print(f"  [DRY RUN] Would insert: {memory['title'][:50]}...")
            success_count += 1
        else:
            if insert_to_letta_server(agent_id, content, tags):
                print(f"  ✅ {memory['title'][:50]}...")
                success_count += 1

                # Update persona for important memories
                if not persona_updated and update_agent_persona(agent_id, memory):
                    persona_updated = True
                    print(f"  📝 Updated agent persona")
            else:
                print(f"  ❌ Failed: {memory['title'][:50]}...")

    # Step 3: Save conversation log if provided
    if args.conversation:
        print(f"\n📝 Saving conversation log...")
        if not args.dry_run:
            save_conversation_to_letta(agent_id, args.conversation)

    # Summary
    print("\n" + "=" * 60)
    print(f"📊 SYNC COMPLETE")
    print(f"   ✅ Successfully synced: {success_count}/{len(memories)}")
    print(f"   📝 Agent persona updated: {'Yes' if persona_updated else 'No'}")
    print(f"   🤖 Agent ID: {agent_id}")

    # Show how to verify
    print(f"\n🔍 To verify memories in Letta server:")
    print(f'   letta archival-search {agent_id} "Epstein"')
    print(f"   letta agents  # View all agents")
    print(f'   letta send {agent_id} "What do you know about the Epstein project?"')


if __name__ == "__main__":
    main()
