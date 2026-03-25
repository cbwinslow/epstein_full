#!/usr/bin/env python3
"""
Epstein Project — Auto Memory Saver

Automatically saves memories to mem0 and folder-based storage.
Agents should call this after completing significant tasks.

Usage:
  python save_memory.py "Memory content here"
  python save_memory.py --tier status_update "New status update"
  python save_memory.py --tier finding "Important discovery"
  python save_memory.py --list                    # List all memories
  python save_memory.py --search "keyword"         # Search memories

Environment:
  MEM0_API_KEY: Mem0 API key (reads from .env if not set)
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

# =============================================================================
# Configuration
# =============================================================================

MEM0_API_KEY = os.environ.get("MEM0_API_KEY", "m0-3A6AR118Y6jrmP30ULZXrBkbUjABJnZsd4Vv798U")
USER_ID = "epstein-project"
MEMORY_DIR = "/home/cbwinslow/workspace/epstein/memories"
SESSION_DIR = os.path.join(MEMORY_DIR, "sessions")

# Load from .env if available
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.startswith("MEM0_API_KEY="):
                MEM0_API_KEY = line.split("=", 1)[1].strip()
                break


# =============================================================================
# Memory Operations
# =============================================================================

def save_to_mem0(content: str, tier: str = "general") -> bool:
    """Save memory to mem0 cloud.

    Args:
        content: Memory text.
        tier: Category tier (critical, architecture, gpu, data, finding, status_update).

    Returns:
        True if saved successfully.
    """
    try:
        from mem0 import MemoryClient
        client = MemoryClient(api_key=MEM0_API_KEY)
        metadata = {
            "tier": tier,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "auto_memory"
        }
        result = client.add(content, user_id=USER_ID, metadata=metadata)
        print(f"  ✓ mem0: {content[:60]}...")
        return True
    except Exception as e:
        print(f"  ✗ mem0 error: {e}")
        return False


def save_to_folder(content: str, tier: str = "general") -> bool:
    """Save memory to folder-based storage.

    Args:
        content: Memory text.
        tier: Category tier.

    Returns:
        True if saved successfully.
    """
    try:
        # Determine target folder
        tier_dirs = {
            "critical": "tier1-critical",
            "architecture": "tier2-architecture",
            "gpu": "tier3-gpu",
            "data": "tier4-data",
            "finding": "tier4-data",
            "status_update": "sessions",
            "general": "sessions",
        }
        target_dir = tier_dirs.get(tier, "sessions")
        target_path = os.path.join(MEMORY_DIR, target_dir)

        # Find or create file
        today = datetime.now().strftime("%Y-%m-%d")
        if target_dir == "sessions":
            filepath = os.path.join(target_path, f"{today}.md")
        else:
            filepath = os.path.join(target_path, f"{tier}_memories.md")

        # Append memory
        os.makedirs(target_path, exist_ok=True)
        with open(filepath, "a") as f:
            timestamp = datetime.now().strftime("%H:%M:%S")
            f.write(f"\n### [{timestamp}] {tier}\n")
            f.write(f"{content}\n")

        print(f"  ✓ folder: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ folder error: {e}")
        return False


def list_memories():
    """List all memories from folder storage."""
    print("\n=== Memory Index ===\n")
    for tier_dir in sorted(os.listdir(MEMORY_DIR)):
        tier_path = os.path.join(MEMORY_DIR, tier_dir)
        if os.path.isdir(tier_path):
            files = [f for f in os.listdir(tier_path) if f.endswith(".md")]
            print(f"  {tier_dir}:")
            for f in sorted(files):
                filepath = os.path.join(tier_path, f)
                size = os.path.getsize(filepath)
                print(f"    {f} ({size:,} bytes)")


def search_memories(query: str):
    """Search memories via mem0 semantic search."""
    try:
        from mem0 import MemoryClient
        client = MemoryClient(api_key=MEM0_API_KEY)
        results = client.search(query, user_id=USER_ID)
        print(f"\n=== Search: '{query}' ===\n")
        for r in results.get("results", []):
            print(f"  {r.get('memory', '')[:200]}")
            print(f"    Score: {r.get('score', 0):.3f}")
            print()
    except Exception as e:
        print(f"Search error: {e}")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Auto memory saver")
    parser.add_argument("content", nargs="?", help="Memory content")
    parser.add_argument("--tier", default="general",
                        choices=["critical", "architecture", "gpu", "data",
                                 "finding", "status_update", "general"],
                        help="Memory category")
    parser.add_argument("--list", action="store_true", help="List memories")
    parser.add_argument("--search", type=str, help="Search memories")

    args = parser.parse_args()

    if args.list:
        list_memories()
    elif args.search:
        search_memories(args.search)
    elif args.content:
        print(f"Saving memory (tier: {args.tier})...")
        save_to_mem0(args.content, args.tier)
        save_to_folder(args.content, args.tier)
        print("Done.")
    else:
        print("Usage: python save_memory.py 'memory content'")
        print("       python save_memory.py --tier finding 'discovery'")
        print("       python save_memory.py --list")
        print("       python save_memory.py --search 'keyword'")


if __name__ == "__main__":
    main()
