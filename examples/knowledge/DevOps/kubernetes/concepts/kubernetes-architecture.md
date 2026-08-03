---
title: Kubernetes Architecture
type: concept
category: kubernetes
tags:
  - architecture
  - orchestration
  - containers
  - control-plane
aliases:
  - k8s architecture
  - kubernetes-components
status: active
created: 2026-04-27
updated: 2026-04-27
id: kubernetes.architecture
version: "1.0.0"
confidence: high
source: docs
---

# Kubernetes Architecture

## Overview
Kubernetes (k8s) is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications. It groups containers into logical units for easy discovery and management.

## Purpose
Kubernetes was designed to eliminate manual processes for deploying and scaling containerized applications. It provides a declarative API for describing application infrastructure and automated tools for maintaining desired state.

## Content

### Core Components

#### Control Plane
- **kube-apiserver**: Exposes the Kubernetes API, the front-end for all control plane operations
- **etcd**: Consistent, distributed key-value store for all cluster data
- **kube-scheduler**: Assigns Pods to nodes based on resource availability
- **kube-controller-manager**: Runs controller processes that regulate cluster state
- **cloud-controller-manager**: Integrates with cloud provider APIs

#### Worker Nodes
- **kubelet**: Agent that ensures containers are running in Pods
- **kube-proxy**: Network proxy that maintains network rules on nodes
- **container runtime**: Software responsible for running containers (containerd, CRI-O)

### Key Concepts
- **Pod**: Smallest deployable unit, wraps one or more containers
- **Service**: Stable network endpoint for accessing Pods
- **Deployment**: Manages ReplicaSets for declarative updates
- **Namespace**: Virtual cluster partition for resource isolation

## Usage

### Basic Commands
```bash
# Get cluster info
kubectl cluster-info

# List all pods
kubectl get pods -A

# Apply a deployment
kubectl apply -f deployment.yaml

# Scale deployment
kubectl scale deployment my-app --replicas=3
```

## Relationships
- [[kubernetes-pods]]
- [[kubernetes-deployments]]
- [[kubernetes-services]]

## Notes
- Control plane components typically run on dedicated nodes
- Worker nodes can be physical servers or VMs
- etcd is critical - always backup regularly

## References
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Architecture](https://kubernetes.io/docs/concepts/overview/)
