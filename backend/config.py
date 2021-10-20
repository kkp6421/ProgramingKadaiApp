import os
from datetime import timedelta
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(override=True)

class Config:
    JSON_AS_ASCII = False
    JWT_AUTH_URL_RULE = '/api/auth'
    JWT_AUTH_USERNAME_KEY = 'email'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_EXPIRATION_DELTA = timedelta(minutes=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_ADDRESS")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
    @staticmethod
    def init_app(app):
        pass

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-production.sqlite')

config = {
    'development': Development,
    'testing': Testing,
    'production': Production,

    'default': Development
}