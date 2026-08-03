---
title: LangChain
type: reference
category: AI
domain: llm
created: 2026-08-03
updated: 2026-08-03
tags:
  - langchain
  - llm
  - agents
  - python
status: active
id: llm.reference.langchain
version: "1.0.0"
confidence: high
source: https://docs.langchain.com/oss/python/langchain/overview
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: [langchain framework]
summary: LangChain é o framework para construir aplicações com LLMs — create_agent combina model + tools + prompt + middleware em um agente executável, com ecossistema de integrações e composição via Runnable.
---

# LangChain

## 🧠 Definition

LangChain é um framework para construir aplicações com **LLMs** (agentes, RAG, chatbots, workflows). O conceito central moderno é o **Agent**: `Agent = Model + Harness`. O **harness** (create_agent) junta model + tools + system prompt + middleware em um executável único com loop de tool calls embutido.

## 📚 Explanation

### create_agent (o harness)

```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Retorna o clima atual de uma cidade."""
    return f"Sunny, 25°C in {city}"

agent = create_agent(
    model="gpt-5.5",                     # ou ChatModel instance
    tools=[get_weather],                 # lista de tools
    system_prompt="You are a helpful weather assistant.",
    middleware=[],                        # error handling, HITL, retry
)

result = agent.invoke({"messages": [{"role": "user", "content": "Weather in Berlin?"}]})
print(result["messages"][-1].content_blocks)
```

- `create_agent` constrói o **AgentExecutor** com loop de tool calls: model → tool call → executa → observa → repete.
- O resultado final é a última mensagem (`content_blocks` para conteúdo estruturado).
- Middleware pode interceptar (human-in-the-loop, retries, logging).

### LangChain vs LangGraph vs Deep Agents

| Camada | Foco | Uso |
|--------|------|-----|
| **LangChain** | `create_agent` + componentes (tools, models, RAG) | agentes com batteries-included, customizáveis |
| **LangGraph** | orquestração low-level com StateGraph | controle fino de estado, loops, branching |
| **Deep Agents** | agentes prontos com tooling (playwright, browser) | autonomia full-stack, integração IDE |

### Estrutura de pacotes

- `langchain-core`: abstrações base — BaseChatModel, BaseTool, Runnable, prompts, output parsers.
- `langchain`: components — agents, chains, document loaders, retrievers.
- `langchain-community`: integrações da comunidade (vector stores, tools, memory).
- `langchain-openai` / `langchain-anthropic` / etc.: wrappers oficiais de providers.

### Padrões comuns

- **Tool decorator**: `@tool` transforma função Python com docstring em tool executável.
- **init_chat_model**: carrega qualquer modelo por string (`init_chat_model("gpt-5.5")`).
- **Runnable composition**: `prompt | model | parser` (LCEL) — pipeline composável e streamable.
- **with_structured_output**: modelo retorna Pydantic/Zod schema validado.

## 🔗 Related

- [[LangGraph]]
- [[AI Agents]]
- [[GraphRAG]]

## 🧩 Key Insights

- `create_agent` = "agent out of the box": model + tools + prompt + middleware em uma linha.
- LCEL (`|`) torna pipelines testáveis e streamable.
- LangChain e LangGraph são complementares: comece com LangChain, desça para LangGraph quando precisar de controle.
- Middleware é o ponto de extensão para HITL e error handling.

## ⚠️ Trade-offs

- Abstrações mudam rápido — seguir a documentação da versão instalada.
- "Agent out of the box" pode esconder o loop; para controle fino use LangGraph.
- Muitas integrações (community) variam em maturidade.

## 📊 Observability

- **SLIs**: agent turn count, tool call success rate, latency per step
- **SLOs**: task completion > 95%, tool success > 99%
- **Metrics**: LangSmith traces, token usage, step duration

## 🔐 Security Considerations

- API keys via env vars / secret manager (nunca no código).
- Validação de tool inputs; allowlist de tools perigrosas.
- Prompt injection: sanear input do usuário; separar system prompt de user content.
- Middleware de approval para tool calls destrutivas.

## 🏗️ Usage Context

- Quando usar: agentes com tools, RAG, chatbots, pipelines LLM com integrações.
- Quando NÃO usar: orquestração complexa com branches/loops explícitos (use LangGraph); agentes full-autonomy (use Deep Agents).
- Pré-requisitos: Python 3.9+, API key de um provider.

## 📚 References

- [LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain Docs](https://docs.langchain.com/)
- [LangChain vs LangGraph vs Deep Agents](https://docs.langchain.com/oss/python/langchain/overview)
- [Agents concepts](https://docs.langchain.com/oss/python/langchain/agents)
