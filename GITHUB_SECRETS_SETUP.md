# GitHub Secrets Configuration

To use the deployment workflow, you need to configure the following secrets in your GitHub repository:

## Required Secrets

1. `MATRIX_SERVER_HOST` - IP address or hostname of your Matrix server
   Example: `91.219.150.226`

2. `MATRIX_SERVER_USER` - SSH username to connect to your server
   Example: `hash`

3. `MATRIX_SERVER_SSH_KEY` - Private SSH key to access your server
   This should be the full content of your private key file (usually ~/.ssh/id_rsa)

4. `MATRIX_ADMIN_PASSWORD` - Password for the Matrix admin user

## How to Add Secrets

1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Add each of the secrets listed above

## Deployment Process

1. Go to the "Actions" tab in your repository
2. Select "Deploy Matrix Messenger" workflow from the left sidebar
3. Click "Run workflow"
4. Choose the target environment (staging/production)
5. Optionally check "Force deployment even if tests fail"
6. Click "Run workflow" to start the deployment

## Required Environment Variables

You'll also need to set up an environment called "production" (and optionally "staging") in your repository settings with any environment-specific variables.