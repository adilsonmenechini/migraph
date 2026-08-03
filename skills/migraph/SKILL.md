---
name: migraph
description: Create, maintain, query, and visualize a local Markdown knowledge base. Initialize a wiki, import files or webpages, collect inbox items, dedupe similar pages, answer from existing knowledge, and generate HTML viewer and graph artifacts. Use when the user mentions knowledge base, wiki, note capture, deduplication, knowledge graph, add note, document this, create knowledge, research, build knowledge, create pattern, build runbook, capture architecture, find duplicates, merge notes, or clean up notes.
license: "MIT"
compatibility: "Requires Python 3 with venv support. MiGraph bootstraps its own .venv, installs runtime dependencies from requirements.txt, and supports macOS, Linux, and Windows."
metadata:
  version: "1.0.0"
  author: adilsonmenechini
---

# MiGraph

MiGraph is a single public skill for working with a local Markdown knowledge base. It covers the full knowledge lifecycle: creating notes across 13 page types, organizing by category, importing external content, validating schema, deduplicating, cross-linking, querying, and visualizing.

## Role

- Act as the end-user-facing knowledge base assistant.
- Translate user intent into stable MiGraph actions.
- Prefer natural conversation over exposing raw subcommands.
- Treat existing wiki pages as the primary evidence base for answers.
- Escalate to page creation only when the output is valuable enough to preserve.

## Operating Principles

- Keep MiGraph as the only visible skill entry point.
- Resolve the wiki root before running any read, write, or generation task.
- Prefer evidence-first answers from existing pages.
- Prefer HTML deliverables such as inbox, viewer, graph, and governance pages when the user asks to inspect or browse the workspace.
- Surface ambiguity explicitly when confidence is low, sources conflict, or entity identity is unclear.

## When To Use This Skill

- The user wants to create or maintain a local knowledge base.
- The user wants to import Markdown, PDF, DOCX, XLSX, XLS, PPTX, webpages, or plain text.
- The user wants to collect content into an inbox before formal ingest.
- The user wants to ask questions against an existing wiki.
- The user wants to save results as `query`, `synthesis`, `decision`, or `concept` pages.
- The user wants to add a new knowledge note (concept, guide, reference, example, pattern, runbook, architecture).
- The user wants to find, merge, or clean up duplicate notes.
- The user wants to generate a viewer, a graph, or a governance report.
- The user wants to review entity alias collisions or perform deterministic entity merges.

## When Not To Use This Skill

- The task is unrelated to a local Markdown knowledge base.
- The user only wants general chat without knowledge capture, lookup, or maintenance.
- The task belongs to a different productivity domain such as spreadsheets, slides, or unrelated code work.

## Required Environment Variables

Remote AI features are **disabled by default**. Configure only what you need.

### Content generation (`crystallize`, `digest`)

Requires all three variables. Any OpenAI-compatible chat completion endpoint works.

| Variable | Required | Used By | Notes |
|----------|----------|---------|-------|
| `MIGRAPH_LLM_API_KEY` | Yes, to enable | `llm_client.py` | API key for the configured LLM provider |
| `MIGRAPH_LLM_BASE_URL` | Yes, to enable | `llm_client.py` | Chat completions URL |
| `MIGRAPH_LLM_MODEL` | Yes, to enable | `llm_client.py` | Model name |
| `MIGRAPH_LLM_TEMPERATURE` | No | `llm_client.py` | Optional temperature override |

Without a complete LLM configuration, `crystallize` and `digest` use local heuristics only.

### Entity embedding (`entity-merge-review`, `graph-report`, `health`)

Enabled when `MIGRAPH_EMBED_API_KEY` is set. Defaults to SiliconFlow BGE-M3.

| Variable | Required | Used By | Notes |
|----------|----------|---------|-------|
| `MIGRAPH_EMBED_API_KEY` | Yes, to enable | `embed_client.py` | API key for the embedding provider |
| `MIGRAPH_EMBED_BASE_URL` | No | `embed_client.py` | Default `https://api.siliconflow.cn/v1/embeddings` |
| `MIGRAPH_EMBED_MODEL` | No | `embed_client.py` | Default `BAAI/bge-m3` |

