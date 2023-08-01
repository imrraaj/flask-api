import random, string
from jsonschema import Draft4Validator
from functools import wraps
from flask import request,jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError


def validate_schema(schema):
    validator = Draft4Validator(schema)

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            input = request.get_json(force=True)
            errors = [error.message for error in validator.iter_errors(input)]
            if errors:
                response = jsonify(dict(success=False,
                                        message="invalid input",
                                        errors=errors))
                response.status_code = 406
                return response
            else:
                return fn(*args, **kwargs)
        return wrapped
    return wrapper
def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Verify JWT token in the request
            current_user = get_jwt_identity()
            current_role = current_user['role']

            if not current_role:
                raise NoAuthorizationError("Invalid token")

            if current_role == allowed_roles.name:
                return func(*args, **kwargs)

            return jsonify({'message': 'Unauthorized'}), 403

        return wrapper

    return decorator


def generate_reward_code(n = 8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


