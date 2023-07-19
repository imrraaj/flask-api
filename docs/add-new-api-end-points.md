# How to add new API endpoints

To add new api end points here are some pre built modules/middlewares

## Public API Endpoint

This endpoint is publicly accessible and does not require any authentication.
You can use it by defining a normal Flask endpoint as shown below:

### Example

```python
@app.get('/')
def func():
    return "success"
```

## Endpoint for end users

This endpoint only accessible to users who are authenticate.
To create endpoint use `@jwt_required()` decorator.

### Example

```python
@app.post('/change-password')
@jwt_required()
def func():
    current_user = get_jwt_identity()
    # curent user has the fields by which the JWT token was signed
```

## Rate limiting the endpoint

This endpoint is rate limited which means it can be called only certain number of times defined.
To create endpoint use `@limiter.limit` decorator.

### Example

```python
@app.post('/change-password')
@limiter.limit("10/minute")
def func():
    pass
    # This endpoint can be only called 10 times every minute.
```

## Data validation for the endpoint

To validate the user inputted data, I am using json validator schema. If the data validation fails appropriate error and response will be thrown to the user (we do not need to worry about that)
To validate the data which has body, use `@validate_schema()` decorator.

### Example

```python
@app.post('/')
@validate_schema({
    "type": "object",
    "properties": {
        "password": { "type": "string", "minLength": 6, "maxLength": 80 }
    },
    "required": ["password"]
})
def func():
    # to access the data
    data = request.get_json()
    password = data.get('password')
    # This endpoint can be only called 10 times every minute.
```

## Rule based authentication

To check the whether the request came from the user or the admin or any other role we defined, we can use`@role_required()` decorator.
Only role that is defined in this decorator can access the endpoint. rest all will be unauthorized.

### Example

```python
@app.get('/dashboard')
@role_required(UserRole.ADMIN)
def dash():
    # Only JWT token with role as ADMIN can see this
    return "success"
```
