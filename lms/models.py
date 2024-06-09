from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='courses/preview/%Y/%m/%d', blank=True, null=True,
                                      verbose_name='превью курса', help_text='выберите превью курса')
    description = models.TextField(verbose_name='описание курса', blank=True, null=True,
                                   help_text='введите описание курса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='lessons/preview/%Y/%m/%d', blank=True, null=True,
                                      verbose_name='превью урока', help_text='выберите превью урока')
    description = models.TextField(verbose_name='описание урока', blank=True, null=True,
                                   help_text='введите описание урока')
    link_to_video = models.URLField(verbose_name='ссылка на видео', help_text='введите ссылку на видео')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
