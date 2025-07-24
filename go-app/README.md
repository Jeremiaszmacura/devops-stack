# Go Application

This project is a simple Go application that includes a health check endpoint. It is structured to follow best practices for Go applications, with a clear separation of concerns.

## Project Structure

```
go-app
├── cmd
│   └── main.go          # Entry point of the application
├── internal
│   ├── handlers
│   │   └── health.go    # Health check handler
│   └── server
│       └── server.go     # Server setup and route definitions
├── kubernetes
│   └── go-app-deployment.yaml # Kubernetes deployment and service configuration
├── Dockerfile            # Dockerfile for building the application image
├── go.mod                # Go module definition
├── go.sum                # Dependency checksums
└── README.md             # Project documentation
```

## Getting Started

### Prerequisites

- Go 1.16 or later
- Docker (for building the Docker image)
- Kubernetes (for deploying the application)

### Building the Application

To build the application, navigate to the project directory and run:

```
go build -o go-app ./cmd/main.go
```

### Running the Application

You can run the application locally using:

```
go run ./cmd/main.go
```

The application will start on `http://localhost:8000`. You can check the health of the application by visiting `http://localhost:8000/health`.

### Docker

To build the Docker image, run:

```
docker build -t go-app:dev .
```

### Kubernetes Deployment

To deploy the application on a Kubernetes cluster, apply the deployment configuration:

```
kubectl apply -f kubernetes/go-app-deployment.yaml
```

This will create a deployment with one replica and expose the application via a service on port 8000.

## License

This project is licensed under the MIT License. See the LICENSE file for details.