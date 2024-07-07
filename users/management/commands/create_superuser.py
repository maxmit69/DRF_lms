from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Команда для создания суперпользователя python manage.py create_superuser'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@localhost.com',
            first_name='admin2',
            last_name='admin2',
        )

        user.set_password('1234qwer')
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        self.stdout.write(self.style.SUCCESS('Суперпользователь создан'))
