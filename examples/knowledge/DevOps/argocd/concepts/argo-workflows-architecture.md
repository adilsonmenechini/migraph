---
title: ArgoCD Architecture
type: concept
category: argocd
tags:
  - gitops
  - continuous-delivery
  - kubernetes
  - argo
aliases:
  - argocd-concept
  - argo-cd-architecture
status: active
created: 2026-04-27
updated: 2026-04-27
---

# ArgoCD Architecture

## Overview
ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. It automates the deployment of applications to target environments by ensuring the live state matches the desired state defined in Git.

## Purpose
ArgoCD provides:
- GitOps-based deployment
- Automatic application synchronization
- Multi-tenancy support
- Visual UI for deployment status
- Rollback capabilities

## Content

### Core Concepts

#### Application
A custom resource defining what to deploy:
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

#### Project
Logical grouping of applications with access controls:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: my-project
  namespace: argocd
spec:
  description: Project description
  sourceRepos:
    - https://github.com/org/*
  destinations:
    - namespace: production
      server: https://kubernetes.default.svc
  roles:
    - name: admin
      groups: [team-a]
```

#### Sync and Health
| Term | Description |
|------|-------------|
| Sync | Process of deploying application to match Git state |
| Health | Status of deployed application (Healthy, Degraded, Missing) |
| Drift | Difference between live state and Git state |

### Components

| Component | Description |
|-----------|-------------|
| API Server | REST API, UI, CLI interface |
| Repository Server | Handles Git operations |
| Application Controller | Watches Applications, syncs state |
| Redis | Cache for session data |

### Architecture Flow

```
Git Repository
      ↓
Repository Server (parse YAML)
      ↓
Application Controller (reconcile)
      ↓
Kubernetes API (apply resources)
      ↓
Cluster State → UI/CLI
```

## Usage

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/install.yaml

# Access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Login (admin / <password from secret>)
argocd login localhost:8080
```

## Relationships
- [[argocd-basics]]
- [[argocd-commands]]

## Notes
- ArgoCD uses "push" model - watches Git and applies to cluster
- Two sync modes: Manual and Automated
- Health checks verify deployed resources are healthy
- Works with any Kubernetes manifests (YAML, Helm, Kustomize)

## References
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ArgoCD GitHub](https://github.com/argoproj/argo-cd)