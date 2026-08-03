---
title: LangChain Fundamentals
type: concept
category: langchain-ai
tags:
  - llm
  - ai
  - chains
  - agents
  - langchain
aliases:
  - langchain-concept
  - lc-fundamentals
status: active
created: 2026-04-27
updated: 2026-04-27
id: langchain-ai.langchain-fundamentals
version: "1.0.0"
confidence: high
source: docs
---

# LangChain Fundamentals

## Overview
LangChain is a framework for building applications with large language models (LLMs). It provides abstractions for chains, agents, memory, and tools that make it easy to build LLM-powered applications.

## Purpose
LangChain enables:
- Chain multiple LLM calls
- Connect LLMs to data sources
- Build autonomous agents
- Manage conversation memory
- Use tools and external APIs

## Content

### Core Components

#### Chains
Sequence of LLM calls:
```python
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
prompt = PromptTemplate.from_template("Summarize: {text}")
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.invoke({"text": "Long document..."})
```

#### Agents
Autonomous decision-makers with tools:
```python
from langchain.agents import create_openai_agent
from langchain.tools import Tool

tools = [
    Tool(name="search", func=search_fn, description="Search the web"),
]

agent = create_openai_agent(llm, tools, prompt)
result = agent.invoke({"input": "What's the weather?"})
```

#### Memory
Conversation state persistence:
```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)
chain.invoke({"input": "Hi! I'm John"})
chain.invoke({"input": "What's my name?"})  # Remembers "John"
```

#### Chat Models
| Model | Provider |
|-------|----------|
| ChatOpenAI | OpenAI |
| ChatAnthropic | Anthropic |
| ChatGoogleGenerativeAI | Google |
| ChatMistralAI | Mistral |

### Architecture

```
┌─────────────────────────────────────────┐
│           Application                   │
├─────────────────────────────────────────┤
│  Chains → Agents → Tools                │
├─────────────────────────────────────────┤
│  Memory (Buffer, KG, Summary)           │
├─────────────────────────────────────────┤
│  LLM Providers (OpenAI, Anthropic...)   │
└─────────────────────────────────────────┘
```

## Usage

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm
result = chain.invoke({"input": "Hello!"})
```

## Relationships
- [[langchain-getting-started]]
- [[langchain-components]]

## Notes
- LangChain has multiple versions (0.1, 0.2, 0.3)
- Use langchain-core for core abstractions
- LangGraph for complex agent graphs
- LCEL for composable chains

## References
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)