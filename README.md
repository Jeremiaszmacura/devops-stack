# DevOps Practice Cluster

This project contains Kubernetes cluster for DevOps learning purposes. Kubernetes cluster is deployed with `kind` tool and contains multiple components that are commonly used in production environments. The cluster is designed to be a playground for learning and experimenting with Kubernetes and its ecosystem.

## Components

- `Prometheus` for monitoring
- `Grafana` for visualization
- `NGINX` as a sample application
- `Python` and `Go applications` as sample backend services
- `Frontend application` for testing the Python and Go applications

## Deploy

Create Kubernetes Cluster with all the components:

```sh
./recreate-cluster.sh
```
