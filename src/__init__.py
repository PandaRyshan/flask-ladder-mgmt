import os
from src import config

from logger import LoggerConfigurator
from flask import Flask, redirect,  url_for
from flask.cli import load_dotenv
from flask_login import login_required
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    # shell env -> .env -> .flaskenv -> os.environ
    load_dotenv()

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    CSRFProtect(app)

    if not test_config:
        # load the instance .env
        match os.environ['FLASK_ENV']:
            case 'prod':
                app.config.from_object(config.ProductionConfig)
            case 'test':
                app.config.from_object(config.TestingConfig)
            case 'dev':
                app.config.from_object(config.DevelopmentConfig)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # logging configuration
    LoggerConfigurator.setup_app_logger(app)


    @app.route("/index")
    @app.route("/", endpoint='index')
    @login_required
    def hello():
        return redirect(url_for("user.dashboard"))

    @app.route("/register", methods=["GET"], endpoint="register")
    def register():
        return redirect(url_for("auth.register"))

    @app.route("/login", methods=["GET"], endpoint="login")
    def login():
        return redirect(url_for("auth.login"))

    # register the database commands (sqlalchemy)
    from src.utils import db
    db.init_app(app)

    from src.route_manager import RouteManager
    
    # register flask admin & blueprint
    RouteManager.register_admin(app)
    RouteManager.register_security(app, db.db)
    RouteManager.register_routes(app)

    from src.views.auth import login_manager
    login_manager.init_app(app)

    from src.utils.mail import init_mail
    init_mail(app)

    return app
