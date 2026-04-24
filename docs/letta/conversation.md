


Please complete the payment process to use Enterprise features
can you help me create a document that has instructions on how to deploy and use letta memory system on a bare metal postgresql database called letta. i need help starting, setting up and using the letta tools and features as well. we need to make skills as wlel for windsurf to make memories and all of the features
Completed 4 steps





letta_bare_metal_postgres_windsurf_guide
Document
letta_bare_metal_postgres_windsurf_guide
Letta on Bare-Metal PostgreSQL (letta) with Windsurf Memory/Skills
This guide explains how to deploy a self-hosted Letta server against an existing bare-metal PostgreSQL database named letta, how to start and configure the service, how to use Letta memory blocks, CLI tools, and memfs features, and how to create Windsurf memories and skills that work well with a Letta-backed workflow.

Target architecture
The recommended setup is a Letta server running in Docker while PostgreSQL runs outside Docker on bare metal, with Letta connecting to Postgres through LETTA_PG_URI.
 Letta requires the pgvector extension in the target database because agent memory and related state are stored in PostgreSQL with vector support.

Prerequisites
Prepare the following before deployment:

A reachable PostgreSQL instance with a database named letta.

A PostgreSQL role dedicated to Letta, ideally with ownership of the letta database.

pgvector installed and enabled in that database.

Docker installed on the Letta host, because the documented self-hosting path runs the Letta server in a container.

At least one model provider configuration, such as OpenAI or another supported provider, because the server still needs an LLM backend after startup.

PostgreSQL setup
Create the database and role if they do not already exist, then enable pgvector inside letta.

sql
CREATE DATABASE letta;
CREATE USER letta_user WITH PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE letta TO letta_user;
\c letta
CREATE EXTENSION IF NOT EXISTS vector;
If PostgreSQL is on another host, ensure postgresql.conf and pg_hba.conf allow the Letta server to connect on port 5432 from the Letta machine.
 Use a strong password and prefer a dedicated database role rather than reusing a superuser account.

Environment file
Create a .env file for the Letta server so connection details and provider keys are not embedded in the Docker command.

text
LETTA_PG_URI=postgresql://letta_user:change-this-password@POSTGRES_HOST:5432/letta
OPENAI_API_KEY=replace-me
LETTA_DEBUG=1
For a local bare-metal PostgreSQL server running on the same Linux host as Docker, replace POSTGRES_HOST with the host address reachable from the container, often the machine IP or another routable interface instead of assuming localhost will work inside the container.

Starting Letta
The documented Docker guide shows Letta server deployment through docker run, and it supports connecting to an external PostgreSQL instance by setting LETTA_PG_URI.
 A practical starting command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
After startup, Letta should connect to PostgreSQL, initialize its schema, and expose the API on port 8283 unless overridden.
 Set LETTA_BASE_URL=http://YOUR_HOST:8283 in clients such as Letta Code when using the self-hosted server.

First-run checks
Validate the deployment with these checks:

Confirm the container is running: docker ps.

Confirm PostgreSQL connectivity from the host or container using the same connection string.

Confirm vector exists: SELECT extname FROM pg_extension WHERE extname = 'vector';.

Confirm your client points at the server with LETTA_BASE_URL.

If the server fails early, the most common causes are missing pgvector, bad network routing to PostgreSQL, or an invalid database URI.

Letta Code installation
Letta Code is the CLI entry point for working with agents, memory, conversations, memfs, and skills-related workflows.
 Its basic usage includes resuming default sessions, creating new agents, selecting models, and pointing at a self-hosted server with LETTA_BASE_URL.

Common environment variables for CLI use:

bash
export LETTA_BASE_URL=http://YOUR_HOST:8283
export LETTA_DEBUG=1
export DISABLE_AUTOUPDATER=1
Then start a session with:

bash
letta
or create a new agent session with:

bash
letta --new-agent
The CLI also supports explicit model and system configuration flags such as --model, --embedding, --system, --skills, and --toolset.

Creating a useful agent
Letta supports preset and custom memory blocks during agent creation through flags such as --init-blocks, --memory-blocks, --block-value, and --memfs.
 Memory blocks are core memory sections that persist across interactions and are always visible in the context window, so they are the right place for persona, project facts, operating rules, and long-lived task state.

Example:

bash
letta --new-agent \
  --model sonnet \
  --init-blocks persona,project \
  --block-value persona="You are an engineering assistant for homelab and AI infra tasks." \
  --block-value project="Current project: deploy and operate Letta with PostgreSQL and Windsurf." \
  --memfs
This creates an agent with persistent core memory blocks and enables the Memory Filesystem feature for file-oriented state.

Memory blocks
Memory blocks are structured, persistent sections of an agent’s context window that Letta automatically manages, and agents can read and update them using built-in memory tools.
 Blocks can be read-write or marked read-only, and they can also be attached to multiple agents to provide shared memory.

Recommended block layout for an engineering assistant:

Block	Purpose
persona	Stable behavior, role, tone, and operating constraints.
project	Current system architecture, hosts, services, repos, and environment notes.
runbook	Deployment facts, commands, and troubleshooting conventions.
scratchpad	Working notes the agent may revise frequently.
policies	Read-only compliance, guardrails, or organization rules.
For shared teams or multi-agent setups, create blocks once and attach them to several agents so they all see the same evolving context.

Managing memory from the CLI
Letta exposes JSON-oriented subcommands to inspect and manipulate agents, messages, memfs, and blocks.
 Important commands include letta agents list, letta blocks list --agent <id>, letta blocks attach --block-id <id>, and letta messages search --query <text>.

Useful examples:

bash
letta agents list
letta blocks list --agent AGENT_ID
letta blocks attach --block-id BLOCK_ID --agent AGENT_ID
letta messages search --query "postgres pgvector" --agent AGENT_ID
letta memfs status --agent AGENT_ID
letta memfs export --agent AGENT_ID --out ./agent_memfs_export
These commands are useful for auditing what the agent knows, exporting file-backed memory, and reusing blocks across agents.

MemFS usage
Letta Code supports a Memory Filesystem feature enabled with --memfs, along with commands for status, diff, resolve, backup, restore, and export.
 The Docker deployment guide also notes that full git sync requires a sidecar implementing Git smart HTTP and the LETTA_MEMFS_SERVICE_URL environment variable if you want proxied /v1/git/ integration.

A safe workflow for memfs-enabled agents is:

Create the agent with --memfs.

Check sync state with letta memfs status --agent AGENT_ID.

Review conflicts with letta memfs diff --agent AGENT_ID.

Back up important state with letta memfs backup --agent AGENT_ID before destructive changes.

If using git-backed sync, add the sidecar and LETTA_MEMFS_SERVICE_URL later rather than on day one.

Starting to use Letta day to day
A practical daily workflow is to create one agent per major domain, pin stable instructions into memory blocks, and keep project-specific state in project, runbook, and scratchpad blocks.
 Search past messages when needed, export memfs snapshots before major refactors, and use shared blocks when multiple agents need a common operational memory.

A good first pattern is:

One infra agent for homelab, Docker, PostgreSQL, and observability.

One coding agent per repository or stack.

One shared read-only policies block for standards and constraints.

One shared mutable team-context block for current milestones and incidents.

Windsurf memories
Windsurf supports persisted memories and rules at global and workspace levels, and its docs recommend keeping rules simple, concise, specific, and structured with markdown lists rather than long vague paragraphs.
 Windsurf memories are a good place to define how Cascade should capture or update Letta-relevant facts during development work.

Suggested Windsurf memory rules:

text
- When infrastructure, environment variables, ports, hosts, database names, or deployment commands change, summarize the final state clearly.
- When a deployment task finishes, propose a concise memory update covering what was changed, where it runs, and how to verify it.
- Prefer durable facts over temporary debugging noise.
- Separate workspace-specific memories from global habits.
- When a fact belongs in long-term agent context, suggest adding it to the appropriate Letta memory block.
This keeps Windsurf from storing noisy implementation details while still preserving deployable system knowledge.

Windsurf skills
Windsurf skills can be created through the UI or manually by creating .windsurf/skills/<skill-name>/SKILL.md for a workspace skill, or ~/.codeium/windsurf/skills/<skill-name>/SKILL.md for a global one.
 The docs recommend clear descriptions and useful supporting resources so Cascade can decide when to invoke the skill.

Recommended skills for a Letta workflow:

Skill name	Use
letta-memory-update	Turns finished work into candidate Letta memory block updates.
letta-deploy-runbook	Generates deployment and troubleshooting steps for Letta server changes.
letta-block-design	Suggests memory block schemas for new agents or projects.
windsurf-memory-hygiene	Filters temporary chatter from durable rules and memories.
Example Windsurf skill
Create .windsurf/skills/letta-memory-update/SKILL.md with content like this:

text
---
name: letta-memory-update
description: Generate concise, durable Letta memory updates after infrastructure, coding, or deployment work. Use this skill when a task changes system facts, runbooks, environment variables, ports, agents, or database configuration.
---

# Letta Memory Update

When invoked, produce:

1. A short summary of the durable change.
2. The recommended Letta block target (`persona`, `project`, `runbook`, `scratchpad`, or another named block).
3. A proposed memory entry written as plain text.
4. A note on whether the item should be read-only, shared, or agent-local.
5. A verification command if relevant.

Rules:
- Prefer facts that will still matter next week.
- Exclude transient logs, stack traces, and one-off debugging attempts.
- Normalize ports, URLs, hostnames, service names, and env vars.
- If the change affects deployment, include rollback or verification notes.
This skill gives Windsurf a consistent pattern for turning completed work into memory-ready artifacts.

Suggested Windsurf support files
Attach supporting resources to each skill so the output stays consistent.
 Useful companion files include:

examples/good-memory-updates.md with several before/after examples.

templates/letta-block-template.md with standard fields for persona, project, runbook, and scratchpad.

checklists/deploy-verification.md with health checks for Letta, PostgreSQL, and memfs workflows.

Example Letta block templates
Use a simple schema so memory remains easy to maintain.

project
text
Project: Letta self-hosting
Server URL: http://YOUR_HOST:8283
Database: postgresql://letta_user@POSTGRES_HOST:5432/letta
Key requirements: pgvector enabled, Docker runtime, provider keys configured
Primary verification: docker ps; psql extension check; CLI connection test
runbook
text
Start server: docker run -d --name letta --restart unless-stopped --env-file .env -p 8283:8283 letta/letta:latest
Verify database: SELECT extname FROM pg_extension WHERE extname = 'vector';
Client base URL: export LETTA_BASE_URL=http://YOUR_HOST:8283
Memfs backup: letta memfs backup --agent AGENT_ID
policies
text
Do not store secrets directly in memory blocks.
Prefer environment variables or vault-backed secret storage.
Use shared blocks only for information safe to expose to every attached agent.
Recommended rollout plan
Use a staged rollout so the memory model stays manageable.

