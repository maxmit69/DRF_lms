from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, max_length=50, verbose_name='почта', help_text='введите почту')
    phone = models.CharField(unique=True, max_length=50, verbose_name='телефон', help_text='введите телефон')
    city = models.CharField(max_length=50, verbose_name='город', help_text='введите город')
    avatar = models.ImageField(upload_to='users/avatars/%Y/%m/%d', blank=True, null=True, verbose_name='аватар',
                               help_text='выберите аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payments(models.Model):
    """ Платежи пользователя
    """
    PAYMENT_METHOD_CHOICES = (
        ('card', 'карта'),
        ('cash', 'наличные'),
    )
    PAINT_CHOICES = (
        ('course', 'курс'),
        ('lesson', 'урок'),
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payments',
                             verbose_name='пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты', help_text='дата оплаты')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='payments',
                                     verbose_name='тип контента', help_text='тип контента')
    object_id = models.PositiveIntegerField(verbose_name='идентификатор контента')
    content_object = GenericForeignKey('content_type', 'object_id')
    payment_amount = models.IntegerField(verbose_name='сумма платежа', help_text='введите сумму платежа')
    payment_method = models.CharField(verbose_name='способ оплаты', max_length=100,
                                      choices=PAYMENT_METHOD_CHOICES,
                                      help_text='выберите способ оплаты')

    def __str__(self):
        return f'Платеж пользователя {self.user} на {self.payment_date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-id']

        # Пользователь не может иметь несколько платежей одного типа
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'content_type', 'object_id'],
                name='unique_user_content_type_object_id'
            )
        ]

    def clean(self):
        """ Проверка наличия объекта контента
        """
        if not self.content_object:
            raise ValidationError('Объект контента не может быть пустым')

    def save(self, *args, **kwargs):
        """ Сохранение объекта контента
        """
        if self.content_object and not isinstance(self.content_object, (Course, Lesson)):
            raise ValueError('Тип контента должен быть Course или Lesson')
        super().save(*args, **kwargs)
