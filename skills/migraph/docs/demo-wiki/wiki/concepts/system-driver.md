---
title: System Driver
type: concept
category: AI
domain: systems
created: 2026-08-03
updated: 2026-08-03
tags:
  - system-driver
  - agentic-systems
  - control-loop
  - orchestration
  - agentic-architecture
status: active
id: systems.concept.system-driver
version: "1.0.0"
confidence: high
source: https://dev.to/xinyangwuethz/an-agent-is-a-loop-a-working-mental-model-for-agentic-systems-3ckl
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: [agent driver, control loop, orchestrator, system driver pattern]
summary: System Driver é o padrão de arquitetura que implementa o loop de controle mestre em sistemas agenticos — o componente que orquestra o ciclo Perceive → Reason → Plan → Act → Observe, gerencia estado, impõe governança, impõe limites de autonomia e garante que o loop termine.
---

# System Driver

## 🧠 Definition

**System Driver** é o componente de arquitetura que **implementa e governa o loop de controle principal (agent loop)** em sistemas agenticos. É o "motor" que executa o ciclo iterativo **Perceive → Reason → Plan → Act → Observe**, gerencia estado (curto e longo prazo), impõe fronteiras de governança/autonomia, e garante condições de término. Em frameworks como LangGraph, AutoGen, CrewAI, o System Driver é o **grafo compilado** ou o **runtime executor** que conduz o agente.

> "Strip away the vendor decks and an agent is exactly this: a language model placed inside a loop that can call tools, remember things, and hand control back to a human when it gets stuck." — dev.to/xinyangwuethz

## 📚 Explanation

### O loop canônico (ReAct)

```text
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM DRIVER                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │ Perceive │───▶│  Reason  │───▶│  Plan    │               │
│  └──────────┘    └──────────┘    └────┬─────┘               │
│                                        │                      │
│  ┌──────────┐    ┌──────────┐    ┌────▶│                     │
│  │ Observe  │◀───│   Act    │◀────┘     │                     │
│  └────┬─────┘    └──────────┘           │                     │
│       │                                  │                      │
│       ▼                                  │                     │
│  [Loop Control: continue? terminate?]  │                      │
│       │                                  │                      │
└───────┴──────────────────────────────────┘                      │
         │                           │
         ▼                           ▼
   ┌─────────────┐            ┌─────────────┐
   │  State      │            │  Governance │
   │  (short/    │            │  (autonomy  │
   │   long-term)│            │   levels,   │
   │   memory)   │            │   escalation)│
   └─────────────┘            └─────────────┘
```

### As 5 etapas do ciclo (Oracle / Microsoft)

| Etapa | Descrição |
|---|---|
| **1. Perceive** | Recebe input: user message, API response, error, tool result. |
| **2. Reason** | LLM processa contexto completo, decide next action. |
| **3. Plan** | Decompor objetivo em subtasks (opcional — complex tasks). |
| **4. Act** | Executa: tool call, API request, DB query, code execution. |
| **5. Observe** | Examina resultado: funcionou? task complete? replan needed? |

> **ReAct framework** (Yao et al., 2022): interleaving reasoning + acting → 34% improvement on ALFWorld, 10% on WebShop vs single-pass.

### Arquitetura do System Driver

```python
# Conceitual — LangGraph / AutoGen / CrewAI pattern
class SystemDriver:
    def __init__(self, llm, tools, state, governance):
        self.llm = llm
        self.tools = tools
        self.state = state          # short + long-term memory
        self.governance = governance # autonomy levels, escalation
        self.max_iterations = 10
        self.token_budget = 50000

    def run(self, goal: str):
        while not self._should_terminate():
            context = self._assemble_context()
            action = self.llm.invoke(context)  # Reason + Plan
            result = self._execute(action)     # Act (tool calls)
            self.state.update(result)          # Observe → Update
            if self._goal_achieved(goal): break
        return self.state.final_output
```

### Camadas de governança (autonomy levels)

| Level | Meaning | When |
|---|---|---|
| **Suggest-only** | Sistema propõe; humano executa | High risk, learning phase |
| **Human-in-the-loop** | Agente propõe; humano aprova cada action | Default para writes, emails, deletes |
| **Human-on-the-loop** | Agente age autônomo; humano monitora + pode parar | Default para reads, queries locais |
| **Full autonomy** | Sem humano no processo | Apenas reads/queries baixos risco |

