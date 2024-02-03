import uuid

from flask import Blueprint, redirect, render_template, request, \
    url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from src.models.user import User
from src.models.role import Role
from src.extensions.db import db
from src.utils.mail import send_mail
from src.forms.auth_form import SignupForm, SigninForm
from src.views.contants import RoleEnum


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup", methods=["GET", "POST"], endpoint="signup")
def register():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(
                password=generate_password_hash(form.password.data),
                username=form.email.data,
                email=form.email.data,
                name=form.name.data,
                roles=[db.session.query(Role).filter_by(id=RoleEnum.USER.value).first()],
                fs_uniquifier=uuid.uuid4().hex
            )
            db.session.add(user)

            token = generate_verification_token(form.email.data)
            verification_url = url_for("auth.signup_verify", safe_token=token, _external=True)
            send_mail.delay(
                to=form.email.data,
                subject="Verify Your Email Address",
                template="mail/verification",
                verification_url=verification_url,
                name=form.name.data
            )
            return jsonify({"next_url": url_for("auth.signup_pending")})
        else:
            return jsonify(form.errors), 400

    return render_template("auth/signup.html", form=form)


@bp.route("/signup/pending", methods=["GET"], endpoint="signup_pending")
def signup_pending():
    referrer = request.referrer
    if referrer is None or not referrer.startswith(request.host_url):
        return redirect(url_for("index"))
    return render_template("auth/verification.html")


@bp.route("/signup/verify/<safe_token>", methods=["GET"], endpoint="signup_verify")
def verify_account(safe_token=None):
    if safe_token:
        email = verify_token(safe_token)

        # invalid token
        if not email:
            return render_template("auth/verification.html", verification_result="invalid")

        user = User.query.filter_by(email=email).first()
        if user.is_active:
            return render_template("auth/verification.html", verification_result="invalid")
        else:
            # active user account
            user.is_active = True
            user.is_authenticated = True
            db.session.add(user)
            return render_template("auth/verification.html",
                                   verification_result="valid", name=user.name)

    return redirect(url_for("index"))


@bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    form = SigninForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return jsonify(form.errors), 400

        user = User.query.filter_by(username=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("user.dashboard"))
        else:
            flash("Username or password is not correct", "error")
    
    if current_user.is_authenticated:
        return redirect(url_for("user.dashboard"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["GET", "POST"], endpoint="logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@bp.route("/reset", methods=["GET", "POST"], endpoint="reset")
@bp.route("/reset/<safe_token>", methods=["GET", "POST"], endpoint="reset")
def reset():
    # TODO: implement reset password
    if request.method == "POST":
        # email = request.form.get("email")
        # user = User.query.filter_by(email=email).first()
        # token = generate_verification_token(email)
        pass
    
    return render_template("auth/reset.html")


def generate_verification_token(email):
    secret_key = current_app.config["SECRET_KEY"]
    salt = current_app.config["SECURITY_PASSWORD_SALT"]
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


def verify_token(saved_token, expiration=10800):
    secret_key = current_app.config["SECRET_KEY"]
    salt = current_app.config["SECURITY_PASSWORD_SALT"]
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(saved_token, salt=salt, max_age=expiration)
    except SignatureExpired:
        return False
    return email
