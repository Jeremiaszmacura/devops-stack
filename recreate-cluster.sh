#!/bin/bash
set -euo pipefail

# Poll an URL every 2s until it answers over HTTP or the timeout (seconds)
# elapses; prints a success line or a warning, never fails the script.
wait_for_url() {
    local name=$1 url=$2 timeout=$3
    echo "  Checking ${name}..."
    while ! curl -s "$url" > /dev/null && [ "$timeout" -gt 0 ]; do
        sleep 2
        timeout=$((timeout-2))
    done
    if [ "$timeout" -le 0 ]; then
        echo "⚠️  Warning: ${name} not accessible at ${url}"
        echo "   Check service and pod status with: kubectl get pods,services"
        return 0
    fi
    echo "✅ ${name} is accessible"
}

echo "🔄 Recreating Kind cluster..."

# Cleanup and create cluster; deletion may fail when no cluster exists yet
kind delete cluster --name sample-cluster || true
kind create cluster --config kind-cluster.yaml --name sample-cluster

# Install the ingress controller early so it starts while images build
echo "🌐 Installing ingress-nginx controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.13.1/deploy/static/provider/kind/deploy.yaml

# Build and load application images
echo "🐳 Building and loading Docker images..."
docker build -t python-app:dev ./python-app
docker build -t go-app:dev ./go-app
docker build -t mkdocs-documentation:dev ./documentation
docker build -t frontend-app:dev ./frontend-app

kind load docker-image python-app:dev --name sample-cluster
kind load docker-image go-app:dev --name sample-cluster
kind load docker-image mkdocs-documentation:dev --name sample-cluster
kind load docker-image frontend-app:dev --name sample-cluster

# The controller's admission webhook must be up before Ingress resources apply
echo "⏳ Waiting for ingress-nginx controller..."
kubectl rollout status deployment/ingress-nginx-controller -n ingress-nginx --timeout=180s

# Deploy applications in order
echo "🚀 Deploying applications..."

# Deploy monitoring (Prometheus, then Grafana)
echo "  📊 Deploying Prometheus..."
kubectl apply -f monitoring/prometheus/k8s/

echo "  📈 Deploying Grafana..."
kubectl apply -f monitoring/grafana/k8s/

# Deploy web services
echo "  🌐 Deploying NGINX..."
kubectl apply -f nginx/k8s/

echo "  🐍 Deploying Python app..."
kubectl apply -f python-app/k8s/

echo "  🔧 Deploying Go app..."
kubectl apply -f go-app/k8s/

echo "  ⚛️  Deploying Frontend App..."
kubectl apply -f frontend-app/k8s/

echo "  📚 Deploying documentation..."
kubectl apply -f documentation/k8s/

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment --all || echo "⚠️  Warning: some deployments did not become ready within 300s"

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
        kubectl describe pod $pod | grep -A 10 -B 5 "Events:" || true
        echo ""
    done
fi

# Wait for services to be accessible
echo "⏳ Waiting for services to be accessible..."
wait_for_url "Grafana" http://grafana.localhost 60
wait_for_url "Python app" http://python.localhost 30
wait_for_url "Frontend app" http://app.localhost 30
wait_for_url "Documentation" http://docs.localhost 30

# Show service URLs
echo ""
echo "🎉 Cluster ready! Services available at:"
echo "  📊 Prometheus: http://prometheus.localhost"
echo "  📈 Grafana: http://grafana.localhost"
echo "  🌐 NGINX: http://nginx.localhost"
echo "  🐍 Python App: http://python.localhost"
echo "  🔧 Go App: http://go.localhost"
echo "  ⚛️  Frontend App: http://app.localhost"
echo "  📚 Documentation: http://docs.localhost"
echo ""

# Deploy Grafana dashboards only if Grafana is accessible
if curl -s http://grafana.localhost > /dev/null; then
    echo "🚀 Deploying dashboards to DEV environment..."
    ansible-playbook monitoring/grafana/ansible/deploy-dev.yaml
else
    echo "⚠️  Skipping dashboard deployment - Grafana not accessible"
    echo "   Run the following command manually once Grafana is ready:"
    echo "   ansible-playbook monitoring/grafana/ansible/deploy-dev.yaml"
fi

echo "✅ Cluster setup complete!"