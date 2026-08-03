---
title: Terraform Commands
type: reference
category: terraform
tags:
  - commands
  - cli
  - cheatsheet
aliases:
  - terraform-cli
  - tf-commands
status: active
created: 2026-04-27
updated: 2026-04-27
id: terraform.commands
version: "1.0.0"
confidence: high
source: docs
---

# Terraform Commands

## Overview
Quick reference for common Terraform CLI commands and their usage.

## Purpose
This is a command reference - use this when you need to:
- Remember a specific command
- Check available options
- Find the right flag

## Content

### Initialization

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize working directory |
| `terraform init -upgrade` | Upgrade providers |
| `terraform init -backend=false` | Skip backend initialization |
| `terraform init -get-plugins=false` | Skip plugin download |

### Planning and Applying

| Command | Description |
|---------|-------------|
| `terraform plan` | Generate execution plan |
| `terraform plan -out=file` | Save plan to file |
| `terraform plan -var 'key=value'` | Set variable |
| `terraform plan -destroy` | Plan destruction |
| `terraform apply` | Apply changes |
| `terraform apply file` | Apply saved plan |
| `terraform apply -auto-approve` | Skip confirmation |
| `terraform apply -var 'key=value'` | Set variable |

### Destroying

| Command | Description |
|---------|-------------|
| `terraform destroy` | Destroy all resources |
| `terraform destroy -auto-approve` | Skip confirmation |
| `terraform plan -destroy` | Preview destruction |

### Inspection

| Command | Description |
|---------|-------------|
| `terraform show` | Show current state |
| `terraform show plan` | Show plan file |
| `terraform state list` | List resources |
| `terraform state show resource` | Show resource details |
| `terraform output` | Show outputs |
| `terraform output name` | Show specific output |
| `terraform graph` | Show dependency graph |

### Formatting and Validation

| Command | Description |
|---------|-------------|
| `terraform fmt` | Format code |
| `terraform fmt -recursive` | Recursive formatting |
| `terraform validate` | Validate syntax |
| `terraform validate -json` | JSON output |

### Modules

| Command | Description |
|---------|-------------|
| `terraform get` | Download modules |
| `terraform init -get-modules=false` | Skip module download |

### Workspaces

| Command | Description |
|---------|-------------|
| `terraform workspace new name` | Create workspace |
| `terraform workspace select name` | Switch workspace |
| `terraform workspace list` | List workspaces |
| `terraform workspace show` | Current workspace |
| `terraform workspace delete name` | Delete workspace |

### Debugging

| Command | Description |
|---------|-------------|
| `TF_LOG=ERROR terraform apply` | Error logs |
| `TF_LOG=DEBUG terraform apply` | Debug logs |
| `TF_LOG_CORE=TRACE terraform apply` | Core logs |

## Usage Examples

### Full Workflow
```bash
# Setup
terraform init
terraform fmt
terraform validate

# Plan and apply
terraform plan -out=tfplan
terraform apply tfplan

# View outputs
terraform output

# Clean up
terraform destroy
```

### With Variables
```bash
# Single variable
terraform apply -var="instance_count=3"

# Variable file
terraform apply -var-file=prod.tfvars

# Multiple files
terraform apply -var-file=prod.tfvars -var-file=secrets.tfvars
```

### State Management
```bash
# Pull remote state
terraform state pull

# Push state
terraform state push

# Move resource
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state
terraform state rm aws_instance.example
```

## Relationships
- [[terraform-architecture]]
- [[terraform-basics]]

## Notes
- Use `terraform plan` before every `apply`
- Lock file (.lock.hcl) should be version controlled
- Use `-auto-approve` only in CI/CD

## References
- [Terraform CLI Documentation](https://www.terraform.io/docs/cli/index.html)
- [Terraform Commands](https://www.terraform.io/docs/cli/commands/index.html)