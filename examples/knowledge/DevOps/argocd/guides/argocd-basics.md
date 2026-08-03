---
id: argocd.basics
title: ArgoCD Basics
type: guide
category: argocd
tags:
  - gitops
  - tutorial
  - getting-started
  - kubernetes
  - best-practices
aliases:
  - argocd-tutorial
  - argocd-getting-started
status: active
version: "1.0.0"
created: 2026-04-27
updated: 2026-04-28
confidence: high
source: docs
---

# ArgoCD Basics

## Overview
A practical guide to getting started with ArgoCD - from installation to your first GitOps deployment.

## Purpose
Learn ArgoCD fundamentals:
- Installing ArgoCD
- Creating your first Application
- Understanding sync policies
- Managing deployments

## Best Practices (from ArgoCD Documentation)

Based on [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/):

### 1. Separate Config from Source Code
- Use a **separate Git repository** for Kubernetes manifests
- Clean separation: app code ≠ config code
- Cleaner audit log for changes
- Multiple repos can deploy as single unit
- **Separation of access**: Developers ≠ Production push access

### 2. Leave Room for Imperativeness
- Don't track everything in Git (e.g., HPA-controlled replicas)
- Allow automation to manage dynamic values
- Example: Don't include `replicas` if using HorizontalPodAutoscaler

### 3. Ensure Manifests At Git Revisions Are Truly Immutable
- Use **Git tags or commit SHA**, not HEAD
- Bad: `github.com/org/repo//manifests`
- Good: `github.com/org/repo//manifests?ref=v1.0.0`

### 4. Alternative: App of Apps Pattern
- Use ApplicationSet for multi-cluster deployments
- Progressive sync for controlled rollouts

## Content

### Installation

```bash
# Namespace installation
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/install.yaml

# Or install with Helm
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace
```

### Access the UI

```bash
# Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Creating Your First Application

**Option 1: Using CLI**

```bash
# Login
argocd login localhost:8080

# Create application
argocd app create my-app \
  --repo https://github.com/org/repo \
  --path deploy \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production
```

**Option 2: Using YAML**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: HEAD
    path: deploy
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```bash
kubectl apply -f my-app.yaml
```

### Sync Policies

| Policy | Behavior |
|--------|----------|
| Manual | User triggers sync manually |
| Automated | Auto-sync on Git changes |

```yaml
syncPolicy:
  automated:
    prune: true      # Remove stale resources
    selfHeal: true   # Restore deleted resources
  syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
```

### Managing Applications

```bash
# Sync manually
argocd app sync my-app

# View status
argocd app get my-app

# Rollback
argocd app rollback my-app 1

# Delete
argocd app delete my-app
```

## Usage Examples

### With Helm

```yaml
source:
  repoURL: https://charts.helm.sh/stable
  chart: mysql
  targetRevision: 9.9.2
  helm:
    valueFiles:
      - values-prod.yaml
    parameters:
      - name: persistence.enabled
        value: "true"
```

### With Kustomize

```yaml
source:
  repoURL: https://github.com/org/repo
  path: overlays/production
  kustomize:
    images:
      - my-app:v2.0.0
```

### With Multiple Sources

```yaml
source:
  - repoURL: https://github.com/org/manifests
    path: base
  - repoURL: https://github.com/org/configs
    path: prod
    ref: values
```

## Relationships
- [[argo-workflows-architecture]]
- [[argocd-commands]]

## Notes
- Start with Manual sync to understand behavior
- Use "prune" to clean up deleted resources
- Set up health checks for custom resources
- Use projects to isolate teams

## References
- [ArgoCD Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)
- [ArgoCD User Guide](https://argo-cd.readthedocs.io/en/stable/user-guide/)