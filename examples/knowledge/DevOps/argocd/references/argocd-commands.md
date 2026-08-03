---
title: ArgoCD Commands
type: reference
category: argocd
tags:
  - commands
  - cli
  - cheatsheet
aliases:
  - argocd-cli
  - argocd-reference
status: active
created: 2026-04-27
updated: 2026-04-27
---

# ArgoCD Commands

## Overview
Quick reference for common ArgoCD CLI commands and their usage.

## Purpose
This is a command reference - use this when you need to:
- Remember a specific command
- Check available options
- Find the right flag

## Content

### Installation & Setup

| Command | Description |
|---------|-------------|
| `brew install argocd` | Install ArgoCD CLI |
| `argocd version` | Show version |
| `argocd login <server>` | Login to ArgoCD |
| `argocd context` | List contexts |

### Application Management

| Command | Description |
|---------|-------------|
| `argocd app create <name>` | Create application |
| `argocd app get <name>` | Get application details |
| `argocd app list` | List applications |
| `argocd app delete <name>` | Delete application |
| `argocd app sync <name>` | Sync application |
| `argocd app rollback <name> <revision>` | Rollback to revision |
| `argocd app diff <name>` | Show diff |
| `argocd app logs <name>` | Show logs |
| `argocd app resources <name>` | List child resources |

### Sync Options

| Command | Description |
|---------|-------------|
| `argocd app sync <name> --prune` | Sync with prune |
| `argocd app sync <name> --force` | Force sync |
| `argocd app sync <name> --strategy apply` | Apply strategy |
| `argocd app sync <name> --async` | Async sync |

### Application Set

| Command | Description |
|---------|-------------|
| `argocd appset create <file>` | Create AppSet |
| `argocd appset list` | List AppSets |
| `argocd appset get <name>` | Get AppSet details |
| `argocd appset delete <name>` | Delete AppSet |

### Project Management

| Command | Description |
|---------|-------------|
| `argocd proj create <name>` | Create project |
| `argocd proj list` | List projects |
| `argocd proj add-source <project> <repo>` | Add source repo |
| `argocd proj add-destination <project> <server> <ns>` | Add destination |
| `argocd proj delete <name>` | Delete project |

### Repository Management

| Command | Description |
|---------|-------------|
| `argocd repo add <url>` | Add repository |
| `argocd repo list` | List repositories |
| `argocd repo remove <url>` | Remove repository |
| `argocd repo add <url> --ssh-private-key-path <path>` | SSH key auth |

### Cluster Management

| Command | Description |
|---------|-------------|
| `argocd cluster add <context>` | Add cluster |
| `argocd cluster list` | List clusters |
| `argocd cluster get <name>` | Get cluster info |
| `argocd cluster remove <name>` | Remove cluster |

### Authentication

| Command | Description |
|---------|-------------|
| `argocd account get-user-info` | Get user info |
| `argocd account update-password` | Update password |
| `argocd role list` | List roles |
| `argocd role create <name>` | Create role |

## Usage Examples

### Full Workflow

```bash
# Login
argocd login argocd.example.com

# Create app
argocd app create my-app \
  --repo https://github.com/org/repo \
  --path deploy \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace prod

# Sync
argocd app sync my-app

# Check status
argocd app get my-app

# Rollback if needed
argocd app rollback my-app 1

# Delete
argocd app delete my-app
```

### AppSet Example

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-appset
spec:
  generators:
    - matrix:
        generators:
          - git:
              repoURL: https://github.com/org/repo
              directories:
                - path: apps/*
          - clusters:
              selector:
                matchLabels:
                  environment: production
  template:
    metadata:
      name: '{{path.basename}}-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/repo
        path: '{{path}}'
        targetRevision: HEAD
      destination:
        server: '{{server}}'
        namespace: default
```

### With Parameters

```bash
# Override parameters
argocd app set my-app --param image.tag=v2.0.0

# Override Helm values
argocd app set my-app --values prod-values.yaml

# Set resource limits
argocd app set my-app --helm-set-string replicaCount=3
```

## Relationships
- [[argo-workflows-architecture]]
- [[argocd-basics]]

## Notes
- Use `--help` flag for detailed options
- Many commands support `-o json` or `-o yaml` for output
- Cluster add requires valid kubeconfig context

## References
- [ArgoCD CLI Reference](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd/)
- [ArgoCD AppSet Tutorial](https://argo-cd.readthedocs.io/en/stable/user-guide/application-set/)