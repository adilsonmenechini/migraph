---
title: GitOps
type: concept
category: DevOps
domain: gitops
created: 2026-08-03
updated: 2026-08-03
tags:
  - gitops
  - ci-cd
  - kubernetes
status: active
id: gitops.concept.gitops
version: "1.0.0"
confidence: high
source: https://www.gitops.tech/
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: []
summary: GitOps é um padrão operacional onde o Git é a fonte da verdade declarativa para infraestrutura e aplicações — o estado desejado é definido no repo, e um operador reconcilia o estado real continuamente.
---

# GitOps

## 🧠 Definition

GitOps é um padrão de operação onde o **Git é a fonte da verdade** (single source of truth) para infraestrutura e aplicações. O estado desejado é descrito declarativamente em manifests versionados, e um controlador (operador) reconcilia continuamente o cluster com esse estado — com pull-based deployment, rollback via Git, e auditoria completa.

## 📚 Explanation

### Princípios

1. **Declarative state**: todo o estado desejado é declarado em arquivos versionados no Git.
2. **Git é a fonte da verdade**: nenhuma mudança fora do Git.
3. **Automated reconciliation**: operador compara live vs desired, converge.
4. **Pull-based**: o operador puxa do Git (não CI push), reduzindo superfície de ataque.

### Padrões

- **Push vs Pull**: CI/CD clássico empurra artefatos; GitOps puxa via operador (Argo CD, Flux).
- **Rollback**: `git revert` + sync = rollback confiável e auditable.
- **Audit**: cada mudança tem commit, autor, diff — trilha completa.

## 🔗 Related

- [[ArgoCD]]
- [[Kubernetes]]
- [[Helm]]

## 🧩 Key Insights

- Argo CD e Flux são os operadores GitOps mais usados em Kubernetes.
- Kustomize/Helm/Jsonnet renderizam manifests a partir do repo.
- GitOps reduz drift e habilita self-healing (Argo CD `selfHeal: true`).

## ⚠️ Trade-offs

- Exige disciplina de processo (nada fora do Git).
- Operador GitOps adiciona complexidade operacional.
- Segredos e configuração sensível exigem gestão cuidadosa (SealedSecrets, SOPS, External Secrets).

## 📊 Observability

- **SLIs**: drift detection time, reconciliation success rate, sync latency
- **SLOs**: reconciliation < 1min, sync success > 99%
- **Metrics**: sync status, health, reconciliation frequency

## 🔐 Security Considerations

- Pull-based reduz exposição (sem credenciais de cluster no CI).
- RBAC no operador (AppProject no Argo CD).
- Secrets via External Secrets Operator, SOPS, Vault.

## 🏗️ Usage Context

- Quando usar: Kubernetes, infra-as-code, equipes que precisam de rollback confiável.
- Quando NÃO usar: infraestrutura imperativa, sem Git central, workloads efêmeros.

## 📚 References

- [GitOps.tech](https://www.gitops.tech/)
- [Argo CD Docs](https://argo-cd.readthedocs.io/)
- [Flux CD](https://fluxcd.io/)
