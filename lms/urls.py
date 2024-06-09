from rest_framework import routers
from lms.apps import LmsConfig
from lms import views
from django.urls import path

app_name = LmsConfig.name

router = routers.DefaultRouter()
router.register(r'', views.CourseViewSet)

urlpatterns = [
    path('lesson/', views.LessonListApiView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', views.LessonRetrieveApiView.as_view(), name='lesson-detail'),
    path('lesson/create/', views.LessonCreateApiView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/update/', views.LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', views.LessonDestroyApiView.as_view(), name='lesson-delete'),
]

urlpatterns += router.urls
