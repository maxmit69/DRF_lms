from rest_framework import serializers


def validate_link_to_video(value):
    """ Валидация ссылки на видео
    """
    if not value.startswith('https://www.youtube.com/watch?v='):
        raise serializers.ValidationError('Ссылка должна начинаться с "https://www.youtube.com/watch?v="')
