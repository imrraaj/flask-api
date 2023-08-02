import datetime, os
from flask import Blueprint, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Reward, User, RewardType, UserRole
from main import db
from sqlalchemy import func
from utils import generate_reward_code, validate_schema
from mail.utils import create_email_body
from mail.mail import send_email
rewards_bp = Blueprint('rewards', __name__)


def send_bunch_mail(users_data):
    for user in users_data:
        print(f'sending mail to {user.name}')
        expiry = datetime.datetime.now() + datetime.timedelta(days=15)
        custom_code = generate_reward_code()
        new_reward = Reward(name="Birthday Discount", description="A gift for your birthday from us", custom_code=custom_code, expiry_date=expiry,user_id=user.id, discount_percentage=25)
        db.session.add(new_reward)
        db.session.commit()
        (mail_subject, mail_body) = create_email_body(RewardType.BIRTHDAY, user, new_reward)
        send_email(user.email, mail_subject, mail_body)




@rewards_bp.get('/view/all')
@jwt_required()
def view_all():
    current_user = get_jwt_identity()['id']
    rewards = Reward.query.filter_by(user_id = current_user).all()
    response = []
    for reward in rewards:
        response.append({
            'name': reward.name,
            'description': reward.description,
            'custom_code': reward.custom_code,
            'expiry_date': reward.expiry_date,
            'discount_percentage': reward.discount_percentage,
            'status': reward.status.name,
            'used_on': reward.used_on
        })
        
    return make_response(response, 200)



@rewards_bp.post('/send-birthday-discount')
@validate_schema({
    "type": "object",
    "properties": {
        "api_key": { "type": "string", "minLength": 1 },
    },
    "required": ["api_key"]
})
def send_birthday_discount():
    data = request.get_json()
    api_key = data['api_key']
    API_KEY = os.environ.get('API_KEY')
    if api_key is None or api_key != API_KEY:
        return make_response({'status': False , 'message': "The API key is Invalid"}, 400)
    users_with_birthday_today = User.query.filter(
                                    func.extract('day', User.birth_date) == datetime.datetime.now().day,
                                    func.extract('month', User.birth_date) == datetime.datetime.now().month).all()  
    send_bunch_mail(users_with_birthday_today)
    return make_response({'status': True }, 200)
