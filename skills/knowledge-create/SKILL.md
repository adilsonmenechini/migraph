---
name: knowledge-create
description: Create structured, validated knowledge files for Obsidian + RAG + Agents. Use this skill whenever user wants to document concepts, create patterns, runbooks, or architecture docs with atomic structure, proper frontmatter, and RAG compatibility. Triggers on: "create knowledge", "add note", "document", "build runbook", "create pattern", "capture architecture".
version: 1.0.0
tags: [knowledge, obsidian, rag, automation, documentation]
---

# Knowledge Create

Create high-quality, atomic knowledge files using standardized structure, metadata, and relationships.

## 🎯 Objective

This skill ensures:
- **Consistency**: Standardized templates and frontmatter
- **Discoverability**: Proper metadata for search/filter
- **Compatibility**: Works with Obsidian + Qdrant + Neo4j
- **Minimal Duplication**: Pre-creation search

## 📥 Inputs

```yaml
title: string          # Required
type: string           # concept | pattern | runbook | architecture
domain: string         # e.g., sre, kubernetes, terraform
tags: string[]         # e.g., [monitoring, alerting]
summary: string        # 1-2 sentence summary
content: markdown      # Main content
related: string[]      # IDs of related knowledge
source: string         # Documentation URL
confidence: string    # low | medium | high
```

## 📤 Output

- A `.md` file created in the correct folder
- Valid frontmatter with all required fields
- Linked references using [[id]] wikilinks
- Ready for indexing (Obsidian + RAG)

## 📂 Folder Mapping

| Type | Path |
|------|------|
| concept | `examples/knowledge/<category>/<topic>/concepts/` |
| pattern | `examples/knowledge/patterns/` |
| runbook | `examples/knowledge/<category>/<topic>/runbooks/` |
| architecture | `examples/knowledge/<category>/<topic>/architectures/` |

**Category Mapping:**
| Domain | Category |
|--------|----------|
| terraform, terragrunt, ansible | IaC |
| kubernetes, argocd, docker | DevOps |
| deepagents, langchain | AI |

## 🧱 Frontmatter Template

```yaml
---
id: {{domain}}.{{type}}.{{slug}}
type: {{type}}
domain: {{domain}}
tags:
  - {{tag1}}
  - {{tag2}}
summary: {{summary}}
related:
  - [[{{related-id-1}}]]
  - [[{{related-id-2}}]]
source: {{source}}
created_at: {{now}}
updated_at: {{now}}
confidence: {{confidence}}
version: "1.0.0"
quality_score: 0
---
```

## 🧠 Rules

### 1. Atomicity
- One idea per file
- Maximum ~500 lines
- If too long, split into multiple files

### 2. Naming Convention
- Filename: `slug-case.md` (e.g., `incident-response.md`)
- ID: `{domain}.{type}.{slug}` (e.g., `sre.runbook.incident-response`)

### 3. Relationships
- Always link related knowledge using `[[id]]` wikilinks
- At least 1 related link required

### 4. Avoid Duplication
- Search existing knowledge before creating
- If similarity > 0.85, suggest merge

### 5. Validation
- Required fields: `id`, `type`, `domain`, `tags`, `summary`
- `id` must be unique
- `tags` must not be empty
- `domain` must be valid category

## ⚙️ Steps

### Step 1: Normalize Input
- Sanitize title → slug
- Validate required fields
- Normalize tags (lowercase, hyphen-separated)

### Step 2: Generate Slug
```python
slug = title.lower().replace(' ', '-').replace('_', '-')
slug = re.sub(r'[^a-z0-9-]', '', slug)
```

### Step 3: Generate ID
```
id = {domain}.{type}.{slug}
```

### Step 4: Check for Duplicates
- Search existing knowledge with same ID
- If exists, append `-v2` or increment version

### Step 5: Select Template
| Type | Template |
|------|----------|
| concept | `templates/concept.md` |
| pattern | `templates/pattern.md` |
| runbook | `templates/runbook.md` |
| architecture | `templates/architecture.md` |

### Step 6: Generate Content
- Fill template with inputs
- Add required sections
- Include [[related]] links

### Step 7: Save File
- Create directory if not exists
- Write file with UTF-8 encoding

### Step 8: Update Index (CRITICAL)

**For patterns (cross-category):**
- Add entry to `examples/knowledge/patterns/INDEX.md`

**For topics in categories:**
- Add entry to **category INDEX.md** (e.g., `examples/knowledge/IaC/terraform/INDEX.md`)
- Add entry to **main INDEX.md** (`examples/knowledge/INDEX.md`)

**Folder Mapping:**
| Type | Path |
|------|------|
| pattern | `examples/knowledge/patterns/` |
| concept/runbook/architecture | `examples/knowledge/<category>/<topic>/` |

## 🔁 Post-actions

After creation:
1. **Validate**: Check frontmatter completeness
2. **Suggest links**: If no related provided, search for similar topics
3. **Check duplication**: If similarity > 0.7, flag for review
4. **Emit event**: `knowledge.created`

## ⚠️ Validation Checklist

Before completing, verify:
- [ ] `id` is unique
- [ ] `type` is valid enum value
- [ ] `domain` exists or will be created
- [ ] `tags` array has at least 1 item
- [ ] `summary` is 1-2 sentences
- [ ] At least 1 `[[related]]` link exists
- [ ] File saved in correct folder
- [ ] Category INDEX.md updated
- [ ] Main INDEX.md updated

## 📚 Templates

### Concept Template
Used for explanatory content, definitions, core ideas.

### Pattern Template
Used for solved problems with proven solutions.

### Runbook Template
Used for operational procedures, troubleshooting steps.

### Architecture Template
Used for system designs, component relationships.

## 🔗 Integration

This skill integrates with:
- **Obsidian**: Native graph view and backlinks
- **Qdrant**: Vector embeddings for semantic search
- **Neo4j**: Graph relationships for traversal
- **knowledge-validator**: Post-creation validation
- **knowledge-refactor**: Duplicate detection