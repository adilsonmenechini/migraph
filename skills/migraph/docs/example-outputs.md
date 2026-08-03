# MiGraph Example Outputs

_Real command outputs captured on 2026-08-02 by running each command against a clean demo workspace. `<wiki-root>` is a placeholder for your workspace path. All commands run via the unified CLI: `python3 scripts/migraph <command>`._

## init

```text
Initialized wiki at <wiki-root>
Next: run `python scripts/migraph viewer --root <wiki-root>` to generate the local viewer page.
Next: run `python scripts/migraph graph --root <wiki-root>` to generate the knowledge graph page.
```

## clip (web)

```text
Clipped Knowledge graph into inbox
Inbox raw: raw/inbox/2026-08-02-knowledge-graph.html
Inbox normalized: normalized/inbox/2026-08-02-knowledge-graph.md
Inbox metadata: normalized/inbox/2026-08-02-knowledge-graph.json
Web adapter: generic
Capture mode: auto
Capture state: ok
Capture reason: ready
Media status: kept_remote (0/6)
Inbox review: output/inbox/index.html
Inbox review URI: file://<wiki-root>/output/inbox/index.html
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
Next: run `python scripts/migraph ingest --root <wiki-root> --source normalized/inbox/2026-08-02-knowledge-graph.md`
```

## clip (text)

```text
Clipped MiGraph is a local knowledge base tool that organizes notes, into inbox
Inbox raw: raw/inbox/2026-08-02-migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md
Inbox normalized: normalized/inbox/2026-08-02-migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md
Inbox review: output/inbox/index.html
Inbox review URI: file://<wiki-root>/output/inbox/index.html
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
Next: run `python scripts/migraph ingest --root <wiki-root> --source normalized/inbox/2026-08-02-migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md`
```

## batch-ingest (review)

```text
# MiGraph Batch Ingest

- Root: <wiki-root>
- Quality Filter: review
- Limit: all
- Dry Run: no
- Matched Items: 2

## Selected Items

- 2026 08 02 migraph is a local knowledge base tool that organizes notes | normalized/inbox/2026-08-02-migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md | quality=review
- Knowledge graph | normalized/inbox/2026-08-02-knowledge-graph.md | quality=review

## Results

- Ingested: 2
- Cleared Inbox Artifacts: 5
- Failed: 0
- MiGraph is a local knowledge base tool that organizes notes, -> wiki/sources/migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md
- Knowledge graph -> wiki/sources/knowledge-graph.md

Inbox review: output/inbox/index.html
Inbox review URI: file://<wiki-root>/output/inbox/index.html
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
Next: run `python scripts/migraph viewer --root <wiki-root>` to refresh the local viewer page.
Next: run `python scripts/migraph graph --root <wiki-root>` to refresh the knowledge graph page.
```

## viewer

```text
Built viewer for 7 pages
Viewer metadata: output/viewer/viewer.json
Viewer page: output/viewer/index.html
Viewer page URI: file://<wiki-root>/output/viewer/index.html
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
Browse via HTTP: run `python scripts/migraph serve --root <wiki-root>` -> http://127.0.0.1:8765/index.html
```

## graph

```text
Built graph with 14 nodes and 27 edges
Graph data: output/graph/graph.json
Graph summary: output/graph/graph.md
Graph viewer: output/graph/index.html
Graph viewer URI: file://<wiki-root>/output/graph/index.html
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
Browse via HTTP: run `python scripts/migraph serve --root <wiki-root>` -> http://127.0.0.1:8765/index.html
```

## graph-report

