---
title: Deep Agents Reference
type: reference
category: deepagents
tags:
  - commands
  - api
  - cheatsheet
aliases:
  - deepagents-api
  - deep-agents-reference
status: active
created: 2026-04-27
updated: 2026-04-27
id: deepagents.commands
version: "1.0.0"
confidence: high
source: docs
---

# Deep Agents Reference

## Overview
Quick reference for Deep Agents API, functions, and configuration options.

## Purpose
This is a command reference - use this when you need to:
- Remember a specific function
- Check available options
- Find the right configuration

## Content

### Core Functions

| Function | Description |
|----------|-------------|
| `create_deep_agent()` | Create an agent with tools and capabilities |
| `invoke()` | Run the agent with input |
| `stream()` | Stream agent responses |
| `batch()` | Run agent on multiple inputs |

### create_deep_agent Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model name (provider:model format) |
| `tools` | list[Tool] | Custom tools |
| `system_prompt` | string | Agent instructions |
| `include_todo` | bool | Enable task planning (default: false) |
| `include_filesystem` | bool | Enable file operations (default: false) |
| `include_subagents` | bool | Enable subagent spawning (default: false) |
| `include_skills` | bool | Enable skills (default: false) |
| `memory` | list[str] | Memory configuration |
| `backend` | BackendProtocol | Filesystem backend |
| `checkpointer` | Checkpointer | State persistence |
| `store` | BaseStore | Long-term storage |

### Model Provider Format

| Provider | Format Example |
|----------|---------------|
| Anthropic | `anthropic:claude-sonnet-4-6` |
| OpenAI | `openai:gpt-5.4` |
| Google | `google_genai:gemini-3.1-pro-preview` |
| OpenRouter | `openrouter:anthropic/claude-sonnet-4-6` |
| Fireworks | `fireworks:accounts/fireworks/models/qwen3p5-397b-a17b` |
| Ollama | `ollama:devstral-2` |

### Built-in Tools

| Tool | Description |
|------|-------------|
| `write_todos` | Task planning and decomposition |
| `task` | Spawn subagents |
| `ls` | List directory contents |
| `read_file` | Read file content |
| `write_file` | Write to file |
| `edit_file` | Edit file content |
| `execute` | Run shell commands (sandbox only) |

### Backends

| Backend | Description |
|---------|-------------|
| `StateBackend` | In-memory state |
| `StoreBackend` | Persistent across threads |
| `SandboxBackend` | Isolated code execution |
| `CompositeBackend` | Multiple backends combined |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `LANGSMITH_TRACING` | Enable tracing |
| `LANGSMITH_API_KEY` | LangSmith API key |
| `OPENAI_API_KEY` | OpenAI models |
| `ANTHROPIC_API_KEY` | Anthropic models |

## Usage Examples

### Basic Agent

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[my_tool],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
```

### With Capabilities

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    include_todo=True,         # Task planning
    include_filesystem=True,   # File operations
    include_subagents=True,    # Subagent spawning
)
```

### Streaming

```python
for chunk in agent.stream({"messages": [{"role": "user", "content": "Hello"}]}):
    print(chunk, end="", flush=True)
```

## Relationships
- [[deepagents-architecture]]
- [[deepagents-basics]]

## Notes
- Use provider:model format for models
- Include capabilities with boolean flags
- LangSmith for debugging and tracing

## References
- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [API Reference](https://reference.langchain.com/python/deepagents/)
- [Customization Guide](https://docs.langchain.com/oss/python/deepagents/customization/)