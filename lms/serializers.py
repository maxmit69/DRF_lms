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
    # lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
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
