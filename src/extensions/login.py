import base64
from http import HTTPStatus
from flask import Flask, url_for, request, redirect, jsonify, g
from flask.sessions import SecureCookieSessionInterface
from flask_login import LoginManager, user_loaded_from_request
from src.models.user import User
from src.extensions.cache import cache
from sqlalchemy.orm import joinedload


# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to access this page."


@staticmethod
def init(app: Flask):
    login_manager.init_app(app)


@login_manager.user_loader
@cache.memoize(timeout=60)
def load_user(user_id):
    return User.query.options(joinedload(User.roles)).get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == "api":
        jsonify({"message": "Unauthorized access"}), HTTPStatus.UNAUTHORIZED
    return redirect(url_for("auth.login", next=request.endpoint))


@login_manager.request_loader
def load_user_from_request(req: request):
    api_key = req.args.get("api_key")
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    api_key = req.headers.get("Authorization")
    if api_key:
        api_key = api_key.replace("Bearer ", "", 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


@user_loaded_from_request.connect
def user_loaded_from_request(app: Flask, user=None):
    g.login_via_request = True


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get("login_via_request"):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)
