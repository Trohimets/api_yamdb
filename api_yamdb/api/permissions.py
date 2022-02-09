from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsRoleAdmin(BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin or user.is_superuser
        )


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or user.is_authenticated and user.is_admin or user.is_superuser
        )


class UserOrNot(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS 