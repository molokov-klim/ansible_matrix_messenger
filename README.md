# Ansible Project for Matrix Messenger

## Overview
This Ansible project sets up a server for Matrix Messenger on Ubuntu 22.04. It performs initial server setup including system updates and installation of required packages.

## Prerequisites
- Python 3.x
- Ansible
- SSH access to target server

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd ansible_matrix_messenger
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Update the `.env.yml` file with your specific values:
- `ansible_user`: Your server username
- `server_ip`: Your server IP address
- `ansible_ssh_private_key_path`: Path to your SSH private key
- Other variables as needed

### 4. Generate inventory file
Run the following command to generate the inventory.ini file from the template:
```bash
python generate_inventory.py
```

### 5. Run the playbook
Execute the initial setup playbook:
```bash
ansible-playbook -i inventory.ini playbooks/initial_setup.yml
```

## CI/CD Configuration
For use in GitHub Actions or other CI/CD pipelines:
1. Store sensitive variables in GitHub Secrets
2. Pass secrets as environment variables during playbook execution
3. Use the same `generate_inventory.py` script to generate inventory from environment variables

Example GitHub Actions step:
```yaml
- name: Generate inventory
  run: |
    echo "server_ip=${{ secrets.SERVER_IP }}" >> .env.local
    echo "ansible_user=${{ secrets.ANSIBLE_USER }}" >> .env.local
    # Add other variables as needed
    python generate_inventory.py
```

## Files Description
- `.env.yml`: Contains environment variables (credentials, server info, etc.)
- `inventory.ini.j2`: Jinja2 template for inventory file
- `generate_inventory.py`: Script to generate inventory from template and variables
- `ansible.cfg`: Ansible configuration file
- `playbooks/initial_setup.yml`: Main playbook for initial server setup
- `group_vars/`, `host_vars/`, `roles/`: Standard Ansible directories for future expansion

## Security Notes
- Do not commit `.env.yml` or `inventory.ini` to version control
- Use Ansible Vault for encrypting sensitive data in production environments
- Ensure proper SSH key permissions (typically 600)