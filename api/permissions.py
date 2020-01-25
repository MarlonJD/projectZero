from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    """
    Permission class that allow user or admin to access
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser or request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    """
    Permission class that allow only admin
    """
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_staff
