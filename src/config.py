import os


class BaseConfig(object):
    FLASK_DEBUG = False
    TESTING = False
    FLASK_ENV = os.environ['FLASK_ENV']
    # make sure all security config are overriden in production
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    # flask-security
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
    SECURITY_REGISTERABLE = True
    # flask-mail
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
    # flask admin theme
    FLASK_ADMIN_SWATCH = 'cerulean'
    # log path
    LOG_PATH = '/tmp/vpn_admin.log'


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    LOG_PATH = '/var/log/vpn_admin/app.log'
