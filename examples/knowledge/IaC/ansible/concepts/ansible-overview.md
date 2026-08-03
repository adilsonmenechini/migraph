---
id: ansible.concept.overview
title: Ansible Overview
type: concept
domain: ansible
tags:
  - ansible
  - iac
  - automation
  - configuration-management
  - devops
summary: Ansible is an agentless IT automation tool that uses declarative YAML playbooks for configuration management, application deployment, and task orchestration.
related:
  - [[ansible.concept.directory-layout]]
source: https://docs.ansible.com/projects/ansible/2.9/user_guide/playbooks_best_practices.html
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 85
---

# Ansible Overview

## Definition
Ansible is an IT automation tool that configures systems, deploys software, and orchestrates advanced IT tasks like continuous deployments. It uses declarative YAML playbooks and requires no agents on target systems.

## Core Concepts

### Key Terms

| Term | Description |
|------|-------------|
| **Playbook** | YAML file defining automation tasks |
| **Module** | Unit of work executed on targets |
| **Role** | Reusable playbook organization |
| **Inventory** | List of managed hosts |
| **Fact** | System information collected by Ansible |

### How Ansible Works

```
Playbook (YAML)
    ↓
Inventory (hosts)
    ↓
Modules (tasks)
    ↓
SSH → Target Systems
```

### Ansible vs Other Tools

| Feature | Ansible | Chef | Puppet |
|---------|---------|------|-------|
| Agentless | ✅ | ❌ | ❌ |
| Language | YAML | Ruby DSL | Puppet DSL |
| Transport | SSH | Agent | Agent |

## Directory Layout (Best Practice)

```
production                # inventory for production
staging                   # inventory for staging

group_vars/
   group1.yml             # variables for groups
   group2.yml

host_vars/
   hostname1.yml          # variables for hosts

library/                  # custom modules
module_utils/             # module utilities
filter_plugins/           # custom filters

site.yml                  # master playbook
webservers.yml            # webserver tier
dbservers.yml             # dbserver tier

roles/
    common/               # role structure
        tasks/
        handlers/
        templates/
        files/
        vars/
        defaults/
        meta/
```

## Key Best Practices

### 1. Separate Inventory Files

Use separate inventory files for staging vs production:

```
production    # production hosts
staging       # staging hosts
```

### 2. Use Roles for Reusability

Organize playbooks into roles:
- `roles/common/` - shared tasks
- `roles/webtier/` - web server config
- `roles/dbtier/` - database config

### 3. Group by Role

Group hosts by purpose:
```
[webservers]
www-atl-1.example.com
www-atl-2.example.com

[dbservers]
db-atl-1.example.com
```

### 4. Use Variables Effectively

```
group_vars/webservers    # webserver variables
group_vars/dbservers    # database variables
host_vars/           # host-specific variables
```

## Related

- [[ansible.concept.directory-layout]] - Directory layout best practices
- [[ansible.reference.commands]] - CLI commands

## References

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/projects/ansible/2.9/user_guide/playbooks_best_practices.html)