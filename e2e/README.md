# End-to-End Tests

Black-box tests that exercise the running cluster over HTTP, the same way a
user (or Prometheus) would. They cover the workflows described in
`documentation/docs/design.md`:

- **Cluster smoke** (`test_cluster_health.py`) — every component answers on its
  ingress host.
- **Backend contract** (`test_backend_workflows.py`) — the shared endpoint
  contract (`/`, `/health`, `/error`, `/redirect`, `/metrics`) on both
  python-app and go-app, including traffic being counted in each app's own
  metrics.
- **Frontend** (`test_frontend.py`) — the React UI is served, and the backend
  ingresses answer the frontend's cross-origin calls with CORS headers.
- **Monitoring pipeline** (`test_monitoring_pipeline.py`) — Prometheus scrape
  targets are up, generated traffic becomes queryable in Prometheus, and
  Grafana has its datasource and all dashboards provisioned.

## Running

The suite expects the cluster to be up and reachable through the ingress on
port 80 (`*.localhost` hostnames resolve to loopback without any DNS setup):

```sh
./recreate-cluster.sh   # once, to (re)create the cluster
make test-e2e           # from the repository root
```

`make test-e2e` creates `e2e/.venv`, installs the pinned dependencies, and runs
pytest. To run tests directly during development:

```sh
cd e2e && .venv/bin/pytest tests/test_frontend.py
```

## Conventions

- Tests are black-box only: they talk to the cluster exclusively over HTTP,
  never to pods or kubectl.
- Eventual consistency (Prometheus scrapes, target discovery) is handled by
  polling with `cluster.wait_until`, never with bare sleeps.
- Tests that apply to both backends are parametrized via the `backend` fixture
  in `conftest.py` instead of being duplicated.
- There is intentionally no `tox.ini` here: the root Makefile discovers unit-test
  suites by `tox.ini`, and this suite must not run as part of `make test-unit`
  because it needs a live cluster.
