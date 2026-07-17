from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_config import PrometheusMiddleware
from endpoints import router
from logger import configure_logging, get_logs_dir, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logs_file_path = configure_logging(get_logs_dir())
    logger.info(f"Logger configured. Logs path: {logs_file_path}")
    yield


app = FastAPI(lifespan=lifespan)

# Add the middleware
app.add_middleware(PrometheusMiddleware)

# Include the router
app.include_router(router)
