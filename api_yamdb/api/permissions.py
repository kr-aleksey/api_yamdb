from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if view.action in ['list', 'create']:
            return bool(user and user.is_authenticated and user.is_admin())
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        a = request.user.is_admin()
        b = request.user == obj
        c = a or b
        return c

