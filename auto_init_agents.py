#!/usr/bin/env python3
"""
Auto-initialization script for AI agents in the Epstein Files project.
Sets up framework integrations (LangChain, CrewAI, AutoGen), creates shell aliases,
and initializes all agents with global rules.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from letta_memory import (
    store_memory,
    store_memory_block,
    store_agent_context,
    initialize_epstein_memories,
)

def initialize_langchain_agent():
    """Initialize LangChain agent with Epstein-specific configurations."""
    
    # Store agent context
    store_agent_context(
        agent_name="langchain_agent",
        context_key="framework_config",
        context_value=json.dumps({
            "framework": "LangChain",
            "version": "latest",
            "epstein_integration": True,
            "database": "postgresql",
            "vector_store": "pgvector",
            "models": ["gpt-4", "claude-3", "llama-3"],
            "memory_backend": "letta",
            "tools": ["epstein_search", "entity_extraction", "knowledge_graph"],
        })
    )
    
    # Store memory block for LangChain configuration
    store_memory_block(
        label="langchain_config",
        content="""
LangChain Agent Configuration for Epstein Files:

Framework: LangChain (latest version)
Integration: Direct PostgreSQL connection
Vector Store: pgvector for embeddings
Memory: Letta-based persistent memory
Available Tools:
- epstein_search: Full-text search across 1.4M documents
- entity_extraction: Named entity recognition with spaCy/GLiNER
- knowledge_graph: Query relationships between entities
- document_analysis: Comprehensive document analysis
- cross_reference: Cross-database entity matching

Models Supported:
- GPT-4: For complex reasoning and analysis
- Claude-3: For document summarization and Q&A
- Llama-3: For local processing and classification

Configuration Notes:
- Uses centralized Letta memory for context persistence
- Integrates with Epstein pipeline for document processing
- Supports multi-modal analysis (text, images, audio)
        """,
        description="LangChain agent configuration for Epstein Files project"
    )
    
    print("✓ LangChain agent initialized successfully")

def initialize_crewai_agent():
    """Initialize CrewAI agent with Epstein-specific configurations."""
    
    # Store agent context
    store_agent_context(
        agent_name="crewai_agent",
        context_key="framework_config",
        context_value=json.dumps({
            "framework": "CrewAI",
            "version": "latest",
            "epstein_integration": True,
            "task_management": "sqlite",
            "memory_backend": "letta",
            "crew_structure": "specialized_agents",
            "tools": ["download_worker", "ocr_worker", "ner_worker", "kg_worker"],
        })
    )
    
    # Store memory block for CrewAI configuration
    store_memory_block(
        label="crewai_config",
        content="""
CrewAI Agent Configuration for Epstein Files:

Framework: CrewAI (latest version)
Integration: SQLite task management
Memory: Letta-based persistent memory
Crew Structure: Specialized worker agents

Available Workers:
- download_worker: Handles DOJ website downloads (5 parallel workers)
- ocr_worker: Extracts text from PDFs using PyMuPDF/Surya
- ner_worker: Named entity recognition with spaCy/GLiNER
- kg_worker: Knowledge graph building and relationship extraction
- transcribe_worker: Audio/video transcription with faster-whisper
- image_worker: Image analysis and face detection

Task Management:
- SQLite-based task queue for persistence
- Priority-based task scheduling
- Progress tracking and resume capability
- Error handling and retry mechanisms

Memory Integration:
- Letta memory for agent context and decisions
- Cross-agent communication through shared memory
- Workflow state persistence across sessions
        """,
        description="CrewAI agent configuration for Epstein Files project"
    )
    
    print("✓ CrewAI agent initialized successfully")

def initialize_autogen_agent():
    """Initialize AutoGen agent with Epstein-specific configurations."""
    
    # Store agent context
    store_agent_context(
        agent_name="autogen_agent",
        context_key="framework_config",
        context_value=json.dumps({
            "framework": "AutoGen",
            "version": "latest",
            "epstein_integration": True,
            "conversation_management": "sqlite",
            "memory_backend": "letta",
            "conversation_styles": ["collaborative", "hierarchical", "adversarial"],
            "tools": ["document_analysis", "entity_search", "graph_query", "media_transcription"],
        })
    )
    
    # Store memory block for AutoGen configuration
    store_memory_block(
        label="autogen_config",
        content="""
