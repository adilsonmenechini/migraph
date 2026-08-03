---
id: terraform.architecture
title: Terraform Architecture
type: concept
category: terraform
tags:
  - iac
  - infrastructure-as-code
  - provisioning
  - hashicorp
  - collaborative-iac
  - workspaces
aliases:
  - terraform-iac
  - tf-architecture
status: active
version: "1.0.0"
created: 2026-04-27
updated: 2026-04-28
confidence: high
source: docs
---

# Terraform Architecture

## Overview
Terraform is an Infrastructure as Code (IaC) tool by HashiCorp that defines cloud and on-prem resources in declarative configuration files. The recommended approach is **collaborative infrastructure as code** using HCP Terraform.

## Purpose
Terraform enables:
- Version-controlled infrastructure
- Reproducible environments
- Multi-cloud provisioning (AWS, Azure, GCP, etc.)
- Collaboration via shared state
- Drift detection
- **Team collaboration** via workspaces and access control

## Content

### Core Components

#### Providers
Plugins that interact with cloud APIs:
```hcl
provider "aws" {
  region = "us-east-1"
}
```

#### Resources
Infrastructure objects to manage:
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  tags = {
    Name = "web-server"
  }
}
```

### Recommended Workflow: Collaborative IaC

The recommended workflow addresses two fundamental challenges:

1. **Technical Complexity**
   - Different providers use different interfaces
   - Terraform separates provisioning workload using provider plugins
   - Uses workflow-level abstraction, not resource-level

2. **Organizational Complexity**
   - Infrastructure scales with more teams
   - Delegate ownership across teams
   - Empower parallel development without conflict

#### Workspace Model

**Formula**: `Terraform configurations × environments = workspaces`

| Component | Dev | Stage | Prod |
|-----------|-----|-------|------|
| billing-app | billing-app-dev | billing-app-stage | billing-app-prod |
| networking | networking-dev | networking-stage | networking-prod |

#### Delegation via Workspaces

- **Central IT**: Define practices, enforce policy, maintain shared services
- **Organization Architect**: Define global infrastructure division
- **Workspace Owner**: Owns workspace, manages dev→prod lifecycle
- **Workspace Contributor**: Submit changes, can modify dev/staging

### State Management

- **Local state**: Single machine, not collaborative
- **Remote state**: HCP Terraform, shared across teams
- **Remote state storage**: S3, GCS, Azure Blob, etc.

### Provider Ecosystem

| Provider | Type |
|----------|------|
| aws | IaaS |
| google | IaaS |
| azurerm | IaaS |
| heroku | PaaS |
| github | SaaS |

## Relationships
- [[terraform-basics]]
- [[terraform-commands]]

## Notes
- Use **one workspace per environment per configuration**
- Separate configurations by team ownership
- Use output variables to publish APIs between workspaces
- Use remote state to access data from other workspaces
- HCP Terraform enforces access control across all workspaces

## References
- [Terraform Recommended Practices](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices)
- [Workspace Documentation](https://developer.hashicorp.com/terraform/cloud-docs/workspaces)
- [Part 1: Overview](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices/part1) {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}
```

#### Data Sources
Read-only information from providers:
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners     = ["099720109477"]
}
```

#### Variables
Parameterize configurations:
```hcl
variable "instance_type" {
  type        = string
  default    = "t2.micro"
  description = "EC2 instance type"
}
```

#### Outputs
Expose resource information:
```hcl
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

### State Management

| State Type | Description |
|------------|-------------|
| Local | File on disk (default) |
| Remote | Shared (S3, etc.) |
| Locking | Prevents concurrent changes |

### Workflow

```
1. Write configuration (.tf)
2. terraform init     # Initialize providers
3. terraform plan   # Preview changes
4. terraform apply # Execute changes
5. terraform destroy # Clean up
```

## Usage

```bash
# Initialize
terraform init

# Plan changes
terraform plan -out=tfplan

# Apply plan
terraform apply tfplan

# Destroy resources
terraform destroy

# Format code
terraform fmt

# Validate
terraform validate
```

## Relationships
- [[terraform-basics]]
- [[terraform-commands]]

## Notes
- State file contains sensitive data - use remote state with encryption
- Providers must be initialized with `terraform init`
- Use workspaces for multi-environment management

## References
- [Terraform Documentation](https://www.terraform.io/docs/)
- [Terraform Registry](https://registry.terraform.io/)