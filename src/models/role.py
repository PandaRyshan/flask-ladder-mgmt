from sqlalchemy.orm import Mapped, mapped_column
from flask_security import RoleMixin
from src.extensions.db import db


class Role(db.Model, RoleMixin):
    id: Mapped[int] = mapped_column(db.SmallInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(80), unique=True)
    description: Mapped[str] = mapped_column(db.String(255), nullable=True)
