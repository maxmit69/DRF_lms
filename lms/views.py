from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from lms.models import Course, Lesson
from lms.paginators import MyPagination
from lms.permissions import IsModer, IsOwner, IsUser
from lms import serializers
from lms.models import Subscription
from lms.tasks import send_update_email
from users.models import Payments


# Курсы _____________________________________________________________________
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = MyPagination

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CourseDetailSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'retrieve']:
            self.permission_classes = (~IsModer | IsOwner,)
        if self.action in ['create', 'destroy']:
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_update(self, serializer):
        course = serializer.save()
        subscriptions = Subscription.objects.filter(course=course)
        for subscription in subscriptions:
            send_update_email.delay(subscription.user.email, course.name)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Если у экземпляра объекта есть кэш предварительно загруженных объектов, этот кэш очищается
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# Уроки___________________________________________________________________
class LessonListApiView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated,)
    pagination_class = MyPagination

    def get(self, request):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveApiView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (IsModer | IsOwner,)


class LessonCreateApiView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonUpdateApiView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (IsModer | IsOwner,)


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (~IsModer | IsOwner,)


# Платежи___________________________________________________________________
class PaymentsListApiView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = serializers.PaymentsSerializer
    filterset_fields = ('payment_method', 'content_type',)
    ordering_fields = ('payment_date',)


# Подписки________________________________________________________________
class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = serializers.SubscriptionsSerializer

    def get_permissions(self):
        """ Права для действий """
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """ Права для создания подписки """
        user = self.request.user
        if 'user' in self.request.data and self.request.data['user'] != user.id:
            raise PermissionDenied('У вас нет прав для создания подписки')
        serializer.save(user=user)

    def perform_destroy(self, instance):
        """ Права для удаления подписки """
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied('У вас нет прав для удаления подписки')

    @action(detail=False, methods=['post'], url_path='subscribe')
    def subscribe(self, request):
        """Подписка на курс
        """
        user = request.user
        course_id = request.data.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        if created:
            return Response({'message': 'Подписка оформлена'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Вы уже подписаны'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request):
        """Отмена подписки на курс
        """
        user = request.user
        course_id = request.data.get('course_id')
        try:
            subscription = Subscription.objects.get(user=user, course_id=course_id)
        except Subscription.DoesNotExist:
            return Response({'error': 'Подписка не найдена'}, status=status.HTTP_404_NOT_FOUND)

        subscription.delete()
        return Response({'message': 'Подписка отменена'}, status=status.HTTP_200_OK)
