---
name: knowledge
description: Complete knowledge base management - create, organize, and maintain Obsidian-style knowledge notes with RAG compatibility. Covers the full lifecycle: create notes across 7 types (concept, guide, reference, example, pattern, runbook, architecture) with unified frontmatter and folder organization, validate schema, detect and merge duplicates, optimize cross-linking, and maintain INDEX files.
triggers: ["add note", "document this", "create knowledge", "research", "learn about", "build knowledge", "capture", "add IaC", "add DevOps", "add AI", "create pattern", "build runbook", "capture architecture", "find duplicates", "merge notes", "clean up", "check duplicates", "organization", "maintain knowledge", "optimize knowledge", "deduplicate", "fix overlapping notes"]
tools: [filesystem, read, write, glob, mkdir, grep]
category: knowledge-management
version: 2.0.0
tags: [knowledge, obsidian, rag, automation, documentation]
---

# Knowledge

Complete knowledge base management skill that handles the full knowledge lifecycle: creating new notes across 7 types, organizing by category, validating schema, detecting duplicates, and maintaining cross-links. Built on Obsidian best practices with RAG compatibility.

---

# When to use

## Creation Mode Trigger Phrases
- "add [topic]" or "add note about [topic]"
- "add [category]/[topic]" - e.g., "add IaC/ansible", "add DevOps/kubernetes"
- "document [subject]"
- "create knowledge about [topic]"
- "research [topic]"
- "capture information about [subject]"
- "build knowledge base on [topic]"
- "learn about [subject]"
- "create documentation about [X]"
- "create pattern for [X]"
- "build runbook for [X]"
- "capture architecture of [X]"

## Refactor Mode Trigger Phrases
- "find duplicates"
- "check for duplicates"
- "merge notes"
- "clean up notes"
- "deduplicate"
- "fix overlapping notes"
- "organize knowledge"
- "maintain knowledge"

---

# Mode Selection

The skill automatically detects which mode to use:

| User Request | Mode |
|-------------|------|
| New topic to document | Create Mode |
| Add existing knowledge | Create Mode |
| Research something | Create Mode |
| Find duplicates | Refactor Mode |
| Merge notes | Refactor Mode |
| Clean up | Refactor Mode |

---

# CREATE MODE Instructions

Follow these steps when creating new knowledge notes.

## Step 1: Identify Topic, Type, and Category

### A. Determine the TOPIC (REQUIRED)
Extract topic from user's request:
- "add kubernetes" → topic: `kubernetes`
- "add ansible" → topic: `ansible`

### B. Determine the CATEGORY (if provided by user)
Extract category from request format: `"add <category>/<topic>"`:
- "add IaC/ansible" → category: `IaC`, topic: `ansible`
- "add DevOps/kubernetes" → category: `DevOps`, topic: `kubernetes`
- "add AI/langchain" → category: `AI`, topic: `langchain`

If no category provided, topic goes directly to `examples/knowledge/<topic>/`

### C. Determine CONTENT TYPE (7 types)

Type inference:
| Phrase | Type | Folder |
|--------|------|--------|
| "how does X work" | concept | concepts/ |
| "explain X", "what is X" | concept | concepts/ |
| "how to do X" | guide | guides/ |
| "setup", "tutorial" | guide | guides/ |
| "commands", "reference" | reference | references/ |
| "example", "code", "sample" | example | examples/ |
| "pattern", "best practice", "solved problem" | pattern | patterns/ |
| "runbook", "incident", "troubleshooting" | runbook | runbooks/ |
| "architecture", "system design" | architecture | architectures/ |

---

## Step 2: Create Folder Structure (CRITICAL)

**If category provided:**
```
examples/knowledge/<category>/<topic>/
    ├── concepts/
    ├── guides/
    ├── references/
    ├── examples/
    ├── patterns/
    ├── runbooks/
    ├── architectures/
    └── INDEX.md
```

Example:
- "add IaC/ansible" → `examples/knowledge/IaC/ansible/`
- "add DevOps/kubernetes" → `examples/knowledge/DevOps/kubernetes/`
- "add AI/langchain" → `examples/knowledge/AI/langchain-ai/`

