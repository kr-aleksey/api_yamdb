from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class UserAPIPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'update':
            return False
        user = request.user
        if view.action in ['list', 'create', 'destroy']:
            return bool(user and user.is_authenticated and user.is_admin())
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin() or request.user == obj
