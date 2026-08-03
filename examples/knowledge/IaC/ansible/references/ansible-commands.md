---
id: ansible.reference.commands
title: Ansible Commands
type: reference
domain: ansible
tags:
  - ansible
  - commands
  - cli
  - cheatsheet
summary: Quick reference for common Ansible CLI commands for running playbooks, managing inventory, and ad-hoc commands.
related:
  - [[ansible.concept.overview]]
source: https://docs.ansible.com/projects/ansible/2.9/user_guide/playbooks_best_practices.html
created: 2026-04-28
updated: 2026-04-28
confidence: high
status: active
version: "1.0.0"
quality_score: 80
---

# Ansible Commands

## Overview
Quick reference for common Ansible CLI commands.

## Running Playbooks

| Command | Description |
|---------|-------------|
| `ansible-playbook site.yml` | Run master playbook |
| `ansible-playbook -i production site.yml` | Run with specific inventory |
| `ansible-playbook site.yml --limit webservers` | Limit to group |
| `ansible-playbook site.yml --tags ntp` | Run only tagged tasks |
| `ansible-playbook site.yml --check` | Dry run (check mode) |

## Inventory Commands

| Command | Description |
|---------|-------------|
| `ansible all -i production -m ping` | Ping all hosts |
| `ansible webservers -i production -m command -a '/sbin/reboot'` | Ad-hoc command |
| `ansible-playbook --list-hosts site.yml` | List hosts that would run |
| `ansible-playbook --list-tasks site.yml` | List tasks that would run |

## Inventory File Example

```ini
# production
[webservers]
www-atl-1.example.com
www-atl-2.example.com

[dbservers]
db-atl-1.example.com
db-atl-2.example.com

[webservers:children]
atlanta_webservers
boston_webservers

[dbservers:children]
atlanta_dbservers
boston_dbservers
```

## Common Options

| Option | Description |
|--------|-------------|
| `-i` | Inventory file |
| `-l` | Limit to hosts (short for --limit) |
| `-t` | Tags (short for --tags) |
| `-k` | Ask for SSH password |
| `--become` | Become sudo |
| `--ask-become-pass` | Ask for sudo password |

## Examples

```bash
# Run on production webservers
ansible-playbook -i production webservers.yml

# Run on boston only
ansible-playbook -i production webservers.yml --limit boston

# Run NTP tasks only
ansible-playbook -i production site.yml --tags ntp

# Check mode (dry run)
ansible-playbook -i production site.yml --check
```

## Related

- [[ansible.concept.overview]] - Ansible overview
- [[ansible.concept.directory-layout]] - Directory layout