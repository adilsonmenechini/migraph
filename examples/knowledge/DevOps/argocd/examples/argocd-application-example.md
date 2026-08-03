---
title: ArgoCD Application Example
type: example
category: argocd
tags:
  - example
  - code
  - sample
  - application
  - gitops
aliases:
  - argocd-example
  - application-example
status: active
created: 2026-04-27
updated: 2026-04-27
---

# ArgoCD Application Example

## Overview
Practical example demonstrating how to create an ArgoCD Application with auto-sync, based on official documentation.

## Code

### Basic Application (YAML)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  
  destination:
    server: https://kubernetes.default.svc
    namespace: default
```

### With Auto-Sync

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-app
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/example/app.git
    targetRevision: main
    path: manifests
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  syncPolicy:
    automated:
      enabled: true
      prune: true      # Remove stale resources
      selfHeal: true   # Restore deleted resources
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Via CLI

```bash
# Create application
argocd app create guestbook \
  --repo https://github.com/argoproj/argocd-example-apps.git \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default

# Sync manually
argocd app sync guestbook

# Check status
argocd app get guestbook

# Enable auto-sync
argocd app set guestbook --sync-policy automated

# Delete application
argocd app delete guestbook
```

## Explanation

- **project**: Logical grouping (default)
- **source**: Git repository and path
- **destination**: Target cluster and namespace
- **syncPolicy.automated**: Auto-deploy on Git changes
- **prune**: Clean up deleted resources
- **selfHeal**: Restore drifted resources

## Related
- [[argocd-basics]]
- [[argo-workflows-architecture]]

## References
- [ArgoCD Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)
- [Declarative Setup](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)