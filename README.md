# DevOps Practice Cluster

This project contains Kubernetes cluster for DevOps learning purposes.

## Components

- HashiCorp `Vault` for secrets management
- `Prometheus` for monitoring
- `Grafana` for visualization
- `NGINX` as a sample application
- `Python` and `Go applications` for testing Vault integration
- `Frontend application` for testing the Python and Go applications

## Deploy

Create Kubernetes Cluster with all the components:

```sh
./recreate-cluster.sh
```
