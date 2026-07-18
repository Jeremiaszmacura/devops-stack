# Vault

HashiCorp Vault is the cluster's shared secret store. Both sample backends
(python-app and go-app) write and read secrets in it through their `/secret`
endpoints.

Vault runs in **dev mode** (`vault server -dev`): in-memory storage (secrets
are lost on pod restart), auto-initialized and unsealed, root token fixed to
`root`. Fine for this playground, unsuitable for anything else.

## Secret path layout

A one-shot `vault-configure` Job (`vault/k8s/vault-configure-job.yaml`,
idempotent) enables two KV v2 mounts once Vault is reachable:

```
services/                      (KV v2 mount)
├── python-app/<key>   ← only python-app reads/writes here
└── go-app/<key>       ← only go-app reads/writes here
infra/                         (KV v2 mount, reserved for future infra secrets)
```

(The `secret/` mount dev mode pre-creates is unused.) Each backend gets its
own path via `VAULT_SECRET_PATH` (`python-app` / `go-app`), so one backend can
never read another's secrets — `GET /secret/{key}` answers 404 across
services.

Both services currently authenticate with the dev-mode root token; the
per-service path is what makes real scoping possible later — one Vault policy
per service, e.g.:

```hcl
# Policy "python-app" — grants access to python-app's path only
path "services/data/python-app/*" {
  capabilities = ["create", "update", "read"]
}
```

attached to a per-service token or Kubernetes-auth role instead of the root
token.

## How the backends use it

Each backend Deployment sets `VAULT_ADDR` (`http://vault-service:8200`),
`VAULT_TOKEN` (`root`), and `VAULT_SECRET_PATH`, and implements the same
endpoint contract on top of Vault's
[KV v2 HTTP API](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2)
(`/v1/services/data/<service>/<key>`):

- `POST /secret` `{"key", "value"}` — store a secret (`201`, `502` if Vault fails)
- `GET /secret/{key}` — read a secret (`200`, `404` if missing, `502` if Vault fails)

python-app uses [hvac](https://github.com/hvac/hvac)
(`python-app/src/vault_client.py`); go-app uses a small stdlib HTTP client
(`go-app/internal/vaultclient`).

## Trying it out

```bash
curl -X POST http://python.localhost/secret \
  -H 'Content-Type: application/json' -d '{"key": "demo", "value": "hunter2"}'

curl http://python.localhost/secret/demo   # 200 — same backend
curl http://go.localhost/secret/demo       # 404 — different path in services/
```

## Deployment & testing

`./recreate-cluster.sh` applies `vault/k8s/` (Deployment, Service, Ingress for
`vault.localhost`, `vault-configure` Job) before the backends and waits for
the Job to complete. `e2e/tests/test_vault_workflows.py` covers Vault health,
both mounts existing, the write/read/404 contract, and cross-service
isolation.
