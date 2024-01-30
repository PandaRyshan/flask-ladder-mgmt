from flask_mailman import Mail


mail = Mail()


@staticmethod
def init(app):
    mail.init_app(app)
