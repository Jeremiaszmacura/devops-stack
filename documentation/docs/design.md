# Architecture Design

## Purpose

A local Kubernetes playground (`kind`, 3 nodes: 1 control-plane, 2 workers) for practicing DevOps workflows: deploying services, exposing metrics, building Grafana dashboards, and observing traffic end-to-end.

## Components

| Component | Role | NodePort (host) |
|---|---|---|
| `python-app` | FastAPI sample backend, exposes `/metrics` | 8000 |
| `go-app` | Gin sample backend, exposes `/metrics` | 31080 |
| `nginx` | Standalone sample app, scraped via `nginx-exporter` | 30080 |
| `frontend-app` | React UI to trigger requests against python-app/go-app | 3000 |
| `prometheus` | Scrapes metrics from all app `/metrics` endpoints + node exporters | 30090 |
| `grafana` | Dashboards over Prometheus data, provisioned via Ansible | 30030 |
| `documentation` | MkDocs site (this doc) | 12000 |

## Traffic Flow

```
Browser → frontend-app (nginx, :3000)
            ├─ /api/python/* → python-app-service:8000
            └─ /api/go/*     → go-app-service:8080

All apps → /metrics → Prometheus (:30090) → Grafana (:30030)
```

- `frontend-app` ships its own internal nginx reverse proxy (`frontend-app/nginx.conf`) to route API calls to backend services by Kubernetes service name, avoiding CORS.
- The standalone `nginx` component is unrelated to that proxy — it's a sample app monitored via `nginx-exporter` on port 9113.

## Sample Backends (python-app, go-app)

Both expose the same endpoint contract so the frontend can target either interchangeably:
- `GET /` — home
- `GET /health` — health check
- `GET /error` — simulated 500
- `GET /redirect` — redirect to `/health`
- `GET /metrics` — Prometheus format

## Monitoring

- Prometheus scrapes: node exporters (cluster/node metrics) + each app's `/metrics` + `nginx-exporter`.
- Grafana dashboards are provisioned as code via Ansible (`monitoring/grafana/ansible/deploy-dev.yaml`), reading JSON definitions from `monitoring/grafana/ansible/dashboards/*.json` (one file per dashboard: `go-app`, `python-app`, `nginx`, `infrastructure`).
- Dev credentials are hardcoded (`admin`/`admin`), no Vault.

## Deployment

- Entry point: `./recreate-cluster.sh` — idempotent, deletes/recreates the `kind` cluster, builds and loads all Docker images, applies each component's `k8s/` manifests in order (Prometheus → Grafana → NGINX → python-app → go-app → frontend-app → documentation), then provisions Grafana dashboards via Ansible.
- Each component directory is self-contained: its own `Dockerfile`, `k8s/` manifests, and `README.md`.
- Host↔NodePort mappings are fixed in `kind-cluster.yaml`.

## Conventions

- All K8s manifests applied idempotently (`kubectl apply`).
- New Go services are auto-discovered by presence of `go.mod`; new Python services by presence of `tox.ini` (see `adding-a-service.md`).
