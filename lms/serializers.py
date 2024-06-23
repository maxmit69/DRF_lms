from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from lms.models import Course, Lesson
from lms.validators import validate_link_to_video
from users.models import Payments
from lms.models import Subscription


class LessonSerializer(ModelSerializer):
    link_to_video = serializers.CharField(validators=[validate_link_to_video])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, obj):
        """ Подписан ли пользователь на курс
        """
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class CourseDetailSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        """ Кол-во уроков в курсе """
        return Lesson.objects.filter(course=obj).count()
        # return obj.lessons.count()


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionsSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def create(self, validated_data):
        """ Создание подписки пользователями"""
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
