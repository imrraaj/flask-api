from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from enum import Enum
db = SQLAlchemy()


class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    GUEST = 'GUEST'

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    avatar = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
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