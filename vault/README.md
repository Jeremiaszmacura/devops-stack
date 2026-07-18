# Vault

HashiCorp Vault in **dev mode** — shared secret store for python-app and
go-app, each scoped to its own path (`services/<service>/...`). In-memory
storage, root token `root`. Full details:
[documentation/docs/vault.md](../documentation/docs/vault.md).

- UI/API: http://vault.localhost (token `root`)
- Redeploy: `kubectl apply -f vault/k8s/`
