from flask import render_template
from flask_mailman import Mail, EmailMultiAlternatives
# from flask_mail import Mail, Message


mail = Mail()


def init_mail(app):
    mail.init_app(app)


def send_mail(to, subject, template, **kwargs):
    text_content = render_template(f"{template}.txt", **kwargs)              
    html_content = render_template(f"{template}.html", **kwargs)
    print(f"TEXT CONTENT: {text_content}")
    print(f"HTML CONTENT: {html_content}")
    msg = EmailMultiAlternatives(
        subject=subject,
        to=[to],
        body=text_content
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # flask_email2 usage
    # msg = Message(
    #     subject=subject,
    #     recipients=[to],
    #     body=text_content,
    #     html=html_content,
    #     sender=('PandasRun', 'noreply@pandas.run')
    # )
    # mail.send(msg)
