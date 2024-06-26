# Generated by Django 5.0.6 on 2024-06-13 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_alter_lesson_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(help_text='введите название курса', max_length=100, verbose_name='название курса'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='lms.course', verbose_name='курс'),
        ),
    ]
