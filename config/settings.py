import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('MY_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',

    'django_celery_beat',
    'rest_framework_simplejwt',
    'django_filters',
    'lms',
    'users',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'  # Фильтрация
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Аутентификация по токенам
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.AllowAny',       # Всё разрешено
        'rest_framework.permissions.IsAuthenticated',  # Только аутентифицированные пользователи
    ]
}

# Настройки срока действия токенов
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),  # Название БД
        'USER': os.getenv('POSTGRES_USER'),  # Пользователь для подключения
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  # Пароль для этого пользователя
        'HOST': os.getenv('POSTGRES_HOST'),  # Адрес, на котором развернут сервер БД
        'PORT': os.getenv('POSTGRES_PORT')  # Порт, на котором работает сервер БД
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

STRIPE_SECRET_KEY = os.getenv('MY_STRIPE_SECRET_KEY')
STRIPE_SUCCESS_URL = 'https://127.0.0.1:8000/admin'
STRIPE_CANCEL_URL = 'https://127.0.0.1:8000/admin'

COURSE_PRICE = 0

# Настройки Celery
CELERY_BROKER_URL = os.getenv('MY_CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('MY_CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']   # Принимаем данные в формате JSON
CELERY_TASK_SERIALIZER = 'json'    # Сериализатор задач
CELERY_RESULT_SERIALIZER = 'json'  # Сериализатор результата
CELERY_TIMEZONE = TIME_ZONE        # Часовой пояс
CELERY_TASK_TRACK_STARTED = True   # Отслеживание задач
CELERY_TASK_TIME_LIMIT = 30 * 60   # 30 минут


# Настройки django-celery-beat
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_BEAT_SCHEDULE = {
    'check-inactive-users': {
        'task': 'users.tasks.check_inactive_users',
        'schedule': crontab(minute=0, hour=0),  # Запускать ежедневно в полночь
    }
}

# Настройки почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('MY_EMAIL_HOST')
EMAIL_PORT = os.getenv('MY_EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('MY_EMAIL_USE_TLS', 'False') == 'True'
EMAIL_USE_SSL = os.getenv('MY_EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('MY_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('MY_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('MY_DEFAULT_FROM_EMAIL')
