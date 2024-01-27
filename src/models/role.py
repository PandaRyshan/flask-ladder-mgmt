from flask_security import RoleMixin
from extensions.db import db


class Role(db.Model, RoleMixin):
    id = db.Column(db.SmallInteger(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
