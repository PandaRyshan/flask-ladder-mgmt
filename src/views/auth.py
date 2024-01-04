from src.utils.db import db
from flask import Blueprint, g, redirect, render_template, request, session, url_for, flash, current_app
from flask_login import LoginManager
from src.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from src.utils.mail import send_mail
from src.forms.registration_form import RegistrationForm


bp = Blueprint("auth", __name__, url_prefix="/auth")


# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        user_name = email
        name = form.name.data

        error = None

        if User.query.filter_by(email=email).first() is not None:
            error = f"Email {email} is already registered."
        
        if error is None:
            user = User(password=generate_password_hash(password), user_name=user_name, email=email, name=name)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

        token = generate_confirmation_token(email,
                                            current_app.config["SECRET_KEY"],
                                            current_app.config["SECURITY_PASSWORD_SALT"])
        confirm_url = url_for("confirm", token=token, _external=True)
        send_mail(email, "Confirm Your Email Address", "mail/confirm", confirm_url=confirm_url)
        return render_template("auth/register_finish.html")
    
    return render_template("auth/register.html", form=form)


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
