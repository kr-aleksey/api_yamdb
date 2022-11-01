from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
