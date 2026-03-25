#!/usr/bin/env python3
"""
Simple wrapper for conversation logging.

Usage:
    # Log current conversation (from file)
    python log_conversation.py /path/to/conversation.md

    # Log from stdin
    echo "Conversation content" | python log_conversation.py -

    # Start watching
    python log_conversation.py --watch
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from conversation_logger.cli import main

    if __name__ == "__main__":
        # If no arguments, show help
        if len(sys.argv) == 1:
            print("Conversation Logger")
            print("Usage:")
            print("  python log_conversation.py <file>     # Log conversation from file")
            print("  python log_conversation.py -          # Log from stdin")
            print("  python log_conversation.py --watch    # Start watching for conversations")
            print("  python log_conversation.py --test     # Test Letta connection")
            print("  python log_conversation.py --stats    # Show statistics")
            sys.exit(0)

        # Modify sys.argv to work with CLI
        # Remove this script name, keep the rest
        original_argv = sys.argv[1:]

        # Map simple arguments to CLI commands
        if original_argv and not original_argv[0].startswith("-"):
            # First argument is a file path
            sys.argv = ["conversation_logger", "log"] + original_argv
        elif original_argv == ["--watch"]:
            sys.argv = ["conversation_logger", "watch"]
        elif original_argv == ["--test"]:
            sys.argv = ["conversation_logger", "test"]
        elif original_argv == ["--stats"]:
            sys.argv = ["conversation_logger", "stats"]
        elif original_argv == ["--search"] and len(original_argv) > 1:
            sys.argv = ["conversation_logger", "search", original_argv[1]]
        else:
            sys.argv = ["conversation_logger"] + original_argv

        main()

except ImportError as e:
    print(f"Error importing conversation_logger: {e}")
    print("Make sure you're running from the correct directory.")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
