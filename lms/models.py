from django.db import models
from django.conf import settings


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название курса', help_text='введите название курса')
    preview_image = models.ImageField(upload_to='courses/preview/%Y/%m/%d', blank=True, null=True,
                                      verbose_name='превью курса', help_text='выберите превью курса')
    description = models.TextField(verbose_name='описание курса', blank=True, null=True,
                                   help_text='введите описание курса')
    owner = models.ForeignKey('users.User', related_name='courses', on_delete=models.SET_NULL,
                              blank=True, null=True, help_text='выберите автора курса', verbose_name='автор курса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name='курс')
    name = models.CharField(max_length=100, verbose_name='название урока', help_text='введите название урока')
    preview_image = models.ImageField(upload_to='lessons/preview/%Y/%m/%d', blank=True, null=True,
                                      verbose_name='превью урока', help_text='выберите превью урока')
    description = models.TextField(verbose_name='описание урока', blank=True, null=True,
                                   help_text='введите описание урока')
    link_to_video = models.URLField(verbose_name='ссылка на видео', help_text='введите ссылку на видео')
    owner = models.ForeignKey('users.User', related_name='lessons', on_delete=models.SET_NULL, blank=True, null=True,
                              help_text='выберите автора урока', verbose_name='автор урока')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    """ Подписки пользователя
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions',
                             verbose_name='пользователь')
    course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, related_name='subscriptions',
                               verbose_name='курс', help_text='курс')
    subscription_date = models.DateTimeField(auto_now_add=True, verbose_name='дата подписки', help_text='дата подписки')

    def __str__(self):
        return f'{self.user} подписан на {self.course}'

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['-id']
