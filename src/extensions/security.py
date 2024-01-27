from flask_security import Security, SQLAlchemyUserDatastore
from src.models.user import User
from src.models.role import Role


@staticmethod
def init(app, db):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
