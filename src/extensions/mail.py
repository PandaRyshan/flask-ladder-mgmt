from flask_mailman import Mail


mail = Mail()


def init(app):
    mail.init_app(app)
