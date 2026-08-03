# Design: Unificar skills knowledge-create e knowledge-manager em uma única skill `knowledge`

**Data**: 2026-08-03
**Status**: Proposto (aguardando revisão do usuário)
**Abordagem escolhida**: A — Monolítico com modos (um SKILL.md único com Create Mode + Refactor Mode)

## Contexto

O repositório possui duas skills irmãs instaladas em `skills/` (e também em `~/.claude/skills/`):

| Skill | Linhas | Tipos | Extra |
|---|---|---|---|
| `knowledge-create` | 200 | concept, pattern, runbook, architecture | 4 templates, validators/schema.json, hooks/post_create.md |
| `knowledge-manager` | 719 | concept, guide, reference, example | scripts/deduplicate.py + update_schema.py, resources/ |

Ambas fazem criação de notas de conhecimento com sobreposição clara (Create Mode no manager), mas com **esquemas de tipos conflitantes** e **frontmatter diferentes**. O usuário pediu para unir em uma única skill.

## Decisões (aprovadas pelo usuário)

1. **Nome**: `knowledge`
2. **Tipos**: União — 7 tipos: `concept, guide, reference, example, pattern, runbook, architecture`
3. **Frontmatter**: Schema unificado (base Obsidian do manager + `domain`/`id` do create)
4. **Destino**: Só no repo (`skills/knowledge/`) — `~/.claude/skills/` não será tocado até o usuário testar

## Estrutura de arquivos final

```
skills/knowledge/
├── SKILL.md                 # frontmatter + Create Mode (7 tipos) + Refactor Mode + Rules
├── templates/               # 7 templates: concept, guide, reference, example, pattern, runbook, architecture
├── validators/
│   └── schema.json          # schema unificado p/ 7 tipos (base: do create, estendido)
├── hooks/
│   └── post_create.md       # do create
├── resources/
│   ├── quality_rules.md     # do manager
│   └── template.md          # do manager
├── scripts/
│   ├── deduplicate.py       # do manager
│   └── update_schema.py     # do manager
└── evals/
    └── evals.json           # unificado
```

**Remover** do repo: `skills/knowledge-create/` e `skills/knowledge-manager/`.

## Frontmatter do SKILL.md unificado

```yaml
---
name: knowledge
description: Complete knowledge base management - create, organize, and maintain
  Obsidian-style knowledge notes with RAG compatibility. Covers the full lifecycle:
  create notes across 7 types (concept, guide, reference, example, pattern, runbook,
  architecture) with unified frontmatter and folder organization, validate schema,
  detect and merge duplicates, optimize cross-linking, and maintain INDEX files.
triggers: [add note, document this, create knowledge, research, learn about, build knowledge,
  capture, add IaC, add DevOps, add AI, create pattern, build runbook, capture architecture,
  find duplicates, merge notes, clean up, check duplicates, organization, maintain knowledge,
  optimize knowledge, deduplicate, fix overlapping notes]
tools: [filesystem, read, write, glob, mkdir, grep]
category: knowledge-management
version: 2.0.0
tags: [knowledge, obsidian, rag, automation, documentation]
---
```

## Conteúdo do SKILL.md (seções)

| Seção | Origem | Mudança |
|---|---|---|
| When to use + Mode Selection | manager | Union dos triggers; 7 tipos |
| **Create Mode** | | |
| Step 1: Identificar topic/category/tipo | manager | Tabela de inferência com os **7 tipos** |
| Step 2: Folder structure | manager | Subpastas por tipo: `concepts/ guides/ references/ examples/ patterns/ runbooks/ architectures/` + `patterns/` cross-category + INDEX.md |
| Step 3: Example from docs | manager | Mantém (temas IaC/DevOps/AI) |
| Step 4: File path | manager | Slug rules |
| Step 5: Create content | **merged** | Schema unificado + seleção de template pelos 7 tipos |
| Step 6: Obsidian features | manager | Mantém (wikilinks, callouts, block IDs, embeds) |
| Step 7: INDEX.md | manager + create | Mantém + regras do create |
| Step 8: Validate | **merged** | Checklist unificado + validators/schema.json |
| **Refactor Mode** | manager | Mantém (deduplicate.py, merge, deprecate) |
| Rules | **merged** | Union das 10 do manager + atomicidade/naming/validação do create |
| Resources | **merged** | Lista todos os assets |

## Schema unificado de frontmatter (para os 7 tipos)

```yaml
---
# Core (obrigatório p/ todos os tipos)
title: <Title>              # legível
type: <concept|guide|reference|example|pattern|runbook|architecture>
category: <category>        # IaC | DevOps | AI | outro
domain: <domain>            # ex: sre, kubernetes, terraform (reutilizado do create)
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:                       # lista, 2 espaços, mínimo 1
  - <tag1>
status: active              # draft | active | deprecated | archived
# Schema (obrigatório p/ pattern/runbook/architecture; opcional p/ os demais)
id: <domain>.<type>.<slug>
version: "1.0.0"
confidence: high            # high | medium | low
source: docs                # docs | internal | external
inputs: []
outputs: []
dependencies:
  - [[<related-note>]]
quality_score: 0            # 0-100
# Opcionais
aliases:
  - <alternative-name>
---
```

Regras YAML herdadas do manager: `---` na linha 1, indentação de 2 espaços, tags em lista (`- `), datas ISO 8601, wikilinks em frontmatter entre aspas, bool minúsculo sem aspas.

## Templates (7) — mapeamento

| Template | Origem |
|---|---|
| `concept.md` | do create (mantido) |
| `pattern.md` | do create (mantido) |
| `runbook.md` | do create (mantido) |
| `architecture.md` | do create (mantido) |
| `guide.md` | **novo** — derivado do corpo do manager (Overview/Purpose/Content/Usage) |
| `reference.md` | **novo** — derivado do corpo do manager (quick reference) |
| `example.md` | **novo** — derivado do Step 3 do manager (formato de example) |

Todos os 7 templates alinhados ao schema unificado (mesmo frontmatter, seções do corpo variando por tipo).

## Conflitos resolvidos

1. **Tipos**: 7 unificados — tabela de inferência ampliada com os 7.
2. **Folder mapping**: `patterns/` unificado como cross-category + por tópico quando category definida.
3. **`resources/index_rules.md`** (referenciado pelo manager mas inexistente): **removida a referência** — regras de INDEX já no SKILL.md (Step 7); evitar duplicação.
4. **Menções a skills inexistentes** (`knowledge-validator`, `knowledge-refactor` no create): removidas — validação interna (schema.json + checklist).
5. **Evals**: merge dos dois `evals.json` — `skill_name: knowledge`, description unificada, evals de create + refactor.

## Fora de escopo (nesta fase)

- `~/.claude/skills/` não será tocado (decisão do usuário: testar no repo primeiro).
- `examples/knowledge/` (o exemplo no repo) não muda.
- Nenhuma mudança nos scripts do MiGraph.

## Critérios de aceite

- [ ] `skills/knowledge/` existe com todos os assets (templates x7, schema.json, hooks, resources, scripts, evals)
- [ ] `skills/knowledge-create/` e `skills/knowledge-manager/` removidos do repo
- [ ] SKILL.md descreve os 7 tipos com tabela de inferência, schema unificado, Create Mode e Refactor Mode
- [ ] `resources/index_rules.md` não é mais referenciado
- [ ] Menções a `knowledge-validator`/`knowledge-refactor` removidas
- [ ] evals.json válido (JSON parseável, skill_name: knowledge)
- [ ] Todos os 7 templates usam o mesmo frontmatter do schema unificado
- [ ] `~/.claude/skills/` intocado
