from flask import Flask
from flask_security import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from src.models.user import User
from src.models.role import Role
from src.forms.auth_form import ConfirmRegisterFormExtended
from src.utils.mail import SecurityMail
from src.extensions.db import db


security = Security()


@staticmethod
def init(app: Flask):
    app.security = Security(
        app=app,
        datastore=CustomUserDatastore(db, User, Role),
        confirm_register_form=ConfirmRegisterFormExtended,
        mail_util_cls=SecurityMail
    )


class CustomUserDatastore(SQLAlchemyUserDatastore):
    def create_user(self, **kwargs):
        kwargs["roles"] = [self.find_role("USER")]
        user = super().create_user(**kwargs)
        return user
