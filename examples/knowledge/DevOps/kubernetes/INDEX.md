---
name: kubernetes
description: Kubernetes (k8s) - Container orchestration platform for automating deployment, scaling, and management of containerized applications. Includes best practices from Kubernetes blog.
tags:
  - kubernetes
  - containers
  - orchestration
  - devops
  - cloud-native
  - best-practices
aliases:
  - k8s
  - kubernetes-k8s
---

# Kubernetes

## Overview
This category covers Kubernetes (k8s) concepts, guides, and references for container orchestration. Kubernetes is an open-source platform for automating deployment, scaling, and management of containerized applications.

## Best Practices (from Kubernetes Blog)

Based on [Kubernetes Configuration Good Practices](https://kubernetes.io/blog/2025/11/25/configuration-good-practices/):

### General Practices
- Use latest stable API version (`apps/v1`)
- Store configuration in version control
- Write configs in YAML, not JSON
- Keep configuration simple and minimal
- Add helpful annotations

### Workload Practices
- Use **Deployments** for apps that should always run
- Use **Jobs** for tasks that should finish
- Always configure health checks (liveness + readiness)
- Set resource requests and limits

### Service & Networking
- Create Services before workloads
- Use DNS for Service discovery
- Avoid `hostPort` and `hostNetwork`
- Use headless Services for internal discovery

### Labels
- Use semantic labels (`app`, `version`, `environment`)
- Use common Kubernetes labels
- Use labels for debugging

### Concepts
- [[kubernetes-architecture]] - Core components and architecture (Control Plane, Nodes)
- [[kubernetes-pods]] - Pods - smallest deployable unit, wraps containers

### Guides
- [[kubernetes-deployments]] - Deployments with best practices (health checks, PDBs, rolling updates)
- [[kubernetes-ingress]] - HTTP/HTTPS routing, URL rewriting, TLS termination
- [[kubernetes-helm]] - Helm package manager, charts, version control

### References
- [[kubernetes-services]] - Service types (ClusterIP, NodePort, LoadBalancer)
- [[kubernetes-configmaps-secrets]] - ConfigMaps and Secrets for configuration management

### Examples
- [[kubernetes-deployment-example]] - Deployment + Service example

---

*Last updated: 2026-04-28*