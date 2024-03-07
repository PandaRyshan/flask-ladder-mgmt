from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.extensions.db import db
from src.models.server_status import ServerStatus


class Server(db.Model):
    __tablename__ = "server"
    id: Mapped[int] = mapped_column(db.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100))
    ip_address: Mapped[str] = mapped_column(db.String(100))
    status: Mapped[list[ServerStatus]] = relationship("ServerStatus", lazy="dynamic")
