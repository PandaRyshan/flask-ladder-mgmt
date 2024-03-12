from flask_admin import AdminIndexView, expose
# from flask_admin.actions import action
# from flask_admin.model.template import LinkRowAction
from flask_security.decorators import roles_required, auth_required
from src.services.server_service import ServerService
from src.contants import ADMIN


class IndexView(AdminIndexView):

    @expose("/")
    @auth_required()
    @roles_required(ADMIN)
    def index(self):
        servers = ServerService().get_all_servers()
        return self.render("admin/index.html", servers=servers)


    @expose("/node_usage/<ip>/")
    def node_usage(self, ip: str):
        cpu_usage = ServerService().get_cpu_usage(ip)
        ram_usage = ServerService().get_memory_usage(ip)
        disk_usage = ServerService().get_disk_usage(ip)
        result = {
            "cpu": cpu_usage.get(ip),
            "ram": ram_usage.get(ip),
            "disk": disk_usage.get(ip)
        }
        print("result: ", result)
        return result
