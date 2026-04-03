# Comprehensive Dotfiles Plan — Chezmoi-Based Server Restoration

**Date**: 2026-04-02
**User**: cbwinslow (Blaine Winslow)
**Server**: Linux (Ubuntu) with GPU (Tesla K80/K40m)
**Tool**: chezmoi (already installed at `~/bin/chezmoi`)

---

## Executive Summary

This plan creates a new, clean `cbwinslow/dotfiles` GitHub repository using chezmoi that captures your **entire server identity** — shell configs, AI agent ecosystem, Docker stacks, IaC templates, MCP servers, cron jobs, systemd services, and a one-command bootstrap script for full server restoration.

The existing `~/.local/share/chezmoi/` has a stale remote with a leaked GitHub token. We start fresh.

---

## 1. Current State Assessment

### What You Have

| Category | Location | Size | Status |
|----------|----------|------|--------|
| Shell configs | `~/.bashrc`, `~/.zshrc`, `~/.bash_aliases`, `~/.bash_functions` | ~18KB | Active, rich config |
| AI agent system | `~/dotfiles/ai/` (19 skills, 12 agents) | 290MB total | Active, symlinked everywhere |
| Docker stacks | `~/docker/stacks/`, `~/infra/` | 2.7GB infra | Active |
| IaC | `~/infra/{ansible,terraform,k8s,gitops}` | Scaffolding | Partially populated |
| MCP servers | `~/.config/mcp/settings.json` | Active | 11 servers configured |
| Chezmoi source | `~/.local/share/chezmoi/` | Stale | **Broken remote (token leaked)** |
| Old repo | `cbwinslow/dotfiles_old` (was `shu`) | Archived | Read-only reference |
| Crontab | 4 entries | Active | Kuma, FEC, email, GitHub scanner |
| Systemd services | `openclaw-gateway.service` | Active | User service |
| Starship prompt | `~/.config/starship.toml` | Active | Minimal config |
| Git config | `~/.gitconfig` | Active | OAuth2 rewrite for GitHub |
| SSH | `~/.ssh/config`, `id_ed25519` | Active | 2 hosts configured |
| Editor | LunarVim (`~/.config/lvim/`) | Active | Full Lua config |
| Monitoring | `~/infra/monitoring/` | Active | Prometheus, Grafana, Kuma |
| Secrets | `~/.bash_secrets`, `~/.env.ai`, `~/.env` | Active | **Must encrypt in chezmoi** |

### What's Missing / Broken

1. No `chezmoi.toml` or `.chezmoi.toml.tmpl` — machine-specific config never generated
2. No `.chezmoiscripts/` — no bootstrap automation
3. No `.chezmoidata/` — no shared data layer
4. Leaked GitHub token in chezmoi git remote URL
5. AI skills referenced via symlinks — fragile, not captured
6. No restore-from-zero script
7. Cron jobs not versioned
8. Systemd user services not versioned

---

## 2. Target Repository Structure

Following modern chezmoi conventions from research (martinemde/dotfiles, mizchi/chezmoi-dotfiles, natelandau/dotfiles):

```
cbwinslow/dotfiles/
├── .chezmoi.toml.tmpl          # Machine-specific config generator
├── .chezmoiignore              # Files chezmoi should skip
├── .chezmoiexternal.toml       # External deps (git repos, archives)
├── .chezmoidata.toml           # Shared data across all machines
├── .chezmoiversion             # Pin chezmoi version
├── .chezmoiroot                # Set root to "home/" (optional)
├── .editorconfig               # Editor standards
├── .gitignore                  # Repo-level ignores
├── .gitleaks.toml              # Secret scanning config
├── README.md
├── LICENSE
│
├── .chezmoiscripts/            # Bootstrap & lifecycle scripts
│   ├── run_once_before_00-system-packages.sh
│   ├── run_once_before_01-docker-setup.sh
│   ├── run_once_before_02-ai-models.sh
│   ├── run_once_00-install-tools.sh
│   ├── run_once_01-setup-dirs.sh
│   ├── run_once_02-setup-ssh.sh
│   ├── run_once_03-setup-git.sh
│   ├── run_once_04-setup-docker-stacks.sh
│   ├── run_once_05-setup-crontabs.sh
│   ├── run_once_06-setup-systemd.sh
│   ├── run_once_07-setup-ai-agents.sh
│   ├── run_once_08-setup-monitoring.sh
│   └── run_onchange_00-update-packages.sh
│
├── .chezmoidata/               # Shared data files
│   ├── packages.toml           # apt/brew/pip/npm package lists
│   ├── tools.toml              # CLI tool versions
│   ├── docker.toml             # Docker stack inventory
│   └── ai.toml                 # AI model/agent metadata
│
├── home/                       # Files mapped to ~/ (if using .chezmoiroot)
│   └── ...
│
├── dot_bashrc                  # → ~/.bashrc
├── dot_bashrc_letta            # → ~/.bashrc_letta
├── dot_bash_aliases            # → ~/.bash_aliases
├── dot_bash_functions          # → ~/.bash_functions
├── dot_bash_profile            # → ~/.bash_profile
├── dot_profile                 # → ~/.profile
├── dot_zshrc                   # → ~/.zshrc
├── dot_zshrc_letta             # → ~/.zshrc_letta (if exists)
│
├── dot_bash_secrets.tmpl       # → ~/.bash_secrets (encrypted/tmpl)
├── dot_env_ai.tmpl             # → ~/.env.ai (secrets template)
│
├── dot_gitconfig               # → ~/.gitconfig
├── dot_gitignore               # → ~/.gitignore
│
├── private_dot_ssh/            # → ~/.ssh/ (mode 0700)
│   ├── private_config          # → ~/.ssh/config (mode 0600)
│   ├── dot_authorized_keys     # → ~/.ssh/authorized_keys
│   └── run_create_ssh_key.sh   # Script to generate key if missing
│
├── private_dot_config/         # → ~/.config/
│   ├── starship/
│   │   └── starship.toml       # → ~/.config/starship.toml
│   ├── mcp/
│   │   └── settings.json.tmpl  # → ~/.config/mcp/settings.json
│   ├── chezmoi/
│   │   └── chezmoi.toml.tmpl   # → ~/.config/chezmoi/chezmoi.toml
│   ├── git/
│   │   └── config              # → ~/.config/git/config
│   ├── lvim/                   # → ~/.config/lvim/ (LunarVim)
│   │   └── config.lua
│   ├── code-server/            # → ~/.config/code-server/
│   │   └── config.yaml
│   ├── kilo/                   # → ~/.config/kilo/
│   │   ├── kilo.jsonc
│   │   └── ...
│   └── opencode/               # → ~/.config/opencode/
│       ├── config.yaml
│       └── instructions.md
│
├── dot_config/                 # Alternative: .config files via dot_config/
│   └── (symlinked structure)
│
├── private_dot_openclaw/       # → ~/.openclaw/ (mode 0700)
│   ├── config.yaml
│   ├── openclaw.json
│   └── dot_env.tmpl
│
├── private_dot_gemini/         # → ~/.gemini/
│   ├── settings.json
│   └── projects.json
│
├── private_dot_claude.json     # → ~/.claude.json
│
├── dotfiles-ai/                # → ~/dotfiles/ai/ (the AI agent system)
│   ├── config.yaml
│   ├── agents/
│   ├── skills/
│   ├── shared/
│   ├── frameworks/
│   ├── packages/
│   ├── workflows/
│   ├── setup.sh
│   └── ARCHITECTURE.md
│
├── infra/                      # → ~/infra/ (IaC templates)
│   ├── ansible/
│   │   ├── ansible.cfg
│   │   ├── playbooks/
│   │   ├── roles/
│   │   └── inventory/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── environments/
│   │       ├── dev/
│   │       ├── stage/
│   │       └── prod/
│   ├── k8s/
│   │   ├── base/
│   │   └── overlays/
│   ├── monitoring/
│   │   ├── prometheus/
│   │   ├── grafana/
│   │   ├── exporters/
│   │   └── kuma/
│   └── bootstrap_server_folders.sh
│
├── docker/                     # → ~/docker/ (compose stacks)
│   ├── stacks/
│   │   ├── traefik/
│   │   │   └── docker-compose.yml
│   │   ├── postgres/
│   │   │   └── docker-compose.yml
│   │   ├── monitoring/
│   │   │   └── docker-compose.yml
│   │   ├── openclaw/
│   │   │   └── docker-compose.yml
│   │   ├── n8n/
│   │   │   └── docker-compose.yml
│   │   ├── local-ai/
│   │   │   └── docker-compose.yml
│   │   ├── letta/
│   │   │   └── docker-compose.yml
│   │   └── open-webui/
│   │       └── docker-compose.yml
│   ├── templates/
│   └── bin/
│
├── scripts/                    # → ~/scripts/ (utility scripts)
│   ├── admin/
│   ├── maintenance/
│   ├── ai/
│   └── meta/
│
├── procedures/                 # → ~/procedures/ (runbooks)
│   ├── infra/
│   ├── docker/
│   ├── incidents/
│   ├── operations/
│   └── ai/
│
├── systemd/                    # → ~/.config/systemd/user/
│   └── user/
│       └── openclaw-gateway.service
│
├── crontab.txt                 # Crontab entries (restored via crontab command)
│
├── dot_cbw_firewall_rules.conf # → ~/.cbw_firewall_rules.conf
├── dot_cbw_packages.conf       # → ~/.cbw_packages.conf
│
└── bin/                        # Scripts in ~/bin/
    ├── rag-index
    └── rag-search
```

