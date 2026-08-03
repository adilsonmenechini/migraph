---
title: Terraform EC2 Example
type: example
category: terraform
tags:
  - example
  - code
  - sample
  - aws
  - ec2
aliases:
  - terraform-example
  - tf-ec2-example
status: active
created: 2026-04-27
updated: 2026-04-27
id: terraform.ec2-example
version: "1.0.0"
confidence: high
source: docs
---

# Terraform EC2 Example

## Overview
Practical example demonstrating how to create an AWS EC2 instance with Terraform, based on official documentation.

## Code

### Basic EC2 Instance

```hcl
# main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Look up latest Amazon Linux AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# Create EC2 instance
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  tags = {
    Name = "my-terraform-instance"
  }
}

# Output instance ID
output "instance_id" {
  value = aws_instance.web.id
}

# Output public IP
output "public_ip" {
  value = aws_instance.web.public_ip
}
```

### With Security Group

```hcl
# Create security group
resource "aws_security_group" "web_sg" {
  name        = "web-server-sg"
  description = "Allow SSH and HTTP"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Update instance with security group
resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags {
    Name = "web-server"
  }
}
```

## Commands

```bash
# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply

# Apply with auto-approve
terraform apply -auto-approve

# Destroy resources
terraform destroy
```

## Explanation

- **provider**: AWS configuration with region
- **data**: Lookup AMI dynamically
- **resource**: Create EC2 instance
- **output**: Expose instance ID and IP

## Related
- [[terraform-basics]]
- [[terraform-architecture]]

## References
- [Terraform AWS Instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)
- [Terraform Tutorials](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-build)