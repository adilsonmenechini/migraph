---
title: LangGraph
type: reference
category: AI
domain: llm
created: 2026-08-03
updated: 2026-08-03
tags:
  - langgraph
  - langchain
  - state-machine
  - agents
status: active
id: llm.reference.langgraph
version: "1.0.0"
confidence: high
source: https://docs.langchain.com/oss/python/langgraph/use-graph-api
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: [langgraph framework]
summary: LangGraph é a camada de orquestração low-level do ecossistema LangChain — modela agentes como grafos de estado (StateGraph) com nós, arestas, branches e loops, checkpointing e controle fino de fluxo.
---

# LangGraph

## 🧠 Definition

LangGraph é um framework para **orquestração de agentes como grafos de estado**. Você define um **State** tipado, **nós** (funções) que o processam e **arestas** que conectam os nós — com suporte a branches, loops, **Send API** (map-reduce) e **Command API** (controle de fluxo dinâmico). Persistência via checkpointers habilita time travel e memória.

## 📚 Explanation

### State (o coração do grafo)

```python
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]   # reducer: concatena
    query: str
```

- State pode ser `TypedDict`, Pydantic model ou dataclass.
- **Reducers** (`Annotated[list, operator.add]`) definem como updates se acumulam.
- Cada nó recebe o state e retorna um **update parcial** (`{"messages": [new_msg]}`).

### StateGraph

```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)
graph.add_edge("agent", "tools")            # aresta fixa
graph.add_conditional_edges("tools", should_continue,
    {"continue": "agent", "end": END})      # branch
app = graph.compile(checkpointer=memory)
```

- `add_node`: registra função de nó.
- `add_edge` / `add_conditional_edges`: conectam nós; `END` encerra.
- Loops: aresta de volta a um nó anterior.
- `compile()`: gera o executável; checkpointer opcional.

### Command API (controle dinâmico)

```python
return Command(
    update={"messages": [msg]},   # state update
    goto="tools",                 # próximo nó (pode ser condicional)
)
```

- Combina **state update** com **"hop" para outro nó** em um único retorno.
- Permite roteamento dinâmico sem conditional edges explícitas.
- `Command(resume=...)` para retomar após `interrupt()`.

### Send API (map-reduce / paralelismo)

```python
from langgraph.types import Send

return [Send("analyze_chunk", {"chunk": c}) for c in chunks]
```

- Dispara **múltiplas invocações paralelas** do mesmo nó com inputs diferentes.
- Padrão para fan-out (ex.: processar N documentos) seguido de agregação.

### Checkpointing e memória

- **Checkpointer** (ex.: `InMemorySaver`, `SqliteSaver`) persiste o state por `thread_id`.
- **Time travel**: `get_state_history()` / `update_state()` para navegar/ramificar execuções.
- **interrupt()**: pausa para human-in-the-loop; `Command(resume=...)` retoma.
- Subgraphs: grafos aninhados com escopo de checkpointer configurável.

### Streaming

```python
for event in app.stream(input, stream_mode="messages"):
    print(event)
```

- `stream_mode="values"` (state a cada passo), `"updates"` (deltas), `"messages"` (tokens streaming).

## Connections

- [LangChain](langchain.md)
- [AI Agents](../topics/ai-agents.md)

## 🧩 Key Insights

- LangGraph é a camada de orquestração: para controle fino de estado/fluxo, não agente "out of the box".
- Reducers definem a semântica de acumulação de state — essencial para `messages`.
- `Send` habilita paralelismo explícito; `Command` dá roteamento dinâmico.
- Checkpointer + `thread_id` = conversas multi-turn com memória; time travel para debugging.

## ⚠️ Trade-offs

- API de mais baixo nível: mais código e responsabilidade que `create_agent`.
- Grafo explícito exige design prévio do fluxo.
- Reducers mal definidos causam bugs sutis de state.

## 📊 Observability

- **SLIs**: node execution time, loop iterations, checkpointer ops
- **SLOs**: graph completion > 95%, time travel recoverable
- **Metrics**: LangSmith traces por node, stream events, checkpoint size

## 🔐 Security Considerations

- Checkpointers persistem dados sensíveis — criptografar em repouso.
- `interrupt()` para approval de ações destrutivas.
- Validar inputs de nós que executam tools externas.

## 🏗️ Usage Context

- Quando usar: agentes com fluxo complexo (branches, loops, paralelo), HITL, memória multi-turn.
- Quando NÃO usar: agentes simples com tools (LangChain `create_agent` basta).
- Pré-requisitos: LangChain + um provider de modelo; entendimento de state machines.

## 📚 References

- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)
- [LangGraph Docs](https://docs.langchain.com/oss/python/langgraph/)
- [LangGraph concepts](https://docs.langchain.com/oss/python/langgraph/concepts)
