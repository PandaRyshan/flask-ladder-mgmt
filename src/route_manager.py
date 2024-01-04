from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from src.models.user import User
from src.models.role import Role
from src.views.user import bp as user_bp
from src.views.auth import bp as auth_bp
from src.views.admin import VPNAdminIndexView, AuthModeView


class RouteManager:

    @staticmethod
    def register_admin(app):
        # flask admin view registration
        admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=VPNAdminIndexView())
        # admin.add_view(AuthModelView(User, db.session))

    @staticmethod
    def register_security(app, db):
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security(app, user_datastore)

    @staticmethod
    def register_routes(app):

        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)

        # dynamically create url rules for the index view
        app.add_url_rule('/', endpoint='index')
