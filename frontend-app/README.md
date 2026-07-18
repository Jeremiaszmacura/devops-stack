# Frontend App

A React.js frontend-app application for testing the Python and Go applications deployed in the Kubernetes cluster.

## Features

- 🎯 **Application Selection**: Choose between Python (FastAPI) and Go (Gin) applications
- 🌐 **Endpoint Testing**: Test all available endpoints (/, /health, /error, /redirect, /metrics)
- 📊 **Load Testing**: Send 1-100 concurrent requests to stress test applications
- 📈 **Real-time Statistics**: View success/failure rates and average response times
- 🔍 **Detailed Results**: See individual request results with status codes and response data
- 💅 **Modern UI**: Beautiful gradient design with responsive layout

## Development

### Prerequisites
- Node.js 18+
- npm or yarn

### Local Development
```bash
cd frontend-app
npm install
npm start
```

### Building for Production
```bash
npm run build
```

### Docker Build
```bash
docker build -t frontend-app:dev .
```

## Kubernetes Deployment

The application is deployed as:
- **Deployment**: `frontend-app-deployment` 
- **Service**: `frontend-app-service` (ClusterIP, exposed via `frontend-app-ingress`)
- **Access**: http://app.localhost

## Usage

1. Open http://app.localhost in your browser
2. Select target application (Python or Go)
3. Choose endpoint to test
4. Set number of requests (1-100)
5. Click "Send Requests"
6. View results and statistics

## Architecture

The frontend calls the backends directly on their ingress hosts:
- `http://python.localhost/*`
- `http://go.localhost/*`

These are cross-origin requests, so both backend Ingress resources enable CORS
(`nginx.ingress.kubernetes.io/enable-cors`).