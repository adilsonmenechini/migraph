---
title: Kubernetes Helm
type: guide
category: kubernetes
tags:
  - helm
  - packaging
  - charts
  - package-manager
aliases:
  - helm-charts
  - helm-guide
status: active
created: 2026-04-27
updated: 2026-04-27
id: kubernetes.helm
version: "1.0.0"
confidence: high
source: docs
---

# Kubernetes Helm

## Overview
Helm is the Kubernetes package manager - a tool for defining, installing, and upgrading complex Kubernetes applications using charts (packages).

## Purpose
Helm simplifies Kubernetes deployments:
- Package as charts (reusable templates)
- Version control for deployments
- Easy rollback to previous versions
- Share applications as charts

## Content

### Helm Concepts

| Term | Description |
|------|-------------|
| Chart | Package definition (like npm package) |
| Release | Deployed chart instance |
| Repository | Chart storage (like npm registry) |
| Values | Configuration overrides |

### Chart Structure

```
my-chart/
├── Chart.yaml          # Chart metadata
├── values.yaml        # Default values
├── charts/          # Dependencies
├── templates/       # Kubernetes manifests
└── README.md       # Documentation
```

### Chart.yaml Example

```yaml
apiVersion: v2
name: my-app
description: My application
type: application
version: 1.0.0
appVersion: "1.0.0"
```

### values.yaml Example

```yaml
replicaCount: 3

image:
  repository: my-app
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 500m
    memory: 128Mi
  requests:
    cpu: 200m
    memory: 64Mi
```

## Usage

### Basic Commands

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update repos
helm repo update

# Search charts
helm search repo nginx

# Install chart
helm install my-release bitnami/nginx

# Install with custom values
helm install my-release bitnami/nginx \
  --set service.type=LoadBalancer

# Upgrade release
helm upgrade my-release bitnami/nginx

# Rollback
helm rollback my-release 1

# List releases
helm list

# Uninstall release
helm uninstall my-release
```

### Template and Debug

```bash
# Render templates locally
helm template my-release bitnami/nginx

# Dry run
helm install my-release bitnami/nginx --dry-run

# Debug with values
helm install my-release bitnami/nginx --debug --dry-run
```

### Create Custom Chart

```bash
# Create chart structure
helm create my-app

# Package chart
helm package my-app

# Validate chart
helm lint my-app
```

### Common Use Cases

| Task | Command |
|------|---------|
| Install DB | `helm install mysql bitnami/mysql` |
| Install monitoring | `helm install prometheus prometheus-community/kube-prometheus-stack` |
| Upgrade app | `helm upgrade my-app ./my-chart` |
| Test upgrade | `helm upgrade my-app ./my-chart --dry-run` |

## Relationships
- [[kubernetes-deployments]]
- [[kubernetes-configmaps-secrets]]

## Notes
- Use Helm 3 (no Tiller needed)
- Store charts in OCI registries
- Use values files for environment differences

## References
- [Helm Documentation](https://helm.sh/docs/)
- [Helm Hub](https://hub.helm.sh/)