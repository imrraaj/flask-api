# Endpoints

## POST /auth/login

**Description:** Authenticate user and retrieve access token.

### Request

```json
{
  "username": required,
  "password": required
}
```

### Response

**Status Code**: 201 Created.

```json
{
  "access_token": "Bearer eyJh...",
  "refresh_token": "Bearer eyJhbG...",
  "status": true
}
```

## POST /auth/register

**Description:** creates a user.

### Request

```json
{
  "name": required,
  "email": required,
  "password": required,
  "username": required,
  "birthdate": "YYYY-MM-DD" (required)
}
```

### Response

**Status Code**: 201 Created.

```json
{
  "message": "User created successfully!",
  "status": true
}
```

## GET /auth/protected

**Description:** To test whether a user is authenticated or not.

### Headers:

    "Authorization" : "Bearer eyJh..."

### Response

**Status Code**: 200 OK.

```json
{
  "message": "Protected endpoint. User ID: {'id': 6, 'role': 'USER'}"
}
```

## POST /auth/change-password

**Description:** changes the password of a user.

### Headers:

    "Authorization" : "Bearer eyJh..."

### Request

```json
{
  "password": required
}
```

### Response

**Status Code**: 201 Created.

```json
{
  "message": "Password changed successfully!",
  "status": true
}
```

## POST /auth/grant-user-permission

(**admin role required**)

**Description:** changes the permission granted to the user.

### Headers:

    "Authorization" : "Bearer eyJh..."

### Request

```json
{
  "username": required
}
```

### Response

**Status Code**: 201 Created.

```json
{
  "message": "User priviledge upgraded!!",
  "status": true
}
```

## POST /auth/revoke-user-permission

(**admin role required**)

**Description:** revokes the permission granted to the user.

### Headers:

    "Authorization" : "Bearer eyJh..."

### Request

```json
{
  "username": required
}
```

### Response

**Status Code**: 201 Created.

```json
{
  "message": "User priviledge upgraded!!",
  "status": true
}
```