---

## 3. Key Design Decisions

### 3.1 Secret Management Strategy

**Approach**: chezmoi templates + Bitwarden CLI integration

| Secret Type | Method | File |
|-------------|--------|------|
| GitHub token | `{{ bitwardenFields "github-token" }}` or `.chezmoi.toml` data | `.gitconfig` template |
| SSH private key | `run_once_` script generates if missing, never in repo | `.chezmoiscripts/` |
| API keys (OpenRouter, Gemini, etc.) | `.env.ai.tmpl` with `promptStringOnce` | `dot_env_ai.tmpl` |
| Bitwarden master password | Prompt on init, stored in `.chezmoi.toml` local only | `.chezmoi.toml.tmpl` |
| PostgreSQL password | `.bash_secrets.tmpl` with `promptStringOnce` | `dot_bash_secrets.tmpl` |
| MCP server API keys | `settings.json.tmpl` with conditional includes | `private_dot_config/mcp/settings.json.tmpl` |

**Never in the repo**: private keys, passwords, tokens, `.env` files with real values.

### 3.2 AI Agent System Handling

The `~/dotfiles/ai/` directory (290MB) is too large for a standard chezmoi add. Strategy:

1. **Core config** (small files): Managed directly by chezmoi
2. **Skills registry**: `skills/registry.json` + individual skill directories managed by chezmoi
3. **Large models/dependencies**: `.chezmoiexternal.toml` pointing to git repos or releases
4. **Symlinks**: Re-created by `.chezmoiscripts/run_once_07-setup-ai-agents.sh`

The symlink pattern used today (`~/.openclaw/skills → ~/dotfiles/ai/skills`) gets codified in a run_once script.

### 3.3 Docker Stack Strategy

Docker compose files are managed by chezmoi. Volumes/data are NOT in the repo. The bootstrap script:
1. Creates directory structure (`~/docker/stacks/{name}/`)
2. Applies compose files via chezmoi
3. Pulls images
4. Starts stacks with `docker compose up -d`

### 3.4 Infrastructure as Code

- **Ansible**: Playbooks and roles in repo, inventories generated per environment
- **Terraform**: Module code in repo, state files NEVER in repo (use remote state)
- **K8s**: Kustomize base + overlays in repo

### 3.5 Machine Differentiation

If you add more machines later, chezmoi templates handle it:

```toml
# .chezmoi.toml (generated on each machine)
[data]
    hostname = "epstein-server"
    has_gpu = true
    gpu_count = 3
    os = "linux"
    username = "cbwinslow"
```

Templates use `{{ if .has_gpu }}` blocks to conditionally include GPU-dependent configs.

---

## 4. Bootstrap & Restoration Flow

### One-Command Full Restore

```bash
# On a fresh server:
curl -sfL https://get.chezmoi.io | sh
~/bin/chezmoi init --apply cbwinslow/dotfiles
```

This single command triggers:

