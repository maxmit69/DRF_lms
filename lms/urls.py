from rest_framework import routers
from lms.apps import LmsConfig
from lms import views
from django.urls import path

app_name = LmsConfig.name

router = routers.DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='course')
router.register(r'subscription', views.SubscriptionViewSet, basename='subscription')

urlpatterns = [
    # Уроки
    path('lesson/', views.LessonListApiView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', views.LessonRetrieveApiView.as_view(), name='lesson-detail'),
    path('lesson/create/', views.LessonCreateApiView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/update/', views.LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', views.LessonDestroyApiView.as_view(), name='lesson-delete'),
    # Платежи
    path('payment/', views.PaymentsListApiView.as_view(), name='payments-list'),
]

urlpatterns += router.urls