```text
# MiGraph Graph Report

- Root: <wiki-root>
- Summary: pages=7, relations=20, entities=5, aliasedEntities=0, aliases=0, ambiguousAliasGroups=0, ambiguousEntities=0, isolatedPages=0, weakPages=0, hubStubs=0, fragileBridges=0, isolatedClusters=1, suggestedLinks=8
- Isolated Pages: 0
- Hub Stubs: 0
- Fragile Bridges: 0
- Suggested Links: 8

Top Actions:
- Reconnect isolated clusters back to the main graph.
- Review suggested links and convert strong candidates into explicit page links.

Graph report: output/graph/report.html
Graph report URI: file://<wiki-root>/output/graph/report.html
Graph report markdown: output/graph/report.md
Graph report data: output/graph/report.json
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
Browse via HTTP: run `python scripts/migraph serve --root <wiki-root>` -> http://127.0.0.1:8765/index.html
```

## entity-merge-review

```text
# MiGraph Entity Merge Review

- Root: <wiki-root>
- Summary: No new ambiguous entity merge groups were detected.
- Ambiguous Alias Groups: 0
- Ambiguous Entities: 0

Top Actions:
- No manual entity merge review is needed right now. You can keep expanding entity knowledge objects.

Entity merge review: output/graph/entity-merge-review.html
Entity merge review URI: file://<wiki-root>/output/graph/entity-merge-review.html
Entity merge review markdown: output/graph/entity-merge-review.md
Entity merge review data: output/graph/entity-merge-review.json
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
```

## status

```text
# MiGraph Status

- Root: <wiki-root>
- Title: migraph-demo
- Pages: 7 (entity=5, source=2)
- Inbox: total=0, ready=0, review=0, weak=0
- Output Home: ready (updated 2026-08-02 02:32)
- Viewer: ready (generated 2026-08-02, pageCount=7)
- Graph: ready (generated 2026-08-02, schema=v2, defaultView=knowledge, nodes=7, edges=20, knowledgeNodes=14, claims=7, entities=5, aliasedEntities=0, aliases=0, ambiguousAliasGroups=0, ambiguousEntities=0, suggestedLinks=8)
- Graph Report: ready (generated 2026-08-02, isolatedPages=0, isolatedEntities=0, aliasedEntities=0, aliases=0, ambiguousAliasGroups=0, ambiguousEntities=0, hubStubs=0, fragileBridges=0, clusters=1)
- Inbox Review: ready (updated 2026-08-02 02:32)
```

## health

```text
# MiGraph Health Report

- Root: <wiki-root>
- Title: migraph-demo
- Errors: 0
- Warnings: 0

## Summary

- Pages: total=7, types=entity=5, source=2
- Inbox: total=0, ready=0, review=0, weak=0
- Outputs: hub=ready, viewer=ready, graph=ready, inbox=ready
- Knowledge Graph: schema=v2, defaultView=knowledge, knowledgeNodes=14, claims=7, entities=5, aliasedEntities=0, aliases=0, ambiguousAliasGroups=0, ambiguousEntities=0, suggestedEdges=8
- Graph Report: ready, isolatedPages=0, isolatedEntities=0, aliasedEntities=0, aliases=0, ambiguousAliasGroups=0, ambiguousEntities=0, hubStubs=0, fragileBridges=0, clusters=1

## Result

- All checks passed
```

## ask (local heuristics, no AI configured)