```
┌─────────────────────────────────────────────────────────────┐
│  chezmoi init --apply cbwinslow/dotfiles                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Clone dotfiles repo → ~/.local/share/chezmoi/           │
│  2. Generate .chezmoi.toml from template (prompt for keys)  │
│  3. run_once_before_00-system-packages.sh                   │
│     └─ apt install: git, curl, wget, docker.io, etc.       │
│  4. run_once_before_01-docker-setup.sh                      │
│     └─ Install Docker, add user to docker group            │
│  5. run_once_before_02-ai-models.sh                         │
│     └─ Install Ollama, pull models                          │
│  6. Apply all dotfiles to ~/                                │
│     ├─ ~/.bashrc, ~/.zshrc, ~/.bash_aliases, ...           │
│     ├─ ~/.gitconfig, ~/.ssh/config                          │
│     ├─ ~/.config/starship.toml                              │
│     ├─ ~/.config/mcp/settings.json                          │
│     ├─ ~/dotfiles/ai/ (full agent system)                   │
│     ├─ ~/infra/ (IaC templates)                             │
│     ├─ ~/docker/ (compose stacks)                           │
│     └─ ~/scripts/, ~/procedures/                            │
│  7. run_once_00-install-tools.sh                            │
│     └─ Install: starship, atuin, nvm, cargo tools, etc.    │
│  8. run_once_01-setup-dirs.sh                               │
│     └─ Create ~/infra, ~/docker, ~/meta, XDG dirs          │
│  9. run_once_02-setup-ssh.sh                                │
│     └─ Generate SSH key if missing, set permissions         │
│  10. run_once_03-setup-git.sh                               │
│     └─ Configure git credentials, LFS                       │
│  11. run_once_04-setup-docker-stacks.sh                     │
│     └─ Pull images, create networks                         │
│  12. run_once_05-setup-crontabs.sh                          │
│     └─ Restore crontab from crontab.txt                     │
│  13. run_once_06-setup-systemd.sh                           │
│     └─ Enable user services (openclaw-gateway)              │
│  14. run_once_07-setup-ai-agents.sh                         │
│     └─ Create symlinks, install skills, configure agents    │
│  15. run_once_08-setup-monitoring.sh                        │
│     └─ Configure Prometheus, Grafana, Kuma                  │
│                                                             │
│  Result: Fully restored server from fresh OS                │
└─────────────────────────────────────────────────────────────┘
```

### Incremental Update Flow (Daily Use)

```bash
# After changing a config file:
chezmoi add ~/.bashrc              # Stage the change
chezmoi diff                       # Preview what changed
chezmoi apply                      # Apply pending changes
cd ~/.local/share/chezmoi
git add -A && git commit -m "Update bashrc" && git push
```

---

## 5. Implementation Phases

### Phase 1: Repository Foundation (Day 1)

| Step | Action | Command/Details |
|------|--------|-----------------|
| 1.1 | Remove stale chezmoi state | `rm -rf ~/.local/share/chezmoi` |
| 1.2 | Revoke leaked GitHub token | Go to GitHub → Settings → Tokens → Revoke `ghp_ktq...` |
| 1.3 | Create fresh chezmoi source | `chezmoi init` (local only, no remote yet) |
| 1.4 | Create `.chezmoi.toml.tmpl` | Template for machine-specific data |
| 1.5 | Create `.chezmoiversion` | Pin to current chezmoi version |
| 1.6 | Create `.chezmoiignore` | Exclude large/generated files |
| 1.7 | Create `.gitleaks.toml` | Prevent secret leaks |
| 1.8 | Create `.editorconfig` | Consistent formatting |
| 1.9 | Create `README.md` | Setup instructions |

**Feasibility**: HIGH — No risk, just scaffolding.

### Phase 2: Shell Configuration (Day 1)

| Step | Action | Command/Details |
|------|--------|-----------------|
| 2.1 | Add bash configs | `chezmoi add ~/.bashrc ~/.bash_aliases ~/.bash_functions ~/.bash_profile ~/.profile ~/.bash_logout` |
| 2.2 | Add zsh config | `chezmoi add ~/.zshrc` |
| 2.3 | Create secrets templates | `dot_bash_secrets.tmpl`, `dot_env_ai.tmpl` with `promptStringOnce` |
| 2.4 | Add starship config | `chezmoi add ~/.config/starship.toml` |
| 2.5 | Add `.bashrc_letta` | `chezmoi add ~/.bashrc_letta` |
| 2.6 | Add firewall/packages | `chezmoi add ~/.cbw_firewall_rules.conf ~/.cbw_packages.conf` |

