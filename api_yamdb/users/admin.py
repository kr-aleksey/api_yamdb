from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


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


admin.site.register(User, CustomUserAdmin)
# Яков:
# На мой взгляд декоратор @admin.register выглядит более лаконично и приятно,
# чем вызов функции admin.site.register в коце файла.
# Так мы точно не забудем добавить модель в админку.
