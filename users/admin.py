from django.contrib import admin
from .models import User, UserConfirm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone_number", "email", "gender", "auth_type", "auth_status", "date_joined")
    list_filter = ("gender", "auth_type", "auth_status", "is_active", "is_staff")
    search_fields = ("username", "phone_number", "email")
    date_hierarchy = "date_joined"
    ordering = ("-date_joined",)


@admin.register(UserConfirm)
class UserConfirmAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "user", "expiration_time", "is_confirmed")
    list_filter = ("is_confirmed",)
    search_fields = ("user", "code")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)