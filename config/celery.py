import os
from celery import Celery

# Устанавливаем настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем приложение Celery
app = Celery('config')

# Загружаем конфигурацию из настройки Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи (tasks.py) в каждом установленном приложении Django
app.autodiscover_tasks()
