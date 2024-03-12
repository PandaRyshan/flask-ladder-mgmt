from typing import Optional
from pydantic import BaseModel, ConfigDict


class ServerDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    ip_address: str
    disk_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    ram_usage: Optional[float] = None
    bandwidth_usage: Optional[float] = None
