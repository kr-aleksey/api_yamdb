from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
# Яков:
# По канону в начале должно быть Is.
# А вообще мы тут врем. Имя пермиссии говорит, что доступ дан только автору, а по факту получается не так.
# Я бы сделал 3 тонких пермисси под каждую роль и объединял их с помощью or/and.

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user or request.user.role in [
            User.MODERATOR,
            User.ADMIN
        ]:
        # Яков:
        # У нашего юзера есть методы, которые проверяют является ли юзер админом/модератором.
        # Давайте использовать их.

        # Алексей:
        # Сори, я в понедельник добавил методы модели User и неуспел о них сказать: is_admin() и is_moderator()

            return True
        return False


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == User.ADMIN

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.role == User.ADMIN
        )
