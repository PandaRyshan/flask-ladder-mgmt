from flask import Flask
from flask_admin import Admin
from src.models.user import User
from src.models.server import Server
from src.views.admin.user import UserView
from src.views.admin.server import ServerView
from src.extensions.db import db


@staticmethod
def init(app: Flask):
    # flask admin view registration
    admin = Admin(
        app=app,
        name="Admin",
        template_mode="bootstrap4",
        # index_view=,
        url="/admin/"
    )

    admin.add_view(
        UserView(
            model=User,
            session=db.session,
            name="Users",
            endpoint="users",
            menu_icon_type="glyph",
            menu_icon_value="glyphicon-user"
        )
    )

    admin.add_view(
        ServerView(
            model=Server,
            session=db.session,
            name="Servers",
            endpoint="servers",
            menu_icon_type="glyph",
            menu_icon_value="glyphicon-hdd"
        )
    )
