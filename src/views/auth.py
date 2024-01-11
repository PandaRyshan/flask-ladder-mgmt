import uuid

from flask import Blueprint, redirect, render_template, request, session, \
    url_for, flash, current_app, jsonify
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from src.models.user import User
from src.models.role import Role
from src.utils.db import db
from src.utils.mail import send_mail
from src.forms.signup_form import SignupForm
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
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(
                password=generate_password_hash(form.password.data),
                username=form.email.data,
                email=form.email.data,
                name=form.name.data,
                active=False,
                roles=[Role.query.filter_by(id=RoleEnum.USER.value).first()],
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


@bp.route("/signup/pending/", methods=["GET"], endpoint="signup_pending")
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
        if user.active:
            return render_template("auth/verification.html", verification_result="invalid")
        else:
            # active user account
            user.active = True
            db.session.add(user)
            return render_template("auth/verification.html",
                                   verification_result="valid", name=user.name)

    return redirect(url_for("index"))


@bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    # TODO: add flask-session and redis
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
