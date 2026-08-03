---
name: terraform
description: Terraform - Infrastructure as Code tool by HashiCorp for provisioning cloud and on-premises resources declaratively using collaborative IaC workflow. Covers concepts (architecture, terragrunt), guides (basics), and references (commands).
tags:
  - terraform
  - terragrunt
  - iac
  - infrastructure-as-code
  - devops
  - hashicorp
  - collaborative-iac
  - workspaces
  - hcp-terraform
  - open-tofu
aliases:
  - terraform-iac
  - tf
---

# Terraform

## Overview
This category covers Terraform - Infrastructure as Code tool by HashiCorp for provisioning cloud and on-premises resources declaratively using the **collaborative infrastructure as code** workflow.

## Recommended Practices

Based on [HashiCorp Recommended Practices](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices):

### Collaborative IaC Workflow

1. **One workspace per environment per configuration**
   - Pattern: `Terraform configurations × environments = workspaces`
   - Example: `billing-app-dev`, `billing-app-prod`

2. **Four Personas**:
   - Central IT: Define practices, enforce policy
   - Organization Architect: Define infrastructure division
   - Workspace Owner: Manage dev→prod lifecycle
   - Workspace Contributor: Submit changes to dev/staging

3. **Delegation Model**
   - Teams own specific workspaces
   - Use access control to regulate production changes
   - Enable parallel development

### Concepts
- [[terraform-architecture]] - Core architecture, providers, resources, workspaces, collaborative IaC
- [[terraform-basics]] - Getting started, collaborative workflow, workspace structure
- [[terragrunt-overview]] - Terragrunt overview (DRY configs, remote state, dependency management)

### References
- [[terraform-commands]] - Terraform CLI commands
- [[terragrunt-commands]] - Terragrunt CLI commands (run-all, stack, catalog)

### Examples
- [[terraform-ec2-example]] - EC2 instance with Security Group

---

*Last updated: 2026-04-28*