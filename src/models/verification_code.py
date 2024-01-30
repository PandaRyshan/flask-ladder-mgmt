from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from src.extensions.db import db


class VerificationCode(db.Model):
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(db.String(80), unique=True)
    used: Mapped[bool] = mapped_column(db.Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime(), default=db.func.current_timestamp())
    expires_at: Mapped[datetime] = mapped_column(db.DateTime(), default=db.func.current_timestamp() + db.func.interval('1 day'))
