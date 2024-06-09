from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, max_length=50, verbose_name='почта', help_text='введите почту')
    phone = models.CharField(unique=True, max_length=50, verbose_name='телефон', help_text='введите телефон')
    city = models.CharField(max_length=50, verbose_name='город', help_text='введите город')
    avatar = models.ImageField(upload_to='users/avatars/%Y/%m/%d', verbose_name='аватар', help_text='выберите аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
