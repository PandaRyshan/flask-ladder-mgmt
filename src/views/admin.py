from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security.decorators import roles_required
from src.services import user_service
from src.contants import ADMIN


class IndexViews(AdminIndexView):

    @expose("/")
    @roles_required(ADMIN)
    def index(self):
        return self.render("admin/index.html")


class UserView(ModelView):
    column_list = ["email", "password", "name", "roles"]
    page_size = 20

    form_excluded_columns = ["username", "fs_uniquifier", "created_at", "updated_at"]

    @expose("/")
    @roles_required(ADMIN)
    def index(self):
        users = user_service.get_all_users()
        return self.render("admin/users.html", users=users)


    @expose("/edit/<int:id>/", methods=["GET", "POST"])
    @roles_required(ADMIN)
    def edit(self, id):
        return super(UserView, self).edit(id)
