from flask import Flask
from flask_login import LoginManager
from src.models.user import User


# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@staticmethod
def init(app: Flask):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
