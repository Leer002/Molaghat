from django.contrib import admin

from .models import Gateway, Payment


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable', 'updated_time']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'gateway', 'price', 'status', 'phone_number', 'created_time']
    list_filter = ['status', 'gateway']
    search_fields = ['user__username', 'phone_number']