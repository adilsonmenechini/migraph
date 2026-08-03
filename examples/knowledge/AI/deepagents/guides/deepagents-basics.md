---
title: Deep Agents Basics
type: guide
category: deepagents
tags:
  - tutorial
  - getting-started
  - python
aliases:
  - deepagents-tutorial
  - deep-agents-basics
status: active
created: 2026-04-27
updated: 2026-04-27
id: deepagents.basics
version: "1.0.0"
confidence: high
source: docs
---

# Deep Agents Basics

## Overview
A practical guide to getting started with Deep Agents - from installation to your first autonomous agent.

## Purpose
Learn Deep Agents fundamentals:
- Installing Deep Agents
- Creating your first agent
- Adding tools and memory
- Running agent tasks

## Content

### Installation

```bash
# Install deepagents
pip install deepagents

# Install with specific provider
pip install deepagents langchain-openai
pip install deepagents langchain-anthropic
pip install deepagents langchain-google-genai
```

### Your First Agent

```python
from deepagents import create_deep_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# Create agent
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

### With Different Providers

```python
# OpenAI
agent = create_deep_agent(
    model="openai:gpt-5.4",
    tools=[my_tool],
    system_prompt="You are a helpful assistant",
)

# Google
agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[my_tool],
    system_prompt="You are a helpful assistant",
)

# Ollama (local)
agent = create_deep_agent(
    model="ollama:devstral-2",
    tools=[my_tool],
    system_prompt="You are a helpful assistant",
)
```

### Filesystem Tools

Deep Agents includes built-in filesystem tools:

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    include_filesystem=True,  # Enables ls, read_file, write_file tools
)
```

### Planning with Todos

```python
# Agent automatically gets write_todos tool for task planning
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    include_todo=True,  # Enables task decomposition
)
```

### Subagent Spawning

```python
# Create agent with subagent capability
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    include_subagents=True,  # Enables task tool for spawning subagents
)
```

## Usage Examples

### Complete Example

```python
from deepagents import create_deep_agent

# Define tools
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

def write_file(path: str, content: str) -> str:
    """Write to file."""
    return f"Written to {path}"

# Create agent with multiple capabilities
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[search, write_file],
    system_prompt="You are a research assistant.",
    include_todo=True,
    include_filesystem=True,
)

# Run complex task
result = agent.invoke({
    "messages": [{
        "role": "user", 
        "content": "Research AI trends and save a summary to file"
    }]
})
```

### With LangSmith Tracing

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-key"

# Now all agent calls are traced
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[my_tool],
)
```

## Relationships
- [[deepagents-architecture]]
- [[deepagents-commands]]

## Notes
- Start simple, add capabilities as needed
- Use `include_todo` for planning
- Use `include_filesystem` for file operations
- Use `include_subagents` for delegation
- LangSmith helps debug agent behavior

## References
- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [Quickstart Guide](https://docs.langchain.com/oss/python/deepagents/quickstart/)
- [Customization Guide](https://docs.langchain.com/oss/python/deepagents/customization/)
- [API Reference](https://reference.langchain.com/python/deepagents/)