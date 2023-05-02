from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            request.user.is_authenticated and request.user.is_moderator
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.user.is_authenticated and request.user.is_moderator
            or request.user.is_staff
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            request.user.is_authenticated and request.user.is_user
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
