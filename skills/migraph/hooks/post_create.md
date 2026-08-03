# Post-Creation Hook

Run these actions after creating a new wiki page.

## 1. Update Index Files

After creating a new page, update the relevant INDEX.md:

```bash
# Add entry to category INDEX.md
# Example for kubernetes.concepts:
- [[kubernetes.concepts.new-note]] - Description
```

## 2. Suggest Backlinks

Check for potential backlinks (pages that might reference this new page):

```bash
# Search for mentions of title or keywords
grep -r "title_keyword" wiki/
```

## 3. Check for Duplication

Run similarity check:

```bash
python3 skills/migraph/scripts/migraph deduplicate <wiki-root>
```

If similarity > 0.85:
- Flag for merge review
- Suggest to user

## 4. Validation Check

Verify the created file:

```bash
# Check required fields exist
python3 -c "
import json
import sys
import yaml

with open('{{file_path}}') as f:
    content = f.read()
    fm = yaml.safe_load(content.split('---')[1])

    required = ['id', 'type', 'domain', 'tags', 'summary']
    missing = [k for k in required if k not in fm]

    if missing:
        print(f'MISSING: {missing}')
        sys.exit(1)
    print('VALID')
"
```

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
- [ ] INDEX.md updated
- [ ] Backlinks suggested
- [ ] No duplicates found (similarity < 0.85)
- [ ] Valid frontmatter verified
- [ ] Event emitted