Deploy Letta against the letta PostgreSQL database with pgvector enabled.

Create one primary agent with persona, project, and runbook blocks.

Enable --memfs only after the base workflow is stable.

Add one shared read-only policies block and one shared mutable team context block.

Create Windsurf memories and the letta-memory-update skill to turn completed work into durable memory suggestions.

Later, add git-backed memfs sidecar support only if that workflow is clearly needed.

Common pitfalls
The highest-risk setup issues are missing pgvector, using a container-local localhost for PostgreSQL, and mixing temporary debugging notes into long-term memory blocks.
 Another common design mistake is making every block mutable; read-only blocks are better for policies and canonical facts that should not drift during ordinary agent operation.

Next build targets
After the base deployment works, the next useful artifacts are a repo-local .windsurf/skills/ directory, a standardized block taxonomy, and a lightweight operational script set for creating agents, listing blocks, backing up memfs, and exporting agent state.
 That combination gives a repeatable foundation for using Letta as a long-term memory layer while Windsurf handles development-time guidance and memory capture.

Letta on Bare-Metal PostgreSQL (letta) with Windsurf Memory/Skills
This guide explains how to deploy a self-hosted Letta server against an existing bare-metal PostgreSQL database named letta, how to start and configure the service, how to use Letta memory blocks, CLI tools, and memfs features, and how to create Windsurf memories and skills that work well with a Letta-backed workflow.

Target architecture
The recommended setup is a Letta server running in Docker while PostgreSQL runs outside Docker on bare metal, with Letta connecting to Postgres through LETTA_PG_URI. Letta requires the pgvector extension in the target database because agent memory and related state are stored in PostgreSQL with vector support.

Prerequisites
Prepare the following before deployment:

A reachable PostgreSQL instance with a database named letta.

A PostgreSQL role dedicated to Letta, ideally with ownership of the letta database.

pgvector installed and enabled in that database.

Docker installed on the Letta host, because the documented self-hosting path runs the Letta server in a container.

At least one model provider configuration, such as OpenAI or another supported provider, because the server still needs an LLM backend after startup.

PostgreSQL setup
Create the database and role if they do not already exist, then enable pgvector inside letta.

sql
CREATE DATABASE letta;
CREATE USER letta_user WITH PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE letta TO letta_user;
\c letta
CREATE EXTENSION IF NOT EXISTS vector;
If PostgreSQL is on another host, ensure postgresql.conf and pg_hba.conf allow the Letta server to connect on port 5432 from the Letta machine. Use a strong password and prefer a dedicated database role rather than reusing a superuser account.

Environment file
Create a .env file for the Letta server so connection details and provider keys are not embedded in the Docker command.

text
LETTA_PG_URI=postgresql://letta_user:change-this-password@POSTGRES_HOST:5432/letta
OPENAI_API_KEY=replace-me
LETTA_DEBUG=1
For a local bare-metal PostgreSQL server running on the same Linux host as Docker, replace POSTGRES_HOST with the host address reachable from the container, often the machine IP or another routable interface instead of assuming localhost will work inside the container.

Starting Letta
The documented Docker guide shows Letta server deployment through docker run, and it supports connecting to an external PostgreSQL instance by setting LETTA_PG_URI. A practical starting command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
After startup, Letta should connect to PostgreSQL, initialize its schema, and expose the API on port 8283 unless overridden. Set LETTA_BASE_URL=http://YOUR_HOST:8283 in clients such as Letta Code when using the self-hosted server.

First-run checks
Validate the deployment with these checks:

Confirm the container is running: docker ps.

Confirm PostgreSQL connectivity from the host or container using the same connection string.

Confirm vector exists: SELECT extname FROM pg_extension WHERE extname = 'vector';.

Confirm your client points at the server with LETTA_BASE_URL.

If the server fails early, the most common causes are missing pgvector, bad network routing to PostgreSQL, or an invalid database URI.

Letta Code installation
Letta Code is the CLI entry point for working with agents, memory, conversations, memfs, and skills-related workflows. Its basic usage includes resuming default sessions, creating new agents, selecting models, and pointing at a self-hosted server with LETTA_BASE_URL.

Common environment variables for CLI use:

bash
export LETTA_BASE_URL=http://YOUR_HOST:8283
export LETTA_DEBUG=1
export DISABLE_AUTOUPDATER=1
Then start a session with:

bash
letta
or create a new agent session with:

bash
letta --new-agent
The CLI also supports explicit model and system configuration flags such as --model, --embedding, --system, --skills, and --toolset.

Creating a useful agent
Letta supports preset and custom memory blocks during agent creation through flags such as --init-blocks, --memory-blocks, --block-value, and --memfs. Memory blocks are core memory sections that persist across interactions and are always visible in the context window, so they are the right place for persona, project facts, operating rules, and long-lived task state.

Example:

bash
letta --new-agent \
  --model sonnet \
  --init-blocks persona,project \
  --block-value persona="You are an engineering assistant for homelab and AI infra tasks." \
  --block-value project="Current project: deploy and operate Letta with PostgreSQL and Windsurf." \
  --memfs
This creates an agent with persistent core memory blocks and enables the Memory Filesystem feature for file-oriented state.

Memory blocks
Memory blocks are structured, persistent sections of an agent’s context window that Letta automatically manages, and agents can read and update them using built-in memory tools. Blocks can be read-write or marked read-only, and they can also be attached to multiple agents to provide shared memory.

Recommended block layout for an engineering assistant:

Block	Purpose
persona	Stable behavior, role, tone, and operating constraints.
project	Current system architecture, hosts, services, repos, and environment notes.
runbook	Deployment facts, commands, and troubleshooting conventions.
scratchpad	Working notes the agent may revise frequently.
policies	Read-only compliance, guardrails, or organization rules.
For shared teams or multi-agent setups, create blocks once and attach them to several agents so they all see the same evolving context.

Managing memory from the CLI
Letta exposes JSON-oriented subcommands to inspect and manipulate agents, messages, memfs, and blocks. Important commands include letta agents list, letta blocks list --agent <id>, letta blocks attach --block-id <id>, and letta messages search --query <text>.

Useful examples:

bash
letta agents list
letta blocks list --agent AGENT_ID
letta blocks attach --block-id BLOCK_ID --agent AGENT_ID
letta messages search --query "postgres pgvector" --agent AGENT_ID
letta memfs status --agent AGENT_ID
letta memfs export --agent AGENT_ID --out ./agent_memfs_export
These commands are useful for auditing what the agent knows, exporting file-backed memory, and reusing blocks across agents.

MemFS usage
Letta Code supports a Memory Filesystem feature enabled with --memfs, along with commands for status, diff, resolve, backup, restore, and export. The Docker deployment guide also notes that full git sync requires a sidecar implementing Git smart HTTP and the LETTA_MEMFS_SERVICE_URL environment variable if you want proxied /v1/git/ integration.

A safe workflow for memfs-enabled agents is:

Create the agent with --memfs.

Check sync state with letta memfs status --agent AGENT_ID.

Review conflicts with letta memfs diff --agent AGENT_ID.

Back up important state with letta memfs backup --agent AGENT_ID before destructive changes.

If using git-backed sync, add the sidecar and LETTA_MEMFS_SERVICE_URL later rather than on day one.

Starting to use Letta day to day
A practical daily workflow is to create one agent per major domain, pin stable instructions into memory blocks, and keep project-specific state in project, runbook, and scratchpad blocks. Search past messages when needed, export memfs snapshots before major refactors, and use shared blocks when multiple agents need a common operational memory.

A good first pattern is:

One infra agent for homelab, Docker, PostgreSQL, and observability.

One coding agent per repository or stack.

One shared read-only policies block for standards and constraints.

One shared mutable team-context block for current milestones and incidents.

Windsurf memories
Windsurf supports persisted memories and rules at global and workspace levels, and its docs recommend keeping rules simple, concise, specific, and structured with markdown lists rather than long vague paragraphs. Windsurf memories are a good place to define how Cascade should capture or update Letta-relevant facts during development work.

Suggested Windsurf memory rules:

text
- When infrastructure, environment variables, ports, hosts, database names, or deployment commands change, summarize the final state clearly.
- When a deployment task finishes, propose a concise memory update covering what was changed, where it runs, and how to verify it.
- Prefer durable facts over temporary debugging noise.
- Separate workspace-specific memories from global habits.
- When a fact belongs in long-term agent context, suggest adding it to the appropriate Letta memory block.
This keeps Windsurf from storing noisy implementation details while still preserving deployable system knowledge.

Windsurf skills
Windsurf skills can be created through the UI or manually by creating .windsurf/skills/<skill-name>/SKILL.md for a workspace skill, or ~/.codeium/windsurf/skills/<skill-name>/SKILL.md for a global one. The docs recommend clear descriptions and useful supporting resources so Cascade can decide when to invoke the skill.

Recommended skills for a Letta workflow:

Skill name	Use
letta-memory-update	Turns finished work into candidate Letta memory block updates.
letta-deploy-runbook	Generates deployment and troubleshooting steps for Letta server changes.
letta-block-design	Suggests memory block schemas for new agents or projects.
windsurf-memory-hygiene	Filters temporary chatter from durable rules and memories.
Example Windsurf skill
Create .windsurf/skills/letta-memory-update/SKILL.md with content like this:

text
---
name: letta-memory-update
description: Generate concise, durable Letta memory updates after infrastructure, coding, or deployment work. Use this skill when a task changes system facts, runbooks, environment variables, ports, agents, or database configuration.
---

# Letta Memory Update

When invoked, produce:

1. A short summary of the durable change.
2. The recommended Letta block target (`persona`, `project`, `runbook`, `scratchpad`, or another named block).
3. A proposed memory entry written as plain text.
4. A note on whether the item should be read-only, shared, or agent-local.
5. A verification command if relevant.

Rules:
- Prefer facts that will still matter next week.
- Exclude transient logs, stack traces, and one-off debugging attempts.
- Normalize ports, URLs, hostnames, service names, and env vars.
- If the change affects deployment, include rollback or verification notes.
This skill gives Windsurf a consistent pattern for turning completed work into memory-ready artifacts.

