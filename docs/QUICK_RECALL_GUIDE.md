# Quick Recall Guide for Epstein Project

## After Restarting Computer

To pick up where you left off, use these commands:

### 1. Recall Recent Conversations (Last 7 days)
```bash
cd /home/cbwinslow/workspace/epstein
python3 scripts/recall_conversation.py --recent 7
```

### 2. Search for Specific Topics
```bash
# Search for AI skills integration
python3 scripts/recall_conversation.py --search "AI skills integration"

# Search for configuration changes
python3 scripts/recall_conversation.py --search "OpenCode configuration"

# Search for Letta memory
python3 scripts/recall_conversation.py --search "Letta memory"
```

### 3. Search by Tags
```bash
# Search for conversation sessions
python3 scripts/recall_conversation.py --tags "conversation,session"

# Search for AI skills related memories
python3 scripts/recall_conversation.py --tags "ai_skills,configuration"

# Search for decisions
python3 scripts/recall_conversation.py --tags "decisions"
```

### 4. View Memory Statistics
```bash
python3 scripts/recall_conversation.py --stats
```

### 5. Advanced Search with memory_search.py
```bash
# Semantic search
python3 scripts/memory_search.py --search "AI skills"

# Search by tags
python3 scripts/memory_search.py --search-tags "ai_skills,opencode"

# Search by text content
python3 scripts/memory_search.py --search-text "configuration"

# List all memories
python3 scripts/memory_search.py --list

# Get stats
python3 scripts/memory_search.py --stats
```

### 6. Save New Conversations
```bash
# Save a conversation summary
python3 scripts/save_conversation_to_letta.py --summary "Your conversation summary here"

# Save key decisions
python3 scripts/save_conversation_to_letta.py --decisions "Decision 1" "Decision 2" "Decision 3"

# Save from JSON file
python3 scripts/save_conversation_to_letta.py --file conversation.json
```

### 7. Using Letta CLI Directly
```bash
# Search memories
letta archival-search agent-1167f15a-a10a-4595-b962-ec0f372aae0d "AI skills"

# Store a memory
letta archival-insert agent-1167f15a-a10a-4595-b962-ec0f372aae0d "Memory text" "tag1,tag2"

# List all memories
letta archival agent-1167f15a-a10a-4595-b962-ec0f372aae0d
```

## Current Session Context

**Last Session**: AI Skills Integration
- Updated OpenCode configuration to use centralized skills
- Created memory search protocols and scripts
- Stored conversation and decisions in Letta memory

**Agent ID**: `agent-1167f15a-a10a-4595-b962-ec0f372aae0d`
**Server URL**: `http://localhost:8283`

## Tips for Easy Recall

1. **Always tag conversations** with relevant tags like `conversation`, `session`, `ai_skills`, `opencode`
2. **Save decisions** separately for easy retrieval
3. **Use semantic search** for topic-based recall
4. **Check memory statistics** to see what's stored
5. **Save conversation summaries** at the end of each session
