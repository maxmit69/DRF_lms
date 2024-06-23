from datetime import datetime, timedelta
from celery import shared_task
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def check_inactive_users():
    """ Деактивация пользователя при отсутствии активности более 30 дней.
    """
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
