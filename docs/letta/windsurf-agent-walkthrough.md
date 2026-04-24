# Windsurf + OpenRouter + Letta setup pack

This pack explains how to configure OpenRouter free models for general agentic use, how that differs from Letta-hosted agents, how to connect Letta to a PostgreSQL database on localhost:5432, and how to troubleshoot a half-working Docker deployment that should already be close to functional.[1][2][3][4][5][6]

## First confirmation

Yes, these are different layers.[1][2][4] Windsurf/Cascade can use model providers and memories for coding assistance in the IDE, while Letta is a separate agent server and memory system with its own agent runtime, memory blocks, and API.[4][1][3]

A practical way to think about it is:[4][1][2]

| Layer | Role |
|---|---|
| Windsurf / Cascade | The coding assistant in the editor, with rules, skills, and auto-generated workspace memories.[4][5] |
| OpenRouter | The model gateway and API endpoint that provides access to free and paid models through one base URL.[2] |
| Letta | A separate self-hosted agent server with long-term memory blocks, memfs support, tools, and APIs.[3][1] |
| PostgreSQL | The backing database for Letta state when `LETTA_PG_URI` points to your own database.[3] |

So your Windsurf agent trying to "set up OpenRouter" is usually about configuring the IDE or related tooling to call OpenRouter correctly, while Letta agent configuration is about how Letta itself selects a provider and model for its own agents.[4][1][2]

## Your current target

Based on your note, the intended setup is Letta running in Docker while PostgreSQL runs on localhost port 5432 outside the Letta app path, using a database named `letta`, user `cbwinslow`, password `123qweasd`, and the normal PostgreSQL port.[3] That is still consistent with Letta’s documented approach for connecting Dockerized Letta to your own Postgres instance via `LETTA_PG_URI`.[3]

## Important localhost warning

If Letta is inside Docker and PostgreSQL is on the host machine, `localhost` inside the container usually refers to the container itself, not the host OS.[3][6] In that case, using `postgresql://cbwinslow:123qweasd@localhost:5432/letta` from inside the container may fail unless you deliberately mapped or bridged networking for host access.[3]

In practice, one of these is usually required:[3][6]

- Use the host machine IP instead of `localhost`.[3]
- Use Docker host networking if appropriate for your platform.[3]
- Use a host alias such as `host.docker.internal` if your environment supports it.[3]
- If PostgreSQL is itself in a Docker container and exposed with `-p 5432:5432`, connect to the correct reachable host address rather than assuming plain container-local `localhost` semantics.[6]

## PostgreSQL connection string

Start with this target URI if Letta can truly reach host localhost from its runtime path:[3]

```env
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
```

If that fails from the Dockerized Letta process, try replacing `localhost` with the actual host-reachable address used by Docker on your machine.[3][6]

## OpenRouter for general agent use

OpenRouter is configured through a single API base URL, `https://openrouter.ai/api/v1`, using an API key in the `Authorization` header, and optional app attribution headers `HTTP-Referer` and `X-OpenRouter-Title`.[2] That means any agentic tool that speaks an OpenAI-compatible chat-completions API can often be pointed at OpenRouter by changing the base URL and API key.[2][7]

This is why Windsurf, scripts, helper tools, and Letta may each need their own provider configuration even though they can all use OpenRouter underneath.[4][1][2] The shared provider is OpenRouter, but the configuration entry points differ by application.[4][1][2]

## OpenRouter free-model strategy

OpenRouter documents a free-model router named `openrouter/free`, and it also supports specific free model variants ending in `:free` when those are available.[8] For unstable or exploratory work, the free router is the easiest starting point, while pinned `:free` models are better when consistent behavior matters.[8]

Recommended use by task:[8]

- Windsurf drafting, code explanation, and iterative non-critical assistance: `openrouter/free`.[8]
- Memory suggestion generation, summarization, and cleanup: `openrouter/free` or a pinned `:free` model.[8]
- Tool-heavy or critical automation: keep a paid fallback model available because free availability and behavior can vary.[8]

## Letta model naming with OpenRouter

