from datetime import datetime
from flask_security import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.extensions.db import db
from src.models.role import Role
from src.models.user_roles import UserRoles


class User(db.Model, UserMixin):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        username (str): The username of the user.
        name (str): The name of the user.
        is_active (bool): Indicates whether the user is active or not.
        is_verified (bool): Indicates whether the user is verified or not.
        roles (list[Role]): The roles assigned to the user.
        fs_uniquifier (str): The unique identifier used for file storage.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
        last_login_at (datetime): The timestamp of the last login.
        last_login_ip (str): The IP address of the last login.
        current_login_at (datetime): The timestamp of the current login.
        login_count (int): The number of logins made by the user.
    """

    id: Mapped[int] = mapped_column(db.BigInteger(), primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(db.String(), unique=True)
    password: Mapped[str] = mapped_column(db.String())
    username: Mapped[str] = mapped_column(db.String(64), nullable=True)
    name: Mapped[str] = mapped_column(db.String(100))
    active: Mapped[bool] = mapped_column(db.Boolean(), default=True)
    roles: Mapped[list[Role]] = relationship(
        "Role", secondary=UserRoles.__tablename__,
        backref=db.backref('user', lazy='dynamic')
    )
    fs_uniquifier: Mapped[str] = mapped_column(db.String(64), unique=True)
    tf_totp_secret: Mapped[str] = mapped_column(db.String(255), nullable=True)
    tf_primary_method: Mapped[str] = mapped_column(db.String(20), nullable=True)
    tf_phone_number: Mapped[str] = mapped_column(db.String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, server_default=db.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    last_login_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    last_login_ip: Mapped[str] = mapped_column(db.String(100), nullable=True)
    current_login_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    current_login_ip: Mapped[str] = mapped_column(db.String(100), nullable=True)
    confirmed_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    login_count: Mapped[int] = mapped_column(db.Integer, default=0)


    def get_id(self) -> str:
        """
        Returns the string representation of the user's ID.

        :return: The string representation of the user's ID.
        :rtype: str
        """
        return str(self.id)
