#!/usr/bin/env python3
"""
Quick Recall Script for Conversations

This script provides quick recall of recent conversations from Letta memory.
It's designed to be used after restarting to pick up where you left off.

Usage:
    python recall_conversation.py --recent 7
    python recall_conversation.py --search "AI skills"
    python recall_conversation.py --tags "conversation,session"
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta


def recall_recent(days: int = 7, agent_id: str = "agent-1167f15a-a10a-4595-b962-ec0f372aae0d"):
    """Recall conversations from the last N days."""
    print(f"🔍 Recalling conversations from the last {days} days...")

    # Use memory search script
    cmd = [
        "python3",
        "/home/cbwinslow/workspace/epstein/scripts/memory_search.py",
        "--recent",
        str(days),
        "--agent-id",
        agent_id,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
    except Exception as e:
        print(f"Error running recall: {e}")


def search_conversations(query: str, agent_id: str = "agent-1167f15a-a10a-4595-b962-ec0f372aae0d"):
    """Search for specific conversations."""
    print(f"🔎 Searching for: {query}")

    cmd = [
        "python3",
        "/home/cbwinslow/workspace/epstein/scripts/memory_search.py",
        "--search",
        query,
        "--agent-id",
        agent_id,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
    except Exception as e:
        print(f"Error searching: {e}")


def search_by_tags(tags: str, agent_id: str = "agent-1167f15a-a10a-4595-b962-ec0f372aae0d"):
    """Search conversations by tags."""
    print(f"🏷️  Searching by tags: {tags}")

    cmd = [
        "python3",
        "/home/cbwinslow/workspace/epstein/scripts/memory_search.py",
        "--search-tags",
        tags,
        "--agent-id",
        agent_id,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
    except Exception as e:
        print(f"Error searching by tags: {e}")


def show_stats(agent_id: str = "agent-1167f15a-a10a-4595-b962-ec0f372aae0d"):
    """Show memory statistics."""
    print("📊 Memory Statistics:")

    cmd = [
        "python3",
        "/home/cbwinslow/workspace/epstein/scripts/memory_search.py",
        "--stats",
        "--agent-id",
        agent_id,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
    except Exception as e:
        print(f"Error getting stats: {e}")


def main():
    parser = argparse.ArgumentParser(description="Quick Recall for Conversations")
    parser.add_argument("--recent", type=int, help="Recall conversations from last N days")
    parser.add_argument("--search", help="Search for specific conversations")
    parser.add_argument("--tags", help="Search by tags (comma-separated)")
    parser.add_argument("--stats", action="store_true", help="Show memory statistics")
    parser.add_argument(
        "--agent-id",
        default="agent-1167f15a-a10a-4595-b962-ec0f372aae0d",
        help="Agent ID to search",
    )

    args = parser.parse_args()

    if args.recent:
        recall_recent(args.recent, args.agent_id)
    elif args.search:
        search_conversations(args.search, args.agent_id)
    elif args.tags:
        search_by_tags(args.tags, args.agent_id)
    elif args.stats:
        show_stats(args.agent_id)
    else:
        # Default: show recent conversations from last 7 days
        print("📋 Quick Recall - Recent Conversations (last 7 days)")
        print("=" * 60)
        recall_recent(7, args.agent_id)
        print("\n" + "=" * 60)
        print("💡 Other commands:")
        print("  python recall_conversation.py --search 'query'")
        print("  python recall_conversation.py --tags 'conversation,ai_skills'")
        print("  python recall_conversation.py --stats")


if __name__ == "__main__":
    main()