**Feasibility**: HIGH — Straightforward file additions.

### Phase 3: Git & SSH (Day 1)

| Step | Action | Command/Details |
|------|--------|-----------------|
| 3.1 | Add gitconfig | `chezmoi add ~/.gitconfig` — template out the token |
| 3.2 | Add gitignore | `chezmoi add ~/.gitignore` |
| 3.3 | Add SSH config (not keys!) | `chezmoi add --template ~/.ssh/config` |
| 3.4 | Add authorized_keys | `chezmoi add ~/.ssh/authorized_keys` |
| 3.5 | Create SSH key gen script | `.chezmoiscripts/run_once_02-setup-ssh.sh` |

**Feasibility**: HIGH — SSH private keys are generated, not stored.

### Phase 4: AI Agent System (Day 2)

| Step | Action | Command/Details |
|------|--------|-----------------|
| 4.1 | Add AI config core | `chezmoi add ~/dotfiles/ai/config.yaml` |
| 4.2 | Add agent definitions | `chezmoi add ~/dotfiles/ai/agents/` |
| 4.3 | Add skills registry | `chezmoi add ~/dotfiles/ai/skills/registry.json` |
| 4.4 | Add skill directories | `chezmoi add ~/dotfiles/ai/skills/*/SKILL.md` + core files |
| 4.5 | Add shared frameworks | `chezmoi add ~/dotfiles/ai/frameworks/` |
| 4.6 | Add setup scripts | `chezmoi add ~/dotfiles/ai/setup.sh ~/dotfiles/ai/setup_ai.sh` |
| 4.7 | Create symlink script | `.chezmoiscripts/run_once_07-setup-ai-agents.sh` |
| 4.8 | Add Kilo config | `chezmoi add ~/.config/kilo/kilo.jsonc` |
| 4.9 | Add OpenCode config | `chezmoi add ~/.config/opencode/config.yaml` |
| 4.10 | Add Claude config | `chezmoi add ~/.claude.json` |
| 4.11 | Add Gemini config | `chezmoi add ~/.gemini/settings.json ~/.gemini/projects.json` |
| 4.12 | Add OpenClaw config | `chezmoi add ~/.openclaw/openclaw.json ~/.openclaw/config.yaml` |

**Feasibility**: MEDIUM — Large directory (290MB), need to decide what's essential vs external. Skills are the core value; model caches should be excluded.

### Phase 5: MCP & Tool Configs (Day 2)

| Step | Action | Command/Details |
|------|--------|-----------------|
| 5.1 | Add MCP settings template | `private_dot_config/mcp/settings.json.tmpl` — template out API keys |
| 5.2 | Add LunarVim config | `chezmoi add ~/.config/lvim/config.lua` (if custom) |
| 5.3 | Add code-server config | `chezmoi add ~/.config/code-server/config.yaml` |

**Feasibility**: HIGH — Small files, clear ownership.

### Phase 6: Docker & Infrastructure (Day 2-3)

| Step | Action | Command/Details |
|------|--------|-----------------|
| 6.1 | Add docker compose stacks | `chezmoi add ~/docker/stacks/*/docker-compose.yml` |
| 6.2 | Add docker helper scripts | `chezmoi add ~/docker/bin/` |
| 6.3 | Add ansible config | `chezmoi add ~/infra/ansible/ansible.cfg` + playbooks |
| 6.4 | Add terraform modules | `chezmoi add ~/infra/terraform/` (exclude `.terraform/`, state) |
| 6.5 | Add k8s manifests | `chezmoi add ~/infra/k8s/` |
| 6.6 | Add monitoring configs | `chezmoi add ~/infra/monitoring/` |
| 6.7 | Add bootstrap script | `chezmoi add ~/infra/bootstrap_server_folders.sh` |
| 6.8 | Add OpenClaw infra | `chezmoi add ~/infra/openclaw/docker-compose.yml` + Dockerfiles |
| 6.9 | Add n8n infra | `chezmoi add ~/infra/n8n/docker-compose.n8n.yml` |
| 6.10 | Add local-ai infra | `chezmoi add ~/infra/local-ai/docker-compose.yml` |
| 6.11 | Add Letta infra | `chezmoi add ~/infra/letta/docker-compose.letta.yml` |

