from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from src.models.user import User
from src.models.role import Role


@staticmethod
def init(app: Flask, db: SQLAlchemy):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
