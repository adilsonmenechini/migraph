---
title: Datadog
type: reference
category: SRE
domain: observability
created: 2026-08-03
updated: 2026-08-03
tags:
  - observability
  - monitoring
  - apm
  - tracing
  - kubernetes
  - sre
status: active
id: observability.reference.datadog
version: "1.0.0"
confidence: high
source: https://docs.datadoghq.com/tracing/
summary: Datadog é a plataforma SaaS de observabilidade com APM e distributed tracing end-to-end — Single Step Instrumentation, Trace Explorer, Service Pages e correlação de traces com logs, métricas, DBM e RUM para produção em Kubernetes.
---

# Datadog

## 🧠 Definition

Datadog é a plataforma de observabilidade e monitoramento SaaS para infraestrutura, aplicações e logs — com APM e distributed tracing de ponta a ponta (browser → backend → banco de dados), métricas de infraestrutura e correlação automática entre traces, logs, métricas e perfis.

## 📚 Explanation

O Datadog APM (Application Performance Monitoring) entrega distributed tracing com foco em produção:

- **Single Step Instrumentation**: o Agent coleta automaticamente traces das principais linguagens e frameworks (Java, Python, Go, .NET, Node.js, Ruby, PHP, C++) sem exigir mudanças significativas no código — instalação do Agent + instrumentação em um único passo.
- **Trace Explorer**: consulta e visualização de traces ponta a ponta com filtros por serviço, recurso, erro, latência e tags — permitindo debugar uma requisição inteira do browser até o banco de dados.
- **Service Pages**: visão consolidada por serviço — health, deployments, latência, throughput, erro e recursos dependentes — com fallback automático para deep dive.
- **Ingestion Controls**: políticas de amostragem (sampling) por serviço/recurso para controlar custo e volume de spans.
- **Retention Filters**: os spans são retidos por 15 dias após a ingestão, permitindo análise posterior de erros e rastreios lentos.
- **Correlação**: integração com DBM (Database Monitoring), RUM (Real User Monitoring), logs, synthetics e profiles — um trace pode abrir o log da exceção, a query SQL lenta ou o profile do processo.

A plataforma cobre também métricas de infraestrutura (hosts, containers, Kubernetes, clouds), logs, dashboards e alertas — com API e Terraform para tudo como código.

## 🧩 Key Insights

- **Observabilidade unificada**: traces, logs, métricas e profiles correlacionados no mesmo contexto de requisição.
- **Single Step Instrumentation**: onboarding de APM em minutos, com auto-detecção de bibliotecas e frameworks.
- **Controle de custo por amostragem**: Ingestion Controls + Retention Filters separam ingestão de retenção.
- **Tudo como código**: dashboards, monitors e configuração via Terraform — GitOps-friendly.

## ⚠️ Trade-offs

| Aspecto | Prós | Contras |
|---------|------|---------|
| Profundidade | Traces end-to-end + correlação | Custo cresce com volume (spans/logs) |
| Setup | Single Step Instrumentation | Dependência do Agent em cada host |
| Escala | SaaS gerenciado, zero manutenção | Dados saem do cluster (compliance) |
| Governança | RBAC, tag-based policies | Configuração rica exige cuidado |

## 📊 Observability

- Service/resource pages com latência, throughput e erro.
- Trace Explorer com query de spans e flame graphs.
- Correlação com DBM, RUM, logs, synthetics e profiles.
- Dashboards e alerts via UI ou Terraform.

## 🔐 Security Considerations

- Dados de traces/logs podem conter PII — usar tag-based filtering e controles de ingestão.
- Agentes requerem acesso ao Agent socket e rede para o backend — restringir por namespace/network policy.
- API keys (app keys) com RBAC mínimo para leitura/escrita.

## 🏗️ Usage Context

- **SRE/Plataforma**: monitorar serviços Kubernetes com dashboards e alertas por SLO.
- **APM**: diagnóstico de latência ponta a ponta (frontend → serviço → DB).
- **Incident response**: correlacionar trace do erro com log, perfil e métrica de infra.
- **FinOps de observabilidade**: sampling e retention filters para controlar custo.

## 📚 References

- [Datadog Tracing Documentation](https://docs.datadoghq.com/tracing/)
- [Datadog Trace Explorer](https://docs.datadoghq.com/tracing/trace_explorer/)

## Connections

- [Kubernetes](../references/kubernetes.md)
- [Domain-Driven-Design](../concepts/domain-driven-design.md)
- [Model-Platform](../topics/model-platform.md)
