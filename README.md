# Platform Engineering Cluster Sample

This project contains Kubernetes cluster for Platform Engineering learning purposes. Kubernetes cluster is deployed with `kind` tool and contains multiple components that are commonly used in production environments. The cluster is designed to be a playground for learning and experimenting with Kubernetes and its ecosystem.

## Documentation

https://jeremiaszmacura.github.io/devops-stack/

## Deploy

Create Kubernetes Cluster with all the components:

```sh
./recreate-cluster.sh
```

All services are then reachable through ingress hostnames — the frontend at
http://app.localhost, Grafana at http://grafana.localhost, and the full
documentation at http://docs.localhost.
