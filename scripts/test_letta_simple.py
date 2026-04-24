#!/usr/bin/env python3
"""
Simple test to add a memory to Letta using the Python SDK.
Based on Letta skills documentation.
"""

import sys

from letta_client import Letta

# Letta server configuration
LETTA_BASE_URL = "http://localhost:8283"
LETTA_API_KEY = "123qweasd"  # Server password as API key per Letta docs


def test_connection():
    """Test connection to Letta server."""
    print("Testing Letta server connection...")
    try:
        client = Letta(base_url=LETTA_BASE_URL, api_key=LETTA_API_KEY)
        print("  ✓ Connected successfully")
        return client
    except Exception as e:
        print(f"  ✗ Connection failed: {e}")
        return None


def list_agents(client):
    """List existing agents."""
    print("\nListing existing agents...")
    try:
        agents_page = client.agents.list()
        # Handle paginated response
        agents = list(agents_page)
        print(f"  Found {len(agents)} agents")
        for agent in agents:
            print(f"    - {agent.name} (ID: {agent.id})")
        return agents
    except Exception as e:
        print(f"  ✗ Failed to list agents: {e}")
        return []


def main():
    """Main test function."""
    print("=== Simple Letta Memory Test ===\n")

    # Test connection
    client = test_connection()
    if not client:
        sys.exit(1)

    # List existing agents
    agents = list_agents(client)

    # Create a new agent with correct OpenRouter configuration
    print("\nCreating new agent with OpenRouter configuration...")
    try:
        new_agent = client.agents.create(
            name="openrouter-test-agent",
            description="Test agent with OpenRouter configuration",
            llm_config={
                "model": "OpenRouter/nvidia/nemotron-3-super-120b-a12b:free",  # Use free 120B model
                "model_endpoint_type": "openrouter",  # Use openrouter endpoint type
                "context_window": 131072,  # Large context window for 120B model
            },
            memory_blocks=[
                {
                    "label": "persona",
                    "value": "You are a helpful test agent using OpenRouter.",
                    "limit": 1000,
                    "description": "Agent personality",
                }
            ],
        )
        print(f"  ✓ Created new agent: {new_agent.name} (ID: {new_agent.id})")
        test_agent = new_agent
    except Exception as e:
        print(f"  ✗ Failed to create agent: {e}")
        sys.exit(1)

    # Test adding a simple message to the agent
    print("\nTesting message insertion...")
    try:
        response = client.agents.messages.create(
            agent_id=test_agent.id,
            messages=[{"role": "user", "content": "Test message: This is a simple test memory."}],
        )
        print("  ✓ Message sent successfully")
    except Exception as e:
        print(f"  ✗ Failed to send message: {e}")

    print("\n=== Test Complete ===")


if __name__ == "__main__":
    main()
