from flask_mailman import EmailMultiAlternatives
from flask_security.mail_util import MailUtil
from src.extensions.celery import celery


@celery.task(name="send_flask_mail", bind=True, max_retries=3, default_retry_delay=60)
def send_flask_mail(self, **kwargs):
    html = kwargs.pop("html", None)
    msg = EmailMultiAlternatives(**kwargs)
    if html:
        msg.attach_alternative(html, "text/html")
    msg.send()
    

class SecurityMail(MailUtil):

    def send_mail(self, template, subject, recipient, sender, body, html, **kwargs):
        send_flask_mail.delay(
            subject=subject,
            from_email=sender,
            to=[recipient],
            body=body,
            html=html
        )
