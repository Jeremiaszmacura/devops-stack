# DevOps Practice Cluster

This project contains Kubernetes cluster with sample applications, Prometheus monitoring, Grafana for DevOps learning purposes.

## Deploy

Create Kubernetes Cluster with all the components:

```sh
./recreate-cluster.sh
```

## Exposed Cluster Components

Port forwards:

Prometheus
```text
http://localhost:9090
```

Grafana
```text
http://localhost:3000
```

Ngnix
```text
http://localhost:30080
```

Python App
```text
http://localhost:30100
```