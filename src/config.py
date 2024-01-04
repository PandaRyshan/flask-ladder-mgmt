import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    FLASK_ENV = os.environ['FLASK_ENV']
    # make sure all security config are overriden in production
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    # flask-security
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT'],
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH'],
    SECURITY_REGISTERABLE = True,
    # flask-mail
    MAIL_SERVER = os.environ['MAIL_SERVER'],
    MAIL_PORT = os.environ['MAIL_PORT'],
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS'],
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL'],
    MAIL_USERNAME = os.environ['MAIL_USERNAME'],
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD'],
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER'],


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/vpn_admin' 


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
