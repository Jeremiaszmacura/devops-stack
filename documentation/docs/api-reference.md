# API Reference

## Overview
This document provides detailed information about the API endpoints available in the project.

## Endpoints

### GET /api/v1/resource
- **Description**: Retrieves a list of resources.
- **Request**: 
  - Headers: 
    - Authorization: Bearer `<token>`
- **Response**:
  - Status Code: 200 OK
  - Body: 
    ```json
    {
      "resources": [
        {
          "id": "1",
          "name": "Resource 1"
        },
        {
          "id": "2",
          "name": "Resource 2"
        }
      ]
    }
    ```

### POST /api/v1/resource
- **Description**: Creates a new resource.
- **Request**:
  - Headers: 
    - Authorization: Bearer `<token>`
  - Body:
    ```json
    {
      "name": "New Resource"
    }
    ```
- **Response**:
  - Status Code: 201 Created
  - Body: 
    ```json
    {
      "id": "3",
      "name": "New Resource"
    }
    ```

### GET /api/v1/resource/{id}
- **Description**: Retrieves a specific resource by ID.
- **Request**:
  - Headers: 
    - Authorization: Bearer `<token>`
- **Response**:
  - Status Code: 200 OK
  - Body: 
    ```json
    {
      "id": "1",
      "name": "Resource 1"
    }
    ```

### PUT /api/v1/resource/{id}
- **Description**: Updates a specific resource by ID.
- **Request**:
  - Headers: 
    - Authorization: Bearer `<token>`
  - Body:
    ```json
    {
      "name": "Updated Resource"
    }
    ```
- **Response**:
  - Status Code: 200 OK
  - Body: 
    ```json
    {
      "id": "1",
      "name": "Updated Resource"
    }
    ```

### DELETE /api/v1/resource/{id}
- **Description**: Deletes a specific resource by ID.
- **Request**:
  - Headers: 
    - Authorization: Bearer `<token>`
- **Response**:
  - Status Code: 204 No Content

## Error Handling
- **400 Bad Request**: Returned when the request is malformed.
- **401 Unauthorized**: Returned when authentication fails.
- **404 Not Found**: Returned when the requested resource does not exist.
- **500 Internal Server Error**: Returned when an unexpected error occurs.