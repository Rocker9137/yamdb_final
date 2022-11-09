from rest_framework import permissions


class AuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Редактирование доступно автору или админу."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Редактирование доступно админу."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and (
                request.user.is_superuser or request.user.is_admin
            ))
        )
