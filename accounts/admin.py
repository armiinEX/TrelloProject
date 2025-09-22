# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Preferences", {"fields": ("preferred_language",)}),
    )
    list_display = ("username", "email", "preferred_language", "is_staff")