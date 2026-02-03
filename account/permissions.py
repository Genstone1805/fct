from django.conf import settings
from rest_framework.permissions import BasePermission


# class HasRoutesAPIKey(BasePermission):
#     """
#     Permission class that requires a valid API key in the request header.
#     Expects header: API-KEY: <key>
#     """
#     message = "Invalid or missing API key."

#     def has_permission(self, request, view):
#         api_key = request.META.get('HTTP_API_KEY', '')
#         expected_key = getattr(settings, 'API_KEY', '')

#         if not expected_key:
#             return False

#         return api_key == expected_key


class HasRoutesAPIKey(BasePermission):
    message = "Invalid or missing API key."

    def has_permission(self, request, view):
        # 🔍 Print all headers sent by the client
        print("=== Incoming Headers ===")
        for key, value in request.headers.items():
            print(f"{key}: {value}")

        api_key = request.headers.get("Api-Key")
        expected_key = getattr(settings, "API_KEY", None)

        if not expected_key:
            return False

        return api_key == expected_key



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
    message = "You do not have permission to access route resources."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Admin users have all permissions
        if request.user.is_superuser:
            return True
        return 'routes' in request.user.user_permissions

class HasVehiclePermission(BasePermission):
    message = "You do not have permission to access route resources."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Admin users have all permissions
        if request.user.is_superuser:
            return True
        return 'vehicles' in request.user.user_permissions


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
