# Vault

HashiCorp Vault running in **dev mode**, used as the shared secret store for
the sample backends: python-app and go-app write and read secrets through
their `/secret` endpoints, which talk to Vault's KV v2 secrets engine. Each
service keeps its secrets under its own path (`secret/python-app/...`,
`secret/go-app/...`) so Vault policies can scope each service to its own
path later.

## Dev mode

Dev mode keeps the component fit for this local playground and nothing else:

- In-memory storage — all secrets are lost when the pod restarts.
- Automatically initialized and unsealed.
- KV v2 secrets engine pre-mounted at `secret/`.
- Root token is fixed to `root` (`VAULT_DEV_ROOT_TOKEN_ID`).

## Access

- In-cluster API: `http://vault-service:8200` (used by the backends via the
  `VAULT_ADDR` / `VAULT_TOKEN` / `VAULT_SECRET_PATH` env vars in their
  Deployments).
- From the host: http://vault.localhost — Vault UI and API through
  ingress-nginx. Log in with token `root`.

## Example

```bash
# Write a secret into python-app's path through Vault's API
curl -H "X-Vault-Token: root" \
  -X POST -d '{"data": {"value": "hunter2"}}' \
  http://vault.localhost/v1/secret/data/python-app/demo

# Read it back
curl -H "X-Vault-Token: root" http://vault.localhost/v1/secret/data/python-app/demo
```

## Deployment

Applied by `./recreate-cluster.sh` together with the other components:

```bash
kubectl apply -f vault/k8s/
```
