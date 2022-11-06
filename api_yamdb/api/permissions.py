from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user or request.user.role in [
            User.MODERATOR,
            User.ADMIN
        ]:
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


class UserAPIPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if view.action in ['list', 'create', 'destroy']:
            return bool(user and user.is_authenticated and user.is_admin())
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin()