> **Rule of thumb**: gating de ação escala com `irreversibilidade × blast radius`.
> - Reads/queries → full autonomy
> - Local file write → review after
> - Email, money, delete, publish outward → human approve every time

### Escalation (safety valve)

O System Driver deve interromper e escalar quando:
- Confidence < threshold
- Tool call blocked (permissions)
- Missing info / missing permissions
- High-risk irreversible action
- No-progress detection (repeated iterations = no new info)
- Token/cost budget exceeded

Escalation **não é falha** — é default responsável. Mecanismos: confidence thresholds, `ask_human` tool, review queues, orchestrator escalation em multi-agent.

### State Management

| Type | Description | TTL |
|---|---|---|
| **Short-term** | Context window (conversation + tool results) | Session (compaction/sliding window/offloading) |
| **Long-term** | Episodic (log of what happened) + Semantic (distilled knowledge) | Persistent (files, vector store, DB) |
| **Checkpointing** | Snapshots para restart após crash | Per iteration / milestone |

### Capabilities (tools)

O System Driver expõe tools ao LLM. Cada tool: `name`, `description`, `JSON schema (parameters)`. Harness valida e executa — **model requests, code decides** (security boundary). Step 3 é a fronteira de segurança.

### Grounding

RAG para binding answers: embed query → retrieve (hybrid BM25 + vectors + reranker) → cite sources. Citações mantêm resposta auditable.

## 🔗 Related

- [[Loop Engineering]]
- [[GraphRAG]]
- [[ArgoCD]]
- [[Agent Loop]]

## 🧩 Key Insights

- **System Driver = o loop compilado**. Frameworks (LangGraph, AutoGen, CrewAI) compilam declarative config → executable graph/runtime.
- **Governança não é afterthought** — é layer acima do loop que constrange autonomia.
- **Escalation não é falha** — é default responsável. Melhor perguntar demais que agir irreversivelmente.
- **State = spine do loop**. Sem state persistente, loop não aprende, não retoma após crash, não evita repetição.
- **Cost control no driver**: max_iterations, token budget, no-progress detection, goal-achievement checks. Magentic-One usa dual-loop (outer resets strategy when inner stalls).

## ⚠️ Trade-offs

- **Model-driven control flow** (LLM picks next tool): flexível, lida com imprevisto, mas imprevisível, hard to reproduce, pode wander/loop forever.
- **Deterministic workflows** (hard-coded control flow): reprodutível, testável, barato, mas rígido.
- **Hybrid**: plan-and-execute (planner → executor → re-planner), routing, orchestrator-worker, evaluator-optimizer.

### Multi-agent

- Não são "mais inteligentes" — melhor isolamento de contexto e paralelismo.
- Se single agent com boas tools resolve, use single agent.
- Sub-agent = context isolation + parallelism + specialization.
- Factory pattern: declarative config (role prompt, tool set, model, permissions) → spawn instances.

## 📊 Observability

- **SLIs**: iterations/task, token cost/turn, success rate, escalation rate
- **SLOs**: task completion > 95%, escalation < 5%, token budget adherence
- **Metrics**: traces (LangSmith, AutoGen Telemetry), token cost/turn, iteration histogram, escalation reasons

## 🔐 Security Considerations

- **Harness = security boundary**. Model requests, code executes. Todas permissões, rate limits, audit logs vivem no harness.
- Permission gates: user auth rules, rate limiting, audit logging, graduated trust.
- Escalation mechanisms: confidence thresholds, explicit `ask_human` tool, review queues.

## 🏗️ Usage Context

- Quando usar: qualquer sistema agentico que precise de autonomia controlada, state persistente, governança.
- Quando NÃO usar: workflows determinísticos simples, single-pass LLM calls.
- Pré-requisitos: LLM + tools + state store + governance config.

## 📚 References

- [An Agent Is a Loop (dev.to)](https://dev.to/xinyangwuethz/an-agent-is-a-loop-a-working-mental-model-for-agentic-systems-3ckl)
- [What Is the AI Agent Loop? (Oracle)](https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems)
- [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [AutoGen](https://github.com/microsoft/autogen)
- [CrewAI](https://github.com/crewAIInc/crewAI)