Suggested Windsurf support files
Attach supporting resources to each skill so the output stays consistent. Useful companion files include:

examples/good-memory-updates.md with several before/after examples.

templates/letta-block-template.md with standard fields for persona, project, runbook, and scratchpad.

checklists/deploy-verification.md with health checks for Letta, PostgreSQL, and memfs workflows.

Example Letta block templates
Use a simple schema so memory remains easy to maintain.

project
text
Project: Letta self-hosting
Server URL: http://YOUR_HOST:8283
Database: postgresql://letta_user@POSTGRES_HOST:5432/letta
Key requirements: pgvector enabled, Docker runtime, provider keys configured
Primary verification: docker ps; psql extension check; CLI connection test
runbook
text
Start server: docker run -d --name letta --restart unless-stopped --env-file .env -p 8283:8283 letta/letta:latest
Verify database: SELECT extname FROM pg_extension WHERE extname = 'vector';
Client base URL: export LETTA_BASE_URL=http://YOUR_HOST:8283
Memfs backup: letta memfs backup --agent AGENT_ID
policies
text
Do not store secrets directly in memory blocks.
Prefer environment variables or vault-backed secret storage.
Use shared blocks only for information safe to expose to every attached agent.
Recommended rollout plan
Use a staged rollout so the memory model stays manageable.

Deploy Letta against the letta PostgreSQL database with pgvector enabled.

Create one primary agent with persona, project, and runbook blocks.

Enable --memfs only after the base workflow is stable.

Add one shared read-only policies block and one shared mutable team context block.

Create Windsurf memories and the letta-memory-update skill to turn completed work into durable memory suggestions.

Later, add git-backed memfs sidecar support only if that workflow is clearly needed.

Common pitfalls
The highest-risk setup issues are missing pgvector, using a container-local localhost for PostgreSQL, and mixing temporary debugging notes into long-term memory blocks. Another common design mistake is making every block mutable; read-only blocks are better for policies and canonical facts that should not drift during ordinary agent operation.

Next build targets
After the base deployment works, the next useful artifacts are a repo-local .windsurf/skills/ directory, a standardized block taxonomy, and a lightweight operational script set for creating agents, listing blocks, backing up memfs, and exporting agent state. That combination gives a repeatable foundation for using Letta as a long-term memory layer while Windsurf handles development-time guidance and memory capture.

we also need to use openrouter free models if there are any needs for agents
Completed 4 steps





letta_bare_metal_postgres_windsurf_guide
Document
letta_bare_metal_postgres_windsurf_guide
Letta on Bare-Metal PostgreSQL (letta) with Windsurf Memory/Skills
This guide explains how to deploy a self-hosted Letta server against an existing bare-metal PostgreSQL database named letta, how to start and configure the service, how to use Letta memory blocks, CLI tools, and memfs features, and how to create Windsurf memories and skills that work well with a Letta-backed workflow.

Target architecture
The recommended setup is a Letta server running in Docker while PostgreSQL runs outside Docker on bare metal, with Letta connecting to Postgres through LETTA_PG_URI.
 Letta requires the pgvector extension in the target database because agent memory and related state are stored in PostgreSQL with vector support.

Prerequisites
Prepare the following before deployment:

A reachable PostgreSQL instance with a database named letta.

A PostgreSQL role dedicated to Letta, ideally with ownership of the letta database.

pgvector installed and enabled in that database.

Docker installed on the Letta host, because the documented self-hosting path runs the Letta server in a container.

At least one model provider configuration, such as OpenAI or another supported provider, because the server still needs an LLM backend after startup.

PostgreSQL setup
Create the database and role if they do not already exist, then enable pgvector inside letta.

sql
CREATE DATABASE letta;
CREATE USER letta_user WITH PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE letta TO letta_user;
\c letta
CREATE EXTENSION IF NOT EXISTS vector;
If PostgreSQL is on another host, ensure postgresql.conf and pg_hba.conf allow the Letta server to connect on port 5432 from the Letta machine.
 Use a strong password and prefer a dedicated database role rather than reusing a superuser account.

Environment file
Create a .env file for the Letta server so connection details and provider keys are not embedded in the Docker command.

text
LETTA_PG_URI=postgresql://letta_user:change-this-password@POSTGRES_HOST:5432/letta
OPENAI_API_KEY=replace-me
LETTA_DEBUG=1
For a local bare-metal PostgreSQL server running on the same Linux host as Docker, replace POSTGRES_HOST with the host address reachable from the container, often the machine IP or another routable interface instead of assuming localhost will work inside the container.

Starting Letta
The documented Docker guide shows Letta server deployment through docker run, and it supports connecting to an external PostgreSQL instance by setting LETTA_PG_URI.
 A practical starting command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
After startup, Letta should connect to PostgreSQL, initialize its schema, and expose the API on port 8283 unless overridden.
 Set LETTA_BASE_URL=http://YOUR_HOST:8283 in clients such as Letta Code when using the self-hosted server.

First-run checks
Validate the deployment with these checks:

Confirm the container is running: docker ps.

Confirm PostgreSQL connectivity from the host or container using the same connection string.

Confirm vector exists: SELECT extname FROM pg_extension WHERE extname = 'vector';.

Confirm your client points at the server with LETTA_BASE_URL.

If the server fails early, the most common causes are missing pgvector, bad network routing to PostgreSQL, or an invalid database URI.

Letta Code installation
Letta Code is the CLI entry point for working with agents, memory, conversations, memfs, and skills-related workflows.
 Its basic usage includes resuming default sessions, creating new agents, selecting models, and pointing at a self-hosted server with LETTA_BASE_URL.

Common environment variables for CLI use:

bash
export LETTA_BASE_URL=http://YOUR_HOST:8283
export LETTA_DEBUG=1
export DISABLE_AUTOUPDATER=1
Then start a session with:

bash
letta
or create a new agent session with:

bash
letta --new-agent
The CLI also supports explicit model and system configuration flags such as --model, --embedding, --system, --skills, and --toolset.

Creating a useful agent
Letta supports preset and custom memory blocks during agent creation through flags such as --init-blocks, --memory-blocks, --block-value, and --memfs.
 Memory blocks are core memory sections that persist across interactions and are always visible in the context window, so they are the right place for persona, project facts, operating rules, and long-lived task state.

Example:

bash
letta --new-agent \
  --model sonnet \
  --init-blocks persona,project \
  --block-value persona="You are an engineering assistant for homelab and AI infra tasks." \
  --block-value project="Current project: deploy and operate Letta with PostgreSQL and Windsurf." \
  --memfs
This creates an agent with persistent core memory blocks and enables the Memory Filesystem feature for file-oriented state.

Memory blocks
Memory blocks are structured, persistent sections of an agent’s context window that Letta automatically manages, and agents can read and update them using built-in memory tools.
 Blocks can be read-write or marked read-only, and they can also be attached to multiple agents to provide shared memory.

Recommended block layout for an engineering assistant:

Block	Purpose
persona	Stable behavior, role, tone, and operating constraints.
project	Current system architecture, hosts, services, repos, and environment notes.
runbook	Deployment facts, commands, and troubleshooting conventions.
scratchpad	Working notes the agent may revise frequently.
policies	Read-only compliance, guardrails, or organization rules.
For shared teams or multi-agent setups, create blocks once and attach them to several agents so they all see the same evolving context.

Managing memory from the CLI
Letta exposes JSON-oriented subcommands to inspect and manipulate agents, messages, memfs, and blocks.
 Important commands include letta agents list, letta blocks list --agent <id>, letta blocks attach --block-id <id>, and letta messages search --query <text>.

Useful examples:

bash
letta agents list
letta blocks list --agent AGENT_ID
letta blocks attach --block-id BLOCK_ID --agent AGENT_ID
letta messages search --query "postgres pgvector" --agent AGENT_ID
letta memfs status --agent AGENT_ID
letta memfs export --agent AGENT_ID --out ./agent_memfs_export
These commands are useful for auditing what the agent knows, exporting file-backed memory, and reusing blocks across agents.

MemFS usage
Letta Code supports a Memory Filesystem feature enabled with --memfs, along with commands for status, diff, resolve, backup, restore, and export.
 The Docker deployment guide also notes that full git sync requires a sidecar implementing Git smart HTTP and the LETTA_MEMFS_SERVICE_URL environment variable if you want proxied /v1/git/ integration.

A safe workflow for memfs-enabled agents is:

Create the agent with --memfs.

Check sync state with letta memfs status --agent AGENT_ID.

Review conflicts with letta memfs diff --agent AGENT_ID.

Back up important state with letta memfs backup --agent AGENT_ID before destructive changes.

If using git-backed sync, add the sidecar and LETTA_MEMFS_SERVICE_URL later rather than on day one.

Starting to use Letta day to day
A practical daily workflow is to create one agent per major domain, pin stable instructions into memory blocks, and keep project-specific state in project, runbook, and scratchpad blocks.
 Search past messages when needed, export memfs snapshots before major refactors, and use shared blocks when multiple agents need a common operational memory.

A good first pattern is:

One infra agent for homelab, Docker, PostgreSQL, and observability.

One coding agent per repository or stack.

One shared read-only policies block for standards and constraints.

One shared mutable team-context block for current milestones and incidents.

Windsurf memories
Windsurf supports persisted memories and rules at global and workspace levels, and its docs recommend keeping rules simple, concise, specific, and structured with markdown lists rather than long vague paragraphs.
 Windsurf memories are a good place to define how Cascade should capture or update Letta-relevant facts during development work.

Suggested Windsurf memory rules:

text
- When infrastructure, environment variables, ports, hosts, database names, or deployment commands change, summarize the final state clearly.
- When a deployment task finishes, propose a concise memory update covering what was changed, where it runs, and how to verify it.
- Prefer durable facts over temporary debugging noise.
- Separate workspace-specific memories from global habits.
- When a fact belongs in long-term agent context, suggest adding it to the appropriate Letta memory block.
This keeps Windsurf from storing noisy implementation details while still preserving deployable system knowledge.

Windsurf skills
Windsurf skills can be created through the UI or manually by creating .windsurf/skills/<skill-name>/SKILL.md for a workspace skill, or ~/.codeium/windsurf/skills/<skill-name>/SKILL.md for a global one.
 The docs recommend clear descriptions and useful supporting resources so Cascade can decide when to invoke the skill.

Recommended skills for a Letta workflow:

Skill name	Use
letta-memory-update	Turns finished work into candidate Letta memory block updates.
letta-deploy-runbook	Generates deployment and troubleshooting steps for Letta server changes.
letta-block-design	Suggests memory block schemas for new agents or projects.
windsurf-memory-hygiene	Filters temporary chatter from durable rules and memories.
Example Windsurf skill
Create .windsurf/skills/letta-memory-update/SKILL.md with content like this:

text
---
name: letta-memory-update
description: Generate concise, durable Letta memory updates after infrastructure, coding, or deployment work. Use this skill when a task changes system facts, runbooks, environment variables, ports, agents, or database configuration.
---

# Letta Memory Update

When invoked, produce:

1. A short summary of the durable change.
2. The recommended Letta block target (`persona`, `project`, `runbook`, `scratchpad`, or another named block).
3. A proposed memory entry written as plain text.
4. A note on whether the item should be read-only, shared, or agent-local.
5. A verification command if relevant.

Rules:
- Prefer facts that will still matter next week.
- Exclude transient logs, stack traces, and one-off debugging attempts.
- Normalize ports, URLs, hostnames, service names, and env vars.
- If the change affects deployment, include rollback or verification notes.
This skill gives Windsurf a consistent pattern for turning completed work into memory-ready artifacts.

Suggested Windsurf support files
Attach supporting resources to each skill so the output stays consistent.
 Useful companion files include:

examples/good-memory-updates.md with several before/after examples.

templates/letta-block-template.md with standard fields for persona, project, runbook, and scratchpad.

checklists/deploy-verification.md with health checks for Letta, PostgreSQL, and memfs workflows.

Example Letta block templates
Use a simple schema so memory remains easy to maintain.

project
text
Project: Letta self-hosting
Server URL: http://YOUR_HOST:8283
Database: postgresql://letta_user@POSTGRES_HOST:5432/letta
Key requirements: pgvector enabled, Docker runtime, provider keys configured
Primary verification: docker ps; psql extension check; CLI connection test
runbook
text
Start server: docker run -d --name letta --restart unless-stopped --env-file .env -p 8283:8283 letta/letta:latest
Verify database: SELECT extname FROM pg_extension WHERE extname = 'vector';
Client base URL: export LETTA_BASE_URL=http://YOUR_HOST:8283
Memfs backup: letta memfs backup --agent AGENT_ID
policies
text
Do not store secrets directly in memory blocks.
Prefer environment variables or vault-backed secret storage.
Use shared blocks only for information safe to expose to every attached agent.
Recommended rollout plan
Use a staged rollout so the memory model stays manageable.

Deploy Letta against the letta PostgreSQL database with pgvector enabled.

Create one primary agent with persona, project, and runbook blocks.

Enable --memfs only after the base workflow is stable.

Add one shared read-only policies block and one shared mutable team context block.

Create Windsurf memories and the letta-memory-update skill to turn completed work into durable memory suggestions.

Later, add git-backed memfs sidecar support only if that workflow is clearly needed.

Common pitfalls
The highest-risk setup issues are missing pgvector, using a container-local localhost for PostgreSQL, and mixing temporary debugging notes into long-term memory blocks.
 Another common design mistake is making every block mutable; read-only blocks are better for policies and canonical facts that should not drift during ordinary agent operation.

Next build targets
After the base deployment works, the next useful artifacts are a repo-local .windsurf/skills/ directory, a standardized block taxonomy, and a lightweight operational script set for creating agents, listing blocks, backing up memfs, and exporting agent state.
 That combination gives a repeatable foundation for using Letta as a long-term memory layer while Windsurf handles development-time guidance and memory capture.

OpenRouter free models for agents
If agents need low-cost or zero-cost model access, Letta supports OpenRouter as a bring-your-own-key provider, and the Letta provider docs list OpenRouter among the supported external providers.
 OpenRouter also offers a free-model router named openrouter/free, plus specific model variants suffixed with :free when those variants are available.

Recommended environment variables
Add OpenRouter credentials to the Letta server environment when you want agent models to come from OpenRouter:

text
OPENROUTER_API_KEY=replace-me
OPENROUTER_SITE_URL=https://your-domain-or-github-profile
OPENROUTER_APP_NAME=Letta Self-Host
Keep these alongside LETTA_PG_URI in the server .env file so the server can expose OpenRouter-backed models to clients and agents.

Model selection strategy
Use the following pattern for practical deployments:

Default experimentation model: openrouter/free when cost matters most and occasional model variation is acceptable.

Stable pinned free model: use a specific :free variant when one exists and behavior consistency matters more than automatic routing.

Production-critical agent: keep a paid fallback model available because free model availability, rate limits, and latency can vary.

Good defaults
These are safe starting recommendations based on the OpenRouter free router behavior and Letta’s provider/model naming pattern:

Agent type	Recommended model choice
General assistant	openrouter/free for cheapest iteration.
Memory curation / summarization	openrouter/free, then pin a specific :free model later if output style matters.
Coding or tool-heavy agent	Prefer testing a specific :free model with tool support, then keep a paid fallback ready.
Important long-running workflow	Avoid relying only on random free routing; pin a model or configure fallback.
Example agent model naming
Letta’s model docs show OpenRouter models referenced with the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet for a paid model.
 For free models, use either the router or a specific free variant such as openrouter/free or provider/model:free, depending on what OpenRouter currently exposes.

Windsurf + Letta recommendation
For your workflow, a strong budget-first setup is to use OpenRouter free models for drafting, memory suggestion generation, and non-critical agents, while reserving a more stable paid model only for agents that must handle complex tool use or critical automation.
 That keeps Windsurf-generated memory proposals cheap while still letting Letta remain the durable memory layer backed by PostgreSQL.

Suggested document update
Add this note to the project or runbook block for the deployment:

text
Preferred low-cost provider: OpenRouter
Default budget model: openrouter/free
Rule: use free models for drafting, summarization, and memory proposal tasks; use pinned or paid models for critical agent workflows.
Letta on Bare-Metal PostgreSQL (letta) with Windsurf Memory/Skills
This guide explains how to deploy a self-hosted Letta server against an existing bare-metal PostgreSQL database named letta, how to start and configure the service, how to use Letta memory blocks, CLI tools, and memfs features, and how to create Windsurf memories and skills that work well with a Letta-backed workflow.

Target architecture
The recommended setup is a Letta server running in Docker while PostgreSQL runs outside Docker on bare metal, with Letta connecting to Postgres through LETTA_PG_URI. Letta requires the pgvector extension in the target database because agent memory and related state are stored in PostgreSQL with vector support.

Prerequisites
Prepare the following before deployment:

A reachable PostgreSQL instance with a database named letta.

A PostgreSQL role dedicated to Letta, ideally with ownership of the letta database.

pgvector installed and enabled in that database.

Docker installed on the Letta host, because the documented self-hosting path runs the Letta server in a container.

At least one model provider configuration, such as OpenAI or another supported provider, because the server still needs an LLM backend after startup.

PostgreSQL setup
Create the database and role if they do not already exist, then enable pgvector inside letta.

sql
CREATE DATABASE letta;
CREATE USER letta_user WITH PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE letta TO letta_user;
\c letta
CREATE EXTENSION IF NOT EXISTS vector;
If PostgreSQL is on another host, ensure postgresql.conf and pg_hba.conf allow the Letta server to connect on port 5432 from the Letta machine. Use a strong password and prefer a dedicated database role rather than reusing a superuser account.

Environment file
Create a .env file for the Letta server so connection details and provider keys are not embedded in the Docker command.

text
LETTA_PG_URI=postgresql://letta_user:change-this-password@POSTGRES_HOST:5432/letta
OPENAI_API_KEY=replace-me
LETTA_DEBUG=1
For a local bare-metal PostgreSQL server running on the same Linux host as Docker, replace POSTGRES_HOST with the host address reachable from the container, often the machine IP or another routable interface instead of assuming localhost will work inside the container.

Starting Letta
The documented Docker guide shows Letta server deployment through docker run, and it supports connecting to an external PostgreSQL instance by setting LETTA_PG_URI. A practical starting command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
After startup, Letta should connect to PostgreSQL, initialize its schema, and expose the API on port 8283 unless overridden. Set LETTA_BASE_URL=http://YOUR_HOST:8283 in clients such as Letta Code when using the self-hosted server.

First-run checks
Validate the deployment with these checks:

Confirm the container is running: docker ps.

Confirm PostgreSQL connectivity from the host or container using the same connection string.

Confirm vector exists: SELECT extname FROM pg_extension WHERE extname = 'vector';.

Confirm your client points at the server with LETTA_BASE_URL.

If the server fails early, the most common causes are missing pgvector, bad network routing to PostgreSQL, or an invalid database URI.

Letta Code installation
Letta Code is the CLI entry point for working with agents, memory, conversations, memfs, and skills-related workflows. Its basic usage includes resuming default sessions, creating new agents, selecting models, and pointing at a self-hosted server with LETTA_BASE_URL.

Common environment variables for CLI use:

bash
export LETTA_BASE_URL=http://YOUR_HOST:8283
export LETTA_DEBUG=1
export DISABLE_AUTOUPDATER=1
Then start a session with:

bash
letta
or create a new agent session with:

bash
letta --new-agent
The CLI also supports explicit model and system configuration flags such as --model, --embedding, --system, --skills, and --toolset.

Creating a useful agent
Letta supports preset and custom memory blocks during agent creation through flags such as --init-blocks, --memory-blocks, --block-value, and --memfs. Memory blocks are core memory sections that persist across interactions and are always visible in the context window, so they are the right place for persona, project facts, operating rules, and long-lived task state.

Example:

bash
letta --new-agent \
  --model sonnet \
  --init-blocks persona,project \
  --block-value persona="You are an engineering assistant for homelab and AI infra tasks." \
  --block-value project="Current project: deploy and operate Letta with PostgreSQL and Windsurf." \
  --memfs
This creates an agent with persistent core memory blocks and enables the Memory Filesystem feature for file-oriented state.

Memory blocks
Memory blocks are structured, persistent sections of an agent’s context window that Letta automatically manages, and agents can read and update them using built-in memory tools. Blocks can be read-write or marked read-only, and they can also be attached to multiple agents to provide shared memory.

Recommended block layout for an engineering assistant:

Block	Purpose
persona	Stable behavior, role, tone, and operating constraints.
project	Current system architecture, hosts, services, repos, and environment notes.
runbook	Deployment facts, commands, and troubleshooting conventions.
scratchpad	Working notes the agent may revise frequently.
policies	Read-only compliance, guardrails, or organization rules.
For shared teams or multi-agent setups, create blocks once and attach them to several agents so they all see the same evolving context.

Managing memory from the CLI
Letta exposes JSON-oriented subcommands to inspect and manipulate agents, messages, memfs, and blocks. Important commands include letta agents list, letta blocks list --agent <id>, letta blocks attach --block-id <id>, and letta messages search --query <text>.

Useful examples:

bash
letta agents list
letta blocks list --agent AGENT_ID
letta blocks attach --block-id BLOCK_ID --agent AGENT_ID
letta messages search --query "postgres pgvector" --agent AGENT_ID
letta memfs status --agent AGENT_ID
letta memfs export --agent AGENT_ID --out ./agent_memfs_export
These commands are useful for auditing what the agent knows, exporting file-backed memory, and reusing blocks across agents.

MemFS usage
Letta Code supports a Memory Filesystem feature enabled with --memfs, along with commands for status, diff, resolve, backup, restore, and export. The Docker deployment guide also notes that full git sync requires a sidecar implementing Git smart HTTP and the LETTA_MEMFS_SERVICE_URL environment variable if you want proxied /v1/git/ integration.

A safe workflow for memfs-enabled agents is:

Create the agent with --memfs.

Check sync state with letta memfs status --agent AGENT_ID.

Review conflicts with letta memfs diff --agent AGENT_ID.

Back up important state with letta memfs backup --agent AGENT_ID before destructive changes.

If using git-backed sync, add the sidecar and LETTA_MEMFS_SERVICE_URL later rather than on day one.

Starting to use Letta day to day
A practical daily workflow is to create one agent per major domain, pin stable instructions into memory blocks, and keep project-specific state in project, runbook, and scratchpad blocks. Search past messages when needed, export memfs snapshots before major refactors, and use shared blocks when multiple agents need a common operational memory.

A good first pattern is:

One infra agent for homelab, Docker, PostgreSQL, and observability.

One coding agent per repository or stack.

One shared read-only policies block for standards and constraints.

One shared mutable team-context block for current milestones and incidents.

Windsurf memories
Windsurf supports persisted memories and rules at global and workspace levels, and its docs recommend keeping rules simple, concise, specific, and structured with markdown lists rather than long vague paragraphs. Windsurf memories are a good place to define how Cascade should capture or update Letta-relevant facts during development work.

Suggested Windsurf memory rules:

text
- When infrastructure, environment variables, ports, hosts, database names, or deployment commands change, summarize the final state clearly.
- When a deployment task finishes, propose a concise memory update covering what was changed, where it runs, and how to verify it.
- Prefer durable facts over temporary debugging noise.
- Separate workspace-specific memories from global habits.
- When a fact belongs in long-term agent context, suggest adding it to the appropriate Letta memory block.
This keeps Windsurf from storing noisy implementation details while still preserving deployable system knowledge.

Windsurf skills
Windsurf skills can be created through the UI or manually by creating .windsurf/skills/<skill-name>/SKILL.md for a workspace skill, or ~/.codeium/windsurf/skills/<skill-name>/SKILL.md for a global one. The docs recommend clear descriptions and useful supporting resources so Cascade can decide when to invoke the skill.

Recommended skills for a Letta workflow:

Skill name	Use
letta-memory-update	Turns finished work into candidate Letta memory block updates.
letta-deploy-runbook	Generates deployment and troubleshooting steps for Letta server changes.
letta-block-design	Suggests memory block schemas for new agents or projects.
windsurf-memory-hygiene	Filters temporary chatter from durable rules and memories.
Example Windsurf skill
Create .windsurf/skills/letta-memory-update/SKILL.md with content like this:

text
---
name: letta-memory-update
description: Generate concise, durable Letta memory updates after infrastructure, coding, or deployment work. Use this skill when a task changes system facts, runbooks, environment variables, ports, agents, or database configuration.
---

# Letta Memory Update

When invoked, produce:

1. A short summary of the durable change.
2. The recommended Letta block target (`persona`, `project`, `runbook`, `scratchpad`, or another named block).
3. A proposed memory entry written as plain text.
4. A note on whether the item should be read-only, shared, or agent-local.
5. A verification command if relevant.

Rules:
- Prefer facts that will still matter next week.
- Exclude transient logs, stack traces, and one-off debugging attempts.
- Normalize ports, URLs, hostnames, service names, and env vars.
- If the change affects deployment, include rollback or verification notes.
This skill gives Windsurf a consistent pattern for turning completed work into memory-ready artifacts.

Suggested Windsurf support files
Attach supporting resources to each skill so the output stays consistent. Useful companion files include:

examples/good-memory-updates.md with several before/after examples.

templates/letta-block-template.md with standard fields for persona, project, runbook, and scratchpad.

checklists/deploy-verification.md with health checks for Letta, PostgreSQL, and memfs workflows.

Example Letta block templates
Use a simple schema so memory remains easy to maintain.

project
text
Project: Letta self-hosting
Server URL: http://YOUR_HOST:8283
Database: postgresql://letta_user@POSTGRES_HOST:5432/letta
Key requirements: pgvector enabled, Docker runtime, provider keys configured
Primary verification: docker ps; psql extension check; CLI connection test
runbook
text
Start server: docker run -d --name letta --restart unless-stopped --env-file .env -p 8283:8283 letta/letta:latest
Verify database: SELECT extname FROM pg_extension WHERE extname = 'vector';
Client base URL: export LETTA_BASE_URL=http://YOUR_HOST:8283
Memfs backup: letta memfs backup --agent AGENT_ID
policies
text
Do not store secrets directly in memory blocks.
Prefer environment variables or vault-backed secret storage.
Use shared blocks only for information safe to expose to every attached agent.
Recommended rollout plan
Use a staged rollout so the memory model stays manageable.

Deploy Letta against the letta PostgreSQL database with pgvector enabled.

Create one primary agent with persona, project, and runbook blocks.

Enable --memfs only after the base workflow is stable.

Add one shared read-only policies block and one shared mutable team context block.

Create Windsurf memories and the letta-memory-update skill to turn completed work into durable memory suggestions.

Later, add git-backed memfs sidecar support only if that workflow is clearly needed.

Common pitfalls
The highest-risk setup issues are missing pgvector, using a container-local localhost for PostgreSQL, and mixing temporary debugging notes into long-term memory blocks. Another common design mistake is making every block mutable; read-only blocks are better for policies and canonical facts that should not drift during ordinary agent operation.

Next build targets
After the base deployment works, the next useful artifacts are a repo-local .windsurf/skills/ directory, a standardized block taxonomy, and a lightweight operational script set for creating agents, listing blocks, backing up memfs, and exporting agent state. That combination gives a repeatable foundation for using Letta as a long-term memory layer while Windsurf handles development-time guidance and memory capture.

OpenRouter free models for agents
If agents need low-cost or zero-cost model access, Letta supports OpenRouter as a bring-your-own-key provider, and the Letta provider docs list OpenRouter among the supported external providers. OpenRouter also offers a free-model router named openrouter/free, plus specific model variants suffixed with :free when those variants are available.

Recommended environment variables
Add OpenRouter credentials to the Letta server environment when you want agent models to come from OpenRouter:

text
OPENROUTER_API_KEY=replace-me
OPENROUTER_SITE_URL=https://your-domain-or-github-profile
OPENROUTER_APP_NAME=Letta Self-Host
Keep these alongside LETTA_PG_URI in the server .env file so the server can expose OpenRouter-backed models to clients and agents.

Model selection strategy
Use the following pattern for practical deployments:

Default experimentation model: openrouter/free when cost matters most and occasional model variation is acceptable.

Stable pinned free model: use a specific :free variant when one exists and behavior consistency matters more than automatic routing.

Production-critical agent: keep a paid fallback model available because free model availability, rate limits, and latency can vary.

Good defaults
These are safe starting recommendations based on the OpenRouter free router behavior and Letta’s provider/model naming pattern:

Agent type	Recommended model choice
General assistant	openrouter/free for cheapest iteration.
Memory curation / summarization	openrouter/free, then pin a specific :free model later if output style matters.
Coding or tool-heavy agent	Prefer testing a specific :free model with tool support, then keep a paid fallback ready.
Important long-running workflow	Avoid relying only on random free routing; pin a model or configure fallback.
Example agent model naming
Letta’s model docs show OpenRouter models referenced with the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet for a paid model. For free models, use either the router or a specific free variant such as openrouter/free or provider/model:free, depending on what OpenRouter currently exposes.

Windsurf + Letta recommendation
For your workflow, a strong budget-first setup is to use OpenRouter free models for drafting, memory suggestion generation, and non-critical agents, while reserving a more stable paid model only for agents that must handle complex tool use or critical automation. That keeps Windsurf-generated memory proposals cheap while still letting Letta remain the durable memory layer backed by PostgreSQL.

Suggested document update
Add this note to the project or runbook block for the deployment:

please include details on setting up using openrouter free models for any agent use to power any agentic needs. this is different from the letta agents i think. please confirm. my windsurf agent is struggling as its tryingto setup openrouter use. please walk me thorugh how to do that. create markdown documents for all of this to walk through the windsurf agent. please include other troubleshooting instructions for deploymetn and setup as well. use localhost postgresql and i think the user is cbwinslow and the password is 123qweasd for the database. and the db port is the regular 5432 can you update the docs and create instructions and help files for an ai agent to use to fix my current setup. i have it setup and it shouldbe working soon. i have it installed and we are using the docker container tot access the database i believe. its however the docs origianlly said for bare metal dbs
Completed 4 steps





README
Document

windsurf-agent-walkthrough
Document

letta-openrouter-deploy-runbook
Document
README
Windsurf + OpenRouter + Letta setup pack
This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.

First confirmation
Yes, these are different layers.
 Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.

A practical way to think about it is:

Layer	Role
Windsurf / Cascade	The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.
OpenRouter	The model gateway and API endpoint that provides access to free and paid models through one base URL.
Letta	A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.
PostgreSQL	The backing database for Letta state when LETTA_PG_URI points to your own database.
So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.

Your current target
Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named letta, user cbwinslow, password 123qweasd, and the normal PostgreSQL port.
 That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via LETTA_PG_URI.

Important localhost warning
If Letta is inside Docker and PostgreSQL is on the host machine, localhost inside the container usually refers to the container itself, not the host OS.
 In that case, using postgresql://cbwinslow:123qweasd@localhost:5432/letta from inside the container may fail unless you deliberately mapped or bridged networking for host access.