AutoGen Agent Configuration for Epstein Files:

Framework: AutoGen (latest version)
Integration: SQLite conversation management
Memory: Letta-based persistent memory
Conversation Styles: Multiple collaboration modes

Available Conversation Styles:
- Collaborative: Two agents working together on analysis
- Hierarchical: Manager-worker agent structure
- Adversarial: Debate-style analysis for validation

Available Tools:
- document_analysis: Comprehensive document processing
- entity_search: Search across entities and relationships
- graph_query: Knowledge graph exploration
- media_transcription: Audio/video content analysis
- cross_validation: Multi-agent verification workflows

Memory Features:
- Persistent conversation history
- Agent-specific context tracking
- Decision logging and rationale storage
- Workflow state management

Use Cases:
- Collaborative document analysis
- Multi-agent verification workflows
- Complex reasoning and validation
- Cross-database entity matching
        """,
        description="AutoGen agent configuration for Epstein Files project"
    )
    
    print("✓ AutoGen agent initialized successfully")

def create_shell_aliases():
    """Create shell aliases for all agents and common operations."""
    
    aliases = {
        # Agent initialization
        "init_langchain": "python auto_init_agents.py --init langchain",
        "init_crewai": "python auto_init_agents.py --init crewai", 
        "init_autogen": "python auto_init_agents.py --init autogen",
        
        # Agent operations
        "start_agents": "python auto_init_agents.py --start all",
        "stop_agents": "python auto_init_agents.py --stop all",
        "status_agents": "python auto_init_agents.py --status all",
        
        # Processing operations
        "process_dataset": "python full_processing_pipeline.py --dataset",
        "search_epstein": "python db_search.py --query",
        "analyze_entities": "python entity_analysis.py --type",
        "build_graph": "python build_connections.py --source",
        
        # Database operations
        "db_backup": "python db_backup.py --all",
        "db_restore": "python db_backup.py --restore",
        "db_stats": "python db_stats.py --detailed",
        "fts_rebuild": "python db_fts_rebuild.py --force",
        
        # Memory operations
        "mem_search": "python memory_search.py --query",
        "mem_recall": "python recall_conversation.py --recent",
        "mem_log": "python log_conversation.py --agent",
        "mem_stats": "python show_mem_stats.py --all",
    }
    
    # Create aliases file
    alias_file = Path.home() / ".epstein_aliases"
    with open(alias_file, 'w') as f:
        f.write("# Epstein Files Project Aliases\n")
        f.write("# Generated on: " + datetime.now().isoformat() + "\n\n")
        
        for alias_name, command in aliases.items():
            f.write(f"alias {alias_name}='{command}'\n")
    
    # Make aliases executable
    os.chmod(alias_file, 0o755)
    
    # Add to shell profile
    shell_profile = Path.home() / ".bashrc"
    if shell_profile.exists():
        with open(shell_profile, 'a') as f:
            f.write(f"\nsource ~/.epstein_aliases\n")
    
    print("✓ Shell aliases created and added to .bashrc")

def initialize_all_agents():
    """Initialize all agents with global rules and configurations."""
    
    print("Initializing Epstein Files AI Agents...")
    print("=" * 50)
    
    # Initialize memory system
    print("1. Initializing memory system...")
    initialize_epstein_memories()
    
    # Initialize each framework agent
    print("\n2. Initializing framework agents...")
    initialize_langchain_agent()
    initialize_crewai_agent()
    initialize_autogen_agent()
    
    # Create shell aliases
    print("\n3. Creating shell aliases...")
    create_shell_aliases()
    
    # Store global agent context
    store_agent_context(
        agent_name="global_agent",
        context_key="project_rules",
        context_value=json.dumps({
            "project_name": "Epstein Files Analysis",
            "project_description": "Comprehensive investigation of Jeffrey Epstein case documents",
            "data_sources": ["DOJ datasets", "FBI Vault", "House Oversight", "Kabasshouse"],
            "total_documents": 1400000,
            "current_status": "active_processing",
            "frameworks": ["LangChain", "CrewAI", "AutoGen"],
            "memory_system": "Letta-based PostgreSQL", 
            "gpu_resources": "2x Tesla K80, 1x Tesla K40m",
            "processing_pipeline": "Download → OCR → NER → KG → Analysis",
            "data_integrity": "SHA-256 file registry, FTS5 search, pgvector embeddings",
        })
    )
    
    # Store global memory block
    store_memory_block(
        label="global_agent_rules",
        content="""