## Root Resolution

- If the user provides a wiki path, use it directly.
- If the working directory already contains `.wiki-schema.md`, treat that directory as the wiki root.
- If the user wants a new workspace, run `init`.
- If no wiki root can be found, ask the user where the wiki should live before making changes.

## Page Types

MiGraph stores pages in `wiki/<type-plural>/`. Each page has unified frontmatter.

| Type | Directory | Purpose |
|------|-----------|---------|
| `source` | `wiki/sources/` | Imported documents (converted, ingested) |
| `topic` | `wiki/topics/` | Subject-area pages |
| `concept` | `wiki/concepts/` | Reusable concepts |
| `decision` | `wiki/decisions/` | Decisions and their rationale |
| `query` | `wiki/queries/` | Saved Q&A results |
| `synthesis` | `wiki/syntheses/` | Combined digests |
| `entity` | `wiki/entities/` | Named entities (people, tools, systems) |
| `pattern` | `wiki/patterns/` | Reusable patterns |
| `runbook` | `wiki/runbooks/` | Operational runbooks |
| `architecture` | `wiki/architectures/` | Architecture documentation |
| `guide` | `wiki/guides/` | How-to guides |
| `reference` | `wiki/references/` | Reference material |
| `example` | `wiki/examples/` | Practical examples |

## Unified Frontmatter Schema (ALL types)

```yaml
---
title: <Title>
type: <type>
category: <category>          # IaC | DevOps | AI | other
domain: <domain>              # e.g., sre, kubernetes, terraform
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:                         # list, 2-space indent, min 1
  - <tag1>
status: active                # draft | active | deprecated | archived
summary: <1-2 sentence summary>
id: <domain>.<type>.<slug>    # for pattern/runbook/architecture
version: "1.0.0"
confidence: high              # high | medium | low (for pattern/runbook/architecture)
source: docs                  # for pattern/runbook/architecture
---
```

Validation rules:
- Boolean values: `true` / `false` (lowercase, no quotes)
- Dates: ISO 8601 format `YYYY-MM-DD`
- Wikilinks in frontmatter must be quoted: `project: "[[Project Name]]"`
- Filename: `slug-case.md`
- ID: `{domain}.{type}.{slug}` (e.g., `sre.runbook.incident-response`)

The validator lives at `validators/schema.json`. Run it via `update-schema` or validate manually against the rules above.

## Execution Entry

When you need to invoke MiGraph, use the unified entry:

```bash
<python-command> skills/migraph/scripts/migraph <command> ...
```

Platform note:

- On macOS and Linux, `<python-command>` is usually `python3`.
- On Windows, `<python-command>` is usually `python`.

## Intent Mapping

- Create a wiki -> `init`
- Warm up the runtime -> `bootstrap`
- Convert a file or webpage to Markdown -> `convert`
- Import a file or webpage into the wiki -> `ingest`
- Collect content into inbox first -> `clip`
- Build or refresh inbox review -> `inbox`
- Ask from existing wiki knowledge -> `ask`
- Save a correction or lesson learned -> `correct`
- Save a valuable answer -> `query`
- Create a concept, decision, or synthesis artifact -> `crystallize` or `digest`
- Build the graph explorer -> `graph`
- Build the graph governance report -> `graph-report`
- Review entity merge candidates -> `entity-merge-review`
- Preview or apply entity merges -> `entity-merge-apply`
- Browse HTML outputs in a browser -> `serve`
- Check workspace health -> `health`
- Check a compact workspace snapshot -> `status`
- Validate environment capabilities -> `doctor`
- Detect duplicate or similar pages in the wiki -> `dedupe-pages`
- Detect duplicate or similar notes by title/content/tag similarity -> `deduplicate`
- Backfill schema fields (id, version, confidence, source) -> `update-schema`

