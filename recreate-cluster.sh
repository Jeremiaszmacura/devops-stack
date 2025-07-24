#!/bin/bash

echo "🔄 Recreating Kind cluster..."

# Cleanup and create cluster
kind delete cluster --name sample-cluster
kind create cluster --config kind-cluster.yaml --name sample-cluster

# Build and load application images
echo "🐳 Building and loading Docker images..."
docker build -t python-app:dev ./python-app
docker build -t mkdocs-documentation:dev ./documentation

kind load docker-image python-app:dev --name sample-cluster
kind load docker-image mkdocs-documentation:dev --name sample-cluster

# Deploy infrastructure components first (namespaces, RBAC, etc.)
echo "🏗️  Deploying infrastructure components..."
if [ -d "infrastructure/k8s" ]; then
    kubectl apply -f infrastructure/k8s/
fi

# Deploy applications in order
echo "🚀 Deploying applications..."

# Deploy monitoring first (Prometheus, then Grafana)
echo "  📊 Deploying Prometheus..."
kubectl apply -f monitoring/prometheus/k8s/

echo "  📈 Deploying Grafana..."
kubectl apply -f monitoring/grafana/k8s/

# Deploy web services
echo "  🌐 Deploying NGINX..."
kubectl apply -f nginx/k8s/

echo "  🐍 Deploying Python app..."
kubectl apply -f python-app/k8s/

echo "  📚 Deploying documentation..."
kubectl apply -f documentation/k8s/

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment --all

# Check for any failed pods
echo "🔍 Checking pod status..."
failed_pods=$(kubectl get pods --field-selector=status.phase!=Running -o jsonpath='{.items[*].metadata.name}')
if [ ! -z "$failed_pods" ]; then
    echo "⚠️  Some pods are not running:"
    kubectl get pods --field-selector=status.phase!=Running
    echo ""
    echo "📋 Pod details:"
    for pod in $failed_pods; do
        echo "--- Pod: $pod ---"
        kubectl describe pod $pod | grep -A 10 -B 5 "Events:"
        echo ""
    done
fi

# Wait for services to be accessible
echo "⏳ Waiting for services to be accessible..."

# Check Grafana
echo "  Checking Grafana..."
timeout=60
while ! curl -s http://localhost:30030 > /dev/null && [ $timeout -gt 0 ]; do
    sleep 2
    timeout=$((timeout-2))
done

if [ $timeout -le 0 ]; then
    echo "⚠️  Warning: Grafana not accessible at http://localhost:30030"
    echo "   You may need to wait longer or check the service status"
    kubectl get pods -l app=grafana
else
    echo "✅ Grafana is accessible"
fi

# Check Python App
echo "  Checking Python app..."
timeout=30
while ! curl -s http://localhost:8000 > /dev/null && [ $timeout -gt 0 ]; do
    sleep 2
    timeout=$((timeout-2))
done

if [ $timeout -le 0 ]; then
    echo "⚠️  Warning: Python app not accessible at http://localhost:8000"
    echo "   Check service and pod status:"
    kubectl get services python-app-service
    kubectl get pods -l app=python-app
else
    echo "✅ Python app is accessible"
fi

# Check MkDocs
echo "  Checking Documentation..."
timeout=30
while ! curl -s http://localhost:12000 > /dev/null && [ $timeout -gt 0 ]; do
    sleep 2
    timeout=$((timeout-2))
done

if [ $timeout -le 0 ]; then
    echo "⚠️  Warning: Documentation not accessible at http://localhost:12000"
    echo "   Check service and pod status:"
    kubectl get services mkdocs-service
    kubectl get pods -l app=mkdocs
    echo "   Pod events:"
    kubectl get events --field-selector involvedObject.kind=Pod --sort-by='.lastTimestamp' | grep mkdocs
else
    echo "✅ Documentation is accessible"
fi

# Show service URLs (using NodePort from kind-cluster.yaml)
echo ""
echo "🎉 Cluster ready! Services available at:"
echo "  📊 Prometheus: http://localhost:30090"
echo "  📈 Grafana: http://localhost:30030"
echo "  🌐 NGINX: http://localhost:30080"
echo "  🐍 Python App: http://localhost:8000"
echo "  📚 Documentation: http://localhost:12000"
echo ""

# Show all service status
echo "📊 Service Status:"
kubectl get services
echo ""

echo "🚀 Pod Status:"
kubectl get pods
echo ""

# Deploy Grafana dashboards only if Grafana is accessible
if curl -s http://localhost:30030 > /dev/null; then
    echo "🚀 Deploying dashboards to DEV environment..."
    # Update the Grafana URL in the Ansible playbook to use the correct port
    GRAFANA_URL="http://localhost:30030" ansible-playbook monitoring/grafana/ansible/deploy-dev.yaml --vault-password-file monitoring/grafana/ansible/vault/.vault_pass
else
    echo "⚠️  Skipping dashboard deployment - Grafana not accessible"
    echo "   Run the following command manually once Grafana is ready:"
    echo "   GRAFANA_URL='http://localhost:30030' ansible-playbook monitoring/grafana/ansible/deploy-dev.yaml --vault-password-file monitoring/grafana/ansible/vault/.vault_pass"
fi

echo "✅ Cluster setup complete!"
