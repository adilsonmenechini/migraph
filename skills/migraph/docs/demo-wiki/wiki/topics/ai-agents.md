---
title: AI Agents
type: topic
category: AI
domain: agents
created: 2026-08-03
updated: 2026-08-03
tags:
  - ai-agents
  - agentic-systems
  - llm
status: active
id: ai.topic.ai-agents
version: "1.0.0"
confidence: high
source: https://agentwiki.org/agent_loop
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: [agentic systems, autonomous agents]
summary: AI Agents são LLMs dentro de um loop que chamam tools, percebem o ambiente, raciocinam, agem, observam resultados e repetem até completar a tarefa — com governança, estado e escalação.
---

# AI Agents

## 🧠 Definition

**AI Agents** são sistemas que colocam um LLM dentro de um **loop iterativo** (agent loop): o modelo percebe o ambiente, raciocina sobre o contexto, decide uma ação, executa via tool calls, observa o resultado e repete até completar a tarefa ou atingir uma condição de parada.

## 📚 Explanation

### O loop do agente

1. **Context Assembly**: query + retrieved docs + previous results + system constraints.
2. **Model Invocation**: LLM gera next action (tool call request em JSON/XML).
3. **Response Parsing**: extrai tool-use requests estruturados.
4. **Permission Evaluation**: valida contra access control, rate limits, safety.
5. **Tool Execution**: roda operação aprovada, captura resultado.
6. **Loop Control**: continua (volta ao 1 com contexto atualizado) ou termina.

### Autonomia e governança

| Level | Meaning |
|---|---|
| Suggest-only | Sistema propõe; humano executa |
| Human-in-the-loop | Agente propõe; humano aprova cada action |
| Human-on-the-loop | Agente age; humano monitora e pode parar |
| Full autonomy | Sem humano no processo |

### Tipos de controle

- **Model-driven** (LLM escolhe próxima tool): flexível, imprevisível.
- **Deterministic workflows**: reprodutível, testável, barato.
- **Named patterns**: prompt chaining, routing, orchestrator-worker, evaluator-optimizer.

## 🔗 Related

- [[Loop Engineering]]
- [[System Driver]]
- [[GraphRAG]]

## 🧩 Key Insights

- Agentes são ~4x mais caros que chat; multi-agent ~15x (Anthropic).
- Multi-agent não é mais inteligente — é melhor isolamento de contexto + paralelismo.
- Escalation não é falha — é default responsável.
- Grounding via RAG com citações mantém respostas auditable.

## ⚠️ Trade-offs

- Token cost por iteração.
- Impredictibilidade de model-driven loops.
- Comprehension/intent debt quando humanos não revisam.

## 📊 Observability

- **SLIs**: iterations/task, token cost/turn, success rate
- **SLOs**: completion > 95%, cost/turn < threshold
- **Metrics**: traces, token cost, iteration histogram

## 🔐 Security Considerations

- Permission gates: rate limits, audit logs, graduated trust.
- Reads autônomos; writes revisados; email/money/delete aprovados por humano.
- Escalation: confidence thresholds, ask_human tool, review queues.

## 🏗️ Usage Context

- Quando usar: tarefas multi-step, tool interactions, adaptação a resultados.
- Quando NÃO usar: single-pass responses, tarefas simples.
- Pré-requisitos: LLM + tools + state + governança.

## 📚 References

- [Agent Loop Wiki](https://agentwiki.org/agent_loop)
- [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)
- [An Agent Is a Loop (dev.to)](https://dev.to/xinyangwuethz/an-agent-is-a-loop-a-working-mental-model-for-agentic-systems-3ckl)
