from flask import Flask, redirect, render_template,  url_for
from flask_security import auth_required
from src.views.user import bp as user_bp
# from src.views.admin import bp as admin_bp


@staticmethod
def init(app: Flask):

    app.register_blueprint(user_bp)
    # app.register_blueprint(admin_bp)

    # dynamically create url rules for the index view
    # app.add_url_rule('/', endpoint='index')

    @app.route("/index/")
    @app.route("/", endpoint='index')
    @auth_required()
    def hello():
        return redirect(url_for("user.dashboard"))

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
