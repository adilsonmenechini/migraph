---
id: terragrunt.guide.getting-started
title: Terragrunt Getting Started
type: guide
domain: terragrunt
tags:
  - terragrunt
  - terraform
  - guide
  - getting-started
  - tutorial
summary: Step-by-step guide to set up Terragrunt with a basic project structure and DRY configuration.
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

# Terragrunt Getting Started

## Prerequisites

- OpenTofu or Terraform installed
- Terragrunt installed
- AWS credentials configured

## Installation

```bash
# macOS
brew install terragrunt

# Linux/macOS
curl -Ls https://terragrunt.sh | bash

# Verify
terragrunt --version
```

## Step 1: Create Project Structure

```bash
mkdir -p my-infra/vpc
cd my-infra
```

## Step 2: Create root.hcl

Create `root.hcl` in the root directory:

```hcl
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

## Step 3: Create VPC Unit

Create `vpc/terragrunt.hcl`:

```hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.16.0"
}

inputs = {
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
}
```

## Step 4: Run Terragrunt

```bash
cd vpc
terragrunt init
terragrunt plan
terragrunt apply
```

## Next Steps

- Add more units (ec2, rds, etc.)
- Use [[terragrunt-dry-configs]] pattern for advanced setups
- Explore [[terragrunt-commands]] for stack operations

## Related

- [[terragrunt-overview]] - Terragrunt overview
- [[terragrunt-commands]] - CLI commands
- [[terragrunt-dry-configs]] - DRY pattern