```text
# Ask Result

- Date: 2026-08-02
- Question: What is a knowledge graph?
- Consulted: 5

## Answer

- 当前最相关的条目是《MiGraph is a local knowledge base tool that organizes notes,》，类型为 source，置信度为 extracted，状态为 active。
- 该页摘要：MiGraph is a local knowledge base tool that organizes notes, webpages and conversations into a Markdown workspace with an interactive knowle
- 最直接的证据摘录来自《MiGraph is a local knowledge base tool that organizes notes,》的“Summary”部分：MiGraph is a local knowledge base tool that organizes notes, webpages and conversations into a Markdown workspace with an interactive knowle
- 其他可交叉参考的页面有：《Knowledge graph》；《Knowledge graph》；《2026-08-02-migraph-is-a-local-knowledge-base-tool-that-organizes-notes》。
- 需要额外验证的页面包括：《For》。
- 检索排序优先考虑标题命中、摘要命中、置信度、状态和更新时间；最佳匹配得分为 53。

## Evidence

- 《MiGraph is a local knowledge base tool that organizes notes,》 | path: wiki/sources/migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md | type: source | section: Summary | ref: wiki/sources/migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md#summary | confidence: extracted | status: active | score: 39 | snippet: MiGraph is a local knowledge base tool that organizes notes, webpages and conversations into a Markdown workspace with an interactive knowle
- 《Knowledge graph》 | path: normalized/articles/2026-08-02-knowledge-graph.md | type: normalized | section: References | ref: normalized/articles/2026-08-02-knowledge-graph.md#references | confidence: extracted | status: active | score: 50 | snippet: 1. ↑ "What is a Knowledge Graph?". *ontotext*. 2018. Retrieved 2025-12-05. 2. ↑ Kumar Pandey, Atul (2020-12-18). "What defines a knowledge graph?". *AtulHost*. Retrieved 2025-12-05. 3. 1 2 3 Ehrlinger, Lisa; Wöß, Wolfram (2016). *Towards a Definition of Knowledge Graphs* (PDF). SEMANTiCS2016. Leipzig: Joint Proceedings of the Posters and Demos Track of 12th International Conference on Semantic Sys
- 《Knowledge graph》 | path: wiki/sources/knowledge-graph.md | type: source | section: Key Points | ref: wiki/sources/knowledge-graph.md#key-points | confidence: extracted | status: active | score: 42 | snippet: Main article: Ontology (information science) "Ontology (information science)") A knowledge graph formally represents sem - Knowledge graphs Ontology (information science) "Category:Ontology (information science)") Formal semantics (natural lan - Articles with short description Short description is different from Wikidata CS1 maint: url-status CS1: long volume valu - There is no single commonly acc
```

## lint

```text
# Lint Report

- Date: 2026-08-02
- Issues: 2

- [weak-summary] wiki/sources/knowledge-graph.md summary looks incomplete because it lacks terminal punctuation
- [weak-summary] wiki/sources/migraph-is-a-local-knowledge-base-tool-that-organizes-notes.md summary looks incomplete because it lacks terminal punctuation
```

## correct

```text
Created wiki/concepts/a-knowledge-graph-is-a-graph-structured-knowledge-representation-with-typed-relations-between-entities.md
```

## query

```text
Created wiki/queries/how-does-migraph-organize-knowledge.md
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
```

## crystallize (local heuristics)

```text
Created wiki/concepts/knowledge-graph.md
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
```

## digest (local heuristics)

```text
Created wiki/syntheses/knowledge-graphs-digest.md
Output hub: output/index.html
Output hub URI: file://<wiki-root>/output/index.html
```

## serve (--print-urls)

```text
MiGraph output server: http://127.0.0.1:65198
Wiki root: <wiki-root>
Serving directory: <wiki-root>/output
Workspace Home: http://127.0.0.1:65198/index.html
Inbox Review: http://127.0.0.1:65198/inbox/index.html
Local Viewer: http://127.0.0.1:65198/viewer/index.html
Knowledge Graph: http://127.0.0.1:65198/graph/index.html
Graph Governance Report: http://127.0.0.1:65198/graph/report.html
Entity Merge Review: http://127.0.0.1:65198/graph/entity-merge-review.html
OpenClaw browser: openclaw browser --browser-profile openclaw open http://127.0.0.1:65198/index.html
```

## doctor (on repo root)

```text
# Runtime Doctor Report

- Repo Root: <repo-root>
- Python: <venv-python>
- Issues: 0

## Capability Status

- Core runtime: ready
- Web import: ready
- PDF import: ready
- DOCX import: ready
- XLSX import: ready
- XLS import: ready
- PPTX import: ready

- All checks passed
```
