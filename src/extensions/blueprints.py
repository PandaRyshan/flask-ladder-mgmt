from flask import Flask, redirect,  url_for
from flask_login import login_required
from src.views.user import bp as user_bp
from src.views.auth import bp as auth_bp


@staticmethod
def init(app: Flask):

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    # dynamically create url rules for the index view
    # app.add_url_rule('/', endpoint='index')

    @app.route("/index")
    @app.route("/", endpoint='index')
    @login_required
    def hello():
        return redirect(url_for("user.dashboard"))

    @app.route("/signup", methods=["GET"], endpoint="signup")
    def signup():
        return redirect(url_for("auth.signup"))

    @app.route("/login", methods=["GET"], endpoint="login")
    def login():
        return redirect(url_for("auth.login"))
