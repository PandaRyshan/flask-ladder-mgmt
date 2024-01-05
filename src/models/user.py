from flask_security import UserMixin
from src.utils.db import db
from src.models.role import Role
from src.models.user_roles import UserRoles


class User(db.Model, UserMixin):
    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    roles = db.relationship('Role', secondary=UserRoles.__tablename__,
                            backref=db.backref('user', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String, nullable=False, unique=True)
