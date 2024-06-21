import stripe
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from users.models import User, Payments
from users.serializers import UserSerializer
from users.services import create_stripe_product_and_price, create_stripe_session, get_stripe_session_status
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(self.request.data.get('password'))
        user.save()


class UserListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateApiView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyApiView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


def get_model_from_content_type(content_type):
    """ Получение модели по типу контента
    """
    if content_type == 'course':
        return Course
    elif content_type == 'lesson':
        return Lesson
    elif content_type == 'subscription':
        return Subscription
    else:
        raise ValueError(f'Неизвестный тип контента: {content_type}')


class CreatePaymentView(APIView):
    def post(self, request):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')

        if not content_type:
            return Response({'error': 'Тип контента не указан.'}, status=status.HTTP_400_BAD_REQUEST)

        if not object_id:
            return Response({'error': 'ID объекта не указан.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_model = get_model_from_content_type(content_type)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_object = content_model.objects.get(id=object_id)
        except content_model.DoesNotExist:
            return Response({'error': 'Объект контента не найден.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        content_type_instance = ContentType.objects.get_for_model(content_object)

        # Проверка на существующий платеж
        existing_payment = Payments.objects.filter(
            user=user,
            content_type=content_type_instance,
            object_id=object_id
        ).first()

        if existing_payment:
            # Обновление существующего платежа
            existing_payment.payment_amount = int(content_object.price * 100)
            existing_payment.save()
            return Response({'message': 'Платеж обновлен.',
                             'payment_url': existing_payment.payment_url}, status=status.HTTP_200_OK)

        # Создание продукта и цены в Stripe
        stripe_product_id, stripe_price_id = create_stripe_product_and_price(content_object)

        # Создание платежа в нашей системе
        payment = Payments.objects.create(
            user=user,
            content_type=content_type_instance,
            object_id=object_id,
            payment_amount=int(content_object.price * 100),
            payment_method='card',  # Здесь можно указать другой способ оплаты
            stripe_product_id=stripe_product_id,
            stripe_price_id=stripe_price_id
        )

        # Создание сессии оплаты в Stripe
        stripe_session_id, payment_url = create_stripe_session(payment)
        payment.stripe_session_id = stripe_session_id
        payment.payment_url = payment_url
        payment.save()

        return Response({'payment_url': payment_url}, status=status.HTTP_201_CREATED)


class CheckPaymentStatusView(APIView):
    def get(self, request, session_id):
        try:
            session = get_stripe_session_status(session_id)
        except stripe.error.InvalidRequestError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'payment_status': session.payment_status}, status=status.HTTP_200_OK)
