from rest_framework import permissions
from users.models import User


class ReadOnlyOrAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user:
            return True
        if request.user.is_superuser:
            return True
        if request.user.role in [User.ADMIN, User.MODERATOR]:
            return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False