In practice, one of these is usually required:

Use the host machine IP instead of localhost.

Use Docker host networking if appropriate for your platform.

Use a host alias such as host.docker.internal if your environment supports it.

If PostgreSQL is itself in a Docker container and exposed with -p 5432:5432, connect to the correct reachable host address rather than assuming plain container-local localhost semantics.

PostgreSQL connection string
Start with this target URI if Letta can truly reach host localhost from its runtime path:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
If that fails from the Dockerized Letta process, try replacing localhost with the actual host-reachable address used by Docker on your machine.

OpenRouter for general agent use
OpenRouter is configured through a single API base URL, https://openrouter.ai/api/v1, using an API key in the Authorization header, and optional app attribution headers HTTP-Referer and X-OpenRouter-Title.
 That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath.
 The shared provider is OpenRouter, but the configuration entry points differ by application.

OpenRouter free-model strategy
OpenRouter documents a free-model router named openrouter/free, and it also supports specific free model variants ending in :free when those are available.
 For unstable or exploratory work, the free router is the easiest starting point, while pinned :free models are better when consistent behavior matters.

Recommended use by task:

Windsurf drafting, code explanation, and iterative non-critical assistance: openrouter/free.

Memory suggestion generation, summarization, and cleanup: openrouter/free or a pinned :free model.

Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.

Letta model naming with OpenRouter
Letta documents OpenRouter model names using the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet.
 For free usage, follow the same pattern using openrouter/free or an explicitly free model variant exposed by OpenRouter at the time of setup.

Server environment example
Use a Letta .env file like this as a starting point:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to https://openrouter.ai/api/v1 and use the OpenRouter key in the API key slot.

Docker starting point
Letta’s Docker guide shows that environment variables can be passed through an .env file and that the server becomes available on port 8283 by default.
 A practical command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
If the database is another Docker container and you need to inspect it from the host, exposing 5432:5432 is the documented pattern for direct inspection tools like pgAdmin.

Windsurf walkthrough
Windsurf distinguishes among Rules, Skills, and Memories.
 Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.

A good recovery workflow in Windsurf is:

Add a workspace rule describing the intended OpenRouter and Letta architecture.

Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.

Ask Cascade to create a memory of the final working connection details once verified.

Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.

Troubleshooting checklist
When a setup is “almost working,” these are the most common failure points for your stack:

Wrong hostname in LETTA_PG_URI, especially using localhost from inside Docker when the database lives on the host.

pgvector missing in the letta database.

Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of https://openrouter.ai/api/v1.

Windsurf configured to use one provider while helper scripts or Letta still use another.

PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.

Container starts, but no actual model provider is configured for Letta agent execution.

Quick triage sequence
Run or verify these in order:

Confirm PostgreSQL is reachable at localhost:5432 from the host and confirm the letta DB exists.

Confirm vector is enabled in that database.

Confirm whether the Letta container can actually reach the host database using the same hostname in LETTA_PG_URI.

Confirm the OpenRouter API key is valid and the client is using https://openrouter.ai/api/v1.

Confirm Letta is listening on http://localhost:8283/v1 after startup.

Confirm Windsurf is not mixing a different model provider configuration during testing.

Files in this pack
This pack includes:

windsurf-agent-walkthrough.md: a direct walkthrough for an AI coding agent in Windsurf.

letta-openrouter-deploy-runbook.md: deployment, provider setup, and troubleshooting notes.

.windsurf/skills/openrouter-fix-agent/SKILL.md: a skill to diagnose OpenRouter misconfiguration.

.windsurf/skills/letta-troubleshooter/SKILL.md: a skill to diagnose Letta/PostgreSQL/Docker issues.

helpers/system-prompt-for-agent.md: a direct instruction file you can paste into an AI agent or use as a reference.

windsurf-agent-walkthrough
Windsurf + OpenRouter + Letta setup pack
This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.

First confirmation
Yes, these are different layers.
 Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.

A practical way to think about it is:

Layer	Role
Windsurf / Cascade	The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.
OpenRouter	The model gateway and API endpoint that provides access to free and paid models through one base URL.
Letta	A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.
PostgreSQL	The backing database for Letta state when LETTA_PG_URI points to your own database.
So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.

Your current target
Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named letta, user cbwinslow, password 123qweasd, and the normal PostgreSQL port.
 That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via LETTA_PG_URI.

Important localhost warning
If Letta is inside Docker and PostgreSQL is on the host machine, localhost inside the container usually refers to the container itself, not the host OS.
 In that case, using postgresql://cbwinslow:123qweasd@localhost:5432/letta from inside the container may fail unless you deliberately mapped or bridged networking for host access.

In practice, one of these is usually required:

Use the host machine IP instead of localhost.

Use Docker host networking if appropriate for your platform.

Use a host alias such as host.docker.internal if your environment supports it.

If PostgreSQL is itself in a Docker container and exposed with -p 5432:5432, connect to the correct reachable host address rather than assuming plain container-local localhost semantics.

PostgreSQL connection string
Start with this target URI if Letta can truly reach host localhost from its runtime path:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
If that fails from the Dockerized Letta process, try replacing localhost with the actual host-reachable address used by Docker on your machine.

OpenRouter for general agent use
OpenRouter is configured through a single API base URL, https://openrouter.ai/api/v1, using an API key in the Authorization header, and optional app attribution headers HTTP-Referer and X-OpenRouter-Title.
 That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath.
 The shared provider is OpenRouter, but the configuration entry points differ by application.

OpenRouter free-model strategy
OpenRouter documents a free-model router named openrouter/free, and it also supports specific free model variants ending in :free when those are available.
 For unstable or exploratory work, the free router is the easiest starting point, while pinned :free models are better when consistent behavior matters.

Recommended use by task:

Windsurf drafting, code explanation, and iterative non-critical assistance: openrouter/free.

Memory suggestion generation, summarization, and cleanup: openrouter/free or a pinned :free model.

Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.

Letta model naming with OpenRouter
Letta documents OpenRouter model names using the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet.
 For free usage, follow the same pattern using openrouter/free or an explicitly free model variant exposed by OpenRouter at the time of setup.

Server environment example
Use a Letta .env file like this as a starting point:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to https://openrouter.ai/api/v1 and use the OpenRouter key in the API key slot.

Docker starting point
Letta’s Docker guide shows that environment variables can be passed through an .env file and that the server becomes available on port 8283 by default.
 A practical command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
If the database is another Docker container and you need to inspect it from the host, exposing 5432:5432 is the documented pattern for direct inspection tools like pgAdmin.

Windsurf walkthrough
Windsurf distinguishes among Rules, Skills, and Memories.
 Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.

A good recovery workflow in Windsurf is:

Add a workspace rule describing the intended OpenRouter and Letta architecture.

Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.

Ask Cascade to create a memory of the final working connection details once verified.

Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.

Troubleshooting checklist
When a setup is “almost working,” these are the most common failure points for your stack:

Wrong hostname in LETTA_PG_URI, especially using localhost from inside Docker when the database lives on the host.

pgvector missing in the letta database.

Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of https://openrouter.ai/api/v1.

Windsurf configured to use one provider while helper scripts or Letta still use another.

PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.

Container starts, but no actual model provider is configured for Letta agent execution.

Quick triage sequence
Run or verify these in order:

Confirm PostgreSQL is reachable at localhost:5432 from the host and confirm the letta DB exists.

Confirm vector is enabled in that database.

Confirm whether the Letta container can actually reach the host database using the same hostname in LETTA_PG_URI.

Confirm the OpenRouter API key is valid and the client is using https://openrouter.ai/api/v1.

Confirm Letta is listening on http://localhost:8283/v1 after startup.

Confirm Windsurf is not mixing a different model provider configuration during testing.

Files in this pack
This pack includes:

windsurf-agent-walkthrough.md: a direct walkthrough for an AI coding agent in Windsurf.

letta-openrouter-deploy-runbook.md: deployment, provider setup, and troubleshooting notes.

.windsurf/skills/openrouter-fix-agent/SKILL.md: a skill to diagnose OpenRouter misconfiguration.

.windsurf/skills/letta-troubleshooter/SKILL.md: a skill to diagnose Letta/PostgreSQL/Docker issues.

helpers/system-prompt-for-agent.md: a direct instruction file you can paste into an AI agent or use as a reference.

letta-openrouter-deploy-runbook
Windsurf + OpenRouter + Letta setup pack
This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.

First confirmation
Yes, these are different layers.
 Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.

A practical way to think about it is:

Layer	Role
Windsurf / Cascade	The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.
OpenRouter	The model gateway and API endpoint that provides access to free and paid models through one base URL.
Letta	A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.
PostgreSQL	The backing database for Letta state when LETTA_PG_URI points to your own database.
So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.

Your current target
Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named letta, user cbwinslow, password 123qweasd, and the normal PostgreSQL port.
 That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via LETTA_PG_URI.

Important localhost warning
If Letta is inside Docker and PostgreSQL is on the host machine, localhost inside the container usually refers to the container itself, not the host OS.
 In that case, using postgresql://cbwinslow:123qweasd@localhost:5432/letta from inside the container may fail unless you deliberately mapped or bridged networking for host access.

In practice, one of these is usually required:

Use the host machine IP instead of localhost.

Use Docker host networking if appropriate for your platform.

Use a host alias such as host.docker.internal if your environment supports it.

If PostgreSQL is itself in a Docker container and exposed with -p 5432:5432, connect to the correct reachable host address rather than assuming plain container-local localhost semantics.

PostgreSQL connection string
Start with this target URI if Letta can truly reach host localhost from its runtime path:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
If that fails from the Dockerized Letta process, try replacing localhost with the actual host-reachable address used by Docker on your machine.

OpenRouter for general agent use
OpenRouter is configured through a single API base URL, https://openrouter.ai/api/v1, using an API key in the Authorization header, and optional app attribution headers HTTP-Referer and X-OpenRouter-Title.
 That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath.
 The shared provider is OpenRouter, but the configuration entry points differ by application.

OpenRouter free-model strategy
OpenRouter documents a free-model router named openrouter/free, and it also supports specific free model variants ending in :free when those are available.
 For unstable or exploratory work, the free router is the easiest starting point, while pinned :free models are better when consistent behavior matters.

Recommended use by task:

Windsurf drafting, code explanation, and iterative non-critical assistance: openrouter/free.

Memory suggestion generation, summarization, and cleanup: openrouter/free or a pinned :free model.

Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.

