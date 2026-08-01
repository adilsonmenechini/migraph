# MiGraph

[![License](https://img.shields.io/github/license/adilsonmenechini/migraph)](LICENSE)
[![Python](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)

**Your local knowledge base, powered by conversation.**

Transform loose documents, webpages, notes, and conversations into a durable Markdown workspace. Talk to your agent to create, organize, and research knowledge — with inbox review, local browsing, and an interactive knowledge graph you open in the browser.

[![Workspace preview](docs/assets/output-hub-preview.png)](docs/assets/output-hub-preview.png)

---

## Get started in 2 minutes

1. **Install the skill** — point your agent to this repository and ask to install.
2. **Create your wiki** — "Create a local knowledge base called `My Studies`."
3. **Capture something** — "Save this article to the inbox: https://example.com/article"
4. **Ask** — "What have we already decided about context budget?"
5. **Browse** — "Show the graph" → opens in browser and you're done.

[![Inbox review preview](docs/assets/inbox-preview.png)](docs/assets/inbox-preview.png)

---

## How it works

MiGraph is a **native skill for agents**, following the open [Agent Skills](https://agentskills.io) format. Your agent reads `SKILL.md`, understands your intent, and takes the right action — without you needing to memorize commands.

| Agent | How to use |
| --- | --- |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Install the repo as a skill, then ask it to create and query your wiki |
| [OpenClaw](https://openclaw.ai) | Full skill workflow; use `serve` + the integrated browser to open the HTML |
| [Trae](https://www.trae.ai) | Install in `.trae/skills`, then manage the wiki in chat |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Local skill directory + command execution |
| [OpenAI Codex](https://developers.openai.com/codex) / Codex CLI | Skill-compatible agents with local file access |
| [Cursor](https://cursor.com) | Agent mode with project skills |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Skill-compatible CLI agent |
| [GitHub Copilot](https://github.com/features/copilot) | Agent/coding flows in VS Code with skill support |
| Other skill hosts | Any product that loads `SKILL.md` and runs `python3 scripts/migraph …` locally |

**Requirement:** a local environment with Python 3. MiGraph configures its runtime automatically on first use. Pure cloud chat, without file or shell access, cannot run a local wiki.

> **Example prompt for your agent:**
>
> Please install the MiGraph skill from https://github.com/adilsonmenechini/migraph, configure the runtime, and run a health check to confirm everything works on my machine.

Then just talk:

> Create a local knowledge base called `My Studies`.
>
> Save this article to the inbox: https://example.com/article
>
> Import this PDF: /path/to/file.pdf
>
> Does my wiki say anything about context budget?
>
> Show the graph and open the workspace in the browser.

---

## What MiGraph produces

A workspace with ready-to-browse HTML:

| Artifact | What it is |
| --- | --- |
| `output/index.html` | 🏠 Workspace home |
| `output/inbox/index.html` | 📥 Review captures before importing |
| `output/viewer/index.html` | 📖 Wiki page browser |
| `output/graph/index.html` | 🌐 Interactive knowledge graph |
| `output/graph/report.html` | 📊 Graph governance report |
| `output/graph/entity-merge-review.html` | 🔍 Ambiguous alias review |
| `output/graph/entity-merge-plan.html` | 📋 Entity merge simulation |

### Preview

![Workspace home](docs/assets/output-hub-preview.png)

**Workspace home** — recent changes, next actions, and inbox backlog summary in one place.

![Inbox review](docs/assets/inbox-preview.png)

**Inbox review** — review webpages, files, and notes before importing. Grouped into `ready`, `to review`, and `weak`.

![Local viewer](docs/assets/viewer-preview.png)

**Viewer** — browse by page type, confidence, and status. Open any page without leaving the HTML workspace.

![Knowledge graph](docs/assets/graph-preview.png)

**Knowledge graph** — explore semantic relationships between topics, concepts, entities, and claims. Three views: `knowledge`, `document`, and `suggested`.

![Governance report](docs/assets/graph-report-preview.png)

**Governance report** — graph health signals: isolated pages, fragile hubs, suggested links, and merge candidates.

---

## What you can ask your agent

| You say | MiGraph does |
| --- | --- |
| Create a wiki called `Research Notes` | Initializes the local workspace |
| Save this URL or file to the inbox | Captures it for later review |
| Import the ready inbox items | Promotes reviewed captures to pages |
| Does my wiki say anything about X? | Answers with real evidence |
| Save this answer as a `query` page | Persists valuable results |
| Show the knowledge graph | Generates/updates the graph HTML |
| Review entity merge candidates | Points out ambiguous aliases |
| Open the workspace in the browser | Runs `serve` and returns http://127.0.0.1:8765 |

---

## Why use MiGraph

- **Built for agents:** you talk, you don't type commands.
- **Local and private:** Markdown files are the source of truth on your machine.
- **Browsable HTML:** inbox, viewer, and graph are real pages, not dumps.
- **Structured knowledge:** the graph represents concepts, claims, and governance — not just files.

---

## Advanced features

### Knowledge graph (schema v2)

Since `v1.6.0`, the graph uses `default_view = knowledge` and can contain:

- Page-backed nodes: `source`, `topic`, `concept`, `decision`, `synthesis`, `query`, `entity`
- Claims extracted from structured content
- Semantic relations: `about`, `belongs_to`, `depends_on`, `asserts`, `supports`, `contradicts`, `suggests_related_to`

The graph goes beyond file references — it represents knowledge structure, evidence, and entity governance.

### Artificial intelligence (disabled by default)

Remote features require configuration. Without them, MiGraph uses local heuristics.

**Content generation** (`crystallize`, `digest`):

| Variable | Rule | Purpose |
| --- | --- | --- |
| `MIGRAPH_LLM_API_KEY` | Required | Provider API key |
| `MIGRAPH_LLM_BASE_URL` | Required | Chat endpoint URL |
| `MIGRAPH_LLM_MODEL` | Required | Model name |
| `MIGRAPH_LLM_TEMPERATURE` | Optional | Temperature |

Works with OpenAI, DeepSeek, MiniMax, local Ollama, and any compatible endpoint.

**Entity embeddings** (`entity-merge-review`, `graph-report`, `health`, `dedupe-pages`):

| Variable | Rule | Purpose |
| --- | --- | --- |
| `MIGRAPH_EMBED_API_KEY` | Required | API key |
| `MIGRAPH_EMBED_BASE_URL` | Optional | Endpoint; defaults to local Ollama |
| `MIGRAPH_EMBED_MODEL` | Optional | Model; defaults to `BAAI/bge-m3` |

To use embeddings, run Ollama locally:

```bash
ollama pull bge-m3
ollama serve
```

Then set `MIGRAPH_EMBED_API_KEY=dummy` (Ollama does not require a real key, but the variable must exist). The endpoint defaults to `http://localhost:11434/v1/embeddings`.

---

## Manual installation

If you prefer to do it yourself:

```bash
git clone https://github.com/adilsonmenechini/migraph MiGraph
cd MiGraph
python3 scripts/migraph bootstrap
python3 scripts/migraph doctor --repo-root .
```

Then install the folder in your agent's skill directory according to each host's documentation.

---

## CLI reference (for agents and advanced users)

One stable entry point:

```bash
python3 scripts/migraph <command> [args]
```

Common commands: `init`, `clip`, `ingest`, `inbox`, `viewer`, `graph`, `graph-report`, `entity-merge-review`, `entity-merge-apply`, `serve`, `health`, `status`, `doctor`, `bootstrap`, `convert`, `batch-clip`, `batch-ingest`, `ask`, `correct`, `query`, `crystallize`, `digest`, `lint`, `rebuild-index`, `dedupe-pages`, `migrate-skill-kwonledge`.

See `SKILL.md` for the behavior contract and intent mapping.

---

## Repository documentation

- **README.md** — this page
- **SKILL.md** — behavior contract for agents
- **CHANGELOG.md** — version history

---

## License

MIT
