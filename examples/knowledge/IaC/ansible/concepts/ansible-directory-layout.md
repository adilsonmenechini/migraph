---
id: ansible.concept.directory-layout
title: Ansible Directory Layout
type: concept
domain: ansible
tags:
  - ansible
  - directory-layout
  - best-practices
  - roles
  - structure
summary: Recommended directory structure for Ansible projects including inventory, group_vars, host_vars, roles, and playbooks.
related:
  - [[ansible.concept.overview]]
source: https://docs.ansible.com/projects/ansible/2.9/user_guide/playbooks_best_practices.html
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 85
---

# Ansible Directory Layout

## Standard Directory Structure

```
.
├── production                # inventory file for production servers
├── staging                   # inventory file for staging environment
├── group_vars/
│   ├── group1.yml         # variables for particular groups
│   └── group2.yml
├── host_vars/
│   ├── hostname1.yml      # variables for particular systems
│   └── hostname2.yml
├── library/                  # custom modules (optional)
├── module_utils/             # custom module_utils (optional)
├── filter_plugins/           # custom filter plugins (optional)
├── site.yml                # master playbook
├── webservers.yml         # playbook for webserver tier
├── dbservers.yml          # playbook for dbserver tier
└── roles/
    ├── common/
    │   ├── tasks/
    │   │   └── main.yml
    │   ├── handlers/
    │   │   └── main.yml
    │   ├── templates/
    │   │   └── ntp.conf.j2
    │   ├── files/
    │   │   ├── bar.txt
    │   │   └── foo.sh
    │   ├── vars/
    │   │   └── main.yml
    │   ├── defaults/
    │   │   └── main.yml
    │   └── meta/
    │       └── main.yml
    ├── webtier/
    ├── monitoring/
    └── fooapp/
```

## Key Components

### Inventory Files

Separate files for different environments:
- `production` - production hosts
- `staging` - staging hosts

### Group Variables (`group_vars/`)

Variables applied to groups:

```yaml
# group_vars/webservers
apacheMaxRequestsPerChild: 3000
apacheMaxClients: 900
```

### Host Variables (`host_vars/`)

Variables specific to hosts:

```yaml
# host_vars/db-server1
mysql_port: 3306
```

### Roles Structure

Each role contains:
- `tasks/main.yml` - main tasks
- `handlers/main.yml` - handlers
- `templates/` - Jinja2 templates
- `files/` - static files
- `vars/main.yml` - role variables
- `defaults/main.yml` - default variables (lowest priority)
- `meta/main.yml` - role dependencies

## Alternative Layout

For larger environments with more separation:

```
inventories/
├── production/
│   ├── hosts
│   ├── group_vars/
│   └── host_vars/
└── staging/
    ├── hosts
    ├── group_vars/
    └── host_vars/

library/
module_utils/
filter_plugins/

site.yml
webservers.yml
dbservers.yml

roles/
```

## Best Practices Summary

1. **Separate inventory** for staging vs production
2. **Use roles** for reusable playbooks
3. **Group by role** (webservers, dbservers)
4. **Group by geography** if applicable
5. **Version control** your playbooks
6. **Always name tasks** for clarity
7. **Keep it simple** - don't overcomplicate

## Related

- [[ansible.concept.overview]] - Ansible overview

## References

- [Ansible Best Practices](https://docs.ansible.com/projects/ansible/2.9/user_guide/playbooks_best_practices.html)