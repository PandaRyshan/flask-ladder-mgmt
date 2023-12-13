from flask_security import UserMixin, RoleMixin
from src.utils.db import db


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String, nullable=False, unique=True)
