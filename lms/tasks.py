from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_update_email(user_email, course_name):
    """ Отправка письма об обновлении курса.
    """
    subject = f'Обновление курса {course_name}'
    message = f'Курс {course_name} был обновлен. Пожалуйста, проверьте новые материалы.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
