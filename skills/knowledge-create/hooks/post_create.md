# Post-Creation Hook

Run these actions after creating a new knowledge note.

## 1. Update Index Files

After creating a new note, update the relevant INDEX.md:

```bash
# Add entry to category INDEX.md
# Example for kubernetes.concepts:
- [[kubernetes.concepts.new-note]] - Description
```

## 2. Suggest Backlinks

Check for potential backlinks (notes that might reference this new note):

```bash
# Search for mentions of title or keywords
grep -r "title_keyword" knowledge/
```

## 3. Check for Duplication

Run similarity check:

```bash
python3 scripts/deduplicate.py knowledge/
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
  "event": "knowledge.created",
  "id": "{{note_id}}",
  "type": "{{type}}",
  "domain": "{{domain}}",
  "source": "knowledge-create"
}
```

## 6. Integration Notifications

Send to relevant systems:

- **Obsidian**: Automatic graph update
- **Qdrant**: Trigger embedding generation
- **Neo4j**: Create node with relationships
- **Slack**: Notify #knowledge channel (optional)

## Checklist

Before completing:
- [ ] INDEX.md updated
- [ ] Backlinks suggested
- [ ] No duplicates found (similarity < 0.85)
- [ ] Valid frontmatter verified
- [ ] Event emitted