**If no category:**
```
examples/knowledge/<topic>/
    ├── concepts/
    ├── guides/
    ├── references/
    ├── examples/
    ├── patterns/
    ├── runbooks/
    ├── architectures/
    └── INDEX.md
```

**For cross-category patterns:**
```
examples/knowledge/patterns/
    └── <pattern-name>.md
```

Example:
- "create pattern for DRY configs" → `examples/knowledge/patterns/terragrunt-dry-configs.md`

**Category Folders (always use these paths):**
```
examples/knowledge/
├── IaC/           # terraform, terragrunt, ansible
├── DevOps/         # kubernetes, argocd
├── AI/             # deepagents, langchain-ai
└── patterns/      # cross-category patterns
```

---

## Step 3: Generate Example from Documentation (CRITICAL)

**IMPORTANT**: When creating a new topic, ALWAYS fetch documentation to create an example in `examples/` folder.

### Supported Categories

| Category | Topics |
|----------|-------|
| IaC | terraform, terragrunt, ansible, puppet, chef |
| DevOps | kubernetes, argocd, docker, helm, kubectl |
| AI | deepagents, langchain, langgraph, openai |

### A. Find Documentation URL

Search for official documentation based on topic:

| Topic | Documentation |
|----------|---------------|
| kubernetes | https://kubernetes.io/docs/ |
| terraform | https://www.terraform.io/docs/ |
| terragrunt | https://docs.terragrunt.com/ |
| ansible | https://docs.ansible.com/ |
| argocd | https://argo-cd.readthedocs.io/ |
| deepagents | https://docs.langchain.com/oss/python/deepagents/overview |
| langchain | https://python.langchain.com/ |
| docker | https://docs.docker.com/ |
| aws | https://docs.aws.amazon.com/ |

### B. Fetch and Create Example

1. Use web search or fetch to get official documentation
2. Extract a practical code example
3. Create file in `examples/` folder using `templates/example.md`

---

## Step 4: Generate File Path

Format: `examples/knowledge/<category>/<type>/<slug>.md`

Example:
- kubernetes + concept + architecture → `examples/knowledge/kubernetes/concepts/kubernetes-architecture.md`

Slug rules:
- Lowercase
- Hyphen-separated
- Remove special characters

---

## Step 5: Create Note Content

### Select Template by Type

| Type | Template |
|------|----------|
| concept | `templates/concept.md` |
| guide | `templates/guide.md` |
| reference | `templates/reference.md` |
| example | `templates/example.md` |
| pattern | `templates/pattern.md` |
| runbook | `templates/runbook.md` |
| architecture | `templates/architecture.md` |

### Unified Frontmatter Schema (ALL types)

```yaml
---
# Core (required for all types)
title: <Title>              # human-readable
type: <concept|guide|reference|example|pattern|runbook|architecture>
category: <category>        # IaC | DevOps | AI | other
domain: <domain>            # e.g., sre, kubernetes, terraform
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:                       # list, 2-space indent, min 1
  - <tag1>
status: active              # draft | active | deprecated | archived
summary: <1-2 sentence summary>
# Schema (required for pattern/runbook/architecture; optional for others)
id: <domain>.<type>.<slug>
version: "1.0.0"
confidence: high            # high | medium | low
source: docs                # docs | internal | external
inputs: []
outputs: []
dependencies:
  - [[<related-note>]]
quality_score: 0            # 0-100
# Optional
aliases:
  - <alternative-name>
---
```

**Critical YAML rules:**
- Opening `---` must be on line 1 with no preceding blank lines
- Use **two-space indentation** for list items (not tabs)
- List items must use `- ` (dash + space) prefix
- **NEVER use inline list format**: `[tag1, tag2]` is invalid
- String values with colons should be quoted: `title: "My Note: A Subtitle"`
- Boolean values: `true` / `false` (lowercase, no quotes)
- Dates: ISO 8601 format `YYYY-MM-DD`
- Wikilinks in frontmatter must be quoted: `project: "[[Project Name]]"`

