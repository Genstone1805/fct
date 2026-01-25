from rest_framework.permissions import BasePermission


# class CustomPermission(BasePermission):
    # """
    # Permission class that checks if the user has 'booking' permission.
    # """
    # message = "You do not have permission to access booking resources."

    # def has_permission(self, request, view):
    #     if not request.user or not request.user.is_authenticated:
    #         return False
    #     if request.user.is_superuser:
    #         return True
    #     if 'booking' in request.user.user_permissions:
    #         return True
    #     if 'driver' in request.user.user_permissions:
    #         return True
    #     if 'routes' in request.user.user_permissions:
    #         return True
    #     if 'routes' in request.user.user_permissions:
    #         return True
    #     return False

class HasBookingPermission(BasePermission):
    """
    Permission class that checks if the user has 'booking' permission.
    """
    message = "You do not have permission to access booking resources."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Admin users have all permissions
        if request.user.is_superuser:
            return True
        return 'booking' in request.user.user_permissions


class HasDriverPermission(BasePermission):
    """
    Permission class that checks if the user has 'drivers' permission.
    """
    message = "You do not have permission to access driver resources."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Admin users have all permissions
        if request.user.is_superuser:
            return True
        return 'drivers' in request.user.user_permissions


class HasRoutePermission(BasePermission):
    """
    Permission class that checks if the user has 'routes' permission.
    """
    message = "You do not have permission to access route resources."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Admin users have all permissions
        if request.user.is_superuser:
            return True
        return 'routes' in request.user.user_permissions


class IsAdminUser(BasePermission):
    """
    Permission class that checks if the user has 'adminUsers' permission or is_staff.
    """
    message = "You do not have admin access."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or 'adminUsers' in request.user.user_permissions


class HasAnyPermission(BasePermission):
    """
    Permission class that checks if the user has at least one permission.
    """
    message = "You do not have any permissions assigned."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return len(request.user.user_permissions) > 0
