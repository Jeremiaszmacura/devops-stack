# End-to-End Tests

The `e2e/` directory contains a black-box pytest suite that verifies the
deployed cluster's workflows over HTTP — the same paths a user or Prometheus
would take. It never talks to pods or kubectl directly: every request goes
through the ingress on port 80, routed by `*.localhost` hostname, so the suite
runs identically on a developer machine and in CI.

## What is covered

| Suite | Workflow |
|---|---|
| `test_cluster_health.py` | Every component answers HTTP 200 on its ingress host |
| `test_backend_workflows.py` | Shared backend contract (`/`, `/health`, `/error`, `/redirect`, `/metrics`) on python-app and go-app, and traffic being counted in each app's metrics |
| `test_frontend.py` | Frontend serves the UI, and the backend ingresses answer its cross-origin calls with CORS headers |
| `test_monitoring_pipeline.py` | Prometheus targets up, generated traffic queryable in Prometheus, Grafana datasource and dashboards provisioned |

Tests that apply to both backends run twice via the parametrized `backend`
fixture. Eventual consistency (scrape intervals, target discovery) is handled
by polling with timeouts, not sleeps.

## Running locally

```sh
./recreate-cluster.sh   # deploy the cluster first
make test-e2e
```

`make test-e2e` creates a virtualenv in `e2e/.venv`, installs pinned
dependencies, and runs pytest.

## Continuous integration

`.github/workflows/e2e.yaml` runs on pull requests, pushes to `main`, and
manual dispatch. The job installs kind and Ansible on the runner, executes
`./recreate-cluster.sh` to build images and deploy everything into a real kind
cluster, then runs `make test-e2e` as the pass/fail gate. On failure it dumps
pod status, recent events, and deployment logs.
