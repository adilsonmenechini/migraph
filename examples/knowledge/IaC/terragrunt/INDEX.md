---
name: terragrunt
description: Terragrunt - thin wrapper for OpenTofu/Terraform that provides DRY configurations, remote state management, and stack operations. Each topic has concepts (overview), references (commands), and patterns (DRY configs).
tags:
  - terragrunt
  - terraform
  - iac
  - infrastructure-as-code
  - open-tofu
  - dry
  - stack
aliases:
  - tg
  - terragrunt-iac
---

# Terragrunt

## Overview
Terragrunt is a thin wrapper for OpenTofu/Terraform that provides extra tools for keeping configurations DRY, managing remote state, and working with multiple Terraform modules.

## Key Features

- **DRY Configurations**: Use `include` blocks to share configuration
- **Remote State Management**: Automatic S3/DynamoDB setup
- **Stack Operations**: `run-all` commands for multiple units
- **Dependency Management**: Built-in DAG resolution

## Concepts
- [[terragrunt-overview]] - What is Terragrunt, key features, usage

## Guides
- [[terragrunt-getting-started]] - Step-by-step setup guide

## References
- [[terragrunt-commands]] - CLI commands (run-all, stack, catalog)

## Examples
- [[terragrunt-vpc-example]] - VPC example with DRY config pattern

## Patterns
- [[terragrunt-dry-configs]] - DRY configuration pattern

---

*Last updated: 2026-04-28*