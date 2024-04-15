import requests
from src.models.server import Server
from src.dto.server_dto import ServerDTO


class ServerService:

    def get_all_servers(self):
        servers = Server.query.all()
        server_DTOs = []
        for server in servers:
            server_DTO = ServerDTO.model_validate(server)
            server_DTOs.append(server_DTO)
        return server_DTOs


    def get_cpu_usage(self, ip: str):
        cpu_usages = requests.get(
            "http://localhost:9090/api/v1/query",
            params={"query": f"sum(rate(node_cpu_seconds_total{{instance='{ip}:9100', mode='idle'}}[5m]))"}
        ).json().get("data").get("result")
        cpu_usage_dict = {}
        for usage in cpu_usages:
            cpu_usage_dict[ip] = usage.get("value")[1]
        return cpu_usage_dict


    def get_disk_usage(self, ip: str):
        disk_usages = requests.get(
            "http://localhost:9090/api/v1/query",
            params={"query": f"100 - (node_filesystem_avail_bytes{{instance='{ip}:9100', mountpoint='/etc/hostname'}} / node_filesystem_size_bytes{{instance='{ip}:9100', mountpoint='/etc/hostname'}} * 100)"}
        ).json().get("data").get("result")
        disk_usage_dict = {}
        for usage in disk_usages:
            disk_usage_dict[ip] = usage.get("value")[1]
        return disk_usage_dict


    def get_memory_usage(self, ip: str):
        memory_usages = requests.get(
            "http://localhost:9090/api/v1/query",
            params={"query": f"((node_memory_MemTotal_bytes{{instance='{ip}:9100'}} - node_memory_MemAvailable_bytes{{instance='{ip}:9100'}}) / node_memory_MemTotal_bytes{{instance='{ip}:9100'}}) * 100"}
        ).json().get("data").get("result")
        memory_usage_dict = {}
        for usage in memory_usages:
            memory_usage_dict[ip] = usage.get("value")[1]
        return memory_usage_dict


    def get_bandwidth_usage(self, ip: str):
        bandwidth_usages = requests.get(
            "http://localhost:9090/api/v1/query",
            params={"query": f"irate(node_network_transmit_bytes_total{{instance='{ip}:9100'}}[5m]) / 1024 / 1024"}
        ).json().get("data").get("result")
        bandwidth_usage_dict = {}
        for usage in bandwidth_usages:
            bandwidth_usage_dict[ip] = usage.get("value")[1]
        return bandwidth_usage_dict

    def upgrade_server(self, id: int):
        pass