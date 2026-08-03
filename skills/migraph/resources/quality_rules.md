# Quality Rules

## Structure Quality

### Frontmatter Requirements
Every page MUST have:
- `type`: one of the 13 page types (source, topic, concept, decision, query, synthesis, entity, pattern, runbook, architecture, guide, reference, example)
- `category`: folder name (from topic)
- `domain`: knowledge domain/category
- `tags`: array of relevant keywords (min 1)
- `status`: draft | active | deprecated | archived
- `summary`: 1-2 sentence summary
- `created` / `updated`: YYYY-MM-DD
- `id`: `{domain}.{type}.{slug}` (e.g., `sre.runbook.incident-response`)

### Section Requirements
Sections vary by page type — use the matching template in `templates/pages/`:

- `concept`: Definition, Explanation, Key Insights, Trade-offs, Usage Context
- `guide`: How-to steps with prerequisites
- `reference`: Quick reference tables
- `example`: Code samples with explanation
- `pattern`: Problem, Solution, Architecture, Implementation, Trade-offs
- `runbook`: Context, Detection, Steps, Recovery, Validation
- `architecture`: Overview, Components, Data Flow, Observability
- `decision`: Context, Options, Decision, Consequences
- `source` / `topic` / `query` / `synthesis` / `entity`: follow the corresponding template

Every page MUST have at least one `## 🔗 Related` link (or equivalent Connections section).

## Content Quality

### Writing Standards
- Use clear, direct language
- Prefer active voice
- Include practical examples
- Avoid filler words and redundancy

### Completeness Checklist
- [ ] Topic is fully explained
- [ ] Purpose is clearly stated
- [ ] Usage instructions are actionable
- [ ] Examples are realistic and working
- [ ] Related notes are linked

## Connectivity Quality

### Link Requirements
- At least one [[link]] to related notes
- Links should be functional (note exists)
- Cross-reference related topics

## Scoring Weights

| Category | Weight | Description |
|----------|--------|-------------|
| Structure | 35 | Frontmatter, sections, formatting |
| Content | 30 | Clarity, completeness, examples |
| Completeness | 20 | All sections filled, no placeholders |
| Connectivity | 15 | Links, tags, cross-references |
