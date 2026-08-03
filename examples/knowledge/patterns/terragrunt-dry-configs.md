---
id: terragrunt.pattern.dry-configs
title: Terragrunt DRY Configurations
type: pattern
domain: terragrunt
tags:
  - terragrunt
  - terraform
  - dry
  - patterns
  - include
summary: Use include blocks and shared configurations to avoid code duplication across Terraform units.
related:
  - [[terragrunt-overview]]
  - [[terragrunt-commands]]
  - [[terragrunt-vpc-example]]
source: https://docs.terragrunt.com/getting-started/overview
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 90
---

# Terragrunt DRY Configurations

## Problem
Managing multiple Terraform units leads to code duplication. Each unit needs the same provider configuration, backend settings, and common variables. Manually maintaining these across many units is error-prone and hard to maintain.

## Solution
Use Terragrunt's `include` block to create a configuration hierarchy where shared settings are defined once in a root file and inherited by child units.

## Pattern

### Root Configuration (root.hcl)

```hcl
# Configure remote state
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "my-terraform-state"
    key             = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt         = true
    dynamodb_table  = "terraform-locks"
  }
}

# Generate provider configuration for all units
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = var.aws_region
}
EOF
}
```

### Child Configuration (vpc/terragrunt.hcl)

```hcl
# Inherit from root
include "root" {
  path = find_in_parent_folders("root.hcl")
}

# Module-specific configuration only
terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.16.0"
}

inputs = {
  name            = "my-vpc"
  cidr            = "10.0.0.0/16"
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.10.0/24", "10.0.20.0/24"]

  tags = {
    Environment = "dev"
    ManagedBy   = "terragrunt"
  }
}
```

## Architecture

### Configuration Hierarchy

```
.
├── root.hcl                    # Shared config (backend, provider)
├── vpc/
│   └── terragrunt.hcl         # Inherits root + VPC inputs
├── ec2/
│   └── terragrunt.hcl         # Inherits root + EC2 inputs
└── rds/
    └── terragrunt.hcl         # Inherits root + RDS inputs
```

### Generated Files

```
.terragrunt-cache/
└── vpc/
    ├── backend.tf      # Generated from remote_state
    ├── provider.tf    # Generated from generate block
    └── main.tf        # Downloaded module
```

## Key Patterns

### 1. Dynamic State Keys
Use `path_relative_to_include()` to avoid state key collisions:

```hcl
config = {
  key = "${path_relative_to_include()}/terraform.tfstate"
}
```

Result:
- `vpc/terragrunt.hcl` → state key: `vpc/terraform.tfstate`
- `ec2/terragrunt.hcl` → state key: `ec2/terraform.tfstate`

### 2. Multiple Include Types

```hcl
# Include root config
include "root" {
  path = find_in_parent_folders("root.hcl")
}

# Include region-specific config
include "region" {
  path = find_in_parent_folders("region.hcl")
  merge  = true  # Merge instead of overwrite
}
```

### 3. Dependency with Mock Outputs

```hcl
dependency "vpc" {
  config_path = "../vpc"

  mock_outputs = {
    vpc_id = "mock-vpc-id"
    private_subnets = ["mock-subnet"]
  }

  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}
```

## Trade-offs

| Aspect | Benefit | Risk |
|--------|---------|------|
| DRY configs | Single source of truth | Hidden complexity |
| Auto-generation | Less boilerplate | Magic behavior |
| Include inheritance | Easy updates | Debugging harder |
| Cache directory | Reproducibility | Disk usage |

## Related
- [[terragrunt-overview]] - Terragrunt overview
- [[terragrunt-commands]] - Terragrunt CLI commands
- [[terragrunt-vpc-example]] - VPC example

## References
- [Terragrunt Include Block](https://docs.terragrunt.com/features/units/includes/)
- [Terragrunt Remote State](https://docs.terragrunt.com/features/units/state-backend/)