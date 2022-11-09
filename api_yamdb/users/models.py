from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    REQUIRED_FIELDS = ['email']

    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    email = models.EmailField(
        'Email',
        unique=True
    )
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

    class Meta:
        ordering = ('username', )

    @property
    def is_admin(self):
        """Возвращает True, если пользователь
        исполняет роль "Администратор". Иначе False."""
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Возвращает True, если пользователь
         исполняет роль "Модератор". Иначе False."""
        return self.role == self.MODERATOR
