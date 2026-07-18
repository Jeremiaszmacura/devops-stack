from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel

from logger import logger
from vault_client import SecretNotFoundError, VaultClient, VaultClientError, get_vault_client

router = APIRouter()


class SecretPayload(BaseModel):
    """Request body for storing a secret.

    Attributes:
        key: Secret path within Vault's KV v2 mount.
        value: Secret value to store.
    """

    key: str
    value: str


@router.get("/")
def root():
    """Return a hello message identifying the service."""
    logger.info("Root endpoint called")
    return {"message": "Hello from FastAPI"}


@router.get("/health")
def health():
    """Report service health for probes and monitoring."""
    logger.info("Health endpoint called")
    return {"status": "healthy"}


@router.get("/error")
def error():
    """Return a simulated 500 response for testing error monitoring."""
    logger.info("Error endpoint called")
    return Response(content="Internal Server Error", status_code=500)


@router.get("/redirect")
def redirect():
    """Redirect the client to the /health endpoint."""
    logger.info("Redirect endpoint called")
    return RedirectResponse(url="/health", status_code=302)


@router.post("/secret", status_code=201)
def write_secret(payload: SecretPayload, vault: VaultClient = Depends(get_vault_client)):
    """Store a secret in Vault under the given key."""
    logger.info(f"Write secret endpoint called for key: {payload.key}")
    try:
        vault.write_secret(payload.key, payload.value)
    except VaultClientError:
        raise HTTPException(status_code=502, detail="vault request failed")
    return {"key": payload.key, "status": "stored"}


@router.get("/secret/{key}")
def read_secret(key: str, vault: VaultClient = Depends(get_vault_client)):
    """Read a secret from Vault by key."""
    logger.info(f"Read secret endpoint called for key: {key}")
    try:
        value = vault.read_secret(key)
    except SecretNotFoundError:
        raise HTTPException(status_code=404, detail="secret not found")
    except VaultClientError:
        raise HTTPException(status_code=502, detail="vault request failed")
    return {"key": key, "value": value}


@router.get("/metrics")
def metrics():
    """Expose Prometheus metrics in text exposition format."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
