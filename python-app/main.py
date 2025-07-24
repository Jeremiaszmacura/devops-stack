from fastapi import FastAPI, Response
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
import logging
from prometheus_config import PrometheusMiddleware


app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi-logger")


# Add the middleware
app.add_middleware(PrometheusMiddleware)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Hello from FastAPI"}

@app.get("/health")
def health():
    logger.info("Health endpoint called")
    return {"status": "healthy"}

@app.get("/error")
def error():
    logger.info("Error endpoint called")
    return Response(content="Internal Server Error", status_code=500)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)