from flask import Flask
from flask_admin import Admin
from src.views.admin import VPNAdminIndexView


@staticmethod
def init(app: Flask):
    # flask admin view registration
    admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=VPNAdminIndexView())
    # admin.add_view(AuthModelView(User, db.session))
