"""End-to-end tests of the Vault-backed secret workflow.

Both backends expose the same /secret endpoints (see design.md) but each
stores its secrets under its own path in the shared dev-mode Vault
(secret/<service>/<key>), so one backend must never see another backend's
keys. Keys are randomized per test run because dev-mode Vault keeps state
for the lifetime of its pod.
"""

import uuid

import requests

from cluster import BACKENDS, REQUEST_TIMEOUT_SECONDS, VAULT_URL


def unique_key(prefix):
    """Return a secret key that no earlier test run can have written.

    Args:
        prefix: Human-readable prefix identifying the test.

    Returns:
        A key string of the form ``<prefix>-<random hex>``.
    """
    return f"{prefix}-{uuid.uuid4().hex}"


def test_vault_is_initialized_and_unsealed():
    """Vault's health endpoint reports a ready dev-mode server."""
    response = requests.get(f"{VAULT_URL}/v1/sys/health", timeout=REQUEST_TIMEOUT_SECONDS)
    assert response.status_code == 200
    health = response.json()
    assert health["initialized"] is True
    assert health["sealed"] is False


def test_secret_write_read_roundtrip(backend):
    """A secret stored via POST /secret comes back via GET /secret/{key}."""
    key = unique_key(f"e2e-{backend.name}")

    write = requests.post(
        f"{backend.base_url}/secret",
        json={"key": key, "value": "hunter2"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert write.status_code == 201

    read = requests.get(f"{backend.base_url}/secret/{key}", timeout=REQUEST_TIMEOUT_SECONDS)
    assert read.status_code == 200
    assert read.json() == {"key": key, "value": "hunter2"}


def test_reading_missing_secret_returns_not_found(backend):
    """GET /secret/{key} answers 404 for a key that was never written."""
    response = requests.get(
        f"{backend.base_url}/secret/{unique_key('e2e-missing')}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    assert response.status_code == 404


def test_secret_paths_are_isolated_between_backends():
    """A secret written through one backend is invisible to the other.

    Each service keeps its secrets under its own KV path
    (secret/python-app/... vs secret/go-app/...), so reading the same key
    through the other backend must answer 404 in both directions.
    """
    python_app, go_app = BACKENDS

    for writer, reader in ((python_app, go_app), (go_app, python_app)):
        key = unique_key("e2e-isolated")
        write = requests.post(
            f"{writer.base_url}/secret",
            json={"key": key, "value": f"only-for-{writer.name}"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        assert write.status_code == 201

        read = requests.get(f"{reader.base_url}/secret/{key}", timeout=REQUEST_TIMEOUT_SECONDS)
        assert read.status_code == 404
