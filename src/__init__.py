import os

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
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY = os.environ['SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI'],
        # set optional bootswatch theme
        FLASK_ADMIN_SWATCH = 'cerulean',
        
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
    )

    csrf = CSRFProtect(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
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
