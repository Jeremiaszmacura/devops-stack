kind delete cluster
kind create cluster
docker build -t python-app:dev ./python-app
kind load docker-image python-app:dev
kubectl apply -f kubernetes

sleep 120

echo http://localhost:9090
echo http://localhost:3000
echo http://localhost:8080
echo http://localhost:8000

kubectl port-forward svc/prometheus 9090:9090 \
& kubectl port-forward svc/grafana-service 3000:3000 \
& kubectl port-forward svc/nginx-service 8080:80 \
& kubectl port-forward svc/python-app-service 8000:8000 \
& sleep 15 && echo "🚀 Deploying dashboards to DEV environment..." && ansible-playbook grafana-ansible/deploy-dev.yaml --vault-password-file grafana-ansible/vault/.vault_pass