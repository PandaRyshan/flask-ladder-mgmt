from flask_mail import Mail, Message
from flask import current_app, render_template


mail = Mail()


def init_mail(app):
    mail.init_app(app)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to], 
                  sender=current_app.config["MAIL_USERNAME"])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
