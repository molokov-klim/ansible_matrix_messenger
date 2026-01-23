# Ansible Matrix Messenger

Private messenger ansible project for deploying a family-oriented Matrix messenger server.

## Features

- Deploy Matrix Synapse homeserver
- Configure Nginx reverse proxy with SSL
- Automatic SSL certificate setup (Let's Encrypt)
- User account management
- Security hardening

## GitHub Actions CI/CD

This project includes GitHub Actions workflows for:
- Ansible syntax validation
- Linting with ansible-lint
- Testing with Molecule and Docker
- Manual deployment to server

Workflows are triggered on pushes and pull requests to the main branch. Additionally, there's a manual deployment workflow that can be triggered with a button press.

## Requirements

- Ubuntu 22.04 LTS
- Ansible 2.9+
- Python 3.x

## Installation

1. Clone the repository
2. Install requirements: `ansible-galaxy install -r requirements.yml`
3. Update inventory file with your server details
4. Run the playbook: `ansible-playbook -i inventory site.yml`

## License

MIT
