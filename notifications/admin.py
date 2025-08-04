from django.contrib import admin
from .models import Tenant, Notification


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_key")
    search_fields = ("name",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "tenant", "created_at")
    list_filter = ("tenant", "created_at")
    search_fields = ("title", "message")

