---
title: Kubernetes ConfigMaps and Secrets
type: reference
category: kubernetes
tags:
  - config
  - secrets
  - environment
  - configuration
aliases:
  - configmaps
  - k8s-secrets
status: active
created: 2026-04-27
updated: 2026-04-27
id: kubernetes.configmaps-secrets
version: "1.0.0"
confidence: high
source: docs
---

# Kubernetes ConfigMaps and Secrets

## Overview
ConfigMaps store non-sensitive configuration data, while Secrets store sensitive data (passwords, API keys, tokens) in an encoded format. Both inject configuration into containers at runtime.

## Purpose
Separate configuration from application code:
- Change config without rebuilding images
- Use different configs for different environments
- Store application settings centrally
- Manage sensitive data securely (Secrets)

## Content

### ConfigMap Example

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Simple key-value
  database_url: "postgres://db:5432/app"
  
  # Files as keys
  config.json: |
    {
      "logLevel": "info",
      "timeout": 30
    }
```

### Secret Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  # Plain text (auto-encoded)
  username: admin
  password: secretpassword
```

### Alternative: External Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-key
type: Opaque
data:
  # Base64 encoded
  key: cGxlYXNlQWRkU2VjcmV0S2V5Rm9yQXBp
```

## Usage

### Inject as Environment Variables

```yaml
env:
- name: DB_URL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: database_url
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: password
```

### Mount as Files

```yaml
volumeMounts:
- name: config
  mountPath: /etc/config
  readOnly: true
volumes:
- name: config
  configMap:
    name: app-config
```

### Commands

```bash
# Create ConfigMap from literal
kubectl create configmap app-config \
  --from-literal=database_url=postgres://db:5432

# Create ConfigMap from file
kubectl create configmap app-config \
  --from-file=config.json

# Create Secret from literal
kubectl create secret generic app-secrets \
  --from-literal=username=admin \
  --from-literal=password=secret

# List ConfigMaps
kubectl get configmaps

# Describe ConfigMap
kubectl describe configmap app-config
```

## Comparison

| Feature | ConfigMap | Secret |
|---------|----------|--------|
| Encoding | Plain text | Base64 |
| Use case | Non-sensitive config | Sensitive data |
| Encryption at rest | No | Optional (with encryption) |
| Size limit | 1MB | 1MB |

## Relationships
- [[kubernetes-pods]]
- [[kubernetes-deployments]]
- [[kubernetes-helm]]

## Notes
- Secrets are base64 encoded, not encrypted by default
- Use external secrets operators for production secrets
- Kubernetes secrets are in etcd (consider encryption at rest)

## References
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)