Letta model naming with OpenRouter
Letta documents OpenRouter model names using the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet.
 For free usage, follow the same pattern using openrouter/free or an explicitly free model variant exposed by OpenRouter at the time of setup.

Server environment example
Use a Letta .env file like this as a starting point:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to https://openrouter.ai/api/v1 and use the OpenRouter key in the API key slot.

Docker starting point
Letta’s Docker guide shows that environment variables can be passed through an .env file and that the server becomes available on port 8283 by default.
 A practical command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
If the database is another Docker container and you need to inspect it from the host, exposing 5432:5432 is the documented pattern for direct inspection tools like pgAdmin.

Windsurf walkthrough
Windsurf distinguishes among Rules, Skills, and Memories.
 Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.

A good recovery workflow in Windsurf is:

Add a workspace rule describing the intended OpenRouter and Letta architecture.

Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.

Ask Cascade to create a memory of the final working connection details once verified.

Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.

Troubleshooting checklist
When a setup is “almost working,” these are the most common failure points for your stack:

Wrong hostname in LETTA_PG_URI, especially using localhost from inside Docker when the database lives on the host.

pgvector missing in the letta database.

Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of https://openrouter.ai/api/v1.

Windsurf configured to use one provider while helper scripts or Letta still use another.

PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.

Container starts, but no actual model provider is configured for Letta agent execution.

Quick triage sequence
Run or verify these in order:

Confirm PostgreSQL is reachable at localhost:5432 from the host and confirm the letta DB exists.

Confirm vector is enabled in that database.

Confirm whether the Letta container can actually reach the host database using the same hostname in LETTA_PG_URI.

Confirm the OpenRouter API key is valid and the client is using https://openrouter.ai/api/v1.

Confirm Letta is listening on http://localhost:8283/v1 after startup.

Confirm Windsurf is not mixing a different model provider configuration during testing.

Files in this pack
This pack includes:

windsurf-agent-walkthrough.md: a direct walkthrough for an AI coding agent in Windsurf.

letta-openrouter-deploy-runbook.md: deployment, provider setup, and troubleshooting notes.

.windsurf/skills/openrouter-fix-agent/SKILL.md: a skill to diagnose OpenRouter misconfiguration.

.windsurf/skills/letta-troubleshooter/SKILL.md: a skill to diagnose Letta/PostgreSQL/Docker issues.

helpers/system-prompt-for-agent.md: a direct instruction file you can paste into an AI agent or use as a reference.

SECURITY_NOTE
Windsurf + OpenRouter + Letta setup pack
This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.

First confirmation
Yes, these are different layers.
 Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.

A practical way to think about it is:

Layer	Role
Windsurf / Cascade	The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.
OpenRouter	The model gateway and API endpoint that provides access to free and paid models through one base URL.
Letta	A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.
PostgreSQL	The backing database for Letta state when LETTA_PG_URI points to your own database.
So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.

Your current target
Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named letta, user cbwinslow, password 123qweasd, and the normal PostgreSQL port.
 That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via LETTA_PG_URI.

Important localhost warning
If Letta is inside Docker and PostgreSQL is on the host machine, localhost inside the container usually refers to the container itself, not the host OS.
 In that case, using postgresql://cbwinslow:123qweasd@localhost:5432/letta from inside the container may fail unless you deliberately mapped or bridged networking for host access.

In practice, one of these is usually required:

Use the host machine IP instead of localhost.

Use Docker host networking if appropriate for your platform.

Use a host alias such as host.docker.internal if your environment supports it.

If PostgreSQL is itself in a Docker container and exposed with -p 5432:5432, connect to the correct reachable host address rather than assuming plain container-local localhost semantics.

PostgreSQL connection string
Start with this target URI if Letta can truly reach host localhost from its runtime path:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
If that fails from the Dockerized Letta process, try replacing localhost with the actual host-reachable address used by Docker on your machine.

OpenRouter for general agent use
OpenRouter is configured through a single API base URL, https://openrouter.ai/api/v1, using an API key in the Authorization header, and optional app attribution headers HTTP-Referer and X-OpenRouter-Title.
 That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath.
 The shared provider is OpenRouter, but the configuration entry points differ by application.

OpenRouter free-model strategy
OpenRouter documents a free-model router named openrouter/free, and it also supports specific free model variants ending in :free when those are available.
 For unstable or exploratory work, the free router is the easiest starting point, while pinned :free models are better when consistent behavior matters.

Recommended use by task:

Windsurf drafting, code explanation, and iterative non-critical assistance: openrouter/free.

Memory suggestion generation, summarization, and cleanup: openrouter/free or a pinned :free model.

Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.

Letta model naming with OpenRouter
Letta documents OpenRouter model names using the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet.
 For free usage, follow the same pattern using openrouter/free or an explicitly free model variant exposed by OpenRouter at the time of setup.

Server environment example
Use a Letta .env file like this as a starting point:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to https://openrouter.ai/api/v1 and use the OpenRouter key in the API key slot.

Docker starting point
Letta’s Docker guide shows that environment variables can be passed through an .env file and that the server becomes available on port 8283 by default.
 A practical command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
If the database is another Docker container and you need to inspect it from the host, exposing 5432:5432 is the documented pattern for direct inspection tools like pgAdmin.

Windsurf walkthrough
Windsurf distinguishes among Rules, Skills, and Memories.
 Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.

A good recovery workflow in Windsurf is:

Add a workspace rule describing the intended OpenRouter and Letta architecture.

Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.

Ask Cascade to create a memory of the final working connection details once verified.

Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.

Troubleshooting checklist
When a setup is “almost working,” these are the most common failure points for your stack:

Wrong hostname in LETTA_PG_URI, especially using localhost from inside Docker when the database lives on the host.

pgvector missing in the letta database.

Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of https://openrouter.ai/api/v1.

Windsurf configured to use one provider while helper scripts or Letta still use another.

PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.

Container starts, but no actual model provider is configured for Letta agent execution.

Quick triage sequence
Run or verify these in order:

Confirm PostgreSQL is reachable at localhost:5432 from the host and confirm the letta DB exists.

Confirm vector is enabled in that database.

Confirm whether the Letta container can actually reach the host database using the same hostname in LETTA_PG_URI.

Confirm the OpenRouter API key is valid and the client is using https://openrouter.ai/api/v1.

Confirm Letta is listening on http://localhost:8283/v1 after startup.

Confirm Windsurf is not mixing a different model provider configuration during testing.

Files in this pack
This pack includes:

windsurf-agent-walkthrough.md: a direct walkthrough for an AI coding agent in Windsurf.

letta-openrouter-deploy-runbook.md: deployment, provider setup, and troubleshooting notes.

.windsurf/skills/openrouter-fix-agent/SKILL.md: a skill to diagnose OpenRouter misconfiguration.

.windsurf/skills/letta-troubleshooter/SKILL.md: a skill to diagnose Letta/PostgreSQL/Docker issues.

helpers/system-prompt-for-agent.md: a direct instruction file you can paste into an AI agent or use as a reference.

system-prompt-for-agent
Windsurf + OpenRouter + Letta setup pack
This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.

First confirmation
Yes, these are different layers.
 Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.

A practical way to think about it is:

Layer	Role
Windsurf / Cascade	The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.
OpenRouter	The model gateway and API endpoint that provides access to free and paid models through one base URL.
Letta	A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.
PostgreSQL	The backing database for Letta state when LETTA_PG_URI points to your own database.
So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.

Your current target
Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named letta, user cbwinslow, password 123qweasd, and the normal PostgreSQL port.
 That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via LETTA_PG_URI.

Important localhost warning
If Letta is inside Docker and PostgreSQL is on the host machine, localhost inside the container usually refers to the container itself, not the host OS.
 In that case, using postgresql://cbwinslow:123qweasd@localhost:5432/letta from inside the container may fail unless you deliberately mapped or bridged networking for host access.

In practice, one of these is usually required:

Use the host machine IP instead of localhost.

Use Docker host networking if appropriate for your platform.

Use a host alias such as host.docker.internal if your environment supports it.

If PostgreSQL is itself in a Docker container and exposed with -p 5432:5432, connect to the correct reachable host address rather than assuming plain container-local localhost semantics.

PostgreSQL connection string
Start with this target URI if Letta can truly reach host localhost from its runtime path:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
If that fails from the Dockerized Letta process, try replacing localhost with the actual host-reachable address used by Docker on your machine.

OpenRouter for general agent use
OpenRouter is configured through a single API base URL, https://openrouter.ai/api/v1, using an API key in the Authorization header, and optional app attribution headers HTTP-Referer and X-OpenRouter-Title.
 That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath.
 The shared provider is OpenRouter, but the configuration entry points differ by application.

OpenRouter free-model strategy
OpenRouter documents a free-model router named openrouter/free, and it also supports specific free model variants ending in :free when those are available.
 For unstable or exploratory work, the free router is the easiest starting point, while pinned :free models are better when consistent behavior matters.

Recommended use by task:

Windsurf drafting, code explanation, and iterative non-critical assistance: openrouter/free.

Memory suggestion generation, summarization, and cleanup: openrouter/free or a pinned :free model.

Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.

Letta model naming with OpenRouter
Letta documents OpenRouter model names using the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet.
 For free usage, follow the same pattern using openrouter/free or an explicitly free model variant exposed by OpenRouter at the time of setup.

Server environment example
Use a Letta .env file like this as a starting point:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to https://openrouter.ai/api/v1 and use the OpenRouter key in the API key slot.

Docker starting point
Letta’s Docker guide shows that environment variables can be passed through an .env file and that the server becomes available on port 8283 by default.
 A practical command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
If the database is another Docker container and you need to inspect it from the host, exposing 5432:5432 is the documented pattern for direct inspection tools like pgAdmin.

Windsurf walkthrough
Windsurf distinguishes among Rules, Skills, and Memories.
 Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.

A good recovery workflow in Windsurf is:

Add a workspace rule describing the intended OpenRouter and Letta architecture.

Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.

Ask Cascade to create a memory of the final working connection details once verified.

Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.

Troubleshooting checklist
When a setup is “almost working,” these are the most common failure points for your stack:

Wrong hostname in LETTA_PG_URI, especially using localhost from inside Docker when the database lives on the host.

pgvector missing in the letta database.

Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of https://openrouter.ai/api/v1.

Windsurf configured to use one provider while helper scripts or Letta still use another.

PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.

Container starts, but no actual model provider is configured for Letta agent execution.