## Gotchas

- `python3` on macOS and Linux, `python` on Windows — never assume `python`.
- AI features are disabled by default. Without a complete LLM config, `crystallize` and `digest` fall back to local heuristics; without an embed config, semantic scores degrade to lexical only.
- `serve` serves `output/` over HTTP; agent chat UIs usually cannot render `file://` HTML inline. Prefer `serve` when the user wants to browse.
- `dedupe-pages` compares pairs across the same type. `deduplicate` uses fuzzy title (40%), content/Jaccard (40%), and tag (20%) similarity with HIGH ≥70% / MEDIUM 40–69% thresholds.
- New page types `pattern`, `runbook`, `architecture` live in `wiki/patterns/`, `wiki/runbooks/`, `wiki/architectures/`.

## Import Workflow

Progress:
- [ ] Step 1: Resolve the wiki root (`init` or locate `.wiki-schema.md`)
- [ ] Step 2: Convert or clip the file (`convert` / `clip`)
- [ ] Step 3: Review the inbox (`inbox`)
- [ ] Step 4: Ingest (`ingest`)
- [ ] Step 5: Rebuild outputs (`graph`, `viewer`)

## Create Mode

When the user asks to add, document, capture, or research a topic, create a new wiki page.

### Step 1: Identify Topic, Type, and Category

- Extract topic from the request ("add kubernetes" → topic `kubernetes`).
- If the user provides a category (IaC, DevOps, AI, other), use it.
- Otherwise infer the category from the topic.
- Pick the page type: concept (reusable idea), guide (how-to), reference (facts), example (code/sample), pattern (reusable solution), runbook (operations), or architecture (design).

### Step 2: Run `migraph create` (MANDATORY)

Every new page MUST be created through the `create` command — never by writing
the file directly. It generates the unified frontmatter, validates the page
**before** it lands in the wiki, and rebuilds outputs on success:

```bash
<python-command> skills/migraph/scripts/migraph create --root <wiki-root> \
  --title "Page Title" --type reference --domain <domain> \
  --summary "1-2 sentence summary" --tags "tag1,tag2" \
  --source "https://..." \
  --connections "../references/other-page.md,../concepts/other-concept.md"
```

Arguments:

| Argument | Required | Purpose |
|----------|----------|---------|
| `--root` | no (default `.`) | Wiki root |
| `--title` | yes | Page title (also derives the slug) |
| `--type` | yes | One of the 13 valid page types |
| `--domain` | yes | Knowledge domain slug (`domain.type.slug` id) |
| `--summary` | yes | 1–2 sentence summary |
| `--tags` | yes* | Comma-separated tags (min 1) |
| `--source` | yes* | Source documentation URL |
| `--connections` | yes* | Comma-separated markdown links to existing wiki pages |
| `--content` | no | Body markdown (defaults to the type template) |
| `--category` / `--status` / `--confidence` / `--version` | no | Metadata overrides |

Blocking validation (fail = no file written, exit 1):

- Frontmatter against `validators/schema.json`
- Required fields (title, type, created, updated, source, tags, confidence, status)
- Required sections for the page type
- At least one `## Connections` markdown link resolving to an existing wiki page
- No placeholder text / weak summary
- No duplicate title or duplicate id

### Step 3: Link Neighbors

After the page is created, link related existing pages:
- Add `## Connections` markdown links (`[Title](../<type>/<slug>.md)`) in the new page — these drive the knowledge graph edges.
- Add a link to the new page from related pages' Connections sections.
- For patterns (cross-category), also link from the category overview page.

Note: the graph only follows markdown links under `## Connections` — Obsidian wikilinks (`[[Note]]`) do not create graph edges.

### Step 4: Verify

