#!/usr/bin/env python3
"""
Save Conversation to Letta

This script saves the current conversation to Letta memory.
It creates a comprehensive summary of the conversation and stores it with appropriate tags.

Usage:
    python save_conversation_to_letta.py --summary "Conversation summary"
    python save_conversation_to_letta.py --file conversation.json
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Any


class ConversationSaver:
    """Save conversations to Letta memory."""

    def __init__(self, agent_id: str = "agent-1167f15a-a10a-4595-b962-ec0f372aae0d"):
        self.agent_id = agent_id

    def save_summary(self, summary: str, tags: List[str] = None) -> Dict[str, Any]:
        """Save a conversation summary to Letta."""
        if tags is None:
            tags = ["conversation", "summary", datetime.now().strftime("%Y-%m-%d")]

        # Create a comprehensive memory entry
        memory_text = f"Conversation Summary ({datetime.now().isoformat()}):\n{summary}"

        # Use Letta CLI to store the memory
        tags_str = ",".join(tags)
        command = ["letta", "archival-insert", self.agent_id, memory_text, tags_str]

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Conversation saved to Letta memory",
                    "agent_id": self.agent_id,
                    "tags": tags,
                }
            else:
                return {"success": False, "error": result.stderr, "command": " ".join(command)}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def save_full_conversation(
        self, messages: List[Dict[str, str]], tags: List[str] = None
    ) -> Dict[str, Any]:
        """Save full conversation messages to Letta."""
        if tags is None:
            tags = ["conversation", "full", datetime.now().strftime("%Y-%m-%d")]

        # Format conversation as text
        conversation_text = "Full Conversation:\n\n"
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            conversation_text += f"{role.upper()}: {content}\n\n"

        # Save as memory
        return self.save_summary(conversation_text, tags)

    def save_decisions(self, decisions: List[str], tags: List[str] = None) -> Dict[str, Any]:
        """Save key decisions from conversation."""
        if tags is None:
            tags = ["decisions", "conversation", datetime.now().strftime("%Y-%m-%d")]

        decisions_text = "Key Decisions:\n"
        for i, decision in enumerate(decisions, 1):
            decisions_text += f"{i}. {decision}\n"

        memory_text = f"Conversation Decisions ({datetime.now().isoformat()}):\n{decisions_text}"

        tags_str = ",".join(tags)
        command = ["letta", "archival-insert", self.agent_id, memory_text, tags_str]

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Decisions saved to Letta memory",
                    "agent_id": self.agent_id,
                    "tags": tags,
                }
            else:
                return {"success": False, "error": result.stderr}

        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Save conversation to Letta memory")
    parser.add_argument(
        "--agent-id",
        default="agent-1167f15a-a10a-4595-b962-ec0f372aae0d",
        help="Agent ID to save to",
    )
    parser.add_argument("--summary", help="Conversation summary text")
    parser.add_argument("--file", help="JSON file with conversation messages")
    parser.add_argument("--decisions", nargs="+", help="List of key decisions")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    saver = ConversationSaver(args.agent_id)

    if args.summary:
        tags = args.tags.split(",") if args.tags else None
        result = saver.save_summary(args.summary, tags)
    elif args.file:
        try:
            with open(args.file, "r") as f:
                messages = json.load(f)
            tags = args.tags.split(",") if args.tags else None
            result = saver.save_full_conversation(messages, tags)
        except Exception as e:
            result = {"success": False, "error": str(e)}
    elif args.decisions:
        tags = args.tags.split(",") if args.tags else None
        result = saver.save_decisions(args.decisions, tags)
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"✓ {result['message']}")
            print(f"  Agent: {result['agent_id']}")
            print(f"  Tags: {', '.join(result['tags'])}")
        else:
            print(f"✗ Error: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
