from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.actions import action
from flask_admin.model.template import LinkRowAction
from flask_security import current_user, admin_change_password
from src.models.role import Role
from src.models.user import User
from src.contants import ADMIN


class UserView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role(ADMIN)

    def format_roles(view, context, model, name):
        return ", ".join([role.name for role in model.roles])

    def format_date(view, context, model, name):
        return model.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def role_query():
        return Role.query

    def get_user_by_id(self, id):
        return User.query.get(id)

    @action("reset_password", "Reset Password", "Are you sure you want to reset the password of this user?")
    def reset_user_access(self, id):
        admin_change_password(self.get_user_by_id(id), "NewPassword")

    can_create = True
    can_delete = False
    can_edit = True
    can_view_details = True

    page_size = 20

    column_list = ["email", "name", "roles", "active", "created_at", "last_login_at"]
    # column_editable_list = ["active"]
    column_searchable_list = ["email", "name", "active"]
    column_filters = ["email", "name"]
    column_extra_row_actions = [
        LinkRowAction("glyphicon glyphicon-refresh", "users.reset_password", "Reset Password")
    ]

    form_columns = ["email", "name", "roles", "active"]
    form_edit_rules = ["email", "name", "roles", "active"]
    form_extra_fields = {
        "roles": QuerySelectMultipleField(
            label="Roles",
            query_factory=role_query,
            get_label="name"
        )
    }

    create_modal = True
    edit_modal = True

    column_formatters = {
        "roles": format_roles,
        "created_at": format_date,
        "last_login_at": format_date
    }