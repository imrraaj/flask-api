from flask import Blueprint, current_app, request, jsonify, make_response
from utils import validate_schema, role_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token


from main import limiter, bcrypt, db
from models.models import User, UserRole
from sqlalchemy import or_

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/login')
@validate_schema({
    "type": "object",
    "properties": {
    "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    "password": { "type": "string", "minLength": 6, "maxLength": 80 }
    },
    "required": ["username", "password"]
})
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role.name})
        refresh_token = create_refresh_token(identity={'id': user.id, 'role': user.role.name})
        return make_response(jsonify({'status':True, 'access_token': 'Bearer '+ access_token, 'refresh_token': 'Bearer '+ refresh_token}), 201)
    else:
        return make_response(jsonify({'status':False, 'message': 'Invalid username or password.'}), 401)



@auth_bp.post('/register')
@validate_schema({
    "type": "object",
    "properties": {
    "name": { "type": "string" },
    "email": {   "type": "string", 
                "pattern": "^\\S+@\\S+\\.\\S+$",
                "format": "email",
                "minLength": 6,
                "maxLength": 127
            },
    "avatar": { "type": "string" },
    "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    "password": { "type": "string", "minLength": 6, "maxLength": 80 },
    "birthdate": { "type": "string", "format": "date" }
    },
    "required": ["name", "email", "username", "password", "birthdate"]
})
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    avatar = data.get('avatar')
    username = data.get('username')
    password = data.get('password')
    birthdate = data.get('birthdate')
    hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
    does_user_exists = db.session.execute(db.select(User).where(or_(User.username == username, User.email == email))).first()
    if does_user_exists:
        return make_response(jsonify({'status':False, 'message': 'Account already exists with the provided email and username. Please Login'}), 401)  
    user = User(name=name, avatar=avatar, email=email, username=username, password=hashed_password,birth_date=birthdate)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'User created successfully!'}), 201)
        

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return make_response(jsonify({'message': f'Protected endpoint. User ID: {current_user}'}), 200)




@auth_bp.post('/change-password')
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
    current_user = get_jwt_identity()['id']
    data = request.get_json()
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
    user = db.session.execute(db.select(User).where(User.id == current_user)).first()[0]
    if not user:
        return make_response(jsonify({'status':False, 'message': 'Please Login'}), 401)
    user.password = hashed_password
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'Password changed successfully!'}), 201)


@auth_bp.post('/grant-user-permission')
@validate_schema({
    "type": "object",
    "properties": {
        "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    },
    "required": ["username"]
})
@role_required(UserRole.ADMIN)
def promote_user():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response(jsonify({'status':False, 'message': 'User does not exits'}), 401)
    user.role = UserRole.ADMIN
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'User priviledge upgraded!!'}), 201)


@auth_bp.post('/revoke-user-permission')
@validate_schema({
    "type": "object",
    "properties": {
        "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    },
    "required": ["username"]
})
@role_required(UserRole.ADMIN)
def revoke_user():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response(jsonify({'status':False, 'message': 'User does not exits'}), 401)
    user.role = UserRole.USER
    db.session.commit()
    return make_response(jsonify({'status': True, 'message': 'User priviledge upgraded!!'}), 201)

@auth_bp.get('/dashboard')
@role_required(UserRole.ADMIN)
def dash():
    return "success"


@auth_bp.get('/get-dummy-token-admin')
def get_token():
    access_token = create_access_token(identity={'id': 1, 'role': UserRole.ADMIN.name})
    return make_response(jsonify({'status': True, 'access_token': 'Bearer '+ access_token}), 201)



