---
id: patterns.clawteam-swarm
title: ClawTeam - Agent Swarm Intelligence
type: pattern
domain: patterns
tags:
  - patterns
  - ai-agents
  - swarm
  - multi-agent
  - orchestration
  - clawteam
  - hku
summary: Pattern for enabling AI agents to form collaborative swarms that self-organize, delegate tasks, and coordinate execution without human intervention.
related:
  - [[deepagents-architecture]]
  - [[deepagents-basics]]
source: https://github.com/HKUDS/ClawTeam
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 90
---

# ClawTeam - Agent Swarm Intelligence

## Definition
ClawTeam is a framework that enables AI agents to form collaborative swarms - where multiple agents self-organize, intelligently divide complex work, share insights in real-time, and coordinate execution without human intervention. It transforms solo AI agents into team-based intelligence.

## Key Concepts

### From Solo to Swarm

| Approach | Description |
|----------|-------------|
| **Solo Agent** | Single AI agent working in isolation manually coordinated |
| **Swarm** | Multiple agents that self-organize and collaborate autonomously |

ClawTeam solves the problem of manually coordinating multiple AI agents when facing complex tasks.

### Core Features

1. **Agent Self-Organization**: Leader agents spawn and manage worker agents with auto-injected coordination prompts
2. **Workspace Isolation**: Each agent gets its own git worktree (separate branch) - no merge conflicts
3. **Task Tracking with Dependencies**: Kanban-style tracking with `--blocked-by` chains that auto-unblock
4. **Inter-Agent Messaging**: Inboxes for point-to-point communication between agents
5. **Monitoring & Dashboards**: `board attach` for tiled tmux view of all agents

## Architecture

### How It Works

```
Human prompt: "Build a full-stack todo app."

🦞 Leader agent's actions:
├── 🏗️ clawteam team spawn-team webapp
├── 📋 Created tasks with dependency chains:
│   ├── T1: "Design REST API" → architect
│   ├── T2: "Implement auth" --blocked-by T1 → backend1
│   ├── T3: "Build database" --blocked-by T1 → backend2
│   ├── T4: "Build React UI" → frontend
│   └── T5: "Integration tests" --blocked-by T2,T3,T4 → tester
├── 🚀 Spawned 5 sub-agents (each in its own git worktree)
├── 🔗 Dependency auto-resolution
├── 💬 Sub-agents coordinate via inbox
└── 🌳 Leader merges all worktrees into main
```

### CLI Commands

```bash
# Create a team (you become the leader)
clawteam team spawn-team my-team -d "Build the auth module"

# Spawn worker agents - each gets git worktree, tmux window, identity
clawteam spawn --team my-team --agent-name alice --task "Implement OAuth2"

# Workers auto-receive coordination prompt to:
# - Check tasks: clawteam task list my-team --owner alice
# - Update status: clawteam task update my-team <id> --status completed
# - Message leader: clawteam inbox send my-team leader "Done!"

# Watch them work side-by-side
clawteam board attach my-team
```

## Usage Context

### When to Use ClawTeam

- Complex multi-module tasks that require different expertise
- Large-scale experiments (e.g., ML hyperparameter tuning across GPUs)
- Collaborative software engineering projects
- Research automation requiring parallel exploration

### Supported Agents

| Agent | Spawn Command |
|-------|-------------|
| Claude Code | `clawteam spawn tmux claude --team ...` |
| Codex | `clawteam spawn tmux codex --team ...` |
| OpenClaw | `clawteam spawn tmux openclaw --team ...` |
| nanobot | `clawteam spawn tmux nanobot --team ...` |
| Kimi CLI | `clawteam spawn tmux kimi --team ...` |

### Prerequisites

- Python 3.10+
- tmux installed
- A CLI coding agent (Claude Code, Codex, etc.)

## Installation

```bash
pip install clawteam

# Or from source
git clone https://github.com/HKUDS/ClawTeam.git
cd ClawTeam
pip install -e .
```

## Trade-offs

| Aspect | Benefit | Risk |
|--------|---------|------|
| Multi-agent | Parallel execution, diverse expertise | Coordination complexity |
| Git worktrees | No merge conflicts | Branch proliferation |
| Auto-injected prompts | Zero manual setup | Magic behavior, harder debugging |
| Any CLI agent | Flexibility | Agent-specific quirks |

## Related

- [[deepagents-architecture]] - Deep Agents architecture
- [[deepagents-basics]] - Deep Agents basics

## References

- [ClawTeam GitHub](https://github.com/HKUDS/ClawTeam)
- [ClawTeam Docs](https://github.com/HKUDS/ClawTeam#-quick-start)
- [AutoResearch Example](https://github.com/karpathy/autoresearch)