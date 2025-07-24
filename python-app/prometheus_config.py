from prometheus_client import Counter, Histogram
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total", 
    "Total number of HTTP requests", 
    ["method", "endpoint", "status_code"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds", 
    "HTTP request duration in seconds", 
    ["method", "endpoint"]
)

RESPONSE_STATUS = Counter(
    "http_responses_by_status_total", 
    "HTTP responses by status code", 
    ["status_class"]
)

# Separate metric for monitoring requests
MONITORING_REQUESTS = Counter(
    "monitoring_requests_total",
    "Total number of monitoring/metrics requests",
    ["endpoint", "user_agent"]
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Extract endpoint path
        endpoint = request.url.path
        method = request.method
        status_code = str(response.status_code)
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Increment counters for ALL requests (including /metrics)
        if endpoint not in ["/metrics", "/health"]:
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
            REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(process_time)
        
            # Status class (2XX, 3XX, 4XX, 5XX)
            status_class = f"{status_code[0]}XX"
            RESPONSE_STATUS.labels(status_class=status_class).inc()
        
        # Separate tracking for monitoring endpoints
        if endpoint in ["/metrics", "/health"]:
            # Extract simplified user agent (e.g., "Prometheus" from "Prometheus/2.x.x")
            simplified_ua = user_agent.split("/")[0] if "/" in user_agent else user_agent
            MONITORING_REQUESTS.labels(endpoint=endpoint, user_agent=simplified_ua).inc()
        
        return response