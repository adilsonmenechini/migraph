---
name: argocd
description: ArgoCD - GitOps continuous delivery tool for Kubernetes. Declarative, automated deployment ensuring cluster state matches Git. Includes best practices from ArgoCD documentation.
tags:
  - argocd
  - gitops
  - continuous-delivery
  - kubernetes
  - devops
  - best-practices
aliases:
  - argocd-gitops
  - argo
---

# ArgoCD

## Overview
This category covers ArgoCD - GitOps continuous delivery tool for Kubernetes that automates deployment by ensuring live state matches desired state defined in Git.

## Best Practices (from ArgoCD Documentation)

Based on [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/):

### 1. Separate Config from Source Code
- Use a **separate Git repository** for Kubernetes manifests
- Clean separation: app code ≠ config code
- Cleaner audit log
- Multiple repos can deploy as single unit
- **Separation of access**: developers ≠ production push

### 2. Leave Room for Imperativeness
- Don't track everything in Git
- Allow HPA to manage replicas dynamically
- Example: Don't include `replicas` if using HorizontalPodAutoscaler

### 3. Ensure Manifests Are Truly Immutable
- Use **Git tags or commit SHA**, not HEAD
- Bad: `github.com/org/repo//manifests` (unstable)
- Good: `github.com/org/repo//manifests?ref=v1.0.0`

### 4. Use ApplicationSet
- For multi-cluster deployments
- Progressive sync for controlled rollouts

### Concepts
- [[argo-workflows-architecture]] - Core architecture, Application, Project, sync
- [[argocd-basics]] - Getting started, installation, first Application (with best practices)

### References
- [[argocd-commands]] - CLI commands, workflow, options

### Examples
- [[argocd-application-example]] - Application with auto-sync

---

*Last updated: 2026-04-28*