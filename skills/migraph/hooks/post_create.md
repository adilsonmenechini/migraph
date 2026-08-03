# Post-Creation Hook

Run these actions after creating a new wiki page.

## 1. Create Through the Canonical Path

New pages MUST be created through `migraph create`, which generates the
frontmatter and validates the page **before** it lands in the wiki:

```bash
python3 skills/migraph/scripts/migraph create --root <wiki-root> \
  --title "Page Title" --type <type> --domain <domain> \
  --summary "1-2 sentence summary" --tags "tag1,tag2" \
  --source "https://..." \
  --connections "../references/other-page.md,../concepts/other-concept.md"
```

Blocking validation performed by `create_page.py`:

- Frontmatter against `validators/schema.json` (id, type, domain, tags, summary)
- Required fields (title, type, created, updated, source, tags, confidence, status)
- Required sections for the page type
- At least one `## Connections` markdown link resolving to an existing wiki page
- No placeholder text / weak summary
- No duplicate title or duplicate id

On failure the file is NOT written and the command exits non-zero. On success
the graph, viewer, inbox and graph report are rebuilt automatically.

## 2. Update Index Files

After creating a new page, update the relevant INDEX.md:

```bash
# Add entry to category INDEX.md
# Example for kubernetes.concepts:
- [[kubernetes.concepts.new-note]] - Description
```

## 3. Suggest Backlinks

Check for potential backlinks (pages that might reference this new page):

```bash
# Search for mentions of title or keywords
grep -r "title_keyword" wiki/
```

## 4. Check for Duplication

Run similarity check:

```bash
python3 skills/migraph/scripts/migraph deduplicate <wiki-root>
```

If similarity > 0.85:
- Flag for merge review
- Suggest to user

## 5. Emit Event

For automation systems:

```json
{
  "event": "migraph.note.created",
  "id": "{{note_id}}",
  "type": "{{type}}",
  "domain": "{{domain}}",
  "source": "migraph"
}
```

## 6. Integration Notifications

Send to relevant systems:

- **Obsidian**: Automatic graph update
- **MiGraph outputs**: Trigger `graph` / `viewer` / `graph-report` rebuild

## Checklist

Before completing:
- [ ] Page created via `migraph create` (validation passed)
- [ ] INDEX.md updated
- [ ] Backlinks suggested
- [ ] No duplicates found (similarity < 0.85)
- [ ] Event emitted
