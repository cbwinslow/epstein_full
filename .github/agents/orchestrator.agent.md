---
name: orchestrator
description: |
  A reusable VS Code Copilot agent that can coordinate multiple sub‑agents
  (via `runSubagent`) to work on different parts of a problem in parallel
  or in a defined sequence. It provides an "ensemble" capability – spawning a
  set of specialized agents, collecting their outputs, and synthesising a final
  answer.
applyTo: "**/*"
useWhen: "orchestrate, ensemble, parallel tasks, coordinate agents"
toolRestrictions:
  # The orchestrator needs only a few core tools plus the ability to spawn sub‑agents.
  allow:
    - read_file
    - write_file
    - apply_patch
    - runSubagent
    - get_errors
    - grep_search
    - semantic_search
    - start_process
    - interact_with_process
    - run_in_terminal
    - run_playwright_code
  deny: []
hooks: {}
---

## Orchestration Workflow

1. **Define the overall goal** – The user provides a high‑level task (e.g.,
   "refactor the data ingestion pipeline and add unit tests").

2. **Decompose into sub‑tasks** – The orchestrator creates a list of logical
   sub‑tasks. Each sub‑task is mapped to a specialized agent (debug, test‑writer,
   documentation, etc.) by name.

3. **Spawn sub‑agents** – For each sub‑task the orchestrator calls
   `runSubagent` with the appropriate `agentName` and a concise prompt. The
   `description` field of each sub‑agent determines when it will be selected.

4. **Parallel execution** – Sub‑agents are launched without waiting for the
   previous one to finish, allowing true parallelism when the underlying model
   supports it. The orchestrator collects the `result` field from each call.

5. **Synthesis** – Once all sub‑agents have returned, the orchestrator merges
   their outputs, resolves conflicts, and produces a final answer or a set of
   patches.

6. **Apply changes** – If the synthesis includes code modifications, the
   orchestrator uses `apply_patch` to commit them, then optionally runs the test
   suite to verify the overall result.

## Example Prompt
```
Orchestrate a refactor of the `ingest_capitolgains.py` script:
  • Extract the download logic into a reusable function (use the `debug` agent).
  • Add unit tests for the new function (use a `test‑writer` agent).
  • Update documentation in `docs/INGESTION_GUIDES/` (use a `doc‑writer` agent).
```

The orchestrator will automatically split the request, spawn the three agents,
collect their outputs, apply the patches, and run the full test suite to ensure
everything works.

## Extensibility
* **Add new sub‑agents** – Simply create another `.agent.md` file with a clear
  `useWhen` description. The orchestrator can reference it by name.
* **Control concurrency** – The orchestrator can be extended with a `maxParallel`
  setting in the front‑matter to limit how many sub‑agents run at once.

---

### Usage Tips
* Invoke explicitly with `@orchestrator` or let the agent be selected when the
  prompt contains any of the `useWhen` keywords.
* Keep sub‑task prompts short and focused – the orchestrator will handle the
  coordination.
