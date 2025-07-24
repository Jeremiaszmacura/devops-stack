#!/bin/bash
echo "🚀 Deploying to PRODUCTION environment..."
echo "⚠️  WARNING: This will deploy to PRODUCTION!"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    ansible-playbook deploy-prod.yaml --vault-password-file .vault_pass
else
    echo "❌ Deployment cancelled"
    exit 1
fi