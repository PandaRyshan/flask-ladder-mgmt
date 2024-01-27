from extensions.db import db


class UserRoles(db.Model):
    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
