---
title: GraphRAG
type: reference
category: AI
domain: rag
created: 2026-08-03
updated: 2026-08-03
tags:
  - graphrag
  - rag
  - knowledge-graph
  - microsoft
  - leiden
status: active
id: ai.reference.graphrag
version: "1.0.0"
confidence: high
source: https://microsoft.github.io/graphrag/
summary: GraphRAG é uma abordagem hierárquica e baseada em grafos para RAG (Retrieval-Augmented Generation) que extrai um knowledge graph do texto bruto, constrói hierarquia de comunidades via Leiden, gera sumários em bottom-up e usa essas estruturas para queries globais (map-reduce sobre community reports) e locais (fan-out no grafo).
---

# GraphRAG

## 🧠 Definition

GraphRAG é uma abordagem **estruturada e hierárquica para RAG (Retrieval-Augmented Generation)** que difere fundamentalmente de métodos baseados em busca semântica pura (vector search). Em vez de snippets de texto isolados, o GraphRAG:

1. Extrai um **knowledge graph** do texto bruto (entidades, relacionamentos, claims)
2. Constrói hierarquia de **comunidades** via algoritmo **Leiden** recursivo
3. Gera **sumários de comunidade (community reports)** em bottom-up
4. Usa essas estruturas para queries: **Global Search** (map-reduce sobre community reports), **Local Search** (fan-out no grafo), **DRIFT Search** (híbrido), **Basic Search** (vector search clássico)

## 📚 Explanation

### Pipeline de Indexação

```
Documents → Chunk (1200 tokens default) → TextUnits
    → Entity/Relationship/Claim Extraction (LLM)
    → Graph Construction
    → Hierarchical Leiden Clustering (recursive, max_cluster_size=10)
    → Community Summarization (bottom-up, LLM-generated)
    → Text Embeddings (entities, text units, community reports) → Vector Store
```

### Data Model (Parquet tables default)

| Entity Type | Description |
|---|---|
| `Document` | Input files (CSV rows ou .txt files) |
| `TextUnit` | Chunks analisáveis (default 1200 tokens, configurável) |
| `Entity` | Pessoas, lugares, organizações, eventos — com tipo e descrição |
| `Relationship` | Conexões entre entidades com contexto descritivo |
| `Covariate` | Claims time-bound sobre entidades (opcional) |
| `Community` | Clusters hierárquicos do Leiden (level 0 = leaf, level N = root) |
| `Community Report` | Sumário LLM-gerado de cada comunidade (executive overview + key entities/relationships/claims) |

### Hierarchical Leiden Clustering

- **Algoritmo**: Leiden (melhor que Louvain — connected communities, eficiente em grafos grandes, suporte nativo a multi-level hierarchy, reproducible seed 0xDEADBEEF).
- **Parâmetros chave**:
  - `max_cluster_size` (default 10): entidades máximas por leaf community. Menor = mais níveis, mais relatórios, mais custo LLM. Maior = menos níveis, sumários mais amplos.
  - `use_lcc` (default true): restringe ao maior connected component.
  - `resolution` (1.0): preferência tamanho comunidade.
  - `randomness` (0.001), `use_modularity` (true), `iterations` (1).

- **Hierarchy**: recursivo até todos os leaf communities < `max_cluster_size`. Cria parent communities agregando children.
- **Output**: tree structure de comunidades com `Community Report` por nível.

### Query Strategies

| Strategy | Best For | Mechanism |
|---|---|---|
| **Global Search** | Questões globais/holísticas ("Quais os temas principais?") | Map-reduce sobre community reports em nível escolhido (root/mid/leaf). Map: intermediate answers per chunk. Reduce: aggregate. |
| **Local Search** | Perguntas sobre entidades específicas ("O que cura a camomila?") | Fan-out: entity → neighbors + relationships + text units. Combina graph + raw text. |
| **DRIFT Search** | Exploração balanceada | Primer com community reports (global) + refinamento local via fan-out. Gera follow-up questions. |
| **Basic Search** | Similaridade semântica simples | Standard top-k vector search. |

### Dynamic Community Selection (otimização recente)

Em vez de map-reduce estático em nível fixo: **rater LLM** (GPT-4o-mini) classifica relevância de community reports **top-down**. Irrelevantes = poda sub-árvore. Relevantes = traverse down. Só reports relevantes → map-reduce.
- **Benefícios**: ~77% redução custo token (level 1), ~58-60% win rate vs static. Level 3 → mais detalhes, +34% custo.

### Cost Comparison

| Approach | Token Use per Query | Comprehensiveness |
|---|---|---|
| Baseline RAG | 100% (baseline) | Baseline |
| GraphRAG (intermediate/low) | 20–70% | 70-80% win rate |
| GraphRAG (high-level) | 2-3% | Competitive |
| GraphRAG (source text summarization) | 100%+ | Lower |

## 🔗 Related

- [[RAG]]
- [[Knowledge Graph]]
- [[Leiden Algorithm]]
- [[Loop Engineering]]
- [[System Driver]]

## 🧩 Key Insights

- **Estrutura explícita**: entities/relationships como first-class objects → traversal multi-hop, entity importance via graph metrics, relationship-aware retrieval.
- **Community detection + bottom-up summarization** → multi-level understanding, pre-computed summaries reduzem custo query-time, reasoning sobre estrutura do dataset.
- **Provenance**: cada fato mantém links para source text units, documentos originais, entities/relationships relacionados, community memberships.
- **Global queries** (ex: "Quais os temas principais?") são o killer feature — baseline RAG falha porque top-k snippets não cobrem o todo.

## ⚠️ Trade-offs

- **Upfront cost**: indexação pesada (LLM extraction + Leiden + community summarization). Custos podem ser altos para datasets grandes.
- **Complexidade**: pipeline multi-phase, múltiplas chamadas LLM, Leiden config, vector store.
- **Quando NÃO usar**: datasets pequenos, queries simples, custo de indexação não justificado.

## 📊 Observability

- **SLIs**: answer quality (comprehensiveness, diversity, empowerment), token cost/query, latency
- **SLOs**: win rate > 70% vs baseline RAG
- **Metrics**: token cost/query, latency, win rate (LLM evaluator), community detection quality

## 🔐 Security Considerations

- Dados privados nunca saem do ambiente (local LLM ou endpoint controlado).
- Covariates opcionais para claims time-bound (compliance).
- Provenance links permitem auditoria completa.

## 🏗️ Usage Context

- Quando usar: datasets complexos, queries globais, necessidade de provenance, sumarização cross-document.
- Quando NÃO usar: datasets pequenos/simples, queries apenas locais/semelhantes, budget apertado.
- Pré-requisitos: LLM para extraction + summarization, vector store (LanceDB default, Qdrant, etc.), Leiden (graspologic_native).

## 📚 References

- [GraphRAG Official](https://microsoft.github.io/graphrag/)
- [microsoft/GraphRAG (GitHub)](https://github.com/microsoft/GraphRAG)
- [GraphRAG: Unlocking LLM Discovery on Narrative Private Data](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)
- [GraphRAG: Improving Global Search via Dynamic Community Selection](https://www.microsoft.com/en-us/research/blog/graphrag-improving-global-search-via-dynamic-community-selection/)
- [Core Concepts Overview](https://microsoft-graphrag.mintlify.app/concepts/overview)
- [Community Detection (Leiden)](https://microsoft-graphrag.mintlify.app/concepts/community-detection)
- [Global Search](https://github.com/microsoft/graphrag/blob/main/docs/query/global_search.md)
- [GraphRAG Project (Microsoft Research)](https://www.microsoft.com/en-us/research/project/graphrag/)