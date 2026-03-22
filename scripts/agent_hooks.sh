#!/bin/bash
# Agent Memory Hooks — call from cline, kilo, opencode, or any AI agent
# Usage: source this file, then call agent_hook <agent> <event> [context]
#
# Examples:
#   agent_hook cline task-complete "Fixed bug in scraper"
#   agent_hook kilo error "ImportError: no module xyz"
#   agent_hook opencode file-edit "Edited scripts/download.py"

MEMORY_SCRIPT="$HOME/workspace/epstein/scripts/letta_memory.py"
PYTHON="$HOME/workspace/epstein/.venv/bin/python"

agent_hook() {
    local agent="${1:-unknown}"
    local event="${2:-unknown}"
    local context="${3:-}"
    "$PYTHON" "$MEMORY_SCRIPT" auto-hook "$agent" "$event" "$context" 2>/dev/null
}

# Quick aliases
mem-save() {
    "$PYTHON" "$MEMORY_SCRIPT" save-memory --text "$1" --tags "${2:-manual}" 2>/dev/null
}

mem-search() {
    "$PYTHON" "$MEMORY_SCRIPT" search --query "$1" 2>/dev/null
}

mem-log() {
    "$PYTHON" "$MEMORY_SCRIPT" list --limit "${1:-10}" 2>/dev/null
}

mem-stats() {
    "$PYTHON" "$MEMORY_SCRIPT" stats 2>/dev/null
}

session-start() {
    "$PYTHON" "$MEMORY_SCRIPT" session-start "${1:-epstein}" 2>/dev/null
}

session-end() {
    "$PYTHON" "$MEMORY_SCRIPT" session-end --agent "${1:-epstein}" --summary "${2:-}" 2>/dev/null
}
