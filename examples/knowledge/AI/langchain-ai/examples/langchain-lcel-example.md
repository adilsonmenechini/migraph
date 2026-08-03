---
title: LangChain LCEL Example
type: example
category: langchain-ai
tags:
  - example
  - code
  - sample
  - lcel
  - chain
aliases:
  - langchain-example
  - lc-example
status: active
created: 2026-04-27
updated: 2026-04-27
id: langchain-ai.langchain-lcel-example
version: "1.0.0"
confidence: high
source: docs
---

# LangChain LCEL Example

## Overview
Practical example demonstrating how to create a chain using LCEL (LangChain Expression Language), based on official documentation.

## Code

### Basic LCEL Chain

```python
# Install: pip install langchain langchain-openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful coding assistant."),
    ("user", "Explain {topic} in 3 bullet points.")
])

# 2. Initialize model
model = ChatOpenAI(model="gpt-4o")

# 3. Create output parser
parser = StrOutputParser()

# 4. Build chain with pipe operator (|)
chain = prompt | model | parser

# 5. Invoke
result = chain.invoke({"topic": "async programming in Python"})
print(result)
```

## Explanation

- **Pipe operator (|)**: Connects components in sequence
- **ChatPromptTemplate**: Creates prompts with variables
- **ChatOpenAI**: LLM integration
- **StrOutputParser**: Converts response to string
- **invoke()**: Runs the chain with input

## With Tools (Agent)

```python
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: sunny, 22°C"

# Create agent with tools
agent = create_agent(
    model="openai:gpt-4o",
    tools=[get_weather],
    system_prompt="You are a helpful assistant.",
)

# Run agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Tokyo?"}]}
)
```

## Streaming

```python
# Stream responses for better UX
for chunk in chain.stream({"topic": "LCEL"}):
    print(chunk, end="", flush=True)
```

## Related
- [[langchain-getting-started]]
- [[langchain-fundamentals]]

## References
- [LangChain LCEL Tutorial](https://python.langchain.com/docs/how_to/lcel_cheatsheet)
- [LangChain Documentation](https://python.langchain.com/)