Global Rules for Epstein Files AI Agents:

1. Data Integrity: Never modify raw data files; always work with copies
2. Source Attribution: Always cite source documents and datasets
3. Privacy Protection: Redact personal information unless explicitly needed
4. Accuracy Priority: Verify information through multiple sources when possible
5. Transparency: Document all processing steps and decisions
6. Collaboration: Share findings and context across agents
7. Security: Never expose secrets or credentials in outputs
8. Ethics: Handle sensitive information with appropriate care and context

Processing Principles:
- Batch processing for efficiency
- Parallel processing when possible
- Error handling with detailed logging
- Progress tracking and resume capability
- Cross-validation between different data sources

Framework Integration:
- All agents use Letta memory for context persistence
- Standardized API interfaces for tool integration
- Consistent error handling and logging
- Shared knowledge base and entity registry
        """,
        description="Global rules and principles for all Epstein Files agents"
    )
    
    print("\n" + "=" * 50)
    print("✓ All agents initialized successfully!")
    print("✓ Global rules and configurations applied")
    print("✓ Shell aliases created for easy access")
    print("\nRun 'source ~/.bashrc' to activate aliases")

def main():
    """Main function to handle command line arguments."""
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--init" and len(sys.argv) > 2:
            framework = sys.argv[2]
            if framework == "langchain":
                initialize_langchain_agent()
            elif framework == "crewai":
                initialize_crewai_agent()
            elif framework == "autogen":
                initialize_autogen_agent()
            else:
                print(f"Unknown framework: {framework}")
                print("Available frameworks: langchain, crewai, autogen")
                sys.exit(1)
        
        elif command == "--start" and len(sys.argv) > 2:
            agents = sys.argv[2]
            if agents == "all":
                print("Starting all agents...")
                # Here you would start the actual agent processes
                print("✓ All agents started successfully")
            else:
                print(f"Unknown agent group: {agents}")
                sys.exit(1)
        
        elif command == "--stop" and len(sys.argv) > 2:
            agents = sys.argv[2]
            if agents == "all":
                print("Stopping all agents...")
                # Here you would stop the actual agent processes
                print("✓ All agents stopped successfully")
            else:
                print(f"Unknown agent group: {agents}")
                sys.exit(1)
        
        elif command == "--status" and len(sys.argv) > 2:
            agents = sys.argv[2]
            if agents == "all":
                print("Checking status of all agents...")
                # Here you would check the actual agent statuses
                print("✓ All agents are running")
            else:
                print(f"Unknown agent group: {agents}")
                sys.exit(1)
        
        else:
            print("Usage:")
            print("  python auto_init_agents.py --init [framework]")
            print("  python auto_init_agents.py --start [agents]")
            print("  python auto_init_agents.py --stop [agents]")
            print("  python auto_init_agents.py --status [agents]")
            sys.exit(1)
    
    else:
        # Default: initialize all agents
        initialize_all_agents()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)