# API Documentation

## Introduction

This API provides authentication and user management functionality.

Base URL: `http://localhost:5000`

## Endpoints

### Login [POST /login]

**Description:** Authenticate user and retrieve access token.
**Rate Limit:** 10 requests per minute.

#### Request

- **Body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

#### Response

- **Success Response**

  **Status Code**: 201 Created.

  **Content-Type**: application/json

  ```json
  {
    "status": true,
    "access_token": "Bearer <access_token>"
  }
  ```

- **Error Response**

**Status Code**: 401 Unauthorized.

**Content-Type**: application/json

```json
{
  "status": false,
  "message": "Invalid username or password."
}
```
