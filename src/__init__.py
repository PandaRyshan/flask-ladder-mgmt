import os

from flask import Flask
from flask.cli import load_dotenv
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    # shell env -> .env -> .flaskenv -> os.environ
    load_dotenv()

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    from src import config
    if not test_config:
        # load the instance .env
        match os.environ['FLASK_ENV']:
            case 'production':
                app.config.from_object(config.ProductionConfig)
            case 'testing':
                app.config.from_object(config.TestingConfig)
            case 'development':
                app.config.from_object(config.DevelopmentConfig)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # logging configuration
    from logger import LoggerConfigurator
    LoggerConfigurator.setup_app_logger(app)

    # csrf protection lazily
    csrf = CSRFProtect()
    csrf.init_app(app)

    # register app extensions
    from src.extensions import blueprints, login, admin, security, \
        celery, db, redis, mail

    db.init(app)
    redis.init(app)
    celery.init(app)
    blueprints.init(app)
    mail.init(app)
    login.init(app)
    admin.init(app)
    security.init(app, db)

    return app
