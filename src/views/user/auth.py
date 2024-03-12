from flask import Blueprint, redirect, render_template, request, \
    url_for, jsonify
from flask_security import login_user, logout_user, current_user, login_required
from services import user_service
from werkzeug.security import generate_password_hash, check_password_hash
from src.dto.user_dto import UserDTO
from src.models.user import User
from src.forms.auth_form import SignupForm, SigninForm


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup/", methods=["GET", "POST"], endpoint="signup")
def register():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = UserDTO(
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data,
            )
            user_service.create_user(user)

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


@bp.route("/signup/verify/<safe_token>/", methods=["GET"], endpoint="signup_verify")
def verify_account(safe_token=None):
    if safe_token:
        email = user_service.verify_token(safe_token)

        # invalid token
        if not email:
            return render_template("auth/verification.html", verification_result="invalid")

        name_of_user = user_service.verify_user(email)
        return render_template("auth/verification.html",
                                verification_result="valid", name=name_of_user)

    return redirect(url_for("index"))


@bp.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    form = SigninForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return jsonify(form.errors), 400

        user = User.query.filter_by(email=form.email.data).first()
        next_url = request.args.get("next")

        if user and check_password_hash(user.password, form.password.data):
            if login_user(user=user, remember=form.remember.data):
                return jsonify({"next_url": next_url or url_for("user.dashboard")})
            return jsonify({"error": "Invalid email or password"}), 400
        else:
            return jsonify({"error": "Invalid email or password"}), 400
    
    if current_user and current_user.is_active:
        return redirect(url_for("user.dashboard"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout/", methods=["GET", "POST"], endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/reset/", methods=["GET", "POST"], endpoint="reset")
@bp.route("/reset/<safe_token>/", methods=["GET", "POST"], endpoint="reset")
def reset():
    # TODO: implement reset password
    if request.method == "POST":
        # email = request.form.get("email")
        # user = User.query.filter_by(email=email).first()
        # token = generate_verification_token(email)
        pass
    
    return render_template("auth/reset.html")
