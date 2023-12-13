from flask import redirect, url_for, request
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.exceptions import abort


class VPNAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin and current_user.is_active

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        abort(403)


class AuthModeView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin and current_user.is_active

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        abort(403)
