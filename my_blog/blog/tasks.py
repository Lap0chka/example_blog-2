from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_celery(name, email, subject, user_message):
    message = f'Сообщение от: {name}\n' \
              f'Почта: {email}\n' \
              f'Сообщение: \n{user_message}'
    send_mail(
        subject,
        message,
        email,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
