---
title: Kubernetes
type: reference
category: DevOps
domain: kubernetes
created: 2026-08-03
updated: 2026-08-03
tags:
  - kubernetes
  - containers
  - orchestration
  - devops
status: active
id: kubernetes.reference.kubernetes
version: "1.0.0"
confidence: high
source: https://kubernetes.io/docs/concepts/architecture/
inputs: []
outputs: []
dependencies: []
quality_score: 0
aliases: [k8s]
summary: Kubernetes é o sistema de orquestração de containers de código aberto que automatiza deployment, scaling e operação de aplicações containerizadas — declarativo, self-healing e baseado em control plane + worker nodes.
---

# Kubernetes

## 🧠 Definition

Kubernetes (K8s) é uma plataforma de **orquestração de containers** que automatiza deployment, scaling e operação de workloads containerizados. O usuário declara o **estado desejado** (Pods, Deployments, Services...) e o control plane reconcilia continuamente o cluster com esse estado — self-healing, rollout/rollback automatizados e descoberta de serviço.

## 📚 Explanation

### Arquitetura: Control Plane + Worker Nodes

```
┌──────────────────── Control Plane ────────────────────┐
│ kube-apiserver    → front-end da API (escalável horizontalmente)│
│ etcd              → backing store (source of truth, backup plane)│
│ kube-scheduler    → escolhe node para cada novo Pod         │
│ kube-controller-manager → control loops (Deployment, ReplicaSet...)│
└──────────────────────────────────────────────────────────┘
┌───────────────────── Worker Node ──────────────────────┐
│ kubelet            → agente que garante containers rodando│
│ kube-proxy         → network rules (opcional se CNI provê) │
│ container runtime  → containerd / CRI-O (via CRI)        │
└──────────────────────────────────────────────────────────┘
```

- **kube-apiserver**: única porta de entrada (REST + kubectl), autentica/autoriza, escala horizontalmente.
- **etcd**: armazena o estado completo do cluster (chave-valor); exige plano de backup.
- **kube-scheduler**: filtra/aponta Pods sem node para o node mais adequado (resources, taints, affinity).
- **kube-controller-manager**: roda control loops; ex.: Deployment cria ReplicaSets quando o número de réplicas desejado não é satisfeito.

### Workloads

| Workload | Uso |
|----------|-----|
| Pod | unidade mínima — 1+ containers com storage/rede compartilhados |
| Deployment | apps stateless: réplicas, rollout, rollback, auto-healing |
| StatefulSet | apps stateful: identidade estável, storage persistente por réplica |
| DaemonSet | um Pod por node (monitoring, logs, CNI) |
| Job / CronJob | tarefas batch / agendadas |

### Serviços e Ingress

- **Service** (ClusterIP, NodePort, LoadBalancer): descoberta e balanceamento estáveis.
- **Ingress / Gateway API**: entrada HTTP(S) com TLS, routing por host/path.
- **DNS interno**: `my-svc.namespace.svc.cluster.local`.

### Storage

- **PersistentVolume (PV)** + **PersistentVolumeClaim (PVC)**: storage desacoplado do Pod.
- **StorageClass**: provisionamento dinâmico (EBS, GCE PD, NFS, CSI).

### Configuração

- **ConfigMap**: configuração não sensível.
- **Secret**: dados sensíveis (base64; idealmente cifrados + External Secrets/SOPS).
- **RBAC**: Role/ClusterRole + RoleBinding/ClusterRoleBinding.

## Connections

- [ArgoCD](argocd.md)
- [GitOps](../concepts/gitops.md)

## 🧩 Key Insights

- Declarativo: `kubectl apply -f manifest.yaml` → control plane converge o cluster.
- Control plane escala horizontalmente; etcd é o único estado central (backup é mandatório).
- kube-proxy é opcional se a CNI já provê service proxy.
- Controller loop é o coração: o sistema compara desired vs actual continuamente.

## ⚠️ Trade-offs

- Complexidade operacional alta (control plane, networking, upgrades).
- Curva de aprendizado íngreme (abstrações: Pod, Deployment, Service, Ingress).
- Overhead de recursos; para workloads pequenos pode ser excesso.

## 📊 Observability

- **SLIs**: pod readiness, rollout progress, node health, API latency
- **SLOs**: API availability 99.9%, deploy time < 5min
- **Metrics**: `kube_pod_status_ready`, `kube_deployment_status_replicas_available`, kube-state-metrics + Prometheus

## 🔐 Security Considerations

- RBAC mínimo privilégio; namespaces para isolamento.
- Secrets cifrados (KMS) + External Secrets Operator/SOPS.
- NetworkPolicies para microsegmentação; Pod Security Standards.
- Atualização regular do cluster e images scanning.

## 🏗️ Usage Context

- Quando usar: aplicações containerizadas em escala, microsserviços, GitOps, multi-tenant workloads.
- Quando NÃO usar: aplicação única simples (Docker basta), sem equipe para operar.
- Pré-requisitos: containers, YAML, entendimento de redes/volumes.

## 📚 References

- [Kubernetes Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
