---
title: Loop Engineering
type: concept
category: AI
domain: agents
created: 2026-08-03
updated: 2026-08-03
tags:
  - loop-engineering
  - agentic-systems
  - ai-agents
  - feedback-loops
  - ReAct
status: active
id: agents.concept.loop-engineering
version: "1.0.0"
confidence: high
source: https://addyosmani.com/blog/loop-engineering/
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: [loopcraft, agentic loops]
summary: Loop Engineering é a disciplina de projetar sistemas autônomos baseados em loops de feedback fechados — observe, decida, atue, avalie, atualize estado, repita — que substituem o prompting manual por sistemas autônomos que se autopromptam e se autoavaliam.
---

# Loop Engineering

## 🧠 Definition

Loop Engineering é a disciplina de engenharia de **sistemas autônomos baseados em loops de feedback fechados** (Observe → Decide → Act → Evaluate → Update State → repeat) que substituem o prompting manual por sistemas que se autopromptam e se autoavaliam até atingir um objetivo recursivo verificável.

> "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." — Peter Steinberger

## 📚 Explanation

### A evolução da otimização

| Era | Foco | Unidade otimizada | Teto cognitivo |
|---|---|---|---|
| 2020–2023 | Prompt Engineering | Single turn, in-context cues | No closure, state loss |
| 2023–2024 | Context Engineering | Static RAG memory | Unchanged params, no iteration |
| 2024–2025 | Agent Engineering | Autonomous delegation & tools | No systemic eval, feedback-blind |
| **2025+** | **Loop Engineering** | **Closed dynamical feedback loops** | **Unbounded, self-directed systems** |

> **Hierarchy of Optimization:** Prompt engineering optimizes a *single interaction*. Agent engineering optimizes an *autonomous actor*. **Loop engineering optimizes the entire closed system** — cheaper to run, faster to ship, impossible to hand-wave, and built to get better every iteration.

### O loop canônico

```text
       Observe
          │
          ▼
        Decide
          │
          ▼
         Act
          │
          ▼
       Evaluate
          │
    Update State
          │
          └───────────(repeat)───────────► [Observe]
```

Matematicamente: $\mathcal{L} = (S, A, O, T, E, M, \tau)$
- $S$: State space
- $A$: Action space
- $O$: Observation space (feedback signals)
- $T$: Transition functions ($S \times A \to S$)
- $E$: Evaluator models (scores & rewards)
- $M$: Memory representation (episodic & parameter state)
* $\tau$: Termination conditions & criteria

### 4 níveis de loops (LangChain / LangGraph)

| Loop | O que faz | Impacto | Primitiva LangChain |
|---|---|---|---|
| 1. Agent loop | Modelo chama tools até task done | Automate work | `create_agent` |
| 2. Verification loop | Grader avalia output, feedback se falha | Ensure quality | `RubricMiddleware` |
| 3. Event-driven loop | Eventos disparam agente (webhook, cron, webhook) | Automate at scale | LangSmith Deployment |
| 4. Hill climbing loop | Traces de produção alimentam analysis agent que melhora harness | Harness improvements | LangSmith Engine |

### LSS (Loop Specification Schema)

Declarative, machine-readable format para definir arquitetura, inputs, constraints de qualquer loop. Permite validação, scoring (LES - Loop Effectiveness Score), diagramação Mermaid, replay sandbox.

## 🔗 Related

- [[AI Agents]]
- [[ReAct Framework]]
- [[GraphRAG]]
- [[System Driver]]

## 🧩 Key Insights

- **Prompt engineering optimiza um turno. Agent engineering optimiza um ator. Loop engineering optimiza o sistema fechado inteiro** — mais barato, mais rápido, impossível de hand-waving, construído para melhorar a cada iteração.
- O loop separa **maker** (escreve) de **checker** (verifica). O modelo que escreveu o código é muito "nice" avaliando seu próprio dever de casa.
- **Loops 3 e 4** são onde o valor composta: event-driven (embed no ecossistema) e hill climbing (auto-melhoria contínua).
- **Spine**: estado persistente (markdown, Linear, markdown file) que rastreia progresso, evita repetição de erros, mantém contexto.
- **Governance**: autonomia escalada por irreversibilidade × blast radius. Reads=auto, writes=review, delete/email/money=human approve.

## ⚠️ Trade-offs

- **Tokens**: agentes consomem ~4x tokens de chat; multi-agent ~15x. Guardrails: max_iterations, token budget, no-progress detection, goal-achievement checks.
- **Cognitive surrender**: confiar cegamente no loop → comprehension debt + intent debt.
- **Custo vs autonomia**: full autonomy = irreversível; human-on-the-loop = monitor + stop; human-in-the-loop = approve each action.

## 📊 Observability

- **SLIs**: loop iterations, token cost/turn, LES score, task success rate
- **SLOs**: task completion > 95%, cost/turn < threshold
- **Metrics**: traces (LangSmith), LES score, token cost/turn, iteration count

## 🔐 Security Considerations

- Governance layer: autonomy levels (suggest-only → human-in-the-loop → human-on-the-loop → full autonomy).
- Permission gates: rate limits, audit logs, graduated trust.
- Escalation: confidence thresholds, ask-human tool, review queues.
- Escalation não é falha — é default responsável.

## 🏗️ Usage Context

- Quando usar: agentes de longa duração, code generation autônomo, software maintenance, multi-step task execution.
- Quando NÃO usar: interações one-off, tarefas simples, sem necessidade de iteração.
- Pré-requisitos: agente com tools, grader/verifier, state persistence, termination criteria.

## 📚 References

- [Loop Engineering (Addy Osmani)](https://addyosmani.com/blog/loop-engineering/)
- [The Art of Loop Engineering (LangChain)](https://www.langchain.com/blog/the-art-of-loop-engineering)
- [What Is Loop Engineering? (IBM)](https://www.ibm.com/think/topics/loop-engineering)
- [KanakMalpani/Loop-Engineering (GitHub)](https://github.com/KanakMalpani/Loop-Engineering)
- [Agent Loop Wiki](https://agentwiki.org/agent_loop)
- [Loop Core Engineering](https://github.com/KanakMalpani/Loop-Core-Engineering)