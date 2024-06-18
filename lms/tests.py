from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson, Subscription
from django.contrib.auth.models import Group

User = get_user_model()


class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        self.moder_user = User.objects.create_user(email='moder@example.com', password='moder123', phone='88005553535',
                                                   city='Moscow')
        self.regular_user = User.objects.create_user(email='user@example.com', password='user123', phone='88005584535',
                                                     city='Moscow')
        self.regular_user2 = User.objects.create_user(email='user2@example.com', password='user123',
                                                      phone='88045584535',
                                                      city='Moscow')
        moderator_group, created = Group.objects.get_or_create(name='moderator')
        self.moder_user.groups.add(moderator_group)

        self.course = Course.objects.create(name='Test Course', description='Test Description')
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Test Content', course=self.course,
                                            owner=self.regular_user, link_to_video='https://www.youtube.com/watch?v=')

        self.new_lesson_data = {'name': 'New Lesson', 'course': self.course.id,
                                'link_to_video': 'https://www.youtube.com/watch?v='}

        self.lesson_list_url = reverse('lms:lesson-list')
        self.lesson_detail_url = reverse('lms:lesson-detail', args=[self.lesson.id])
        self.lesson_create_url = reverse('lms:lesson-create')
        self.lesson_update_url = reverse('lms:lesson-update', args=[self.lesson.id])
        self.lesson_delete_url = reverse('lms:lesson-delete', args=[self.lesson.id])

    def test_create_lesson_as_moder(self):
        """ Модератор не может создавать уроки
        """
        self.client.force_authenticate(user=self.moder_user)
        response = self.client.post(self.lesson_create_url, self.new_lesson_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_as_regular_user(self):
        """ Авторизованный пользователь может создавать уроки
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.lesson_create_url, self.new_lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lesson(self):
        """ Авторизованный пользователь может получить информацию о своем уроке
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson_as_owner(self):
        """ Владелец может изменять свои уроки
        """
        self.client.force_authenticate(user=self.regular_user)
        update_data = {'name': 'Updated Lesson', 'description': 'Updated Content', 'course': self.course.id,
                       'link_to_video': 'https://www.youtube.com/watch?v='}
        response = self.client.put(self.lesson_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')
        self.assertEqual(self.lesson.description, 'Updated Content')

    def test_update_lesson_as_other_user(self):
        """ Другой пользователь не может изменять чужие уроки """
        self.client.force_authenticate(user=self.regular_user2)
        update_data = {'name': 'Updated Lesson', 'description': 'Updated Content', 'course': self.course.id,
                       'link_to_video': 'https://www.youtube.com/watch?v='}
        response = self.client.put(self.lesson_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.lesson.refresh_from_db()
        self.assertNotEqual(self.lesson.name, 'Updated Lesson')
        self.assertNotEqual(self.lesson.description, 'Updated Content')

    def test_delete_lesson_as_owner(self):
        """ Владелец может удалять свои уроки
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_as_moder(self):
        """ Модератор не может удалять уроки
        """
        self.client.force_authenticate(user=self.moder_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_delete_lesson_as_other_user(self):
        """ Другой пользователь не может удалять чужие уроки
        """
        self.client.force_authenticate(user=self.regular_user2)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseSubscriptionTestCase(APITestCase):

    def setUp(self):
        self.moder_user = User.objects.create_user(email='moder@example.com', password='moder123', phone='1238457890',
                                                   city='Moscow')
        self.regular_user = User.objects.create_user(email='user@example.com', password='user123', phone='1234447890',)

        self.course = Course.objects.create(name='Subscribable Course', description='Description')
        self.subscribe_url = reverse('lms:subscription-subscribe')
        self.unsubscribe_url = reverse('lms:subscription-unsubscribe')

    def test_subscribe_to_course_as_authenticated_user(self):
        """ Авторизованный пользователь может подписаться на курс
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.subscribe_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.regular_user, course=self.course).exists())

    def test_subscribe_to_course_as_anonymous_user(self):
        """ Неавторизованный пользователь не может подписаться на курс
        """
        response = self.client.post(self.subscribe_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsubscribe_from_course_as_authenticated_user(self):
        """ Авторизованный пользователь может отменить подписку на курс
        """
        self.client.force_authenticate(user=self.regular_user)
        self.client.post(self.subscribe_url, {'course_id': self.course.id})  # подписываемся
        response = self.client.post(self.unsubscribe_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.regular_user, course=self.course).exists())

    def test_unsubscribe_from_course_as_anonymous_user(self):
        """ Неавторизованный пользователь не может отменить подписку на курс
        """
        response = self.client.post(self.unsubscribe_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
