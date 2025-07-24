# Getting Started with MkDocs Kubernetes Project

Welcome to the MkDocs Kubernetes project! This guide will help you set up the project and get started with building and deploying your documentation.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6 or higher
- pip (Python package installer)
- Docker (for containerization)
- kubectl (for interacting with your Kubernetes cluster)
- A Kubernetes cluster (local or cloud-based)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/microsoft/vscode-remote-try-rust.git
   cd vscode-remote-try-rust/mkdocs-k8s-project
   ```

2. **Install the required Python packages:**

   It is recommended to use a virtual environment. You can create one using the following commands:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Then install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Building the Documentation

To build the documentation, run the following command:

```bash
mkdocs build
```

This will generate the static site in the `site` directory.

## Running the Documentation Locally

You can preview the documentation locally by running:

```bash
mkdocs serve
```

This will start a local server at `http://127.0.0.1:8000`, where you can view your documentation.

## Deploying to Kubernetes

1. **Build the Docker image:**

   Run the following command to build the Docker image:

   ```bash
   docker build -t mkdocs-k8s-project .
   ```

2. **Deploy to your Kubernetes cluster:**

   Apply the Kubernetes deployment and service configurations:

   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

3. **Access the application:**

   If you have set up ingress, you can access your documentation through the configured domain. Otherwise, you can port-forward the service to access it locally:

   ```bash
   kubectl port-forward service/mkdocs-k8s-project 8000:80
   ```

   Then visit `http://localhost:8000` in your browser.

## Conclusion

You are now set up to use the MkDocs Kubernetes project! For more detailed information, check out the [API Reference](api-reference.md) and other sections of the documentation. Happy documenting!