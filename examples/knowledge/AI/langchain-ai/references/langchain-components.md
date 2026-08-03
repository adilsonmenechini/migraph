---
title: LangChain Components
type: reference
category: langchain-ai
tags:
  - components
  - api
  - cheatsheet
aliases:
  - langchain-api
  - lc-components
status: active
created: 2026-04-27
updated: 2026-04-27
id: langchain-ai.langchain-components
version: "1.0.0"
confidence: high
source: docs
---

# LangChain Components

## Overview
Quick reference for LangChain components, modules, and common patterns.

## Purpose
This is a reference - use this when you need to:
- Find the right component
- Check available integrations
- Remember common patterns

## Content

### Chat Models

| Class | Provider |
|-------|----------|
| `ChatOpenAI` | OpenAI GPT models |
| `ChatAnthropic` | Anthropic Claude models |
| `ChatGoogleGenerativeAI` | Google Gemini |
| `ChatMistralAI` | Mistral models |
| `ChatCohere` | Cohere models |

### Prompt Templates

| Template | Description |
|----------|-------------|
| `PromptTemplate` | Simple variable substitution |
| `ChatPromptTemplate` | Messages-based prompts |
| `MessagesPlaceholder` | Dynamic message lists |
| `FewShotPromptTemplate` | Few-shot learning |

### Chains

| Chain | Use Case |
|-------|----------|
| `LLMChain` | Simple LLM + prompt |
| `ConversationChain` | With memory |
| `RetrievalQA` | RAG question answering |
| `SequentialChain` | Multi-step |
| `RouterChain` | Dynamic routing |

### Memory Types

| Type | Description |
|------|-------------|
| `ConversationBufferMemory` | Full history |
| `ConversationBufferWindowMemory` | Last N messages |
| `ConversationSummaryMemory` | Summarized history |
| `EntityMemory` | Entity facts |
| `KGBufferMemory` | Knowledge graph |

### Output Parsers

| Parser | Output |
|--------|--------|
| `StrOutputParser` | String |
| `PydanticOutputParser` | Pydantic model |
| `JSONOutputParser` | JSON |
| `CommaSeparatedListOutputParser` | List |
| `XMLOutputParser` | XML/HTML |

### Tools & Retriers

#### Built-in Tools
| Tool | Description |
|------|-------------|
| `WikipediaQueryRun` | Wikipedia search |
| `WolframAlphaQueryRun` | Math/Wolfram |
| `GoogleSearchRun` | Google search |
| `PythonREPLTool` | Python execution |

#### Retriever Types
| Retriever | Description |
|-----------|-------------|
| `VectorstoreRetriever` | Similarity search |
| `ContextualCompressionRetriever` | Compressed docs |
| `EnsembleRetriever` | Multiple sources |

### Agents

| Agent | Description |
|-------|-------------|
| `create_openai_agent` | OpenAI function calling |
| `create_react_agent` | ReAct pattern |
| `create_self_ask_with_search_agent` | Self-ask with search |
| `create_structured_chat_agent` | Structured output |

### LCEL Operators

| Operator | Description |
|----------|-------------|
| `|` | Pipe/chain |
| `+` | Concatenate |
| `*` | Repeat |
| `.bind()` | Bind parameters |

## Usage Examples

### Complete RAG Pipeline

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Embeddings
embeddings = OpenAIEmbeddings()

# Vector store
vectorstore = Chroma.from_documents(docs, embeddings)

# RAG chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
```

### Conversation with Summary

```python
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain

memory = ConversationSummaryMemory(llm=ChatOpenAI())
chain = ConversationChain(
    llm=ChatOpenAI(),
    memory=memory,
)
```

### Tool Binding

```python
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI

llm = ChatOpenAI().bind(
    functions=[format_tool]
)
```

## Relationships
- [[langchain-fundamentals]]
- [[langchain-getting-started]]

## Notes
- Use LCEL for composability
- Chat models preferred over legacy
- Memory is pluggable
- Many integrations in community

## References
- [API Reference](https://api.python.langchain.com/)
- [Integrations](https://python.langchain.com/docs/integrations/)