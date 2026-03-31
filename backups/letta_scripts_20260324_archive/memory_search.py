#!/usr/bin/env python3
"""
Memory Search Protocols for Letta Server

This script provides multiple search protocols for retrieving memories from Letta server.
It wraps the Letta CLI and provides functions for different search strategies.

Usage:
    python memory_search.py --search "query"
    python memory_search.py --search-tags "tag1,tag2"
    python memory_search.py --list
    python memory_search.py --stats
"""

import argparse
import json
import subprocess
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class MemorySearch:
    """Memory search protocols for Letta server."""

    def __init__(self, agent_id: str = "agent-1167f15a-a10a-4595-b962-ec0f372aae0d"):
        self.agent_id = agent_id
        self.server_url = "http://localhost:8283"

    def run_letta_command(self, command: List[str]) -> Dict[str, Any]:
        """Run a Letta CLI command and return the result."""
        try:
            # Build the full command
            full_command = ["letta"] + command
            result = subprocess.run(full_command, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                return {"success": False, "error": result.stderr, "command": " ".join(full_command)}

            # Try to parse as JSON, otherwise return raw text
            try:
                data = json.loads(result.stdout)
                return {"success": True, "data": data, "raw": result.stdout}
            except json.JSONDecodeError:
                return {"success": True, "data": result.stdout, "raw": result.stdout}

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out", "command": " ".join(command)}
        except Exception as e:
            return {"success": False, "error": str(e), "command": " ".join(command)}

    def semantic_search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search memories using semantic similarity (archival-search)."""
        command = ["archival-search", self.agent_id, query]
        return self.run_letta_command(command)

    def list_memories(self, limit: int = 50) -> Dict[str, Any]:
        """List all archival memories."""
        command = ["archival", self.agent_id]
        return self.run_letta_command(command)

    def search_by_tags(self, tags: List[str]) -> Dict[str, Any]:
        """Search memories by tags (using grep on list output)."""
        # First get all memories
        result = self.list_memories()
        if not result["success"]:
            return result

        # Parse and filter by tags
        memories = result["data"] if isinstance(result["data"], list) else []
        filtered = []

        for memory in memories:
            memory_tags = memory.get("tags", [])
            if isinstance(memory_tags, str):
                memory_tags = memory_tags.split(",")
            if any(tag in memory_tags for tag in tags):
                filtered.append(memory)

        return {"success": True, "data": filtered, "filter": {"tags": tags}}

    def search_by_text(self, text: str) -> Dict[str, Any]:
        """Search memories by text content (grep)."""
        result = self.list_memories()
        if not result["success"]:
            return result

        memories = result["data"] if isinstance(result["data"], list) else []
        filtered = []

        for memory in memories:
            content = memory.get("text", "")
            if text.lower() in content.lower():
                filtered.append(memory)

        return {"success": True, "data": filtered, "filter": {"text": text}}

    def get_recent_memories(self, days: int = 7) -> Dict[str, Any]:
        """Get memories from the last N days."""
        result = self.list_memories()
        if not result["success"]:
            return result

        memories = result["data"] if isinstance(result["data"], list) else []
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = []

        for memory in memories:
            created_at = memory.get("created_at")
            if created_at:
                try:
                    mem_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    if mem_date >= cutoff_date:
                        recent.append(memory)
                except:
                    # Include if we can't parse date
                    recent.append(memory)

        return {"success": True, "data": recent, "filter": {"days": days}}

    def cross_agent_search(self, query: str, agent_ids: List[str] = None) -> Dict[str, Any]:
        """Search across multiple agents."""
        if agent_ids is None:
            agent_ids = [self.agent_id]

        all_results = {}

        for agent_id in agent_ids:
            # Temporarily change agent_id
            original_agent_id = self.agent_id
            self.agent_id = agent_id

            result = self.semantic_search(query)
            if result["success"]:
                all_results[agent_id] = result["data"]

            # Restore original agent_id
            self.agent_id = original_agent_id

        return {"success": True, "data": all_results, "agent_ids": agent_ids}

    def store_memory(self, text: str, tags: List[str] = None) -> Dict[str, Any]:
        """Store a new memory."""
        tags_str = ",".join(tags) if tags else ""
        command = ["archival-insert", self.agent_id, text, tags_str]
        return self.run_letta_command(command)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        result = self.list_memories()
        if not result["success"]:
            return result

        memories = result["data"] if isinstance(result["data"], list) else []

        # Count by tags
        tag_counts = {}
        for memory in memories:
            tags = memory.get("tags", [])
            if isinstance(tags, str):
                tags = tags.split(",")
            for tag in tags:
                tag = tag.strip()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return {
            "success": True,
            "data": {
                "total_memories": len(memories),
                "tag_counts": tag_counts,
                "recent_memories": self.get_recent_memories(7)["data"][:5],
            },
        }


def main():
    parser = argparse.ArgumentParser(description="Memory Search Protocols for Letta Server")
    parser.add_argument(
        "--agent-id",
        default="agent-1167f15a-a10a-4595-b962-ec0f372aae0d",
        help="Agent ID to search",
    )
    parser.add_argument("--search", help="Search memories by semantic similarity")
    parser.add_argument("--search-tags", help="Search by tags (comma-separated)")
    parser.add_argument("--search-text", help="Search by text content")
    parser.add_argument("--list", action="store_true", help="List all memories")
    parser.add_argument("--recent", type=int, help="Get memories from last N days")
    parser.add_argument("--stats", action="store_true", help="Get memory statistics")
    parser.add_argument("--store", help="Store a new memory")
    parser.add_argument("--tags", help="Tags for storage (comma-separated)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    searcher = MemorySearch(args.agent_id)

    if args.search:
        result = searcher.semantic_search(args.search)
    elif args.search_tags:
        tags = args.search_tags.split(",")
        result = searcher.search_by_tags(tags)
    elif args.search_text:
        result = searcher.search_by_text(args.search_text)
    elif args.list:
        result = searcher.list_memories()
    elif args.recent:
        result = searcher.get_recent_memories(args.recent)
    elif args.stats:
        result = searcher.get_memory_stats()
    elif args.store:
        tags = args.tags.split(",") if args.tags else []
        result = searcher.store_memory(args.store, tags)
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            if isinstance(result["data"], list):
                print(f"Found {len(result['data'])} memories:")
                for i, memory in enumerate(result["data"][:10], 1):
                    tags = memory.get("tags", "")
                    text = (
                        memory.get("text", "")[:100] + "..."
                        if len(memory.get("text", "")) > 100
                        else memory.get("text", "")
                    )
                    print(f"{i}. [{tags}] {text}")
            elif isinstance(result["data"], dict):
                for key, value in result["data"].items():
                    print(f"{key}: {value}")
            else:
                print(result["data"])
        else:
            print(f"Error: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
