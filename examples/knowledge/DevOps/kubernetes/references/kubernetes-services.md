---
title: Kubernetes Services
type: reference
category: kubernetes
tags:
  - networking
  - services
  - load-balancing
  - service-types
aliases:
  - k8s service
  - service-reference
status: active
created: 2026-04-27
updated: 2026-04-27
id: kubernetes.services
version: "1.0.0"
confidence: high
source: docs
---

# Kubernetes Services

## Overview
A Service is an abstraction layer that defines a logical set of Pods and a policy for accessing them. Services provide stable IP addresses and DNS names, enabling loose coupling between dependent Pods.

## Purpose
Services solve the problem of pod volatility:
- Pods are ephemeral and can be recreated with new IPs
- Multiple pod replicas need to share traffic
- Applications need a stable endpoint for communication

## Content

### Service Types

| Type | Description | Use Case |
|------|-------------|----------|
| `ClusterIP` | Internal cluster IP (default) | Internal communication |
| `NodePort` | Exposes via node port | Development/testing |
| `LoadBalancer` | External load balancer | Production cloud deployments |
| `ExternalName` | Maps to external DNS | External service discovery |

### ClusterIP Service Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-backend-service
spec:
  type: ClusterIP
  selector:
    app: my-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### NodePort Service Example

```yaml
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080
```

## Usage

### Service Operations

```bash
# Create service
kubectl apply -f service.yaml

# List services
kubectl get services

# Describe service
kubectl describe service my-service

# Delete service
kubectl delete service my-service

# Port forwarding for local testing
kubectl port-forward service/my-service 8080:80

# Check endpoints
kubectl get endpoints my-service
```

### DNS Resolution
Services are discoverable within the cluster via DNS:
```
my-service.namespace.svc.cluster.local
```

Short forms:
- `my-service` → same namespace
- `my-service.namespace` → different namespace
- `my-service.namespace.svc` → fully qualified

## Relationships
- [[kubernetes-architecture]]
- [[kubernetes-deployments]]
- [[kubernetes-ingress]]

## Notes
- Services use label selectors to route traffic to matching pods
- Use `kubectl get endpoints` to verify service backends
- Headless services (ClusterIP: None) return pod IPs directly

## References
- [Services Documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Service Types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)