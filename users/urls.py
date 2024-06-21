from django.urls import path
from rest_framework.permissions import AllowAny
from .views import CreatePaymentView, CheckPaymentStatusView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.UserCreateApiView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('check-payment-status/<str:session_id>/', CheckPaymentStatusView.as_view(), name='check-payment-status'),
]
