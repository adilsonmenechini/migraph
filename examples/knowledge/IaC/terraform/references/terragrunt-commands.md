---
id: terragrunt.commands
title: Terragrunt Commands
type: reference
domain: terragrunt
tags:
  - terragrunt
  - commands
  - cli
  - cheatsheet
summary: Quick reference for common Terragrunt CLI commands for managing infrastructure stacks.
related:
  - [[terragrunt.concept.overview]]
  - [[terraform.commands]]
source: https://docs.terragrunt.com/reference/cli/
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 85
---

# Terragrunt Commands

## Overview
Quick reference for Terragrunt CLI commands. Most commands work as drop-in replacement for `tofu`/`terraform`.

## Usage Pattern

Replace `tofu` or `terraform` with `terragrunt`:

```bash
# Instead of:
tofu plan
terraform apply

# Use:
terragrunt plan
terragrunt apply
```

Terragrunt automatically handles:
- Auto-init when needed
- Dependency ordering
- State management

---

## Main Commands

| Command | Description |
|---------|-------------|
| `terragrunt run-all plan` | Plan all units in stack |
| `terragrunt run-all apply` | Apply all units in stack |
| `terragrunt run-all destroy` | Destroy all units |
| `terragrunt run-all run --terragrunt-print-struct` | Show execution order (DAG) |
| `terragrunt exec -- <command>` | Execute arbitrary command |
| `terragrunt run <command>` | Run tofu/terraform command |

---

## Stack Commands

| Command | Description |
|---------|-------------|
| `terragrunt stack generate` | Generate stack from terragrunt.stack.hcl |
| `terragrunt stack run` | Run command against stack |
| `terragrunt stack output` | Get outputs from stack |
| `terragrunt stack clean` | Remove .terragrunt-stack directories |

---

## Backend Commands

| Command | Description |
|---------|-------------|
| `terragrunt backend bootstrap` | Bootstrap S3/DynamoDB backend |
| `terragrunt backend migrate` | Migrate state between units |
| `terragrunt backend delete` | Delete backend state |

---

## Discovery Commands

| Command | Description |
|---------|-------------|
| `terragrunt find` | Find relevant configurations |
| `terragrunt list` | List all configurations |
| `terragruntgraph dag` | Graph DAG in DOT format |

---

## Configuration Commands

| Command | Description |
|---------|-------------|
| `terragrunt hcl fmt` | Format HCL files |
| `terragrunt hcl validate` | Validate HCL files |
| `terragrunt info print` | Print Terragrunt context |
| `terragrunt render` | Render merged config |

---

## Catalog Commands

| Command | Description |
|---------|-------------|
| `terragrunt catalog` | Launch catalog TUI |
| `terragrunt scaffold` | Generate config from catalog |

---

## Common Examples

### Plan Stack with Dependencies

```bash
terragrunt run-all plan
```

### Apply in Order (DAG)

```bash
terragrunt run-all apply
```

### Destroy All

```bash
terragrunt run-all destroy
```

### Show Execution Order

```bash
terragrunt run-all run --terragrunt-print-struct
```

---

## Related

- [[terragrunt.concept.overview]] - Terragrunt overview
- [[terraform.commands]] - Terraform commands

---

## References

- [Terragrunt CLI Reference](https://docs.terragrunt.com/reference/cli/)