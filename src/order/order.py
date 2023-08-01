import datetime
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import validate_schema, role_required, generate_reward_code
from main import db
from models.models import *

from mail.mail import send_email
from mail.utils import create_email_body

orders_bp = Blueprint('orders', __name__)

@orders_bp.post('/create')
@jwt_required()
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
        },
        "reward_code": { "type": "string", "minLength": 8, "maxLength": 8 },
    },
    "required": ["items"]
})
def create_order():
    data = request.get_json()
    items = data.get('items')
    reward_code = data.get('reward_code')
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


    if reward_code is not None:
        reward_exists  = Reward.query.filter_by(user_id = current_user, custom_code=reward_code).first()
        
        
        if reward_exists is not None and reward_exists.status == RewardStatus.NOT_REDEEMED:
            # check if it is valid
            current_date = datetime.datetime.now().date()
            if reward_exists.expiry_date >= current_date:
                discounted_total_amount = (new_order.total_amount * reward_exists.discount_percentage) / 100 
                actual_total_amount = new_order.total_amount
                new_order.total_amount -= discounted_total_amount
                payable_amount = actual_total_amount - discounted_total_amount
                reward_exists.status = RewardStatus.REDEEMED
                reward_exists.used_on = datetime.datetime.now()
                db.session.commit()
                return make_response(jsonify({'status': True, 
                                              'total_amount': actual_total_amount, 
                                              'reward': False, 
                                              'discounted_total_amount':discounted_total_amount,
                                              'net_payable_amount': payable_amount
                                              }), 201)
        
        
        return make_response({'status': False, 'message':"The reward code is not valid"}, 403)
    
    db.session.commit()

    
    if not reward_code and new_order.total_amount > 5000:
        expiry = datetime.datetime.now() + datetime.timedelta(days=15)
        custom_code = generate_reward_code()
        new_reward = Reward(name="Normal Discount", description="On the purchase of more than 5000", custom_code=custom_code, expiry_date=expiry,user_id=current_user, discount_percentage=10)
        db.session.add(new_reward)
        db.session.commit()

        current_user_data = User.query.filter_by(id=current_user).first()
        (mail_subject, mail_body) = create_email_body(RewardType.DEFAULT, current_user_data, new_reward)
        send_email(current_user_data.email, mail_subject, mail_body)
        return make_response(jsonify({'status': True, 
                                      'total_amount': new_order.total_amount, 
                                      'reward': True, 
                                      'reward_code': new_reward.custom_code,
                                      'net_payable_amount': new_order.total_amount 
                                      }), 201)
    


@orders_bp.get('/view/all')
@jwt_required()
def get_all_order():

    user_id = get_jwt_identity()['id']
    user_orders  = Order.query.filter_by(user_id = user_id).outerjoin(OrderDetail).all()
    orders_list = []
    for single_order in user_orders:
        orders_list.append(
            {'id': single_order.id, 'order_date': single_order.order_date, 'total_amount': single_order.total_amount,
            'order_status': single_order.status.name,
             'order_details': [{'product_id': od.product_id, 'quantity': od.quantity, 'price': od.price} for od in single_order.order_details]
            }
        )
    return jsonify({ 'status': True,  'orders': orders_list }), 200






#Change the status
@orders_bp.get('/status/<int:id>')
@role_required(UserRole.ADMIN)
def change_order_status(id):
    user_order  = Order.query.filter_by(id = id).first()
    if user_order is None:
        return jsonify({'status' : False, 'Message': "order does not exists" })
    if user_order.status == OrderStatus.ORDERED:
        user_order.status = OrderStatus.DELIVERY

    if user_order.status == OrderStatus.DELIVERY:
        user_order.status = OrderStatus.PAID
        
    db.session.commit()
    return jsonify({ 'status': True, }), 200

