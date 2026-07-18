from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from logger import logger

router = APIRouter()


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


@router.get("/metrics")
def metrics():
    """Expose Prometheus metrics in text exposition format."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
