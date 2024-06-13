from django.contrib import admin

from users.models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'group', 'first_name', 'last_name',)

    def group(self, obj):
        return obj.groups.first()

    group.short_description = 'группа'


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'user', 'name_curse', 'name_lesson', 'payment_method', 'payment_date',
                    'payment_amount')

    def name_curse(self, obj):
        if obj.content_type.model == 'course':
            return obj.content_object.name
        return None

    def name_lesson(self, obj):
        if obj.content_type.model == 'lesson':
            return obj.content_object.name
        return None

    name_curse.short_description = 'курс'
    name_lesson.short_description = 'урок'