- [ ] `migraph create` exited 0 and printed `created ... (validated OK)`
- [ ] `id` is unique and follows `domain.type.slug`
- [ ] `type` is one of the 13 valid values
- [ ] `tags` array has at least 1 item
- [ ] `summary` is 1–2 sentences
- [ ] Connections resolved to real pages (graph edges present in `output/graph/graph.json`)

## Refactor Mode

When the user asks to find duplicates, merge notes, clean up, or organize, run the deduplication script.

### Step 1: Run Duplicate Check

```bash
<python-command> skills/migraph/scripts/migraph deduplicate <wiki-root> [--output results.json] [--report report.md]
```

The script uses:
- **Title similarity**: Fuzzy matching (40% weight)
- **Content similarity**: Word overlap / Jaccard (40% weight)
- **Tag similarity**: Jaccard index (20% weight)
- **Combined score**: Weighted average

### Step 2: Analyze Results

- **HIGH similarity (≥70%)**: Likely duplicates — action required
- **MEDIUM similarity (40–69%)**: Related notes — consider linking
- **LOW similarity (<40%)**: Ignore

For HIGH-similarity pairs, propose a merge:
- Compare both notes' content.
- Keep the richer, more complete note as canonical.
- Merge missing sections from the duplicate.
- Update links pointing to the merged-away note.
- Delete the duplicate.
- Run `dedupe-pages` or rebuild outputs afterwards.

### Alternative: Wiki-level Dedupe

For pages already inside a wiki (same-type pairs, entity-aware), use:

```bash
<python-command> skills/migraph/scripts/migraph dedupe-pages --root <wiki-root>
```

## Browsing HTML Outputs

MiGraph HTML pages are static files under `<wiki-root>/output/`. Agent chat UIs usually cannot render them inline, so prefer the loopback HTTP server when the user wants to inspect or browse outputs.

Default workflow:

```bash
<python-command> skills/migraph/scripts/migraph serve --root <wiki-root>
```

This serves `<wiki-root>/output/` at `http://127.0.0.1:8765/` by default.

Useful URLs:

- Workspace home: `http://127.0.0.1:8765/index.html`
- Inbox review: `http://127.0.0.1:8765/inbox/index.html`
- Local viewer: `http://127.0.0.1:8765/viewer/index.html`
- Knowledge graph: `http://127.0.0.1:8765/graph/index.html`
- Graph report: `http://127.0.0.1:8765/graph/report.html`

OpenClaw integration:

- After `viewer`, `graph`, `inbox`, or `graph-report`, run `serve` when the user wants to browse the results.
- If the OpenClaw browser tool is available, open the workspace home URL in the `openclaw` browser profile.
- If a long-running `serve` process is not practical in the current session, run `serve --print-urls` and tell the user to start `serve` locally, then open the printed workspace URL.

## Completion Criteria

- After initialization, report where the wiki was created.
- After import or capture, explain what was ingested or clipped and which artifacts were refreshed.
- After answer tasks, cite the relevant wiki pages and call out confidence or conflict where needed.
- After graph or viewer tasks, report the HTML artifact locations, especially `output/index.html`.
- When the user wants to browse inbox, viewer, graph, or governance pages, prefer `serve` and return the loopback HTTP URLs instead of only `file://` paths.
- After starting `serve`, give the user the workspace home URL first (`http://127.0.0.1:8765/index.html` by default) and, in OpenClaw, offer to open it with `openclaw browser --browser-profile openclaw open <url>`.
- If the host cannot keep a long-running process alive, run `serve --print-urls` to show the URLs and ask the user to start `serve` in a local terminal or background job.
- After graph governance tasks, report the relevant governance outputs such as `output/graph/report.html`.
- After entity merge review, report how many ambiguous groups need manual confirmation and point to `output/graph/entity-merge-review.html`.
- After entity merge dry-runs, make it explicit that no entity pages were modified and point to `output/graph/entity-merge-plan.html`.
- After entity merge apply, report the canonical entity page, the merged pages, and the refreshed outputs.
- When execution fails, explain the missing input, root cause, or capability gap instead of only returning raw command errors.
