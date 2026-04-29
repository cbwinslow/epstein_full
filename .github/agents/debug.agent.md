---
name: debug
description: |
  Use when you need to diagnose and fix problems in the project. The agent will
  first gather information about errors (log files, test failures, stack traces),
  then reason step‑by‑step to propose a solution, write or update tests that
  reproduce the issue, and finally apply a fix using appropriate tools.
applyTo: "**/*"
useWhen: "debugging"
toolRestrictions:
  # Allow all standard tools but avoid destructive commands without confirmation.
  # Allow all standard tools; no explicit deny list.
  allow:
    - read_file
    - write_file
    - apply_patch
    - start_process
    - interact_with_process
    - grep_search
    - semantic_search
    - get_errors
    - run_playwright_code
    - run_in_terminal
hooks:
  PreToolUse:
    # No confirmation needed; allow full tool usage.
    - command: "echo 'Running tool...';"
    description: "Placeholder hook – can be removed or customized later."
  PostToolUse:
    - command: "echo 'Tool completed'"
    description: "Simple acknowledgement after tool execution."
---

## Debugging Workflow

1. **Collect error information**
   - Search `logs/` and any `*.log` files for recent error messages.
   - Run the project's test suite (`pytest` or the configured framework) and capture failures.
   - If a stack trace is provided by the user, include it verbatim.

2. **Analyse the problem**
   - Use sequential reasoning: list possible causes, narrow down by evidence.
   - Identify the code locations involved (file paths, functions, line numbers).

3. **Create or update tests**
   - Write a minimal reproducing test that fails with the observed error.
   - Place the test in the appropriate test directory (`tests/` or `src/tests/`).
   - Ensure the test follows the project's testing framework conventions.

4. **Propose a fix**
   - Draft a code change that resolves the issue while keeping existing behaviour.
   - Apply the change using `apply_patch`.
   - Re‑run the test suite to confirm the fix.
  - If the issue involves UI or integration behavior, run the Playwright end‑to‑end tests (`scripts/run_e2e.sh`) to verify the fix in a real browser environment.

5. **Iterate**
   - If tests still fail, repeat steps 2‑4 until the problem is resolved.
  - For persistent UI regressions, add or update a Playwright test in `e2e/` and re‑run the suite.

## Example Prompts
```
Debug the failing `test_user_import` test.
Diagnose the TypeError raised when loading `data/raw/users.csv`.
```

The agent will automatically gather logs, run the failing test, create a minimal
repro test if needed, suggest a code edit, apply it, and verify the fix.

---

### Notes for the user
* The agent respects the `toolRestrictions` above – it will ask for confirmation
  before executing any `run_in_terminal` command that could modify files or the
  environment.
* You can invoke the agent explicitly with `@debug-agent` or let it be selected
  automatically when your prompt contains any of the `useWhen` keywords.
