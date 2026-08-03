---
name: knowledge-base
description: Knowledge base with Obsidian-style notes organized by category (IaC, DevOps, AI). Each category contains topics with concepts, guides, references, and examples.
tags:
  - knowledge-base
  - documentation
  - obsidian
  - iac
  - devops
  - ai
  - patterns
aliases:
  - kb
  - knowledge
---

# Knowledge Base

## Overview
This is the main knowledge base index, organized by category.

## Categories

| Category | Topics |
|----------|-------|
| [[IaC]] | Terraform, Terragrunt, Ansible |
| [[DevOps]] | Kubernetes, ArgoCD |
| [[AI]] | Deep Agents, LangChain |
| [[Patterns]] | Cross-category patterns |

## Topics by Category

For detailed topics in each category, see the category INDEX.md:

- [[IaC/INDEX]] - Terraform, Terragrunt, Ansible
- [[DevOps/INDEX]] - Kubernetes, ArgoCD
- [[AI/INDEX]] - Deep Agents, LangChain
- [[patterns/INDEX]] - Cross-category patterns

## Adding New Topics

**For full category structure, use knowledge-manager:**
- "add IaC/ansible" → `examples/knowledge/IaC/ansible/`
- "add DevOps/kubernetes" → `examples/knowledge/DevOps/kubernetes/`
- "add AI/langchain" → `examples/knowledge/AI/langchain-ai/`

**For patterns (cross-category):**
- "create pattern for X" → `examples/knowledge/patterns/`

**Examples:**
- "add IaC/terragrunt" → creates new Terragrunt knowledge in IaC/
- "add DevOps/argocd" → creates new ArgoCD knowledge in DevOps/
- "create pattern for blue-green" → creates cross-category pattern

---

*Last updated: 2026-04-28*