**Feasibility**: HIGH — Compose files are small and text-based. Exclude volume data.

### Phase 7: System Services & Automation (Day 3)

| Step | Action | Command/Details |
|------|--------|-----------------|
| 7.1 | Add systemd service | `chezmoi add ~/.config/systemd/user/openclaw-gateway.service` |
| 7.2 | Export crontab | `crontab -l > crontab.txt && chezmoi add crontab.txt` |
| 7.3 | Create crontab restore script | `.chezmoiscripts/run_once_05-setup-crontabs.sh` |
| 7.4 | Add Cloudflare tunnel config | `chezmoi add ~/.cloudflared/` (template out secrets) |
| 7.5 | Add utility scripts | `chezmoi add ~/scripts/` |

**Feasibility**: HIGH — Standard system configs.

### Phase 8: Bootstrap Scripts (Day 3)

| Step | Action | File |
|------|--------|------|
| 8.1 | System packages installer | `run_once_before_00-system-packages.sh` |
| 8.2 | Docker installer | `run_once_before_01-docker-setup.sh` |
| 8.3 | AI model puller | `run_once_before_02-ai-models.sh` |
| 8.4 | Tool installer (starship, atuin, nvm, etc.) | `run_once_00-install-tools.sh` |
| 8.5 | Directory structure creator | `run_once_01-setup-dirs.sh` (reuses your `bootstrap_server_folders.sh`) |
| 8.6 | Docker network/image prep | `run_once_04-setup-docker-stacks.sh` |
| 8.7 | Monitoring setup | `run_once_08-setup-monitoring.sh` |

**Feasibility**: MEDIUM — Requires testing on clean server or container.

### Phase 9: Testing & Validation (Day 3-4)

| Step | Action | Details |
|------|--------|---------|
| 9.1 | Dry-run on current server | `chezmoi diff` to verify no destructive changes |
| 9.2 | Test in Docker container | Spin up Ubuntu container, run `chezmoi init --apply` |
| 9.3 | Verify all services start | Check Docker stacks, systemd services, cron |
| 9.4 | Verify AI agent system | Run `~/dotfiles/ai/setup.sh`, test a skill |
| 9.5 | Verify secrets flow | Ensure templates prompt correctly, no leaks |
| 9.6 | Run gitleaks | `gitleaks detect --source ~/.local/share/chezmoi` |

**Feasibility**: HIGH — Validation is straightforward.

### Phase 10: Publish & Document (Day 4)

| Step | Action | Details |
|------|--------|---------|
| 10.1 | Push to GitHub | `git remote add origin git@github.com:cbwinslow/dotfiles.git` |
| 10.2 | Set repo to private initially | Can go public after secret audit |
| 10.3 | Add GitHub Actions CI | Lint shell scripts, gitleaks scan |
| 10.4 | Write final README.md | One-command restore instructions |

---

## 6. What Goes Where — Decision Matrix

### Managed by Chezmoi (in repo)

- Shell configs (`.bashrc`, `.zshrc`, aliases, functions)
- Git config (`.gitconfig`, `.gitignore`)
- SSH config (NOT private keys)
- Starship, editor, terminal configs
- AI agent definitions, skills, workflows, setup scripts
- Docker compose files
- IaC templates (Ansible, Terraform, K8s)
- Monitoring configs (Prometheus, Grafana)
- Systemd service files
- Crontab entries
- Utility scripts and procedures
- MCP server configs (API keys templated)
- Firewall rules, package lists

### NOT in Repo (Generated/Excluded)

- SSH private keys (`~/.ssh/id_*`)
- `.ssh/known_hosts`
- Docker volume data (`/srv/docker/`)
- Terraform state (remote backend)
- AI model weights (`~/.ollama/`, model caches)
- Python venvs, node_modules
- Log files
- `__pycache__`, `.pyc`
- Chezmoi state DB (`chezmoistate.boltdb`)
- HuggingFace cache
- Large binary files

