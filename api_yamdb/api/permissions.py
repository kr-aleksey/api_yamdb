from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user or request.user.role in [
            'admin',
            'moderator'
        ]:
            return True
        return False


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'
