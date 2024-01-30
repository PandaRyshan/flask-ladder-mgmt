from sqlalchemy.orm import Mapped, mapped_column
from src.extensions.db import db


class UserRoles(db.Model):
    id: Mapped[int] = mapped_column(db.BigInteger(), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(db.BigInteger(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id: Mapped[int] = mapped_column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
