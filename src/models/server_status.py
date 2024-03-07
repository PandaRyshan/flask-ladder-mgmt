from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from src.extensions.db import db, Base


class ServerStatus(Base):
    __tablename__ = "server_status"
    id: Mapped[int] = mapped_column(db.BigInteger(), primary_key=True, autoincrement=True)
    server_id: Mapped[int] = mapped_column(db.BigInteger(), db.ForeignKey("server.id"))
    disk_usage: Mapped[float] = mapped_column(db.Float())
    cpu_usage: Mapped[float] = mapped_column(db.Float())
    ram_usage: Mapped[float] = mapped_column(db.Float())
    bandwidth: Mapped[float] = mapped_column(db.Float())
    created_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=db.func.now())
