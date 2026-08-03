---
title: Deep Agents Quickstart Example
type: example
category: deepagents
tags:
  - example
  - code
  - sample
  - quickstart
aliases:
  - deepagents-example
  - deep-agents-quickstart
status: active
created: 2026-04-27
updated: 2026-04-27
id: deepagents.quickstart
version: "1.0.0"
confidence: high
source: docs
---

# Deep Agents Quickstart Example

## Overview
Practical example demonstrating how to create and run a Deep Agent, based on official documentation at https://docs.langchain.com/oss/python/deepagents/overview

## Code

### Basic Agent (Anthropic)

```python
# pip install -qU deepagents langchain-anthropic
from deepagents import create_deep_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

### With OpenAI

```python
# pip install -qU deepagents langchain-openai
from deepagents import create_deep_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_deep_agent(
    model="openai:gpt-5.4",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

### With Planning (Todos)

```python
from deepagents import create_deep_agent

# include_todo=True adds write_todos tool for task planning
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    include_todo=True,
)

# Agent will break down complex tasks into steps
agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Create a Python web scraper and save it to file"
    }]
})
```

### With Filesystem Access

```python
from deepagents import create_deep_agent

# include_filesystem=True adds ls, read_file, write_file tools
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    include_filesystem=True,
)

# Agent can read/write files
agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Read the config.json file and summarize it"
    }]
})
```

## Explanation

- **model**: Uses `provider:model` format (e.g., `anthropic:claude-sonnet-4-6`)
- **tools**: Custom functions the agent can call
- **system_prompt**: Defines agent behavior
- **include_todo**: Enables task planning
- **include_filesystem**: Enables file operations
- **invoke()**: Runs agent with input messages

## When to Use Deep Agents

Use Deep Agents when building agents that:
- Handle complex, multi-step tasks
- Need task planning and decomposition
- Require filesystem context management
- Need to delegate to subagents
- Need persistent memory across threads

## Related
- [[deepagents-basics]]
- [[deepagents-architecture]]

## References
- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [Quickstart Guide](https://docs.langchain.com/oss/python/deepagents/quickstart/)
- [API Reference](https://reference.langchain.com/python/deepagents/)