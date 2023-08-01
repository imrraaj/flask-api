# config.py

import os, datetime

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
    DEBUG = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 2525
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'storefront@shopify.com'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Add other production-specific settings here, like database configurations, caching, etc.

class TestingConfig(Config):
    TESTING = True
    # Add other testing-specific settings here, like database configurations for testing, etc.

config = DevelopmentConfig
