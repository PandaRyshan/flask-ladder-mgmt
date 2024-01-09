from flask import render_template
from flask_mailman import EmailMultiAlternatives
from src.utils.celery import celery


@celery.task(name="send_mail", max_retries=3, default_retry_delay=60)
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
