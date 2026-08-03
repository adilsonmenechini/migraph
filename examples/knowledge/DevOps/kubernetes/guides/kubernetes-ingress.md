---
title: Kubernetes Ingress
type: guide
category: kubernetes
tags:
  - ingress
  - routing
  - http
  - load-balancing
aliases:
  - k8s ingress
  - ingress-controller
status: active
created: 2026-04-27
updated: 2026-04-27
id: kubernetes.ingress
version: "1.0.0"
confidence: high
source: docs
---

# Kubernetes Ingress

## Overview
Ingress is an API object that manages external HTTP/HTTPS access to services, providing URL routing, SSL termination, and load balancing.

## Purpose
Ingress exposes services to the outside world:
- Single entry point for multiple services
- Path-based or host-based routing
- SSL/TLS termination
- Custom load balancing

## Content

### Ingress Specification

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### TLS/SSL

```yaml
spec:
  tls:
  - hosts:
    - example.com
    secretName: tls-secret
```

### Commands

```bash
# List ingresses
kubectl get ingress

# Describe ingress
kubectl describe ingress my-ingress

# Apply ingress
kubectl apply -f ingress.yaml

# Delete ingress
kubectl delete ingress my-ingress
```

## Usage Examples

### Path-based Routing

```yaml
- path: /users
  pathType: Prefix
  backend:
    service:
      name: users-service
      port:
        number: 80
```

### Host-based Routing

```yaml
- host: api.example.com
  http:
    paths:
    - path: /
      backend:
        service:
          name: api-service
```

## Relationships
- [[kubernetes-services]]
- [[kubernetes-architecture]]

## Notes
> [!warning]
> You need an Ingress controller (nginx, traefik, etc.) installed

- Configure TLS for production
- Use `pathType: ImplementationSpecific` for nginx

## References
- [Ingress Documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
