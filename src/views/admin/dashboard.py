from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.actions import action
from flask_admin.model.template import LinkRowAction
from flask_security.decorators import roles_required, auth_required
from src.contants import ADMIN


class DashboardView(ModelView):

    @expose("/")
    @auth_required()
    @roles_required(ADMIN)
    def index(self):
        return self.render("admin/index.html")

