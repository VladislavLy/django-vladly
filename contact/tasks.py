from celery import shared_task

from django.core.mail import EmailMessage

from mysite.settings import ADMIN_EMAIL, EMAIL_HOST_USER


@shared_task
def send_email_contact(title, email_from, message):
    email = EmailMessage(
        subject=title,
        body=f"Email from: {email_from}. \n Message: {message} \n ",
        from_email=f'DJANGO_PROJECT {EMAIL_HOST_USER}',
        to=ADMIN_EMAIL
    )
    email.send()
    return "Success"
