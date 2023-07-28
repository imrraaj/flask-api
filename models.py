from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from enum import Enum
db = SQLAlchemy()


class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    GUEST = 'GUEST'
class OrderStatus(Enum):
    ORDERED = 'ORDERED'
    CANCELLED = 'CANCELLED',
    PAID = 'PAID',
    DELIVERY = 'DELIVERY'
class RewardStatus(Enum):
    NOT_REDEEMED = 'NOT_REDEEMED',
    REDEEMED = 'REDEEMED',
    EXPIRED = 'EXPIRED'

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    avatar = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    rewards = db.relationship('Reward', backref='user', lazy=True)

    
    def __init__(self, name, username, password, email, avatar):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
    def __repr__(self):
        return f'<User {self.id}: {self.name} {self.username}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    images = db.relationship('ProductImage', backref='product', lazy='joined')

    def __init__(self, name, price, description, category_id):
        self.name = name
        self.price = price
        self.description = description
        self.category_id = category_id



class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, url, product_id):
        self.url = url
        self.product_id = product_id
    
    def __repr__(self):
        return f"ProductImage('{self.product_id}', '{self.url}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __init__(self, name):
        self.name = name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    total_amount = db.Column(db.Float, nullable=False)
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.ORDERED)
    def __init__(self, user_id, total_amount):
        self.user_id = user_id
        self.total_amount = total_amount

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    discount_percentage = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    custom_code = db.Column(db.String(8), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    used_on = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(db.Enum(RewardStatus), default=RewardStatus.NOT_REDEEMED)


    def __init__(self, name, description, discount_percentage, expiry_date, custom_code,user_id):
        self.name = name
        self.description = description
        self.discount_percentage = discount_percentage
        self.expiry_date = expiry_date
        self.custom_code = custom_code
        self.user_id = user_id

    def __repr__(self):
        return f'<Reward {self.name}> {self.discount_percentage} isUsed = {self.used}>'
    