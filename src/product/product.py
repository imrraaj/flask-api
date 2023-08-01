from flask import Blueprint, request, jsonify, make_response
from utils import validate_schema, role_required
from main import db
from models.models import Product, ProductImage, Category, UserRole


products_bp = Blueprint('products', __name__)

@products_bp.get('/view/all')
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

@products_bp.get('/view/<int:product_id>')
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



@products_bp.post('/add')
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
@products_bp.put('/edit/<int:product_id>')
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

