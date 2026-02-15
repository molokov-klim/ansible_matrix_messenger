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
Set the required environment variables with your specific values:
- `ANSIBLE_USER`: Your server username
- `SERVER_IP`: Your server IP address
- `ANSIBLE_SSH_PRIVATE_KEY_PATH`: Path to your SSH private key
- Other variables as needed

For local development, you can use a .env file loader or export variables directly in your shell.

### 4. Generate inventory file
Run the following command to generate the inventory.ini file from the template:
```bash
python generate_inventory.py
```

### 5. Запуск через CI/CD
Плейбук запускается автоматически через GitHub Actions при пуше в ветку main.

## CI/CD Configuration
Для использования в GitHub Actions или других CI/CD системах:
1. Сохраните чувствительные переменные в GitHub Secrets
2. Передавайте секреты как переменные окружения во время выполнения плейбука
3. Используйте скрипт `generate_inventory.py` для генерации inventory из переменных окружения

ВАЖНО: Все запуски плейбуков должны происходить исключительно через CI/CD pipeline, локальный запуск не предусмотрен.

## Files Description
- `inventory.ini.j2`: Jinja2 template for inventory file
- `generate_inventory.py`: Script to generate inventory from template and environment variables
- `ansible.cfg`: Ansible configuration file
- `playbooks/initial_setup.yml`: Main playbook for initial server setup
- `group_vars/`, `host_vars/`, `roles/`: Standard Ansible directories for future expansion

## Security Notes
- Do not commit `.env.yml` or `inventory.ini` to version control
- Use Ansible Vault for encrypting sensitive data in production environments
- Ensure proper SSH key permissions (typically 600)

## Setup Instructions
See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed instructions on how to set up both the server-side and environment variables.