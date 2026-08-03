---
title: Deep Agents Architecture
type: concept
category: deepagents
tags:
  - ai-agents
  - orchestration
  - autonomous-agents
  - langchain
  - langgraph
aliases:
  - deepagents-concept
  - deep-agents-architecture
status: active
created: 2026-04-27
updated: 2026-04-27
id: deepagents.architecture
version: "1.0.0"
confidence: high
source: docs
---

# Deep Agents Architecture

## Overview
Deep Agents is an "agent harness" built on top of [LangChain](langchain) and [LangGraph](langgraph) for building autonomous AI agents. It provides built-in capabilities for task planning, file systems, subagent spawning, and long-term memory.

## Purpose
Deep Agents is designed for complex, multi-step tasks that require:
- Planning and task decomposition
- Context management via filesystem tools
- Subagent delegation
- Persistent memory across conversations
- Human-in-the-loop approval

## Content

### What is Deep Agents?

Deep Agents is a **standalone library** built on LangChain's core building blocks. It uses the [LangGraph](langgraph) runtime for:
- Durable execution
- Streaming
- Human-in-the-loop
- Checkpointing

### Core Components

#### create_deep_agent()
Primary function for agent creation:
```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[my_tool],
    system_prompt="You are a helpful assistant",
)
```

#### Supported Models
| Provider | Model Example |
|----------|---------------|
| OpenAI | `openai:gpt-5.4` |
| Anthropic | `anthropic:claude-sonnet-4-6` |
| Google | `google_genai:gemini-3.1-pro-preview` |
| OpenRouter | `openrouter:anthropic/claude-sonnet-4-6` |
| Fireworks | `fireworks:accounts/fireworks/models/qwen3p5-397b-a17b` |
| Ollama | `ollama:devstral-2` |

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Planning** | Built-in `write_todos` tool for task decomposition |
| **Context Management** | Filesystem tools (ls, read_file, write_file, edit_file) |
| **Shell Execution** | `execute` tool via sandbox backends |
| **Filesystem Backends** | Pluggable backends (memory, disk, sandbox, composite) |
| **Subagent Spawning** | `task` tool for context isolation |
| **Long-term Memory** | LangGraph Memory Store integration |
| **Permissions** | Declarative rules for filesystem access |
| **Human-in-the-loop** | Interrupt capabilities for approval |
| **Skills** | Reusable specialized workflows |

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Deep Agents SDK                       │
├─────────────────────────────────────────────────────────┤
│  create_deep_agent() → CompiledStateGraph              │
├─────────────────────────────────────────────────────────┤
│  Tools: write_todos, task, ls, read_file, write_file  │
├─────────────────────────────────────────────────────────┤
│  Backends: StateBackend, StoreBackend, SandboxBackend  │
├─────────────────────────────────────────────────────────┤
│              LangGraph Runtime                          │
├─────────────────────────────────────────────────────────┤
│    LangChain (prompts, tools, output parsers)          │
└─────────────────────────────────────────────────────────┘
```

## Relationships
- [[deepagents-basics]]
- [[deepagents-commands]]
- [[langchain-fundamentals]]
- [[langgraph-fundamentals]]

## Notes
- Deep Agents is provider-agnostic - works with any model supporting tool calling
- Ships with opinionated system prompts
- Can use LangSmith for tracing and debugging
- Different from LangChain's `create_agent` - for complex multi-step tasks

## References
- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [GitHub Repository](https://github.com/langchain-ai/deepagents)
- [API Reference](https://reference.langchain.com/python/deepagents/)