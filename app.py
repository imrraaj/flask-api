from functools import wraps
from jsonschema import Draft4Validator
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate


from sqlalchemy import or_

# Data models
from models import db, User, user_roles, UserRole
from validators import login_schema, register_schema

#app init
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['SECRET_KEY'] = 'any secret string'

# bind the app
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"],
    storage_uri="memory://",
)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)



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
def role_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Verify JWT token in the request
            current_user = get_jwt_identity()
            print(current_user)
            current_role = current_user['role']

            if not current_role:
                raise NoAuthorizationError("Invalid token")

            if current_role in user_roles:
                allowed_rules = user_roles[current_role]
                if any(rule in allowed_rules for rule in allowed_roles):
                    return func(*args, **kwargs)

            return jsonify({'message': 'Unauthorized'}), 403

        return wrapper

    return decorator







@app.post('/login')
@limiter.limit("10/minute") 
@validate_schema(login_schema)
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role.name})
        return make_response(jsonify({'status':True,'access_token': 'Bearer '+ access_token}), 201)
    else:
        return make_response(jsonify({'status':False, 'message': 'Invalid username or password.'}), 401)



@app.post('/register')
@limiter.limit("10/minute") 
@validate_schema(register_schema)
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    avatar = data.get('avatar')
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
    does_user_exists = db.session.execute(db.select(User).where(or_(User.username == username, User.email == email))).first()
    if does_user_exists:
        return make_response(jsonify({'status':False, 'message': 'Account already exists with the provided email and username. Please Login'}), 401)  
    user = User(name=name, avatar=avatar, email=email, username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'User created successfully!'}), 201)
        

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return make_response(jsonify({'message': f'Protected endpoint. User ID: {current_user}'}), 200)




@app.route('/change-password', methods=['POST'])
@limiter.limit("10/minute") 
@jwt_required()
@validate_schema({
    "type": "object",
    "properties": {
        "password": { "type": "string", "minLength": 6, "maxLength": 80 }
    },
    "required": ["password"]
})
def change_password():
    current_user = get_jwt_identity()
    data = request.get_json()
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
    user = db.session.execute(db.select(User).where(User.id == current_user)).first()[0]
    print(password, hashed_password)
    if not user:
        return make_response(jsonify({'status':False, 'message': 'Please Login'}), 401)
    user.password = hashed_password
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'Password changed successfully!'}), 201)



# @app.get('/get-dummy-token-admin')
# def get_token():
#     access_token = create_access_token(identity={'id': 1, 'role': UserRole.ADMIN.name})
#     return make_response(jsonify({'status': True, 'access_token': 'Bearer '+ access_token}), 201)



@app.post('/grant-user-permission')
@validate_schema({
    "type": "object",
    "properties": {
        "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    },
    "required": ["username"]
})
@role_required('write')
def promote_user():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response(jsonify({'status':False, 'message': 'User does not exits'}), 401)
    user.role = UserRole.ADMIN
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'User priviledge upgraded!!'}), 201)


@app.post('/revoke-user-permission')
@validate_schema({
    "type": "object",
    "properties": {
        "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    },
    "required": ["username"]
})
@role_required('write')
def revoke_user():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response(jsonify({'status':False, 'message': 'User does not exits'}), 401)
    user.role = UserRole.USER
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'User priviledge upgraded!!'}), 201)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)