# Quality Rules

## Structure Quality

### Frontmatter Requirements
Every note MUST have:
- `type`: guide | concept | reference
- `category`: folder name (from topic)
- `tags`: array of relevant keywords
- `status`: active | deprecated
- `created`: YYYY-MM-DD

### Section Requirements
All 7 sections required:
- Overview (required)
- Purpose (required)
- Content (required)
- Usage (required)
- Relationships (required - at least one link)
- Notes (required)
- References (required)

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