from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from enum import Enum
db = SQLAlchemy()


user_roles = {
    'USER': ['read'],
    'ADMIN': ['read', 'write']
}

class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    avatar = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # bookings = db.relationship('Booking', backref='user', cascade='all, delete-orphan')
    def __init__(self, name, username, password, email, avatar):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
    def __repr__(self):
        return f'<User {self.id}: {self.name} {self.username}>'


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    # tables = db.relationship('Table', backref='restaurant', cascade='all, delete-orphan')

# class Table(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
#     table_number = db.Column(db.String(10), nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     bookings = db.relationship('Booking', backref='table', cascade='all, delete-orphan')

# class Booking(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
#     booking_date = db.Column(db.Date, nullable=False)
#     booking_time = db.Column(db.Time, nullable=False)
#     party_size = db.Column(db.Integer, nullable=False)
    #special note = String
    # timing of the booking dateTime.

    