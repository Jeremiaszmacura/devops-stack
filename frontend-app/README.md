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
- **Service**: `frontend-app-service` (NodePort 30070)
- **Access**: http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser
2. Select target application (Python or Go)
3. Choose endpoint to test
4. Set number of requests (1-100)
5. Click "Send Requests"
6. View results and statistics

## Architecture

The frontend-app uses an nginx reverse proxy to route API calls:
- `/api/python/*` → `python-app-service:8000/*`
- `/api/go/*` → `go-app-service:8080/*`

This avoids CORS issues and allows the frontend-app to communicate with backend services using Kubernetes service names.