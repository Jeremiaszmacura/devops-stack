# Go Application

A Go web application built with Gin framework to expose Prometheus metrics and simulate traffic patterns.

## Features

- HTTP endpoints with Prometheus metrics
- Middleware for automatic request tracking
- Health checks and error simulation
- Compatible with Prometheus scraping

## Endpoints

- `GET /` - Home endpoint
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /error` - Simulated error (returns 500)
- `GET /redirect` - Redirect to /health

## Metrics Exposed

- `http_requests_total` - Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds` - Request duration histogram
- `http_responses_by_status_total` - Response count by status class (2XX, 4XX, etc.)
- `monitoring_requests_total` - Separate tracking for /metrics and /health endpoints

## Development

### Running Locally

```bash
go mod tidy
go run cmd/main.go
```

The application will be available at http://localhost:8080

### Running with Docker

```bash
docker build -t go-app:dev .
docker run -p 8080:8080 go-app:dev
```

### Deploying to Kubernetes

```bash
# Build and load image to kind cluster
docker build -t go-app:dev .
kind load docker-image go-app:dev --name sample-cluster

# Deploy to cluster
kubectl apply -f k8s/

# Access via NodePort
curl http://localhost:31000
```

## Prometheus Integration

The app automatically exposes metrics on `/metrics` endpoint in Prometheus format. Add this job to your Prometheus configuration:

```yaml
- job_name: 'go-app'
  static_configs:
    - targets: ['go-app-service:8080']
  metrics_path: '/metrics'
  scrape_interval: 5s
```