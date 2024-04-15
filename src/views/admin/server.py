from flask_admin import expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.actions import action
from flask_admin.model.template import LinkRowAction
from flask_security import current_user
from flask_security.decorators import roles_required, auth_required
from markupsafe import Markup
from src.services.server_service import ServerService
from src.contants import ADMIN


class ServerView(ModelView):

    # @expose("/")
    # @auth_required()
    # @roles_required(ADMIN)
    # def index(self):
    #     servers = ServerService().get_all_servers()
    #     return self.render("admin/servers.html", servers=servers)


    # @expose("/node_usage/<ip>/")
    # def node_usage(self, ip: str):
    #     cpu_usage = ServerService().get_cpu_usage(ip)
    #     ram_usage = ServerService().get_memory_usage(ip)
    #     disk_usage = ServerService().get_disk_usage(ip)
    #     bandwidth_usage = ServerService().get_bandwidth_usage(ip)
    #     result = {
    #         "cpu": cpu_usage.get(ip),
    #         "ram": ram_usage.get(ip),
    #         "disk": disk_usage.get(ip),
    #         "bandwidth": bandwidth_usage.get(ip)
    #     }
    #     return result

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role(ADMIN)

    def format_date(view, context, model, name):
        return model.created_at.strftime("%Y-%m-%d %H:%M:%S")

    # def role_query():
    #     return Role.query

    # def get_user_by_id(self, id):
    #     return User.query.get(id)

    @action("upgrade", "Upgrade", "Confirm to upgrade selected servers?")
    def upgrade_server(self, id):
        ServerService().upgrade_server(id)

    can_create = True
    can_delete = False
    can_view_details = True

    page_size = 20

    column_list = ["name", "ip_address", "cpu", "ram", "bandwidth", "disk"]
    column_searchable_list = ["name", "ip_address"]
    column_filters = ["name", "ip_address"]
    column_extra_row_actions = [
        LinkRowAction("glyphicon glyphicon-refresh", "", "")
    ]

    # form_columns = ["email", "name", "roles", "active"]
    # form_edit_rules = ["email", "name", "roles", "active"]
    # form_extra_fields = {
    #     "roles": QuerySelectMultipleField(
    #         label="Roles",
    #         query_factory=,
    #         get_label="name"
    #     )
    # }

    create_modal = True
    edit_modal = False

    def format_cpu(view, context, model, name):
        usage = ServerService().get_cpu_usage(model.ip_address).get(model.ip_address)
        return Markup(f'<div class="progress"><div class="progress-bar" role="progressbar" style="width: {usage}%" '
                      f'aria-valuenow="{usage}" aria-valuemin="0" aria-valuemax="100">{usage}%</div></div>')

    def format_ram(view, context, model, name):
        usage = ServerService().get_memory_usage(model.ip_address).get(model.ip_address)
        return Markup(f'<div class="progress"><div class="progress-bar" role="progressbar" style="width: {usage}%" '
                      f'aria-valuenow="{usage}" aria-valuemin="0" aria-valuemax="100">{usage}%</div></div>')

    def format_bandwidth(view, context, model, name):
        usage = ServerService().get_bandwidth_usage(model.ip_address).get(model.ip_address)
        return Markup(f'<div class="progress"><div class="progress-bar" role="progressbar" style="width: {usage}%" '
                      f'aria-valuenow="{usage}" aria-valuemin="0" aria-valuemax="100">{usage}%</div></div>')

    def format_disk(view, context, model, name):
        usage = ServerService().get_disk_usage(model.ip_address).get(model.ip_address)
        return Markup(f'<div class="progress"><div class="progress-bar" role="progressbar" style="width: {usage}%" '
                      f'aria-valuenow="{usage}" aria-valuemin="0" aria-valuemax="100">{usage}%</div></div>')

    column_formatters = {
        "cpu": format_cpu,
        "ram": format_ram,
        "bandwidth": format_bandwidth,
        "disk": format_disk
    }
