from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsRoleAdmin(BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.admin or user.is_superuser
        )


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.has_perm('reviews.delete_genre')
        )
