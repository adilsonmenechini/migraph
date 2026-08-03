---
title: ArgoCD
type: reference
category: DevOps
domain: gitops
created: 2026-08-03
updated: 2026-08-03
tags:
  - gitops
  - kubernetes
  - argocd
  - cd
status: active
id: gitops.reference.argocd
version: "1.0.0"
confidence: high
source: https://argo-cd.readthedocs.io/
summary: ArgoCD é o controlador GitOps declarativo para Kubernetes — o Git é a fonte da verdade e o cluster converge para o estado desejado.
---

# ArgoCD

## 🧠 Definition

Argo CD é um controlador Kubernetes declarativo que segue o padrão **GitOps**: o repositório Git é a fonte da verdade do estado desejado, e o Argo CD monitora continuamente as aplicações, comparando o estado atual (live) com o desejado (target). Desvios são reportados como `OutOfSync` e podem ser sincronizados automática ou manualmente.

## 📚 Explanation

### Modelo GitOps

- **Git como fonte da verdade**: manifests (Kustomize, Helm, Jsonnet, plain YAML) vivem no repo.
- **Controller loop**: o Argo CD reconcilia continuamente — se o live state diverge do target, marca `OutOfSync`.
- **Rollback**: qualquer configuração commitada no Git pode ser restaurada (roll-anywhere).

### Recursos principais

| Recurso | Função |
|---------|--------|
| `Application` | Declara source (repo + path + revision), destination (cluster + namespace) e syncPolicy |
| `AppProject` | Multi-tenancy e RBAC: restringe repos, clusters, namespaces e recursos |
| `ApplicationSet` | Gera Applications programaticamente via generators (list, cluster, git) |

### ApplicationSet generators

- **List generator**: elementos estáticos com `{{param}}` → múltiplas Applications.
- **Cluster generator**: usa os clusters definidos no Argo CD para gerar Applications.
- **Git generator**: usa arquivos/diretórios do próprio repo para template (via `directories` ou `files` com JSON).

### Sync Phases e Waves

Ordenação de aplicação dos recursos:

1. **Phase**: `PreSync` → `Sync` → `PostSync` (hooks: PreSync, Sync, Skip, PostSync, SyncFail, PreDelete, PostDelete).
2. **Wave**: anotação `argocd.argoproj.io/sync-wave` (inteiro, default 0, pode ser negativo).
3. **Kind**: namespaces primeiro, depois outros recursos.
4. **Name**.

Atraso entre waves: 2s por default (`ARGOCD_SYNC_WAVE_DELAY`).

### Sync options comuns

- `CreateNamespace=true` — cria namespace automaticamente
- `PruneLast=true` — pruning como wave final implícita
- `ApplyOutOfSyncOnly=true` — aplica só o que está out-of-sync
- `Replace=true` — usa `kubectl replace/create`
- `Validate=false` — desabilita validação (equivalente a `kubectl apply --validate=false`)

### syncPolicy.automated

```yaml
syncPolicy:
  automated:
    prune: true      # remove recursos que não existem mais no Git
    selfHeal: true   # corrige drift no cluster mesmo sem mudança no Git
    allowEmpty: false
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

### Progressive Syncs (beta v3.3+)

ApplicationSet com `strategy.type: RollingSync` — agrupa Applications por labels (`matchExpressions`), sincroniza grupo por grupo, esperando `Healthy` antes de avançar. `maxUpdate` controla % simultâneo; `deletionOrder: Reverse` para teardown ordenado.

## 🔗 Related

- [[Kubernetes]]
- [[GitOps]]
- [[Helm]]

## 🧩 Key Insights

- Argo CD é implementado como um controller Kubernetes que roda em loop de reconciliação.
- Suporte nativo a multi-cluster, SSO (OIDC, OAuth2, LDAP, SAML, GitHub, GitLab, Microsoft), RBAC multi-tenant.
- Hooks PreSync/Sync/PostSync permitem blue/green e canary.
- Métricas Prometheus + audit trail de eventos/API.

## ⚠️ Trade-offs

- Complexidade operacional do próprio Argo CD (RBAC, SSO, multi-cluster).
- Git como fonte da verdade exige disciplina de processo.
- Progressive Syncs ainda beta.

## 📊 Observability

- **SLIs**: sync status, health status, reconciliation frequency
- **SLOs**: target 99.9%
- **Metrics**: `argocd_app_info`, `argocd_app_sync_status`, Prometheus metrics built-in

## 🔐 Security Considerations

- RBAC via AppProject (repos, clusters, namespaces restritos).
- SSO com OIDC/OAuth2/LDAP/SAML.
- Access tokens para automação/CI.
- Credenciais de repo/cluster gerenciadas via secrets.

## 🏗️ Usage Context

- Quando usar: deploy GitOps em Kubernetes, multi-cluster, rollback confiável, compliance.
- Quando NÃO usar: workloads fora de Kubernetes, sem repo Git central.
- Pré-requisitos: cluster Kubernetes, repo Git com manifests.

## 📚 References

- [Argo CD Docs](https://argo-cd.readthedocs.io/)
- [Sync Phases and Waves](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)
- [ApplicationSet](https://argo-cd.readthedocs.io/en/stable/user-guide/application-set/)
- [Progressive Syncs](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Progressive-Syncs/)
- [Application Specification](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/)
