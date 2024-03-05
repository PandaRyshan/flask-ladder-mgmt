import json
import time

from flask import render_template, Blueprint, stream_with_context, Response
from flask_security import current_user, auth_required
from src.models.user import User
from src.extensions.db import db


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"], endpoint="list")
@auth_required()
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars().all()
    return render_template("user/list.html", users=users)


@bp.route("/dashboard", methods=["GET"], endpoint="dashboard")
@auth_required()
def dashboard():
    return render_template("user/dashboard.html", name=current_user.name)


@bp.route("/event", methods=["GET", "POST"], endpoint="event")
def test():
    return Response(stream_with_context(generate_msg()), content_type="text/event-stream", status=200)


def generate_msg():
    while True:
        json_data = json.dumps({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "msg": "Hello, World!"})
        yield f"data: {json_data}\n\n"
        time.sleep(1)
