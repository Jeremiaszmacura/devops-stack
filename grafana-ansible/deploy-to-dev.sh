#!/bin/bash
echo "🚀 Deploying to DEVELOPMENT environment..."
ansible-playbook deploy-dev.yaml --vault-password-file .vault_pass