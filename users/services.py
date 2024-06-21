import stripe
from django.conf import settings
from .models import Payments

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product_and_price(content_object):
    # Создание продукта в Stripe
    stripe_product = stripe.Product.create(
        name=content_object.name,
        description=getattr(content_object, 'description', '')
    )

    # Создание цены в Stripe
    stripe_price = stripe.Price.create(
        product=stripe_product.id,
        unit_amount=int(content_object.price * 100),
        currency='rub'
    )

    return stripe_product.id, stripe_price.id


def create_stripe_session(payment: Payments):
    # Создание Stripe-сессии для оплаты
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': payment.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=settings.STRIPE_SUCCESS_URL,  # Ссылка, на которую будет перенаправлен пользователь после оплаты
        cancel_url=settings.STRIPE_CANCEL_URL,  # Ссылка, на которую будет перенаправлен пользователь при отмене оплаты
    )

    return session.id, session.url


def get_stripe_session_status(stripe_session_id):
    # Получение информации о Stripe-сессии
    session = stripe.checkout.Session.retrieve(stripe_session_id)
    return session