Quick triage sequence
Run or verify these in order:

Confirm PostgreSQL is reachable at localhost:5432 from the host and confirm the letta DB exists.

Confirm vector is enabled in that database.

Confirm whether the Letta container can actually reach the host database using the same hostname in LETTA_PG_URI.

Confirm the OpenRouter API key is valid and the client is using https://openrouter.ai/api/v1.

Confirm Letta is listening on http://localhost:8283/v1 after startup.

Confirm Windsurf is not mixing a different model provider configuration during testing.

Files in this pack
This pack includes:

windsurf-agent-walkthrough.md: a direct walkthrough for an AI coding agent in Windsurf.

letta-openrouter-deploy-runbook.md: deployment, provider setup, and troubleshooting notes.

.windsurf/skills/openrouter-fix-agent/SKILL.md: a skill to diagnose OpenRouter misconfiguration.

.windsurf/skills/letta-troubleshooter/SKILL.md: a skill to diagnose Letta/PostgreSQL/Docker issues.

helpers/system-prompt-for-agent.md: a direct instruction file you can paste into an AI agent or use as a reference.

SKILL
Windsurf + OpenRouter + Letta setup pack
This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.

First confirmation
Yes, these are different layers.
 Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.

A practical way to think about it is:

Layer	Role
Windsurf / Cascade	The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.
OpenRouter	The model gateway and API endpoint that provides access to free and paid models through one base URL.
Letta	A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.
PostgreSQL	The backing database for Letta state when LETTA_PG_URI points to your own database.
So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.

Your current target
Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named letta, user cbwinslow, password 123qweasd, and the normal PostgreSQL port.
 That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via LETTA_PG_URI.

Important localhost warning
If Letta is inside Docker and PostgreSQL is on the host machine, localhost inside the container usually refers to the container itself, not the host OS.
 In that case, using postgresql://cbwinslow:123qweasd@localhost:5432/letta from inside the container may fail unless you deliberately mapped or bridged networking for host access.

In practice, one of these is usually required:

Use the host machine IP instead of localhost.

Use Docker host networking if appropriate for your platform.

Use a host alias such as host.docker.internal if your environment supports it.

If PostgreSQL is itself in a Docker container and exposed with -p 5432:5432, connect to the correct reachable host address rather than assuming plain container-local localhost semantics.

PostgreSQL connection string
Start with this target URI if Letta can truly reach host localhost from its runtime path:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
If that fails from the Dockerized Letta process, try replacing localhost with the actual host-reachable address used by Docker on your machine.

OpenRouter for general agent use
OpenRouter is configured through a single API base URL, https://openrouter.ai/api/v1, using an API key in the Authorization header, and optional app attribution headers HTTP-Referer and X-OpenRouter-Title.
 That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath.
 The shared provider is OpenRouter, but the configuration entry points differ by application.

OpenRouter free-model strategy
OpenRouter documents a free-model router named openrouter/free, and it also supports specific free model variants ending in :free when those are available.
 For unstable or exploratory work, the free router is the easiest starting point, while pinned :free models are better when consistent behavior matters.

Recommended use by task:

Windsurf drafting, code explanation, and iterative non-critical assistance: openrouter/free.

Memory suggestion generation, summarization, and cleanup: openrouter/free or a pinned :free model.

Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.

Letta model naming with OpenRouter
Letta documents OpenRouter model names using the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet.
 For free usage, follow the same pattern using openrouter/free or an explicitly free model variant exposed by OpenRouter at the time of setup.

Server environment example
Use a Letta .env file like this as a starting point:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to https://openrouter.ai/api/v1 and use the OpenRouter key in the API key slot.

Docker starting point
Letta’s Docker guide shows that environment variables can be passed through an .env file and that the server becomes available on port 8283 by default.
 A practical command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
If the database is another Docker container and you need to inspect it from the host, exposing 5432:5432 is the documented pattern for direct inspection tools like pgAdmin.

Windsurf walkthrough
Windsurf distinguishes among Rules, Skills, and Memories.
 Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.

A good recovery workflow in Windsurf is:

Add a workspace rule describing the intended OpenRouter and Letta architecture.

Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.

Ask Cascade to create a memory of the final working connection details once verified.

Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.

Troubleshooting checklist
When a setup is “almost working,” these are the most common failure points for your stack:

Wrong hostname in LETTA_PG_URI, especially using localhost from inside Docker when the database lives on the host.

pgvector missing in the letta database.

Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of https://openrouter.ai/api/v1.

Windsurf configured to use one provider while helper scripts or Letta still use another.

PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.

Container starts, but no actual model provider is configured for Letta agent execution.

Quick triage sequence
Run or verify these in order:

Confirm PostgreSQL is reachable at localhost:5432 from the host and confirm the letta DB exists.

Confirm vector is enabled in that database.

Confirm whether the Letta container can actually reach the host database using the same hostname in LETTA_PG_URI.

Confirm the OpenRouter API key is valid and the client is using https://openrouter.ai/api/v1.

Confirm Letta is listening on http://localhost:8283/v1 after startup.

Confirm Windsurf is not mixing a different model provider configuration during testing.

Files in this pack
This pack includes:

windsurf-agent-walkthrough.md: a direct walkthrough for an AI coding agent in Windsurf.

letta-openrouter-deploy-runbook.md: deployment, provider setup, and troubleshooting notes.

.windsurf/skills/openrouter-fix-agent/SKILL.md: a skill to diagnose OpenRouter misconfiguration.

.windsurf/skills/letta-troubleshooter/SKILL.md: a skill to diagnose Letta/PostgreSQL/Docker issues.

helpers/system-prompt-for-agent.md: a direct instruction file you can paste into an AI agent or use as a reference.

Windsurf + OpenRouter + Letta setup pack
This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.

First confirmation
Yes, these are different layers. Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.

A practical way to think about it is:

Layer	Role
Windsurf / Cascade	The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.
OpenRouter	The model gateway and API endpoint that provides access to free and paid models through one base URL.
Letta	A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.
PostgreSQL	The backing database for Letta state when LETTA_PG_URI points to your own database.
So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.

Your current target
Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named letta, user cbwinslow, password 123qweasd, and the normal PostgreSQL port. That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via LETTA_PG_URI.

Important localhost warning
If Letta is inside Docker and PostgreSQL is on the host machine, localhost inside the container usually refers to the container itself, not the host OS. In that case, using postgresql://cbwinslow:123qweasd@localhost:5432/letta from inside the container may fail unless you deliberately mapped or bridged networking for host access.

In practice, one of these is usually required:

Use the host machine IP instead of localhost.

Use Docker host networking if appropriate for your platform.

Use a host alias such as host.docker.internal if your environment supports it.

If PostgreSQL is itself in a Docker container and exposed with -p 5432:5432, connect to the correct reachable host address rather than assuming plain container-local localhost semantics.

PostgreSQL connection string
Start with this target URI if Letta can truly reach host localhost from its runtime path:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
If that fails from the Dockerized Letta process, try replacing localhost with the actual host-reachable address used by Docker on your machine.

OpenRouter for general agent use
OpenRouter is configured through a single API base URL, https://openrouter.ai/api/v1, using an API key in the Authorization header, and optional app attribution headers HTTP-Referer and X-OpenRouter-Title. That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath. The shared provider is OpenRouter, but the configuration entry points differ by application.

OpenRouter free-model strategy
OpenRouter documents a free-model router named openrouter/free, and it also supports specific free model variants ending in :free when those are available. For unstable or exploratory work, the free router is the easiest starting point, while pinned :free models are better when consistent behavior matters.

Recommended use by task:

Windsurf drafting, code explanation, and iterative non-critical assistance: openrouter/free.

Memory suggestion generation, summarization, and cleanup: openrouter/free or a pinned :free model.

Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.

Letta model naming with OpenRouter
Letta documents OpenRouter model names using the openrouter/ prefix, for example openrouter/anthropic/claude-3.5-sonnet. For free usage, follow the same pattern using openrouter/free or an explicitly free model variant exposed by OpenRouter at the time of setup.

Server environment example
Use a Letta .env file like this as a starting point:

text
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to https://openrouter.ai/api/v1 and use the OpenRouter key in the API key slot.

Docker starting point
Letta’s Docker guide shows that environment variables can be passed through an .env file and that the server becomes available on port 8283 by default. A practical command is:

bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
If the database is another Docker container and you need to inspect it from the host, exposing 5432:5432 is the documented pattern for direct inspection tools like pgAdmin.

Windsurf walkthrough
Windsurf distinguishes among Rules, Skills, and Memories. Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.

A good recovery workflow in Windsurf is:

Add a workspace rule describing the intended OpenRouter and Letta architecture.

Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.

Ask Cascade to create a memory of the final working connection details once verified.

Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.

Troubleshooting checklist
When a setup is “almost working,” these are the most common failure points for your stack:

Wrong hostname in LETTA_PG_URI, especially using localhost from inside Docker when the database lives on the host.

pgvector missing in the letta database.

Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of https://openrouter.ai/api/v1.

Windsurf configured to use one provider while helper scripts or Letta still use another.

PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.

Container starts, but no actual model provider is configured for Letta agent execution.

Quick triage sequence
Run or verify these in order:

Confirm PostgreSQL is reachable at localhost:5432 from the host and confirm the letta DB exists.

Confirm vector is enabled in that database.

Confirm whether the Letta container can actually reach the host database using the same hostname in LETTA_PG_URI.

Confirm the OpenRouter API key is valid and the client is using https://openrouter.ai/api/v1.

Confirm Letta is listening on http://localhost:8283/v1 after startup.

Confirm Windsurf is not mixing a different model provider configuration during testing.

Files in this pack
This pack includes:

windsurf-agent-walkthrough.md: a direct walkthrough for an AI coding agent in Windsurf.

letta-openrouter-deploy-runbook.md: deployment, provider setup, and troubleshooting notes.

.windsurf/skills/openrouter-fix-agent/SKILL.md: a skill to diagnose OpenRouter misconfiguration.

.windsurf/skills/letta-troubleshooter/SKILL.md: a skill to diagnose Letta/PostgreSQL/Docker issues.

helpers/system-prompt-for-agent.md: a direct instruction file you can paste into an AI agent or use as a reference.

Follow-ups

Your Windsurf agent on OpenRouter free models — full Docker config guide with scripts
Computer
​

How to get and set up a free OpenRouter API key

Example Docker command for Letta with OpenRouter models

Configure Windsurf agent to use OpenRouter instead of Letta

List of free OpenRouter models compatible with Letta
