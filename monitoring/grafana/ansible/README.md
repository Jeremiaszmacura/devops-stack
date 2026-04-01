# Grafana Dashboard Deployment with Ansible

Automated deployment of Grafana dashboards using Ansible.

## Structure

```
grafana-ansible/
├── README.md                  # This file
├── deploy-dev.yaml           # Development deployment
├── deploy-prod.yaml          # Production deployment
├── setup-datasource.yaml    # Configure Prometheus datasource
├── deploy-dashboards.yaml   # Deploy dashboard JSON files
├── deploy-to-dev.sh         # Dev deployment script
├── deploy-to-prod.sh        # Prod deployment script (with confirmation)
└── dashboards/              # Dashboard JSON definitions
    ├── python-app.json
    ├── nginx.json
    └── infrastructure.json
```

## Quick Start

### Development Environment
```bash
# Deploy to development (localhost)
./deploy-to-dev.sh

# Or manually
ansible-playbook deploy-dev.yaml
```

### Production Environment
```bash
# Deploy to production (with safety confirmation)
./deploy-to-prod.sh

# Or manually
ansible-playbook deploy-prod.yaml
```

## Individual Components

```bash
# Setup Prometheus datasource only
ansible-playbook setup-datasource.yaml

# Deploy dashboards only
ansible-playbook deploy-dashboards.yaml
```

## Adding New Dashboards

1. Create a new JSON file in `dashboards/` directory
2. Ensure the JSON includes `"overwrite": true` to replace existing dashboards
3. Run deployment: `./deploy-to-dev.sh`

Example dashboard structure:
```json
{
  "dashboard": {
    "id": null,
    "title": "My New Dashboard",
    "panels": []
  },
  "overwrite": true
}
```

## Troubleshooting

### Connection Issues
- Ensure Grafana is accessible at `http://localhost:30030`
- Check port-forwarding is active for local development

### Dashboard Issues
- Validate JSON syntax in dashboard files
- Ensure `"overwrite": true` is set in JSON
- Check Grafana logs for import errors

## Prerequisites

- Ansible installed (`brew install ansible` or `pip install ansible`)
- Running Grafana instance
- Dashboard JSON files in correct format
