---
title: Kubernetes Deployment Example
type: example
category: kubernetes
tags:
  - example
  - code
  - sample
  - deployment
aliases:
  - k8s-example
  - deployment-example
status: active
created: 2026-04-27
updated: 2026-04-27
id: kubernetes.deployment-example
version: "1.0.0"
confidence: high
source: docs
---

# Kubernetes Deployment Example

## Overview
Practical example demonstrating how to create a Kubernetes Deployment with Service, based on official documentation.

## Code

### Deployment + Service (YAML)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx-svc
  labels:
    app: nginx
spec:
  type: LoadBalancer
  ports:
  - port: 80
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

### Deploy with kubectl

```bash
# Create deployment and service
kubectl apply -f nginx-deployment.yaml

# Check status
kubectl get deployments
kubectl get pods
kubectl get services

# Scale deployment
kubectl scale deployment my-nginx --replicas=5

# Update image
kubectl set image deployment/my-nginx nginx=nginx:1.16.1

# View rollout history
kubectl rollout history deployment/my-nginx

# Rollback to previous
kubectl rollout undo deployment/my-nginx
```

## Explanation

- **Service (LoadBalancer)**: Exposes the deployment externally
- **Deployment**: Manages 3 replicas of nginx pod
- **selector**: Links Service to Deployment pods
- **containerPort**: Container port exposed

## Multiple Resources

Create multiple resources in one file using `---` separator.

## Related
- [[kubernetes-deployments]]
- [[kubernetes-services]]

## References
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Managing Workloads](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)