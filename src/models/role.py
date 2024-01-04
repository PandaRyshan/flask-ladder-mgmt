from flask_security import RoleMixin
from src.utils.db import db


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