Letta documents OpenRouter model names using the `openrouter/` prefix, for example `openrouter/anthropic/claude-3.5-sonnet`.[1] For free usage, follow the same pattern using `openrouter/free` or an explicitly free model variant exposed by OpenRouter at the time of setup.[1][8]

## Server environment example

Use a Letta `.env` file like this as a starting point:[3][9][2]

```env
LETTA_PG_URI=postgresql://cbwinslow:123qweasd@localhost:5432/letta
LETTA_DEBUG=1
OPENROUTER_API_KEY=replace_with_real_key
OPENROUTER_SITE_URL=https://github.com/cbwinslow
OPENROUTER_APP_NAME=Windsurf Letta Setup
```

If Letta or another tool expects OpenAI-compatible settings instead of a dedicated OpenRouter field, point that tool to `https://openrouter.ai/api/v1` and use the OpenRouter key in the API key slot.[2][7]

## Docker starting point

Letta’s Docker guide shows that environment variables can be passed through an `.env` file and that the server becomes available on port 8283 by default.[3][10] A practical command is:

```bash
docker run -d \
  --name letta \
  --restart unless-stopped \
  --env-file .env \
  -p 8283:8283 \
  letta/letta:latest
```

If the database is another Docker container and you need to inspect it from the host, exposing `5432:5432` is the documented pattern for direct inspection tools like pgAdmin.[6]

## Windsurf walkthrough

Windsurf distinguishes among Rules, Skills, and Memories.[4][5] Rules tell Cascade how to behave, Skills package repeatable multi-step procedures, and Memories are auto-generated or manually requested persistent contextual notes stored locally per workspace.[4][5]

A good recovery workflow in Windsurf is:[4][5]

1. Add a workspace rule describing the intended OpenRouter and Letta architecture.[4]
2. Add a troubleshooting skill that checks environment variables, endpoint URLs, and Docker/Postgres reachability.[5]
3. Ask Cascade to create a memory of the final working connection details once verified.[4]
4. Keep secrets out of memories when possible; store only the fact of where the secret is configured, not the secret value itself.[4]

## Troubleshooting checklist

When a setup is “almost working,” these are the most common failure points for your stack:[3][2][6]

- Wrong hostname in `LETTA_PG_URI`, especially using `localhost` from inside Docker when the database lives on the host.[3][6]
- `pgvector` missing in the `letta` database.[3]
- Correct OpenRouter key present, but the app still pointing at the wrong base URL instead of `https://openrouter.ai/api/v1`.[2]
- Windsurf configured to use one provider while helper scripts or Letta still use another.[4][1][2]
- PostgreSQL listening only on a local socket or restricted interface instead of a reachable TCP interface.[3]
- Container starts, but no actual model provider is configured for Letta agent execution.[9][1]

## Quick triage sequence

Run or verify these in order:[3][2][6]

1. Confirm PostgreSQL is reachable at `localhost:5432` from the host and confirm the `letta` DB exists.[3]
2. Confirm `vector` is enabled in that database.[3]
3. Confirm whether the Letta container can actually reach the host database using the same hostname in `LETTA_PG_URI`.[3][6]
4. Confirm the OpenRouter API key is valid and the client is using `https://openrouter.ai/api/v1`.[2]
5. Confirm Letta is listening on `http://localhost:8283/v1` after startup.[3]
6. Confirm Windsurf is not mixing a different model provider configuration during testing.[4]

## Files in this pack

This pack includes:[5][4]

- `windsurf-agent-walkthrough.md`: a direct walkthrough for an AI coding agent in Windsurf.[5][4]
- `letta-openrouter-deploy-runbook.md`: deployment, provider setup, and troubleshooting notes.[3][1][9][2]
- `.windsurf/skills/openrouter-fix-agent/SKILL.md`: a skill to diagnose OpenRouter misconfiguration.[5]
- `.windsurf/skills/letta-troubleshooter/SKILL.md`: a skill to diagnose Letta/PostgreSQL/Docker issues.[5]
- `helpers/system-prompt-for-agent.md`: a direct instruction file you can paste into an AI agent or use as a reference.[5][4]