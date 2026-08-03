---
id: terragrunt.example.vpc
title: Terragrunt VPC Example
type: example
domain: terragrunt
tags:
  - terragrunt
  - terraform
  - vpc
  - example
  - aws
summary: Practical example showing how to use Terragrunt to deploy a VPC with DRY configuration pattern.
related:
  - [[terragrunt-overview]]
  - [[terragrunt-commands]]
  - [[terragrunt-dry-configs]]
source: https://docs.terragrunt.com/getting-started/overview
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 90
---

# Terragrunt VPC Example

## Overview
Practical example demonstrating how to use Terragrunt to deploy a VPC using the DRY configuration pattern with include blocks.

## Project Structure

```
.
├── root.hcl
└── vpc/
    └── terragrunt.hcl
```

## Code

### root.hcl (Shared Configuration)

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
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Generate provider for all units
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents = <<EOF
provider "aws" {
  region = "us-east-1"
}
EOF
}
```

### vpc/terragrunt.hcl (VPC Unit)

```hcl
# Inherit shared config from root.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

# Use VPC module from Terraform Registry
terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.16.0"
}

# VPC configuration
inputs = {
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Environment = "dev"
    ManagedBy   = "terragrunt"
  }
}
```

## Explanation

1. **root.hcl** defines shared configuration:
   - S3 backend for state storage
   - DynamoDB table for locking
   - AWS provider configuration

2. **vpc/terragrunt.hcl** inherits from root:
   - Uses `include` block to pull in shared config
   - Specifies VPC module source
   - Passes only VPC-specific inputs

## How to Run

```bash
# Initialize and create VPC
cd vpc
terragrunt apply

# Or from root (runs all units)
terragrunt run-all apply
```

## Related

- [[terragrunt-overview]] - Terragrunt overview
- [[terragrunt-commands]] - CLI commands
- [[terragrunt-dry-configs]] - DRY pattern explanation