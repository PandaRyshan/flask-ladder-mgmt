from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from src.models.user import User
from src.models.role import Role
from src.forms.auth_form import ConfirmRegisterFormExtended
from src.utils.mail import SecurityMail


security = Security()


@staticmethod
def init(app: Flask, db: SQLAlchemy):
    user_datastore = CustomUserDatastore(db, User, Role)
    security.init_app(
        app=app,
        datastore=user_datastore,
        register_blueprint=True,
        confirm_register_form=ConfirmRegisterFormExtended,
        mail_util_cls=SecurityMail
    )


class CustomUserDatastore(SQLAlchemyUserDatastore):
    def create_user(self, **kwargs):
        kwargs["roles"] = [self.find_role("USER")]
        user = super().create_user(**kwargs)
        return user
