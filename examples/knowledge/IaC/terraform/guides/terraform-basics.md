---
id: terraform.basics
title: Terraform Basics
type: guide
category: terraform
tags:
  - getting-started
  - tutorial
  - basics
  - hcl
  - workspaces
  - collaborative-iac
aliases:
  - terraform-tutorial
  - tf-basics
status: active
version: "1.0.0"
created: 2026-04-27
updated: 2026-04-28
confidence: high
source: docs
---

# Terraform Basics

## Overview
A practical guide to getting started with Terraform - from installation to your first infrastructure deployment using collaborative Infrastructure as Code (IaC) practices.

## Purpose
Learn Terraform fundamentals:
- Installing Terraform
- Writing your first configuration
- Understanding HCL syntax
- Running basic commands
- **Collaborative IaC workflow** (recommended practices)

## Content

### Installation

```bash
# macOS
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Linux
wget -q https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify
terraform -version
```

### First Configuration

Create `main.tf`:

```hcl
# Configure provider
provider "aws" {
  region = "us-east-1"
}

# Create resource
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "terraform-example"
  }
}

# Output
output "instance_ip" {
  value       = aws_instance.example.public_ip
  description = "Public IP of the instance"
}
```

### HCL Syntax Basics

| Element | Example | Purpose |
|---------|---------|---------|
| Block | `resource "type" "name" {}` | Define infrastructure |
| Attribute | `ami = "..."` | Set value |
| Type | `string`, `number`, `bool`, `list`, `map` | Validate data |
| Expression | `var.name`, `aws_instance.example.id` | Reference values |

### Collaborative IaC Workflow (Recommended)

The recommended approach is **collaborative infrastructure as code**, using HCP Terraform to manage boundaries between teams, roles, and deployment tiers.

#### Four Personas

| Persona | Responsibility | Access |
|---------|---------------|--------|
| **Central IT** | Define practices, enforce policy, maintain shared services | All workspaces |
| **Organization Architect** | Define global infrastructure division and delegation | All workspaces |
| **Workspace Owner** | Owns workspaces, manages change lifecycle (dev→prod) | Production approval |
| **Workspace Contributor** | Submit changes, can modify dev/staging | Dev/UAT/Staging |

#### Workspace Structure

**One workspace per environment per configuration**:
```
billing-app-dev
billing-app-stage
billing-app-prod
networking-dev
networking-stage
networking-prod
```

**Pattern**: `Terraform configurations × environments = workspaces`

#### Delegation Model

- Teams can start runs and edit variables in dev/staging
- Owners approve production changes after review
- Central IT administers permissions on all workspaces
- No access = no visibility

### Variables and Outputs

**variables.tf**:
```hcl
variable "instance_type" {
  type        = string
  default     = "t2.micro"
  description = "EC2 instance type"
}

variable "tags" {
  type = map(string)
  default = {
    Environment = "dev"
    Project     = "terraform-example"
  }
}
```

**outputs.tf**:
```hcl
output "instance_id" {
  value = aws_instance.example.id
}

output "public_ip" {
  value = aws_instance.example.public_ip
}
```

## Usage

### Common Workflow

```bash
# 1. Initialize (first time or after adding providers)
terraform init

# 2. Format (optional but recommended)
terraform fmt

# 3. Validate
terraform validate

# 4. Plan (preview changes)
terraform plan -out=tfplan

# 5. Apply (execute plan)
terraform apply tfplan

# 6. Show state
terraform show

# 7. Destroy (clean up)
terraform destroy
```

### Using Variables

```bash
# With CLI variables
terraform apply -var="instance_type=t2.small"

# With variable file
terraform apply -var-file=prod.tfvars

# Auto-load variables
# terraform.tfvars or *.auto.tfvars
```

## Relationships
- [[terraform-architecture]]
- [[terraform-commands]]

## Notes
- Always run `terraform plan` before `apply`
- Use `-auto-approve` for CI/CD pipelines
- Keep state secure - never commit to version control
- **Follow collaborative IaC**: one workspace per environment per configuration
- Use HCP Terraform for team collaboration and access control
- Delegate ownership to enable parallel development

## References
- [Terraform Recommended Practices](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices)
- [Terraform Tutorial](https://learn.hashicorp.com/tutorials/terraform/infrastructure-as-code)
- [Terraform Language Documentation](https://www.terraform.io/docs/language/index.html)