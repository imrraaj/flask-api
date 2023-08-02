from flask import Blueprint, request, jsonify, make_response
from utils import validate_schema, role_required
from main import db
from models.models import Category, UserRole


category_bp = Blueprint('category', __name__)

@category_bp.get('/view/all')
def get_all_category():
    db_categories  = Category.query.all()
    category_list = [{'id': category.id, 'name': category.name} for category in db_categories]
    print(category_list)
    return jsonify(category_list)

@category_bp.delete('/delete/<int:category_id>')
@role_required(UserRole.ADMIN)
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    else:
        return jsonify({'message': 'Category not found'}), 404

@category_bp.post('/add')
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



