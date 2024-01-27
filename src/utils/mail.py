from flask import render_template
from flask_mailman import EmailMultiAlternatives
from extensions.celery import celery


@celery.task(name="send_mail", bind=True, max_retries=3, default_retry_delay=60)
def send_mail(self, to, subject, template, **kwargs):
    text_content = render_template(f"{template}.txt", **kwargs)              
    html_content = render_template(f"{template}.html", **kwargs)
    msg = EmailMultiAlternatives(
        subject=subject,
        to=[to],
        body=text_content
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
