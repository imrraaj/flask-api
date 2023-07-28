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
from models import db, User, UserRole, Product, ProductImage, Category, Order, OrderDetail, OrderStatus
from validators import login_schema, register_schema

#app init
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/flask'
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




@app.post('/change-password')
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


@app.post('/grant-user-permission')
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


@app.post('/revoke-user-permission')
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

@app.get('/dashboard')
@role_required(UserRole.ADMIN)
def dash():
    return "success"


@app.get('/get-dummy-token-admin')
def get_token():
    access_token = create_access_token(identity={'id': 1, 'role': UserRole.ADMIN.name})
    return make_response(jsonify({'status': True, 'access_token': 'Bearer '+ access_token}), 201)





















@app.get('/products')
def get_all_products():
    products_with_images  = Product.query.outerjoin(ProductImage).all()
    result = []
    for product in products_with_images :
        result.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category_id': product.category_id,
            'images': [{'image_url': image.url, 'product_id': image.product_id} for image in product.images]
        })
    return jsonify(result)

@app.get('/products/<int:product_id>')
def get_single_product(product_id):
    product = Product.query.filter_by(id=product_id).outerjoin(ProductImage).first()
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'category_id': product.category_id,
        'image': [{'image_url': image.url, 'product_id': image.product_id} for image in product.images]
    })



@app.post('/products')
@role_required(UserRole.ADMIN)
@validate_schema({
    "type": "object",
    "properties": {
        "name": { "type": "string", "minLength": 4, "maxLength": 20 },
        "price": { "type": "number"},
        "description": { "type": "string", "minLength": 4},
        "category": { "type": "string", "minLength": 4, "maxLength": 20 },
        "images": { "type": "array", "minLength": 4 },
    },
    "required": ["name", "price","category","description"]
})
@role_required(UserRole.ADMIN)
def create_a_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    category_name = data.get('category')
    images = data.get('images')
    description = data.get('description')
    # check category if exists add the id
    # else create it.
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    new_prod = Product(name=name,price=price, description=description, category_id=category.id)
    db.session.add(new_prod)
    db.session.commit()
    for image in images:
        prod_images  = ProductImage(product_id=new_prod.id,url=image)
        db.session.add(prod_images)
    db.session.commit()
    return make_response(jsonify({'status': True }), 201)





######
@app.put('/products/<int:product_id>')
@role_required(UserRole.ADMIN)
@validate_schema({
    "type": "object",
    "properties": {
        "name": { "type": "string", "minLength": 4, "maxLength": 20 },
        "price": { "type": "number" },
        "description": { "type": "string", "minLength": 4},
        "category": { "type": "string", "minLength": 4, "maxLength": 20 },
        "images": { "type": "array", "minLength": 4 },
    }
})
@role_required(UserRole.ADMIN)
def update_a_product(product_id):
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    category_name = data.get('category')
    images = data.get('images')
    description = data.get('description')

    product =  Product.query.filter_by(id=product_id).outerjoin(ProductImage).first()
    print(name,price, description, category_name)
    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if description is not None:
        product.description = description


    if category_name is not None:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            return jsonify({'message': 'Category not found'}), 404
        product.category_id = category.id
    if images is not None:
        for image in images:
            prod_images  = ProductImage(product_id= product.id, url=image)
            db.session.add(prod_images)
    
    db.session.commit()
    return make_response(jsonify({'status': True }), 201)






@app.get('/category')
def get_all_category():
    db_categories  = Category.query.all()
    category_list = [{'id': category.id, 'name': category.name} for category in db_categories]
    print(category_list)
    return jsonify(category_list)

@app.delete('/category/<int:category_id>')
@role_required(UserRole.ADMIN)
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    else:
        return jsonify({'message': 'Category not found'}), 404

@app.post('/category')
@role_required(UserRole.ADMIN)
@validate_schema({
   "type": "object",
    "properties": {
        "name": { "type": "string", "minLength": 4, "maxLength": 20 },
    },
    "required": ["name"]
})
def add_single_category():
    data = request.get_json()
    name = data.get('name')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return make_response(jsonify({'status': True }), 201)









@app.post('/order')
@role_required(UserRole.USER)
@validate_schema({
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "properties": {
                "product_id": {"type": "integer"},
                "quantity": {"type": "integer", "minimum": 1}
            },
            "required": ["product_id", "quantity"]
        }
    },
    "required": ["items"]
})
def create_order():
    data = request.get_json()
    items = data.get('items')
    current_user = get_jwt_identity()['id']
    new_order = Order(user_id = current_user, total_amount=0)
    db.session.add(new_order)
    db.session.commit()


    for item in items:
        prod_id = item['product_id']
        quantity = item['quantity']

        #check if the product even exists or not
        prod_exists  = Product.query.filter_by(id=prod_id).first()
        if not prod_exists:
            return make_response(jsonify({'status': False, 'error': f"Product id: {prod_id} doesn't exist"}), 401)
        
        price = prod_exists.price * quantity
        new_order.total_amount = new_order.total_amount + price

        new_order_details = OrderDetail(order_id=new_order.id, product_id=prod_id, quantity=quantity,price = price)
        db.session.add(new_order_details)

    db.session.commit()
    return make_response(jsonify({'status': True, 'total_amount': new_order.total_amount}), 201)


@app.get('/orders')
@role_required(UserRole.USER)
def get_all_order():

    user_id = get_jwt_identity()['id']
    user_orders  = Order.query.filter_by(user_id = user_id).outerjoin(OrderDetail).all()
    orders_list = []
    for single_order in user_orders:
        orders_list.append(
            {'id': single_order.id, 'order_date': single_order.order_date, 'total_amount': single_order.total_amount ,
            'order_status': single_order.status.value,
             'order_details': [{'product_id': od.product_id, 'quantity': od.quantity, 'price': od.price} for od in single_order.order_details]
            }
        )
    return jsonify({ 'status': True,  'orders': orders_list }), 200






#Change the status
@app.get('/change-order-status/<int:id>')
@role_required(UserRole.ADMIN)
def change_order_status(id):
    user_order  = Order.query.filter_by(id = id).first()
    
    if user_order.status == OrderStatus.ORDERED:
        user_order.status = OrderStatus.DELIVERY

    if user_order.status == OrderStatus.DELIVERY:
        user_order.status = OrderStatus.PAID
        
    db.session.commit()
    return jsonify({ 'status': True, }), 200






@app.get('/d')
def delete():
    o = Order.query.where(True).all()
    db.session.delete(o)
    db.session.commit()
    return {}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)