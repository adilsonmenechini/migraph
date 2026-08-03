---
title: CrewAI
type: reference
category: AI
domain: ai-agents
created: 2026-08-03
updated: 2026-08-03
tags:
  - ai
  - agents
  - multi-agent
  - orchestration
  - crewai
status: active
id: ai-agents.reference.crewai
version: "1.0.0"
confidence: high
source: https://docs.crewai.com/
summary: CrewAI é o framework Python para equipes de agentes de IA — Agents, Crews e Flows com processos Sequencial, Hierárquico e Híbrido, outputs Pydantic e memória integrada para orquestração multi-agente de ponta a ponta.
---

# CrewAI

## 🧠 Definition

CrewAI é um framework Python para orquestrar equipes colaborativas de agentes de IA ("crews") — cada agente tem um papel, objetivos e ferramentas próprios, e os crews executam processos Sequencial, Hierárquico ou Híbrido para completar tarefas complexas de ponta a ponta.

## 📚 Explanation

O CrewAI organiza o desenvolvimento multi-agente em três níveis:

- **Agents**: unidades autônomas com papel (`role`), objetivo (`goal`) e história (`backstory`) — equipados com ferramentas e memória próprias. Suportam guardrails (validação de saída), memória de curto e longo prazo, e knowledge bases (RAG) acopladas.
- **Crews**: a equipe que coordena os agentes com um processo definido. O processo **Sequential** executa tarefas em ordem; o **Hierarchical** usa um agente manager que delega e valida; o **Hybrid** combina os dois, permitindo agentes delegarem entre si sob supervisão.
- **Flows**: orquestração de eventos/estados para pipelines longos — com steps `start`, `listen` e `router`, permitindo persistência e retomada de workflows long-running.

As saídas podem ser estruturadas via Pydantic (JSON Schema), garantindo contratos entre agentes. A observabilidade é fornecida pelo console do CrewAI Enterprise, com rastreamento de execuções de agentes e tarefas.

A instalação é simples: `uv add crewai` — e a configuração dos agentes é declarativa em Python, o que o torna amigável a GitOps e versionamento.

## 🧩 Key Insights

- **Três níveis de abstração**: Agents, Crews e Flows cobrem desde uma única tarefa até pipelines complexos com retomada.
- **Processos configuráveis**: Sequential, Hierarchical e Hybrid atendem a graus diferentes de autonomia e supervisão.
- **Estrutura Pydantic**: outputs tipados garantem integração confiável entre agentes e sistemas externos.
- **Memória e conhecimento**: memória de curto/longo prazo + knowledge bases (RAG) por agente ou crew.

## ⚠️ Trade-offs

| Aspecto | Prós | Contras |
|---------|------|---------|
| Abstração | Multi-agente em poucas linhas | Menos controle fino sobre o loop interno |
| Processos | 3 modos prontos | Hierárquico depende do manager model |
| Estrutura | Pydantic/Zod nativos | Contratos rígidos exigem design cuidadoso |
| Observabilidade | Console Enterprise | Recursos avançados são pagos |

## 📊 Observability

- Console CrewAI Enterprise: trace de agentes, tarefas e custos.
- Logs por agente/tarefa no modo CLI.
- Métricas de execução exportáveis para pipelines de avaliação.

## 🔐 Security Considerations

- Credenciais de modelos (API keys) via variáveis de ambiente — nunca hardcoded.
- Guardrails para validar e filtrar saídas sensíveis dos agentes.
- Sandbox/controle de ferramentas que acessam sistemas externos.

## 🏗️ Usage Context

- **Automação de pesquisa**: equipes de researcher + writer + reviewer trabalhando em conjunto.
- **Pipelines de análise**: extrair, estruturar e sintetizar dados de múltiplas fontes.
- **Workflows long-running**: Flows com retomada para processos de horas/dias.
- **Substituição de cadeias encadeadas de prompts**: orquestração declarativa no lugar de pipelines manuais.

## 📚 References

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI Processes](https://docs.crewai.com/edge/en/concepts/processes)

## Connections

- [Langchain](../references/langchain.md)
- [Langgraph](../references/langgraph.md)
- [Ai-Agents](../topics/ai-agents.md)
