from flask import render_template
from flask import Blueprint
from flask_login import login_required
from src.models.user import User
from extensions.db import db


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/list", methods=["GET"], endpoint="list")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars().all()
    return render_template("user/list.html", users=users)


@bp.route("/dashboard", methods=["GET"], endpoint="dashboard")
@login_required
def dashboard():
    return render_template("user/dashboard.html")
