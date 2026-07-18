# Monitoring

Traffic in the cluster is observed with the classic pipeline: applications expose
Prometheus metrics on `/metrics`, Prometheus scrapes them, Grafana visualizes
Prometheus data. Everything runs in-cluster; only the UIs are exposed through
the ingress (`http://prometheus.localhost`, `http://grafana.localhost`).

## Prometheus

Prometheus is deployed from `monitoring/prometheus/k8s/` with its scrape
configuration in a ConfigMap (`prometheus-config.yaml`). Default scrape
interval is 15s; the sample apps are scraped every 5s so dashboards react
quickly to generated traffic.

| Job | Target | What it measures |
|---|---|---|
| `python-app` | `python-app-service:8000/metrics` | FastAPI backend HTTP metrics |
| `go-app` | `go-app-service:8080/metrics` | Gin backend HTTP metrics |
| `nginx-metrics` | `nginx-exporter:9113` | Standalone NGINX sample app (via `nginx-exporter` sidecar reading `stub_status`) |
| `node-exporter` | `node-exporter:9100` | Node CPU/memory/disk, run as a DaemonSet on every cluster node |
| `self` | `localhost:9090` | Prometheus itself |

## Application metrics

Both sample backends implement the same instrumentation middleware
(`python-app/src/prometheus_config.py`, `go-app/internal/appmetrics/prometheus.go`):

- `http_requests_total{method, endpoint, status_code}` — request counter
- `http_request_duration_seconds{method, endpoint}` — latency histogram
- `http_responses_by_status_total{status_class}` — responses by 2XX/4XX/5XX class
- `monitoring_requests_total{endpoint, user_agent}` — `/metrics` and `/health`
  hits tracked separately, so probe/scrape noise stays out of the app metrics

The `endpoint` label always holds a *registered route path*; requests to
unknown paths are labeled with the constant `unmatched` to keep time-series
cardinality bounded (bot scans must not mint a new series per probed URL).

## Grafana

Grafana is deployed from `monitoring/grafana/k8s/`; admin credentials come
from the `grafana-admin-secret` Secret (dev defaults: `admin`/`admin`).

Provisioning is done as code with Ansible, via the Grafana HTTP API:

- `monitoring/grafana/ansible/setup-datasource.yaml` registers Prometheus
  (`http://prometheus:9090`, in-cluster DNS) as the default datasource.
- `monitoring/grafana/ansible/deploy-dashboards.yaml` uploads every JSON file
  in `monitoring/grafana/ansible/dashboards/` — one file per dashboard:
  `python-app`, `go-app`, `nginx`, `infrastructure`.

Both playbooks run automatically at the end of `./recreate-cluster.sh`
(wrapped by `deploy-dev.yaml`). They are idempotent — dashboards are uploaded
with `overwrite: true` — so they can be re-run at any time:

```sh
ansible-playbook monitoring/grafana/ansible/deploy-dev.yaml
```

### Adding or changing a dashboard

1. Edit the dashboard in the Grafana UI, or edit the JSON directly.
2. Save the JSON model to `monitoring/grafana/ansible/dashboards/<name>.json`
   (one dashboard per file, `"id": null` and `"overwrite": true` semantics are
   handled by the playbook).
3. Re-run the playbook above. The Git repository stays the source of truth —
   dashboards clicked together in the UI but not exported are lost on the next
   cluster recreation.
