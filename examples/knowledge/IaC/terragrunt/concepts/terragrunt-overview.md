---
id: terragrunt.concept.overview
title: Terragrunt Overview
type: concept
domain: terragrunt
tags:
  - terragrunt
  - terraform
  - iac
  - infrastructure-as-code
  - open-tofu
summary: Terragrunt is a thin wrapper for OpenTofu/Terraform that provides extra tools for keeping configurations DRY, managing remote state, and working with multiple Terraform modules.
related:
  - [[terraform.architecture]]
  - [[terragrunt.commands]]
source: https://docs.terragrunt.com/getting-started/overview
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 90
---

# Terragrunt Overview

## Overview
Terragrunt is a thin wrapper for OpenTofu/Terraform that provides extra tools for keeping configurations DRY (Don't Repeat Yourself), managing remote state, and working with multiple Terraform modules. It aims to solve the scaling problems that teams encounter when managing infrastructure as code.

## Purpose
Terragrunt addresses common challenges in infrastructure as code at scale:
- Code duplication across multiple Terraform units
- Remote state management complexity
- Dependency ordering between modules
- Reproducibility and hermetic builds

## Content

### Key Features

1. **DRY Configurations**: Use `include` blocks to share configuration across units
2. **Remote State Management**: Automatic S3/DynamoDB setup for state storage
3. **Dependency Management**: Built-in dependency resolution with DAG
4. **Code Generation**: Generate provider.tf and backend.tf automatically
5. **Stack Operations**: Manage collections of interdependent units

### How It Works

Terragrunt reads `terragrunt.hcl` files and:
1. Downloads Terraform modules to `.terragrunt-cache/`
2. Generates configuration files (provider, backend)
3. Orchestrates Terraform commands with proper ordering

## Usage

### Basic terragrunt.hcl

```hcl
# Configure remote state
remote_state {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key = "env:/dev/terraform.tfstate"
    region = "us-east-1"
  }
}

# Generate provider
generate "provider" {
  path = "provider.tf"
  contents = <<EOF
provider "aws" {
  region = "us-east-1"
}
EOF
}

# Configure module
terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.16.0"
}

# Pass inputs
inputs = {
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

### DRY Pattern with Include

```hcl
# root.hcl - shared config
remote_state {
  backend = "s3"
  config = {
    bucket = "my-state"
    key = "${path_relative_to_include()}/terraform.tfstate"
    region = "us-east-1"
  }
}

# vpc/terragrunt.hcl - inherits root
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.16.0"
}

inputs = {
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

## Relationships
- [[terraform.architecture]] - Terraform architecture
- [[terragrunt.commands]] - Terragrunt CLI commands
- [[terragrunt.dry-configs]] - DRY configuration pattern

## Notes
- Terragrunt doesn't replace Terraform - it wraps it
- Each unit is a hermetic, reproducible container
- Use `run-all` commands for stack operations

## References
- [Terragrunt Documentation](https://docs.terragrunt.com/)
- [Terragrunt GitHub](https://github.com/gruntwork-io/terragrunt)