from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from logger import logger

router = APIRouter()

@router.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Hello from FastAPI"}

@router.get("/health")
def health():
    logger.info("Health endpoint called")
    return {"status": "healthy"}

@router.get("/error")
def error():
    logger.info("Error endpoint called")
    return Response(content="Internal Server Error", status_code=500)

@router.get("/redirect")
def redirect():
    logger.info("Redirect endpoint called")
    return Response(content="Redirecting...", status_code=302, headers={"Location": "/health"})

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)