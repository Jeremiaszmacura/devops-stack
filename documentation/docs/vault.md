# Vault

HashiCorp Vault is the cluster's shared secret store. Both sample backends
(python-app and go-app) write and read secrets in it through their `/secret`
endpoints, demonstrating a service-to-secret-store workflow end to end.

## Dev mode

Vault runs in **dev mode** (`vault server -dev`), which matches the playground
character of this cluster but is unsuitable for anything else:

- Storage is in-memory — **all secrets are lost when the Vault pod restarts**.
- The server starts initialized and unsealed automatically.
- The KV v2 secrets engine is pre-mounted at `secret/`.
- The root token is fixed to `root` via `VAULT_DEV_ROOT_TOKEN_ID`.

## How the backends use it

Each backend Deployment sets three environment variables:

| Variable | Value | Purpose |
|---|---|---|
| `VAULT_ADDR` | `http://vault-service:8200` | In-cluster Vault API address |
| `VAULT_TOKEN` | `root` | Dev-mode root token |
| `VAULT_SECRET_PATH` | `python-app` / `go-app` | Service's own path within the KV mount |

Both backends implement the same endpoint contract on top of Vault's
[KV v2 HTTP API](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2),
each under its own path (`/v1/secret/data/<service>/<key>`):

- `POST /secret` with body `{"key": "...", "value": "..."}` — store a secret
  (`201`, or `502` when Vault is unreachable).
- `GET /secret/{key}` — read a secret (`200` with `{"key", "value"}`, `404`
  when the key does not exist, `502` when Vault is unreachable).

The python-app uses the [hvac](https://github.com/hvac/hvac) client library
(`python-app/src/vault_client.py`); the go-app uses a small standard-library
HTTP client (`go-app/internal/vaultclient`). Secrets traffic never leaves the
cluster — only the demo endpoints are exposed via the backend ingress hosts.

## Per-service secret paths

Each service is namespaced to its own path under the KV mount:

```
secret/
├── python-app/<key>   ← only python-app reads/writes here
└── go-app/<key>       ← only go-app reads/writes here
```

A secret written through one backend is therefore invisible to the other —
`GET /secret/{key}` on the other backend answers 404. Today both services
still authenticate with the dev-mode root token; the per-service layout is
what makes real scoping possible later: one Vault policy per service, e.g.

```hcl
# Policy "python-app" — grants access to python-app's path only
path "secret/data/python-app/*" {
  capabilities = ["create", "update", "read"]
}
```

attached to a per-service token or Kubernetes-auth role instead of the root
token.

## Trying it out

```bash
# Store a secret through python-app (lands in secret/python-app/demo)
curl -X POST http://python.localhost/secret \
  -H 'Content-Type: application/json' \
  -d '{"key": "demo", "value": "hunter2"}'

# Read it back through python-app
curl http://python.localhost/secret/demo

# go-app cannot see it — its path is secret/go-app/ — so this answers 404
curl http://go.localhost/secret/demo
```

The Vault UI and API are also reachable from the host at
http://vault.localhost (log in with token `root`):

```bash
curl -H "X-Vault-Token: root" http://vault.localhost/v1/secret/data/python-app/demo
```

## Deployment

`./recreate-cluster.sh` applies `vault/k8s/` (Deployment, ClusterIP Service on
8200, Ingress for `vault.localhost`) before the backends, so Vault is up by the
time they receive traffic. The image is `hashicorp/vault:1.20` pulled from
Docker Hub; nothing is built locally.

## End-to-end coverage

`e2e/tests/test_vault_workflows.py` verifies Vault health, the write/read
roundtrip through each backend, the 404 contract, and that the per-service
paths isolate the backends from each other's secrets in both directions.
