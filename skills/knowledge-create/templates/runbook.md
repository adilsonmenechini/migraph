# {{title}}

## 🚨 Context

{{summary}}

## 🔍 Detection

### Metrics

- metric_name: description
- metric_name: description

### Alerts

- Alert name: description
- Alert name: description

### Logs

- Log pattern to search
- Log pattern to search

## 🛠️ Steps

### 1. Initial Assessment

1. Check current state:
   ```bash
   command_to_check
   ```
2. Identify impact scope
3. Gather relevant logs

### 2. Containment

1. First containment step
   ```bash
   command
   ```
2. Second containment step

### 3. Resolution

1. Apply fix
2. Verify resolution

### 4. Post-Incident

1. Document findings
2. Update runbook if needed

## 🔁 Recovery

Steps to restore full service:

1. Recovery step 1
2. Recovery step 2

## 📊 Validation

How to verify the issue is resolved:

- Check metric: value should be X
- Run test: command should succeed
- Verify service: endpoint returns 200

## 🔗 Related

{{#each related}}
- [[{{this}}]]
{{/each}}

## 📚 References

- [Source]({{source}})
- [Incident Post-Mortem Template]()