from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {'fields': ('username', 'password')}
        ),
        (
            'Персональные данные',
            {'fields': ('first_name', 'last_name', 'email')}
        ),
        (
            'Права',
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'role'),
            }
        ),
        (
            'Даты',
            {'fields': ('last_login', 'date_joined')}
        ),
    )
