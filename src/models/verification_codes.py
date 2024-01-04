from src.utils.db import db


class VerificationCode(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    code = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    used = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime(), default=db.func.current_timestamp() + db.func.interval('1 day'))