### Generated by Templates (`.tmpl`)

| File | Templated Content |
|------|-------------------|
| `dot_bash_secrets.tmpl` | DB password, Ollama URL |
| `dot_env_ai.tmpl` | API keys (OpenRouter, Gemini, etc.) |
| `dot_gitconfig` | GitHub token (from Bitwarden or prompt) |
| `private_dot_config/mcp/settings.json.tmpl` | MCP server API keys |
| `private_dot_ssh/config` | Host-specific SSH settings |
| `.chezmoi.toml.tmpl` | Machine hostname, GPU count, username |

---

## 7. Package Inventory for Bootstrap Scripts

### apt packages (system)

```
git curl wget htop tmux unzip jq tree ncdu iotop
docker.io docker-compose-v2
python3 python3-pip python3-venv
build-essential cmake
postgresql-client redis-tools
nfs-common cifs-utils
fail2ban ufw
```

### Tools installed via script

```
starship (prompt)
atuin (shell history)
nvm → node (latest LTS)
cargo (rust)
homebrew (linuxbrew)
pipx
ollama
```

### pip packages (global or pipx)

```
pipx
letta
audio-separator
gdown
huggingface-hui
```

### npm global packages

```
@anthropic-ai/claude-code
@openai/codex
@opencode-ai/cli
```

---

## 8. Security Considerations

1. **Leaked token**: The existing `ghp_ktq...` token in `~/.local/share/chezmoi/.git/config` must be revoked immediately
2. **Gitleaks**: Add `.gitleaks.toml` to the repo, run in CI
3. **Secretlint**: Pre-commit hook to catch secrets before push
4. **Age encryption**: Consider encrypting sensitive files with `age` (chezmoi supports this natively)
5. **Bitwarden integration**: Use chezmoi's Bitwarden template functions for secrets
6. **`.chezmoi.toml`**: Never committed — it's machine-local by design
7. **SSH keys**: Generated on each machine, never in the repo

---

## 9. Feasibility Assessment

| Phase | Risk | Effort | Blocker? |
|-------|------|--------|----------|
| 1. Foundation | None | 1 hour | No |
| 2. Shell config | None | 30 min | No |
| 3. Git & SSH | Low | 30 min | No |
| 4. AI agents | Medium (size) | 2 hours | Need to triage 290MB |
| 5. MCP & tools | None | 30 min | No |
| 6. Docker & IaC | Low | 2 hours | No |
| 7. System services | None | 30 min | No |
| 8. Bootstrap scripts | Medium (testing) | 3 hours | Need clean env test |
| 9. Testing | Medium | 2 hours | Need container |
| 10. Publish | None | 30 min | No |

**Total estimated effort**: 12-15 hours across 3-4 days.

### Key Risks

| Risk | Mitigation |
|------|------------|
| 290MB AI skills dir bloats repo | Triage: core configs in repo, large files via `.chezmoiexternal.toml` |
| Bootstrap script fails on clean server | Test in Docker container first |
| Secrets leak into public repo | Gitleaks + secretlint pre-commit, start with private repo |
| Chezmoi state conflicts with existing files | `chezmoi diff` before every `apply` |
| Symlinks break | Document all symlinks, recreate in run_once scripts |

---

## 10. Next Steps

1. **Approve this plan** — Confirm the structure and approach
2. **Revoke the leaked GitHub token** — Immediate security action
3. **Start Phase 1** — Foundation scaffolding
4. **Work through phases sequentially** — Each phase is independent and testable
5. **Test in Docker** — Before touching the production server

---

## References

- Chezmoi docs: https://chezmoi.io
- Chezmoi user guide: https://chezmoi.io/user-guide/setup/
- martinemde/dotfiles (AI-first chezmoi): https://github.com/martinemde/dotfiles
- mizchi/chezmoi-dotfiles (Python/shell): https://github.com/mizchi/chezmoi-dotfiles
- natelandau/dotfiles (bootstrap-focused): https://github.com/natelandau/dotfiles
- andrewbrey/dotfiles (multi-platform chezmoi+deno): https://github.com/andrewbrey/dotfiles
