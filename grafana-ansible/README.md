# Grafana Dashboard Deployment with Ansible

Automated deployment of Grafana dashboards using Ansible with Vault-encrypted credentials for multiple environments.

## 🏗️ Structure

```
grafana-ansible/
├── README.md                  # This file
├── deploy-dev.yaml           # Development deployment
├── deploy-prod.yaml          # Production deployment  
├── setup-datasource.yaml    # Configure Prometheus datasource
├── deploy-dashboards.yaml   # Deploy dashboard JSON files
├── vault-dev.yml            # Encrypted dev credentials
├── vault-prod.yml           # Encrypted prod credentials
├── .vault_pass              # Vault password file
├── deploy-to-dev.sh         # Dev deployment script
├── deploy-to-prod.sh        # Prod deployment script (with confirmation)
└── dashboards/              # Dashboard JSON definitions
    ├── python-app-metrics.json
    └── infrastructure-overview.json
```

## 🚀 Quick Start

### Development Environment
```bash
# Deploy to development (localhost)
./deploy-to-dev.sh

# Or manually
ansible-playbook deploy-dev.yaml --vault-password-file .vault_pass
```

### Production Environment
```bash
# Deploy to production (with safety confirmation)
./deploy-to-prod.sh

# Or manually
ansible-playbook deploy-prod.yaml --vault-password-file .vault_pass
```

## 🔧 Individual Components

```bash
# Setup Prometheus datasource only
ansible-playbook setup-datasource.yaml -e env=dev --vault-password-file .vault_pass

# Deploy dashboards only
ansible-playbook deploy-dashboards.yaml -e env=dev --vault-password-file .vault_pass
```

## 🔐 Vault Management

### View Credentials
```bash
# Development
ansible-vault view vault-dev.yml --vault-password-file .vault_pass

# Production
ansible-vault view vault-prod.yml --vault-password-file .vault_pass
```

### Edit Credentials
```bash
# Development
ansible-vault edit vault-dev.yml --vault-password-file .vault_pass

# Production
ansible-vault edit vault-prod.yml --vault-password-file .vault_pass
```

## 📊 Adding New Dashboards

1. Create a new JSON file in `dashboards/` directory
2. Ensure the JSON includes `"overwrite": true`
3. Run deployment: `./deploy-to-dev.sh`

Example dashboard structure:
```json
{
  "dashboard": {
    "id": null,
    "title": "My New Dashboard",
    "panels": [ /* your panels */ ]
  },
  "overwrite": true
}
```

## 🌍 Environment Configuration

### Development (vault-dev.yml)
- **Grafana URL**: `http://localhost:3000`
- **Prometheus URL**: `http://prometheus:9090`
- **Credentials**: Basic dev credentials

### Production (vault-prod.yml)
- **Grafana URL**: Production Grafana instance
- **Prometheus URL**: Production Prometheus instance
- **Credentials**: Secure production credentials

## ✨ Features

- 🔒 **Secure**: Credentials encrypted with Ansible Vault
- 🏗️ **Multi-environment**: Separate dev/prod configurations
- 🔄 **Automatic updates**: Overwrites existing dashboards
- 📊 **Dashboard discovery**: Automatically finds all JSON files
- 🛡️ **Safety checks**: Production deployment requires confirmation
- 📝 **Detailed logging**: Shows deployment status and results

## 🧪 Integration with Cluster

This is automatically called by `recreate-cluster.sh`:
```bash
# After cluster setup, dashboards are deployed
sleep 15 && ansible-playbook grafana-ansible/deploy-dev.yaml --vault-password-file grafana-ansible/.vault_pass
```

## 🔍 Troubleshooting

### Vault Issues
```bash
# Test vault password
ansible-vault view vault-dev.yml --vault-password-file .vault_pass

# Re-encrypt with new password
ansible-vault rekey vault-dev.yml
```

### Connection Issues
- Ensure Grafana is accessible at the configured URL
- Check port-forwarding is active for local development
- Verify credentials in vault files

### Dashboard Issues
- Validate JSON syntax in dashboard files
- Ensure `"overwrite": true` is set in JSON
- Check Grafana logs for import errors

## 📋 Prerequisites

- Ansible installed (`brew install ansible` or `pip install ansible`)
- Running Grafana instance
- Valid credentials configured in vault files
- Dashboard JSON files in correct format
