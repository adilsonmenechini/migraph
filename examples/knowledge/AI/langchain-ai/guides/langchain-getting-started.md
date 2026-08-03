---
title: LangChain Getting Started
type: guide
category: langchain-ai
tags:
  - tutorial
  - getting-started
  - python
aliases:
  - langchain-tutorial
  - lc-getting-started
status: active
created: 2026-04-27
updated: 2026-04-27
---

# LangChain Getting Started

## Overview
A practical guide to getting started with LangChain - from installation to your first LLM application.

## Purpose
Learn LangChain fundamentals:
- Installing LangChain
- Creating your first chain
- Using prompts and output parsers
- Building simple agents

## Content

### Installation

```bash
# Core
pip install langchain-core

# OpenAI
pip install langchain-openai

# Anthropic
pip install langchain-anthropic

# All integrations
pip install langchain[all]

# Community
pip install langchain-community
```

### Your First Chain

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

# 1. Initialize LLM
llm = ChatOpenAI(model="gpt-4")

# 2. Create prompt
prompt = PromptTemplate.from_template(
    "Explain {topic} in {level} detail."
)

# 3. Create chain
chain = prompt | llm | StrOutputParser()

# 4. Invoke
result = chain.invoke({
    "topic": "quantum computing",
    "level": "simple"
})
print(result)
```

### Using Chat Models

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4")

messages = [
    SystemMessage(content="You are a Python expert."),
    HumanMessage(content="What is a decorator?")
]

response = llm.invoke(messages)
print(response.content)
```

### Building an Agent

```python
from langchain.agents import create_openai_agent
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-4")

def search(query: str) -> str:
    return f"Results for: {query}"

tools = [
    Tool(
        name="search",
        func=search,
        description="Search for information"
    )
]

agent = create_openai_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({
    "input": "Search for AI trends in 2026"
})
```

### Adding Memory

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# First interaction
conversation.invoke({"input": "My favorite color is blue"})

# Second - remembers previous
conversation.invoke({"input": "What's my favorite color?"})
```

### Using Tools

```python
from langchain.tools import tool

@tool
def calculate(expression: str) -> float:
    """Evaluate a math expression."""
    return eval(expression)

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: sunny, 25°C"

# Use with agent
tools = [calculate, get_weather]
```

## Usage Examples

### With Output Parsers

```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class Answer(BaseModel):
    question: str
    answer: str
    confidence: float

parser = PydanticOutputParser(pydantic_object=Answer)

prompt = PromptTemplate(
    template="Answer: {question}\n{format_instructions}",
    input_variables=["question"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | llm | parser
result = chain.invoke({"question": "What is AI?"})
```

### With RAG

```python
from langchain.retrievers import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Create retriever
vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# Create RAG chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=retriever,
)

result = qa.invoke({"query": "What is LangChain?"})
```

## Relationships
- [[langchain-fundamentals]]
- [[langchain-components]]

## Notes
- Start with LCEL (LangChain Expression Language)
- Use Chat models over legacy LLM
- Memory enables conversation continuity
- Tools extend agent capabilities

## References
- [LangChain Tutorials](https://python.langchain.com/docs/tutorials/)
- [LCEL Guide](https://python.langchain.com/docs/expression_language/)