### Naming Convention
- Filename: `slug-case.md` (e.g., `incident-response.md`)
- ID: `{domain}.{type}.{slug}` (e.g., `sre.runbook.incident-response`)

---

## Step 6: Use Obsidian Markdown Features

### Wikilinks (Internal Links)

```markdown
[[Note Name]]                          Link to note by name
[[Note Name|Display Text]]             Custom display text
[[Note Name#Heading]]                  Link to a specific heading
[[Note Name#^block-id]]                Link to a specific block
```

### Callouts

Use callouts for highlighted information:

```markdown
> [!note]
> This is a standard note callout.

> [!warning] Custom Title
> Callout with a custom title.

> [!tip]+ Expanded by default
> The + makes this callout expanded.

> [!example]
> Example callout.
```

Common callout types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`.

### Block IDs

Add unique IDs for precise linking:

```markdown
This paragraph can be linked from anywhere.
^my-block-id
```

### Tags

Inline tags in body:

```markdown
#tag              # Simple tag
#nested/tag       # Nested tag hierarchy
#category/active # Deep nesting
```

### Embeds

Embed content from other notes:

```markdown
![[Other Note]]              # Embed full note
![[Other Note#Heading]]      # Embed section
![[image.png]]               # Embed image
```

---

## Step 7: Create/Update INDEX.md

**IMPORTANT**: INDEX.md must have YAML frontmatter with name, description, and tags!

In `examples/knowledge/<category>/INDEX.md`:

```markdown
---
name: <category>
description: <description of this knowledge category>
tags: [<tag1>, <tag2>, <tag3>]
---

# <Category>

## Overview
Brief description of this knowledge category.

### Concepts
- [[slug]] - description

### Guides
- [[slug]] - description

### References
- [[slug]] - description

### Examples
- [[<category>-example]] - Practical example from official documentation

---

*Last updated: YYYY-MM-DD*
```

**Example for Kubernetes:**
```markdown
---
name: kubernetes
description: Kubernetes (k8s) - Container orchestration platform...
tags: ['kubernetes', 'containers', 'orchestration', 'devops', 'cloud-native']
---

# Kubernetes

## Overview
...

*Last updated: 2026-04-27*
```

**Update rules:**
- **For patterns (cross-category)**: add entry to `examples/knowledge/patterns/INDEX.md`
- **For topics in categories**: add entry to category INDEX.md AND main INDEX.md (`examples/knowledge/INDEX.md`)

---

## Step 8: Validate

Check:
- [ ] `id` is unique and follows `domain.type.slug`
- [ ] `type` is one of the 7 valid values
- [ ] `domain` exists or will be created
- [ ] `tags` array has at least 1 item
- [ ] `summary` is 1-2 sentences
- [ ] Category folder exists
- [ ] Type subfolder exists (concepts/, guides/, references/, examples/, patterns/, runbooks/, architectures/)
- [ ] Note in correct subfolder
- [ ] INDEX.md exists and has frontmatter (name, description, tags)
- [ ] Frontmatter uses two-space indentation
- [ ] Frontmatter uses list format for tags (not inline)
- [ ] Dates in ISO 8601 format (YYYY-MM-DD)
- [ ] At least one [[wikilink]] in body
- [ ] Example file created in examples/ (fetched from official documentation)

Optionally validate against the schema:
```bash
python3 -c "
import json, sys, yaml
with open('<file>') as f:
    fm = yaml.safe_load(f.read().split('---')[1])
schema = json.load(open('skills/knowledge/validators/schema.json'))
required = schema['required']
missing = [k for k in required if k not in fm]
sys.exit(1) if missing else print('VALID')
"
```

---

# REFACTOR MODE Instructions

Follow these steps when refactoring existing knowledge.

**IMPORTANT**: Use the bundled script for automated duplicate checking:

```bash
python3 skills/knowledge/scripts/deduplicate.py <knowledge-path> [--output results.json] [--report report.md]
```

The script uses multiple similarity strategies:
- **Title similarity**: Fuzzy matching (40% weight)
- **Content similarity**: Word overlap / Jaccard (40% weight)
- **Tag similarity**: Jaccard index (20% weight)
- **Combined score**: Weighted average

## Step 1: Run Duplicate Check

Execute the deduplication script:

```bash
python3 skills/knowledge/scripts/deduplicate.py examples/knowledge/ --output duplicate_results.json --report duplicate_report.md
```

## Step 2: Analyze Results

The script outputs:
- **HIGH similarity (≥70%)**: Likely duplicates - action required
- **MEDIUM similarity (40-69%)**: Related notes - consider linking
- **LOW similarity (<40%)**: Ignore

### Running the Script Manually

If you cannot run Python:

## Step 1: Scan Knowledge Base

Traverse all markdown files:

```bash
knowledge/**/*.md
```

Ignore:
- INDEX.md
- Empty files

For each note, extract:
- Title
- Frontmatter
- Content
- Links

---

## Step 2: Normalize Content

For comparison:
- Normalize titles (lowercase, remove special chars)
- Ignore formatting
- Focus on semantic meaning

---

## Step 3: Detect Similarity

### HIGH Similarity (likely duplicate)
- Same or similar title
- Same concept
- Redundant explanations

### MEDIUM Similarity (related)
- Similar sections
- Overlapping examples
- Same domain

### LOW Similarity (ignore)
- Only shared tags
- Weak overlap

---

## Step 4: Generate Report

Output:

```markdown
### HIGH similarity
- [[note-a]] ↔ [[note-b]]
  - reason:

### MEDIUM similarity
- [[note-c]] ↔ [[note-d]]
```

---

## Step 5: Suggest Actions

### HIGH Similarity
- Select primary note (better structure)
- Suggest merge:
  - What to keep
  - What to merge
  - What to remove

### MEDIUM Similarity
- Add [[links]]
- Add cross-references

---

## Step 6: Apply Refactor (ONLY if requested)

### Merge Strategy
1. Keep best structured note
2. Merge unique sections
3. Remove duplicated content
4. Preserve all useful information

### Deprecation Format
```markdown
---
status: deprecated
---

This note has been merged into [[primary-note]].

*Redirected on: YYYY-MM-DD*
```

---

# Rules

1. **Create folder structure FIRST** (create mode)
2. **Use topic as category** - from user's request
3. **Separate by type** - concepts/guides/references/examples/patterns/runbooks/architectures
4. **Never placeholders** - fill all sections
5. **Cross-link** - every note links to related content
6. **NEVER auto-delete** - always suggest (refactor mode)
7. **Update INDEX** - after changes
8. **Create examples/ folder** - always include examples/ folder in structure
9. **Atomicity** - one idea per file, maximum ~500 lines; split if longer
10. **Avoid duplication** - search existing knowledge before creating; if similarity > 0.85, suggest merge
11. **Frontmatter best practices**:
    - Two-space indentation (no tabs)
    - List format for tags (not inline)
    - ISO 8601 dates (YYYY-MM-DD)
    - Quoted wikilinks in frontmatter
12. **Use Obsidian features** - wikilinks, callouts, block IDs, embeds

---

# Output Expectations

## Create Mode Structure
```
examples/knowledge/
└── <category>/
    ├── concepts/
    │   └── <category>-<topic>.md
    ├── guides/
    ├── references/
    ├── examples/
    │   └── <category>-example.md
    ├── patterns/
    ├── runbooks/
    ├── architectures/
    └── INDEX.md
```

## Refactor Mode Output
- Duplicate report grouped by similarity
- Suggested actions for each pair
- Merge suggestions for HIGH similarity

---

# Resources

- templates/ (7 templates: concept, guide, reference, example, pattern, runbook, architecture)
- validators/schema.json (unified 7-type frontmatter schema)
- hooks/post_create.md (post-creation actions)
- resources/quality_rules.md
- resources/template.md
- scripts/deduplicate.py (duplicate detection)
- scripts/update_schema.py (frontmatter schema migration)
