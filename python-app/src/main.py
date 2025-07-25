from fastapi import FastAPI
from prometheus_config import PrometheusMiddleware
from endpoints import router

app = FastAPI()

# Add the middleware
app.add_middleware(PrometheusMiddleware)

# Include the router
app.include_router(router)
