# Adding a New Service

This project auto-discovers Go and Python services from the repo root `Makefile` —
no Makefile changes are needed when you add a new one. Follow the conventions
below so `make test`, `make lint`, and the Claude Code hooks pick it up correctly.

## Go services

A directory is discovered as a Go service if it contains a `go.mod`.

1. Create the service directory with its own `go.mod`.
2. That's it — `make build`, `make test-unit-go`, and `make lint-go` will find it
   automatically via `GO_SERVICES` in the root `Makefile`.

`make lint-go` runs `golangci-lint run --fix` inside each service directory;
`make test-unit-go` runs `go test ./...` inside each. No shared config to copy.

## Python services

A directory is discovered as a Python service if it contains a `tox.ini`.

Lint rules and dev-tool versions are centralized at the repo root so they don't
get duplicated or drift per service:

- `/.pre-commit-config.yaml` — shared black/bandit/hygiene hooks
- `/requirements-dev.txt` — pinned `coverage`, `pre_commit`, `tox` versions

To add a new Python service:

1. Create the service directory with:
   - `requirements.txt` — the service's own runtime dependencies
   - `requirements-dev.txt` containing exactly:
     ```
     -r requirements.txt
     -r ../requirements-dev.txt
     ```
   - `tox.ini` — copy an existing service's `tox.ini` (e.g. `python-app/tox.ini`)
     unchanged; it already points at `../.pre-commit-config.yaml`
   - `tests/` with an `__init__.py` and `test_*.py` files (unittest discovery
     requires the `__init__.py` or tests silently won't be found)
   - `.coveragerc` if you need custom coverage `omit` paths — this one stays
     per-service since it's path-specific
2. Add the new directory name to the `files:` regex at the top of the root
   `.pre-commit-config.yaml`, e.g. `files: ^(python-app|your-new-service)/`.
   This is the **only** shared-config edit required.

Do not create a per-service `.pre-commit-config.yaml` — it would run
`pre-commit run --all-files` scoped to the whole repo by default, since
pre-commit always resolves paths from the git root regardless of cwd. Scoping
must happen via the `files:` regex in the shared root config.

## Verifying

```sh
make lint          # lint-go + lint-python across all discovered services
make test-unit      # test-unit-go + test-unit-python across all discovered services
```

Both commands stop at the first failing service (`||` chained), so during
local development it can help to run the language-specific target for just
the service you're working on, e.g. `cd your-service && tox -e tests`.
