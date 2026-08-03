---
title: Argo Events
type: reference
category: DevOps
domain: event-driven
created: 2026-08-03
updated: 2026-08-03
tags:
  - argo
  - events
  - event-driven
  - kubernetes
  - serverless
status: active
id: event-driven.reference.argo-events
version: "1.0.0"
confidence: high
source: https://argoproj.github.io/argo-events/
summary: Argo Events é o framework event-driven do ecossistema Argo para Kubernetes — EventSource, EventBus e Sensor conectam 20+ fontes de eventos a triggers como Argo Workflows, objetos K8s e funções serverless via CloudEvents.
---

# Argo Events

## 🧠 Definition

Argo Events é um framework de automação de workflows orientado a eventos para Kubernetes — dispara Argo Workflows, objetos K8s, funções serverless e outros destinos a partir de mais de 20 fontes de eventos diferentes.

## 📚 Explanation

O Argo Events é composto por três componentes principais que formam o pipeline de eventos:

- **EventSource**: conecta-se a fontes de eventos externas (GitHub, GitLab, Kafka, AWS SNS/SQS, GCP PubSub, NATS, MQTT, Redis, Slack, Stripe, Webhooks, calendário, entre outras) e converte cada evento em um CloudEvent padronizado.
- **EventBus**: transporta os eventos entre EventSources e Sensors usando NATS Streaming (padrão) ou Kafka.
- **Sensor**: escuta eventos do EventBus, aplica filtros e dependências (and/or), e dispara **triggers** — o componente que executa a ação desejada.

Os triggers suportados incluem: Argo Workflows, objetos Kubernetes, HTTP/serverless (OpenFaaS, Kubeless, KNative), AWS Lambda, NATS, Kafka, Slack, Azure Event Hubs, Argo Rollouts e OpenWhisk.

O fluxo pode ser de uma dependência linear simples (um evento → uma ação) até dependências complexas multi-fonte com lógica de constraints personalizada via expressões.

## 🧩 Key Insights

- **Padrão CloudEvents**: todos os eventos são normalizados para CloudEvents, garantindo interoperabilidade entre fontes e destinos.
- **Componentes declarativos**: EventSource, EventBus e Sensor são CRDs Kubernetes configurados via YAML — GitOps-friendly.
- **Dependências e filtros**: o Sensor suporta agregação de múltiplos eventos (and/or) com filtros por payload, headers e contexto.
- **Reuso do ecossistema Argo**: integra nativamente com Argo Workflows e Argo Rollouts, complementando o ArgoCD no ciclo GitOps.

## ⚠️ Trade-offs

| Aspecto | Prós | Contras |
|---------|------|---------|
| Escopo | Framework completo de event-driven | Curva de aprendizado dos 3 CRDs |
| Transporte | NATS/Kafka embutidos | Operação extra de message broker |
| Integração | 20+ fontes prontas | Fontes customizadas exigem desenvolvimento |
| Complexidade | De simples a multi-fonte | Dependências complexas exigem teste cuidadoso |

## 📊 Observability

- Métricas Prometheus expostas pelos controllers (EventSource, EventBus, Sensor).
- Logs estruturados dos três componentes.
- Dashboard padrão de health/ready dos pods.

## 🔐 Security Considerations

- Secrets das fontes (webhook tokens, credenciais Kafka/SQS) devem ser armazenados como Kubernetes Secrets.
- Webhooks expostos precisam de autenticação e validação de assinatura (ex.: HMAC do GitHub).
- RBAC mínimo para os controllers e para as ações executadas pelos triggers.

## 🏗️ Usage Context

- **CI/CD reativo**: disparar pipelines de deploy quando uma imagem for publicada ou um PR for merged.
- **GitOps**: reagir a eventos do repositório Git em conjunto com ArgoCD.
- **Integração de dados**: sincronizar dados de fontes externas (S3, Kafka, DB) para dentro do cluster.
- **Automação de plataforma**: ações em Slack, e-mail ou serverless baseadas em eventos de infraestrutura.

## 📚 References

- [Argo Events Documentation](https://argoproj.github.io/argo-events/)
- [Argo Events Architecture](https://argoproj.github.io/argo-events/concepts/architecture/)
- [Argo Events Event Sources](https://argoproj.github.io/argo-events/concepts/event_source/)

## Connections

- [Argocd](../references/argocd.md)
- [Gitops](../concepts/gitops.md)
- [Kubernetes](../references/kubernetes.md)
