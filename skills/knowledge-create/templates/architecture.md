# {{title}}

## 🧭 Overview

{{summary}}

## 🏗️ Components

### Core Components

| Component | Responsibility | Tech |
|-----------|---------------|------|
| Component 1 | Description | Technology |
| Component 2 | Description | Technology |

### Supporting Components

| Component | Purpose |
|-----------|---------|
| Component A | Supporting role |
| Component B | Supporting role |

## 🔄 Data Flow

```
User Request
    ↓
[Load Balancer]
    ↓
[API Gateway]
    ↓
[Service Layer]
    ↓
[Data Layer]
    ↓
Response
```

### Flow Description

1. Request arrives at load balancer
2. Gateway routes to appropriate service
3. Service processes business logic
4. Data layer retrieves/stores information
5. Response flows back through the chain

## 📊 Observability

### Traces

- Trace name: Jaeger/Datadog link
- Span: major operations

### Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| request_rate | Requests per second | > 1000 |
| latency_p99 | 99th percentile latency | < 200ms |
| error_rate | Percentage of 5xx | < 0.1% |

### Logs

- Key log patterns to monitor
- Log aggregation: ELK/Datadog

## 🔐 Security

- Authentication: OAuth2/JWT
- Authorization: RBAC
- Encryption: TLS 1.3, Encryption at rest
- Network: VPC, Security Groups

## ⚠️ Trade-offs

| Decision | Trade-off | Mitigation |
|----------|-----------|------------|
| Trade-off 1 | Impact | Mitigation approach |
| Trade-off 2 | Impact | Mitigation approach |

## 🚀 Scaling Strategy

- Horizontal scaling for stateless services
- Vertical scaling for databases
- Auto-scaling based on metrics

## 🔗 Related

{{#each related}}
- [[{{this}}]]
{{/each}}

## 📚 References

- [Source]({{source}})
- [Architecture Decision Records]()