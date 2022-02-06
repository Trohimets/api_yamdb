from rest_framework.permissions import BasePermission


class IsRoleAdmin(BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.admin or user.is_superuser
        )
