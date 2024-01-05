import uuid

from flask import Blueprint, g, redirect, render_template, request, session, \
    url_for, flash, current_app, jsonify
from flask_login import LoginManager
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from src.models.user import User, Role
from src.utils.db import db
from src.utils.mail import send_mail
from src.forms.registration_form import RegistrationForm
from src.views.contants import RoleEnum


bp = Blueprint("auth", __name__, url_prefix="/auth")


# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route("/signup", methods=["GET", "POST"], endpoint="signup")
def register():
    print("-------------- START --------------")
    form = RegistrationForm()
    print(form.data)
    if request.method == "POST":
        if form.validate_on_submit():
            print("----------------- NO ERROR -----------------")

            error = None

            # TODO: make a exception handler
            # TODO: replace user exist check via redis cache
            if User.query.filter_by(email=form.email.data).first() is not None:
                error = f"Email {form.email.data} is already registered."
                return jsonify({"error": [error]}), 400
            
            print("------------------ Start to register -------------------")
            user = User(
                password=generate_password_hash(form.password.data),
                user_name=form.email.data,
                email=form.email.data,
                name=form.name.data,
                active=False,
                roles=[Role.query.filter_by(id=RoleEnum.USER.value).first()],
                fs_uniquifier=uuid.uuid4().hex
            )
            db.session.add(user)

            token = generate_confirmation_token(
                form.email.data,
                current_app.config["SECRET_KEY"],
                current_app.config["SECURITY_PASSWORD_SALT"]
            )
            confirm_url = url_for("auth.confirm", token=token, _external=True)
            print(confirm_url)
            # TODO: make a email template
            # send_mail(email, "Confirm Your Email Address", "mail.confirm", confirm_url=confirm_url)
            return render_template("auth.finish")
        else:
            print("----------------- ERROR -----------------")
            print(form.errors)
            return jsonify(form.errors), 400

    return render_template("auth/signup.html", form=form)


@bp.route("/signup/finish", methods=["GET"], endpoint="finish")
def finish():
    referrer = request.referrer
    if referrer is None or not referrer.startswith(request.host_url):
        return redirect(url_for("index"))
    return render_template("auth/signup_finish.html")


@bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        error = None

        user = User.query.filter_by(username=username).first()
        if user is None or check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)
    
    return render_template("auth/login.html")


@bp.route("/logout", methods=["POST"], endpoint="logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.route("/reset", methods=["GET", "POST"], endpoint="reset")
def reset():
    if request.method == "POST":
        email = request.form.get("email")

        error = None

        user = User.query.filter_by(email=email).first()


def generate_confirmation_token(email, secret_key, salt):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


@bp.route("/confirm/<token>", methods=["GET"], endpoint="confirm")
def confirm_token(token, secret_key, salt, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(token, salt=salt, max_age=expiration)
    except SignatureExpired:
        return False
    return email
