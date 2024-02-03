import os


class BaseConfig(object):
    FLASK_DEBUG = False
    TESTING = False
    FLASK_ENV = os.environ['FLASK_ENV']
    # make sure all security config are overriden in production
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20,
    }
    REDIS_URI = os.environ['REDIS_URI']
    # flask-caching
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
    # flask-security
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
    SECURITY_REGISTERABLE = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"
    # flask-mail
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    # You should only set one of MAIL_USE_TLS or MAIL_USE_SSL in the env
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    # MAIL_USE_SSL = os.environ['MAIL_USE_SSL']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
    MAIL_MAX_MAILS = os.environ['MAIL_MAX_MAILS']
    MAIL_DEBUG = os.environ['FLASK_DEBUG']
    # celery
    CELERY = {
        "broker_url": os.environ['CELERY_BROKER_URL'],
        "result_backend": os.environ['CELERY_RESULT_BACKEND']
    }
    # flask admin theme
    FLASK_ADMIN_SWATCH = 'cerulean'
    # log path
    FLASK_LOG_PATH = os.environ['FLASK_LOG_PATH']


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    SERVER_NAME = os.environ['SERVER_NAME']
