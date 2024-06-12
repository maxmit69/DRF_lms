from django.contrib import admin

from users.models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'payment_method', 'payment_date', 'payment_amount')
