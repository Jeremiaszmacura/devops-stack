# Python Application

A simple Python Web Application built with FastAPI to expose metrics and simulate traffic.

## Prerequisites

- Python 3.13 or higher
- Docker (optional, for containerized deployment)

## Running Without Docker

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or alternatively:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Access the Application

The application will be available at:
- http://localhost:8000

## Running With Docker

### 1. Build the Docker Image

```bash
docker build -t python-app/python-app:dev .
```

### 2. Run the Container

```bash
docker run -p 8000:8000 python-app/python-app:dev
```

### 3. Access the Application

The application will be available at:
- http://localhost:8000

## Development

For development with auto-reload:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

When the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc