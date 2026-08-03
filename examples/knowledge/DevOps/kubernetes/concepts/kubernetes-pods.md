---
title: Kubernetes Pods
type: concept
category: kubernetes
tags:
  - pods
  - containers
  - workload
  - basic-unit
aliases:
  - k8s pods
  - pod-concept
status: active
created: 2026-04-27
updated: 2026-04-27
id: kubernetes.pods
version: "1.0.0"
confidence: high
source: docs
---

# Kubernetes Pods

## Overview
A Pod is the smallest deployable unit in Kubernetes. It wraps one or more containers that share storage and networking, representing a single application instance.

## Purpose
Pods serve as the basic building block for deploying applications:
- Containers in a Pod share the same network namespace (localhost communication)
- Can share volumes for persistent data
- Atomic unit of scheduling and replication
- Easier than managing containers individually

## Content

### Pod Characteristics
- **Shared network**: All containers in a Pod share the same IP address
- **Shared storage**: Can mount shared volumes
- **Atomic**: Created and deleted together
- **Single IP**: One IP per Pod (even with multiple containers)

### Pod States
| State | Description |
|-------|-------------|
| Pending | Pod is being scheduled |
| Running | At least one container is running |
| Succeeded | All containers terminated successfully |
| Failed | At least one container failed |
| Unknown | Pod status cannot be determined |

### Pod Specification

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
spec:
  containers:
  - name: web
    image: nginx:1.21
    ports:
    - containerPort: 80
  - name: sidecar
    image: logsender:latest
```

## Usage

### Basic Pod Commands

```bash
# Create pod
kubectl apply -f pod.yaml

# List pods
kubectl get pods

# Describe pod
kubectl describe pod my-pod

# View pod logs
kubectl logs my-pod

# Execute command in pod
kubectl exec -it my-pod -- /bin/bash

# Delete pod
kubectl delete pod my-pod
```

### Multi-Container Patterns

1. **Sidecar**: Helper container (logging, syncing)
2. **Adapter**: Transform output for external systems
3. **Ambassador**: Proxy for backend services

## Relationships
- [[kubernetes-architecture]]
- [[kubernetes-deployments]]

## Notes
> [!warning]
> Pods are ephemeral — use Deployments for production

- Multi-container Pods should be rare
- Use init containers for setup tasks

## References
- [Pods Documentation](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Pod Patterns](https://kubernetes.io/docs/concepts/workloads/pods/#pod-use-case)
